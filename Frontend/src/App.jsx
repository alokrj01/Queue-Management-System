import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState("");
  const [myTicket, setMyTicket] = useState(null);
  const [queueStatus, setQueueStatus] = useState({ waiting_count: 0 });
  const [skippedList, setSkippedList] = useState([]); // <--- New State for Skipped People

  // 1. Status Loop (Runs every 2 seconds)
  useEffect(() => {
    const interval = setInterval(() => {
      // Fetch Status
      fetch("http://127.0.0.1:8000/status")
        .then(res => res.json())
        .then(data => setQueueStatus(data));
      
      // Fetch Skipped List (NEW)
      fetch("http://127.0.0.1:8000/skipped")
        .then(res => res.json())
        .then(data => setSkippedList(data));
        
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const joinQueue = () => {
    if (!name) return alert("Enter name");
    fetch("http://127.0.0.1:8000/join", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name })
    }).then(res => res.json()).then(data => {
      setMyTicket(data);
      setName(""); 
    });
  };

  const callNext = () => {
    fetch("http://127.0.0.1:8000/next", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.person) alert(`📢 Now Serving: ${data.person.name}`);
        else alert("No one waiting.");
      });
  };

  const markAbsent = () => {
    fetch("http://127.0.0.1:8000/skip", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.person) alert(`⚠️ Skipped: ${data.person.name}`);
      });
  };

  // NEW: Recall Function
  const recallPerson = (id) => {
    fetch(`http://127.0.0.1:8000/recall/${id}`, { method: "POST" })
      .then(res => res.json())
      .then(data => {
        alert(`🚨 RECALLING: ${data.person.name}`);
      });
  };

  return (
    <div className="app-container">
      <div className="main-card">
        
        <div className="header">
          <h1>Queue System</h1>
          <p>Smart Counter Management</p>
        </div>
        
        <div className="status-box">
          <div className="status-label">Currently Waiting</div>
          <div className="status-number">{queueStatus.waiting_count}</div>
        </div>

        <div className="input-group">
          <input type="text" placeholder="Visitor Name" value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <button onClick={joinQueue} className="btn-primary">Generate Ticket</button>

        {myTicket && (
          <div className="ticket-card">
            <div className="ticket-row">
              <span className="ticket-label">Name</span>
              <span className="ticket-value">{myTicket.name}</span>
            </div>
            <div className="ticket-row">
              <span className="ticket-label">Token ID</span>
              <span className="ticket-value">#{myTicket.id.slice(-4).toUpperCase()}</span>
            </div>
            {myTicket.estimated_wait_minutes !== undefined && (
              <div className="wait-time">⏱ Est. Wait: {myTicket.estimated_wait_minutes} mins</div>
            )}
          </div>
        )}

        {/* STAFF CONTROLS */}
        <div className="staff-controls">
          <button onClick={callNext} className="btn-staff">Next</button>
          <button onClick={markAbsent} className="btn-danger">Absent</button>
        </div>

        {/* NEW: MISSED PEOPLE LIST */}
        {skippedList.length > 0 && (
          <div style={{ marginTop: "30px", textAlign: "left" }}>
            <h4 style={{ color: "#ef4444", borderBottom: "1px solid #ddd", paddingBottom: "5px" }}>⚠️ Missed / Skipped</h4>
            {skippedList.map(person => (
              <div key={person.id} style={{ 
                display: "flex", justifyContent: "space-between", alignItems: "center", 
                padding: "10px", borderBottom: "1px solid #eee" 
              }}>
                <span>{person.name} <small>(#{person.id.slice(-4)})</small></span>
                <button 
                  onClick={() => recallPerson(person.id)}
                  style={{ padding: "5px 10px", fontSize: "0.8rem", background: "#f59e0b", color: "white" }}
                >
                  Recall
                </button>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  )
}

export default App