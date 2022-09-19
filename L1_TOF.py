#!/usr/bin/python

# This program relies on pimoroni's VL53L0X drivers for Raspberry Pi, found at:
# https://github.com/pimoroni/VL53L0X-python

import time
import VL53L0X
import RPi.GPIO as GPIO
import os
import rospy
from std_msgs.msg import FloatArr #TESTING REQUIRED TO VERIFY FUNCTIONALITY OF IMPORT SINCE FLOATARR IS A CUSTOM MESSAGE TYPE
# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16
# GPIO for Sensor 3 shutdown pin
sensor3_shutdown = 26
# GPIO for Sensor 4 shutdown pin
sensor4_shutdown = 21


GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)
GPIO.setup(sensor3_shutdown, GPIO.OUT)
GPIO.setup(sensor4_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)
GPIO.output(sensor3_shutdown, GPIO.LOW)
GPIO.output(sensor4_shutdown, GPIO.LOW)


# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof1 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof2 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
tof3 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)

# Set shutdown pin high for the first VL53L0X
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(1)
# Set new address for the first VL53L0X
tof.change_address(0x2B)

# Set shutdown pin high for the second VL53L0X
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(1)
# Set new address for the second VL53L0X
tof1.change_address(0x2D)

# Set shutdown pin high for the third VL53L0X
GPIO.output(sensor3_shutdown, GPIO.HIGH)
time.sleep(1)
# Set new address for the third VL53L0X
tof2.change_address(0x2F)

# Set shutdown pin high for the fourth VL53L0X
GPIO.output(sensor4_shutdown, GPIO.HIGH)
time.sleep(1)
# Set new address for the fourth VL53L0X
tof3.change_address(0x31)
rospy.loginfo('Initialized ToF Sensors')

# start ranging
tof.open()
time.sleep(0.50)
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
rospy.loginfo('ToF 0 Ranging Start')
# start ranging
tof1.open()
time.sleep(0.50)
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
rospy.loginfo('ToF 1 Ranging Start')
# start ranging
tof2.open()
time.sleep(0.50)
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
rospy.loginfo('ToF 2 Ranging Start')
# start ranging
tof3.open()
time.sleep(0.50)
tof3.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
rospy.loginfo('ToF 3 Ranging Start')

def getRange():
    distance = [tof.get_distance(), tof1.get_distance(), tof2.get_distance(), tof3.get_distance()]
    return distance

if __name__ == "__main__":
    timing = tof.get_timing()
    if timing < 20000:
        timing = 20000
    rospy.loginfo("TOF Timing %d ms" % (timing/1000))

    pub = rospy.Publisher('TOF', FloatArr, queue_size=10)
    rospy.init_node('TOF_Node', anonymous=True)
    rate = rospy.Rate(1/timing)
    rospy.loginfo("TOF Node started, Publishing")

    count = 0
    try:
        while not rospy.is_shutdown():
            distance = getRange()
            if distance[0] > 0 and distance[1] > 0 and distance[2] > 0 and distance[3] > 0:
                tof_data = FloatArr
                tof_data.data = distance
                pub.publish(tof_data)
                rate.sleep()
            else:
                rospy.loginfo("TOF Sensor Error - Diagnosis required")
    except rospy.ROSInterruptException:
        rospy.loginfo('ROSPYInterruptException')
        pass
    tof3.stop_ranging()
    GPIO.output(sensor4_shutdown, GPIO.LOW)
    tof2.stop_ranging()
    GPIO.output(sensor3_shutdown, GPIO.LOW)
    tof1.stop_ranging()
    GPIO.output(sensor2_shutdown, GPIO.LOW)
    tof.stop_ranging()
    GPIO.output(sensor1_shutdown, GPIO.LOW)
    tof.close()
    tof1.close()
    tof2.close()
    tof3.close()
