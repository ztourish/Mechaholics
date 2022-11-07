import numpy as np
import time
import csv

import L2_Inverse_Kinematics as ik
import L2_Kinematics as k
import L2_PID as pid

if __name__ == "__main__":
    filename = 'PDL.csv'
    filename2 = 'PDR.csv'
    headerL = ['time', 'pdcl', 'pdtl']
    headerR = ['time', 'pdcr', 'pdtr']
    fileL = open(filename, 'w', newline="")
    fileR = open(filename2, 'w', newline = "")
    csvwriterL = csv.writer(fileL)
    csvwriterR = csv.writer(fileR)
    csvwriterL.writerow(headerL)
    csvwriterR.writerow(headerR)
    while True:
        x_dot , theta_dot = ik.wait_user()                     # user input [x_dot,theta_dot]
        pdt = ik.convert(x_dot, theta_dot)
        pdc = k.getPdCurrent()
        pid.driveClosedLoop(pdt, pdc, 0)
        #timeKeepInitial = time.time()
        for i in range(10000):
            timeKeep = float(i)*0.01
            pdc = k.getPdCurrent()
            dataL = [timeKeep, pdc[0], pdt[0]]
            dataR = [timeKeep, pdc[1], pdt[1]]
            csvwriterL.writerow(dataL)
            csvwriterR.writerow(dataR)  
            time.sleep(.01)