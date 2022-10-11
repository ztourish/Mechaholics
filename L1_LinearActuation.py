#GPIO Pin 25 BCM pin type
#Low default for retraction (no modulation as to distance of linear actuator)
#High - Extend at max
#Low - Retract
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Bool


def callback(data):
    rospy.loginfo("Received Data: %s", data.data)
    if data.data:
        GPIO.output(25, GPIO.HIGH)
    else:
        GPIO.output(25, GPIO.LOW)

def listener():
    rospy.init_node('Linear_Relay_Sub_Node', anonymous = True)
    rospy.Subscriber('Linear_Relay', Bool, callback) #Three arguments: topic, message type, and callback function
    rospy.spin()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25, GPIO.OUT)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass