import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://localhost:8000/api";

function App() {
  const [customers, setCustomers] = useState([]);
  const [customerId, setCustomerId] = useState("c_rahul");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(false);

  const customer = customers.find(c => c.id === customerId);

  useEffect(() => {
    fetch(API + "/customers").then(r => r.json()).then(setCustomers);
  }, []);

  async function send() {
    if (!message.trim() || loading) return;
    const current = message;
    setMessages(x => [...x, { role: "user", text: current }]);
    setMessage("");
    setLoading(true);
    try {
      const r = await fetch(API + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ customer_id: customerId, message: current })
      });
      const data = await r.json();
      setMessages(x => [...x, { role: "agent", text: data.answer }]);
      setMemories(data.memories || []);
    } catch {
      setMessages(x => [...x, { role: "agent", text: "Backend is not running. Start FastAPI on port 8000." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <div>
          <div className="eyebrow">HACKWITHHYDERABAD 3.0</div>
          <h1>MemoryDesk <span>AI</span></h1>
          <p>Support that remembers.</p>
        </div>
        <div className="badge">● Hindsight Memory</div>
      </header>

      <main className="grid">
        <aside className="panel customers">
          <h3>Customers</h3>
          {customers.map(c => (
            <button key={c.id} className={customerId === c.id ? "customer active" : "customer"} onClick={() => {setCustomerId(c.id); setMessages([]); setMemories([]);}}>
              <div className="avatar">{c.name.split(" ").map(x=>x[0]).join("")}</div>
              <div className="customer-meta">
                <strong>{c.name}</strong>
                <small>{c.company}</small>
              </div>
            </button>
          ))}
        </aside>

        <section className="panel chat">
          {customer && (
            <div className="customer-banner">
              <div>
                <div className="label">ACTIVE CUSTOMER</div>
                <h2>{customer.name}</h2>
                <span>{customer.company} · {customer.device}</span>
              </div>
              <div className="ticket">{customer.open_ticket || "No open ticket"}</div>
            </div>
          )}

          <div className="messages">
            {messages.length === 0 && (
              <div className="empty">
                <div className="brain">🧠</div>
                <h3>Start a support interaction</h3>
                <p>Ask about an issue, then ask a related question later to demonstrate persistent memory.</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={"msg " + m.role}>
                <div className="msg-label">{m.role === "agent" ? "MEMORYDESK" : "CUSTOMER"}</div>
                <div className="bubble">{m.text}</div>
              </div>
            ))}
            {loading && <div className="msg agent"><div className="msg-label">MEMORYDESK</div><div className="bubble">Recalling customer context…</div></div>}
          </div>

          <div className="composer">
            <input
              value={message}
              onChange={e => setMessage(e.target.value)}
              onKeyDown={e => e.key === "Enter" && send()}
              placeholder="Describe the customer's issue…"
            />
            <button onClick={send}>Send ↗</button>
          </div>
        </section>

        <aside className="panel memory">
          <div className="memory-head">
            <div>
              <div className="label">MEMORY LAYER</div>
              <h3>What the agent remembers</h3>
            </div>
            <span className="status">{memories.length ? "ACTIVE" : "WAITING"}</span>
          </div>

          {memories.length === 0 ? (
            <div className="memory-empty">
              <div>⌁</div>
              <p>Relevant memories will appear here after a recall.</p>
            </div>
          ) : memories.map((m, i) => (
            <div className="memory-card" key={m.id || i}>
              <div className="memory-type">{m.type}</div>
              <p>{m.text}</p>
              {m.score != null && <small>relevance {Number(m.score).toFixed(2)}</small>}
            </div>
          ))}

          <div className="demo-tip">
            <strong>Demo tip</strong>
            <p>First ask: “My printer keeps disconnecting from Wi‑Fi.” Then ask: “It happened again.” Show how the second answer uses remembered context.</p>
          </div>
        </aside>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
