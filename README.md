# FingerTune

This project demonstrates a hand gesture recognition system that can control the system's volume using finger distance. The project is built using Python with OpenCV and the MediaPipe library for hand tracking, and Pycaw for controlling the system audio on Windows.

## Features
- Detects hand landmarks in real-time using a webcam.
- Uses finger movements (thumb and index finger) to control the system's volume.
- Visual feedback in the form of on-screen landmarks, connections between fingers, and a volume bar.
- Adjustable volume with smooth transitions based on hand gestures.

## Prerequisites

Make sure you have Python installed. You'll need the following Python packages:

- `opencv-python`: For handling video capture and image processing.
- `mediapipe`: For hand tracking and landmark detection.
- `pycaw`: For controlling system audio on Windows.
- `numpy`: For numerical operations.

## Installation

1. Clone the repository:
   `git clone https://github.com/yourusername/hand-gesture-volume-control.git`

2. Navigate to the project directory:
    `cd FingerTune`

3. Install the necessary dependencies:
    `pip install -r requirements.txt`

## Usage

- Make sure you have a working webcam connected to your system.
- Run the Python script to start controlling the volume: `python volume_handcontrol.py`
- Move your thumb and index finger closer or farther apart to adjust the volume. The closer they are, the lower the volume, and vice versa.
  
## How it Works

- The hand landmarks are detected using the MediaPipe library's Hands module.
- The distance between the thumb tip and index finger tip is calculated using simple geometry (math.hypot function).
- The calculated distance is then mapped to the system's volume range using NumPy's interp function.
- The system volume is adjusted dynamically by using the pycaw library

