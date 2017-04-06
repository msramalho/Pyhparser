import sys, time
sys.path.append('../')
from pyhparser import *

def validTypeSingle(t):
    return t in ("int", "str", "bool", "float", "complex")

def printVars(myVars):
    for key, value in myVars.items():
        if type(value) == list and not validTypeSingle(str(type(value[0]).__name__)):
            print("%20s:" % (key))
            for el in value:
                print("%23s%s" % (" ",str(el)))
        else:
            print("%20s:  %s" % (key, value))

def fullTest(inputVar, parserVar, title = "Random Test", expectedCountVars = 0, classes = []):
    startTime = time.time()
    print("--------------------------------%s--------------------------------" % title)
    p = pyhparser(inputVar, parserVar, classes)              #create a pyhparser intance
    p.parse()                                           #execute the parsing
    printVars(p.getVariables())                         #display values of created variables
    result = "SUCCESS" if expectedCountVars == p.countVariables() else "FAILURE"
    print("TOTAL VARS: %d\nTIME: %s\nRESULT: %s" % (p.countVariables(), time.time() - startTime, result))        #display number of created variables
    print("--------------------------------REACHED THE END--------------------------------")
    return p.getVariables()