# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 09:25:28 2020

@author: Stanisław Wasilewski
"""


import win32api
import cv2

face_cascade = cv2.CascadeClassifier('face1.xml')
cap = cv2.VideoCapture(0)

#Trying smiling detector
smile_cascade = cv2.CascadeClassifier('smile.xml')

x_bef = 500
y_bef = 200


while(True):
    
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smile = smile_cascade.detectMultiScale(gray, 1.3, 5)
    face_cascade = cv2.CascadeClassifier('face1.xml')
    final_face = face_cascade.detectMultiScale(gray, 1.3, 5)
    is_face = (len(final_face) != 0)
    
    if is_face == False:
        print("Trying alt face")
        face_cascade = cv2.CascadeClassifier('face_alt.xml')
        final_face = face_cascade.detectMultiScale(gray, 1.3, 5)
        is_face = (len(final_face) != 0)
        print("Trying side face")
        if is_face == False:
            face_cascade = cv2.CascadeClassifier('side_face.xml')
            final_face = face_cascade.detectMultiScale(gray, 1.3, 5)
            print("What the heck there is no face")
            
    #setting the cursor
    if is_face == True:
        y_final = y_bef*4
        x_final = x_bef
        x_final = 975 - ((4*x_bef) - 975)
        win32api.SetCursorPos((x_final, y_final))
        
    
    
    for (x,y,w,h) in final_face:
        gray = cv2.rectangle(frame,(x,y),(x+w,y+h),(65, 252, 3),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(gray,'TWARZ',(x, y-10), font, 0.6, (113, 35, 255), 2, cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        smile = smile_cascade.detectMultiScale(gray, 1.3, 5)
        for (sx,sy,sw,sh) in smile:
            cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,255,0),2)
        x_bef = x
        y_bef = y
        
  
    cv2.imshow('twarzodetektor',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        cap.release()
        cv2.destroyAllWindows()
