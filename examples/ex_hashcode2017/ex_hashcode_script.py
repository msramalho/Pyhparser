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


fullTest(readFile("ex_hashcode_input.txt"), readFile("ex_hashcode_parser.txt"), "Example 01", expectedCountVars = 10, classes= [Endpoint, Request])