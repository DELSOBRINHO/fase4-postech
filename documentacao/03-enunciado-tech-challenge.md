# Enunciado — Tech Challenge Fase 4

Fonte: documento oficial POSTECH *Tech Challenge Fase 04 — Data Analytics* (PDF em `enunciado_tech_challenge_fase4.pdf`).

## Contexto

O Tech Challenge engloba os conhecimentos obtidos em todas as disciplinas da fase. A atividade, em princípio, deve ser desenvolvida em grupo e é obrigatória (corresponde a 90% da nota final).

## O problema

Você foi contratado como cientista de dados de um hospital e tem o desafio de desenvolver um modelo de Machine Learning para auxiliar médicos e médicas a prever se uma pessoa pode ter obesidade.

A obesidade é uma condição médica caracterizada pelo acúmulo excessivo de gordura corporal, a ponto de prejudicar a saúde. É cada vez mais prevalente no mundo, em todas as idades e classes sociais. As causas são multifatoriais: genética, ambiente e comportamento.

Utilizando a base `obesity.csv`, deve-se desenvolver um **modelo preditivo** e um **sistema preditivo** para apoiar a tomada de decisão da equipe médica no diagnóstico da obesidade.

## Requisitos avaliados

- Pipeline de machine learning demonstrando feature engineering e treinamento do modelo.
- Modelo com assertividade acima de 75%.
- Deploy do modelo em uma aplicação preditiva utilizando Streamlit.
- Visão analítica em um painel com os principais insights do estudo para a equipe médica.
- Compartilhar, em arquivo `.doc` ou `.txt` para upload na plataforma:
  - link da aplicação no Streamlit;
  - link do painel analítico;
  - link do repositório GitHub com todo o código.
- Vídeo de 4 a 10 minutos com a estratégia utilizada e a apresentação do sistema preditivo. A visão do sistema **e** a do dashboard devem ser apresentadas em **visão de negócio**.

## Observação do enunciado sobre o dicionário

O PDF oficial lista a variável de tempo em telas como `TER`. No arquivo de dados e no dicionário complementar a coluna se chama **`TUE`** (*Time using electronic devices*). Esta implementação segue o nome real da coluna no CSV: `TUE`.

A coluna alvo aparece no enunciado como `Obesity_level`; no CSV o nome é **`Obesity`**.
