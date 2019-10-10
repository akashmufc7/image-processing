#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Twist
from ball_detection.msg import ball_detection
import time


rospy.init_node('ball_follower')
out=Twist()
p_error=0
count=0
flag_reached=0

def stop():
	out.linear.x=0
	out.angular.z=0
	print("goal reached!!!!!")

def find_ball():
	out.linear.x=0
	out.angular.z=140
	print("Finding ball")
	#stop()
			

def callback(msg,pub):
	global p_error
	global out
	global count
	global flag_reached	
	error=msg.b
	kd=0
	kp=0.8
	if(flag_reached==1):
		stop()
		print("goal reached!!!!!")
	elif(msg.d==1):
		count=0
		d_error=p_error-error
		t_error=kp*error+kd*d_error
		out.angular.z=t_error

		if(out.angular.z<140 and out.angular.z>0):
			out.angular.z=140
			print("setting angle")
		if(out.angular.z>-140 and out.angular.z<0):
			out.angular.z=-140
			print("setting angle")
		if(t_error<80 and t_error>-80):
			if(msg.a==1):
				out.linear.x=0
				out.angular.z=0
				print("goal reached!!!!!")
				flag_reached=1
			elif(msg.a==2):
				out.linear.x=150
				out.angular.z=0
				flag_reached=0
				print("going forward:")
				
			else:	
				out.linear.x=200
				out.angular.z=0
				flag_reached=0
				print("going forward:")
			
			
		'''
		if(out.angular.z>10):
			out.angular.z=10
		if(out.angular.z<-10):
			out.angular.z=-10

		'''
		if(out.angular.z!=0):
			out.linear.x=0
			#print("Setting angle:")
	else:
		#count=0
		if(count==30):
			find_ball()
		else:
			count=count+1
		
			
		
	pub.publish(out)
	
pub=rospy.Publisher('cmd_vel',Twist,queue_size=100)
sub=rospy.Subscriber('ball_detection',ball_detection,callback,pub)

rospy.spin()
