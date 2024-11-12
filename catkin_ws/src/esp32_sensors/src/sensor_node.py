#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu, Range
from std_msgs.msg import Float32
import serial

# Initialize Serial connection to ESP32
ser = serial.Serial('/dev/ttyACM0', 115200)  # Adjust the port as needed

def read_data():
    while not rospy.is_shutdown():
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            distance, angle = data.split(',')
            publish_ultrasonic(float(distance))
            publish_imu(float(angle))
        rospy.sleep(0.1)

def publish_ultrasonic(distance):
    ultrasonic_msg = Range()
    ultrasonic_msg.range = distance
    ultrasonic_pub.publish(ultrasonic_msg)

def publish_imu(angle_z):
    imu_msg = Imu()
    imu_msg.angular_velocity.z = angle_z
    imu_pub.publish(imu_msg)

if __name__ == '__main__':
    rospy.init_node('sensor_node')
    ultrasonic_pub = rospy.Publisher('ultrasonic', Range, queue_size=10)
    imu_pub = rospy.Publisher('imu', Imu, queue_size=10)
    
    try:
        read_data()
    except rospy.ROSInterruptException:
        pass
