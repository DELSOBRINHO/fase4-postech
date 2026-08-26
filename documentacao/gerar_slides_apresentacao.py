"""PDF da apresentação (o que aparece no vídeo). Cada slide traz o texto para ler."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets_slides"
OUT = ROOT / "slides_apresentacao.pdf"
W, H = 1280, 720

pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("SansBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

GREEN = HexColor("#0B6E4F")
GREEN_DARK = HexColor("#0A3D2E")
TEAL = HexColor("#1A9B73")
INK = HexColor("#12352B")
MUTED = HexColor("#4A6B60")
BG = HexColor("#F4F8F6")
CARD = HexColor("#FFFFFF")
LINE = HexColor("#C5DDD2")
READ_BG = HexColor("#FBF8EE")
READ_EDGE = HexColor("#D9CFA8")


# Textos lidos em voz alta — iguais aos do roteiro (05-roteiro-video.md).
T1 = (
    "Olá, eu sou Delmir Bartolomeu Sobrinho. Este é o sistema preditivo hospitalar "
    "de classificação da obesidade, desenvolvido no Tech Challenge da fase 4 da POSTECH FIAP."
)
T2 = (
    "Atuo como cientista de dados de um hospital. A obesidade é crônica e multifatorial. "
    "A triagem hoje é lenta e o olhar de risco varia. O objetivo é padronizar o primeiro "
    "filtro, sem substituir o médico."
)
T3 = (
    "As entregas da disciplina estão neste aplicativo: pipeline de machine learning, "
    "modelo acima de setenta e cinco por cento, sistema preditivo no Streamlit, "
    "painel analítico, repositório no GitHub e este vídeo em visão de negócio."
)
T4 = (
    "O aplicativo tem duas visões. Nesta, o profissional preenche dados biométricos, "
    "hábitos alimentares e estilo de vida. O IMC já aparece como referência clínica. "
    "Em seguida, executa o diagnóstico."
)
T5 = (
    "Paciente de quarenta e dois anos, um metro e setenta, cento e vinte quilos. "
    "O sistema prediz obesidade tipo dois, com IMC de quarenta e um e meio. "
    "A OMS, só pelo IMC, apontaria tipo três. O gráfico mostra a confiança em cada nível."
)
T6 = (
    "O médico lê três coisas: a classe predita, o IMC com a faixa da OMS e a probabilidade. "
    "Quando as duas leituras divergem, vale revisar o contexto comportamental. "
    "Continua sendo apoio à triagem."
)
T7 = (
    "A segunda visão é o painel da gestão. São dois mil cento e onze pacientes. "
    "Oitenta e dois por cento com histórico familiar, cinquenta e nove por cento sedentários, "
    "oitenta e oito por cento com consumo calórico frequente. Diagnóstico e painel no mesmo endereço."
)
T8 = (
    "Três achados. Histórico familiar se concentra nos níveis graves. "
    "Atividade física cai quando a obesidade sobe. Alimento calórico é o hábito dominante. "
    "O IMC separa os níveis; os hábitos dizem por onde intervir."
)
T9 = (
    "A pipeline padroniza números, transforma categorias e calcula o IMC como métrica de apoio. "
    "Comparamos Random Forest e Gradient Boosting. O mesmo pré-processamento segue até a aplicação."
)
T10 = (
    "O critério da disciplina era setenta e cinco por cento. O Gradient Boosting chegou a "
    "noventa e oito vírgula trinta e cinco no teste. O Random Forest, noventa e sete vírgula oitenta e sete. "
    "O campeão foi serializado e é este que o aplicativo usa."
)
T11 = (
    "O deploy oficial é o Streamlit Cloud: avaliapeso ponto streamlit ponto app. "
    "O código está no GitHub, branch main. Como extra de produção, o mesmo modelo "
    "sobe em API FastAPI e em Docker, junto com a tela."
)
T12 = (
    "Na prática, a primeira triagem fica mais curta e padronizada. O painel alimenta prevenção. "
    "Obrigado. Fico à disposição da banca."
)


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


def footer(c: canvas.Canvas, n: int, total: int) -> None:
    c.setFillColor(GREEN)
    c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Sans", 10)
    c.drawString(40, 14, "Tech Challenge Fase 4  ·  sistema preditivo de obesidade")
    c.drawRightString(W - 28, 14, f"{n} / {total}")


def read_box(c: canvas.Canvas, text: str, y0: float = 44) -> float:
    """Bloco inferior: texto que se lê no vídeo (sem rótulo de teleprompter)."""
    pad = 16
    x, w = 28, W - 56
    lines = wrap(c, text, "Sans", 15, w - 2 * pad)
    box_h = 22 + len(lines) * 21
    c.setFillColor(READ_BG)
    c.setStrokeColor(READ_EDGE)
    c.setLineWidth(1)
    c.roundRect(x, y0, w, box_h, 8, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont("Sans", 15)
    ty = y0 + box_h - 20
    for line in lines:
        c.drawString(x + pad, ty, line)
        ty -= 21
    return y0 + box_h


def heading(c: canvas.Canvas, title: str) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(0, H - 78, W, 78, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("SansBold", 26)
    c.drawString(40, H - 48, title)


def shot(c: canvas.Canvas, name: str, x: float, y: float, w: float, h: float) -> None:
    path = ASSETS / name
    c.setFillColor(CARD)
    c.setStrokeColor(LINE)
    c.roundRect(x - 4, y - 4, w + 8, h + 8, 8, fill=1, stroke=1)
    c.drawImage(
        ImageReader(str(path)),
        x,
        y,
        width=w,
        height=h,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    c.setFillColor(CARD)
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)


def slide_01(c: canvas.Canvas, n: int, t: int) -> None:
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, W, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Sans", 14)
    c.drawString(56, 620, "POSTECH FIAP  ·  Tech Challenge Fase 4")
    c.setFont("SansBold", 38)
    c.drawString(56, 520, "Sistema preditivo hospitalar")
    c.setFont("SansBold", 28)
    c.drawString(56, 472, "Classificação do nível de obesidade")
    c.setStrokeColor(TEAL)
    c.setLineWidth(4)
    c.line(56, 444, 300, 444)
    c.setFont("Sans", 16)
    c.drawString(56, 400, "Aplicação Streamlit  ·  diagnóstico  ·  painel analítico")
    read_box(c, T1, y0=56)
    c.setFillColor(white)
    c.setFont("Sans", 10)
    c.drawRightString(W - 28, 20, f"{n} / {t}")


def slide_02(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "O problema no hospital")
    items = [
        ("Doença crônica", "A obesidade envolve genética, ambiente e comportamento."),
        ("Triagem desigual", "O primeiro olhar de risco muda de profissional para profissional."),
        ("Apoio, não substituto", "O sistema padroniza a classificação em sete níveis e devolve a conduta à equipe."),
    ]
    x = 40
    for title, body in items:
        card(c, x, 268, 380, 250)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 16)
        c.drawString(x + 24, 468, title)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        yy = 418
        for line in wrap(c, body, "Sans", 14, 330):
            c.drawString(x + 24, yy, line)
            yy -= 22
        x += 400
    read_box(c, T2)
    footer(c, n, t)


def slide_03(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Entregas da disciplina")
    checks = [
        "Pipeline de machine learning, com preparação dos dados e treino.",
        "Modelo com assertividade acima de 75% no teste — na prática, 98,35%.",
        "Aplicação preditiva no Streamlit, em produção na nuvem.",
        "Painel analítico com insights para a equipe médica.",
        "Repositório no GitHub com o código e o modelo.",
        "Este vídeo: sistema e dashboard em visão de negócio.",
    ]
    top = 548
    for i, item in enumerate(checks):
        y = top - i * 52
        card(c, 40, y - 6, 1200, 44)
        c.setFillColor(TEAL)
        c.circle(68, y + 16, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("SansBold", 11)
        c.drawCentredString(68, y + 12, "✓")
        c.setFillColor(INK)
        c.setFont("Sans", 15)
        c.drawString(96, y + 10, item)
    read_box(c, T3, y0=40)
    footer(c, n, t)


def slide_04(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "O aplicativo — diagnóstico preditivo")
    shot(c, "01_formulario.png", 40, 196, 1200, 336)
    read_box(c, T4)
    footer(c, n, t)


def slide_05(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Exemplo de diagnóstico")
    shot(c, "02_diagnostico.png", 40, 196, 1200, 336)
    read_box(c, T5)
    footer(c, n, t)


def slide_06(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Como a equipe lê o resultado")
    boxes = [
        ("Classe predita", "O nível estimado em sete classes, em português."),
        ("IMC e faixa OMS", "Métrica clínica ao lado da predição, para cruzar as duas leituras."),
        ("Confiança", "Probabilidade em cada nível. Útil quando o caso está na fronteira."),
        ("Limite", "Apoio à triagem. Conduta — dieta, exame, encaminhamento — é da equipe."),
    ]
    positions = [(40, 378), (650, 378), (40, 218), (650, 218)]
    for (title, body), (x, y) in zip(boxes, positions):
        card(c, x, y, 590, 140)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 16)
        c.drawString(x + 24, y + 100, title)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        yy = y + 70
        for line in wrap(c, body, "Sans", 14, 540):
            c.drawString(x + 24, yy, line)
            yy -= 20
    read_box(c, T6, y0=40)
    footer(c, n, t)


def slide_07(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Painel analítico — visão da gestão")
    shot(c, "03_painel_kpis.png", 40, 196, 1200, 336)
    read_box(c, T7)
    footer(c, n, t)


def slide_08(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Hábitos que mudam a conduta")
    shot(c, "04_painel_graficos.png", 40, 196, 1200, 336)
    read_box(c, T8)
    footer(c, n, t)


def slide_09(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Pipeline de machine learning")
    steps = [
        ("1", "Dados", "Biometria, família, alimentação e rotina."),
        ("2", "IMC", "Peso sobre altura ao quadrado, como apoio clínico."),
        ("3", "Preparação", "Números na mesma escala; categorias transformadas."),
        ("4", "Modelos", "Random Forest e Gradient Boosting, no mesmo fluxo."),
    ]
    x = 40
    for num, title, body in steps:
        card(c, x, 268, 290, 262)
        c.setFillColor(GREEN)
        c.circle(x + 36, 492, 16, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("SansBold", 14)
        c.drawCentredString(x + 36, 486, num)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 18)
        c.drawString(x + 24, 432, title)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        yy = 392
        for line in wrap(c, body, "Sans", 14, 240):
            c.drawString(x + 24, yy, line)
            yy -= 22
        x += 310
    read_box(c, T9)
    footer(c, n, t)


def slide_10(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Assertividade do modelo")
    card(c, 40, 268, 580, 262)
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(72, 490, "Mínimo exigido")
    c.setFillColor(INK)
    c.setFont("SansBold", 52)
    c.drawString(72, 418, "75%")
    c.setFillColor(MUTED)
    c.setFont("Sans", 14)
    c.drawString(72, 348, "Campeão no teste  ·  Gradient Boosting")
    c.setFillColor(GREEN)
    c.setFont("SansBold", 52)
    c.drawString(72, 280, "98,35%")
    card(c, 660, 268, 580, 262)
    c.setFillColor(INK)
    c.setFont("SansBold", 18)
    c.drawString(692, 490, "Comparação")
    c.setFont("Sans", 15)
    y = 440
    for line in (
        "Gradient Boosting    98,35% no teste",
        "Random Forest           97,87% no teste",
        "Validação cruzada     97,5%  ±  0,8%",
        "Os dois passam do critério.",
        "O campeão é o modelo do aplicativo.",
    ):
        c.drawString(692, y, line)
        y -= 36
    read_box(c, T10)
    footer(c, n, t)


def slide_11(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Produção e extras")
    boxes = [
        ("Streamlit Cloud", "avaliapeso.streamlit.app", "Deploy oficial: diagnóstico e painel no mesmo link."),
        ("GitHub", "fase4-postech / main", "Código, pipeline, modelo e documentação."),
        ("Extra MLOps", "FastAPI + Docker", "API de inferência e containers unindo API e tela."),
    ]
    x = 40
    for title, sub, body in boxes:
        card(c, x, 268, 390, 262)
        c.setFillColor(GREEN)
        c.setFont("SansBold", 18)
        c.drawString(x + 24, 488, title)
        c.setFillColor(TEAL)
        c.setFont("SansBold", 13)
        c.drawString(x + 24, 456, sub)
        c.setFillColor(INK)
        c.setFont("Sans", 14)
        yy = 408
        for line in wrap(c, body, "Sans", 14, 340):
            c.drawString(x + 24, yy, line)
            yy -= 22
        x += 410
    read_box(c, T11)
    footer(c, n, t)


def slide_12(c: canvas.Canvas, n: int, t: int) -> None:
    heading(c, "Impacto e encerramento")
    bullets = [
        "Primeira triagem mais curta e padronizada em sete níveis.",
        "Painel para campanha de prevenção: família, exercício e alimentação.",
        "Próximo passo no hospital: validar na unidade e, se fizer sentido, ligar a API ao prontuário.",
    ]
    y = 520
    for item in bullets:
        card(c, 40, y - 12, 1200, 56)
        c.setFillColor(TEAL)
        c.circle(68, y + 12, 6, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Sans", 16)
        c.drawString(96, y + 6, item)
        y -= 72
    read_box(c, T12)
    footer(c, n, t)


def main() -> None:
    pages = [
        slide_01,
        slide_02,
        slide_03,
        slide_04,
        slide_05,
        slide_06,
        slide_07,
        slide_08,
        slide_09,
        slide_10,
        slide_11,
        slide_12,
    ]
    total = len(pages)
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("Apresentação do sistema preditivo de obesidade")
    c.setAuthor("Tech Challenge Fase 4")
    for i, fn in enumerate(pages, start=1):
        fn(c, i, total)
        c.showPage()
    c.save()
    print(f"wrote {OUT} ({total} pages)")


if __name__ == "__main__":
    main()
