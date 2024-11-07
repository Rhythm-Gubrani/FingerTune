import cv2
import numpy as np
import time
import os
import HandTracking_Module as htm

folderPath = "Header"
mylist = os.listdir(folderPath)
# print(mylist)
overlayList = []

for imgPath in mylist:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)
# print(len(overlayList))

header = overlayList[0]
drawColor = (255,0,255)
brushThickness = 15 
xp,yp = 0,0
eraserThickness =  100

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1270)
detector = htm.HandDetector(detectionCon=0.85)
imgCanvas = np.zeros((720,1280,3),np.uint8)

while True:
    # 1.importing images
    success, img = cap.read()
    img = cv2.flip(img,1) #fliping the image


    # 2.Find hand landmarks
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        # print(lmlist)

        # tip of index and middle finger
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        # 3.Checking which fingers are up
        # works correctly with right hand
        fingers = detector.fingersUp()
        # print(fingers)
        
        # 4.If selection mode - two fingers are up - then we have to select
        if fingers[1] and fingers[2]:
            xp,yp = 0,0
            # print("Selection Mode")

            # checking for the click
            if y1<125: #we are in header
                if 250<x1<400:
                    header = overlayList[0]
                    drawColor = (255,0,255)
                elif 500<x1<700:
                    header = overlayList[1]
                    drawColor = (255,0,0)
                elif 800<x1<900:
                    header = overlayList[2]
                    drawColor = (0,255,0)
                elif 1000<x1<1200:
                    header = overlayList[3]
                    drawColor = (0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
             


        # 5.If drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),25,drawColor,cv2.FILLED)
            # print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp = x1,y1
            if drawColor == (0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            
            xp,yp = x1,y1
    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    # setting the header image
    img[0:125,0:1280] = header

    # blending the two images 
    img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image",img)
    # cv2.imshow("Canvas",imgCanvas)
    cv2.waitKey(1)

