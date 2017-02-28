import sys
sys.path.append('../../')
import mparserpython

class Complex:
    def __init__(self, realpart, imagpart):
        self.realpart = realpart
        self.imagpart = imagpart
    def __str__(self):
         return ("%di + %d" % (self.realpart, self.imagpart))
class ComplexSpecial:
    def __init__(self, realpart, imagpart, special):
        self.realpart = realpart
        self.imagpart = imagpart
        self.special = special
    def __str__(self):
         return ("%s Is the special oF %di + %d" % (self.special, self.realpart, self.imagpart))

def printStatus(myVars):
    for key, value in myVars.items():
        print("%20s:  %s" % (key, value))
    

mparserpython.mparse("ex_01_parser.txt","ex_01_input.txt", True, [Complex, ComplexSpecial])    #True means verbose

mparserpython.mparseContent("(anotherVar, int)","2020", True)         #True means verbose
if mparserpython.mparseContent("(anotherVar, int)","2017", False):    #notice the redefinition of anotherVar
    print("\n\nI choose to be the one saying the variable was appended")

#the variables are ready but are not accessible in this file's global scope. 
#to achieve this simple do:
tempGlobals = mparserpython.getGlobals()
for key, value in tempGlobals.items():
    globals()[key] = value


#to display our results
printStatus(tempGlobals)