# adapted from Ryu Woon Jung (Leon)
# https://github.com/ROBOTIS-GIT/DynamixelSDK/blob/master/python/tests/protocol2_0/

#
# small one
# XL 430-W250
# id 1
# baud 57600
#

# big one
# PH54-200-S500-R
# id 1
# baud 57600
#


import os, time,sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--position", default=0, type=int, help="set goal position")
parser.add_argument("-v", "--velocity",  default=100, type=int, help="set velocity")

args = parser.parse_args()
print( "speed", args.velocity)
print( "position", args.position)



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

if 1:
    # XL430-W250
    # Control table address
    ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
    ADDR_PRO_GOAL_POSITION      = 116
    ADDR_PRO_PRESENT_POSITION   = 132
    ADDR_PRO_PROFILE_VELOCITY = 112
    ADDR_VELOCITY_LIMIT = 44

else:
    ADDR_PRO_TORQUE_ENABLE      = 512               # Control table address is different in Dynamixel model
    ADDR_PRO_GOAL_POSITION      = 564
    ADDR_PRO_PRESENT_POSITION   = 580
    ADDR_PRO_PROFILE_VELOCITY = 560
    ADDR_VELOCITY_LIMIT = 44
    ADDR_OPERATING_MODE = 11


TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 800000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold



speed = args.velocity

index = 0
goal_position = args.position






portHandler = PortHandler(DEVICENAME)
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

def write4(address, value):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, address, value)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        return False
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        return False
    return True

def write1(address, value):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, address, value)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        return False
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        return False
    return True

def read4(address):
    value, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, address)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return value


print("disable torque", write1(ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE))
# print("set extended control mode", write1(ADDR_OPERATING_MODE,4))
print("set velocity to", speed, write4(ADDR_VELOCITY_LIMIT, speed))
print("enable torque", write1(ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE))



write4( ADDR_PRO_GOAL_POSITION, goal_position) 

while 1:
    # Read present position
    present_position = read4(ADDR_PRO_PRESENT_POSITION)
    #if present_position > 2147483647:
    #    present_position -= 4294967296
    print("GoalPos: {}  PresPos: {} {}".format(goal_position, present_position, hex(present_position)))
    if not abs(goal_position- present_position) > DXL_MOVING_STATUS_THRESHOLD:
        break

print("disable torque")
write1(ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)

# Close port
portHandler.closePort()