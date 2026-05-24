#pip install ultralytics streamlit plotly pandas opencv-python
#python -m streamlit run traffic.py


streamlit run app.py

import streamlit as st
import cv2
from ultralytics import YOLO
import plotly.express as px
import pandas as pd
from datetime import datetime
import time

# Page Configuration
st.set_page_config(page_title="SmartFlow AI", layout="wide")
st.title("🚦 SmartFlow AI - Intelligent Traffic Management System")
st.markdown("**Real-time AI Based Traffic Analysis**")

# Load YOLO Model
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# Video Upload
st.sidebar.header("Upload Video")
uploaded_file = st.sidebar.file_uploader("Apni Traffic Video Upload Kare", 
                                       type=["mp4", "avi", "mov"])

if uploaded_file is None:
    st.info("👈 Sidebar mein video upload karo")
    st.stop()

# Save uploaded video
with open("uploaded_traffic_video.mp4", "wb") as f:
    f.write(uploaded_file.getbuffer())

st.success("✅ Video Uploaded Successfully!")

# Main Layout
col1, col2 = st.columns([3, 2])

with col1:
    stframe = st.empty()

with col2:
    st.subheader("📊 Live Traffic Analysis")
    chart_placeholder = st.empty()
    metric_placeholder = st.empty()

# Video Processing
cap = cv2.VideoCapture("uploaded_traffic_video.mp4")

vehicle_counts = []
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 3 != 0:
        continue

    # AI Detection
    results = model(frame, conf=0.45, verbose=False)
    
    count = 0
    for result in results:
        for box in result.boxes:
            cls_name = result.names[int(box.cls[0])]
            if cls_name in ['car', 'truck', 'bus', 'motorcycle', 'bicycle']:
                count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    vehicle_counts.append({"Time": datetime.now().strftime("%H:%M:%S"), "Vehicles": count})

    # Show Video Frame
    stframe.image(frame, channels="BGR", use_container_width=True)

    # Update Chart
    df = pd.DataFrame(vehicle_counts[-30:])
    fig = px.line(df, x="Time", y="Vehicles", title="Real-time Traffic Density")
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Show Stats
    status = "🔴 High Traffic" if count > 15 else "🟢 Normal Traffic"
    metric_placeholder.metric("Vehicles Detected", count, delta=status)

    time.sleep(0.1)

cap.release()
st.success("🎉 Video Processing Completed!")