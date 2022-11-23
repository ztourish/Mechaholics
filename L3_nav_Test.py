import time as t
import L2_TOF_dataConversion as tof
import L1_TOF as L1tof
import L2_PID as pid
import numpy as np
import L2_Inverse_Kinematics as ik
import L2_Kinematics as k

u_in = int(input('Enter time to run in seconds:'))
for i in range(u_in * 10):
    start_time = t.time()
    dist2row = tof.angDist_avg() # [0] is l_dist, [1] is r_dist, [2] is l_theta, [3] is r_theta
    # max x_dot is 0.1
    theta_dot = np.radians([dist2row[3] - dist2row[2]])
    x_dot = 0.1- abs(theta_dot) 
    to_convert = [x_dot, theta_dot]
    pdt = ik.convert(to_convert)
    pdc = k.getPdCurrent()
    pid.driveClosedLoop(pdt, pdc)
L1tof.cleanup()
print('Exiting')
