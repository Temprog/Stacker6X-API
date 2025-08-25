# Stacker6X-API
Flask REST API for Stacker6X ML model detecting SQLi/XSS with regex-based guardrails


## 🛡️ Stacker6X Backend
This is the backend API for the Stacker6X Security Model, a machine learning system that detects SQL injection (SQLi) and Cross-Site Scripting (XSS) attacks in text inputs.

It exposes a Flask REST API that accepts input text and returns predictions from a trained ensemble model (Stacker6X).
To reduce false positives, the API includes a regex-based guardrail that double-checks suspected SQLi payloads.


## 🚀 Features
- Flask REST API (/predict)
- Loads trained Stacker6X ensemble model + TF-IDF vectorizer
- Guardrail logic for reducing false positives on SQLi predictions
- Custom error handling (e.g. large payloads > 2MB)
- Ready for deployment to Render, Heroku, AWS, etc.


## 🗂️ Project Structure
backend/
│
├── app.py                          # Flask API entrypoint
├── stacker6x_model_definition.py   # Model class definition
├── Stacker6X_trained_model.pkl     # Trained ML model (joblib)
├── tfidf_vectorizer.pkl            # TF-IDF vectorizer
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                  # Optional homepage template
└── README.md                       # This file


## ⚡ Setup & Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/stacker6x-backend.git
cd stacker6x-backend
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies
   
```bash
pip install -r requirements.txt
```

4. Run the Flask server
   
```bash
flask run
```
By default it runs on http://127.0.0.1:5000


## 🔗 API Endpoints
```GET /```
- Returns a simple homepage (index.html if available, fallback message otherwise).

```POST /predict```
- Accepts JSON input and returns a classification.

**Request**
```http
POST /predict
Content-Type: application/json

{
  "text": "SELECT * FROM users WHERE id = 1 OR 1=1"
}
```

**Response**
```http
{
  "prediction": "SQLi (malicious)"
}
```

**Error Handling**

- 413 Payload Too Large
```json
{ "error": "File too large. Maximum upload size is 2MB." }
```

**400 Bad Request (e.g., missing text field)**
```json
{ "error": "Invalid input: \"text\" field is missing" }
```


## 🛠️ Tech Stack
- Python 3.9+
- Flask (REST API)
- scikit-learn / joblib (ML model + vectorizer)
- Regex guardrails for SQL injection sanity check

## 📂 Related Repositories
- 🧠 [Stacker6X Model (ML Training & Core Logic)](https://github.com/Temprog/Stacker6X-Model)  
  Core machine learning repository containing training code, preprocessing, model artifacts, evaluation, configuration, notebooks, utilities and deployment simulation.  
- 🛡️ [Stacker6X Backend (Flask REST API)](https://github.com/Temprog/Stacker6X-API)  
  Flask REST API for serving predictions from the trained model, with an added regex-based guardrail to reduce false positives.  
- 🎨 [Stacker6X Frontend (HTML/JS UI)](https://github.com/Temprog/Stacker6X-frontend)  
  Lightweight web interface for interacting with the backend API and visualizing predictions.  


## ✨ Portfolio Note

This backend project demonstrates:
- Serving a trained ML model via a Flask REST API
- Production-ready API design with regex-based guardrails to reduce false positives
- Error handling and request validation for robust deployment
- Separation of concerns: backend API distinct from model training and frontend UI
