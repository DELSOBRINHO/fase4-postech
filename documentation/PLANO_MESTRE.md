# PLANO MESTRE — Sistema Preditivo de Preço do Petróleo Brent

**Disciplina:** Tech Challenge Fase 4 (Prova Substitutiva) — POSTECH FIAP Data Analytics  
**Papel:** Cientista de Dados Sênior no Setor de Óleo & Gás (Petróleo)  
**Autor:** Delmir Bartolomeu Sobrinho (Professor Bart)

---

## 1. Visão Executiva e Problema de Negócio

O mercado internacional de petróleo bruto (tipo Brent FOB) é marcado por extrema volatilidade decorrente de choques geopolíticos, decisões da OPEP+, crises econômicas globais e dinâmicas de oferta e demanda.

### O Desafio de Negócio

- **Problema:** A oscilação repentina no preço do barril em dólar impacta diretamente o fluxo de caixa, orçamentos de exploração e refino (CAPEX/OPEX), planejamento de hedges financeiros e precificação de combustíveis.
- **Objetivo:** Desenvolver uma solução preditiva de séries temporais para projetar o preço diário do barril Brent em dólar (US$), disponibilizada em uma aplicação interativa (Streamlit) com painel analítico de apoio à diretoria e equipe de trading.

---

## 2. Escopo dos Entregáveis Obrigatórios

1. **Pipeline de Machine Learning / Séries Temporais:**
   - Extração automatizada da série histórica oficial do IPEA Data (série `1650971490` / `EIA366_PBRENT366`).
   - Tratamento de dias não úteis, valores faltantes e ordenação cronológica.
   - Engenharia de atributos temporais (lags de t−1 a t−30, médias móveis e volatilidade).
   - Treinamento e comparação entre modelos de regressão temporal (Prophet, SARIMAX, XGBoost/LightGBM e Random Forest Regressor).
   - Avaliação com métricas adequadas (MAPE, RMSE, MAE e R²) utilizando divisão temporal estrita (*Time Series Split*).
2. **Aplicação Web em Produção (Streamlit Cloud):**
   - Módulo de projeção futura em tempo real (horizontes configuráveis: 7, 15 ou 30 dias úteis).
   - Painel histórico interativo com os grandes choques geopolíticos e econômicos mundiais (Guerra do Golfo, Crise de 2008, Covid-19 em 2020, Conflitos de 2022).
   - Simulador de cenários e sensibilidade financeira.
3. **Repositório GitHub Versionado:**
   - Estrutura profissional e modular com `/data`, `/notebooks`, `/src`, `/app` e documentação.

---

## 3. Arquitetura da Solução Técnica

```text
[ IPEA Data Web Scraping / API ]
              │
              ▼
[ Pipeline de Engenharia & Lags (ETL) ]
              │
              ▼
[ Modelagem Temporal & Validação Cronológica ]
   ├── Prophet (Tendência & Sazonalidade)
   ├── XGBoost / LightGBM / Random Forest (Feature Lagging)
   └── SARIMAX (Baseline Estatístico)
              │
              ▼
[ Seleção do Modelo Campeão (Menor MAPE) & Serialização (.joblib) ]
              │
              ▼
[ Aplicação Streamlit (app/app.py) ]
   ├── Projeção & Simulador em Tempo Real
   ├── Dashboard de Choques Geopolíticos & Volatilidade
   └── Métricas & Confiabilidade do Modelo
```

---

## 4. Métricas de Sucesso e Governança

- **Métrica Principal:** MAPE (Erro Percentual Médio Absoluto) ≤ 5% no curto prazo (horizonte de 7 a 15 dias).
- **Métricas Complementares:** RMSE (penalização de grandes erros em US$) e MAE (erro médio absoluto em dólares).
- **Blindagem de Dados:** Proibição de embaralhamento (*shuffle*); aplicação de validação em janelas expansivas/deslizantes (*Rolling Window Cross-Validation*).
