import L2_Kinematics as k
import numpy as np
import L1_MotorControl as m
import pandas as pd
import L1_Encoder as enc
import time as t

encR = 0x41
while True:
    u_in = int(input('Enter time to run both wheels fwd @ 80% \speed:'))
    m.MotorL(4400)
    m.MotorR(4400)
    pdcurrents = k.getPdCurrent()
    for i in range(u_in*44 - 1):
        newstack = k.getPdCurrent()
        pdcurrents = np.vstack((pdcurrents, newstack))
    
    m.MotorL(0)
    m.MotorR(0)
    DF = pd.DataFrame(pdcurrents)
    DF.to_csv("PDCurrents.csv")

