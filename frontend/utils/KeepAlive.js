// frontend/src/utils/keepAlive.js
export const startKeepAlive = () => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    if (!backendUrl) return;
  
    console.log("⏳ TradeNova KeepAlive started...");
  
    // Send ping every 25 seconds to prevent backend sleep
    setInterval(async () => {
      try {
        await fetch(`${backendUrl}/health`);
        console.log("✅ KeepAlive ping sent to backend");
      } catch (err) {
        console.log("⚠️ KeepAlive ping failed:", err.message);
      }
    }, 25000);
  };