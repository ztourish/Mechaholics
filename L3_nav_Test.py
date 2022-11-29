import time as t
import L2_TOF_dataConversion as tof
import L1_TOF as L1tof
import L2_PID as pid
import numpy as np
import L2_Inverse_Kinematics as ik
import L2_Kinematics as k
import L1_MotorControl as m

row_count = 0
iter = 0
while 1:
    try:
        start_time = t.time()
        dist2row, iter = tof.angDist_avg(iter) # [0] is l_dist, [1] is r_dist, [2] is l_theta, [3] is r_theta
        # max x_dot is 0.1
        dist_diff = dist2row[1] - dist2row[0]
        theta_dot = dist_diff / 80 + np.radians(dist2row[3])
        if abs(theta_dot) >= 0.5:
            sign = np.sign(theta_dot)
            theta_dot = 0.5 * sign  
        x_dot = 0.1 - abs(theta_dot) / 10
        if x_dot < 0:
            x_dot = 0
        to_convert = [x_dot, theta_dot]
        pdt = ik.convert(to_convert)
        pdc = k.getPdCurrent()
        pid.driveClosedLoop(pdt, pdc)

    except KeyboardInterrupt:
        m.MotorL(0)
        m.MotorR(0)
        L1tof.cleanup()
        print('Exiting on Keyboard Interrupt.')
        break
