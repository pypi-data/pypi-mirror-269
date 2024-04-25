__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import time
from datetime import timedelta, datetime
import json

class milestone:
    def __init__(self):
        self.perfCounter = None
        self.startTime = None
        self.stopTime = None
        self.traceSteps = []
        self.msHeader = {}
        self.stepIdx = 1
        self.msHeader = {}

    def initialize(self, args):
        for arg in args.keys():
            self.msHeader[arg] = args[arg]

    def start(self):
        if (self.perfCounter == None):
            self.perfCounter = time.perf_counter()
            self.startTime = datetime.now()

    def add(self, name, description, *others) -> bool:
        try:
            if (self.perfCounter == None):
                self.start()
            curms = {}
            curms["step"] = self.stepIdx
            curms["name"] = name
            curms["description"] = description
            curms["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            curms["stepduration"] = str(timedelta(seconds=time.perf_counter() - self.perfCounter))
            if (len(others) > 0):
                curms["details"] = others
            self.traceSteps.append(curms)
            self.stepIdx = self.stepIdx + 1
            return True
        except Exception as e:
            return False
        
    def stop(self):
        self.stopTime = datetime.now()

    def getFullJSON(self):
        fullJson = {}
        fullJson["parameters"] = self.msHeader
        fullJson["steps"] = self.traceSteps
        fullJson["start"] = str(self.startTime)
        self.stopTime = datetime.now() if self.stopTime == None else self.stopTime
        fullJson["stop"] = str(self.stopTime)
        fullJson["duration"] = str(self.stopTime - self.startTime)
        return json.dumps(fullJson)