# Plano de desenvolvimento com checklist

Este plano desdobra o [plano mestre](01-plano-mestre.md) em fases executáveis. Cada item é um critério verificável. Itens concluídos na implementação inicial já aparecem marcados.

**Como usar:** atualize os checkboxes a cada entrega parcial. Não avance uma fase se o critério de aceite da fase anterior estiver vermelho.

---

## Visão das fases

```text
Fase 0  Documentação e estrutura
   ↓
Fase 1  Dados e dicionário
   ↓
Fase 2  EDA médica (notebook)
   ↓
Fase 3  Pipeline + treino + serialização
   ↓
Fase 4  Aplicação Streamlit (diagnóstico + dashboard)
   ↓
Fase 5  README, submissão e qualidade
   ↓
Fase 6  Deploy Streamlit Cloud  →  vídeo  →  upload na plataforma
```

---

## Fase 0 — Documentação e estrutura do repositório

**Objetivo:** deixar o repositório navegável e o plano rastreável.

- [x] Criar pasta `documentacao/`
- [x] Versionar o plano mestre (`01-plano-mestre.md`)
- [x] Versionar este plano de desenvolvimento com checklist
- [x] Incluir enunciado, dicionário, roteiro de vídeo e guia de deploy
- [x] Criar árvore `data/`, `notebooks/`, `src/`, `app/`
- [x] Adicionar `.gitignore` e `requirements.txt` (raiz e `app/`)
- [x] Definir branch de trabalho a partir de `main`

**Aceite da fase:** um clone do repositório permite localizar dados, código, app e documentação sem adivinhar caminhos.

---

## Fase 1 — Dados e contrato das colunas

**Objetivo:** congelar o dataset e o significado clínico de cada variável.

- [x] Copiar `Obesity.csv` para `data/` (2.111 linhas, 17 colunas)
- [x] Confirmar coluna alvo `Obesity` com 7 classes
- [x] Documentar dicionário (`04-dicionario-dados.md` + PDF original)
- [x] Listar numéricas vs. categóricas em `src/data_pipeline.py`
- [x] Validar ausência de nulos no arquivo de entrega

**Aceite da fase:** `load_raw_dataset()` falha se faltar coluna obrigatória; o README aponta o dicionário.

---

## Fase 2 — Análise exploratória com visão médica

**Objetivo:** gerar insights que alimentem o dashboard e o roteiro do vídeo.

- [x] Notebook `notebooks/01_eda_analise_medica.ipynb`
- [x] Distribuição do alvo e leitura epidemiológica
- [x] Relação histórico familiar × nível de obesidade
- [x] Relação FAF (atividade física) e FAVC (alimentos calóricos)
- [x] Cálculo e análise do IMC
- [x] Correlações numéricas
- [x] Síntese de insights para a equipe médica

**Aceite da fase:** o painel analítico consegue reproduzir os gráficos-chave da EDA.

---

## Fase 3 — Pipeline de ML, treino e exportação

**Objetivo:** modelo reproduzível, acima de 75% de acurácia, serializado para o app.

- [x] `src/data_pipeline.py` com IMC, `ColumnTransformer` e builders
- [x] `src/train.py` com split estratificado 80/20 e `random_state=42`
- [x] Comparar Random Forest e Gradient Boosting
- [x] Relatório de classificação + matriz de confusão
- [x] Validação cruzada estratificada (5 folds) no treino
- [x] Abortar se acurácia de teste < 75%
- [x] Serializar campeão em `app/model.joblib`
- [x] Persistir métricas em `documentacao/metricas_modelo.json`
- [x] Notebook `notebooks/02_pipeline_modelagem.ipynb` documentando a modelagem

**Aceite da fase:** `python -m src.train` grava o modelo e imprime acurácia ≥ 75% (meta: ≥ 94%).

---

## Fase 4 — Aplicação Streamlit

**Objetivo:** duas visões de negócio na mesma aplicação.

### 4.1 Diagnóstico preditivo

- [x] Formulário biométrico (gênero, idade, altura, peso)
- [x] Hábitos alimentares (FAVC, FCVC, NCP, CAEC, SCC, histórico familiar)
- [x] Estilo de vida (SMOKE, CH2O, FAF, TUE, CALC, MTRANS)
- [x] Inferência com o pipeline serializado
- [x] Exibir classe predita em português
- [x] Exibir IMC e faixa OMS de apoio
- [x] Gráfico de probabilidade por classe
- [x] Disclaimer de apoio à decisão (não substitui consulta)

### 4.2 Painel analítico

- [x] KPIs: n pacientes, histórico familiar, sedentários, FAVC
- [x] Distribuição dos níveis de obesidade
- [x] Histórico familiar × classe
- [x] Boxplots de FAF e CH2O
- [x] FAVC e IMC por classe
- [x] Heatmap de correlação
- [x] Importância de atributos do modelo
- [x] Texto de leitura clínica

### 4.3 Engenharia do app

- [x] Caminhos relativos à raiz (funciona no Cloud e local)
- [x] Cache de modelo (`st.cache_resource`) e dados (`st.cache_data`)
- [x] Tema visual hospitalar (`.streamlit/config.toml`)
- [x] Rótulos da interface em português; valores originais enviados ao modelo

**Aceite da fase:** um usuário leigo da equipe médica consegue preencher o formulário e ler o painel sem conhecer os nomes técnicos das colunas.

---

## Fase 5 — Documentação de produto e qualidade

**Objetivo:** o repositório se explica sozinho para avaliadores e para o deploy.

- [x] `README.md` com problema, estrutura, como treinar e como rodar o app
- [x] `entrega_tech_challenge_fase4.txt` com placeholders dos links
- [x] Roteiro de vídeo (`05-roteiro-video.md`)
- [x] Guia de deploy (`06-guia-deploy-streamlit.md`)
- [x] Enunciado oficial e PDF do dicionário na pasta `documentacao/`

**Aceite da fase:** um avaliador encontra, em menos de dois minutos, acurácia, como rodar e o que falta para a submissão (links de Cloud e vídeo).

---

## Fase 6 — Deploy, vídeo e submissão (pós-código)

Itens de Cloud já publicados; vídeo e upload na plataforma FIAP ainda abertos.

- [x] Criar repositório público (ou garantir visibilidade exigida pela disciplina)
- [x] Publicar o app no Streamlit Cloud (`app/app.py` + `requirements.txt` da raiz)
- [x] Validar diagnóstico e painel na URL de produção (`https://avaliapeso.streamlit.app/`)
- [x] Colar links da aplicação, do painel e do GitHub em `entrega_tech_challenge_fase4.txt`
- [ ] Gravar vídeo de 4–10 min seguindo o roteiro
- [ ] Publicar o vídeo (YouTube ou Loom) em modo acessível ao avaliador
- [ ] Colar o link do vídeo em `entrega_tech_challenge_fase4.txt`
- [ ] Fazer upload do `.txt` (ou `.doc`) na plataforma da FIAP

**Aceite da fase:** os quatro links abrem sem autenticação extra para o avaliador.

---

## Ordem de execução recomendada (código)

1. Congelar dados e dicionário.
2. Implementar `src/data_pipeline.py` e `src/train.py`.
3. Treinar e travar o `model.joblib` no repositório (necessário para o Cloud).
4. Subir `app/app.py` e conferir as duas abas.
5. Materializar os notebooks a partir da mesma pipeline (evitar lógica divergente).
6. Só então publicar no Streamlit Cloud e gravar o vídeo.

---

## Critérios de aceite globais (definição de pronto)

O projeto está pronto para a banca quando **todos** os itens abaixo forem verdadeiros:

| # | Critério | Evidência |
| --- | --- | --- |
| 1 | Pipeline completa de feature engineering + treino | `src/data_pipeline.py`, `src/train.py`, notebook 02 |
| 2 | Acurácia de teste > 75% | `documentacao/metricas_modelo.json` e saída do treino |
| 3 | App preditivo no Streamlit | Aba Diagnóstico em `app/app.py` |
| 4 | Painel analítico com insights médicos | Aba Painel em `app/app.py` |
| 5 | Código no GitHub, estruturado | este repositório |
| 6 | Deploy + painel + repo + vídeo em arquivo de entrega | `entrega_tech_challenge_fase4.txt` |
| 7 | Vídeo 4–10 min com visão de negócio | `05-roteiro-video.md` + link publicado |

---

## Riscos e mitigações

| Risco | Impacto | Mitigação |
| --- | --- | --- |
| Caminho `app/model.joblib` quebra no Cloud | App não sobe | Resolver caminhos via `Path(__file__).parent.parent` |
| Classe customizada no pickle | `joblib.load` falha | Pipeline só com estimadores sklearn; IMC adicionado *antes* do `Pipeline` |
| Vazamento conceitual IMC × rótulo OMS | Banca questionar “o modelo só copia o IMC” | Exibir IMC como apoio clínico, incluir hábitos no modelo e discutir isso no vídeo |
| Dependências divergentes entre treino e Cloud | Inferência inconsistente | Um `requirements.txt` na raiz; versões mínimas pinadas |
| Vídeo só técnico | Perde visão de negócio | Seguir o roteiro minuto a minuto |

---

## Registro de progresso desta implementação

| Data | Entrega |
| --- | --- |
| 2026-08-26 | Estrutura do repositório, documentação, pipeline, app, notebooks e treino inicial |
| 2026-08-26 | Deploy em produção: https://avaliapeso.streamlit.app/ (diagnóstico e painel validados) |
