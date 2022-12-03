import numpy as np
import L1_Lidar as liscan
import math as m
#For testing purposes
import pandas as pd

#Downward angle of the 561 Lidar, from straight ahead, in degrees
down_angle = 0

#Number of scan points that you want the LiDAR to make
num_points = 54

def pol2cart(dist, ang):
	x = np.cos(np.radians(ang)) * dist
	y = np.sin(np.radians(ang)) * dist
	return(x, y)

def lidar_xy():
	scan = liscan.polarScan(num_points)
	dists, angs = np.hsplit(scan, 2)
	x, y = pol2cart(dists, angs)
	xy = np.hstack((x, y)) * np.cos(np.radians(down_angle))
	return xy
	# *** +X IS THE DRIVING DIRECTION! X=0 IS DIRECTLY IN FRONT OF LiDAR

	# At this stage, we have the x and y coordinates of the data points in from LiDAR.
	# Next, we need to isolate relevant data (i.e. remove outliers, ground in front)
	# and create 2 linear fit lines for the left and right rows of plants. Finally,
	# we will output the angle and distance to each linear fit line to show the angle
	# and distance from each plant row.
if __name__ == "__main__":
	xy = lidar_xy
	print(xy)
	DF = pd.DataFrame(xy)
	DF.to_csv("lidar_xy.csv")
