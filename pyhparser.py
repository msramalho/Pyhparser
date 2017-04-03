#this is the main class
import re
from parserTools.cleaner import *
from utils import *

#regex constants:
regexConfigurationVariables = r"{(.*),(.*),(.*)}"

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
    def setVariable(self, name, value, initializeOnly = False):#inserts a new variable into the variables dict
        pass
    def setTempVariable(self, name, value, initializeOnly = False):#creates a temporary variable and returns it
        pass
    def parseLenValue(self, text):
        pass
    def isThereEnoughDataToParse(self, length):#returns False if the values left to parse are less than the required ones
        pass
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