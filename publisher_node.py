#This python script is for testing and reference when creating ROS publishers
import rospy
from std_msgs.msg import String
#Various message types, 
def talk_to_me():
    pub = rospy.Publisher('Topic_Name', String, queue_size=10)
    rospy.init_node('Publisher_Node', anonymous=True)
    rate = rospy.Rate(1) #Rate in Hz
    rospy.loginfo("Publisher node started, now publishing")
    while not rospy.is_shutdown():
        msg = "This message is published to topic - %s" % rospy.get_time()
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        talk_to_me()
    except rospy.ROSInterruptException:
        pass


#In  CMakeLists.txt, add a function under catkin_package for each python script we will execute
#catkin_install_python(PROGRAMS scripts/publisher_node.py
#   DESTINATION $(CATKIN_PACKAGE_BIN_DESTINATION)
# )