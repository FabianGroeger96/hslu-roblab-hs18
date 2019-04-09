from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from StateMachine.stateMachine import StateMachine
from enum import Enum

import qi
import time

class MovingVariant(Enum):
    MOVING_WITH_TRACKER = 0
    MOVING_WITH_TRACKER_SEARCH_MARK = 1
    WITHOUT = 99

class HandsVariant(Enum):
    GRABBING_ONEHAND = 0 # for grabbing a bottle
    GRABBING_BOTHHANDS = 1 # for grabbing a box
    GRABBING_BOTHHANDS_TRACKER = 2
    WITHOUT = 99

class BoxVariant(Enum):
    DROPPING = 0
    DROPPING_SEARCH_MARK = 1
    WITHOUT = 99

if __name__ == "__main__":
    ###
    # Config
    ###
    virtualRobotConfig = PepperConfiguration("AmberNew")
    #virtualRobotConfig = PepperConfiguration("Virtual", "localhost", 62087)
    myRobot = Robot(virtualRobotConfig)
    stateMachine = StateMachine(myRobot)

    movingVariant = MovingVariant.MOVING_WITH_TRACKER
    handVariant = HandsVariant.GRABBING_BOTHHANDS
    boxVariant = BoxVariant.DROPPING

    ###
    # Start of the behavior
    ###
    stateMachine.enable_collisionProtection()

    ###
    # Start of Detecting & Moving to Object
    ###
    if movingVariant == MovingVariant.MOVING_WITH_TRACKER:
        # State: init_pos_start
        stateMachine.init_pos()

        # State: move_to_target_with_tracker
        stateMachine.move_to_target_with_tracker(idNaoMark=84) # insert id of object (small box: 84)
    
    elif movingVariant == MovingVariant.MOVING_WITH_TRACKER_SEARCH_MARK:
        # State: init_pos_start
        stateMachine.init_pos()

        # State: findNaoMark #84
        mark = stateMachine.findNaoMark(idNaoMark=[84]) # insert id of object

        # State: move_to_target_with_tracker
        stateMachine.move_to_target_with_tracker(idNaoMark=mark) # insert id of object (small box: 84)

    ###
    # Start of Moving Hands & Grabbing 
    ###
    if handVariant == HandsVariant.GRABBING_ONEHAND:
        # State: init_pos_grabbing
        stateMachine.init_pos_grabbing()

        # State: move_hand_target
        stateMachine.move_hand_target()

        # State: grabbing
        stateMachine.grabbing()

    elif handVariant == HandsVariant.GRABBING_BOTHHANDS:
        # State: init_grabbing_state
        stateMachine.disable_collisionProtection()

        # State: init_pos_grabbing_both
        stateMachine.init_pos_grabbing_both()
        time.sleep(0.2)

        # State: move_both_hands_target
        stateMachine.move_both_hands()
        time.sleep(0.2)

    elif handVariant == HandsVariant.GRABBING_BOTHHANDS_TRACKER:
        # State: init_grabbing_state
        stateMachine.disable_collisionProtection()

        # State: init_pos_grabbing_both
        stateMachine.init_pos_grabbing_both()
        time.sleep(0.2)

        # State: move_both_hands_target
        stateMachine.move_both_hands_target(idNaoMark=80) # insert id of object
        time.sleep(0.2)

    ###
    # Start of Moving to Drop Area
    ###
    if boxVariant == BoxVariant.DROPPING:
        # State: start_arm_movement
        stateMachine.start_arm_movement()
        time.sleep(0.2)

        # State: moving_leftside
        stateMachine.moving_leftside()
        time.sleep(1)

    elif boxVariant == BoxVariant.DROPPING_SEARCH_MARK:
        # State: start_arm_movement
        stateMachine.start_arm_movement()
        time.sleep(0.2)

        # State: moving_backwards
        stateMachine.moving_backwards()
        time.sleep(1)

        # State: findNaoMark #116
        mark = stateMachine.findNaoMark(idNaoMark=[112, 64, 116, 153, 145]) # insert id of drop area

        # State: move_to_target_with_tracker #116
        stateMachine.move_to_target_with_tracker(idNaoMark=mark) # insert id of drop area
        time.sleep(0.2)

    ###
    # End of the behavior
    ###
    # State: stop_arm_movement
    stateMachine.stop_arm_movement()
    time.sleep(5)

    # State: back
    stateMachine.back()