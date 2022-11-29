from picamera import PiCamera
import time as t
import cv2

camera = PiCamera()
t.sleep(1)
print('Initialized camera.')

camera.resolution = (1280, 720)
camera.vflip = True

file_name = "/home/pi/Documents/programs/img.jpg"

def imgTake():
	camera.capture(file_name)



if __name__ == "__main__":
	imgTake()
	print("Exiting.")
