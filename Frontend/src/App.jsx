import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState("");
  const [myTicket, setMyTicket] = useState(null);
  const [queueStatus, setQueueStatus] = useState({ waiting_count: 0 });

  // 1. Automatically check the queue status every 2 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/status")
        .then(response => response.json())
        .then(data => setQueueStatus(data))
        .catch(error => console.error("Error fetching status:", error));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // 2. Function to Join the Queue
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
      setName(""); // Clear the input box
    });
  };

  // 3. Function for Staff to Call Next
  const callNext = () => {
    fetch("http://127.0.0.1:8000/next", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        if (data.person) {
          alert(`📢 Now Serving: ${data.person.name}`);
        } else {
          alert("No one is waiting!");
        }
      });
  };

  return (
    <div className="App" style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🏥 Queue Management System</h1>
      
      {/* SECTION 1: THE DISPLAY BOARD */}
      <div style={{ border: "2px solid #333", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
        <h2>People Waiting: {queueStatus.waiting_count}</h2>
      </div>

      {/* SECTION 2: CUSTOMER KIOSK */}
      <div style={{ marginBottom: "40px" }}>
        <h3>👋 Customer: Get a Ticket</h3>
        <input 
          type="text" 
          placeholder="Enter your name" 
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ padding: "10px", fontSize: "16px", marginRight: "10px" }}
        />
        <button onClick={joinQueue} style={{ padding: "10px 20px", fontSize: "16px", cursor: "pointer" }}>
          Get Ticket
        </button>

        {myTicket && (
          <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#e0f7fa", color: "black" }}>
            <h3>🎟️ Your Ticket</h3>
            <p><strong>Name:</strong> {myTicket.name}</p>
            <p><strong>Status:</strong> {myTicket.status}</p>
            <p><strong>ID:</strong> {myTicket.id}</p>
          </div>
        )}
      </div>

      <hr />

      {/* SECTION 3: STAFF DASHBOARD */}
      <div style={{ marginTop: "20px", backgroundColor: "#f0f0f0", padding: "20px", borderRadius: "10px", color: "black" }}>
        <h3>👮 Staff Control</h3>
        <button onClick={callNext} style={{ padding: "15px 30px", fontSize: "18px", backgroundColor: "green", color: "white", cursor: "pointer" }}>
          📢 Call Next Customer
        </button>
      </div>
    </div>
  )
}

export default App