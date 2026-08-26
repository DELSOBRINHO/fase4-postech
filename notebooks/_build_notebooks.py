#!/usr/bin/env python3
"""Gera os notebooks de EDA e modelagem."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"


def md(cell: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(cell.strip())


def code(cell: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(cell.strip() + "\n")


def write(name: str, cells: list[nbf.NotebookNode]) -> None:
    nb = nbf.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
    )
    path = NB_DIR / name
    nbf.write(nb, path)
    print(f"wrote {path}")


def eda_cells() -> list[nbf.NotebookNode]:
    return [
        md(
            """
# 01 — Análise exploratória médica

Visão epidemiológica da coorte hospitalar (`data/Obesity.csv`) para apoiar a equipe clínica.
O dicionário completo está em `documentacao/04-dicionario-dados.md`.
            """
        ),
        code(
            """
from pathlib import Path
import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ROOT = Path.cwd()
if not (ROOT / "data" / "Obesity.csv").exists():
    ROOT = Path.cwd().parent
sys.path.insert(0, str(ROOT))

from src.data_pipeline import LABEL_PT, add_clinical_features, load_raw_dataset

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", 20)

df = add_clinical_features(load_raw_dataset(ROOT / "data" / "Obesity.csv"))
df["Obesity_PT"] = df["Obesity"].map(LABEL_PT)
print(df.shape)
df.head()
            """
        ),
        md("## Qualidade e distribuição do alvo"),
        code(
            """
print("Nulos por coluna:\\n", df.isna().sum())
print("\\nDistribuição do alvo:")
print(df["Obesity_PT"].value_counts())
print("\\nEstatísticas numéricas:")
df.describe().T
            """
        ),
        code(
            """
order = list(LABEL_PT.values())
plt.figure(figsize=(9, 4))
sns.countplot(data=df, x="Obesity_PT", order=order, hue="Obesity_PT", legend=False)
plt.xticks(rotation=25, ha="right")
plt.title("Distribuição dos níveis de obesidade")
plt.xlabel("")
plt.tight_layout()
            """
        ),
        md(
            """
## Insights clínicos prioritários

Três eixos que o painel do Streamlit reproduz: histórico familiar, atividade física e consumo calórico.
            """
        ),
        code(
            """
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
sns.countplot(data=df, x="Obesity_PT", hue="family_history", order=order, ax=axes[0])
axes[0].set_title("Histórico familiar")
axes[0].tick_params(axis="x", rotation=25)
sns.boxplot(data=df, x="Obesity_PT", y="FAF", order=order, ax=axes[1])
axes[1].set_title("Atividade física (FAF)")
axes[1].tick_params(axis="x", rotation=25)
sns.countplot(data=df, x="Obesity_PT", hue="FAVC", order=order, ax=axes[2])
axes[2].set_title("Alimentos calóricos (FAVC)")
axes[2].tick_params(axis="x", rotation=25)
for ax in axes:
    ax.set_xlabel("")
plt.tight_layout()
            """
        ),
        md("## IMC como métrica clínica de apoio"),
        code(
            """
print(df["IMC"].describe())
plt.figure(figsize=(9, 4.5))
sns.boxplot(data=df, x="Obesity_PT", y="IMC", order=order)
plt.xticks(rotation=25, ha="right")
plt.title("IMC por nível de obesidade")
plt.xlabel("")
plt.tight_layout()
            """
        ),
        code(
            """
num_cols = ["Age", "Height", "Weight", "IMC", "FCVC", "NCP", "CH2O", "FAF", "TUE"]
plt.figure(figsize=(8, 6))
sns.heatmap(df[num_cols].corr(numeric_only=True), annot=True, fmt=".2f", cmap="RdBu_r")
plt.title("Correlação entre variáveis numéricas")
plt.tight_layout()
            """
        ),
        md(
            """
## Síntese para a equipe médica

- A coorte está relativamente equilibrada nas 7 classes (272–351 pacientes).
- Histórico familiar de excesso de peso é o sinal categórico mais associado aos níveis graves.
- FAF baixo (sedentarismo) e FAVC = yes aparecem com frequência nas classes de obesidade.
- O IMC separa bem os níveis, como esperado pela definição clínica; hábitos explicam o *como intervir*.
- Não há nulos no arquivo de entrega: a pipeline pode ir direto para pré-processamento.
            """
        ),
    ]


def model_cells() -> list[nbf.NotebookNode]:
    return [
        md(
            """
# 02 — Pipeline de modelagem

Treino reproduzível com a mesma lógica de `src/train.py`: IMC, `ColumnTransformer`,
comparação Random Forest vs. Gradient Boosting e serialização do campeão.
            """
        ),
        code(
            """
from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

ROOT = Path.cwd()
if not (ROOT / "data" / "Obesity.csv").exists():
    ROOT = Path.cwd().parent
sys.path.insert(0, str(ROOT))

from src.data_pipeline import (
    LABEL_PT,
    build_model_pipeline,
    candidate_estimators,
    load_raw_dataset,
    split_xy,
)

df = load_raw_dataset(ROOT / "data" / "Obesity.csv")
X, y = split_xy(df)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(X_train.shape, X_test.shape)
print("Atributos:", list(X.columns))
            """
        ),
        md("## Comparação dos candidatos"),
        code(
            """
rows = []
fitted = {}
for name, estimator in candidate_estimators().items():
    pipe = build_model_pipeline(estimator)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, pred)
    fitted[name] = (pipe, pred)
    rows.append({"modelo": name, "acuracia_teste": acc})

cmp = pd.DataFrame(rows).sort_values("acuracia_teste", ascending=False)
display(cmp)
champion_name = cmp.iloc[0]["modelo"]
champion, y_pred = fitted[champion_name]
print("Campeão:", champion_name)
            """
        ),
        code(
            """
print(classification_report(y_test, y_pred, target_names=[LABEL_PT[c] for c in champion.classes_]))
fig, ax = plt.subplots(figsize=(7, 6))
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, display_labels=[LABEL_PT[c] for c in champion.classes_], ax=ax, xticks_rotation=45
)
ax.set_title("Matriz de confusão — conjunto de teste")
plt.tight_layout()
            """
        ),
        md("## Importância dos atributos (se o campeão for baseado em árvores)"),
        code(
            """
clf = champion.named_steps["classifier"]
pre = champion.named_steps["preprocessor"]
if hasattr(clf, "feature_importances_"):
    names = pre.get_feature_names_out()
    imp = (
        pd.DataFrame({"feature": names, "importance": clf.feature_importances_})
        .sort_values("importance", ascending=False)
        .head(15)
    )
    display(imp)
    imp.iloc[::-1].plot.barh(x="feature", y="importance", figsize=(8, 5), legend=False)
    plt.title("Top 15 atributos")
    plt.tight_layout()
            """
        ),
        md("## Serialização para o aplicativo"),
        code(
            """
out = ROOT / "app" / "model.joblib"
out.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(champion, out)
print("Modelo salvo em", out)
print("Acurácia de teste do campeão: {:.2%}".format(accuracy_score(y_test, y_pred)))
            """
        ),
    ]


def main() -> None:
    NB_DIR.mkdir(parents=True, exist_ok=True)
    write("01_eda_analise_medica.ipynb", eda_cells())
    write("02_pipeline_modelagem.ipynb", model_cells())


if __name__ == "__main__":
    main()
