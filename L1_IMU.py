#IMU Model: MPU9250IMU
import mpu6050
import time
import sys
mpu = mpu6050(0x68) #PUT ADDRESS OF IMU HERE, DEFAULT IS 0x68


def getIMUData():
        arr = [mpu.get_accel_data(), mpu.get_gyro_data(), mpu.get_temp()]
        return arr

if __name__ == "__main__":
    while(1):
        print("IMU Data: ", getIMUData())