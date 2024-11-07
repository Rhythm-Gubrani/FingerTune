import cv2
import mediapipe as mp  # For hand tracking
import time  # To measure framerate (FPS)

# Define a class to detect hands using MediaPipe's Hands solution
class HandDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        # Initialize parameters for hand detection and tracking
        self.mode = mode  # Whether to use static image mode (False for video)
        self.maxHands = maxHands  # Maximum number of hands to detect
        self.model_complexity = model_complexity  # Complexity of the model used
        self.detectionCon = detectionCon  # Minimum detection confidence threshold
        self.trackCon = trackCon  # Minimum tracking confidence threshold

        # Initialize MediaPipe Hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon, self.trackCon)
        
        # Utility for drawing landmarks on the hand
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4,8,12,16,20]

    # Method to find hands in the given image
    def findHands(self, img, draw=True):
        # Convert the image to RGB (required by MediaPipe)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process the RGB image to find hand landmarks
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)  # Debugging: prints landmarks detected

        # If hands are detected, draw the landmarks on the image
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw hand landmarks and connections between them
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img  # Return the image with or without drawn landmarks
    
    # Method to find the position of landmarks for a specific hand
    def findPosition(self, img, handNo=0, draw=True):
        self.lmlist = []  # List to store the landmark positions (id, x, y)
        
        # If landmarks are detected
        if self.results.multi_hand_landmarks:
            # Get the landmarks of the specified hand (handNo)
            myhand = self.results.multi_hand_landmarks[handNo]
            
            # Enumerate over each landmark and get its id and position
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape  # Get image dimensions
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert normalized values to pixel coordinates
                # print(id, cx, cy)  # Debugging: prints the id and pixel position of the landmark
                self.lmlist.append([id, cx, cy])  # Add the id and coordinates to the list
                
                # Optionally draw a circle at the landmark position
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        
        return self.lmlist  # Return the list of landmarks (id, x, y)
    
    def fingersUp(self):
        fingers = []

        # thumb
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # 4 fingers
        for id in range(1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            
        return fingers


# Main function to run the hand detection on video
def main():
    pTime = 0  # Previous time (used to calculate FPS)
    cTime = 0  # Current time
    
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)
    
    # Create an instance of HandDetector
    detector = HandDetector()
    
    while True:
        success, img = cap.read()  # Capture each frame from the webcam
        
        # Find hands in the current frame
        img = detector.findHands(img)
        
        # Get the positions of hand landmarks (if any)
        lmlist = detector.findPosition(img)
        
        # If there are landmarks detected, print the coordinates of the 4th landmark (thumb tip)
        if len(lmlist) != 0:
            print(lmlist[4])  # Prints the position of the thumb tip
        
        # Calculate FPS
        cTime = time.time()  # Get current time
        fps = 1 / (cTime - pTime)  # Calculate the FPS
        pTime = cTime  # Update previous time
        
        # Display FPS on the image
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        # Show the frame with hand landmarks and FPS
        cv2.imshow("Image", img)
        
        # Wait for 1 millisecond and check if 'q' is pressed to quit
        cv2.waitKey(1)

# If this script is run directly, execute the main function
if __name__ == "__main__":
    main()
