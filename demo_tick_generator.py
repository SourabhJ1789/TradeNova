# demo_tick_generator.py
# Sends fake ticks to TradeNova backend WS for testing
import asyncio, websockets, json, random
async def send_fake_ticks():
    uri = "ws://localhost:8000/ws/live"
    # get token from environment or paste here if using deployed backend
    token = ""
    if token:
        uri += "?token=" + token
    async with websockets.connect(uri) as ws:
        print("Sending fake ticks...")
        while True:
            price = 22000 + random.uniform(-50,50)
            msg = {"type":"stock","tick":{"tradingsymbol":"NIFTY","last_price":round(price,2),"volume":random.randint(8000,12000)}}
            await ws.send(json.dumps(msg))
            await asyncio.sleep(2)
if __name__ == '__main__':
    asyncio.run(send_fake_ticks())
