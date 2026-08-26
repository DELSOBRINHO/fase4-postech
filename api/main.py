"""API REST extra para servir inferências do modelo (FastAPI)."""

from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_pipeline import LABEL_PT  # noqa: E402
from src.inference import load_model, predict_patient  # noqa: E402


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_model()
    yield


app = FastAPI(
    title="API de Diagnóstico de Obesidade",
    description=(
        "Extra de MLOps: serve o mesmo pipeline sklearn usado no Streamlit. "
        "Não substitui o deploy oficial em https://avaliapeso.streamlit.app/"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PatientFeatures(BaseModel):
    Gender: Literal["Female", "Male"]
    Age: float = Field(..., ge=14, le=80)
    Height: float = Field(..., ge=1.2, le=2.2)
    Weight: float = Field(..., ge=30, le=200)
    family_history: Literal["yes", "no"]
    FAVC: Literal["yes", "no"]
    FCVC: float = Field(..., ge=1, le=3)
    NCP: float = Field(..., ge=1, le=4)
    CAEC: Literal["no", "Sometimes", "Frequently", "Always"]
    SMOKE: Literal["yes", "no"]
    CH2O: float = Field(..., ge=1, le=3)
    SCC: Literal["yes", "no"]
    FAF: float = Field(..., ge=0, le=3)
    TUE: float = Field(..., ge=0, le=2)
    CALC: Literal["no", "Sometimes", "Frequently", "Always"]
    MTRANS: Literal[
        "Public_Transportation",
        "Automobile",
        "Walking",
        "Motorbike",
        "Bike",
    ]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Gender": "Female",
                    "Age": 21,
                    "Height": 1.62,
                    "Weight": 64,
                    "family_history": "yes",
                    "FAVC": "no",
                    "FCVC": 2,
                    "NCP": 3,
                    "CAEC": "Sometimes",
                    "SMOKE": "no",
                    "CH2O": 2,
                    "SCC": "no",
                    "FAF": 0,
                    "TUE": 1,
                    "CALC": "no",
                    "MTRANS": "Public_Transportation",
                }
            ]
        }
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "obesity-inference"}


@app.get("/classes")
def classes() -> dict:
    model = load_model()
    return {
        "classes": list(model.classes_),
        "labels_pt": {c: LABEL_PT.get(c, c) for c in model.classes_},
    }


@app.post("/predict")
def predict(payload: PatientFeatures) -> dict:
    try:
        return predict_patient(payload.model_dump())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
