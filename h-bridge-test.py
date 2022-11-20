import RPi.GPIO as GPIO

IN1 = 18
IN2 = 12
IN3 = 13
IN4 = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
pwm_1 = GPIO.PWM(IN1, 5)
pwm_1.start(0)
GPIO.output(IN2, GPIO.LOW)
pwm_3 = GPIO.PWM(IN3, 5)
pwm_3.start(0)
GPIO.output(IN4, GPIO.LOW)
IN1_state = False
IN2_state = False
IN3_state = False
IN4_state = False

while(1):
    u_in = int(input("enter PWM pin to change (1, 2, 3, 4):"))
    if u_in == 1:
        IN1_state = not IN1_state
        GPIO.output(IN1, IN1_state)
    elif u_in == 2:
        IN2_state = not IN2_state
        GPIO.output(IN2, IN2_state)
    elif u_in == 3:
        IN3_state = not IN3_state
        GPIO.output(IN3, IN3_state)
    elif u_in == 4:
        IN4_state = not IN4_state
        GPIO.output(IN4, IN4_state)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        break
    print("In 1, 2, 3, 4:", IN1_state, IN2_state, IN3_state, IN4_state)

while(1):
    u_in = int(input("Enter duty cycle (0 - 100), -1 to change pwm frequency (Hz):"))
    
    if 0 <= u_in <= 100:
        pwm_1.ChangeDutyCycle(u_in)
        pwm_3.ChangeDutyCycle(u_in)
    elif u_in == -1:
        dc = float(input('Enter desired duty cycle in Hz:'))
        pwm_1.ChangeFrequency(dc)
        pwm_3.ChangeFrequency(dc)
    else:
        break

