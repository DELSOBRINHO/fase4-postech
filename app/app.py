"""Aplicação Streamlit: diagnóstico preditivo e painel analítico hospitalar."""

from __future__ import annotations

import os

import joblib
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from repo_path import ROOT, load_project_modules

try:
    ROOT, _pipeline, _inference = load_project_modules()
    CLASS_ORDER = _pipeline.CLASS_ORDER
    LABEL_PT = _pipeline.LABEL_PT
    RISK_LABELS = _pipeline.RISK_LABELS
    add_clinical_features = _pipeline.add_clinical_features
    behavioral_risk_frame = _pipeline.behavioral_risk_frame
    classify_imc = _pipeline.classify_imc
    predict_patient = _inference.predict_patient
except Exception as exc:  # noqa: BLE001
    st.set_page_config(page_title="Erro ao iniciar", layout="wide")
    st.error(f"Falha ao carregar o aplicativo: {type(exc).__name__}: {exc}")
    st.stop()

MODEL_PATH = ROOT / "app" / "model.joblib"
DATA_PATH = ROOT / "data" / "Obesity.csv"
INFERENCE_API_URL = os.getenv("INFERENCE_API_URL", "").rstrip("/")

st.set_page_config(
    page_title="Sistema de Diagnóstico de Obesidade",
    layout="wide",
    page_icon="🏥",
)

GENDER_OPTIONS = {"Feminino": "Female", "Masculino": "Male"}
YES_NO = {"Sim": "yes", "Não": "no"}
CAEC_OPTIONS = {
    "Não": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always",
}
CALC_OPTIONS = {
    "Não bebe": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always",
}
MTRANS_OPTIONS = {
    "Transporte público": "Public_Transportation",
    "Automóvel": "Automobile",
    "A pé": "Walking",
    "Motocicleta": "Motorbike",
    "Bicicleta": "Bike",
}


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Modelo não encontrado. Execute `python -m src.train` na raiz do repositório."
        )
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df = add_clinical_features(df)
    df = behavioral_risk_frame(df)
    df["Obesity_PT"] = df["Obesity"].map(LABEL_PT).fillna(df["Obesity"])
    df["Obesity_PT"] = pd.Categorical(
        df["Obesity_PT"],
        categories=[LABEL_PT[c] for c in CLASS_ORDER],
        ordered=True,
    )
    return df


def render_diagnosis(model) -> None:
    st.title("Sistema de Apoio à Decisão Médica: Predição de Obesidade")
    st.markdown(
        "Preencha os dados clínicos e comportamentais do paciente para obter o "
        "**nível estimado de obesidade**. O resultado é um apoio à triagem e "
        "não substitui avaliação médica presencial."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("1. Dados biométricos")
        gender_label = st.selectbox("Gênero", list(GENDER_OPTIONS.keys()))
        age = st.slider("Idade (anos)", 14, 65, 25)
        height = st.number_input("Altura (m)", min_value=1.40, max_value=2.10, value=1.70, step=0.01)
        weight = st.number_input("Peso (kg)", min_value=35.0, max_value=180.0, value=70.0, step=0.5)

    with col2:
        st.subheader("2. Hábitos alimentares")
        family_label = st.selectbox("Histórico familiar de excesso de peso?", list(YES_NO.keys()))
        favc_label = st.selectbox("Consome alimentos muito calóricos com frequência (FAVC)?", list(YES_NO.keys()))
        fcvc = st.slider("Frequência de consumo de vegetais (1 = raro, 3 = sempre)", 1, 3, 2)
        ncp = st.slider("Número de refeições principais por dia", 1, 4, 3)
        caec_label = st.selectbox("Lanches entre refeições (CAEC)", list(CAEC_OPTIONS.keys()), index=1)
        scc_label = st.selectbox("Monitora calorias diárias (SCC)?", list(YES_NO.keys()), index=1)

    with col3:
        st.subheader("3. Estilo de vida e rotina")
        smoke_label = st.selectbox("Fumante?", ["Não", "Sim"])
        ch2o = st.slider("Consumo de água (1 = <1 L, 2 = 1–2 L, 3 = >2 L)", 1, 3, 2)
        faf = st.slider("Atividade física semanal (0 = nenhuma, 3 = 5x+)", 0, 3, 1)
        tue = st.slider("Tempo em telas por dia (0 = 0–2 h, 2 = >5 h)", 0, 2, 1)
        calc_label = st.selectbox("Consumo de álcool (CALC)", list(CALC_OPTIONS.keys()), index=1)
        mtrans_label = st.selectbox("Meio de transporte habitual", list(MTRANS_OPTIONS.keys()))

    st.markdown("---")
    if not st.button("Executar diagnóstico clínico", type="primary"):
        imc_preview = weight / (height**2)
        st.caption(
            f"IMC pré-calculado com os dados atuais: **{imc_preview:.2f} kg/m²** "
            f"({classify_imc(imc_preview)} pela referência da OMS)."
        )
        return

    payload = {
        "Gender": GENDER_OPTIONS[gender_label],
        "Age": float(age),
        "Height": float(height),
        "Weight": float(weight),
        "family_history": YES_NO[family_label],
        "FAVC": YES_NO[favc_label],
        "FCVC": float(fcvc),
        "NCP": float(ncp),
        "CAEC": CAEC_OPTIONS[caec_label],
        "SMOKE": YES_NO[smoke_label],
        "CH2O": float(ch2o),
        "SCC": YES_NO[scc_label],
        "FAF": float(faf),
        "TUE": float(tue),
        "CALC": CALC_OPTIONS[calc_label],
        "MTRANS": MTRANS_OPTIONS[mtrans_label],
    }
    try:
        if INFERENCE_API_URL:
            response = requests.post(
                f"{INFERENCE_API_URL}/predict",
                json=payload,
                timeout=20,
            )
            response.raise_for_status()
            result = response.json()
        else:
            result = predict_patient(payload, model=model)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Falha na inferência: {exc}")
        return

    prediction = result["prediction"]
    probabilities = [result["probabilities"][c] for c in result["classes"]]
    classes = result["classes"]
    imc = float(result["imc"])
    label_pt = result.get("prediction_pt") or LABEL_PT.get(prediction, prediction.replace("_", " "))

    left, right = st.columns([1, 1])
    with left:
        st.success(f"Diagnóstico predito: **{label_pt}**")
        st.info(
            f"**IMC calculado:** {imc:.2f} kg/m²  \n"
            f"**Referência OMS (IMC):** {classify_imc(imc)}"
        )
        risk = result.get("behavioral_risk") or {}
        if risk:
            risk_text = (
                f"**{risk.get('label', 'Hábitos')}** — o grau de obesidade segue o IMC (OMS); "
                "os hábitos alimentares, o histórico familiar e o estilo de vida entram neste "
                "perfil de risco para a conduta."
            )
            level = risk.get("level")
            if level == "alto":
                st.warning(risk_text)
            elif level == "baixo":
                st.success(risk_text)
            else:
                st.info(risk_text)
        st.caption(
            "Em obesidade tipo I/II/III o diagnóstico acompanha as faixas da OMS "
            "(30 / 35 / 40 kg/m²). O modelo de machine learning continua sendo treinado "
            "com todas as variáveis; hábitos não rebaixam o grau quando o IMC já define a classe."
        )
    with right:
        prob_df = pd.DataFrame(
            {
                "Classe": [LABEL_PT.get(c, c) for c in classes],
                "Probabilidade (%)": [float(p) * 100 for p in probabilities],
            }
        ).sort_values("Probabilidade (%)", ascending=True)
        fig_prob = px.bar(
            prob_df,
            x="Probabilidade (%)",
            y="Classe",
            orientation="h",
            title="Confiança do modelo por nível",
            color="Probabilidade (%)",
            color_continuous_scale="Teal",
        )
        fig_prob.update_layout(yaxis_title="", xaxis_title="Probabilidade (%)")
        st.plotly_chart(fig_prob, width="stretch")


def feature_importance_frame(model, df: pd.DataFrame) -> pd.DataFrame | None:
    classifier = model.named_steps.get("classifier")
    preprocessor = model.named_steps.get("preprocessor")
    if classifier is None or not hasattr(classifier, "feature_importances_"):
        return None
    try:
        names = preprocessor.get_feature_names_out()
    except Exception:
        return None
    importances = classifier.feature_importances_
    if len(names) != len(importances):
        return None
    data = pd.DataFrame({"feature": names, "importance": importances})
    return data.sort_values("importance", ascending=False)


def render_dashboard(model, df: pd.DataFrame) -> None:
    st.title("Painel analítico de fatores de risco da obesidade")
    st.markdown(
        "Visão epidemiológica da coorte hospitalar (n = {:,}) para apoiar "
        "protocolos de triagem, educação nutricional e prevenção.".format(len(df))
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total de pacientes", f"{len(df):,}".replace(",", "."))
    k2.metric(
        "Com histórico familiar",
        f"{(df['family_history'] == 'yes').mean() * 100:.1f}%",
    )
    k3.metric("Sedentários (FAF ≤ 1)", f"{(df['FAF'] <= 1).mean() * 100:.1f}%")
    k4.metric(
        "Consumo frequente calórico",
        f"{(df['FAVC'] == 'yes').mean() * 100:.1f}%",
    )

    st.subheader("Perfis de risco comportamental")
    st.caption(
        "Mesma leitura do diagnóstico individual: histórico familiar, alimentação, "
        "atividade física, telas, álcool e transporte. O grau de obesidade continua "
        "seguindo o IMC (OMS); aqui a equipe vê onde concentrar prevenção."
    )
    risk_order = [
        RISK_LABELS["alto"],
        RISK_LABELS["moderado"],
        RISK_LABELS["baixo"],
    ]
    risk_color = {
        RISK_LABELS["alto"]: "#C0392B",
        RISK_LABELS["moderado"]: "#D68910",
        RISK_LABELS["baixo"]: "#1A9B73",
    }
    share = df["risk_label"].value_counts(normalize=True)
    r1, r2, r3 = st.columns(3)
    r1.metric("Risco elevado", f"{share.get(RISK_LABELS['alto'], 0) * 100:.1f}%")
    r2.metric("Risco moderado", f"{share.get(RISK_LABELS['moderado'], 0) * 100:.1f}%")
    r3.metric("Menor risco", f"{share.get(RISK_LABELS['baixo'], 0) * 100:.1f}%")

    p1, p2 = st.columns(2)
    with p1:
        fig_risk = px.histogram(
            df,
            x="risk_label",
            color="risk_label",
            title="Pacientes por perfil de risco",
            category_orders={"risk_label": risk_order},
            color_discrete_map=risk_color,
        )
        fig_risk.update_layout(
            xaxis_title="",
            yaxis_title="Pacientes",
            showlegend=False,
        )
        st.plotly_chart(fig_risk, width="stretch")
    with p2:
        fig_risk_class = px.histogram(
            df,
            x="Obesity_PT",
            color="risk_label",
            barmode="stack",
            title="Perfil de risco × nível de obesidade",
            category_orders={
                "Obesity_PT": [LABEL_PT[c] for c in CLASS_ORDER],
                "risk_label": risk_order,
            },
            color_discrete_map=risk_color,
            labels={"risk_label": "Perfil de risco"},
        )
        fig_risk_class.update_layout(xaxis_title="", yaxis_title="Pacientes")
        st.plotly_chart(fig_risk_class, width="stretch")

    g1, g2 = st.columns(2)
    with g1:
        fig_dist = px.histogram(
            df,
            x="Obesity_PT",
            title="Distribuição dos níveis de obesidade",
            color="Obesity_PT",
        )
        fig_dist.update_layout(xaxis_title="", yaxis_title="Pacientes", showlegend=False)
        st.plotly_chart(fig_dist, width="stretch")
    with g2:
        fig_fam = px.histogram(
            df,
            x="Obesity_PT",
            color="family_history",
            barmode="group",
            title="Histórico familiar × nível de obesidade",
            labels={"family_history": "Histórico familiar"},
        )
        fig_fam.update_layout(xaxis_title="", yaxis_title="Pacientes")
        st.plotly_chart(fig_fam, width="stretch")

    g3, g4 = st.columns(2)
    with g3:
        fig_act = px.box(
            df,
            x="Obesity_PT",
            y="FAF",
            color="Obesity_PT",
            title="Frequência de atividade física (FAF) por nível",
        )
        fig_act.update_layout(xaxis_title="", showlegend=False)
        st.plotly_chart(fig_act, width="stretch")
    with g4:
        fig_water = px.box(
            df,
            x="Obesity_PT",
            y="CH2O",
            color="Obesity_PT",
            title="Consumo de água (CH2O) por nível",
        )
        fig_water.update_layout(xaxis_title="", showlegend=False)
        st.plotly_chart(fig_water, width="stretch")

    g5, g6 = st.columns(2)
    with g5:
        fig_favc = px.histogram(
            df,
            x="Obesity_PT",
            color="FAVC",
            barmode="group",
            title="Consumo frequente de alimentos calóricos (FAVC)",
            labels={"FAVC": "FAVC"},
        )
        fig_favc.update_layout(xaxis_title="", yaxis_title="Pacientes")
        st.plotly_chart(fig_favc, width="stretch")
    with g6:
        fig_imc = px.box(
            df,
            x="Obesity_PT",
            y="IMC",
            color="Obesity_PT",
            title="IMC por nível de obesidade",
        )
        fig_imc.update_layout(xaxis_title="", showlegend=False)
        st.plotly_chart(fig_imc, width="stretch")

    st.subheader("Correlações e importância das variáveis")
    c1, c2 = st.columns(2)
    with c1:
        num_cols = ["Age", "Height", "Weight", "IMC", "FCVC", "NCP", "CH2O", "FAF", "TUE"]
        corr = df[num_cols].corr(numeric_only=True)
        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Matriz de correlação (variáveis numéricas)",
            aspect="auto",
        )
        st.plotly_chart(fig_corr, width="stretch")
    with c2:
        imp = feature_importance_frame(model, df)
        if imp is None:
            st.info("Importância de atributos indisponível para este modelo.")
        else:
            top = imp.head(12).iloc[::-1]
            fig_imp = px.bar(
                top,
                x="importance",
                y="feature",
                orientation="h",
                title="Importância dos atributos (modelo campeão)",
                color="importance",
                color_continuous_scale="Teal",
            )
            fig_imp.update_layout(yaxis_title="", xaxis_title="Importância")
            st.plotly_chart(fig_imp, width="stretch")

    st.markdown(
        """
**Leitura clínica rápida**
- Histórico familiar de excesso de peso concentra-se nos níveis mais altos de obesidade.
- Baixa frequência de atividade física (FAF) acompanha classes de maior gravidade.
- Consumo frequente de alimentos calóricos (FAVC) é majoritário na coorte e se associa a classes elevadas.
- O painel de **perfis de risco** (elevado / moderado / menor risco) resume hábitos da coorte para priorizar prevenção; o grau I/II/III no paciente individual segue o IMC.
        """
    )


def main() -> None:
    model = load_model()
    df = load_data()

    st.sidebar.title("Navegação clínica")
    page = st.sidebar.radio(
        "Selecione a visão:",
        ["Diagnóstico preditivo", "Painel analítico e insights"],
    )
    st.sidebar.markdown("---")
    inference_mode = (
        f"Inferência via API FastAPI (`{INFERENCE_API_URL}`)"
        if INFERENCE_API_URL
        else "Inferência local (modelo serializado)"
    )
    st.sidebar.caption(
        "Tech Challenge Fase 4 — POSTECH FIAP  \n"
        "Ferramenta de apoio à triagem hospitalar.  \n"
        f"{inference_mode}"
    )

    if page == "Diagnóstico preditivo":
        render_diagnosis(model)
    else:
        render_dashboard(model, df)


if __name__ == "__main__":
    main()
