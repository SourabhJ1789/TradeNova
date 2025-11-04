import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from clients.coindcx_client import start_coindcx_listener

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# store all active websocket clients
connected_clients = set()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_coindcx_listener(broadcast_message))
    print("✅ CoinDCX WebSocket listener started in background")

async def broadcast_message(data: dict):
    # send data to all connected clients
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception:
            disconnected.append(client)
    for client in disconnected:
        connected_clients.remove(client)

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("📡 Client connected")

    try:
        while True:
            await websocket.receive_text()  # keep alive from frontend
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("❌ Client disconnected")