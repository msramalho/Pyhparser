from sys import argv
import re, tokenize, io, getopt

class classParser:#stores and manages a list of the classes used by the parser, also creates instances of them
    def __init__(self, classList):
        self.classList = classList
        self.classNames = list(map(lambda c: c.__name__, classList))
    def hasClass(self, className):
        return className in self.classNames
    def getClass(self, className):
        for c in self.classList:
            if c.__name__ == className:
                return c
        return None
    def initClass(self, className, parameters):#dict
        return self.getClass(className)(**parameters) if self.hasClass(className) else False


#TODO: include set and frozenset, see tuple implementation in (varName, tuple, len) format

def displayUnavailableVariables():
    print("Unavailable variable names (alphabetically): ")
    print("\n".join(prohibitedVariableNames))

def displayUsage():
    print("Master Parser Python")
    print("Parse input files (inputFile.txt) into python variables by specifying the layout of the variables (parserLayout.txt)")
    print("\nCommand line arguments (does not parse classes):")
    print("python mparser.py -flags inputeFile.txt parserLayout.txt")
    print("\nCommand line flags:")
    print("-h --help        display usage instructions")
    print("-v --verbose     increase verbosity")
    print("-u --unavailable list the variable names you cannot use in the parserText")
    print("\n\n\n-------------------------------------------")
    print("Module instructions (parses classes):")
    print(".Create parser file according to the format")
    print(".Have your input file name or content handy, code:\n\n")
    print("    import mparser\n")
    print('    mparser.mparse("parserFile.txt","inputFile.txt", False) #false means not verbose\n')
    print("    tempGlobals = mparser.getGlobals() #get the created variables")
    print("    for key, value in tempGlobals.items(): #iterate the created variables")
    print("        globals()[key] = value #include the created variables in your file as globals, locals() is also possible\n")
    print("    #use your variables as you would any other global :)")


####Variable declarations
createdVariables = dict()           #contains all the variables parsed
availableClasses = None    #an instance of classParser that holds the available classes and is able to instantiate them
######Important constants
regexSingleVarAnonymous = r"^\(([^\(\),\s]+)\)"                             #format (type)
regexSingleVar = r"^\(([^\(\),\s]+),([^\(\),\s]+)\)"                        #format (varName,type)
regexSingleVarLen = r"^\(([^\(\),\s]+),([^\(\),\s]+),([^\(\),\s]+)\)"       #format (varName,type,len)
regexParseLenVariable = r"^{(.+)}"                                          #format {varName}
regexContainerVariable = r"^\[([^\s]+?),([^\s]+?),([^\s]+?),([^\s]+?)\]$"   #format [varName,typeContainer,len,unitType]
regexClassVar = r"^\[([^\[\],\s]+),(class),([^\(\),\s]+),(.+)\]$"       #format [varName,class,className,n*{param:paramType}], at least one param
regexComment = r"\#.*?$"
regexCommentReplacement = ""
regexDuplicateWhitespace= r"([\r\t\f ])+"
regexDuplicateParagraphs= r"([\v\n])+"
regexWhitespaceLeftBracket =  r"({)[\r\t\f ]*"
regexWhitespaceRightBracket =  r"[\r\t\f ]*(})"
regexCommasSpace = r", "    #podia ser r", *", mas o whitespace removal torna redundante
regexCollonSpace = r": "    #podia ser r", *", mas o whitespace removal torna redundante
regexCommasSpaceReplacement = ","
regexCollonSpaceReplacement = ":"
regexRemoveSingleQuoteFromString = r"^'(.*)'$"
regexRemoveDoubleQuoteFromString = r"^\"(.*)\"$"
regexConfigurationVariables = r"{(.*),(.*),(.*)}"

pythonTypes = {'int': int, 'float': float, 'complex':complex, 'bool': bool, 'str': str, 'dict':dict, 'tuple':tuple, 'list':list, 'set':set, 'frozenset':frozenset}
    
separatorString = ".body"
parserHead=""
parserBody=""
inputText=""

######configuration variables
defaultDelimiter = ' '


####Prepare the input for parsing
def removeComments(text):#removes #comments from the inputs
    return re.sub(regexComment, regexCommentReplacement, text, 0, re.MULTILINE)

def removeRedundantWhitespaces(text):
    text = text.strip()#strip sideways
    text =  re.sub(regexDuplicateWhitespace, "\\1", text, 0, re.MULTILINE)
    text =  re.sub(regexDuplicateParagraphs, "\\1", text, 0, re.MULTILINE)
    text = re.sub(regexWhitespaceLeftBracket, "\\1", text, 0, re.MULTILINE)
    return re.sub(regexWhitespaceRightBracket, "\\1", text, 0, re.MULTILINE)

def removePunctuationSpaces(text):
    text = re.sub(regexCommasSpace, regexCommasSpaceReplacement, text, 0, re.MULTILINE)
    return re.sub(regexCollonSpace, regexCollonSpaceReplacement, text, 0, re.MULTILINE)
def removeQuotes(text):
    text = re.sub(regexRemoveSingleQuoteFromString, "\\1", text, 0)
    return re.sub(regexRemoveDoubleQuoteFromString, "\\1", text, 0)
def cleanText(text):
    return removePunctuationSpaces(removeRedundantWhitespaces(removeComments(text)))

    

####Important functions
def readFile(filename):#read a file or print an error
    try:
        file = open(filename)
    except IOError:
        print("ERROR - Unable to open file %s" % filename)
        exit()
    return file.read()
def separateHeadBody(text):
    global parserHead, parserBody
    parts = text.split(separatorString,1)  #separate head from body
    if len(parts)==2:
        parserHead = parts[0].strip("\n")
        parserBody = parts[1].strip("\n")
    else:
        parserBody = parts[0].strip("\n")

def inputTextToList(text):
    temp = []
    for line in text.splitlines():
        parts = line.split(defaultDelimiter)
        for part in parts:  
            temp.append(part)
    return temp

def validTypeSingle(t):
    return t in ("int", "str", "bool", "float", "complex")
def validTypeContainer(t):
    return t in ("list", "dict", "tuple", "set", "frozenset")

def setGlobal(name, value, t, initializeOnly = False):#creates a global variable with a given value
    if validTypeSingle(t):
        createdVariables[name] = pythonTypes[t](value) #cast to type
    elif validTypeContainer(t):
        if initializeOnly:
            createdVariables[name] = pythonTypes[t]()
        else:
            createdVariables[name] = value
    return createdVariables[name]

def setLocal(name, value, t, initializeOnly = False):#creates a global variable with a given value
    if validTypeSingle(t):
        locals()[name] = pythonTypes[t](value) #cast to type
    elif validTypeContainer(t):
        if initializeOnly:
            locals()[name] = pythonTypes[t]()
        else:
            locals()[name] = value
    return locals()[name]
def setGlobalOrLocal(name, value, t, setAsGlobal, initializeOnly = False):#creates a global variable with a given value
    if setAsGlobal:
        return setGlobal(name, value, t, initializeOnly)
    return setLocal(name, value, t, initializeOnly)
def setvar(name, value, t):#creates a global variable with a given value checks for the type
    if not t in pythonTypes.keys():
        return False
    createdVariables[name] = pythonTypes[t](value) #cast to type
    return True
####parsing functions
def parseDictGetBothParts(text, separator = ","):#returns (keyText, valueText)
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
def parseConfigurationVariables(text):
    matches = re.finditer(regexConfigurationVariables, text, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        tempConfig = [] #0 -> name 1 -> value, 2 -> type    
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            tempConfig.append(match.group(groupNum))
        tempConfig[1] = removeQuotes(tempConfig[1])
        if not setvar(tempConfig[0], tempConfig[1], tempConfig[2]):
            print("ERROR - Failed to apply configuration variable (INVALID TYPE): number %d, name: %s, type: %s" % (matchNum, tempConfig[0], tempConfig[2]))
    return False

def parseLenValue(text):#checks if the text is a value or a variable name containing the size in the format {varName}
    text.strip(defaultDelimiter)
    if text[0] == "{" and ";" in text:
        parserTemp = parseDictGetBothParts(text, ";")
        if parserTemp and parserTemp[0] in createdVariables and parserTemp[1] in createdVariables:
            return createdVariables[parserTemp[0]][len(createdVariables[parserTemp[1]])]  #var0[len(var1)], this is like increasing the index, but len is used because it increases by one on each call
    elif text[0] == "{":
        text = re.sub(regexParseLenVariable, "\\1", text, 0, re.MULTILINE)
        if text in createdVariables:
            return createdVariables[text]
    try: 
        return int(text)
    except ValueError:
        print("ERROR - the variable name you specified for the length {%s} does not exist at this point or is not valid" % text)
        exit()
def checkDoableLen(length, output):
    if length > len(inputText):#the user is asking for more than available
        print("ERROR - Failed to input variable (WRONG LENGTH SPECIFIED): name: %s, length: %d" % (output, length))
        exit()
def addElementToContainer(container, element):
    if type(container) == list:
        container.append(element)
    elif type(container) == tuple:
        container+=(element,)
    elif type(container) == dict:
        container.update(element)
    return container

def parseVariable(text, setAsGlobal = False):
    global inputText
    parserVar = ""
    text = text.strip(defaultDelimiter)     #remove side delimeters
    #if elementar variable create local and return
    if text[0] == "(":      #single var
        match = re.search(regexSingleVarAnonymous,text)  #match the format (type)
        if match and validTypeSingle(match.group(1)):
            parserVar = setLocal("parserTemp", inputText[0], match.group(1))#never global
            del inputText[0]
        else:
            match = re.search(regexSingleVar,text)  #match the format (type, len)
            if match and match.group(1) == "str":#the names cannot be protected words so this is type, len
                text = "(parserTemp,%s,%s)" % (match.group(1), match.group(2))
            match = re.search(regexSingleVar,text)  #match the format (varName, type)
            if match and validTypeSingle(match.group(2)):
                parserVar = setGlobal(match.group(1), inputText[0], match.group(2))
                del inputText[0]
            else:
                match = re.search(regexSingleVarLen,text)  #match the format (varName, type, len)
                if match and match.group(2) == "str": 
                    length = parseLenValue(match.group(3))
                    checkDoableLen(length, match.group(1))  #exits if this len is not parsable
                    if not match.group(1) in locals():
                        parserVar = setLocal(match.group(1), inputText[0], "str") #instantiate the string, it is set as global as long as the name is not parserTemp
                        del inputText[0]
                    for valIndex in range(length-1):
                        parserVar+= defaultDelimiter + inputText[0]
                        del inputText[0]
                    if setAsGlobal or match.group(1) != "parserTemp":
                        setGlobal(match.group(1), parserVar, "str")
    elif text[0] == "[":    #container var
        match = re.search(regexContainerVariable,text)  #match the format [varName, typeContainer, length, unitType]
        if match and validTypeContainer(match.group(2)):
            parserIndexList = 0
            length = parseLenValue(match.group(3))
            checkDoableLen(length, match.group(1))      #exits if this len is not parsable
            parserVar = setLocal(match.group(1), "", match.group(2), True) #instantiate the local variable
            if setAsGlobal:
                setGlobal(match.group(1), parserVar, match.group(2), True)
            parserTemp = parseVariable(match.group(4))
            parserVar = addElementToContainer(parserVar, parserTemp)
            for parserIndexList in range(1,length):
                if setAsGlobal:
                    setGlobal(match.group(1), parserVar, match.group(2))
                parserTemp = parseVariable(match.group(4))
                parserVar = addElementToContainer(parserVar, parserTemp)
            if setAsGlobal:
                setGlobal(match.group(1), parserVar, match.group(2))
        else:   #did not match common container so it is a CLASS
            match = re.search(regexClassVar, text)
            if match:   #format [varName,class,className,n*{param:paramType}]
                if not availableClasses.hasClass(match.group(3)):
                    print("\nERROR - the specified class (%s) was not specified in the last argument of the mparser or mparserContent functions in:\n   %s" % (match.group(3), text))
                    exit()
                classParamsText = match.group(4)
                classParams = dict()    #this will contain a dict of {paramName : value}
                while len(classParamsText)>0:
                    splitted = parseDictGetBothParts(classParamsText, ":")
                    classParams[splitted[0]] = parseVariable(splitted[1])
                    classParamsText = splitted[2]
                createdVariables[match.group(1)] = availableClasses.initClass(match.group(3),classParams)
    elif text[0] == "{":        #dict
        match = parseDictGetBothParts(text)
        #match = re.search(regexParseDictionary,text)  #match the format {type1,type2}
        if match:                        #instantiate the local variable
            parserTempKey = parseVariable(match[0])
            parserTempValue = parseVariable(match[1])
            parserVar = {parserTempKey: parserTempValue}
    else:
        print("ERROR - Unable to detect if single or container variable in:\n    %s" % text)
        exit()
    #if container create local var to return later
    return parserVar #the local variable created



################################################## Main program flow
def mparseContent(parseText, it, verbosity = False, classes = []):
    global parserHead, parserBody, inputText, availableClasses
    availableClasses = classParser(classes)
    parseText = cleanText(parseText)        #remove irrelvant chars that affect parsing - aka OCD
    separateHeadBody(parseText)             #fill the head and body variables
    parseConfigurationVariables(parserHead) #get the value of the configuration variables in the head

    inputText = it
    inputText = cleanText(inputText)        #remove irrelvant chars that affect parsing - aka OCD - from the input
    inputText = inputTextToList(inputText)  #split the input file by the delimiter into a list

    if verbosity:
        linePrint = "Parsing line %2d  - %"+str(len(max(parserBody.splitlines(), key=len)))+"s...   "
    for lineIndex, line in enumerate(parserBody.splitlines()):              #iterate body line by line
        if verbosity:
            print(linePrint % (lineIndex, line), end='')
        line = line.strip(defaultDelimiter)
        parts = line.split(defaultDelimiter)
        for part in parts:                      #iterate line part by part, separated by the defaultDelimiter
            if len(inputText) == 0:
                print("\nERROR - The input file has less variables than the parser file indicated, stopped at instruction:\n       %s" % part)
                exit()
            if len(part)>0:
                parseVariable(part, True)
        if verbosity:
            print("Done")
    if verbosity:
        if len(inputText)>0:
            print("\n\nWARNING - there were %d values left to parse check your parsing file for descrepancies!" % len(inputText))
        elif len(inputText) == 0:
            print("\n\nSUCCESS - There was a perfect match between the parser and input files")
        print("Master Parser Done")
    return len(inputText) == 0

def mparse(parseFileName, imputFileName, verbosity = False, classes = []):
    global parserHead, parserBody, inputText
    parseText = readFile(parseFileName)      #get the text from the parser file
    inputText = readFile(imputFileName)      #get the text from the input file
    return mparseContent(parseText, inputText, verbosity, classes)

def mparseCmd():#receives the input from the command line
    parserVerbosity = False
    try:
        options, remainder = getopt.getopt(argv[1:], 'hvu', ['help', 'verbose', 'unavailable'])
    except getopt.GetoptError as err:
        print('GETOPT ERROR:', err)
        displayUsage()
        exit(1)
    for opt, arg in options:
        if opt in ('-h', '--help'):
            displayUsage()
            exit()
        if opt in ('-u', '--unavailable'):
            displayUnavailableVariables()
            exit()
        if opt in ('-v', '--verbose'):
            parserVerbosity = True
    ####Initial checks
    if len(remainder) != 2:
        print("Wrong number of arguments\n>>python %s -flags parseFile.txt inputFile.txt" % argv[0])
        exit()
    mparse(remainder[0], remainder[1], parserVerbosity)
    
def getGlobals():
    return createdVariables

if __name__ == "__main__":
    mparseCmd()