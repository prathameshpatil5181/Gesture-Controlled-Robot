import cv2
import serial
import time
import handtrackingmodule as htm

wcam,hcam = 640,480
cap = cv2.VideoCapture(0)

cap.set(3,wcam)
cap.set(4,hcam)
pTime = 0;
cTime = 0;
detector = htm.handDetector(detectionCon=0.75)

direction = ['stop','forward','back','left','right','rotate']
tipIds= [4,8,12,16,20]

serialcom = serial.Serial('COM12',115200)
serialcom.timeout = 1

while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList  =detector.findPosition(img,draw=False)
    # print(lmList)

    if len(lmList)!=0 :
        finger =[]

        # thumb cheak
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)

        # finger cheak
        for id in range (1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                finger.append(1)
            else :
                finger.append(0)

        totalfingers = finger.count(1)
        # print(direction[totalfingers])
        cv2.putText(img, direction[totalfingers], (320, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        i = direction[totalfingers]+'\n'
        # print(i)

        time.sleep(3/1000)
        serialcom.write(i.encode())


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)