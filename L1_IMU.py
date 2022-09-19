#IMU Model: MPU9250IMU
import FaBo9Axis_MPU9250
import time
import sys
import rospy
from std_msgs.msg import MPU9250
mpu9250 = FaBo9Axis_MPU9250.MPU9250()


def startIMUPub():
    pub = rospy.Publisher('IMU', MPU9250, queue_size=10)
    rospy.init_node('IMU_Pub_Node', anonymous=True)
    rate = rospy.Rate(20) #Rate in Hz
    rospy.loginfo("IMU publisher node started, now publishing")
    while not rospy.is_shutdown():
        msg = MPU9250
        msg.accel = mpu9250.readAccel()
        msg.gyro = mpu9250.readGyro()
        msg.mag = mpu9250.readMag()
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        startIMUPub()
    except rospy.ROSInterruptException:
        pass