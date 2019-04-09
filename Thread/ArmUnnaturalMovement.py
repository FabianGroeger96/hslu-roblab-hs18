from Wrappers.movement import Movement, Actuators
import time
import datetime
from math import radians

class ArmUnnaturalMovement():
    movement = None
    stop = False

    def __init__(self, movement):
        self.movement = movement

    def Run(self):
        while not self.stop:
            self.movement.moveArmsBackThread()

    def Stop(self):
        self.stop = True