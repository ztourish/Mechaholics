#Simple I/O for turning on/off relay
#Pin is 18
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


def setRelay(data):
    if data:
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)

if __name__ == "__main__":
    while 1:
        u_in = bool(input("Give 1 (on) or 0 (off) to control Weedeater Relay: "))
        setRelay(u_in)