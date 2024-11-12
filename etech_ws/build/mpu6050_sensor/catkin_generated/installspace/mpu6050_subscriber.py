#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

def mpu6050_callback(data):
    rospy.loginfo("Received Yaw Angle: %f", data.data)

def mpu6050_listener():
    rospy.init_node('mpu6050_listener', anonymous=True)
    rospy.Subscriber('yaw_angle', Float32, mpu6050_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        mpu6050_listener()
    except rospy.ROSInterruptException:
        pass
