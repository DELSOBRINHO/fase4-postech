# Roteiro do vídeo de apresentação (5 a 7 minutos)

Duração-alvo: **5–7 minutos** (limite oficial: 4–10). Linguagem: **visão de negócio hospitalar**, não tutorial de código.

## Minuto 1 — Introdução e problema de negócio

- Apresentação pessoal / grupo.
- Papel: cientista de dados contratado pelo hospital.
- Problema: obesidade como doença crônica multifatorial; triagem manual é lenta e desigual.
- Promessa da entrega: um sistema de apoio à decisão que classifica o nível de obesidade e um painel para a gestão clínica.

**Frase de fechamento:** “O objetivo não é substituir o médico; é reduzir o tempo de triagem e padronizar o primeiro olhar sobre o risco.”

## Minuto 2 — Dados e insights clínicos

Mostrar 2–3 gráficos do painel (não a tabela cru):

1. Histórico familiar concentra casos graves.
2. Sedentarismo (`FAF`) acompanha níveis mais altos.
3. Consumo frequente de alimentos calóricos (`FAVC`) é o hábito dominante da coorte.

Citar o tamanho da base: **2.111** pacientes, **7** níveis, classes equilibradas o suficiente para treinar sem reamostragem agressiva.

## Minuto 3 — Engenharia de atributos e modelagem

- Pipeline Scikit-Learn: `ColumnTransformer` (padronização + one-hot) dentro de um `Pipeline`.
- IMC calculado como métrica clínica de apoio.
- Comparação Random Forest vs. Gradient Boosting; campeão serializado.
- Resultado: acurácia de teste **acima de 94%**, muito acima do mínimo de **75%**.
- Uma frase honesta: altura e peso (via IMC) são fortes, mas hábitos explicam o contexto da intervenção.

Não abrir o notebook inteiro. Um slide ou 10 segundos no `classification_report` bastam.

## Minutos 4 e 5 — Demonstração do Streamlit

Roteiro de cliques (gravar tela cheia, narrar em voz de produto):

1. Abrir **Diagnóstico preditivo**.
2. Preencher um paciente de risco (histórico familiar sim, FAVC sim, FAF baixo, IMC elevado).
3. Clicar em **Executar diagnóstico clínico**.
4. Ler a classe predita, o IMC/OMS e o gráfico de probabilidade.
5. Mudar para **Painel analítico e insights**.
6. Passar pelos KPIs e por dois gráficos (histórico familiar e FAF).
7. Fechar com a leitura clínica do rodapé do painel.

## Minuto 6 — Impacto e encerramento

- Triagem mais rápida no ambulatório / endocrinologia / nutrição.
- Painel alimenta campanhas internas (atividade física, redução de ultraprocessados, aconselhamento familiar).
- Próximos passos possíveis: validação prospectiva no hospital, calibração por faixa etária, integração com prontuário.
- Agradecimento e indicação dos links (app, GitHub, vídeo).

## Checklist de gravação

- [ ] Mostrar as duas visões do app (preditivo + dashboard)
- [ ] Falar em benefício clínico, não só em acurácia
- [ ] Evitar jargão (`ColumnTransformer`, `n_estimators`) em excesso; se citar, traduzir
- [ ] Resolução legível; não cobrir KPIs com a cabeça na câmera
- [ ] Duração entre 4 e 10 minutos
