# Left has address 40 and right has 41 (theoretical)
#Needed information: Default encoder address of our encoders
#Data resolution (8-bit, 14-bit, 20-bit?) - This changes the readEnc function, increasing or decreasing the start bit as compared to the end-bit (0xFF)

# Import external libraries
import Adafruit_GPIO.I2C as Adafruit_I2C        # for i2c communication functions
import time
import numpy as np                              # for handling arrays
import rospy
from std_msgs.msg import FloatArr

encL = Adafruit_I2C.Device(0x40, 1)             # encoder i2c address
encR = Adafruit_I2C.Device(0x41, 1)             # encoder i2c address


# The case of reading an individual encoder, primarily called by the Encoder read() function
def readEnc(channel):
    try:
        # The AS5048B encoder gives a 14 bit angular reading
        if channel == 'L':
            msB = encL.readU8(0xFE)    # capture the 8 msb's from encoder
            lsB = encL.readU8(0xFF)    # capture the 6 lsb's from encoder
        elif channel == "R":
            msB = encR.readU8(0xFE)    # capture the 8 msb's from encoder
            lsB = encR.readU8(0xFF)    # capture the 6 lsb's from encoder

        # lsB can contribute  at most 1.4 degrees to the reading
        # for msB, perform bitwise operation to get true scaling of these bits
        angle_raw = (msB << 6) | lsB

    except:
        print('Warning (I2C): Could not read encoder ' + channel)
        angle_raw = 0                           # set to zero, avoid sending wrong value
    return angle_raw                            # the returned value must be scaled by ( 359deg / 2^14 )


# The read() function returns both encoder values (RAW).
# Call this function from external programs.
def read():
    encLeft = readEnc('L')                      # call for left enc value
    encRight = readEnc('R')                     # call for right enc value
    encoders = np.array([encLeft, encRight])    # form array from left and right
    return encoders

def runEncoderPub():
    pub = rospy.Publisher('Encoder', FloatArr, queue_size=10)
    rospy.init_node('Encoder_Pub_Node', anonymous=True)
    rate = rospy.Rate(90) #Rate in Hz currently set for 90 readings per second
    rospy.loginfo("Encoder Publisher node started, now publishing")    
    while not rospy.is_shutdown():
        encoders = read()
        encoders = np.round((encoders * (360 / 2**14)), 2)      # scale values to get degrees
        msg = FloatArr
        msg.data = encoders
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        runEncoderPub()
    except rospy.ROSInterruptException:
        pass
#PID WILL EITHER UTILIZE PYTHON YIELD STATEMENT OR ROS PUBLISHERS/SUBSCRIBERS