# SPEED IS EXPRESSED IN RPM
# Import external libraries
import RPi.GPIO as GPIO
import time                                     # only necessary if running this program as a loop
import numpy as np                              # for clip function
import rospy
from std_msgs.msg import FloatArr
global MOTOR_SPEED_MAX
MOTOR_SPEED_MAX = 5500                      #NEED TO MODIFY BASED UPON REAL MAX RPM*********************************
#RPi Software PWM Usage: soft_pwm = GPIO.PWM([pin], [freq])
#Software PWM Parameters: Frequency, Duty Cycle, Channel (pin)

tau = 1 #Electrical time constant of the motor
freq = 5/(2*np.pi*tau)
soft_PWM_L = GPIO.PWM(12, freq)                 #pin 18, Frequency dependent on motor electrical time constant
soft_PWM_R = GPIO.PWM(33, freq)
motor_L_direc = 32 #H-BRIDGE LEFT DIRECTION PIN
motor_R_direc = 35 #H-BRIDGE RIGHT DIRECTION PIN
GPIO.setup(motor_L_direc, GPIO.OUT)
GPIO.setup(motor_R_direc, GPIO.OUT)

def MotorControlStart():
    soft_PWM_L.start(0)
    soft_PWM_R.start(0)

# define functions to command motors, effectively controlling PWM
def MotorL(speed):                              #Speed should be RPM or RAD/S
    if speed < 0:
        duty = speed2Duty(speed*-1)
        soft_PWM_L.ChangeDutyCycle(duty)
        GPIO.output(motor_L_direc, LOW)
    else:    
        duty = speed2Duty(speed)
        soft_PWM_L.ChangeDutyCycle(duty)
        GPIO.output(motor_L_direc, HIGH)


def MotorR(speed):                              #Speed should be RPM or RAD/S
    if speed < 0:
        duty = speed2Duty(speed*-1)
        soft_PWM_R.ChangeDutyCycle(duty)
        GPIO.output(motor_R_direc, LOW)
    else:
        duty = speed2Duty(speed)
        soft_PWM_R.ChangeDutyCycle(duty)
        GPIO.output(motor_R_direc, HIGH)

def speed2Duty(speed):
    duty = speed/MOTOR_SPEED_MAX #NEEDS MODIFICATIONS
    return duty

def callback(data):
    MotorL(data.data[0])
    MotorR(data.data[1])

def listener():
    rospy.init_node('Motor_Control_Subscriber_Node', anonymous = True)
    rospy.Subscriber('Motor_Speeds', FloatArr, callback) #Three arguments: topic, message type, and callback function
    rospy.spin()

if __name__ == "__main__":
    MotorControlStart()
    try:
        listener()
    except rospy.ROSInterruptException:
        pass