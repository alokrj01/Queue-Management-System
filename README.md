<div align="center">

# 📹 AI-Powered Smart Queue Management System
### Real-time Crowd Analytics & Wait-Time Estimation using Computer Vision

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object_Detection-orange?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=for-the-badge&logo=opencv)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)

<br/>

![Project Demo](demo_gif_placeholder.gif) 

<br/>

**A privacy-focused Edge AI solution designed to monitor queues, calculate average wait times, and optimize service efficiency without sending video feeds to the cloud.**

[View Demo Video](YOUR_YOUTUBE_LINK_HERE) • [Report Bug](YOUR_GITHUB_ISSUES_LINK) • [Request Feature](YOUR_GITHUB_ISSUES_LINK)

</div>

---

## 🚀 Key Features

This system replaces manual headcounts with automated, AI-driven analytics.

* **🕵️ Real-Time Tracking:** Uses **YOLOv8 + ByteTrack** to assign unique IDs to individuals and track them across frames.
* **⏱️ Dynamic Wait-Time Calculation:** Automatically calculates how long each person has been standing in the queue zone.
* **🛠️ Custom Zone Configuration:** Includes a **GUI Admin Tool** (`setup_zone.py`) that allows users to draw the queue area on *any* camera feed using mouse clicks. Coordinates are saved in `JSON` for persistence.
* **📊 Interactive Dashboard:** A professional **Streamlit** web interface to view live feeds, KPIs (Key Performance Indicators), and activity logs.
* **🔒 Privacy First:** Processes video streams locally (Edge Computing), ensuring no sensitive footage leaves the premises.

---

## 🏗️ System Architecture

I designed the project using the **MVC (Model-View-Controller)** pattern to ensure scalability.

| Component | File Name | Description |
| :--- | :--- | :--- |
| **Frontend (View)** | `dashboard.py` | A Streamlit-based web dashboard for end-users to monitor stats. |
| **Backend (Controller)** | `main.py` | Contains the core logic for Object Detection, tracking algorithms, and math calculations. |
| **Configuration (Model)** | `setup_zone.py` | An admin utility to define the ROI (Region of Interest) and save it to `config.json`. |
| **Data Store** | `config.json` | Stores deployment-specific settings like Zone Coordinates and Camera Source ID. |

---

## ⚙️ Installation & Setup

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/alokrj01/Queue-Management-System](https://github.com/alokrj01/Queue-Management-System)
cd Queue-Management-System
```

### 2. Install Dependencies
```bash
[pip install -r requirements.txt](pip install -r requirements.txt)
```

### 3. Configure the Queue Zone (One-Time Setup)

Run the admin tool to define where the queue is located in your camera frame.
```bash
[python setup_zone.py](python setup_zone.py)
```

Click 4 points on the camera window to draw the polygon and press 'q' to save.

after that, run command;
```bash
[python main.py](python main.py)
```

### 4. Run the Dashboard

Launch the web application.
```bash
[streamlit run dashboard.py](streamlit run dashboard.py)
```

## 🧠 Technical Challenges Solved
1. The "Camera Angle" Problem
Challenge: Every CCTV camera is installed at a different height and angle. Hardcoding coordinates (e.g., x=100, y=200) made the code fail on new cameras. Solution: I built a generic setup_zone.py tool. It captures mouse clicks to generate a custom polygon and saves it to a config.json file. The main system reads this file dynamically, making the software Plug-and-Play.

2. Occlusion & ID Switching
Challenge: In crowded lines, people hide behind each other, causing the detector to lose them and reset their timer. Solution: Implemented Object Tracking (persist=True) logic and optimized the confidence threshold. I also added a memory buffer that retains a person's ID for a few frames even if detection flickers.

### 🔮 Future Improvements
[1] Integration with SQL Database for historical reporting.

[2] Add SMS/WhatsApp Alerts if wait time exceeds 10 minutes.

[3] Deploy on NVIDIA Jetson Nano for standalone edge device usage.

<div align="center"> Made with ❤️ by Alok Ranjan </div>
