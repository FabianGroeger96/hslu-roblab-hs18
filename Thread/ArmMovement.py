from Wrappers.movement import Movement, Actuators
import time
import datetime
from math import radians

class ArmMovement():
    movement = None
    stop = False

    def __init__(self, movement):
        self.movement = movement

    def Run(self):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=60)
        #while not self.stop or datetime.datetime.now() < end_time:
        while not self.stop:
            self.movement.moveArmsThread()

        self.movement.dropArmsThread()

    def Stop(self):
        self.stop = True