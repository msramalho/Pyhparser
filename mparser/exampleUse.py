import mparser

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
    print("anotherVar = " + str(anotherVar))
    

mparser.mparse("exampleParser.txt","exampleInput.txt", True)    #True means verbose

mparser.mparseContent("(anotherVar, int)","2020", True)         #True means verbose
if mparser.mparseContent("(anotherVar, int)","2017", False):    #notice the redefinition of anotherVar
    print("\n\nI choose to be the one saying the variable was appended")

#the variables are ready but are not accessible in this file's global scope. 
#to achieve this simple do:
tempGlobals = mparser.getGlobals()
for key, value in tempGlobals.items():
    globals()[key] = value


#to display our results
printStatus()