
from sys import argv
import re, tokenize, io, getopt

#TODO: include set and frozenset, see tuple implementation in (varName, tuple, len) format

####prohibited variable names in the parser file
prohibitedVariableNames = ["argv", "regexSingleVar", "regexSingleVarLen", "regexComment", "regexCommentReplacement", "regexDuplicateWhitespace", "regexDuplicateWhitespace", "regexDuplicateParagraphs", "regexWhitespaceLeftBracket", "regexWhitespaceRightBracket", "regexCommasSpace", "regexCommasSpaceReplacement", "regexRemoveQuoteFromString", "regexConfigurationVariables", "pythonTypes", "separatorString", "parserHead", "parserBody", "parseText", "inputText", "inputPointer", "defaultDelimiter", "lineIndex", "line"]
prohibitedVariableNames.sort()
####Utils functions
def displayUnavailableVariables():
    print("Unavailable variable names (alphabetically): ")
    print("\n".join(prohibitedVariableNames))

def displayUsage():
    print("Master Parser Python")
    print("Parse input files (inputFile.txt) into python variables by specifying the layout of the variables (parserLayout.txt)")
    print("\nCommand line arguments:")
    print("python mparser.py inputeFile.txt parserLayout.txt")
    print("\nCommand line flags:")
    print("-h --help        display usage instructions")
    print("-v --verbose     increase verbosity")
    print("-u --unavailable list the variable names you cannot use in the parserText")

####Command line arguments
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
    print("Wrong number of arguments\n>>python %s -flags parseText.txt inputFile.txt" % argv[0])
    exit()

####Variable declarations
    ####Important constants
regexSingleVarAnonymous = r"^\(([^\(\),\s]+)\)"                             #format (type)
regexSingleVar = r"^\(([^\(\),\s]+),([^\(\),\s]+)\)"                        #format (varName,type)
regexSingleVarLen = r"^\(([^\(\),\s]+),([^\(\),\s]+),([^\(\),\s]+)\)"       #format (varName,type,len)
regexParseLenVariable = r"^{(.+)}"                                          #format {varName}
regexContainerVariable = r"^\[([^\s]+?),([^\s]+?),([^\s]+?),([^\s]+?)\]$"   #format [varName,typeContainer,len,unitType]
regexComment = r"\#.*?$"
regexCommentReplacement = ""
regexDuplicateWhitespace= r"([\r\t\f ])+"
regexDuplicateParagraphs= r"([\v\n])+"
regexWhitespaceLeftBracket =  r"({)[\r\t\f ]*"
regexWhitespaceRightBracket =  r"[\r\t\f ]*(})"
regexCommasSpace = r", "    #podia ser r", *", mas o whitespace removal torna redundante
regexCommasSpaceReplacement = ","
regexRemoveSingleQuoteFromString = r"^'(.*)'$"
regexRemoveDoubleQuoteFromString = r"^\"(.*)\"$"
regexConfigurationVariables = r"{(.*),(.*),(.*)}"

pythonTypes = {'int': int, 'float': float, 'complex':complex, 'bool': bool, 'str': str, 'dict':dict, 'tuple':tuple, 'list':list, 'set':set, 'frozenset':frozenset}
    
separatorString = ".body"
parserHead=""
parserBody=""
parseText=""
inputText=""

    ####configuration variables
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

def removeCommaSpaces(text):
    return re.sub(regexCommasSpace, regexCommasSpaceReplacement, text, 0, re.MULTILINE)
def removeQuotes(text):
    text = re.sub(regexRemoveSingleQuoteFromString, "\\1", text, 0)
    return re.sub(regexRemoveDoubleQuoteFromString, "\\1", text, 0)
def cleanText(text):
    return removeCommaSpaces(removeRedundantWhitespaces(removeComments(text)))

    

####Important functions
def readFile(filename):#read a file or print an error
    try:
        file = open(filename)
    except IOError:
        print("Unable to open file %s" % filename)
        return ""
    return file.read()
def separateHeadBody(text):
    global parserHead, parserBody
    parts = parseText.split(separatorString,1)  #separate head from body
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

def setGlobal(name, value, t, initializeOnly):#creates a global variable with a given value
    if validTypeSingle(t):
        globals()[name] = pythonTypes[t](value) #cast to type
    elif validTypeContainer(t):
        if initializeOnly:
            globals()[name] = pythonTypes[t]()
        else:
            globals()[name] = value
    return globals()[name]

def setLocal(name, value, t, initializeOnly):#creates a global variable with a given value
    if validTypeSingle(t):
        locals()[name] = pythonTypes[t](value) #cast to type
    elif validTypeContainer(t):
        if initializeOnly:
            locals()[name] = pythonTypes[t]()
        else:
            locals()[name] = value
    return locals()[name]
def setGlobalOrLocal(name, value, t, setAsGlobal, initializeOnly):#creates a global variable with a given value
    if setAsGlobal:
        return setGlobal(name, value, t, initializeOnly)
    return setLocal(name, value, t, initializeOnly)
def setvar(name, value, t):#creates a global variable with a given value checks for the type
    if not t in pythonTypes.keys():
        return False
    globals()[name] = pythonTypes[t](value) #cast to type
    return True
####parsing functions
def parseDictGetBothParts(text, separator):#returns (keyText, valueText)
    openBrackets = 0
    i = 0
    result=()
    while i < len(text):
        if text[i] in ("{", "(", "["):
            openBrackets+=1
        elif text[i] in ("}", ")", "]"):
            openBrackets-=1
        elif text[i] == separator and openBrackets == 1:
            return [text[1:i],text[i+1:-1]]
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
        print("DICTDIVIDE: " + str(parserTemp))
        if parserTemp and parserTemp[0] in globals() and parserTemp[1] in globals():
            print("GO")
            print(str(globals()[parserTemp[1]][len(globals()[parserTemp[1]])]))
            return globals()[parserTemp[1]][len(globals()[parserTemp[1]])]
    elif text[0] == "{":
        text = re.sub(regexParseLenVariable, "\\1", text, 0, re.MULTILINE)
        if text in globals():
            return globals()[text]
    try: 
        return int(text)
    except ValueError:
        print("ERROR - the variable name you specified for the length {%s} does not exist at this point" % text)
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

def parseVariable(text, setAsGlobal):
    global inputText
    parserVar = ""
    text = text.strip(defaultDelimiter)     #remove side delimeters
    #print("parsing: %s" % text)
    #if elementar variable create local and return
    if text[0] == "(":      #single var
        match = re.search(regexSingleVarAnonymous,text)  #match the format (type)
        if match and validTypeSingle(match.group(1)):
            parserVar = setLocal("parserTemp", inputText[0], match.group(1), False)#never global
            del inputText[0]
        else:
            match = re.search(regexSingleVar,text)  #match the format (type, len)
            if match and match.group(1) == "str":#the names cannot be protected words so this is type, len
                text = "(parserTemp,%s,%s)" % (match.group(1), match.group(2))
                print("NEW TEXT %s" % text)
            match = re.search(regexSingleVar,text)  #match the format (varName, type)
            if match and validTypeSingle(match.group(2)):
                parserVar = setGlobalOrLocal(match.group(1), inputText[0], match.group(2), setAsGlobal, False)
                del inputText[0]
            else:
                match = re.search(regexSingleVarLen,text)  #match the format (varName, type, len)
                if match and match.group(2) == "str": 
                    length = parseLenValue(match.group(3))
                    checkDoableLen(length, match.group(1))  #exits if this len is not parsable
                    if not match.group(1) in locals():
                        parserVar = setGlobalOrLocal(match.group(1), inputText[0], "str", setAsGlobal, False) #instantiate the string
                        del inputText[0]
                    for valIndex in range(length-1):
                        parserVar+= defaultDelimiter + inputText[0]
                        del inputText[0]
    elif text[0] == "[":    #container var
        match = re.search(regexContainerVariable,text)  #match the format [varName, typeContainer, length, unitType]
        if match and validTypeContainer(match.group(2)):
            parserIndexList = 0
            length = parseLenValue(match.group(3))
            checkDoableLen(length, match.group(1))      #exits if this len is not parsable
            parserVar = setLocal(match.group(1), "", match.group(2), True) #instantiate the local variable
            parserTemp = parseVariable(match.group(4), False)
            parserVar = addElementToContainer(parserVar, parserTemp)
            
            for parserIndexList in range(1,length):
                parserTemp = parseVariable(match.group(4), False)
                parserVar = addElementToContainer(parserVar, parserTemp)
                if setAsGlobal:
                    setGlobal(match.group(1), parserVar, match.group(2), False)
            if setAsGlobal:
                setGlobal(match.group(1), parserVar, match.group(2), False)
    elif text[0] == "{":        #dict
        match = parseDictGetBothParts(text, ",")
        #match = re.search(regexParseDictionary,text)  #match the format {type1,type2}
        if match:                        #instantiate the local variable
            parserTempKey = parseVariable(match[0], False)
            parserTempValue = parseVariable(match[1], False)
            parserVar = {parserTempKey: parserTempValue}
    else:
        print("ERROR - Unable to detect if single or container variable in:\n    %s" % text)
        exit()
    #if container create local var to return later
    return parserVar #the local variable created

def printStatus():
    #print("parserHead\n"+parserHead)
    #print("\nparserBody\n"+parserBody)
    print("\n\n")
    print("n = " + str(n))
    print("name = " + name)
    print("inteiros = " + str(inteiros))
    print("nomes = " + str(nomes))
    print("numeros = " + str(numeros))
    print("myDicts = " + str(myDicts))
    print("myDictsList = " + str(myDictsList))
    print("myTuple = " + str(myTuple))
    print("total = " + str(total))
    print("tamanhos = " + str(tamanhos))
    print("frases = " + str(frases))


################################################## Main program flow
parseText = readFile(remainder[0])      #get the text from the parser file
parseText = cleanText(parseText)        #remove irrelvant chars that affect parsing - aka OCD
separateHeadBody(parseText)             #fill the head and body variables
parseConfigurationVariables(parserHead) #get the value of the configuration variables in the head

inputText = readFile(remainder[1])      #get the text from the input file
inputText = cleanText(inputText)        #remove irrelvant chars that affect parsing - aka OCD - from the input
inputText = inputTextToList(inputText)  #split the input file by the delimiter into a list

print(inputText)
for lineIndex, line in enumerate(parserBody.splitlines()):              #iterate body line by line
    if parserVerbosity:
        print("Parsing line %d  - %s..." % (lineIndex, line), end='')
    line = line.strip(defaultDelimiter)
    parts = line.split(defaultDelimiter)
    for part in parts:                      #iterate line part by part, separated by the defaultDelimiter
        if len(inputText) == 0:
            print("\nWARNING: The input file has less variables than the parser file indicated, stopped at instruction:\n       %s" % part)
            exit()
        if len(part)>0:
            parseVariable(part, True)
    if parserVerbosity:
        print("Done")
printStatus()
if len(inputText)>0:
    print("\n\nWARNING - there were %d values left to parse check your parsing file for descrepancies!" % len(inputText))