#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
import socket

# Define UDP IP and port
UDP_IP = "0.0.0.0"  # Listen on specific network interface
UDP_PORT = 4211

def mpu6050_listener():
    rospy.init_node('mpu6050_listener', anonymous=True)
    pub = rospy.Publisher('mpu6050/yaw', Float32, queue_size=10)

    # Set up UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    rospy.loginfo("Listening for UDP packets on port %d" % UDP_PORT)

    while not rospy.is_shutdown():
        try:
            data, _ = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            yaw_angle = float(data.decode('utf-8'))
            rospy.loginfo("Received Yaw Angle: %f", yaw_angle)
            pub.publish(yaw_angle)
        except Exception as e:
            rospy.logwarn("Error receiving UDP packet: %s", e)

if __name__ == "__main__":
    try:
        mpu6050_listener()
    except rospy.ROSInterruptException:
        pass

