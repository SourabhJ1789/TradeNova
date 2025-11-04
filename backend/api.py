# backend/api.py
import os
import time
import json
import asyncio
import logging
from typing import Optional
from urllib.parse import parse_qs

import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Security / env
JWT_SECRET = os.environ.get("JWT_SECRET", "change_this_in_render")
JWT_ALGO = "HS256"
TOKEN_EXP_SECONDS = int(os.environ.get("TOKEN_EXP_SECONDS", "3600"))
APP_USERNAME = os.environ.get("APP_USERNAME", "Sourabh")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "Sourabh1789")

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

def create_token(username: str) -> str:
    payload = {"sub": username, "iat": int(time.time()), "exp": int(time.time()) + TOKEN_EXP_SECONDS}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload.get("sub")
    except Exception as e:
        logging.warning(f"Invalid token: {e}")
        return None

@app.post("/login")
def login(req: LoginRequest):
    if req.username != APP_USERNAME or req.password != APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(req.username)
    return {"access_token": token, "token_type": "bearer", "expires_in": TOKEN_EXP_SECONDS}

class ConnectionManager:
    def __init__(self):
        self.active = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        try:
            self.active.remove(ws)
        except ValueError:
            pass

    async def broadcast(self, message: dict):
        payload = json.dumps(message)
        for ws in list(self.active):
            try:
                await ws.send_text(payload)
            except:
                self.disconnect(ws)

manager = ConnectionManager()

@app.websocket("/ws/live")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    qs = dict(parse_qs(ws.scope.get("query_string", b"").decode()))
    token = qs.get("token", [None])[0]
    username = verify_token(token) if token else None
    if username is None:
        await ws.close(code=1008)
        return

    await manager.connect(ws)
    logging.info(f"WebSocket connected: {username}")
    try:
        while True:
            _ = await ws.receive_text()
            await ws.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        manager.disconnect(ws)
        logging.info("WebSocket disconnected")

@app.get("/")
def health():
    return {"status": "OK", "message": "TradeNova backend running."}
