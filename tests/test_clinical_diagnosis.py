"""Garante que o grau I/II/III no diagnóstico segue o IMC (OMS), não o NCP."""

from src.inference import predict_patient

FEMALE_120KG = dict(
    Gender="Female",
    Age=42.0,
    Height=1.70,
    Weight=120.0,
    family_history="yes",
    FAVC="yes",
    FCVC=1.0,
    NCP=1.0,
    CAEC="no",
    SMOKE="yes",
    CH2O=1.0,
    SCC="yes",
    FAF=0.0,
    TUE=2.0,
    CALC="Frequently",
    MTRANS="Public_Transportation",
)

HEALTHY = dict(
    Gender="Female",
    Age=42.0,
    Height=1.70,
    Weight=120.0,
    family_history="no",
    FAVC="no",
    FCVC=3.0,
    NCP=1.0,
    CAEC="no",
    SMOKE="no",
    CH2O=3.0,
    SCC="yes",
    FAF=3.0,
    TUE=0.0,
    CALC="no",
    MTRANS="Walking",
)


def test_ncp_does_not_drop_type_iii():
    for ncp in (1.0, 2.0, 3.0):
        payload = dict(FEMALE_120KG, NCP=ncp)
        result = predict_patient(payload)
        assert result["imc"] == 41.52
        assert result["imc_oms"] == "Obesidade tipo III"
        assert result["prediction"] == "Obesity_Type_III", result


def test_healthy_lifestyle_still_type_iii_when_bmi_41():
    for ncp in (1.0, 2.0):
        result = predict_patient(dict(HEALTHY, NCP=ncp))
        assert result["prediction"] == "Obesity_Type_III"


def test_who_bands():
    type_i = dict(FEMALE_120KG, Height=1.70, Weight=90.0)  # IMC ~31.1
    type_ii = dict(FEMALE_120KG, Height=1.70, Weight=105.0)  # IMC ~36.3
    r1 = predict_patient(type_i)
    r2 = predict_patient(type_ii)
    assert r1["prediction"] == "Obesity_Type_I", r1
    assert r2["prediction"] == "Obesity_Type_II", r2


if __name__ == "__main__":
    test_ncp_does_not_drop_type_iii()
    test_healthy_lifestyle_still_type_iii_when_bmi_41()
    test_who_bands()
    print("ok")
