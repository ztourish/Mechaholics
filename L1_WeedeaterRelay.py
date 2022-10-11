#Simple I/O for turning on/off relay
#Pin is 18
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Bool
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(18, GPIO.OUT)


def callback(data):
    rospy.loginfo("Received Data: %s", data.data)
    if data.data:
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)

def listener():
    rospy.init_node('Weedeater_Relay_Sub_Node', anonymous = True)
    rospy.Subscriber('Weedeater_Relay', Bool, callback) #Three arguments: topic, message type, and callback function
    rospy.spin()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass