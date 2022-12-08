import time as t
import L2_TOF_dataConversion as tof # print statements removed
import L1_TOF as L1tof # print statements removed
import L2_PID as pid # print statements removed
import numpy as np
import L2_Inverse_Kinematics as ik # print statements removed
import L2_Kinematics as k # print statements removed
import L1_MotorControl as m # print statements removed
import L2_LiDAR_dataConversion as lidar # print statements removed


iter = 0
ground = 0.40 # y measurement for ground distance threshold from LiDAR
crash_prevent = 0.1 # When obstacles are too close to the
singlerow_distance = 0 # initializing single-row follower variable
singlerow_indicator = "" # initializing single-row follower variable
next_row_turn = "R" # initially turns to the right when no rows detected.
turn_distance_from_row = 0.35 # distance the robot should stay from the row it is turning with resepct to. (end of row distance)
no_row_timer = 0 # timer for no rows present condition, to ensure no row switching mid row

def sendToPID(x_dot, theta_dot):
    to_convert = [np.round(x_dot, 3), np.round(theta_dot, 3)]
    pdt = ik.convert(to_convert)
    pdc = k.getPdCurrent()
    pid.driveClosedLoop(pdt, pdc)

while 1: 
    try:

        closest_L_obstacle, closest_R_obstacle = lidar.find_closest_obstacles()
        #print(closest_L_obstacle, closest_R_obstacle, "closest l ground and closest r ground")
        
        if (closest_L_obstacle < crash_prevent) or (closest_R_obstacle > -crash_prevent): # Checking for imminent crash and averting course
            print("Imminent crash detected!")
            if closest_L_obstacle > abs(closest_R_obstacle):
                x_dot = -0.05
                theta_dot = 0.2
            elif closest_L_obstacle < abs(closest_R_obstacle):
                x_dot = -0.05
                theta_dot = -0.2
        elif (closest_L_obstacle < 0.6) and (closest_R_obstacle > -0.6): # Checking if both rows are present in scan
            print("Both rows present, ", end='')
            singlerow_distance = 0 # resetting singlerow distance when both rows are present again
            no_row_timer = 0 # resetting no_row_timer if no row was detected on previous iteration
            if -0.05 <= (closest_L_obstacle + closest_R_obstacle) <= 0.05: # if the distance between the rows is in an acceptable tolerance
                print("driving straight.")
                x_dot = 0.12
                theta_dot = 0
            elif closest_L_obstacle > abs(closest_R_obstacle): # if the right row is closer
                print("right row too close.")
                x_dot = 0.1
                theta_dot = 0.1
            elif closest_L_obstacle < abs(closest_R_obstacle): # if the left row is closer
                print("left row too close.")
                x_dot = 0.1
                theta_dot = -0.1
        elif (closest_L_obstacle > 0.6) and (closest_R_obstacle > -0.6): # If the left row is no longer scannable, follows right row
            print("Left row missing. Following right row.")
            no_row_timer = 0 # resetting no_row_timer if no row was detected on previous iteration
            if (singlerow_distance == 0) or (singlerow_indicator != 'R'): # setting singlerow distance and indicator for left row following
                singlerow_distance = closest_R_obstacle
                singlerow_indicator = 'R'
            if closest_R_obstacle > singlerow_distance: # turn left when row gets closer
                x_dot = 0.1
                theta_dot = 0.1
            elif closest_R_obstacle < singlerow_distance: # turn right when row gets farther
                x_dot = 0.1
                theta_dot = -0.1
            else: # this condition will likely never happen
                x_dot = 0.12
                theta_dot = 0
        elif (closest_L_obstacle < 0.6) and (closest_R_obstacle < -0.6): # If the right row is no longer scannable, do this 
            no_row_timer = 0 # resetting no_row_timer if no row was detected on previous iteration
            print("Right row missing. Following left row.")
            if (singlerow_distance == 0) or (singlerow_indicator != 'L'): # setting singlerow distanace and indicator for right row following
                singlerow_distance = closest_L_obstacle
                singlerow_indicator = 'L'
            if closest_L_obstacle < singlerow_distance: # turn right when row gets closer
                x_dot = 0.1
                theta_dot = -0.1
            elif closest_L_obstacle > singlerow_distance: # turn left when row gets farther
                x_dot = 0.1
                theta_dot = 0.1
            else: # this condition will likely never happen
                x_dot = 0.12
                theta_dot = 0
        else: # neither row is present, give a couple seconds to see if it will reappear. If not, then switch rows.
            if no_row_timer == 0: # counts the time in which both rows have dissappeared.
                no_row_timer = t.time()
            no_row_timer_calc = t.time() - no_row_timer
            if no_row_timer_calc < 2: # If no rows detected after 2 seconds, robot will attempt to switch rows.
                print("No rows detected for", no_row_timer_calc, "seconds.")
                x_dot = 0.12
                theta_dot = 0
            else:
                print("Neither row present. Switching rows to the ", end='')
                if next_row_turn == "R":
                    print("right.")
                    while closest_L_obstacle > 0.6:

                        closest_L_obstacle, closest_R_obstacle = lidar.find_closest_obstacles() # reacquire scans in the while loop

                        if abs(closest_R_obstacle) > turn_distance_from_row:
                            x_dot = 0
                            theta_dot = -0.3
                        elif abs(closest_R_obstacle) < turn_distance_from_row:
                            x_dot = 0.08
                            theta_dot = 0
                        
                        sendToPID(x_dot, theta_dot)

                    next_row_turn = "L" # set next row turn after while loop closes (left side is within tolerance)
                    print("New row acquired.")
                elif next_row_turn == "L":
                    print("left.")

                    while closest_R_obstacle < -0.6:

                        closest_L_obstacle, closest_R_obstacle = lidar.find_closest_obstacles() # reacquire scans in the while loop

                        if closest_L_obstacle > turn_distance_from_row:
                            x_dot = 0
                            theta_dot = 0.3
                        elif closest_L_obstacle < turn_distance_from_row:
                            x_dot = 0.08
                            theta_dot = 0
                        
                        sendToPID(x_dot, theta_dot)

                    next_row_turn = "R" # set next row turn after while loop closes (right side is within tolerance)
                    print("New row acquired.")
                

        sendToPID(x_dot, theta_dot)

    except KeyboardInterrupt:
        m.MotorL(0)
        m.MotorR(0)
        L1tof.cleanup()
        print('Exiting on Keyboard Interrupt.')
        break
