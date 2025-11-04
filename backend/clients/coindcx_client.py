import asyncio
import json
import websockets

COINDCX_WS_URL = "wss://stream.coindcx.com"

async def start_coindcx_listener(broadcast_callback):
    """
    Connects to CoinDCX WebSocket and streams all ticker data.
    """
    async with websockets.connect(COINDCX_WS_URL, ping_interval=None) as ws:
        print("✅ Connected to CoinDCX WebSocket feed")

        # Subscribe to all ticker updates
        subscribe_msg = {
            "type": "subscribe",
            "channels": [{"name": "tickers"}]
        }
        await ws.send(json.dumps(subscribe_msg))

        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)
                # Forward received data to all connected frontend clients
                await broadcast_callback(data)
            except websockets.ConnectionClosed:
                print("⚠️ Connection closed, retrying in 5 seconds...")
                await asyncio.sleep(5)
                return await start_coindcx_listener(broadcast_callback)
            except Exception as e:
                print(f"❌ Error in CoinDCX listener: {e}")
                await asyncio.sleep(5)