# Roteiro do vídeo — um texto por slide

Duração-alvo: **6 minutos** (limite oficial: 4–10).  
Fale como **cientista de dados do hospital**, não como programador.

**Como gravar:** abra só o PDF `documentacao/slides_apresentacao.pdf` em tela cheia (modo apresentação). Avance um slide, leia o texto da faixa inferior (o mesmo parágrafo abaixo), avance. **Não abra o Streamlit** — as telas do aplicativo já estão nos slides.

**Links para citar nos slides 7, 11 e 12**

- App e painel: https://avaliapeso.streamlit.app/
- Código: https://github.com/DELSOBRINHO/fase4-postech/tree/main

---

## Slide 1 — Capa

**Tela:** título do sistema.

> Olá, eu sou Delmir Bartolomeu Sobrinho. Este é o sistema preditivo hospitalar de classificação da obesidade, desenvolvido no Tech Challenge da fase 4 da POSTECH FIAP.

---

## Slide 2 — O problema no hospital

**Tela:** doença crônica, triagem desigual, apoio (não substituto).

> Atuo como cientista de dados de um hospital. A obesidade é crônica e multifatorial. A triagem hoje é lenta e o olhar de risco varia. O objetivo é padronizar o primeiro filtro, sem substituir o médico.

---

## Slide 3 — Entregas da disciplina

**Tela:** lista das entregas oficiais.

> As entregas da disciplina estão neste aplicativo: pipeline de machine learning, modelo acima de setenta e cinco por cento, sistema preditivo no Streamlit, painel analítico, repositório no GitHub e este vídeo em visão de negócio.

---

## Slide 4 — O aplicativo (formulário)

**Tela:** captura da visão Diagnóstico preditivo.

> O aplicativo tem duas visões. Nesta, o profissional preenche dados biométricos, hábitos alimentares e estilo de vida. O IMC já aparece como referência clínica. Em seguida, executa o diagnóstico.

---

## Slide 5 — Exemplo de diagnóstico

**Tela:** captura do resultado (obesidade tipo II, IMC 41,52).

> Paciente de quarenta e dois anos, um metro e setenta, cento e vinte quilos. O sistema prediz obesidade tipo dois, com IMC de quarenta e um e meio. A OMS, só pelo IMC, apontaria tipo três. O gráfico mostra a confiança em cada nível.

---

## Slide 6 — Como a equipe lê o resultado

**Tela:** classe predita, IMC/OMS, confiança, limite clínico.

> O médico lê três coisas: a classe predita, o IMC com a faixa da OMS e a probabilidade. Quando as duas leituras divergem, vale revisar o contexto comportamental. Continua sendo apoio à triagem.

---

## Slide 7 — Painel analítico (gestão)

**Tela:** captura dos KPIs (2.111 pacientes; 81,8%; 59%; 88,4%).

> A segunda visão é o painel da gestão. São dois mil cento e onze pacientes. Oitenta e dois por cento com histórico familiar, cinquenta e nove por cento sedentários, oitenta e oito por cento com consumo calórico frequente. Diagnóstico e painel no mesmo endereço.

---

## Slide 8 — Hábitos que mudam a conduta

**Tela:** captura dos gráficos de atividade física, água, calorias e IMC.

> Três achados. Histórico familiar se concentra nos níveis graves. Atividade física cai quando a obesidade sobe. Alimento calórico é o hábito dominante. O IMC separa os níveis; os hábitos dizem por onde intervir.

---

## Slide 9 — Pipeline de machine learning

**Tela:** dados → IMC → preparação → modelos.

> A pipeline padroniza números, transforma categorias e calcula o IMC como métrica de apoio. Comparamos Random Forest e Gradient Boosting. O mesmo pré-processamento segue até a aplicação.

---

## Slide 10 — Assertividade do modelo

**Tela:** 75% exigido versus 98,35% no teste.

> O critério da disciplina era setenta e cinco por cento. O Gradient Boosting chegou a noventa e oito vírgula trinta e cinco no teste. O Random Forest, noventa e sete vírgula oitenta e sete. O campeão foi serializado e é este que o aplicativo usa.

---

## Slide 11 — Produção e extras

**Tela:** Streamlit Cloud, GitHub, FastAPI + Docker (extra).

> O deploy oficial é o Streamlit Cloud: avaliapeso ponto streamlit ponto app. O código está no GitHub, branch main. Como extra de produção, o mesmo modelo sobe em API FastAPI e em Docker, junto com a tela.

---

## Slide 12 — Impacto e encerramento

**Tela:** triagem, prevenção, próximos passos.

> Na prática, a primeira triagem fica mais curta e padronizada. O painel alimenta prevenção. Obrigado. Fico à disposição da banca.

---

## Se faltar tempo (corte nesta ordem)

1. Frase do extra FastAPI/Docker no slide 11  
2. “Próximo passo no hospital” no slide 12  
3. Um dos três achados no slide 8 (fique com família + atividade física)

## Checklist na hora de gravar

- [ ] Só o PDF em tela cheia — sem abrir o app  
- [ ] Ler a faixa de texto de cada slide (ou este roteiro; o texto é o mesmo)  
- [ ] Falar “apoio à decisão”, nunca “o app diagnostica sozinho”  
- [ ] Dizer 98,35% e o mínimo de 75%  
- [ ] Dizer 2.111 pacientes  
- [ ] Dizer a URL `avaliapeso.streamlit.app` (slides 7 e 11)  
- [ ] No exemplo, falar **obesidade tipo II** (não tipo III — a OMS pelo IMC é que aponta tipo III)  
- [ ] Duração entre 4 e 10 minutos (alvo 6)  
- [ ] Sem música alta; microfone perto da boca  

## Texto de descrição do YouTube / Loom (cole depois)

```text
Tech Challenge Fase 4 — FIAP POSTECH
Sistema preditivo hospitalar de diagnóstico de obesidade
Delmir Bartolomeu Sobrinho

Aplicação: https://avaliapeso.streamlit.app/
Repositório: https://github.com/DELSOBRINHO/fase4-postech/tree/main
```
