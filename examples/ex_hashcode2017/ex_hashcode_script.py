import sys
sys.path.append('../../')
import mparser

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

def printStatus(myVars):
    for key, value in myVars.items():
        if type(value) == list and not mparser.validTypeSingle(str(type(value[0]).__name__)):
            print("%20s:" % (key))
            for el in value:
                print("%23s%s" % (" ",str(el)))
        else:
            print("%20s:  %s" % (key, value))

mparser.mparse("ex_hashcode_parser.txt","ex_hashcode_input.txt", True, [Endpoint, Request])    #True means verbose

#the variables are ready but are not accessible in this file's global scope. 
#to achieve this simple do:
tempGlobals = mparser.getGlobals()
for key, value in tempGlobals.items():
    globals()[key] = value


#to display our results
printStatus(tempGlobals)