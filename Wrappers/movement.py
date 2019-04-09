from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from enum import Enum

import qi
import time
import motion
import math

class Actuators(Enum):
    LArm = 1
    RArm = 2
    BOTH = 3
    HIPS = 4
    ALL = 5

class Quantity(Enum):
    QUARTER = 1
    HALF = 2
    FULL = 3

# setAngles:            Sets angles
# changeAngles:         Changes Angles
# angleInterpolation:   Interpolates one or multiple joints to a target angle or along timed trajectories

class Movement(object):
    def __init__(self, myRobot):
        super(Movement,self).__init__()

        session = myRobot.session

        self.motion_service = session.service("ALMotion")
        self.navigation_service = session.service("ALNavigation")
        self.posture_service = session.service("ALRobotPosture")
        self.tracker_service = session.service("ALTracker")
        self.aLife = session.service("ALAutonomousLife")

        # Using 10% of maximum joint speed
        self.fractionMaxSpeed = 0.1

        self.headJointNames = ["HeadYaw","HeadPitch"]

        self.armJointNamesL = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        self.armJointNamesR = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]

        self.hipsJointNames = ["HipRoll","HipPitch"]

        self.WRISTYAWMIN = -104.5
        self.WRISTYAWMAX = 104.5

        self.ELBOWYAWMIN = -119.5
        self.ELBOWYAWMAX = 119.5

        self.isTracking = False

    def enableCollisionProtection(self, enabled):
        self.motion_service.setExternalCollisionProtectionEnabled("All", enabled)
        self.motion_service.setCollisionProtectionEnabled("Arms", enabled)
        self.motion_service.setExternalCollisionProtectionEnabled("Arms", enabled)
        self.motion_service.setExternalCollisionProtectionEnabled("LArm", enabled)
        self.motion_service.setExternalCollisionProtectionEnabled("RArm", enabled)

        print('enabled collision protection: {}'.format(enabled))

    def enableAutonomousLife(self, enabled):
        # to disable whole autonomous life
        # connect to robot via ssh
        # nao stop
        # naoqi-bin --disable-life
        self.aLife.setAutonomousAbilityEnabled("BackgroundMovement", enabled)
        self.aLife.setAutonomousAbilityEnabled("BasicAwareness", enabled)
        self.aLife.setAutonomousAbilityEnabled("ListeningMovement", enabled)
        self.aLife.setAutonomousAbilityEnabled("SpeakingMovement", enabled)

        self.motion_service.setIdlePostureEnabled('Body', enabled)
        self.motion_service.setBreathEnabled('Body',enabled)

        print('enabled autonomous life: {}'.format(enabled))

    def enableMoveArms(self, enabled):
        self.motion_service.setMoveArmsEnabled(enabled, enabled)

    def initialPosition(self):
        self.posture_service.goToPosture("StandInit", self.fractionMaxSpeed)
        self.moveHeadDown(40)

    def initialPositionStand(self):
        self.posture_service.goToPosture("Stand", self.fractionMaxSpeed)

    def initialPositionMoving(self):
        self.moveShoulderRight(Actuators.RArm, 119.5)
        #self.moveShoulderLeft(Actuators.LArm, 119.5)

    def rest(self):
        self.motion_service.rest()

    def initialPositionGrabbing(self):
        self.initialPosition()
        self.moveHeadDown(30)

        self.moveElbowRight(Actuators.RArm, 89.5)
        self.moveShoulderRight(Actuators.RArm, 89.5)

        time.sleep(2)

        self.moveArmsUp(Actuators.RArm, 80)

        time.sleep(2)

        self.moveShoulderLeft(Actuators.RArm, 89.5)

        time.sleep(2)

        self.rotateElbowLeft(Actuators.RArm, 80)
        self.rotateWristRight(Actuators.RArm, 100)

    def initialPositionGrabbingBothHands(self):
        self.initialPosition()
        self.moveHeadDown(50)

        self.moveElbowRight(Actuators.RArm, 89.5)
        self.moveElbowLeft(Actuators.LArm, 89.5)

        self.moveShoulderRight(Actuators.RArm, 89.5)
        self.moveShoulderLeft(Actuators.LArm, 89.5)

        time.sleep(2)

        self.moveArmsUp(Actuators.BOTH, 90)

        time.sleep(2)

        self.moveShoulderLeft(Actuators.RArm, 89.5)
        self.moveShoulderRight(Actuators.LArm, 89.5)

        time.sleep(2)

        self.rotateElbowLeft(Actuators.RArm, 80)
        self.rotateElbowRight(Actuators.LArm, 80)

        self.rotateWristRight(Actuators.RArm, 100)
        self.rotateWristLeft(Actuators.LArm, 100)

    def initialHeadPosition(self):
        self.motion_service.setAngles("HeadPitch", 1, self.fractionMaxSpeed)

    def initialArmPosition(self, actuator):
        if actuator == Actuators.LArm:
            self.motion_service.setAngles("LShoulderPitch", 0.5, self.fractionMaxSpeed)
        elif actuator == Actuators.RArm:
            self.motion_service.setAngles("RShoulderPitch", 0.5, self.fractionMaxSpeed)
        elif actuator == Actuators.BOTH:
            self.motion_service.setAngles("LShoulderPitch", 0.5, self.fractionMaxSpeed)
            self.motion_service.setAngles("RShoulderPitch", 0.5, self.fractionMaxSpeed)

    def moveHead(self, headArr):
        # Head
        # [   head movement    { - : right, + : left } | Range: -119.5 to 119.5
        #     head movement    { + : down, - : up } | Range: -40.5 to 25.5
        # ]

        headArr = [ x * motion.TO_RAD for x in headArr]

        self.motion_service.angleInterpolationWithSpeed(self.headJointNames, headArr, self.fractionMaxSpeed)

    def __moveHeadIntern(self, deg, index):
        self.motion_service.changeAngles(self.headJointNames[index], math.radians(deg), self.fractionMaxSpeed)

    def moveHeadUp(self, deg):
        self.__moveHeadIntern(-deg, 1)

    def moveHeadDown(self, deg):
        self.__moveHeadIntern(deg, 1)

    def moveHeadRight(self, deg):
        self.__moveHeadIntern(deg, 0)

    def moveHeadLeft(self, deg):
        self.__moveHeadIntern(-deg, 0)

    def moveArmsThread(self):
        self.setArmsUp(Actuators.BOTH, 90)
        self.setElbowLeft(Actuators.RArm, 45)
        self.setElbowRight(Actuators.LArm, 45)
        time.sleep(0.1)
        
        self.motion_service.angleInterpolation('RElbowRoll',[math.radians(-1)],[0.2],False)
        self.motion_service.angleInterpolation('LElbowRoll',[math.radians(-1)],[0.2],False)
        time.sleep(0.1)
        self.motion_service.angleInterpolation('RElbowRoll',[math.radians(1)],[0.2],False)
        self.motion_service.angleInterpolation('LElbowRoll',[math.radians(1)],[0.2],False)

    def moveArmsBackThread(self):
         self.setArmsUp(Actuators.BOTH, 70)
         time.sleep(0.1)

    def dropArmsThread(self):
        self.moveArmsDown(Actuators.BOTH, 40)
        time.sleep(2)
        self.moveElbowRight(Actuators.RArm, 50)
        self.moveElbowLeft(Actuators.LArm, 50)

    def moveArms(self, actuator, armArr):
        # Arm Right (for left arm mirror the movement)
        # [   arm             { - : up, + : down } | Range: -119.5 to 119.5
        #     shoulder        { - : right side horizontal movement, + : left side horizontal movement } | Range: -89.5 to -0.5
        #     elbow rotation  { + : clockwise, - : anti-clockwise } | Range: -119.5 to 119.5
        #     elbow movement  { + : right to left, - : left to right } | Range: 0.5 to 89.5
        #     wrist rotation  { + : clockwise, - : anti-clockwise } | -104.5 to 104.5
        # ]

        armArr = [ x * motion.TO_RAD for x in armArr] # convert the degrees to radiants

        if actuator == Actuators.LArm:
            self.motion_service.angleInterpolationWithSpeed(self.armJointNamesL, armArr, self.fractionMaxSpeed)
        elif actuator == Actuators.RArm:
            self.motion_service.angleInterpolationWithSpeed(self.armJointNamesR, armArr, self.fractionMaxSpeed)
        elif actuator == Actuators.BOTH:
            self.motion_service.angleInterpolationWithSpeed(self.armJointNamesL, armArr, self.fractionMaxSpeed)
            self.motion_service.angleInterpolationWithSpeed(self.armJointNamesR, armArr, self.fractionMaxSpeed)

    def __moveArmsIntern(self, actuator, deg, index):
        if actuator == Actuators.LArm:
            self.motion_service.changeAngles(self.armJointNamesL[index], math.radians(deg), self.fractionMaxSpeed)
        elif actuator == Actuators.RArm:
            self.motion_service.changeAngles(self.armJointNamesR[index], math.radians(deg), self.fractionMaxSpeed)
        elif actuator == Actuators.BOTH:
            # Move left hand without compromising last position
            self.motion_service.changeAngles(self.armJointNamesL[index], math.radians(deg), self.fractionMaxSpeed)
            # Move right hand without compromising last position
            self.motion_service.changeAngles(self.armJointNamesR[index], math.radians(deg), self.fractionMaxSpeed)

    def __setArmsIntern(self, actuator, deg, index):
            if actuator == Actuators.LArm:
                self.motion_service.setAngles(self.armJointNamesL[index], math.radians(deg), self.fractionMaxSpeed)
            elif actuator == Actuators.RArm:
                self.motion_service.setAngles(self.armJointNamesR[index], math.radians(deg), self.fractionMaxSpeed)
            elif actuator == Actuators.BOTH:
                # Move left hand without compromising last position
                self.motion_service.setAngles(self.armJointNamesL[index], math.radians(deg), self.fractionMaxSpeed)
                # Move right hand without compromising last position
                self.motion_service.setAngles(self.armJointNamesR[index], math.radians(deg), self.fractionMaxSpeed)

    def setArmsUp(self, actuator, deg):
        self.__setArmsIntern(actuator, -deg, 0)


    def moveArmsUp(self, actuator, deg):
        self.__moveArmsIntern(actuator, -deg, 0)

    def moveArmsDown(self, actuator, deg):
        self.__moveArmsIntern(actuator, deg, 0)

    def moveShoulderRight(self, actuator, deg):
        self.__moveArmsIntern(actuator, -deg, 1)

    def moveShoulderLeft(self, actuator, deg):
        self.__moveArmsIntern(actuator, deg, 1)

    def setElbowLeft(self, actuator, deg):
        self.__setArmsIntern(actuator, deg, 3)

    def setElbowRight(self, actuator, deg):
        self.__setArmsIntern(actuator, -deg, 3)

    def moveElbowLeft(self, actuator, deg):
        self.__moveArmsIntern(actuator, deg, 3)

    def moveElbowRight(self, actuator, deg):
        self.__moveArmsIntern(actuator, -deg, 3)

    def rotateElbowRight(self, actuator, deg):
        self.__moveArmsIntern(actuator, deg, 2)

    def rotateElbowLeft(self, actuator, deg):
        self.__moveArmsIntern(actuator, -deg, 2)

    def rotateWristRight(self, actuator, deg):
        self.__moveArmsIntern(actuator, deg, 4)

    def rotateWristLeft(self, actuator, deg):
        self.__moveArmsIntern(actuator, -deg, 4)

    def rotateWristRightQuantity(self, actuator, quantity):
        if quantity == Quantity.QUARTER:
            self.__moveArmsIntern(actuator, (self.WRISTYAWMAX / 4), 4)
        elif quantity == Quantity.HALF:
            self.__moveArmsIntern(actuator, (self.WRISTYAWMAX / 2), 4)
        elif quantity == Quantity.FULL:
            self.__moveArmsIntern(actuator, self.WRISTYAWMAX, 4)

    def rotateWristLeftQuantity(self, actuator, quantity):
        if quantity == Quantity.QUARTER:
            self.__moveArmsIntern(actuator, (self.WRISTYAWMIN / 4), 4)
        elif quantity == Quantity.HALF:
            self.__moveArmsIntern(actuator, (self.WRISTYAWMIN / 2), 4)
        elif quantity == Quantity.FULL:
            self.__moveArmsIntern(actuator, self.WRISTYAWMIN, 4)

    def moveHips(self, hipsArr):
        # Hips
        # [   hip movement    { - : right, + : left } | Range: -29.5 to 29.5
        #     hip movement    { + : back, - : front } | Range: -59.5 to 59.5
        # ]

        hipsArr = [ x * motion.TO_RAD for x in hipsArr]

        self.motion_service.angleInterpolationWithSpeed(self.hipsJointNames, hipsArr, self.fractionMaxSpeed)

    def __moveHipIntern(self, deg, index):
        self.motion_service.changeAngles(self.hipsJointNames[index], math.radians(deg), self.fractionMaxSpeed)

    def moveHipsRight(self, deg):
        self.__moveHipIntern(-deg, 0)

    def moveHipsLeft(self, deg):
        self.__moveHipIntern(deg, 0)

    def moveHipsBack(self, deg):
        self.__moveHipIntern(deg, 1)

    def moveHipsFront(self, deg):
        self.__moveHipIntern(-deg, 1)

    def moveToCoordinates(self, x, y):
        print "moving"
        self.motion_service.moveTo(x, y, 0)

    def navigateTo(self, x, y):
        print "navigate to"
        self.navigation_service.navigateTo(x, y)

    def moveAlong(self, x, y):
        print "moving along"
        self.navigation_service.moveAlong(["Composed", ["Holonomic", ["Line", [0.0, y]], 0.0, 2.0], ["Holonomic", ["Line", [x, 0.0]], 0.0, 2.0]])

    def closeHands(self, actuator):
        if actuator == Actuators.LArm:
            self.motion_service.closeHand("LHand")
        elif actuator == Actuators.RArm:
            self.motion_service.closeHand("RHand")
        elif actuator == Actuators.BOTH:
            self.motion_service.closeHand("LHand")
            self.motion_service.closeHand("RHand")

    def openHands(self, actuator):
        if actuator == Actuators.LArm:
            self.motion_service.openHand("LHand")
        elif actuator == Actuators.RArm:
            self.motion_service.openHand("RHand")
        elif actuator == Actuators.BOTH:
            self.motion_service.openHand("LHand")
            self.motion_service.openHand("RHand")

    def findCoordinateDiffArm(self):
        arrArm = self.getPositionEffector('RShoulderPitch')
        arrHand = self.getPositionEffector('RHand')

        diffX = arrHand[0] - arrArm[0]
        diffY = arrHand[1] - arrArm[1]

        diffArr = [diffX, diffY]

        return diffArr

    def getRobotPos(self):
        return self.motion_service.getRobotPosition(True)

    def getPositionEffector(self, name):
        frame  = motion.FRAME_WORLD
        useSensorValues  = False
        # Position6D using meters and radians (x, y, z, wx, wy, wz)
        result = self.motion_service.getPosition(name, frame, useSensorValues)
        return result

    def logPositionCoordinates(self, name):
        print self.getPositionEffector(name)

    def logPosition(self, actuator):
        if actuator == Actuators.LArm:
            print('logging right arm actuators')
            print('LArm')
            for index, val in enumerate(self.armJointNamesL):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
        elif actuator == Actuators.RArm:
            print('logging right arm actuators')
            print('RArm')
            for index, val in enumerate(self.armJointNamesR):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
        elif actuator == Actuators.BOTH:
            print('logging arm actuators')
            print('LArm')
            for index, val in enumerate(self.armJointNamesL):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
            print('RArm')
            for index, val in enumerate(self.armJointNamesR):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
        elif actuator == Actuators.HIPS:
            print('logging hip actuators')
            print('Hips')
            for index, val in enumerate(self.hipsJointNames):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
        elif actuator == Actuators.ALL:
            print('logging all actuators')
            print('Head')
            for index, val in enumerate(self.headJointNames):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
            print('LArm')
            for index, val in enumerate(self.armJointNamesL):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
            print('RArm')
            for index, val in enumerate(self.armJointNamesR):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))
            print('Hips')
            for index, val in enumerate(self.hipsJointNames):
                print('{}: {}'.format(val, str(math.degrees(self.motion_service.getAngles(val, False)[0]))))