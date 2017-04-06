from testUtils import *

title = "Test dict named and unnamed var parsing"
inputVar = "   10       this is five words long    129 my words"
parserVar = "(myDic, {(int), (str, 5)}) {(int), (str, 2)}"
fullTest(inputVar, parserVar, title, 1)


title = "Test list of dicts var parsing"
inputVar = "124 True 234 False 345 0 456 1 567 true"
parserVar = "[myDicts, list, 5, {(int), (bool)}]"
fullTest(inputVar, parserVar, title, 1)