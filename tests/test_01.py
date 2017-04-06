from testUtils import *

title = "Test anonymous single var parsing"
inputVar = "  10   23.998   (2+3j)       1j      1    True  "
parserVar = "(int) (float) (complex) (complex) (bool)  (bool)"
fullTest(inputVar, parserVar, title, 0)


title = "Test named single var parsing"
inputVar = "    10      23.998       (2+3j)         1j           1         True   "
parserVar = "(n, int) (x, float) (c1, complex) (c2, complex) (b1, bool)  (b2, bool)"
fullTest(inputVar, parserVar, title, 6)
