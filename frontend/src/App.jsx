import React, { useEffect, useState } from "react";
const BACKEND = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
export default function App() {
  const [token, setToken] = useState(localStorage.getItem("access_token") || "");
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [stocks, setStocks] = useState([]);
  const [connected, setConnected] = useState(false);

  const login = async () => {
    try {
      const res = await fetch(BACKEND + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user, password: pass }),
      });
      if (!res.ok) throw new Error("Invalid credentials");
      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      setToken(data.access_token);
    } catch (err) {
      alert(err.message);
    }
  };

  useEffect(() => {
    if (!token) return;
    const wsUrl = BACKEND.replace(/^http/, "ws") + "/ws/live?token=" + encodeURIComponent(token);
    const ws = new WebSocket(wsUrl);
    ws.onopen = () => setConnected(true);
    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);
        if (msg.type === "stock") setStocks((s) => [msg, ...s].slice(0, 20));
      } catch {}
    };
    ws.onclose = () => setConnected(false);
    return () => ws.close();
  }, [token]);

  if (!token)
    return (
      <div style={{ textAlign: "center", padding: "40px" }}>
        <h2>🔐 TradeNova Login</h2>
        <input placeholder="Username" value={user} onChange={(e) => setUser(e.target.value)} /> <br />
        <input type="password" placeholder="Password" value={pass} onChange={(e) => setPass(e.target.value)} /> <br />
        <button onClick={login}>Login</button>
      </div>
    );

  return (
    <div style={{ padding: "12px" }}>
      <h1>TradeNova</h1>
      <p>🧠 Connection: {connected ? "🟢 Connected" : "🔴 Disconnected"}</p>
      <h2>Stock Feed</h2>
      {stocks.map((s, i) => (
        <div key={i} style={{ border: "1px solid #eee", marginBottom: "8px", padding: "6px" }}>
          <b>{s.tick && (s.tick.tradingsymbol || s.tick.instrument || 'NIFTY')}</b> — ₹{s.tick && s.tick.last_price}
        </div>
      ))}
    </div>
  );
}
