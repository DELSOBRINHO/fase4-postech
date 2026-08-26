# Roteiro falado do vídeo (5 a 7 minutos)

Duração-alvo: **6 minutos** (limite oficial: 4–10).  
Fale como **cientista de dados do hospital**, não como programador.  
Grave a tela do app em https://avaliapeso.streamlit.app/ em tela cheia. Você pode aparecer num canto pequeno; o que precisa ficar legível são os gráficos e o diagnóstico.

**Antes de gravar:** abrir o app, deixar na aba **Diagnóstico preditivo**, zoom do navegador em 100–110%. Ter este texto à frente (teleprompter ou segunda tela).

**Links para citar no fechamento**

- App e painel: https://avaliapeso.streamlit.app/
- Código: https://github.com/DELSOBRINHO/fase4-postech/tree/main

---

## Bloco 1 — Quem sou e qual é o problema (0:00 a 1:00)

**Tela:** capa do app (Diagnóstico preditivo), sem clicar ainda.

**Fale:**

> Olá, eu sou Delmir Bartolomeu Sobrinho, aluno da POSTECH FIAP, fase 4 — Data Viz and Production Models.
>
> Neste Tech Challenge eu atuo como cientista de dados de um hospital. A demanda da equipe médica é clara: apoiar o diagnóstico precoce da obesidade, que é uma doença crônica, multifatorial, e que hoje sobrecarrega a triagem no ambulatório.
>
> O que entregamos não é um substituto do médico. É um sistema de apoio à decisão: o profissional preenche dados do paciente, recebe o nível estimado de obesidade — de abaixo do peso até obesidade tipo III — e a gestão ganha um painel com os fatores de risco da coorte.
>
> Em uma frase: reduzir o tempo da primeira triagem e padronizar o olhar de risco, com linguagem clínica.

**Não fale:** nomes de biblioteca, Git, Docker. Isso fica para o bloco 3, bem curto.

---

## Bloco 2 — Os dados e o que o hospital precisa enxergar (1:00 a 2:10)

**Tela:** clique em **Painel analítico e insights**. Deixe os quatro KPIs visíveis. Role devagar até o gráfico de histórico familiar e o de atividade física.

**Fale (olhando os números na tela):**

> A base tem 2.111 pacientes e sete níveis de peso, relativamente equilibrados. Isso importa porque o modelo não fica cego para uma classe rara.
>
> Três achados que mudam conduta no ambulatório.
>
> Primeiro: cerca de 82% da coorte tem histórico familiar de excesso de peso. Nos gráficos, esse “sim” se concentra nos níveis mais graves. Ou seja: a anamnese familiar não é detalhe — é sinal de risco.
>
> Segundo: quase 60% estão sedentários. A frequência de atividade física cai conforme o nível de obesidade sobe. Campanha de exercício não é discurso; é o padrão que os dados mostram.
>
> Terceiro: o consumo frequente de alimentos muito calóricos aparece em cerca de 88% dos pacientes. É o hábito dominante. Nutrição entra cedo no plano, não só depois do diagnóstico “fechado”.
>
> O IMC separa bem os níveis, como a clínica já espera. O valor do estudo é cruzar o IMC com hábitos: aí o médico sabe *por onde intervir*.

**Clique / role:** KPI → gráfico “Histórico familiar × nível” → boxplot de FAF. Não precisa mostrar todos os oito gráficos.

---

## Bloco 3 — Como o modelo foi feito (sem virar aula de código) (2:10 a 3:20)

**Tela:** pode voltar ao diagnóstico **ou** mostrar 5 segundos do GitHub (`src/train.py` / métricas). Prefira permanecer no app e só narrar.

**Fale:**

> Do lado técnico, montamos uma pipeline única: dados numéricos padronizados, dados categóricos em one-hot, e o IMC calculado como métrica clínica de apoio — peso sobre altura ao quadrado.
>
> Comparamos duas famílias de modelo: Random Forest e Gradient Boosting. O campeão no teste foi o Gradient Boosting, com 98,35% de acerto. O Random Forest ficou em 97,87%. O critério da disciplina era 75%. Passamos com folga.
>
> Uma leitura honesta para a banca médica: altura e peso, via IMC, têm peso grande na classificação — e isso é coerente com a OMS. Os hábitos não “dispensam” o IMC; eles explicam o contexto da intervenção: família, caloria, sedentarismo.
>
> O modelo está em produção no Streamlit Cloud. Como extra de produção, o mesmo modelo também sobe numa API FastAPI e em container Docker, junto com a tela. O link da entrega da disciplina é o aplicativo na nuvem, que é o que o médico usa.

**Se estiver muito longo, corte o parágrafo do extra FastAPI/Docker** (são ~15 segundos).

---

## Bloco 4 — Demo do diagnóstico (3:20 a 5:00) — a parte mais importante

**Tela:** **Diagnóstico preditivo**. Preencha **enquanto fala**. Não leia cada rótulo técnico (FAVC, FAF); traduza.

### Paciente de demonstração (alto risco)

Use estes valores — IMC fica em torno de **41,5** (obesidade tipo III pela OMS):

| Campo | O que selecionar |
| --- | --- |
| Gênero | Masculino |
| Idade | 42 |
| Altura | 1,70 m |
| Peso | 120 kg |
| Histórico familiar | Sim |
| Alimentos muito calóricos | Sim |
| Vegetais | 1 (raro) |
| Refeições | 2 |
| Lanches | Frequentemente |
| Monitora calorias | Não |
| Fumante | Não |
| Água | 1 (menos de 1 L) |
| Atividade física | 0 (nenhuma) |
| Telas | 2 (mais de 5 h) |
| Álcool | Às vezes |
| Transporte | Automóvel |

**Fale enquanto preenche:**

> Vou simular um paciente de 42 anos, 1 metro e 70, 120 quilos. O IMC já dispara para a faixa de obesidade grau III pela referência da OMS. Tem histórico familiar, come muito alimento calórico, quase não se exercita e passa o dia sentado, de carro e em tela.
>
> Isso é o perfil que o ambulatório não pode deixar passar na triagem.

**Clique em Executar diagnóstico clínico.**

**Fale olhando o resultado (adapte se a classe predita for outra; o esperado é obesidade tipo III):**

> O sistema devolve o diagnóstico predito — neste caso, obesidade tipo III — e mostra o IMC calculado, 41,5, alinhado à faixa da OMS.
>
> Ao lado, o gráfico de confiança: o modelo não dá só um rótulo; ele mostra a probabilidade em cada nível. Isso é útil quando o caso está na fronteira entre sobrepeso e obesidade: o médico vê a dúvida, não um número mágico.
>
> De novo: apoio à triagem. A conduta — dieta, exame, encaminhamento — continua sendo da equipe.

Se o gráfico demorar um segundo, fique em silêncio; não peça desculpa.

---

## Bloco 5 — Demo do painel para a gestão (5:00 a 5:50)

**Tela:** **Painel analítico e insights**. Mostre KPIs e **dois** gráficos. Role até a leitura clínica do rodapé.

**Fale:**

> Para a gestão hospitalar, a outra aba responde: onde investir prevenção?
>
> Quatro números de prontuário populacional: 2.111 pacientes, 82% com histórico familiar, 59% sedentários, 88% com consumo calórico frequente.
>
> Se eu sou coordenador de endocrinologia ou de nutrição, eu não começo um programa genérico. Eu começo por atividade física e por redução de ultraprocessados, e eu treino a recepção a perguntar histórico familiar.
>
> O painel está no mesmo endereço do diagnóstico. A equipe não troca de ferramenta.

---

## Bloco 6 — Impacto, próximos passos e fechamento (5:50 a 6:30)

**Tela:** volte ao diagnóstico **ou** deixe o painel. No final, mostre a URL na barra do navegador.

**Fale:**

> Na prática, isso encurta a primeira conversa no ambulatório, padroniza a classificação em sete níveis e gera insumo para campanha interna.
>
> Próximos passos, se o hospital adotar: validar o modelo em pacientes reais da unidade, calibrar por faixa etária e, no extra de produção, integrar a API FastAPI ao prontuário — o Docker já empacota API e tela juntas.
>
> O aplicativo em produção está em avaliapeso ponto streamlit ponto app. O código-fonte está no GitHub, repositório fase4-postech, branch main.
>
> Obrigado. Fico à disposição da banca.

---

## Se faltar tempo (corte nesta ordem)

1. Extra FastAPI/Docker no bloco 3  
2. “Próximos passos” no bloco 6  
3. Um dos três insights do bloco 2 (fique com família + FAF)

## Se sobrar tempo (até 8–9 min)

- Mostre http://localhost:8000/docs **só se já estiver aberto** (Swagger `/predict`). Uma frase: “o mesmo modelo também responde em API, para integrar com outro sistema.”  
- Não instale Docker ao vivo.

## Checklist na hora de gravar

- [ ] Duas abas: Diagnóstico **e** Painel  
- [ ] Paciente de 120 kg / 1,70 m preenchido na gravação (não só narrado)  
- [ ] Falar “apoio à decisão”, nunca “o app diagnostica sozinho”  
- [ ] Dizer 98,35% e o mínimo de 75%  
- [ ] Dizer 2.111 pacientes  
- [ ] Mostrar a URL `avaliapeso.streamlit.app`  
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
