from pyparsing import *

#elementary operators
pType = Or(Word("int") | Word("long") | Word("float") | Word("bool") | Word("complex")) #primitive types
sType = Or(Word("str") | Word("bytes") | Word("bytearray")) #sequence types
cType = Or(Word("list") | Word("dict") | Word("set") | Word("tuple") | Word("frozenset")) #containerTypes
aType = Or(pType | sType | cType) #any type

immutable = Or(pType | Word("str") | Word("bytes") | Word("tuple") | Word("frozenset"))

varName = Combine(OneOrMore(Word(alphas)) + ZeroOrMore(Word(alphanums + "_"))) #example n camelCase n1 with_underscore

c = Suppress(",")	#comma
op = Suppress("(")	#open parentheses
cp = Suppress(")")	#close parentheses
osb = Suppress("[")	#open square brackets
csb = Suppress("]")	#close square brackets
ocb = Suppress("{")	#open curly brackets
ccb = Suppress("}")	#close curly brackets

length = Or(Word(nums) | Combine(Word("{") + varName + Word("}")))

#primitives
primitiveType = op + Or(pType | sType) + cp	#example (int) (str)
primitiveNameType = op + Or(pType | sType) + c + varName + cp	#example (int, name) (str, name)
primitiveNameLen = op + sType + c + length + cp	#example (str, 3) (str, {n}) NOT (int, 3)
primitiveNameTypeLen = op + sType + c + varName + c + length + cp	#example (bytes, names, 3)
primitive = Group(primitiveType | primitiveNameType | primitiveNameLen | primitiveNameTypeLen) #one of the above

#containers
containerSimple = osb + cType + c + length + c + primitive + csb    #example [list, 10, (int)]
containerName = osb + cType + c + length + c + primitive + c + varName + csb    #example [list, 10, (int), name]

container = Group(containerSimple | containerName)


#dictionaries
#TODO: decide how dictionaries will be, this will depend on immutable, but maybe the immutable have to be redifined on their own
dictionary = ocb + immutable + c + aType + ccb  #example {int, float} {str, list}


#primitives or container = poc
poc = ZeroOrMore(primitive | container)

#grammar
grammar = Forward()
grammar = poc

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

{(int), int}
{int, str}
"""

print(grammar.parseString(toParse))
