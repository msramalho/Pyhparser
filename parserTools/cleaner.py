#This file contains all the functions that are used to parse the input file or text
import re

regexComment = r"\#.*?$"
regexCommentReplacement = ""
regexDuplicateWhitespace= r"([\r\t\f ])+"
regexDuplicateParagraphs= r"([\v\n])+"
regexWhitespaceLeftBracket =  r"({)[\r\t\f ]*"
regexWhitespaceRightBracket =  r"[\r\t\f ]*(})"
regexSpaces = r"([,:{}\[\]]) "       #remove spaces after :,[]{}(), replace by \\1
regexRemoveSingleQuoteFromString = r"^'(.*)'$"
regexRemoveDoubleQuoteFromString = r"^\"(.*)\"$"

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
    return re.sub(regexSpaces, "\\1", text, 0, re.MULTILINE)
def removeQuotes(text):
    text = re.sub(regexRemoveSingleQuoteFromString, "\\1", text, 0)
    return re.sub(regexRemoveDoubleQuoteFromString, "\\1", text, 0)
def cleanText(text):
    return removePunctuationSpaces(removeRedundantWhitespaces(removeComments(text)))
def cleanInput(input):#todo: see if removeRedundantWhitespaces is sufficient
    return removePunctuationSpaces(removeRedundantWhitespaces(input))
