from pynaoqi_mate import Robot
from configuration import PepperConfiguration
from enum import Enum

import qi
import time
import motion
import math
import almath

class Detection(object):
    def __init__(self, myRobot):
        super(Detection,self).__init__()

        self.session = myRobot.session

        self.motion_service = self.session.service("ALMotion")
        self.memory_service = self.session.service("ALMemory")
        self.tracker_service = self.session.service("ALTracker")

        # Using 10% of maximum joint speed
        self.fractionMaxSpeed = 0.1

        self.headJointNames = ["HeadYaw","HeadPitch"]

        self.armJointNamesL = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        self.armJointNamesR = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]

        self.hipsJointNames = ["HipRoll","HipPitch"]

        self.isTracking = False
        self.got_landmark = False
        self.got_landmarkID = -1

    def trackRedBall(self):
        # Add target to track.
        targetName = "RedBall"
        diameterOfBall = 0.03
        self.tracker_service.registerTarget(targetName, diameterOfBall)

        # set mode
        mode = "Head"
        self.tracker_service.setMode(mode)

        # set effector
        self.tracker_service.setEffector('None')

        # Then, start tracker.
        self.tracker_service.track(targetName)

        self.isTracking = True

    def trackLandmark(self, id):
        targetName = "LandMark"
        targetId = id
        targetDiameter = 0.03
        self.tracker_service.registerTarget(targetName, [targetDiameter, [targetId]])

        # set mode
        mode = "Head"
        self.tracker_service.setMode(mode)

        # set effector
        self.tracker_service.setEffector('None')

        # Then, start tracker.
        self.tracker_service.track(targetName)

        self.isTracking = True

        time.sleep(3)

        print "Tracker ID: " + self.tracker_service.getActiveTarget() + " Position " + str(self.tracker_service.getTargetPosition(motion.FRAME_WORLD))
        return self.tracker_service.getTargetPosition(motion.FRAME_ROBOT)

    def trackLandmarkNavigation(self, id):
        targetName = "LandMark"
        targetId = id
        targetDiameter = 0.03
        self.tracker_service.registerTarget(targetName, [targetDiameter, [targetId]])

        # set mode
        mode = "Navigate"
        self.tracker_service.setMode(mode)

        # set effector
        #self.tracker_service.setEffector('None')

        # Then, start tracker.
        self.tracker_service.track(targetName)

        self.isTracking = True

        time.sleep(3)

        print "Tracker ID: " + self.tracker_service.getActiveTarget() + " Position " + str(self.tracker_service.getTargetPosition(motion.FRAME_WORLD))
        return self.tracker_service.getTargetPosition(motion.FRAME_ROBOT)

    def stopTracker(self):
        self.tracker_service.stopTracker()
        self.tracker_service.unregisterAllTargets()

        self.isTracking = False

    def diffLandmarks(self, landmarkID1, landmarkID2):
        # A simple loop that reads the memValue and checks
        # whether landmarks are detected.
        for i in range(0, 50):
            time.sleep(0.5)
            val = self.memory_service.getData('LandmarkDetected', 0)
            # Check whether we got a valid output: a list with two fields.
            if(val and isinstance(val, list) and len(val) >= 2):
                # We detected landmarks !
                # For each mark, we can read its shape info and ID.
                # First Field = TimeStamp.
                #timeStamp = val[0]
                # Second Field = array of Mark_Info's.
                markInfoArray = val[1]
            try:
                # Browse the markInfoArray to get info on each detected mark.
                for markInfo in markInfoArray:
                    # First Field = Shape info.
                    markShapeInfo = markInfo[0]
                    # Second Field = Extra info (i.e., mark ID).
                    markExtraInfo = markInfo[1]
                    if markExtraInfo[0] == landmarkID1 or markExtraInfo[0] == landmarkID2:
                        print "found given landmark"
                        # Print Mark information.
                        print "mark  ID: %d" % (markExtraInfo[0])
                        print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                        print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])
            except Exception, e:
                print "Landmarks detected, but it seems getData is invalid. ALValue ="
                print val
                print "Error msg %s" % (str(e))
            else:
                print "Error with getData. ALValue = %s" % (str(val))

    def startLandmarkSubscriberCamera(self, landmarkID):
        self.landmarkID = landmarkID
        self.landmark_detection = self.session.service("ALLandMarkDetection")

        self.subscriber = self.memory_service.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)

        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0 )
        self.got_landmark = False
        # Set here the size of the landmark in meters.
        self.landmarkTheoreticalSize = 0.03 #in meters
        # Set here the current camera ("CameraTop" or "CameraBottom").
        self.currentCamera = "Head"

    def startLandmarkSubscriber(self, landmarkID):
        self.landmarkID = landmarkID
        self.landmark_detection = self.session.service("ALLandMarkDetection")

        self.subscriber = self.memory_service.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)

        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0 )
        self.got_landmark = False
        # Set here the size of the landmark in meters.
        self.landmarkTheoreticalSize = 0.03 #in meters
        # Set here the current camera ("CameraTop" or "CameraBottom").
        self.currentCamera = "RHand/Touch/Back"

    def stopLandmarkSubscriber(self):
        self.landmarkID = 0
        self.got_landmark = False
        self.got_landmarkID = -1
        self.landmark_detection.unsubscribe("LandmarkDetector")

    def on_landmark_detected(self, markData):
        """
        Callback for event LandmarkDetected.
        """
        if markData == []:  # empty value when the landmark disappears
            self.got_landmark = False
        elif not self.got_landmark:
            self.got_landmark = True
            self.got_landmarkID = markData[1][0][1][0]

            # Retrieve landmark center position in radians.
            wzCamera = markData[1][0][0][1]
            wyCamera = markData[1][0][0][2]

            # Retrieve landmark angular size in radians.
            angularSize = markData[1][0][0][3]

            # Compute distance to landmark.
            distanceFromCameraToLandmark = self.landmarkTheoreticalSize / ( 2 * math.tan( angularSize / 2))

            # Get current camera position in NAO space.
            transform = self.motion_service.getTransform(self.currentCamera, 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)

            # Compute the rotation to point towards the landmark.
            cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)

            # Compute the translation to reach the landmark.
            cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

            # Combine all transformations to get the landmark position in NAO space.
            robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform *cameraToLandmarkTranslationTransform

            #print "x " + str(robotToLandmark.r1_c4) + " (in meters)"
            #print "y " + str(robotToLandmark.r2_c4) + " (in meters)"
            #print "z " + str(robotToLandmark.r3_c4) + " (in meters)"

            self.diffTarget = [robotToLandmark.r1_c4, robotToLandmark.r2_c4, robotToLandmark.r3_c4]

    def getdiffTarget(self):
        if self.got_landmark:
            return self.diffTarget
        else:
            print "Haven't detected landmark"
            return None
    
    def checkIfNaoMarkDetected(self):
        return self.got_landmark

    def getDetectedNaoMarkID(self):
        return self.got_landmarkID

    def logTrackerPosition(self):
        if self.isTracking == True:
            print "Tracker ID: " + self.tracker_service.getActiveTarget() + " Position " + str(self.tracker_service.getTargetPosition(motion.FRAME_WORLD))
            return self.tracker_service.getTargetPosition(motion.FRAME_WORLD)

    def logTrackerLandmarkPosition(self):
        if self.isTracking == True:
            print "Tracker ID: " + self.tracker_service.getActiveTarget() + " Position " + str(self.tracker_service.getTargetCoordinates())
            return self.tracker_service.getTargetCoordinates()