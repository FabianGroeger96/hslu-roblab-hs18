from pynaoqi_mate import Robot
from configuration import PepperConfiguration
import qi
import time
import motion

ONEUNITDIST = 0.5

class MoveHands(object):
    def __init__(self, myrobot):
        super(MoveHands,self).__init__()
        session = myrobot.session

        alife = session.service("ALAutonomousLife")
        alife.setAutonomousAbilityEnabled("BackgroundMovement", False)
        alife.setAutonomousAbilityEnabled("BasicAwareness", False)
        alife.setAutonomousAbilityEnabled("ListeningMovement", False)
        alife.setAutonomousAbilityEnabled("SpeakingMovement", False)

        self.memory_service = session.service("ALMemory")
        self.motion_service = session.service("ALMotion")

        #self.motion_service.setIdlePostureEnabled(False)
        #self.motion_service.setBreathEnabled(False)

    def _moveHand(self):
        JointNamesL = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
        JointNamesR = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]

        # ArmL/R
        # [   hand            { - : up, + : down }
        #     shoulder        { - : right side horizontal movement, + : left side horizontal movement }
        #     Palm rotation   { + : clockwise, - : anti-clockwise }
        #     Elbow movement  { + : right to left, - : left to right }
        # ]
        # these hand movements will only work if rotation are possible in those directions
        # ArmL1 = [-50,  30, 0, 0]
        # ArmL1 = [ x * motion.TO_RAD for x in ArmL1]

        ArmR1 = [0, 0, 50, 0]
        ArmR1 = [ x * motion.TO_RAD for x in ArmR1]

        pFractionMaxSpeed = 0.1
        self.motion_service.angleInterpolationWithSpeed(JointNamesR, ArmR1, pFractionMaxSpeed)

        return

    def _moveForward(self, distToMove):
        X = min(distToMove, ONEUNITDIST)  # forward
        Y = 0.0
        Theta = 0.0

        x = 0
        t0= time.time()

        # Blocking call
        a = self.motion_service.moveTo(X, Y, Theta)

        t1 = time.time()
        t = t1 -t0
        t *= 1000

        units = float(t) * (1.0 / TIME_CALIBERATED)
        # TIME_CALIBERATED is an average time per m length. Need to caliberate according to the flooring.

        resDist = 0
        if units >= 0.2:
            resDist = units

        # print "dist in m : ",units
        possible = True # movement possible in direction
        if units < 0.2:
            possible =  False
            units = ONEUNITDIST # NOT UPDATING AS OBSTCLE JUST IN FRONT HENCE WE DONT WANT 0 BTW GRID LINES

        return [possible , units]

    def run(self):
        time.sleep(60)


virtualRobotConfig = PepperConfiguration("Amber")
myRobot = Robot(virtualRobotConfig)

moveHands = MoveHands(myRobot)
moveHands.run()


