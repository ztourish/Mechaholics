import time as t
import L2_TOF_dataConversion as tof
import L1_TOF as L1tof

u_in = int(input('Enter time to run in seconds:'))
for i in range(u_in * 10):
    start_time = t.time()
    dist2row = tof.angDist_avg()
    print('----%s seconds to iterate----' % (t.time() - start_time))
    print('Left row distance:', dist2row[0], "mm.")
    print('Right row distance:', dist2row[1], 'mm.')
    print('Left row angle:', dist2row[2], 'degrees.')
    print('Right row angle:', dist2row[3], 'degrees.')
    t.sleep(0.5)
L1tof.cleanup()
print('Exiting')
