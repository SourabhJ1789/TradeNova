import asyncio, aiohttp, json, logging, os
logger = logging.getLogger("coindcx_client")

COINDCX_WS = os.getenv("COINDCX_WS", "wss://stream.coindcx.com/market")
SYMBOLS = os.getenv("COINDCX_SYMBOLS", "BTCINR,ETHINR").split(",")

class CoinDCXClient:
    def __init__(self, manager):
        self.manager = manager
        self.session = None
        self.ws = None
        self.running = False

    async def start(self):
        self.running = True
        self.session = aiohttp.ClientSession()
        while self.running:
            try:
                async with self.session.ws_connect(COINDCX_WS) as ws:
                    sub = {"type": "subscribe", "symbols": SYMBOLS}
                    await ws.send_json(sub)
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            out = {"type": "coindcx", "source": "coindcx", "tick": data}
                            await self.manager.broadcast(out)
            except Exception as e:
                logger.exception("CoinDCX reconnecting: %s", e)
                await asyncio.sleep(5)

    async def stop(self):
        self.running = False
        if self.ws: await self.ws.close()
        if self.session: await self.session.close()
