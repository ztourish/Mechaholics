# This file retrieves an image from the usb camera.
#important parameters: 256 pixel length and width (Specified by neural network inputs)
# Import external libraries

#***********************************************************************
# THE IMAGE MESSAGE TYPE IN THIS CODE DOES NOT WORK (I think), MUST BE CHANGED
#***********************************************************************
import cv2
from cv_brisge import CvBridge
import rospy
from sensor_msgs.msg import Image
# Initialize important vars
# width  = 240                      # desired width in pixels
# height = 160                      # desired height in pixels
width = 256                         # desired width in pixels
height = 256                         # desired height in pixels
camera = cv2.VideoCapture(0)        # Take images from the camera assigned as "0"


# A function to capture an image & return all pixel data
def newImage(size=(width, height)):
    ret, image = camera.read()          # return the image as well as ret
    if not ret:                         # (ret is a boolean for returned successfully?)
        print("NO IMAGE")
        return None                     # (return an empty var if the image could not be captured)
    image = cv2.resize(image, size)     # reduce size of image
    return image

def runCameraPub():
    pub = rospy.Publisher('Camera', Image, queue_size=10)
    rospy.init_node('Camnera_Pub_Node', anonymous=True)
    rate = rospy.Rate(1) #Rate in Hz
    br = CvBridge()
    rospy.loginfo("Image Publisher node started, now publishing")
    while not rospy.is_shutdown():
        msg = newImage()
        pub.publish(br.cv2_to_imgmsg(msg))
        rate.sleep()

if __name__ == "__main__":
    try:
        runCameraPub()
    except rospy.ROSInterruptException:
        pass
