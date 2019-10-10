#!usr/bin/env python
import rospy
import cv2
import numpy as np
from ball_detection.msg import ball_detection
import math
rospy.init_node('publisher')
pub = rospy.Publisher('ball_detection',ball_detection,queue_size=10)
clas=ball_detection()
def callback(x):
    pass
cv2.namedWindow('image1')
cap=cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FPS, 10)
fps = int(cap.get(5))
ilowH = 0
ihighH = 255
ilowS = 0
ihighS = 255
ilowV = 0
ihighV = 255
cv2.createTrackbar('lowH1', 'image1', ilowH, 179, callback)
cv2.createTrackbar('highH1', 'image1', ihighH, 179, callback)
cv2.createTrackbar('lowS1', 'image1', ilowS, 255, callback)
cv2.createTrackbar('highS1', 'image1', ihighS, 255, callback)
cv2.createTrackbar('lowV1', 'image1', ilowV, 255, callback)
cv2.createTrackbar('highV1', 'image1', ihighV, 255, callback)
while True:
    ret,frame=cap.read()
    ilowH1 = cv2.getTrackbarPos('lowH1', 'image1')
    ihighH1 = cv2.getTrackbarPos('highH1', 'image1')
    ilowS1 = cv2.getTrackbarPos('lowS1', 'image1')
    ihighS1 = cv2.getTrackbarPos('highS1', 'image1')
    ilowV1 = cv2.getTrackbarPos('lowV1', 'image1')
    ihighV1 = cv2.getTrackbarPos('highV1', 'image1')
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    low1=np.array([ilowH1,ilowS1,ilowV1])
    high1=np.array([ihighH1,ihighS1,ihighV1])
    img_mask1=cv2.inRange(hsv,low1,high1)
    output1=cv2.bitwise_and(frame,frame,mask=img_mask1)
    edged1 = cv2.Canny(output1, 100, 200)
    contours1, hierarchy = cv2.findContours(edged1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    frame_x, frame_y = frame.shape[:2]
    frame_x=frame_x/2
    frame_y=frame_y/2
    cv2.circle(output1,(frame_y,frame_x),3,(0,255,0),-1)
    for c in contours1:
        area1 = cv2.contourArea(c)
        if (area1 > 50):
            x, y, w, h = cv2.boundingRect(c)
            ball_x=(w/2)+x
            ball_y=(h/2)+y
            p=[ball_x,ball_y]
            q=[frame_x,frame_y]
            distance_x = int(p[0] - q[1])
            distance_y=int(-(p[1] - q[0]))
            clas.b=distance_x
	    clas.c=distance_y
            t = int(((2 * x + w) / 2))
            m = int((y + h / 2))
	    m=1
	    clas.d=m
	    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0))
            cv2.putText(frame,'ball detected',(t,m),cv2.FONT_HERSHEY_COMPLEX,0.5,(150,0,0),1,cv2.LINE_AA)
            if (h > 12 and h<25 and w > 12 and h<26):
                l=4
                clas.a=l
            if (h > 26 and h< 30 and w > 27 and w<30):
                l = 2
	        clas.a=l
            if (w > 31):
                l = 1
		clas.a=l 
	else:
	   l=0
	   clas.a=l
	   m=0
	   clas.d=m
    cv2.imshow("image1",output1)
    cv2.imshow("final",frame)
    pub.publish(clas)
    if (cv2.waitKey(1) == 13):
        break
cv2.destroyAllWindows()

