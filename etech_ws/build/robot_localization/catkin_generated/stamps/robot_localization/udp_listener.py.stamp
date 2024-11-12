#!/usr/bin/env python3

import rospy
import tf
import socket
import math
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from tf.transformations import quaternion_from_euler

# Robot parameters
ROBOT_WIDTH = 0.2  # 20 cm width
ROBOT_LENGTH = 0.3  # 30 cm length
LINEAR_SPEED = 0.1  # 1 m in 10 seconds
UDP_IP = "0.0.0.0"
UDP_PORT = 4211

# Initialize variables
yaw_angle = 0.0
x_pos = 0.0
y_pos = 0.0

def udp_listener():
    global yaw_angle
    rospy.init_node('udp_listener', anonymous=True)
    odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
    yaw_pub = rospy.Publisher('/mpu6050/yaw', Float32, queue_size=10)
    
    # Set up UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    rospy.loginfo("Listening for UDP packets on port %d" % UDP_PORT)
    rate = rospy.Rate(10)  # 10 Hz update rate
    
    # Initial odometry message
    odom = Odometry()
    odom.header.frame_id = "odom"
    odom.child_frame_id = "base_link"

    # Transform broadcaster to publish odometry transform
    odom_broadcaster = tf.TransformBroadcaster()

    while not rospy.is_shutdown():
        try:
            data, _ = sock.recvfrom(1024)
            yaw_angle = float(data.decode('utf-8'))
            rospy.loginfo("Received Yaw Angle: %f", yaw_angle)
            yaw_pub.publish(yaw_angle)
            
            # Update odometry
            update_odometry(odom, odom_pub, odom_broadcaster)
        except Exception as e:
            rospy.logwarn("Error receiving UDP packet: %s", e)
        rate.sleep()

def update_odometry(odom, odom_pub, odom_broadcaster):
    global x_pos, y_pos, yaw_angle
    
    # Calculate new position based on linear speed
    dt = 0.1  # Update interval in seconds (corresponds to 10 Hz)
    distance = LINEAR_SPEED * dt
    x_pos += distance * math.cos(math.radians(yaw_angle))
    y_pos += distance * math.sin(math.radians(yaw_angle))

    # Set the odometry pose
    odom.pose.pose.position.x = x_pos
    odom.pose.pose.position.y = y_pos
    quaternion = quaternion_from_euler(0, 0, math.radians(yaw_angle))
    odom.pose.pose.orientation.x = quaternion[0]
    odom.pose.pose.orientation.y = quaternion[1]
    odom.pose.pose.orientation.z = quaternion[2]
    odom.pose.pose.orientation.w = quaternion[3]

    # Publish odometry and transform
    odom.header.stamp = rospy.Time.now()
    odom_pub.publish(odom)
    odom_broadcaster.sendTransform(
        (x_pos, y_pos, 0),
        quaternion,
        rospy.Time.now(),
        "base_link",
        "odom"
    )

def teleop_listener():
    rospy.Subscriber("/cmd_vel", Twist, cmd_vel_callback)

def cmd_vel_callback(msg):
    global x_pos, y_pos, yaw_angle
    linear_x = msg.linear.x
    angular_z = msg.angular.z

    # Calculate linear movement based on cmd_vel input
    if linear_x != 0:
        # Update position with simulated linear movement
        distance = linear_x * 0.1  # Distance per update (10 Hz rate)
        x_pos += distance * math.cos(math.radians(yaw_angle))
        y_pos += distance * math.sin(math.radians(yaw_angle))

    if angular_z != 0:
        # Update yaw angle based on angular velocity
        yaw_angle += math.degrees(angular_z * 0.1)
        yaw_angle = yaw_angle % 360

if __name__ == "__main__":
    try:
        teleop_listener()  # Subscribe to teleop messages
        udp_listener()  # Start listening for MPU6050 data
    except rospy.ROSInterruptException:
        pass
