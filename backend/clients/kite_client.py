import os, asyncio, logging
from kiteconnect import KiteConnect

logger = logging.getLogger("kite_client")
logging.basicConfig(level=logging.INFO)

KITE_API_KEY = os.getenv("KITE_API_KEY")
KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")
WATCH_LIST = os.getenv("KITE_WATCHLIST", "NSE:RELIANCE,NSE:TCS").split(",")
POLL_INTERVAL = int(os.getenv("KITE_POLL_INTERVAL", "2"))

class KiteClient:
    def __init__(self, manager):
        if not (KITE_API_KEY and KITE_ACCESS_TOKEN):
            logger.warning("Kite API not configured.")
            self.kite = None
        else:
            self.kite = KiteConnect(api_key=KITE_API_KEY)
            self.kite.set_access_token(KITE_ACCESS_TOKEN)
        self.manager = manager
        self.running = False

    async def start(self):
        if not self.kite:
            return
        self.running = True
        logger.info("Kite client started…")
        while self.running:
            try:
                data = self.kite.ltp(WATCH_LIST)
                for s, d in data.items():
                    msg = {"type": "kite", "source": "zerodha",
                           "tick": {"instrument": s, "last_price": d.get("last_price")}}
                    await self.manager.broadcast(msg)
                await asyncio.sleep(POLL_INTERVAL)
            except Exception as e:
                logger.exception("Kite error: %s", e)
                await asyncio.sleep(5)

    async def stop(self):
        self.running = False
