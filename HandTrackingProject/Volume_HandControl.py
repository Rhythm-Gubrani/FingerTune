import cv2
import time
import numpy as np
import HandTracking_Module as htm  # Custom module for hand tracking
import math
# Pycaw is a Python library designed for controlling audio devices on Windows systems.
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Set up camera dimensions
wCam, hCam = 640, 480

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set camera width
cap.set(4, hCam)  # Set camera height
pTime = 0  # Previous time for FPS calculation

# Initialize hand detector with 0.7 confidence level
detector = htm.HandDetector(detectionCon=0.7)

# Initialize Pycaw for volume control on Windows
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get volume range (min and max volume levels)
volRange = volume.GetVolumeRange()
minVol = volRange[0]  # Minimum volume level (-63 dB)
maxVol = volRange[1]  # Maximum volume level (0 dB)

# Initialize variables for volume control
vol = 0  # Current volume level
volBar = 400  # Volume bar position (for visual representation)
volPer = 0  # Volume percentage

# Loop to continuously get frames from the camera
while True:
    success, img = cap.read()  # Read frame from camera
    img = detector.findHands(img)  # Detect hand in the frame
    lmlist = detector.findPosition(img, draw=False)  # Get landmark positions of the hand

    # If hand landmarks are detected
    if len(lmlist) != 0:
        # Get positions of thumb tip (landmark 4) and index finger tip (landmark 8)
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        
        # Calculate the center point between thumb and index finger
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circles at the tips of thumb and index finger, and a line between them
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Calculate the distance between thumb and index finger
        length = math.hypot(x2 - x1, y2 - y1)
        
        # Map the hand distance to the system volume range
        # Hand range: 50 - 300 (distance in pixels between thumb and index finger)
        # Volume range: -63 dB to 0 dB (system volume levels)
        vol = np.interp(length, [50, 100], [minVol, maxVol])
        volBar = np.interp(length, [50, 100], [400, 150])  # Visual volume bar
        volPer = np.interp(length, [50, 100], [0, 100])  # Volume percentage

        # Print the hand distance and the corresponding volume level
        print(int(length), vol)

        # Set the system volume based on the calculated volume level
        volume.SetMasterVolumeLevel(vol, None)

        # If the distance is small (indicating the hand is "pinched"), change the center circle to green
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Draw the volume bar and percentage on the screen
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)  # Static volume bar background
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)  # Dynamic volume level bar
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)  # Volume percentage text

    # Calculate FPS (Frames Per Second)
    cTime = time.time()  # Current time
    fps = 1 / (cTime - pTime)  # FPS calculation
    pTime = cTime  # Update previous time

    # Display FPS on the screen
    cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Show the image with the hand tracking and volume control
    cv2.imshow("Img", img)

    # Break loop if 'q' key is pressed
    cv2.waitKey(1)
