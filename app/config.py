"""Configurações visuais, eventos geopolíticos e parâmetros do app Brent."""

from __future__ import annotations

PRIMARY = "#0A3D62"
ACCENT = "#C9A227"
BG = "#F5F7FA"
CARD = "#E8EEF4"
TEXT = "#1B2838"

HORIZON_OPTIONS = (7, 15, 30)
DEFAULT_HORIZON = 15
DEFAULT_BARRELS = 1_000_000

GEOPOLITICAL_EVENTS = [
    {
        "date": "1990-08-02",
        "title": "Guerra do Golfo",
        "impact": "Choque de oferta no Oriente Médio. O preço do Brent dispara com o risco de interrupção do petróleo do Golfo.",
    },
    {
        "date": "2008-07-11",
        "title": "Crise dos Subprimes / pico de US$ 140+",
        "impact": "Demanda global e fluxos financeiros levam o barril a máximas históricas, seguidas de colapso na crise de 2008.",
    },
    {
        "date": "2014-11-27",
        "title": "Guerra de preços da OPEP",
        "impact": "A OPEP decide não cortar produção diante do shale americano. Excesso de oferta e queda prolongada dos preços.",
    },
    {
        "date": "2020-04-21",
        "title": "COVID-19 / choque de demanda",
        "impact": "Lockdowns derrubam o consumo. O WTI chega a negociar negativo; o Brent sofre uma das maiores quedas da série.",
    },
    {
        "date": "2022-02-24",
        "title": "Conflito Rússia–Ucrânia",
        "impact": "Choque de oferta na Europa e sanções sobre o petróleo russo. Novo salto de volatilidade e prêmio geopolítico.",
    },
]
