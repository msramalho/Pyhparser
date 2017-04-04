#this is the main class
import re
from parserTools.cleaner import *
from parserTools.utils import *

#regex constants:
regexConfigurationVariables = r"{(.*),(.*),(.*)}"
regexParseLenVariable = r"^{(.+)}"                      #format {varName}
regexSingleVar = r"^\(([^\(\),\s]+),([^\(\),\s]+)\)"    #format (varName,type)
class pyhparser:
    configs = {"delimiter": ' ', "tempVar": "parserTemp"}#configuration variables
    variables = dict()          #dict of variables to return to the user
    pythonTypes = {'int': int, 'float': float, 'complex':complex, 'bool': bool, 'str': str, 'dict':dict, 'tuple':tuple, 'list':list, 'set':set}
    def __init__(self, inputText, parserText, classes):#creates a new instance
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
            print("Error - appendVariables should receive a dict, passed argument is of type %s" % type(appendTo))
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
        return length <= len(self.inputData)
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
    def parseSingleVarType(self, text):#parses (type)
        regexSingleVarAnonymous = r"^\(([^\(\),\s]+)\)" #format (type)
        match = re.search(regexSingleVarAnonymous,text)  #match the format (type)
        if match and validTypeSingle(match.group(1)):
            parserVar = setLocal("parserTemp", self.inputData[0], match.group(1))#never global
            del self.inputData[0]
            return True
        return False
    def parseSingleVarNameType(self, text):#parses (name,type)
        match = re.search(regexSingleVar,text)  #match the format (varName, type)
        if match and validTypeSingle(match.group(2)):
            parserVar = setGlobal(match.group(1), self.inputData[0], match.group(2))
            del self.inputData[0]
            return True
        return False
    def parseSingleVarNameTypeLen(self, text, setAsGlobal):#parses (name,type,len)
        regexSingleVarLen = r"^\(([^\(\),\s]+),(str),([^\(\),\s]+)\)"       #format (varName,str,len)
        if match: 
            length = self.parseLenValue(match.group(3))
            if not self.isThereEnoughDataToParse(length, match.group(1)):  #exits if this len is not parsable
                print("\n\nERROR - Not enough data to parse in:\n%s" % text)
                exit()

            if length > 0:
                if not match.group(1) in locals():
                    parserVar = self.setTempVariable(match.group(1), self.inputData[0], "str") #instantiate the string, it is set as global as long as the name is not parserTemp
                    del self.inputData[0]
                for valIndex in range(length-1):
                    parserVar+= configs["delimiter"] + self.inputData[0]
                    del self.inputData[0]
            else: #only create an empty string
                parserVar = self.setTempVariable(match.group(1), "", "str")
            if setAsGlobal or match.group(1) != configs["tempVar"]:
                self.setVariable(match.group(1), parserVar, "str")
    def parseSingleVar(self, text):#receives something like (type), (name,type) or (name,type,len) and returns a new variable
        if(!self.parseSingleVarType(text)):
            match = re.search(regexSingleVar,text)  #match the format (type, len), called before
            if match and match.group(1) == "str":#the names cannot be protected words so this is type, len
                text = "(%s,%s,%s)" % (configs["tempVar"], match.group(1), match.group(2))
            if(!self.parseSingleVarNameType(text)):
                if(!self.parseSingleVarNameTypeLen(text)):
                    print("\n\nERROR - Unable to parse single variable in:\n%s" % text)
                    exit()
    def parseClassVariable(self, text):#format [name,class,className,{param1:paramType1,param2:paramType2,...}]
        pass
    def parseContainerVariable(self, text):#format [name,type,length,unitType]
        pass
    def parseDictVariable(self, text):#format {type1,type2}
        pass
    def parseVariable(self, text, saveVar = False):#saveVar == True means this is a variable the user wants, not a temp
        parserVar = ""
        text = text.strip(configs["delimiter"])     #remove side delimeters
        if text[0] == "(":      #single var
            self.parseSingleVar(text)
        elif text[0] == "[":    #container var
            pass
        elif text[0] == "{":        #dict
            pass
        else:
            print("\n\nERROR - Unable to detect if single or container variable in:\n%s" % text)
            exit()
        return parserVar #the local variable created
    def parse(self):#executes the parsing functions and creates the varialbes from the Parser and inputData
        pass