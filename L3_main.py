import L2_PID as PID
import L1_Camera as cam
import L2_ClassifyImage as ml
import L1_LinearActuation as act
import L1_WeedeaterRelay as weed
import multiprocessing


# multiprocess for machine learning iterations goes here! 

while 1:
    # first, check the machine learning process to see if it has identified a weed.
    print(ml.getClassification)
    # second, run the sensors to find the angles and distances between the robot and the row.
    # here, we need to implement a check that tells whether or not the robot has reached the end of the row.
    # also, we need to implement collision detection here. This can be done with the LiDAR, and the TOF sensors.


    # Third, format the data from the sensors and feed into pid.driveClosedLoop() to drive the robot forwards in the row.
    # Consider a static loop that puts the robot into the next row. This could be done by polling the 4 TOFs from L1_TOF
    # to wait until there's normal values across all 4 TOFs (considering you're keeping the first row on the right, the right TOF sensors should
    # attempt to keep the distances equal at a base value while driving forwards. This will allow it to turn in a steady curve
    # around the crop row. Consider a variable that flip flops, so the same process can be done with the left TOF sensors to
    # continue down the crop field.)
    
    # The  program should loop here.