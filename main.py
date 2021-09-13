import cv2
import numpy as np


if __name__ == "__main__":
    # Python program for Detection of a  
    # specific color(blue here) using OpenCV with Python 
    #from https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/
    # Webcamera no 0 is used to capture the frames 
    #cap = cv2.VideoCapture(0)  
    cap = cv2.VideoCapture(0)
    #https://www.youtube.com/watch?v=gJgXsaj_gR0&list=PLGmxyVGSCDKvmLInHxJ9VdiwEb82Lxd2E&index=10
    #https://www.youtube.com/watch?v=BQE2TREDcoQ

    if (cap.isOpened() == False):
        print("capture can't open")

    while(cap.isOpened()):        
        # Captures the live stream frame-by-frame 
        _, frame = cap.read()  
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
            print(x,y,w,h)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        
    # The bitwise and of the frame and mask is done so  
    # that only the blue coloured objects are highlighted  
    # and stored in res 
        cv2.imshow('frame',frame) 
        cv2.imshow('mask',mask) 
        cv2.imshow('res',res) 
    
    # This displays the frame, mask  
    # and res which we created in 3 separate windows. 
        if (cv2.waitKey(25) & 0xFF== ord('q')):
            break
    
    # Destroys all of the HighGUI windows. 
    cv2.destroyAllWindows() 
    
    # release the captured frame 
    cap.release() 