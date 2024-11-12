import rospy
from geometry_msgs.msg import Twist
import socket

# ESP32 IP and port
ESP32_IP = "192.168.0.101"  # Replace with ESP32 IP if needed
ESP32_PORT = 4210

# Initialize UDP client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_cmd_vel(data):
    # Extract linear and angular velocities
    linear_x = data.linear.x
    angular_z = data.angular.z

    # Prepare the message
    message = f"{linear_x},{angular_z}".encode('utf-8')

    # Send message to ESP32
    sock.sendto(message, (ESP32_IP, ESP32_PORT))
    rospy.loginfo(f"Sent cmd_vel to ESP32: {message}")

def cmd_vel_listener():
    rospy.init_node('cmd_vel_listener', anonymous=True)
    rospy.Subscriber('/cmd_vel', Twist, send_cmd_vel)
    rospy.spin()

if __name__ == '__main__':
    try:
        cmd_vel_listener()
    except rospy.ROSInterruptException:
        pass
    finally:
        sock.close()

