from pyparsing import *

#elementary operators
pType = Or(Word("int") | Word("long") | Word("float") | Word("bool") | Word("complex")) #primitive types
sType = Or(Word("str") | Word("bytes") | Word("bytearray")) #sequence types
cType = Or(Word("list") | Word("tuple") | Word("dict") | Word("set") | Word("frozenset")) #containerTypes

immutable = Or(pType | Word("str") | Word("bytes") | Word("tuple") | Word("frozenset"))

varName = Combine(OneOrMore(Word(alphas)) + ZeroOrMore(Word(alphanums + "_"))) #example n camelCase n1 with_underscore

c = Suppress(",")	#comma
op = Suppress("(")	#open parentheses
cp = Suppress(")")	#close parentheses
osb = Suppress("[")	#open square brackets
csb = Suppress("]")	#close square brackets
ocb = Suppress("{")	#open curly brackets
ccb = Suppress("}")	#close curly brackets

length = Word(nums) | Combine(Word("{") + varName + Word("}"))

#primitives
primitiveType = op + (pType | sType) + cp	#example (int) (str)
primitiveNameType = op + (pType | sType) + c + varName + cp	#example (int, name) (str, name)
primitiveNameLen = op + sType + c + length + cp	#example (str, 3) (str, {n}) NOT (int, 3)
primitiveNameTypeLen = op + sType + c + varName + c + length + cp	#example (bytes, names, 3)
primitive = Group(primitiveType | primitiveNameType | primitiveNameLen | primitiveNameTypeLen) #one of the above

#dictionaries
dictionary = ocb + immutable + c + pType + ccb  #example {int, float}

#containers
containerSimple = osb + cType + c + length + c + primitive + csb    #example [list, 10, (int)]
containerName = osb + cType + c + length + c + primitive + c + varName + csb    #example [list, 10, (int), name]

container = Group(containerSimple | containerName)

#grammar
grammar = Forward()
grammar = (ZeroOrMore(primitive | container))

#test
toParse = """
(int)
(str, name)
(bool, result_best)
(str, 10)
(bytes, {n})
(bytearray, 3)
(long)

[list, 10, (str)]
[list, {n}, (int), name]
"""

print(grammar.parseString(toParse))
