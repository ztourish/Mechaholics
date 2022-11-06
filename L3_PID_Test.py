import numpy as np
import time
import csv

import L2_Inverse_Kinematics as ik
import L2_Kinematics as k
import L2_PID as pid

def writeFiles(pdc, pdt, timeKeep):
    txt = open("PDCL.txt", 'w+')         # file for phi dot left current
    txt2 = open("PDCR.txt", 'w+')        # file for phi dot right current
    txt3 = open("PDTL.txt", "w+")        # file for phi dot left target
    txt4 = open("PDTR.txt", "w+")        # file for phi dot right target
    txt5 = open("time.txt", "w+")        # file for time keeping when graphing
    pdcL = round(pdc[0], 2)
    pdcR = round(pdc[1], 2)
    txt.write(str(round(pdcL, 2)))
    txt2.write(str(round(pdcR, 2)))
    pdtL = round(pdt[0], 2)
    pdtR = round(pdt[1], 2)
    txt3.write(str(round(pdtL, 2)))
    txt4.write(str(round(pdtR, 2)))
    txt5.write(str(round(timeKeep, 3)))
    txt.close()
    txt2.close()
    txt3.close()
    txt4.close()
    txt5.close()

if __name__ == "__main__":
    while True:
        x_dot , theta_dot = ik.wait_user()                     # user input [x_dot,theta_dot]
        pdt = ik.convert(x_dot, theta_dot)
        pdc = k.getPdCurrent()
        pid.driveClosedLoop(pdt, pdc, 0)
        #timeKeepInitial = time.time()
        for i in range(10000):
            timeKeep = float(i)*0.01
            pdc = k.getPdCurrent()
            writeFiles(pdc, pdt, timeKeep)
            time.sleep(.01)