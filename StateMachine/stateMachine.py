from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from Wrappers.movement import Movement, Actuators
from Wrappers.detection import Detection
from Thread.ThreadBoard import ThreadBoard
from Thread.ParallelTask import ParallelTask
from Thread.ArmMovement import ArmMovement
from Thread.ArmUnnaturalMovement import ArmUnnaturalMovement

import qi
import time
import motion
import math
import thread
import sys

class StateMachine(object):
    myRobot = None
    movement = None
    detection = None
    threadBoard = None

    def __init__(self, myRobot):
        super(StateMachine,self).__init__()

        self.myRobot = myRobot

        self.movement = Movement(myRobot)
        self.detection = Detection(myRobot)
        self.threadBoard = ThreadBoard()

        self.movement.enableAutonomousLife(False)
        self.movement.enableCollisionProtection(True)

        self.idObject = 115 # insert id of landmark from the object
        self.idHand = 114 # insert id of landmark from the hand

    def disable_collisionProtection(self):
        self.movement.enableCollisionProtection(False)

    def enable_collisionProtection(self):
        self.movement.enableCollisionProtection(True)

    def init_pos(self):
        print 'startet state: init_pos'
        self.movement.initialPosition()
        time.sleep(0.2)

    def move_to_target_with_tracker(self, idNaoMark):
        print 'startet state: move_to_target_with_tracker'
        self.stopped = False
        self.moved_init = False
        while not self.stopped:
            self.detection.trackLandmark(idNaoMark)
            self.detection.startLandmarkSubscriberCamera(idNaoMark)
            time.sleep(0.5)

            diffTarget = self.detection.getdiffTarget()
            if diffTarget == None:
                self.move_to_target_with_tracker(idNaoMark)
            else:
                print 'Difference between Pepper & target x: {}, y: {}, z: {}'.format(diffTarget[0], diffTarget[1], diffTarget[2])
                if not self.moved_init:
                    self.movement.moveToCoordinates(diffTarget[0], diffTarget[1])
                    self.moved_init = True
                else:
                    self.movement.moveAlong(diffTarget[0], diffTarget[1])
                
                diffTarget = self.detection.getdiffTarget()

                if diffTarget == None:
                    self.detection.stopTracker()
                    self.detection.stopLandmarkSubscriber()
                    self.movement.moveAlong(0.15, 0)
                    print 'Tracker close enough'
                    self.stopped = True
                    break
                else:
                    if diffTarget[0] < 0.10:
                        self.detection.stopTracker()
                        self.detection.stopLandmarkSubscriber()
                        self.movement.moveAlong(0.15, 0)
                        print 'Pepper close enough'
                        self.stopped = True
                        break

    def init_pos_grabbing(self):
        print 'startet state: init_pos_grabbing'
        self.movement.initialPositionGrabbing()
        time.sleep(1)

    def init_pos_grabbing_both(self):
        print 'startet state: init_pos_grabbing_both'
        self.movement.initialPositionGrabbingBothHands()
        time.sleep(1)

    def move_hand_target(self):
        print 'startet state: move_hand_target'
        while True:
            self.detection.startLandmarkSubscriber(self.idObject)
            time.sleep(5)
            self.detection.stopLandmarkSubscriber()

            diffTarget = self.detection.getdiffTarget()
            if diffTarget == None:
                self.move_hand_target()
            else:
                print 'Difference between hand & target x: {}, y: {}, z: {}'.format(diffTarget[0], diffTarget[1], diffTarget[2])
                if diffTarget[1] > 0.01:
                    print 'print diff Y: ' + str(diffTarget[1])
                    self.movement.moveElbowLeft(Actuators.RArm, 3)
                    time.sleep(1)
                else:
                    break

    def move_both_hands_target(self, idNaoMark):
        print 'startet state: move_hand_target'
        while True:
            self.detection.startLandmarkSubscriber(idNaoMark)
            time.sleep(1)
            self.detection.stopLandmarkSubscriber()

            diffTarget = self.detection.getdiffTarget()
            if diffTarget == None:
                self.move_both_hands_target(idNaoMark)
            else:
                print 'Difference between hand & target x: {}, y: {}, z: {}'.format(diffTarget[0], diffTarget[1], diffTarget[2])
                if abs(diffTarget[1]) > 0.3:
                    print 'print diff Y: ' + str(diffTarget[1])
                    self.movement.moveElbowLeft(Actuators.RArm, 3)
                    self.movement.moveElbowRight(Actuators.LArm, 3)
                    time.sleep(0.2)
                else:
                    break

    def move_both_hands(self):
        time.sleep(0.2)
        for i in range(0, 8):
            self.movement.moveElbowLeft(Actuators.RArm, i)
            self.movement.moveElbowRight(Actuators.LArm, i)
            time.sleep(0.2)
        time.sleep(0.2)
    
    def grabbing(self):
        print 'startet state: grabbing'
        for i in range(0, 10):
            # maybe change the speed of the movement that it is slower
            self.movement.moveElbowLeft(Actuators.RArm, 1)
            time.sleep(1)

        for i in range(0, 10):
            try:
                thread.start_new_thread(self.movement.closeHands, (Actuators.RArm, ))
                thread.start_new_thread(self.movement.closeHands, (Actuators.RArm, ))
                thread.start_new_thread(self.movement.closeHands, (Actuators.RArm, ))
                thread.start_new_thread(self.movement.closeHands, (Actuators.RArm, ))
                thread.start_new_thread(self.movement.closeHands, (Actuators.RArm, ))
                time.sleep(1)
            except:
                print "Unexpected error while creating thread: ", sys.exc_info()[0]

    def findNaoMark(self, idNaoMark):
        print 'startet state: findNaoMark'
        direction = False
        maxRange = 119.5
        rotation = 30
        self.detection.startLandmarkSubscriberCamera(idNaoMark[0])
        while True:
            time.sleep(4)
            if rotation >= maxRange:
                print 'No landmark found in range'
                break
            else:
                if self.detection.checkIfNaoMarkDetected():
                    if self.detection.getDetectedNaoMarkID() in idNaoMark:
                        print 'found NaoMark #' + str(self.detection.getDetectedNaoMarkID())
                        self.detection.stopLandmarkSubscriber()
                        return str(self.detection.getDetectedNaoMarkID())
                    else:
                        if direction:
                            self.movement.moveHeadLeft(rotation)
                            rotation += 30
                            direction = not direction
                        else:
                            self.movement.moveHeadRight(rotation)
                            rotation += 30
                            direction = not direction
                else:
                    if direction:
                        self.movement.moveHeadLeft(rotation)
                        rotation += 10
                        direction = not direction
                    else:
                        self.movement.moveHeadRight(rotation)
                        rotation += 10
                        direction = not direction

    def start_arm_movement(self):
        print 'startet state: start_arm_movement'
        self.threadBoard.armMovement1 = ParallelTask(ArmMovement(self.movement))
        self.threadBoard.armMovement2 = ParallelTask(ArmMovement(self.movement))
        self.threadBoard.armMovement3 = ParallelTask(ArmMovement(self.movement))
        self.threadBoard.armMovement1.Start()
        self.threadBoard.armMovement2.Start()
        self.threadBoard.armMovement3.Start()

        time.sleep(2)

    def stop_arm_movement(self):
        print 'startet state: stop_arm_movement'
        self.threadBoard.armMovement1.Stop()
        self.threadBoard.armMovement2.Stop()
        self.threadBoard.armMovement3.Stop()

    def moving_leftside(self):
        print 'startet state: moving_leftside'
        time.sleep(0.2)
        self.movement.moveToCoordinates(0, 0.65)
        time.sleep(0.2)

    def moving_backwards(self):
        print 'startet state: moving_leftside'
        time.sleep(0.2)
        self.movement.moveToCoordinates(-0.5,0)
        time.sleep(0.2)

    def drop(self):
        self.movement.moveArmsDown(Actuators.BOTH, 70)
        time.sleep(0.2)
        self.movement.moveElbowLeft(Actuators.RArm, 20)
        self.movement.moveElbowRight(Actuators.LArm, 20)

    def back(self):
        self.threadBoard.armMovement1 = ParallelTask(ArmUnnaturalMovement(self.movement))
        self.threadBoard.armMovement1.Start()
        self.movement.moveToCoordinates(-0.5,0)
        time.sleep(2)
        self.threadBoard.armMovement1.Stop()
        self.enable_collisionProtection()
        self.movement.rest()