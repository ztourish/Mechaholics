#!/usr/bin/python

# This program relies on pimoroni's VL53L0X drivers for Raspberry Pi, found at:
# https://github.com/pimoroni/VL53L0X-python

import time
import VL53L0X
import RPi.GPIO as GPIO
import os
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

# !!!!!!!!!!!! This sequence needs to be ran each time the ToFs are powered on. Address is automatically set to 0x29 upon loss of power.

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
print('Initialized ToF Sensors')

# start ranging
tof.open()
time.sleep(0.50)
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
print('ToF 0 Ranging')
# start ranging
tof1.open()
time.sleep(0.50)
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
print('ToF 1 Ranging')
# start ranging
tof2.open()
time.sleep(0.50)
tof2.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
print('ToF 2 Ranging')
# start ranging
tof3.open()
time.sleep(0.50)
tof3.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
print('ToF 3 Ranging')

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))
count = 0
try:
    while 1:
        count += 1
        distance = tof.get_distance()
        if distance > 0:
            s1print = "sensor %d - %d mm" % (1, distance)
        else:
            s1print = "%d - Error" % 1

        distance = tof1.get_distance()
        if distance > 0:
            s2print = "sensor %d - %d mm" % (2, distance)
        else:
            s2print = "%d - Error" % 2

        distance = tof2.get_distance()
        if distance > 0:
            s3print = "sensor %d - %d mm" % (3, distance)
        else:
            s3print = "%d - Error" % 3

        distance = tof3.get_distance()
        if distance > 0:
            s4print = "sensor %d - %d mm" % (4, distance)
        else:
            s4print = "%d - Error" % 4
        print(s1print, s2print, s3print, s4print, "iteration", str(count))
# os.system('clear')
        time.sleep(timing/1000000.00)
except KeyboardInterrupt:
    print('Loop closed.')
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
