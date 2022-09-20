#IMU Model: MPU9250IMU
import mpu6050
import time
import sys
import rospy
from std_msgs.msg import MPU6050
mpu = mpu6050(0x68) #PUT ADDRESS OF IMU HERE, DEFAULT IS 0x68


def startIMUPub():
    pub = rospy.Publisher('IMU', MPU6050, queue_size=10)
    rospy.init_node('IMU_Pub_Node', anonymous=True)
    rate = rospy.Rate(20) #Rate in Hz
    rospy.loginfo("IMU publisher node started, now publishing")
    while not rospy.is_shutdown():
        msg = MPU6050
        msg.accel = mpu.get_accel_data()
        msg.gyro = mpu.get_gyro_data()
        msg.temp = mpu.get_temp()
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        startIMUPub()
    except rospy.ROSInterruptException:
        pass