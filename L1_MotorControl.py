# SPEED IS EXPRESSED IN RPM
# Import external libraries
import RPi.GPIO as GPIO
import time                                     # only necessary if running this program as a loop
import numpy as np                              # for clip function
global MOTOR_SPEED_MAX
MOTOR_SPEED_MAX = 5500                      #NEED TO MODIFY BASED UPON REAL MAX RPM*********************************
#RPi Software PWM Usage: soft_pwm = GPIO.PWM([pin], [freq])
#Software PWM Parameters: Frequency, Duty Cycle, Channel (pin)

tau = 1 #Electrical time constant of the motor
freq = 5/(2*np.pi*tau)
soft_PWM_L = GPIO.PWM(18, freq)                 #pin 18, Frequency dependent on motor electrical time constant
soft_PWM_R = GPIO.PWM(19, freq)

def MotorControlStart():
    soft_PWM_L.start(0)
    soft_PWM_R.start(0)

# define functions to command motors, effectively controlling PWM
def MotorL(speed):                              #Speed should be RPM or RAD/S
    if speed < 0:
        duty = speed2Duty(speed*-1)
        soft_PWM_L.ChangeDutyCycle(duty)    
    duty = speed2Duty(speed)
    soft_PWM_L.ChangeDutyCycle(duty)


def MotorR(speed):                              #Speed should be RPM or RAD/S
    if speed < 0:
        duty = speed2Duty(speed*-1)
        soft_PWM_R.ChangeDutyCycle(duty)
    duty = speed2Duty(speed)
    soft_PWM_R.ChangeDutyCycle(duty)

def speed2Duty(speed):
    duty = speed/MOTOR_SPEED_MAX #NEEDS MODIFICATIONS
    return duty
