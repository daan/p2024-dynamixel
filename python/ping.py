# adapted from Ryu Woon Jung (Leon)
# https://github.com/ROBOTIS-GIT/DynamixelSDK/blob/master/python/tests/protocol2_0/ping.py

#
# my small one
# XL 430-W250
# id 1
# baud 57600
#

import os

from dynamixel_sdk import *                 # Uses Dynamixel SDK library
from serial_device import *


PROTOCOL_VERSION        = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                  = 1                 # Dynamixel ID : 1
BAUDRATE                = 57600             # Dynamixel default baudrate : 57600

DEVICENAME =  get_ports_with_vid(1027)[-1] 
print(DEVICENAME)
# DEVICENAME              = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()

# Try to ping the Dynamixel
# Get Dynamixel model number
dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, DXL_ID)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("[ID:%03d] ping Succeeded. Dynamixel model number : %d" % (DXL_ID, dxl_model_number))

# Close port
portHandler.closePort()