import L1_TOF as TOF
import numpy as np
import os
import time as t

# min_dist = # enter minimum TOF 

def dist2rowapprox():
    # takes input from the 4 time-of-flight sensors. returns the approx. distance to each row, as well as
    # the angle of each row relative to the current orientation.
    distance = TOF.getRange()
    tof_spacing = 190 # Enter the space between the laser on each ToF sensor here in mm.
    tof_angle = np.radians(0) # Enter the rotational angle of the 4 ToF sensors here. Try to keep all angles identical.
                              # Perpendicular to driving direction = 0 deg.
    out = []   
    FL = distance[3]
    FR = distance[1]
    BL = distance[0]
    BR = distance[2]
    
    # left_dist = (np.cos(tof_angle) * (BL + FL))/2 # approx. dist of crop row relative to central perpendicular axis of robot. (coming out the side)
    # right_dist = (np.cos(tof_angle) * (BR + FR))/2
    out.append((np.cos(tof_angle) * (BL + FL))/2) # approx. dist of crop row relative to central perpendicular axis of robot. (coming out the side)
    out.append((np.cos(tof_angle) * (BR + FR))/2)

    # left_trig_base = tof_spacing + np.sin(tof_angle) * BL * FL # calculating the base of the triangle for trig (adjacent to theta).
    # left_trig_height = np.cos(tof_angle) * (FL - BL) # calculating the height of the triangle for trig (opposite to theta).
    # left_theta = np.arctan(left_trig_height / left_trig_base) # itan(opp/adj) reveals theta. np defaults to radians
    
    # left_theta = np.arctan(np.cos(tof_angle) * (FL - BL) / (tof_spacing + np.sin(tof_angle) * BL * FL))
    out.append(np.round(np.degrees(np.arctan(np.cos(tof_angle) * (FL - BL) / (tof_spacing + np.sin(tof_angle) * BL * FL))), 2))

    # right_trig_base = tof_spacing + np.sin(tof_angle) * BR * FR
    # right_trig_height = np.cos(tof_angle) * (FR - BR)
    # right_theta = np.arctan(right_trig_height / right_trig_base)
    
    # right_theta = np.arctan(np.cos(tof_angle) * (FR - BR) / (tof_spacing + np.sin(tof_angle) * BR * FR))
    out.append(np.round(np.degrees(np.arctan(np.cos(tof_angle) * (FR - BR) / (tof_spacing + np.sin(tof_angle) * BR * FR))), 2))


    # Positive value for theta = outward angle.
    # robot --> |_|   / <--crop row ->> positive right_theta
    # robot --> |_|   \ <--crop row ->> negative right_theta
    # Theta is in RADIANS!
    # return left_dist, right_dist, left_theta, right_theta
    return out

i = 0
mat = np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], 
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], 
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], 
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]])
def angDist_avg():
    curr = dist2rowapprox()
    mat [0][i] = curr[0]
    mat [1][i] = curr[1]
    mat [2][i] = curr[2]
    mat [3][i] = curr[3]

    left_dist_avg = np.nanmean(mat[0])
    right_dist_avg = np.nanmean(mat[1])
    left_theta_avg = np.nanmean(mat[2])
    right_theta_avg = np.nanmean(mat[3])
    if i >= 7:
        i = -1
    avgs = np.array([left_dist_avg, right_dist_avg, left_theta_avg, right_theta_avg])
    i += 1
    return avgs
    



# maybe, average the data points over a half second or so before performing these calculations? may help
# smooth these results.

if __name__ == "__main__":
    u_in = int(input('Enter time to run in seconds:'))
    for i in range(u_in * 10):
        start_time = t.time()
        dist2row = angDist_avg()
        print('----%s seconds to iterate----' % (t.time() - start_time))
        print('Left row distance:', dist2row[0], "mm.")
        print('Right row distance:', dist2row[1], 'mm.')
        print('Left row angle:', dist2row[2], 'degrees.')
        print('Right row angle:', dist2row[3], 'degrees.')
        t.sleep(0.5)
    TOF.cleanup()
    print('Exiting')
