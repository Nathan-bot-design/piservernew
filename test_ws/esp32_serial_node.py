#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu, Range
import serial

# Initialize serial connection to ESP32
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

def cmd_vel_callback(msg):
    # Interpret Twist message from teleoperation
    if msg.linear.x > 0:
        ser.write(b'F')
    elif msg.linear.x < 0:
        ser.write(b'B')
    elif msg.angular.z > 0:
        ser.write(b'L')
    elif msg.angular.z < 0:
        ser.write(b'R')
    else:
        ser.write(b'S')  # Stop if no command

def read_sensor_data():
    # Read from serial and publish to ROS topics
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        if data.startswith("DATA"):
            try:
                # Parse and publish distance and acceleration data
                _, distance, ax, ay, az = data.split(',')
                distance = float(distance)
                ax, ay, az = float(ax), float(ay), float(az)
                
                # Publish distance as Range message
                range_msg = Range()
                range_msg.header.stamp = rospy.Time.now()
                range_msg.range = distance
                range_msg.min_range = 0.02  # Example min range
                range_msg.max_range = 4.0   # Example max range
                range_pub.publish(range_msg)
                
                # Publish IMU data
                imu_msg = Imu()
                imu_msg.header.stamp = rospy.Time.now()
                imu_msg.linear_acceleration.x = ax
                imu_msg.linear_acceleration.y = ay
                imu_msg.linear_acceleration.z = az
                imu_pub.publish(imu_msg)

                rospy.loginfo(f"Published Range: {distance} and IMU data: {ax}, {ay}, {az}")

            except ValueError as e:
                rospy.logwarn(f"Failed to parse sensor data: {data} | Error: {e}")

if __name__ == '__main__':
    rospy.init_node('esp32_serial_node')

    # Setup subscribers and publishers
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)
    range_pub = rospy.Publisher('/ultrasonic_range', Range, queue_size=10)
    imu_pub = rospy.Publisher('/imu/data', Imu, queue_size=10)

    rate = rospy.Rate(10)  # 10 Hz loop rate

    # Main loop to read sensor data and publish to ROS
    while not rospy.is_shutdown():
        read_sensor_data()
        rate.sleep()
