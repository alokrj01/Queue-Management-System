import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState("");
  const [myTicket, setMyTicket] = useState(null);
  const [queueStatus, setQueueStatus] = useState({ waiting_count: 0 });

  // 1. Check Status Loop
  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/status")
        .then(response => response.json())
        .then(data => setQueueStatus(data))
        .catch(error => console.error("Error:", error));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // 2. Join Queue Function
  const joinQueue = () => {
    if (!name) return alert("Please enter your name");
    
    fetch("http://127.0.0.1:8000/join", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name })
    })
    .then(res => res.json())
    .then(data => {
      setMyTicket(data);
      setName(""); 
    })
    .catch(err => console.error("Join Error:", err));
  };

  // 3. Call Next Function
  const callNext = () => {
    fetch("http://127.0.0.1:8000/next", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.person) {
          alert(`📢 Now Serving: ${data.person.name}`);
        } else {
          alert("No one is waiting!");
        }
      })
      .catch(err => console.error("Next Error:", err));
  };

  return (
    <div className="app-container">
      <div className="card glass-effect">
        <h1 className="title">🏥 Queue Management System</h1>
        
        {/* DISPLAY BOARD */}
        <div className="status-board">
          <h2>People Waiting</h2>
          <div className="count-circle">{queueStatus.waiting_count}</div>
        </div>

        {/* CUSTOMER SECTION */}
        <div className="section customer-section">
          <h3>👋 Get a Ticket</h3>
          <div className="input-group">
            <input 
              type="text" 
              placeholder="Enter your name..." 
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <button onClick={joinQueue} className="btn-primary">Join Queue</button>
          </div>

          {/* TICKET DISPLAY */}
          {myTicket && (
            <div className="ticket fade-in">
              <div className="ticket-header">🎟️ YOUR TICKET</div>
              <div className="ticket-body">
                <p className="ticket-name">{myTicket.name}</p>
                <p className="ticket-id">ID: {myTicket.id ? myTicket.id.slice(-4) : "###"}</p>
                
                {/* AI PREDICTION DISPLAY - WITH SAFE CHECK */}
                {myTicket.estimated_wait_minutes !== undefined && (
                   <p style={{fontSize: "0.9em", color: "green", marginTop: "5px", fontWeight: "bold"}}>
                     ⏳ Est. Wait: {myTicket.estimated_wait_minutes} mins
                   </p>
                )}
                
                <span className="badge">Waiting</span>
              </div>
            </div>
          )}
        </div>

        {/* STAFF SECTION */}
        <div className="section staff-section">
          <h3>👮 Staff Control</h3>
          <button onClick={callNext} className="btn-success">
            📢 Call Next Customer
          </button>
        </div>
      </div>
    </div>
  )
}

export default App