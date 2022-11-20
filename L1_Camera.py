from picamera import PiCamera
import time as t
import cv2

camera = PiCamera()
t.sleep(1)
print('Initialized camera.')

camera.resolution = (1280, 720)
camera.vflip = True

file_name = "/home/pi/%NAME OF FILEPATH%/img.jpg"

def imgTake():
	camera.capture(file_name)
	img = cv2.imread(file_name)
	output = cv2.resize(img, (256, 256))
	cv2.imwrite(file_name, output)