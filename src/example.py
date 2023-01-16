from marvelmind import MarvelmindHedge
from time import sleep
import threading

from networktables import NetworkTables

import sys


cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

def main():

    if (len(sys.argv)>1):
        hedge.tty= sys.argv[1]

    hedge = MarvelmindHedge(tty = "/dev/tty.usbmodem2063348E52321", adr=None, debug=False) # create MarvelmindHedge thread

    # TODO: Add correect IP here
    NetworkTables.initialize(server='10.30.5.2')
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    with cond:
        print("Waiting for NetworkTables connection...")
        if not notified[0]:
            cond.wait()

    # Insert your processing code here
    print("Connected!")

    table = NetworkTables.getTable('SmartDashboard')

    
    hedge.start() # start thread
    while True:
        try:
            hedge.dataEvent.wait(1)
            hedge.dataEvent.clear()

            if (hedge.positionUpdated):
                hedge.print_position()
                table.putNumberArray("HedgePos", [hedge.position()[1], hedge.position()[2], hedge.position()[4]]) # X, Y, angle
                table.putNumber("HedgePosZ", hedge.position()[3])
                table.putNumber("HedgeTimestamp", hedge.position()[5])
                
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
