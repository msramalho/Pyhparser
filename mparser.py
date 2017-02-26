from sys import argv
import re, tokenize, io

####Initial checks
if len(argv) != 3:
    print("Wrong number of arguments\n>>python %s parseText.txt inputFile.txt" % argv[0])
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
head=""
body=""

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

#extract the initial parameters


####Important functions
def readFile(filename):#read a file or print an error
    try:
        file = open(filename)
    except IOError:
        print("Unable to open file %s" % filename)
        return ""
    return file.read()

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

def parseIsolatedVariables(text):
    
    pass

def printStatus():
    global body, head
    print("HEAD\n"+head)
    print("\nBODY\n"+body)
    #print("anotherParameter = " + str(anotherParameter))
    #print("anotherParameter2 = " + str(anotherParameter2))


################################################## Main program flow

parseText = readFile(argv[1])       #get the text from the file
parseText = cleanText(parseText)    #remove irrelvant chars that affect parsing - aka OCD
parts = parseText.split(separatorString,1)  #separate head from body
if len(parts)==2:
    head = parts[0]
    body = parts[1]
else:
    body = parts[0]
    
parseConfigurationVariables(head)   #get the value of the configuration variables in the head
#printStatus()

for line in body.splitlines():
    line = line.strip(defaultDelimiter)
    print(line)
    parts = line.split(defaultDelimiter);
    for part in parts:
        part = part.strip('\n').strip('\t').strip(defaultDelimiter)
        