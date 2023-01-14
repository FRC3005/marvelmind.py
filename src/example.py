from marvelmind import MarvelmindHedge
from time import sleep
import threading

from networktables import NetworkTables

import sys


def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

def main():

    if (len(sys.argv)>1):
        hedge.tty= sys.argv[1]

    hedge = MarvelmindHedge(tty = "/dev/ttyACM0", adr=None, debug=False) # create MarvelmindHedge thread

    cond = threading.Condition()
    notified = [False]

    # TODO: Add correect IP here
    NetworkTables.initialize(server='10.xx.xx.2')
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    with cond:
        print("Waiting for NetworkTables connection...")
        if not notified[0]:
            cond.wait()

    # Insert your processing code here
    print("Connected!")

    table = NetworkTablesInstance.getTable('SmartDashboard')

    
    hedge.start() # start thread
    while True:
        try:
            hedge.dataEvent.wait(1)
            hedge.dataEvent.clear()

            if (hedge.positionUpdated):
                hedge.print_position()
                table.putFloat("HedgePosX", hedge.position()[0])
                table.putFloat("HedgePosY", hedge.position()[1])
                table.putInt("HedgeTimestamp", int(hedge.position()[5] % 1000)) # time in MS
                
            if (hedge.distancesUpdated):
                hedge.print_distances()
                
            if (hedge.rawImuUpdated):
                hedge.print_raw_imu()
                
            if (hedge.fusionImuUpdated):
                hedge.print_imu_fusion()
                
            if (hedge.telemetryUpdated):
                hedge.print_telemetry()
                
            if (hedge.qualityUpdated):
                hedge.print_quality()
                
            if (hedge.waypointsUpdated):
                hedge.print_waypoint()
                
            if (hedge.userDataUpdated):
                hedge.print_user_data()
        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            sys.exit()
main()
