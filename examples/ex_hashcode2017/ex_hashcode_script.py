import sys
sys.path.append('../../tests')
sys.path.append('../../')
from testUtils import *

class Endpoint:
    def __init__(self, datacenterLatency, countCaches, caches):
        self.datacenterLatency = datacenterLatency
        self.countCaches = countCaches
        self.caches = caches #list of {endpointId, latency}, could be dict
    def __str__(self):
         return ("%dms latency %d caches (%s)" % (self.datacenterLatency, self.countCaches, self.caches))

class Request:
    def __init__(self, videoId, endpointId, countRequests):
        self.videoId = videoId
        self.endpointId = endpointId
        self.countRequests = countRequests
    def __str__(self):
         return ("%d requests for video %d coming from endpoint %d." % (self.countRequests, self.videoId, self.endpointId))

parserText = readFile("ex_hashcode_parser.txt")
inputFiles = ["ex_hashcode_input.txt", "me_at_the_zoo.in", "videos_worth_spreading.in", "kittens.in"]
debugPrint = False
for fname in inputFiles:
    fullTest(readFile(fname), parserText, "Example Hashcode2017(%s)" % fname, expectedCountVars = 9, classes= [Endpoint, Request], debugPrint = debugPrint)