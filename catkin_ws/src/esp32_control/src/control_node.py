#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import serial

# Initialize Serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust the port as needed

def cmd_vel_callback(msg):
    linear = msg.linear.x
    angular = msg.angular.z
    command = f"{linear},{angular}\n"
    ser.write(command.encode())

def listener():
    rospy.init_node('control_node')
    rospy.Subscriber("cmd_vel", Twist, cmd_vel_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
