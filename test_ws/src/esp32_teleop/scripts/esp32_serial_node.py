#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
import serial

# Initialize serial communication with ESP32
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

def send_command_to_esp32(command):
    if ser.is_open:
        ser.write(command.encode())

def callback(cmd_vel):
    if cmd_vel.linear.x > 0:
        send_command_to_esp32('F')
    elif cmd_vel.linear.x < 0:
        send_command_to_esp32('B')
    elif cmd_vel.angular.z > 0:
        send_command_to_esp32('L')
    elif cmd_vel.angular.z < 0:
        send_command_to_esp32('R')
    else:
        send_command_to_esp32('S')

def publish_sensor_data():
    pub = rospy.Publisher('/sensor_data', Range, queue_size=10)
    rate = rospy.Rate(1)  # Set the publishing rate to 1 Hz
    while not rospy.is_shutdown():
        if ser.is_open and ser.in_waiting > 0:
            line = ser.readline().decode(errors='ignore').strip()
            if line.startswith("DATA"):
                _, distance, ax, ay, az = line.split(',')
                msg = Range()
                msg.range = float(distance)
                pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('esp32_serial_node', anonymous=True)
    rospy.Subscriber('/cmd_vel', Twist, callback)
    publish_sensor_data()
