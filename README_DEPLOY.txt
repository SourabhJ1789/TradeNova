TradeNova - Deploy Guide (short)
--------------------------------
1) Unzip TradeNova folder
2) Backend:
   - Option A: Run locally: cd backend; pip install -r requirements.txt; uvicorn api:app --host 0.0.0.0 --port 8000
   - Option B: Upload backend folder to Render (New -> Web Service -> Upload Folder). Set env vars: APP_USERNAME, APP_PASSWORD, JWT_SECRET
3) Frontend:
   - Option A: Run locally: cd frontend; npm install; npm run dev -- --host
   - Option B: Upload frontend folder to Vercel (drag & drop). Set env var VITE_BACKEND_URL to your backend URL.
4) For testing without auth locally: start backend, then run demo_tick_generator.py to send fake ticks.
