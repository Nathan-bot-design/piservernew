#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

def ultrasonic_callback(data):
    rospy.loginfo(f"Received ultrasonic distance: {data.data}")

def ultrasonic_listener():
    rospy.init_node('ultrasonic_listener', anonymous=True)
    rospy.Subscriber('ultrasonic_distance', Float32, ultrasonic_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        ultrasonic_listener()
    except rospy.ROSInterruptException:
        pass
