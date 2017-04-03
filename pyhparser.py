#this is the main class
import re
from parserTools.cleaner import *
from utils import *

#regex constants:
regexConfigurationVariables = r"{(.*),(.*),(.*)}"
regexParseLenVariable = r"^{(.+)}"                                          #format {varName}

class pyhparser:
    configs = {"delimiter": ' '}#configuration variables
    variables = dict()          #dict of variables to return to the user
    pythonTypes = {'int': int, 'float': float, 'complex':complex, 'bool': bool, 'str': str, 'dict':dict, 'tuple':tuple, 'list':list, 'set':set}
    def __init__(self, inputText, parserData, classes):#creates a new instance
        self.inputData = cleanInput(inputText)  #remove whitespaces
        self.parserData = cleanText(parserText) #remove comments and whitespaces
        self.classes = classParser(classes)     #list of classes required for this input (classParser instance)
        self.head, self.body = separateHeadBody(parseText)
        self.parseConfigs();
    def parseConfigs(self):#parses the head variable for configuration variables
        matches = re.finditer(regexConfigurationVariables, self.head, re.MULTILINE)
        for matchNum, match in enumerate(matches):
            tempConfig = [] #0 -> name 1 -> value, 2 -> type    
            for groupNum in range(0, len(match.groups())):
                print("Aviso miguel isto está a dar saltos de dois em dois, ver se é mesmo suposto e comentar")
                groupNum = groupNum + 1
                tempConfig.append(match.group(groupNum))
            tempConfig[1] = removeQuotes(tempConfig[1])
            if not tempConfig[1] in types.keys():
                print("ERROR - Failed to apply configuration variable (INVALID TYPE): number %d, name: %s, type: %s" % (matchNum+1, tempConfig[0], tempConfig[2]))
            else:
                configs[tempConfig[0]] = types[tempConfig[1]](tempConfig[2]) #cast to type
    def getVariables(self):#returns the variables created after parsing the file
        return variables
    def appendVariables(self, appendTo):#appends out variables to the dict passed
        if type(appendTo)!= dict:
            print("Error - appendVariables should receive a dict, passed argument is of type " + type(appendTo))
            return
        appendTo.update(variables)
    def setTempVariable(self, name, value, initializeOnly = False):#creates a temporary variable and returns it
        if validTypeSingle(t):
            locals()[name] = pythonTypes[t](value) #cast to type
        elif validTypeContainer(t):
            if initializeOnly:
                locals()[name] = pythonTypes[t]()
            else:
                locals()[name] = value
        return locals()[name]
    def setVariable(self, name, value, initializeOnly = False):#inserts a new variable into the variables dict
        return variables[name] = self.setTempVariable(name, value, initializeOnly)
    def parseDictGetBothParts(self, text, separator = ","):#receives something like {keyText, valueText} and returns (keyText, valueText)
        openBrackets = 0
        i = 0
        middle = 0
        result=[]
        while i < len(text):
            if text[i] in ("{", "(", "["):
                openBrackets+=1
            elif text[i] in ("}", ")", "]"):
                openBrackets-=1
            elif text[i] == separator and openBrackets == 1:
                middle = i
                result.append(text[1:i])
            if len(result) == 1 and openBrackets == 0:
                result.append(text[middle+1:i])
                result.append(text[i+2:])
                return result
            i+=1
        return False
    def parseLenValue(self, text):#receives a text to parse, checks if the text is a value or a variable name containing the size in the format {varName}, ex: 10, {n}
        text.strip(configs["delimiter"])
        if text[0] == "{" and ";" in text:
            parserTemp = self.parseDictGetBothParts(text, ";")
            if parserTemp and parserTemp[0] in variables and parserTemp[1] in variables:
                return variables[parserTemp[0]][len(variables[parserTemp[1]])]  #var0[len(var1)], this is like increasing the index, but len is used because it increases by one on each call
        elif text[0] == "{":
            text = re.sub(regexParseLenVariable, "\\1", text, 0, re.MULTILINE)
            if text in variables:
                return variables[text]
        try: 
            return int(text)
        except ValueError:
            print("ERROR - the variable name you specified for the length {%s} does not exist at this point or is not valid" % text)
            exit()
    def isThereEnoughDataToParse(self, length):#returns False if the values left to parse are less than the required ones
        return length <= len(inputData)
    def addElementToContainer(self, container, element):#receives a random type container and adds a new element to it
        if type(container) == list:
            container.append(element)
        elif type(container) == tuple:
            container+=(element,)
        elif type(container) == dict:
            container.update(element)
        elif type(container) == set:
            container.add(element)
        return container
    def parseSingleVarType(self):#parses (type)
        pass
    def parseSingleVarNameType(self):#parses (name,type)
        pass
    def parseSingleVarNameTypeLen(self):#parses (name,type,len)
        pass
    def parseSingleVar(self, text):#receives something like (type), (name,type) or (name,type,len) and returns a new variable
        pass
    def parseClassVariable(self, text):#format [name,class,className,{param1:paramType1,param2:paramType2,...}]
        pass
    def parseContainerVariable(self, text):#format [name,type,length,unitType]
        pass
    def parseDictVariable(self, text):#format {type1,type2}
        pass
    def parseVariable(self, text, saveVar = False):#saveVar == True means this is a variable the user wants, not a temp
        pass
    def parse(self):#executes the parsing functions and creates the varialbes from the Parser and inputData
        pass