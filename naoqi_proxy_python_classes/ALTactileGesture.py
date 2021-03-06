#!/usr/bin/env python
# Class autogenerated from /home/sam/Downloads/aldebaran_sw/nao/naoqi-sdk-2.1.4.13-linux64/include/alproxies/altactilegestureproxy.h
# by Sammy Pfeiffer's <Sammy.Pfeiffer at student.uts.edu.au> generator
# You need an ALBroker running

from naoqi import ALProxy



class ALTactileGesture(object):
    def __init__(self, session):
        self.proxy = None 
        self.session = session

    def force_connect(self):
        self.proxy = self.session.service("ALTactileGesture")

    def createGesture(self, arg1):
        """Define touch gesture.          :param sensor_sequence: List of strings that represent the         sequence of the desired gesture. For example, SingleFront         would be the following: ['000', '100', '000']. NOTE: All         sequences must start with '000' and all non-hold sequences         must end with '000'. Hold gestures should end with the touch         sequence you will be holding. For example, a SingleFrontHold         would be the following: ['000', '100'].          :returns: If sequence is valid, the name of gesture to listen         for, RuntimeError otherwise.

        :param std::vector<std::string> arg1: arg
        :returns str: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.createGesture(arg1)

    def createGesture2(self, arg1):
        """Define touch gesture.          :param sensor_sequence: Comma-separated string that represents         the sequence of the desired gesture. For example, SingleFront         would be the following: "000,100,000". NOTE: All sequences         must start with '000' and all non-hold sequences must end with         '000'. Hold gestures should end with the touch sequence you         will be holding. For example, a SingleFrontHold would be the         following: "000,100".          :returns: If sequence is valid, the name of gesture to listen         for, RuntimeError otherwise.

        :param str arg1: arg
        :returns str: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.createGesture(arg1)

    def getGesture(self, arg1):
        """Get the sequence associated with a gesture name          :param sequence: Sequence you want the gesture name of          :returns: Sequence (as list of strings) if it exists, None otherwise

        :param std::vector<std::string> arg1: arg
        :returns AL::ALValue: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.getGesture(arg1)

    def getGesture2(self, arg1):
        """Get the sequence associated with a gesture name          :param sequence: Sequence you want the gesture name of          :returns: Sequence (as list of strings) if it exists, None otherwise

        :param str arg1: arg
        :returns AL::ALValue: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.getGesture(arg1)

    def getGestures(self):
        """Get all gestures that have been defined in the system          :returns: Dictionary (Map<String, List<String>>) of all gestures

        :returns std::map<std::string , std::vector<std::string> >: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.getGestures()

    def getSequence(self, arg1):
        """Get the sequence associated with a gesture name          :param gesture_name: Name of gesture you want the sequence of          :returns: Sequence (as list of strings) if it exists, None otherwise

        :param str arg1: arg
        :returns std::vector<std::string>: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.getSequence(arg1)

    def setHoldTime(self, arg1):
        """Set length of hold time.          :param hold_time: Desired hold time, in seconds (Default: 0.8s)          :returns: True if hold time successfully updated, RuntimeError otherwise.

        :param float arg1: arg
        :returns bool: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.setHoldTime(arg1)

    def setHoldTime2(self, arg1):
        """Set length of hold time.          :param hold_time: Desired hold time, in seconds (Default: 0.8s)          :returns: True if hold time successfully updated, RuntimeError otherwise.

        :param str arg1: arg
        :returns bool: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.setHoldTime(arg1)

    def setSequenceTime(self, arg1):
        """Set length of sequence time.          :param sequence_time: Desired sequence time, in seconds (Default: 0.2s)          :returns: True if sequence time successfully updated, RuntimeError otherwise.

        :param str arg1: arg
        :returns bool: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.setSequenceTime(arg1)

    def setSequenceTime2(self, arg1):
        """Update length of sequence time.          :param sequence_time: Desired sequence time, in seconds (Default: 0.2s)          :returns: True if sequence time successfully updated, RuntimeError otherwise.

        :param float arg1: arg
        :returns bool: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.setSequenceTime(arg1)

    def setSettleTime(self, arg1):
        """Update length of settling time.          :param settle_time: Desired settling time, in seconds (Default: 0.04s)          :returns: True if settle time successfully updated, RuntimeError otherwise.

        :param str arg1: arg
        :returns bool: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.setSettleTime(arg1)

    def setSettleTime2(self, arg1):
        """Update length of settling time.          :param settle_time: Desired settling time, in seconds (Default: 0.04s)          :returns: True if settle time successfully updated, RuntimeError otherwise.

        :param float arg1: arg
        :returns bool: 
        """
        if not self.proxy:
            self.proxy = self.session.service("ALTactileGesture")
        return self.proxy.setSettleTime(arg1)
