#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Imu
import espnow

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.init()
esp.add_peer(b'\xFC\xE8\xC0\x74\xA2\xD4')  # Replace with the ESP32 MAC address

def parse_data(data):
    """Parse the incoming data from ESP into distance and IMU values."""
    try:
        values = data.decode('utf-8').split(',')
        distance = float(values[0])
        ax = float(values[1])
        ay = float(values[2])
        az = float(values[3])
        return distance, ax, ay, az
    except (ValueError, IndexError):
        rospy.logwarn("Received invalid data format.")
        return None, None, None, None

def sensor_node():
    rospy.init_node('sensor_node', anonymous=True)

    # Publishers
    distance_pub = rospy.Publisher('/sensor/distance', Float32, queue_size=10)
    imu_pub = rospy.Publisher('/sensor/imu', Imu, queue_size=10)

    rate = rospy.Rate(10)  # 10 Hz, adjust as needed

    while not rospy.is_shutdown():
        # Receive data from ESP32
        host, data = esp.recv()
        if data:
            distance, ax, ay, az = parse_data(data)

            if distance is not None:
                # Publish distance data
                distance_pub.publish(distance)
                rospy.loginfo(f"Distance: {distance} cm")

                # Publish IMU data
                imu_msg = Imu()
                imu_msg.linear_acceleration.x = ax
                imu_msg.linear_acceleration.y = ay
                imu_msg.linear_acceleration.z = az
                imu_pub.publish(imu_msg)
                rospy.loginfo(f"IMU Acceleration - ax: {ax}, ay: {ay}, az: {az}")

        rate.sleep()

if __name__ == '__main__':
    try:
        sensor_node()
    except rospy.ROSInterruptException:
        pass
