#This python script is for testing and reference when creating ROS Subscribers
import rospy
from std_msgs.msg import String
#Various message types, 

def callback(data):
    rospy.loginfo("Received Data: %s", data.data)

def listener():
    rospy.init_node('Subscriber_Node', anonymous = True)
    rospy.Subscriber('Topic_Name', String, callback) #Three arguments: topic, message type, and callback function
    rospy.spin()

if __name__ == "__main__":
    try:
        listener()
    except rospy.ROSInterruptException:
        pass