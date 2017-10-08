from grammar import *
import utils as u

class Interpreter:
    def __init__(self, inputText, parseText):   #constructor
        self.inputText = inputText      #the input as text
        self.inputIndex = 0             #the index at which getNextInput starts
        self.parseText = parseText      #the parse rules as text
        self.variables = dict()         #the variables to be read

    def parse(self, stringConnector = " "):    #the only function the user has to call
        self.parserRead = Grammar().parseString(self.parseText)     #map the parser according to the grammar
        self.inputRead = u.textToList(self.inputText)               #convert the input text into a list
        self.stringConnector = stringConnector                      #string added between strings in (str, 7)
        self.debug()
        for element in self.parserRead:
            self.interpret(element)

    def interpret(self, e):#recursive function to interpret a parse match
        if "primitive" in e:
            return self.getPrimitive(e)
        elif "container" in e:
            return self.getContainer(e)
        elif "dictionary" in e:
            return self.getDictionary(e)
        elif "class" in e:
            return self.getClass(e)
        else:
            print("Leaf: %s" % (e))

    def getPrimitive(self, primitive):#match parse and input for primitive
        length = self.getLength(primitive)
        if length == 1:
            var = u.cast(primitive["type"], self.getNextInput())
        else:
            var = u.cast(primitive["type"])
            for i in range(length):
                var = u.addElementToContainer(var, self.getNextInput(), self.stringConnector)#add to container
        return self.addVar(primitive, var)

    def getContainer(self, container):#match parse and input for container
        length = self.getLength(container)
        var = u.cast(container["type"])#empty container
        for i in range(length):
            var = u.addElementToContainer(var, self.interpret(container["value"]))#add to container
        return self.addVar(container, var)

    def getDictionary(self, dictionary):#match parse and input for dictionary
        length = self.getLength(dictionary)
        var = {}
        for i in range(length):
            var = u.addElementToContainer(var, {self.interpret(dictionary["left"]): self.interpret(dictionary["right"])})#add to container
        return self.addVar(dictionary, var)

    def getClass(self, c):#match parse and input for class
        raise Exception("getClass not yet implemented")

    def addVar(self, element, var):#add the variable to self.variables if it has a name
        if "varName" in element:
            self.variables[element["varName"]] = var
        return var

    def parseLen(self, length):#interpret 3 or {n} and return int, fails if n is missing
        if length[0] == "{":
            if length[1:-1] in self.variables:
                return self.variables[length[1:-1]]
            else:
                raise Exception("Pyhparsing: Length '%s' is not yet defined" % length)
        else:
            return int(length)

    def getLength(self, element):#check if element has length and return int
        if "len" in element: #if len is not define then it is 1
            length = self.parseLen(element["len"])
        else:
            length = 1
        return length

    def getNextInput(self):#return the next value in inputRead list
        res = None
        if self.inputIndex < len(self.inputRead):
            res = self.inputRead[self.inputIndex]
            self.inputIndex += 1
        return res


    def debug(self):
        print(self.parserRead)
        print(self.inputRead)
        self.printRecursive(self.parserRead)

    def printRecursive(self, e, i = 0):#TODO: remove debug function
        for element in e:
            if "primitive" in element:
                print("%sprimitive: %s" % ("  " * i, element))
                self.printRecursive(element, i+1)
            elif "container" in element:
                print("%scontainer: %s" % ("  " * i, element))
                self.printRecursive(element, i+1)
            elif "dictionary" in element:
                print("%sdictionary: %s" % ("  " * i, element))
                self.printRecursive(element, i+1)
            else:
                print("%sLeaf: %s" % ("  " * i, element))