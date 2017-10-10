import time
from pyhparser import Pyhparser, readFile

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

def fullTest(inputVar, parserVar, title = "Random Test", expectedCountVars = 0, classes = [], debugPrint = False):
    startTime = time.time()
    print("--------------------------------%s--------------------------------" % title)
    p = Pyhparser(inputVar, parserVar, classes)         #create a pyhparser instance
    p.parse()                                           #execute the parsing
    if debugPrint:
        p.printRecursive(p.parserRead)
        printVars(p.variables)                              #display values of created variables
    result = "SUCCESS" if expectedCountVars == len(p.variables) else "FAILURE"
    print("TOTAL VARS: %d\nTIME: %s\nRESULT: %s" % (len(p.variables), time.time() - startTime, result))        #display number of created variables
    print("--------------------------------REACHED THE END--------------------------------")
    return p.getVariables()