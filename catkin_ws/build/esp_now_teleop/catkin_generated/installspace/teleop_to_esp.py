#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import espnow
import struct

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.init()
esp.add_peer(b'\xfc\xe8\xc0\x74\xa2\xd4')  # ESP32's MAC address

def cmd_vel_callback(msg):
    # Get linear and angular velocities from Twist message
    linear_x = msg.linear.x
    angular_z = msg.angular.z

    # Pack data as binary to match ESP32's struct_message structure
    data = struct.pack('ff', linear_x, angular_z)
    esp.send(data)
    rospy.loginfo(f"Sent linear_x: {linear_x}, angular_z: {angular_z}")

def listener():
    rospy.init_node('esp_now_teleop', anonymous=True)
    rospy.Subscriber("/cmd_vel", Twist, cmd_vel_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
