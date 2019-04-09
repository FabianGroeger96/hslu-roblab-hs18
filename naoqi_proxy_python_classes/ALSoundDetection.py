#!/usr/bin/env python
# Class autogenerated from /home/sam/Downloads/aldebaran_sw/nao/naoqi-sdk-2.1.4.13-linux64/include/alproxies/alsounddetectionproxy.h
# by Sammy Pfeiffer's <Sammy.Pfeiffer at student.uts.edu.au> generator
# You need an ALBroker running

from naoqi import ALProxy



class ALSoundDetection(object):
    def __init__(self, session):
        self.proxy = None 
        self.session = session

    def force_connect(self):
        self.proxy = self.session.service("ALSoundDetection")

    def getCurrentPeriod(self):
        """Gets the current period.

        :returns int: Refresh period (in milliseconds).
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getCurrentPeriod()

    def getCurrentPrecision(self):
        """Gets the current precision.

        :returns float: Precision of the extractor.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getCurrentPrecision()

    def getEventList(self):
        """Get the list of events updated in ALMemory.

        :returns std::vector<std::string>: Array of events updated by this extractor in ALMemory
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getEventList()

    def getMemoryKeyList(self):
        """Get the list of events updated in ALMemory.

        :returns std::vector<std::string>: Array of events updated by this extractor in ALMemory
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getMemoryKeyList()

    def getMyPeriod(self, name):
        """Gets the period for a specific subscription.

        :param str name: Name of the module which has subscribed.
        :returns int: Refresh period (in milliseconds).
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getMyPeriod(name)

    def getMyPrecision(self, name):
        """Gets the precision for a specific subscription.

        :param str name: name of the module which has subscribed
        :returns float: precision of the extractor
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getMyPrecision(name)

    def getOutputNames(self):
        """Get the list of values updated in ALMemory.

        :returns std::vector<std::string>: Array of values updated by this extractor in ALMemory
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getOutputNames()

    def getSubscribersInfo(self):
        """Gets the parameters given by the module.

        :returns AL::ALValue: Array of names and parameters of all subscribers.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.getSubscribersInfo()

    def isPaused(self):
        """Gets extractor pause status

        :returns bool: True if the extractor is paused, False if not
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.isPaused()

    def isProcessing(self):
        """Gets extractor running status

        :returns bool: True if the extractor is currently processing images, False if not
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.isProcessing()

    def pause(self, status):
        """Changes the pause status of the extractor

        :param bool status: New pause satus
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.pause(status)

    def ping(self):
        """Just a ping. Always returns true

        :returns bool: returns true
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.ping()

    def setParameter(self, parameter, value):
        """Set the specified parameter.

        :param str parameter: Name of the parameter. "Sensibility" between 0 and 1 to adjust the capacity of NAO to locate quiet sounds. "EnergyComputation" (1 or 0) that activates the computation of the located source signal energy. This energy is added in the "ALSoundDetection/SoundLocated" ALMemory key.
        :param AL::ALValue value: "Sensibility" : a float in [0,1]. "EnergyComputation" : (1 or 0).
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.setParameter(parameter, value)

    def subscribe(self, name, period, precision):
        """Subscribes to the extractor. This causes the extractor to start writing information to memory using the keys described by getOutputNames(). These can be accessed in memory using ALMemory.getData("keyName"). In many cases you can avoid calling subscribe on the extractor by just calling ALMemory.subscribeToEvent() supplying a callback method. This will automatically subscribe to the extractor for you.

        :param str name: Name of the module which subscribes.
        :param int period: Refresh period (in milliseconds) if relevant.
        :param float precision: Precision of the extractor if relevant.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.subscribe(name, period, precision)

    def subscribe2(self, name):
        """Subscribes to the extractor. This causes the extractor to start writing information to memory using the keys described by getOutputNames(). These can be accessed in memory using ALMemory.getData("keyName"). In many cases you can avoid calling subscribe on the extractor by just calling ALMemory.subscribeToEvent() supplying a callback method. This will automatically subscribe to the extractor for you.

        :param str name: Name of the module which subscribes.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.subscribe(name)

    def unsubscribe(self, name):
        """Unsubscribes from the extractor.

        :param str name: Name of the module which had subscribed.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.unsubscribe(name)

    def updatePeriod(self, name, period):
        """Updates the period if relevant.

        :param str name: Name of the module which has subscribed.
        :param int period: Refresh period (in milliseconds).
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.updatePeriod(name, period)

    def updatePrecision(self, name, precision):
        """Updates the precision if relevant.

        :param str name: Name of the module which has subscribed.
        :param float precision: Precision of the extractor.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.updatePrecision(name, precision)

    def version(self):
        """Returns the version of the module.

        :returns str: A string containing the version of the module.
        """
        if not self.proxy:
            self.proxy = self.session.service("ALSoundDetection")
        return self.proxy.version()
