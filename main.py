import cv2
import numpy as np
import pyautogui
import keyboard

def greenDetection(cap):
    # Python program for Detection of a  
    # specific color(blue here) using OpenCV with Python 
    #from https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/
    # Webcamera no 0 is used to capture the frames 
    #cap = cv2.VideoCapture(0)  
    # cap = cv2.VideoCapture(0)
    # #https://www.youtube.com/watch?v=gJgXsaj_gR0&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=10
    # #https://www.youtube.com/watch?v=BQE2TREDcoQ

    # if (cap.isOpened() == False):
    #     print("capture can't open")

    # while(cap.isOpened()):        
    # Captures the live stream frame-by-frame 
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_green = np.array([70,50,50]) 
    upper_green = np.array([90,255,255]) 
    # Here we are defining range of bluecolor in HSV 
    # This creates a mask of blue coloured  
    # objects found in the frame. 
    mask = cv2.inRange(hsv, lower_green, upper_green) 
    res = cv2.bitwise_and(frame,frame, mask= mask) 

    #there's an issue here somewhere
    #blackWhite = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        rect = cv2.boundingRect(c)
        if rect[2] < 15 or rect[3] < 15: continue
        x,y,w,h = rect
        #print(x,y,w,h)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        #cv2.imshow('frame',frame) 
        return (x, y)
    
# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res 
    #cv2.imshow('frame',frame) 
    #cv2.imshow('mask',mask) 
    #cv2.imshow('res',res) 
    
    # # Destroys all of the HighGUI windows. 
    # cv2.destroyAllWindows() 
    
    # # release the captured frame 
    # cap.release() 
    return None, None

def getScreenCoords(camX, camY, cap, screen):
    screenWidth, screenHeight = screen
    camWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    camHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    screenX = (camX / camWidth * screenWidth)
    screenY = (camY / camHeight * screenHeight)
    return screenX, screenY

if __name__ == "__main__":
    toggleMouse = False
    spaceCooldown = 0
    sCooldown = 0

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #https://www.youtube.com/watch?v=gJgXsaj_gR0&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=10
    #https://www.youtube.com/watch?v=BQE2TREDcoQ

    if (cap.isOpened() == False):
        print("capture can't open")

    while (cap.isOpened()):

        #quit is q
        if keyboard.is_pressed("p"):
            break
        
        x, y = greenDetection(cap)
        if x is not None and y is not None:
            lastX, lastY = x, y

        #toggle mouse following green with space key
        if keyboard.is_pressed(" ") and spaceCooldown == 0:
            print("space pressed!")
            toggleMouse = not toggleMouse
            spaceCooldown = 20

        if keyboard.is_pressed("m") and sCooldown == 0:
            pyautogui.click(pyautogui.position())
            sCooldown = 20

        spaceCooldown = max(0, spaceCooldown - 1)
        sCooldown = max(0, sCooldown - 1)

        if toggleMouse:
            screen = pyautogui.size()
            if x is not None and y is not None:
                pyautogui.moveTo(getScreenCoords(x, y, cap, screen))
            elif lastX is not None and lastY is not None:
                print("can't detect!")
                pyautogui.moveTo(getScreenCoords(lastX, lastY, cap, screen))
            else:
                print("can't detect!")
                pyautogui.moveTo(screen[0] // 2, screen[1] // 2)  

    # Destroys all of the HighGUI windows. 
    cv2.destroyAllWindows() 
    print("exiting!")
    # release the captured frame 
    cap.release()   
            
