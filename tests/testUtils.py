import sys
sys.path.append('../')
from pyhparser import *

def printVars(myVars):
    for key, value in myVars.items():
        print("%20s:  %s" % (key, value))

def fullTest(inputVar, parserVar, title = "Random Test", expectedCountVars = 0):
    print("--------------------------------%s--------------------------------" % title)
    p = pyhparser(inputVar, parserVar, [])              #create a pyhparser intance
    p.parse()                                           #execute the parsing
    printVars(p.getVariables())                         #display values of created variables
    result = "SUCCESS" if expectedCountVars == p.countVariables() else "FAILURE"
    print("TOTAL VARS: %d\nRESULT: %s" % (p.countVariables(), result))        #display number of created variables
    print("--------------------------------REACHED THE END--------------------------------")
    return p.getVariables()