

# api/index.py
"""
Vercel Python Serverless entry-point.
Convert the old Flask app into a single `handler(request)` function.
"""

import base64
import io
import json
from pathlib import Path

import pandas as pd
import pickle

# ---------- load assets once, keep them warm between invocations ----------
ROOT = Path(__file__).resolve().parent.parent   # project root

# ML artefacts
with open(ROOT / "mental_health_model.pkl", "rb") as f:
    model = pickle.load(f)

with open(ROOT / "label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# import your llama chat engine
from llama_engine import get_response   # noqa: E402

# ---------------------------- helpers --------------------------------------


def safe_transform(le, series: pd.Series) -> pd.Series:
    """Map unseen labels to -1 so the model still runs."""
    return series.map(lambda v: le.transform([v])[0] if v in le.classes_ else -1)


def interpret_results(pred):
    depression, anxiety, stress = pred[0]
    return {
        "depression": float(depression),
        "anxiety": float(anxiety),
        "stress": float(stress),
        "suggestions": {
            "depression": (
                "Consider seeing a counselor or practising relaxation techniques."
                if depression > 50
                else "Keep up with healthy habits and stay active."
            ),
            "anxiety": (
                "Practise mindfulness or talk to a therapist."
                if anxiety > 50
                else "Keep maintaining your healthy habits."
            ),
            "stress": (
                "Consider reducing workload or practising stress-relieving exercises."
                if stress > 50
                else "Continue maintaining a stress-free routine."
            ),
        },
    }


# ---------------------------- ROUTES ---------------------------------------
def handle_predict(req):
    """POST /api/predict  – returns model percentages + suggestions"""
    user_data = req.get_json(silent=True) or {}
    df = pd.DataFrame([user_data])

    for col in df.columns:
        if col in label_encoders:
            df[col] = safe_transform(label_encoders[col], df[col])

    out = model.predict(df)
    return interpret_results(out)


def handle_chat(req):
    """POST /api/chat  – chat endpoint that proxies to llama_engine"""
    user_input = (req.get_json(silent=True) or {}).get("user_input", "")
    return {"response": get_response(user_input)}


# ---------------------------------------------------------------------------
def handler(request):  # <-- Vercel looks for this symbol
    """
    Dispatch based on path and method.
    •   GET  /api/              -> health-check JSON
    •   POST /api/predict       -> ML prediction
    •   POST /api/chat          -> chatbot response
    """
    path = request.path.rstrip("/") or "/"
    method = request.method.upper()

    try:
        # ---- ROUTING ----
        if path == "/" and method == "GET":
            return {"statusCode": 200, "body": json.dumps({"ok": True})}

        if path == "/predict" and method == "POST":
            body = handle_predict(request)
            return {"statusCode": 200, "body": json.dumps(body)}

        if path == "/chat" and method == "POST":
            body = handle_chat(request)
            return {"statusCode": 200, "body": json.dumps(body)}

        # fallback 404
        return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}

    except Exception as e:  # pylint: disable=broad-except
        # basic error bubbling
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
