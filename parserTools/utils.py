import re
from parserTools.cleaner import *

separatorString = ".body"
regexFixUserMissingSpaces = r"((\))(\())" #adds a space between )( if it is replaced by "\\2 \\3"

def readFile(filename):#read a file or print an error
    try:
        file = open(filename)
    except IOError:
        print("ERROR - Unable to open file %s" % filename)
        exit()
    return file.read()

def separateHeadBody(text):
    parserHead = parserBody = ""
    parts = text.split(separatorString,1)  #separate head from body
    if len(parts)==2:
        parserHead = parts[0].strip("\n")
        parserBody = parts[1].strip("\n")
    else:
        parserBody = parts[0].strip("\n")
    return parserHead, parserBody

def inputTextToList(text, delimiter):
    temp = []
    for line in text.splitlines():
        parts = line.split(delimiter)
        for part in parts:
            temp.append(part)
    return temp

def parseTextToList(text):
    i = 0
    lines = text.splitlines()
    fullLines = []
    temp = ""
    while i < len(lines):
        if isLineComplete(temp):
            temp = re.sub(regexFixUserMissingSpaces, "\\2 \\3", temp, 0, re.MULTILINE)
            fullLines.append(removePunctuationSpaces(removeRedundantWhitespaces(temp)))
            temp =lines[i]
        else:
            temp+=lines[i]
        if i == len(lines) - 1 and isLineComplete(temp):
            temp = re.sub(regexFixUserMissingSpaces, "\\2 \\3", temp, 0, re.MULTILINE)
            fullLines.append(removePunctuationSpaces(removeRedundantWhitespaces(temp)))
        i+=1
    return fullLines

def validTypeSingle(t):
    return t in ("int", "str", "bool", "float", "complex")

def validTypeContainer(t):
    return t in ("list", "dict", "tuple", "set", "frozenset")

def isLineComplete(line):#true is len > 0 and open parentheses = closed
    openBrackets = 0
    i = 0
    while i < len(line):
        if line[i] in ("{", "(", "["):
            openBrackets+=1
        elif line[i] in ("}", ")", "]"):
            openBrackets-=1
        i+=1
    return openBrackets == 0 and len(line)>0