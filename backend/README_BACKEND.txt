TradeNova backend
-----------------
- Language: Python / FastAPI
- Run locally:
  1. python -m venv .venv
  2. .venv\Scripts\activate
  3. pip install -r requirements.txt
  4. uvicorn api:app --reload --host 0.0.0.0 --port 8000
- For Render: upload this folder; set env vars (APP_USERNAME, APP_PASSWORD, JWT_SECRET)
