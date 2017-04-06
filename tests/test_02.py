from testUtils import *

title = "Test list creation"
inputVar = "      5        each word is another word    "
parserVar = "(size, int) [myList, list, {size}, (str)]"
fullTest(inputVar, parserVar, title, 2)

title = "Test list creation variable size"
inputVar = "      3          1        2         4           first now second and finally the last    "
parserVar = "(size, int) [sizesList, list, {size}, (int)] [sentences, list, {size}, (str, {sizesList;sentences})]"
fullTest(inputVar, parserVar, title, 3)