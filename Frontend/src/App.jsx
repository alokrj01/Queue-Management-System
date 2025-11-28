import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState("");
  const [myTicket, setMyTicket] = useState(null);
  const [queueStatus, setQueueStatus] = useState({ waiting_count: 0 });

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/status")
        .then(response => response.json())
        .then(data => setQueueStatus(data))
        .catch(error => console.error("Error:", error));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

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
    });
  };

  const callNext = () => {
    fetch("http://127.0.0.1:8000/next", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.person) {
          alert(`Now Serving: ${data.person.name}`);
        } else {
          alert("No one is waiting.");
        }
      });
  };

  const markAbsent = () => {
    fetch("http://127.0.0.1:8000/skip", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.person) {
          alert(`Skipped: ${data.person.name}`);
        } else {
          alert("No one to skip.");
        }
      });
  };

  return (
    <div className="app-container">
      <div className="main-card">
        
        {/* HEADER */}
        <div className="header">
          <h1>Queue System</h1>
          <p>Smart Counter Management</p>
        </div>
        
        {/* BIG STATUS NUMBER */}
        <div className="status-box">
          <div className="status-label">Currently Waiting</div>
          <div className="status-number">{queueStatus.waiting_count}</div>
        </div>

        {/* CUSTOMER INPUT */}
        <div className="input-group">
          <input 
            type="text" 
            placeholder="Enter Visitor Name" 
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <button onClick={joinQueue} className="btn-primary">Generate Ticket</button>

        {/* TICKET DISPLAY */}
        {myTicket && (
          <div className="ticket-card">
            <div className="ticket-row">
              <span className="ticket-label">Name</span>
              <span className="ticket-value">{myTicket.name}</span>
            </div>
            <div className="ticket-row">
              <span className="ticket-label">Token ID</span>
              <span className="ticket-value">#{myTicket.id ? myTicket.id.slice(-4).toUpperCase() : "---"}</span>
            </div>
            
            {myTicket.estimated_wait_minutes !== undefined && (
              <div className="wait-time">
                ⏱ Est. Wait: {myTicket.estimated_wait_minutes} mins
              </div>
            )}
          </div>
        )}

        {/* STAFF CONTROLS */}
        <div className="staff-controls">
          <button onClick={callNext} className="btn-staff">
            Next
          </button>
          <button onClick={markAbsent} className="btn-danger">
            Absent
          </button>
        </div>

      </div>
    </div>
  )
}

export default App