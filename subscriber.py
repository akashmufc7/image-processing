#!usr/bin/env python
import rospy
from ball_detection.msg import ball_detection
def callback(clas):
	print (clas.a)
        #print (clas.b)
        #print (clas.c)
	#print (clas.d)
rospy.init_node('subscriber')
sub = rospy.Subscriber('ball_detection',ball_detection, callback)
rospy.spin() 
