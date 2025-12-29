# dashboard.py
import streamlit as st
import cv2
import time
from main import run_queue_logic  # <-- LINKING MAIN.PY HERE

# ---------------------------------------------------------
# 1. UI CONFIGURATION (CSS & LAYOUT)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Queue Admin",
    page_icon="📡",
    layout="wide"
)

# Custom CSS for Professional Dark Look
st.markdown("""
<style>
    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        color: #aaaaaa;
        font-size: 14px;
    }
    [data-testid="stMetricValue"] {
        color: #00FF7F; /* Neon Green */
        font-size: 36px;
        font-weight: bold;
    }
    /* Button Styling */
    div.stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Control Panel")
    st.markdown("---")
    
    # Input Selection
    source_option = st.selectbox("Video Source", ["Webcam (Default)", "IP Camera / Video File"])
    
    src = 0  # Default Webcam
    if source_option == "IP Camera / Video File":
        src = st.text_input("Enter URL or Path", "video.mp4")
    
    # Model Settings
    conf_thresh = st.slider("AI Confidence", 0.1, 1.0, 0.35)
    
    st.markdown("---")
    start_btn = st.button("▶️ Start Monitoring")
    stop_btn = st.button("⏹️ Stop System")
    
    st.info("System linked to `main.py` backend.")

# ---------------------------------------------------------
# 3. MAIN DASHBOARD AREA
# ---------------------------------------------------------
st.title("📡 Live Queue Management System")
st.markdown("Real-time crowd analysis powered by **YOLOv8**")

# Placeholders for Layout
# Row 1: KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Create Empty Slots for Real-Time Updates
with kpi1:
    kpi_count = st.empty()
with kpi2:
    kpi_wait = st.empty()
with kpi3:
    kpi_status = st.empty()
with kpi4:
    kpi_fps = st.empty()

# Initial States
kpi_count.metric("People in Queue", "0")
kpi_wait.metric("Avg Wait Time", "0s")
kpi_status.metric("System Status", "Offline")
kpi_fps.metric("Processing FPS", "0")

st.markdown("---")

# Row 2: Video Feed & Graph
col_vid, col_graph = st.columns([2, 1])

with col_vid:
    st.subheader("📹 Live Camera Feed")
    video_placeholder = st.empty() # Video yahan aayega

with col_graph:
    st.subheader("📈 Live Density Trend")
    chart_placeholder = st.empty() # Graph yahan aayega
    
    st.subheader("📋 Activity Log")
    log_box = st.empty()

# --- FOOTER INJECTION ---
st.markdown("""
<div class="custom-footer">
    Made with ❤️ using <b>YOLOv8</b> & <b>Streamlit</b> | © 2025 Queue Management System
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. EXECUTION LOGIC
# ---------------------------------------------------------
if start_btn:
    kpi_status.metric("System Status", "Live 🟢")
    
    # Variables for FPS calculation
    prev_time = 0
    history_data = [] # Graph ke liye data store karenge

    # --- CALLING MAIN.PY LOGIC ---
    try:
        # Ye loop `main.py` se ek-ek frame maangega
        for frame, stats in run_queue_logic(source=src, conf=conf_thresh):
            
            # 1. Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
            prev_time = curr_time
            
            # 2. Update Video (Convert BGR to RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
            
            # 3. Update Metrics
            kpi_count.metric("People in Queue", stats['count'])
            
            # Color logic for Wait Time (Red if high)
            wait_val = stats['avg_wait']
            wait_label = f"{wait_val} sec"
            kpi_wait.metric("Avg Wait Time", wait_label)

            kpi_fps.metric("Processing FPS", f"{int(fps)}")
            
            # 4. Update Graph (Simple Line Chart)
            history_data.append(stats['count'])
            if len(history_data) > 50: history_data.pop(0) # Keep last 50 points
            chart_placeholder.line_chart(history_data)
            
            # 5. Update Log
            log_box.code(f"Active IDs: {stats['active_ids']}\nZone Config: Loaded")

            # Check for Stop (Streamlit button logic inside loop is tricky, usually requires rerun)
            # For simplicity, user must press 'Stop System' on sidebar which reloads page
            
    except Exception as e:
        st.error(f"Error connecting to Main.py: {e}")

if stop_btn:
    kpi_status.metric("System Status", "Stopped 🔴")
    st.warning("Monitoring Stopped.")