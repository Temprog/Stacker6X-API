import os
import re
import builtins

import dill
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, Request, abort

from stacker6x_model_definition import Stacker6X


# Ensures numpy is available globally for unpickled objects
builtins.np = np


# Class label mapping
CLASS_LABELS = {
    0: "SQLi (malicious)",
    1: "XSS (malicious)",
    2: "Benign (normal)"
}

# Regex patterns for SQL injection
SQLI_PATTERNS = [
    r"(?i)(union\s+select)",
    r"(?i)(or\s+1=1)",
    r"(--|#)",
    r"(?i)(drop\s+table)",
    r"(?i)(insert\s+into)",
    r"(?i)(update\s+\w+\s+set)"
]


def looks_like_sqli(text: str) -> bool:
    """Return True if the input text matches common SQL injection patterns."""
    return any(re.search(pattern, text) for pattern in SQLI_PATTERNS)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Stacker6X_trained_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

# Load the trained model and vectorizer immediately
try:
    stacker6X_model_instance = joblib.load(MODEL_PATH)
    loaded_tfidf_vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and vectorizer loaded successfully.")
except FileNotFoundError as e:
    raise RuntimeError(f"Failed to load model/vectorizer: {e}")


app = Flask(__name__)


@app.route('/')
def home():
    """
    Home route.
    - Default: render index.html
    - Option: switch to plain text if no template is available
    """
    return render_template('index.html')
    #return "Stacker6X Model Deployment API is running!"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Invalid input: \"text\" field is missing'}), 400

        input_text = data['text']
        X_vectorized = loaded_tfidf_vectorizer.transform([input_text])
        prediction = stacker6X_model_instance.predict(X_vectorized)[0]

        # ---------------------------------------------------------------
        # Guardrail logic:
        # Keeping the model’s raw predict() results but adding a
        # rule-based sanity check for SQLi.
        #
        # Why?
        # - Sometimes the model mistakenly predicts SQLi for benign text.
        # - To reduce false positives, the input is checked with regex rules.
        # - If the model says SQLi but the text doesn’t look like injection,
        #   it downgrades it to Benign.
        # ---------------------------------------------------------------
        prediction_label = CLASS_LABELS[int(prediction)]
        if prediction_label.startswith("SQLi") and not looks_like_sqli(input_text):
            prediction_label = "Benign (normal)"

        return jsonify({'prediction': prediction_label})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)  # Payload Too Large
def request_entity_too_large(error):
    """Custom handler for large payloads (files > 2MB)."""
    return jsonify({"error": "File too large. Maximum upload size is 2MB."}), 413
