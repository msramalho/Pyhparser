
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
regexSingleVar = r"^\(([^\(\),\s]+),([^\(\),\s]+)\)"                     #format (varName,type)
regexSingleVarLen = r"^\(([^\(\),\s]+),([^\(\),\s]+),([^\(\),\s]+)\)"    #format (varName,type,len)
regexComment = r"\#.*?$"
regexCommentReplacement = ""
regexDuplicateWhitespace= r"([\r\t\f ])+"
regexDuplicateParagraphs= r"([\v\n])+"
regexWhitespaceLeftBracket =  r"({)[\r\t\f ]*"
regexWhitespaceRightBracket =  r"[\r\t\f ]*(})"
regexCommasSpace = r", "    #podia ser r", *", mas o whitespace removal torna redundante
regexCommasSpaceReplacement = ","
regexRemoveQuoteFromString = r"^'(.*)'$"
regexConfigurationVariables = r"{(.*),(.*),(.*)}"

pythonTypes = {'int': int, 'float': float, 'complex':complex, 'str': str, 'tuple':tuple, 'list':list, 'set':set, 'frozenset':frozenset}
    
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
        parserHead = parts[0]
        parserBody = parts[1]
    else:
        parserBody = parts[0]

def inputTextToList(text):
    temp = []
    for line in text.splitlines():
        parts = line.split(defaultDelimiter)
        for part in parts:  
            temp.append(part)
    return temp


def setvar(name, value, t):#creates a global variable with a given value
    if not t in pythonTypes.keys():
        return False
    globals()[name] = pythonTypes[t](value) #cast to type
    return True

####parsing functions
def parseConfigurationVariables(text):
    matches = re.finditer(regexConfigurationVariables, text, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        tempConfig = [] #0 -> name 1 -> value, 2 -> type    
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            tempConfig.append(match.group(groupNum))
        tempConfig[1] = re.sub(regexRemoveQuoteFromString, "\\1", tempConfig[1], 0)
        if not setvar(tempConfig[0], tempConfig[1], tempConfig[2]):
            print("ERROR - Failed to apply configuration variable (INVALID TYPE): number %d, name: %s, type: %s" % (matchNum, tempConfig[0], tempConfig[2]))
    return False

def parseLenValue(text):#checks if the text is a value or a variable name containing the size in the format {varName}
    return int(text)
def parseIsolatedVariables(text):
    global inputText, inputPointer
    text = text.strip(defaultDelimiter)     #remove side delimeters
    match = re.search(regexSingleVar,part)  #match the format (varName, type)
    if match:
        if setvar(match.group(1), inputText[0], match.group(2)):
            del inputText[0]
        else:
            print("ERROR - Failed to input variable (INVALID TYPE): name: %s, value: %s, type: %s" % (match.group(1), inputText[0], match.group(2)))
    else:
        match = re.search(regexSingleVarLen,part)  #match the format (varName, type, len)
        if match: 
            length = parseLenValue(match.group(3))
            if length > len(inputText):#the user is asking for more than available
                print("ERROR - Failed to input variable (WRONG LENGTH SPECIFIED): name: %s, length: %d, type: %s" % (match.group(1), length, match.group(2)))
            if match.group(2) == "str":
                if not match.group(2) in globals:
                    setvar(match.group(1), inputText[0], match.group(2)) #instantiate the string
                    del inputText[0]
                for valIndex in range(length):
                    globals()[match.group(1)]+=inputText[0]
                    del inputText[0]
            elif match.group(2) == "tuple":
                pass
            elif match.group(2) == "list":
                pass
            elif match.group(2) == "set":
                pass
            elif match.group(2) == "frozenset":
                pass
            else:
                print ("You specified the len attribute(%d) for an unexpected type (%s)" % (parseLenValue(match.group(3)), match.group(2)))
def printStatus():
    #print("parserHead\n"+parserHead)
    #print("\nparserBody\n"+parserBody)
    print("n = " + str(n))
    #print("anotherParameter2 = " + str(anotherParameter2))


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
        print("-----------------------Parsing line %d " % lineIndex)
    line = line.strip(defaultDelimiter)
    parts = line.split(defaultDelimiter)
    for part in parts:                      #iterate line part by part, separated by the defaultDelimiter
        if len(inputText) == 0:
            print("\nWARNING: The input file has less variables than the parser file indicated, stopped at instruction:\n       %s" % part)
            exit()
        parseIsolatedVariables(part)

printStatus()
