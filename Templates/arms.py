from pynaoqi_mate import Robot
from configuration import PepperConfiguration
import qi
import math
import time
import almath
import motion

minShoulderPitch = -119.5
maxShoulderPitch = 119.5
minShoulderAngle = 0.5
maxShoulderAngle = 89.5
minElbowYaw = -119.5
maxElbowYaw = 119.5
minElbowRoll = 0.5
maxElbowRoll = 89.5


virtualRobotConfig = PepperConfiguration("Amber")
myRobot = Robot(virtualRobotConfig)

myRobot.ALRobotPosture.goToPosture("StandInit", 1)

actualShoulderAngle = minShoulderAngle
while actualShoulderAngle < maxShoulderAngle:
    print("Change RShoulderRoll & LShoulderRoll to " + str(actualShoulderAngle) + " Degrees")
    myRobot.ALMotion.changeAngles("LShoulderRoll", math.radians(actualShoulderAngle), 1)
    myRobot.ALMotion.changeAngles("RShoulderRoll", math.radians(-actualShoulderAngle), 1)
    actualShoulderAngle = actualShoulderAngle + 5
    time.sleep(0.5)

actualShoulderPitch = minShoulderPitch
while actualShoulderPitch < maxShoulderPitch:
    print("Change RShoulderPitch & LShoulderPitch to " + str(actualShoulderPitch) + " Degrees")
    myRobot.ALMotion.changeAngles("LShoulderPitch", math.radians(actualShoulderPitch), 1)
    myRobot.ALMotion.changeAngles("RShoulderPitch", math.radians(actualShoulderPitch), 1)
    actualShoulderPitch = actualShoulderPitch + 10
    time.sleep(0.5)

actualElbowYaw = minElbowYaw
while actualElbowYaw < maxElbowYaw:
    print("Change RElbowYaw & LElbowYaw to " + str(actualElbowYaw) + " Degrees")
    myRobot.ALMotion.changeAngles("LElbowYaw", math.radians(actualElbowYaw), 1)
    myRobot.ALMotion.changeAngles("RElbowYaw", math.radians(-actualElbowYaw), 1)
    actualElbowYaw = actualElbowYaw + 10
    time.sleep(0.5)

actualElbowRoll = minElbowRoll
while actualElbowRoll < maxElbowRoll:
    print("Change RElbowRoll & LElbowRoll to " + str(actualElbowRoll) + " Degrees")
    myRobot.ALMotion.changeAngles("LElbowRoll", math.radians(actualElbowRoll), 1)
    myRobot.ALMotion.changeAngles("RElbowRoll", math.radians(-actualElbowRoll), 1)
    actualElbowRoll = actualElbowRoll + 5
    time.sleep(0.5)

i = 0
while i < 5:
    myRobot.ALMotion.closeHand("RHand")
    myRobot.ALMotion.closeHand("LHand")
    time.sleep(1)
    myRobot.ALMotion.openHand("RHand")
    myRobot.ALMotion.openHand("LHand")
    time.sleep(1)
    i = i + 1

frame = motion.FRAME_ROBOT
effectorList = ["LArm", "RArm"]
axisMaskList = [motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL]
timeList     = [[1.0], [1.0]]         # seconds

dy = 0.04
pathList = []
targetLArmTf = almath.Transform(myRobot.ALMotion.getTransform("LArm", frame, False))
targetLArmTf.r2_c4 -= dy
pathList.append(list(targetLArmTf.toVector()))

targetLArmTf = almath.Transform(myRobot.ALMotion.getTransform("RArm", frame, False))
targetLArmTf.r2_c4 -= dy
pathList.append(list(targetLArmTf.toVector()))

myRobot.ALMotion.transformInterpolation("RArm", frame, pathList, 63, timeList, True)