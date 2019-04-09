import qi
import argparse
import sys
import time


def main(session, ballSize, effector):
    """
    This example shows how to use ALTracker with red ball and LArm.
    """
    # Get the services ALTracker, ALMotion and ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    tracker_service = session.service("ALTracker")

    motion_service.setExternalCollisionProtectionEnabled("LArm", True)
    motion_service.setExternalCollisionProtectionEnabled("RArm", True)

    # First, wake up.
    #motion_service.wakeUp()

    fractionMaxSpeed = 0.8
    # Go to posture stand
    #posture_service.goToPosture("StandInit", fractionMaxSpeed)

    motion_service.setAngles("HeadPitch", 1, 0.4)
    #motion_service.changeAngles("LShoulderPitch", 0.5, 1)
    #motion_service.changeAngles("RShoulderPitch", 0.5, 1)

    # Add target to track.
    targetName = "RedBall"
    #targetName = "RedCan"
    diameterOfBall = ballSize
    tracker_service.registerTarget(targetName, diameterOfBall)

    # set mode
    mode = "Head"
    tracker_service.setMode(mode)

    # set effector
    #tracker_service.setEffector(effector)

    # Then, start tracker.
    tracker_service.track(targetName)

    print("Start showing the object")

    try:
        while True:
            time.sleep(10)
            print "Tracker Position " + str(tracker_service.getTargetPosition(1))
            print "LShoulderPitch " + str(motion_service.getAngles("LShoulderPitch", False))
            print "LShoulderRoll " + str(motion_service.getAngles("LShoulderRoll", False))
            print "LElbowRoll " + str(motion_service.getAngles("LElbowRoll", False))
            print ""
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."

    # Stop tracker, go to posture Sit.
    tracker_service.stopTracker()
    tracker_service.unregisterAllTargets()
    tracker_service.setEffector("None")
    #posture_service.goToPosture("Sit", fractionMaxSpeed)
    #motion_service.rest()

    print "ALTracker stopped."


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.101",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--ballsize", type=float, default=1,
                        help="Diameter of ball.")
    parser.add_argument("--effector", type=str, default="Arms",
                        choices=["Arms", "LArm", "RArm"],
                        help="Effector for tracking.")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.ballsize, args.effector)