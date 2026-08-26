"""Gera o PDF de slides da apresentação (widescreen 16:9)."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "slides_apresentacao.pdf"
W, H = 1280, 720

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("Sans", FONT))
pdfmetrics.registerFont(TTFont("SansBold", FONT_B))

GREEN = HexColor("#0B6E4F")
GREEN_DARK = HexColor("#0A3D2E")
GREEN_SOFT = HexColor("#E6F2EC")
TEAL = HexColor("#1A9B73")
INK = HexColor("#12352B")
MUTED = HexColor("#4A6B60")
BG = HexColor("#F7FBF9")
CARD = HexColor("#FFFFFF")
LINE = HexColor("#C5DDD2")


def wrap(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def band(c: canvas.Canvas) -> None:
    c.setFillColor(GREEN)
    c.rect(0, 0, 18, H, fill=1, stroke=0)
    c.setFillColor(BG)
    c.rect(18, 0, W - 18, H, fill=1, stroke=0)


def footer(c: canvas.Canvas, n: int, total: int, cue: str) -> None:
    c.setFillColor(GREEN)
    c.rect(18, 0, W - 18, 42, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Sans", 10)
    c.drawString(48, 16, "Tech Challenge Fase 4  ·  POSTECH FIAP")
    c.drawRightString(W - 36, 16, f"{cue}   {n}/{total}")


def heading(c: canvas.Canvas, title: str, y: float = 640) -> None:
    c.setFillColor(GREEN)
    c.setFont("SansBold", 32)
    c.drawString(56, y, title)
    c.setStrokeColor(TEAL)
    c.setLineWidth(4)
    c.line(56, y - 14, 280, y - 14)


def bullets(c: canvas.Canvas, items: list[str], x: float, y: float, size: float = 18, gap: float = 42) -> None:
    for item in items:
        c.setFillColor(TEAL)
        c.circle(x, y + 6, 5, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Sans", size)
        lines = wrap(c, item, "Sans", size, W - x - 80)
        for i, line in enumerate(lines):
            c.drawString(x + 22, y - i * (size + 6), line)
        y -= gap + max(0, len(lines) - 1) * (size + 6)


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    c.setFillColor(CARD)
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 12, fill=1, stroke=1)


def kpi(c: canvas.Canvas, x: float, y: float, w: float, h: float, value: str, label: str) -> None:
    card(c, x, y, w, h)
    c.setFillColor(GREEN)
    c.setFont("SansBold", 28)
    c.drawCentredString(x + w / 2, y + h / 2 + 8, value)
    c.setFillColor(MUTED)
    c.setFont("Sans", 12)
    c.drawCentredString(x + w / 2, y + 22, label)


def slide_title(c: canvas.Canvas, n: int, total: int) -> None:
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, W, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Sans", 14)
    c.drawString(64, 640, "POSTECH FIAP  ·  Tech Challenge Fase 4")
    c.setFont("SansBold", 40)
    c.drawString(64, 520, "Sistema de apoio à decisão médica")
    c.setFont("SansBold", 28)
    c.drawString(64, 470, "Predição do nível de obesidade")
    c.setStrokeColor(TEAL)
    c.setLineWidth(4)
    c.line(64, 440, 320, 440)
    c.setFont("Sans", 16)
    c.drawString(64, 380, "Visão hospitalar  ·  diagnóstico preditivo  ·  painel analítico")
    c.setFont("Sans", 14)
    c.drawString(64, 80, "Data Viz & Production Models")
    c.drawRightString(W - 64, 80, f"{n}/{total}")


def slide_problem(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "O problema no hospital")
    bullets(
        c,
        [
            "Obesidade é doença crônica e multifatorial — genética, ambiente e hábitos.",
            "A triagem manual é lenta e o olhar de risco varia de profissional para profissional.",
            "A equipe precisa de um primeiro filtro padronizado, em linguagem clínica.",
            "O sistema não substitui o médico: apoia a decisão e reduz o tempo da primeira avaliação.",
        ],
        72,
        540,
    )
    footer(c, n, total, "Bloco 1  ·  0:00–1:00")


def slide_proposal(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "O que foi entregue")
    boxes = [
        ("Diagnóstico", "Formulário clínico e nível estimado de obesidade, com IMC e confiança do modelo."),
        ("Painel", "Visão populacional para a gestão: hábitos, histórico familiar e atividade física."),
        ("Produção", "Aplicação no Streamlit Cloud. Extra: API FastAPI e containers Docker."),
    ]
    x = 56
    for title, text in boxes:
        card(c, x, 180, 370, 360)
        c.setFillColor(GREEN)
        c.roundRect(x + 24, 480, 14, 14, 3, fill=1, stroke=0)
        c.setFont("SansBold", 20)
        c.drawString(x + 48, 480, title)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        y = 430
        for line in wrap(c, text, "Sans", 14, 310):
            c.drawString(x + 24, y, line)
            y -= 22
        x += 390
    footer(c, n, total, "Bloco 1  ·  0:00–1:00")


def slide_cohort(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "A coorte")
    kpi(c, 56, 380, 270, 160, "2.111", "pacientes")
    kpi(c, 350, 380, 270, 160, "7", "níveis de peso")
    kpi(c, 644, 380, 270, 160, "17", "variáveis clínicas")
    kpi(c, 938, 380, 270, 160, "0", "nulos na base")
    c.setFillColor(INK)
    c.setFont("Sans", 16)
    c.drawString(
        56,
        300,
        "Classes relativamente equilibradas: o modelo não fica cego para um nível raro.",
    )
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(56, 250, "Abaixo do peso  →  peso normal  →  sobrepeso I e II  →  obesidade I, II e III")
    footer(c, n, total, "Bloco 2  ·  1:00–2:10")


def slide_insights(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Três achados que mudam conduta")
    rows = [
        ("81,8%", "Histórico familiar", "O “sim” se concentra nos níveis mais graves. Anamnese familiar é sinal de risco."),
        ("59,0%", "Sedentários", "A atividade física cai conforme a obesidade sobe. Exercício entra no plano, não no discurso."),
        ("88,4%", "Alimentos calóricos", "Hábito dominante da coorte. Nutrição precisa entrar cedo, não só depois do rótulo."),
    ]
    y = 500
    for value, title, text in rows:
        card(c, 56, y - 20, 1168, 100)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 26)
        c.drawString(80, y + 30, value)
        c.setFont("SansBold", 16)
        c.drawString(250, y + 36, title)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        c.drawString(250, y + 8, text)
        y -= 120
    footer(c, n, total, "Bloco 2  ·  1:00–2:10")


def slide_pipeline(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Como o modelo foi construído")
    steps = [
        ("1", "Dados clínicos", "Biometria, hábitos, família e rotina."),
        ("2", "IMC de apoio", "Peso dividido pela altura ao quadrado."),
        ("3", "Preparação", "Números na mesma escala; categorias em colunas."),
        ("4", "Dois modelos", "Random Forest e Gradient Boosting."),
    ]
    x = 56
    for num, title, text in steps:
        card(c, x, 280, 280, 260)
        c.setFillColor(GREEN)
        c.circle(x + 36, 500, 16, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("SansBold", 14)
        c.drawCentredString(x + 36, 494, num)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 16)
        c.drawString(x + 24, 440, title)
        c.setFillColor(INK)
        c.setFont("Sans", 13)
        yy = 400
        for line in wrap(c, text, "Sans", 13, 230):
            c.drawString(x + 24, yy, line)
            yy -= 20
        x += 300
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(56, 210, "Leitura honesta: IMC pesa — e isso é coerente com a OMS. Hábitos mostram por onde intervir.")
    footer(c, n, total, "Bloco 3  ·  2:10–3:20")


def slide_result(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Resultado no conjunto de teste")
    card(c, 56, 220, 560, 340)
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(88, 510, "Mínimo da disciplina")
    c.setFillColor(INK)
    c.setFont("SansBold", 48)
    c.drawString(88, 430, "75%")
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(88, 360, "Modelo campeão  ·  Gradient Boosting")
    c.setFillColor(GREEN)
    c.setFont("SansBold", 72)
    c.drawString(88, 260, "98,35%")

    card(c, 660, 220, 560, 340)
    c.setFillColor(INK)
    c.setFont("SansBold", 18)
    c.drawString(692, 500, "Comparação")
    lines = [
        "Gradient Boosting    98,35% no teste",
        "Random Forest           97,87% no teste",
        "Validação cruzada     97,5%  ±  0,8%",
        "",
        "Os dois passam do critério. O campeão",
        "foi serializado e vai para a aplicação.",
    ]
    c.setFont("Sans", 15)
    y = 450
    for line in lines:
        c.setFillColor(INK if line else MUTED)
        c.drawString(692, y, line)
        y -= 32
    footer(c, n, total, "Bloco 3  ·  2:10–3:20")


def slide_demo(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Demonstração — paciente de triagem")
    c.setFillColor(INK)
    c.setFont("Sans", 16)
    c.drawString(56, 580, "A partir daqui, a tela é o aplicativo. Paciente simulado:")
    left = [
        ("Gênero / idade", "Masculino, 42 anos"),
        ("Altura / peso", "1,70 m  ·  120 kg"),
        ("IMC esperado", "≈ 41,5  ·  obesidade III (OMS)"),
        ("Família / calóricos", "Sim  ·  Sim"),
    ]
    right = [
        ("Atividade física", "Nenhuma"),
        ("Água / telas", "Baixa  ·  mais de 5 h"),
        ("Transporte", "Automóvel"),
        ("Ação", "Executar diagnóstico clínico"),
    ]
    y = 480
    for (a, b), (d, e) in zip(left, right):
        card(c, 56, y - 10, 560, 70)
        card(c, 660, y - 10, 560, 70)
        c.setFillColor(MUTED)
        c.setFont("Sans", 11)
        c.drawString(80, y + 32, a)
        c.drawString(684, y + 32, d)
        c.setFillColor(INK)
        c.setFont("SansBold", 16)
        c.drawString(80, y + 8, b)
        c.drawString(684, y + 8, e)
        y -= 88
    footer(c, n, total, "Bloco 4  ·  3:20–5:00  ·  ir ao app")


def slide_readout(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Como ler o resultado")
    items = [
        ("Diagnóstico predito", "O nível estimado em sete classes, em português."),
        ("IMC e faixa OMS", "Métrica clínica ao lado da predição, para o médico cruzar as duas leituras."),
        ("Gráfico de confiança", "Probabilidade em cada nível. Útil quando o caso está na fronteira."),
        ("Limite ético", "Apoio à triagem. Conduta — dieta, exame, encaminhamento — é da equipe."),
    ]
    y = 500
    for title, text in items:
        card(c, 56, y - 16, 1168, 88)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 16)
        c.drawString(88, y + 36, title)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        c.drawString(88, y + 8, text)
        y -= 108
    footer(c, n, total, "Bloco 4  ·  3:20–5:00")


def slide_panel(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Painel para a gestão")
    kpi(c, 56, 430, 270, 130, "2.111", "pacientes")
    kpi(c, 350, 430, 270, 130, "81,8%", "histórico familiar")
    kpi(c, 644, 430, 270, 130, "59,0%", "sedentários")
    kpi(c, 938, 430, 270, 130, "88,4%", "consumo calórico")
    c.setFillColor(INK)
    c.setFont("Sans", 16)
    bullets(
        c,
        [
            "Onde investir prevenção: atividade física, ultraprocessados e pergunta de histórico familiar na recepção.",
            "Diagnóstico e painel no mesmo endereço: a equipe não troca de ferramenta.",
        ],
        72,
        360,
        size=16,
        gap=48,
    )
    footer(c, n, total, "Bloco 5  ·  5:00–5:50  ·  ir ao painel")


def slide_impact(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Impacto no atendimento")
    bullets(
        c,
        [
            "Primeira conversa no ambulatório mais curta e padronizada em sete níveis.",
            "Insumo para campanha interna de nutrição e atividade física.",
            "Próximo passo no hospital: validar em pacientes da unidade e, se fizer sentido, integrar a API ao prontuário.",
        ],
        72,
        500,
        size=18,
        gap=56,
    )
    footer(c, n, total, "Bloco 6  ·  5:50–6:30")


def slide_links(c: canvas.Canvas, n: int, total: int) -> None:
    band(c)
    heading(c, "Onde acessar")
    card(c, 56, 380, 560, 180)
    card(c, 660, 380, 560, 180)
    c.setFillColor(MUTED)
    c.setFont("Sans", 13)
    c.drawString(88, 520, "Aplicação e painel")
    c.drawString(692, 520, "Código-fonte")
    c.setFillColor(GREEN)
    c.setFont("SansBold", 18)
    c.drawString(88, 470, "avaliapeso.streamlit.app")
    c.setFont("SansBold", 16)
    c.drawString(692, 470, "github.com/DELSOBRINHO")
    c.setFillColor(INK)
    c.setFont("Sans", 14)
    c.drawString(88, 430, "Aba Diagnóstico e aba Painel analítico")
    c.drawString(692, 430, "fase4-postech  ·  branch main")
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(56, 300, "O extra de produção (API FastAPI + Docker) está no repositório. O link da banca é o aplicativo na nuvem.")
    footer(c, n, total, "Bloco 6  ·  5:50–6:30")


def slide_end(c: canvas.Canvas, n: int, total: int) -> None:
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, W, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("SansBold", 40)
    c.drawCentredString(W / 2, 400, "Obrigado")
    c.setFont("Sans", 18)
    c.drawCentredString(W / 2, 340, "Fico à disposição da banca.")
    c.setStrokeColor(TEAL)
    c.setLineWidth(3)
    c.line(W / 2 - 80, 310, W / 2 + 80, 310)
    c.setFont("Sans", 13)
    c.drawCentredString(W / 2, 250, "avaliapeso.streamlit.app")
    c.drawCentredString(W / 2, 220, "github.com/DELSOBRINHO/fase4-postech")
    c.setFont("Sans", 11)
    c.drawCentredString(W / 2, 80, f"{n}/{total}")


def main() -> None:
    pages = [
        slide_title,
        slide_problem,
        slide_proposal,
        slide_cohort,
        slide_insights,
        slide_pipeline,
        slide_result,
        slide_demo,
        slide_readout,
        slide_panel,
        slide_impact,
        slide_links,
        slide_end,
    ]
    total = len(pages)
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Apresentação — sistema preditivo de obesidade")
    c.setAuthor("Tech Challenge Fase 4")
    for i, fn in enumerate(pages, start=1):
        fn(c, i, total)
        c.showPage()
    c.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
