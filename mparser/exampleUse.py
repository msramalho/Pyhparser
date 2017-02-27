import mparser

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

def printStatus(): #read exampleParser.txt to check the variable names and exampleInput.txt for their values
    print("\n\n")
    print("n = " + str(n))
    print("Name = " + str(Name))
    print("myInts = " + str(myInts))
    print("Names = " + str(Names))
    print("Numbers = " + str(Numbers))
    print("myDicts = " + str(myDicts))
    print("myDictsList = " + str(myDictsList))
    print("myTuple = " + str(myTuple))
    print("total = " + str(total))
    print("sizesList = " + str(sizesList))
    print("sentences = " + str(sentences))
    print("countLists = " + str(countLists))
    print("mySentences = " + str(mySentences))
    print("complexNumber = " + str(complexNumber))
    print("complexNumber2 = " + str(complexNumber2))
    #print("anotherVar = " + str(anotherVar))
    

mparser.mparse("exampleParser.txt","exampleInput.txt", True, [Complex, ComplexSpecial])    #True means verbose

"""mparser.mparseContent("(anotherVar, int)","2020", True)         #True means verbose
if mparser.mparseContent("(anotherVar, int)","2017", False):    #notice the redefinition of anotherVar
    print("\n\nI choose to be the one saying the variable was appended")"""

#the variables are ready but are not accessible in this file's global scope. 
#to achieve this simple do:
tempGlobals = mparser.getGlobals()
for key, value in tempGlobals.items():
    globals()[key] = value


#to display our results
printStatus()