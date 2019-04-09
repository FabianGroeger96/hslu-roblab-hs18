from pynaoqi_mate import Robot
from configuration import PepperConfiguration
import qi
import time

class Bumper(object):
    def __init__(self, myrobot):
        super(Bumper,self).__init__()
        session = myrobot.session
        self.memory = session.service("ALMemory")
        self.subscriberRight = self.memory.subscriber("RightBumperPressed")
        self.subscriberRight.signal.connect(self.rightLeg)
        self.subscriberLeft = self.memory.subscriber("LeftBumperPressed")
        self.subscriberLeft.signal.connect(self.leftLeg)
        self.subscriberBack = self.memory.subscriber("BackBumperPressed")
        self.subscriberBack.signal.connect(self.back)

        self.subscriberFrontHead = self.memory.subscriber("FrontTactilTouched")
        self.subscriberFrontHead.signal.connect(self.frontHead)
        self.subscriberHead = self.memory.subscriber("MiddleTactilTouched")
        self.subscriberHead.signal.connect(self.head)
        self.subscriberBackHead = self.memory.subscriber("RearTactilTouched")
        self.subscriberBackHead.signal.connect(self.backHead)

        self.subscriberRightHand = self.memory.subscriber("HandRightBackTouched")
        self.subscriberRightHand.signal.connect(self.rightHand)
        self.subscriberLeftHand = self.memory.subscriber("HandLeftBackTouched")
        self.subscriberLeftHand.signal.connect(self.leftHand)

        self.tts = session.service("ALTextToSpeech")


    def rightLeg(self,value):
        if value == 1.0:
            self.tts.say("I hurt my right leg!")
    def leftLeg(self,value):
        if value == 1.0:
            self.tts.say("I hurt my left leg!")
    def back(self,value):
        if value == 1.0:
            self.tts.say("I hurt my back!")

    def frontHead(self,value):
        if value == 1.0:
            self.tts.say("I hurt my front Head!")
    def head(self,value):
        if value == 1.0:
            self.tts.say("I hurt my head!")
    def backHead(self,value):
        if value == 1.0:
            self.tts.say("I hurt my back Head!")

    def rightHand(self,value):
        if value == 1.0:
            self.tts.say("You touch my right Hand!")
    def leftHand(self,value):
        if value == 1.0:
            self.tts.say("You touch my left Hand!")

    def run(self):
        time.sleep(60)


virtualRobotConfig = PepperConfiguration("Amber")
myRobot = Robot(virtualRobotConfig)
bump = Bumper(myRobot)
bump.run()


