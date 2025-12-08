import { useState, useEffect } from 'react';
import './App.css'; 

// Unicode icons for clean look
const UserIcon = "👤"; 
const NextIcon = "👉";
const SkipIcon = "❌";
const TicketIcon = "🎟️"; // Added for visitor ticket button

function App() {
  const [name, setName] = useState("");
  const [myTicket, setMyTicket] = useState(null); 
  const [queueStatus, setQueueStatus] = useState({ waiting_count: 0, now_serving: null });
  const [viewMode, setViewMode] = useState('staff'); 
  const [isLoggedIn, setIsLoggedIn] = useState(false); 

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // --- API/Polling Logic ---
  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/status")
        .then(response => response.json())
        .then(data => setQueueStatus(data))
        .catch(error => console.error("Error fetching status:", error));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // --- Backend Interaction Functions (Kept simple) ---
  const joinQueue = () => {
    if (!name.trim()) return alert("Please enter your name");
    fetch("http://127.0.0.1:8000/join", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: name.trim() }) })
    .then(res => res.json())
    .then(data => { setMyTicket(data); setName(""); });
  };
  const callNext = () => { fetch("http://127.0.0.1:8000/next", { method: "POST" }); };
  const markAbsent = () => { fetch("http://127.0.0.1:8000/skip", { method: "POST" }); };
  const formatTokenId = (id) => { return id ? id.slice(-4).toUpperCase() : "----"; };

  const handleLogin = (e) => {
      e.preventDefault();
      if (username === 'staff' && password === 'admin') {
          setIsLoggedIn(true);
          setUsername(''); // Clear fields on success
          setPassword('');
      } else {
          alert("Invalid credentials (try staff/admin)");
      }
  };

  // --- Components ---

  const StaffLoginForm = () => (
      <form className="login-form-queue" onSubmit={handleLogin}>
          <div className="header-queue">
              <h1 className="queue-logo">QUEUE</h1>
              <p className="queue-slogan">Say goodbye to long lines and hello to **hassle-free service**</p>
          </div>

          <input 
              className="input-queue"
              type="text" 
              placeholder="Username" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
          />
          <input
              className="input-queue"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
          />

          <button type="submit" className="btn-queue btn-primary-black">
              Login
          </button>

          <div className="login-links-queue">
              <a href="#" className="link-queue">Register</a>
              <span className="link-separator-queue">|</span>
              <a href="#" className="link-queue">Forgot password</a>
          </div>
      </form>
  );

  const StaffControls = ({ status }) => (
    <>
      <div className="header-queue">
          <h1 className="queue-logo">QUEUE</h1>
          <p className="queue-slogan">Staff Control Panel</p>
          <button onClick={() => setIsLoggedIn(false)} className="btn-logout-queue">Logout</button>
      </div>
      
      <div className="status-card-queue">
        <div className="status-label-queue">CURRENTLY WAITING</div>
        <div className="status-number-large-queue">{status.waiting_count}</div>
      </div>
      
      <div className="serving-card-queue">
        <p className="serving-label-queue">NOW SERVING</p>
        <h3 className="serving-name-queue">
          {status.now_serving ? status.now_serving.name : "Waiting for Next"}
        </h3>
        {status.now_serving && (
            <p className="serving-token-queue">Token: #{formatTokenId(status.now_serving.id)}</p>
        )}
      </div>

      <div className="staff-controls-queue">
        <button onClick={callNext} className="btn-queue btn-accent-green" disabled={status.waiting_count === 0}>
          {NextIcon} Next
        </button>
        <button onClick={markAbsent} className="btn-queue btn-secondary-grey" disabled={!status.now_serving && status.waiting_count === 0}>
          {SkipIcon} Absent
        </button>
      </div>
    </>
  );

  const VisitorView = () => (
    <>
      <div className="header-queue">
          <h1 className="queue-logo">QUEUE</h1>
          <p className="queue-slogan">Welcome! Get your ticket below.</p>
      </div>
      
      <div className="status-card-queue">
        <div className="status-label-queue">CURRENTLY WAITING</div>
        <div className="status-number-large-queue">{queueStatus.waiting_count}</div>
      </div>
      
      {!myTicket && (
        <>
          <input type="text" placeholder="Enter Your Name" className="input-queue" value={name} onChange={(e) => setName(e.target.value)}/>
          <button onClick={joinQueue} className="btn-queue btn-accent-purple">
            {TicketIcon} Generate Ticket
          </button>
        </>
      )}

      {myTicket && (
        <div className="ticket-display-queue-visitor">
            <p>Name: **{myTicket.name}**</p>
            <p>Your Token: <span className="ticket-value-highlight">#{formatTokenId(myTicket.id)}</span></p>
            <p>Your Position: <span className="ticket-value-highlight">{myTicket.position}</span></p>
            <button onClick={() => setMyTicket(null)} className="btn-queue btn-secondary-grey">
                 Clear Ticket
            </button>
        </div>
      )}
    </>
  );

  return (
    <div className="outer-container-behance"> {/* This will handle the full-screen background */}
      <div className="app-main-card-behance"> {/* This is the centered interface */}
        
        {/* VIEW TOGGLE */}
        <div className="view-toggle-queue">
            <button className={viewMode === 'visitor' ? 'toggle-active' : ''} onClick={() => setViewMode('visitor')}>Visitor</button>
            <button className={viewMode === 'staff' ? 'toggle-active' : ''} onClick={() => setViewMode('staff')}>Staff</button>
        </div>
        
        {/* MAIN PANEL CONTENT */}
        <div className="main-panel-content-queue">
            {viewMode === 'staff' ? (
                isLoggedIn ? <StaffControls status={queueStatus} /> : <StaffLoginForm />
            ) : (
                <VisitorView />
            )}
        </div>
        
      </div>
    </div>
  )
}

export default App
