from pyparsing import *

#delimiters
c = Suppress(",") #comma
op = Suppress("(") #open parentheses
cp = Suppress(")") #close parentheses
osb = Suppress("[") #open square brackets
csb = Suppress("]") #close square brackets
ocb = Suppress("{") #open curly brackets
ccb = Suppress("}") #close curly brackets

#elementary operators
pType = Or([Literal("int"), Literal("long"), Literal("float"), Literal("bool"), Literal("complex")]) #primitive types
sType = Or([Literal("str"), Literal("bytes")]) #sequence types
ciType = Or([Literal("tuple"), Literal("frozenset")]) #container immutable ypes
cmType = Or([Literal("list"), Literal("dict"), Literal("set"), Literal("bytearray")]) #container mutable types

#useful base constructs
varName = Combine(OneOrMore(Word(alphas)) + ZeroOrMore(Word(alphanums + "_"))) #example n camelCase n1 with_underscore
length = Or([Word(nums), Combine(Literal("{") + varName + Literal("}"))]) #example 10 {varName}

#primitives
primitiveType = op + Or([pType, sType]) + cp #example (int) (str)
primitiveNameType = op + Or([pType, sType]) + c + varName + cp #example (int, name) (str, name)
primitiveNameLen = op + sType + c + length + cp #example (str, 3) (str, {n}) NOT (int, 3)
primitiveNameTypeLen = op + sType + c + varName + c + length + cp #example (bytes, names, 3)
primitive = Or([primitiveType, primitiveNameType, primitiveNameLen, primitiveNameTypeLen]) #one of the above
primitive = Group(primitive)

#containers immutable
containerISimple = osb + ciType + c + length + c + primitive + csb #example [frozenset, 10, (int)]
containerIName = osb + ciType + c + length + c + primitive + c + varName + csb #example [tuple, 10, (int), name]
containerI = Or([containerISimple, containerIName])
containerI = Group(containerI)

#containers mutable
containerMSimple = osb + cmType + c + length + c + primitive + csb #example [list, 10, (int)]
containerMName = osb + cmType + c + length + c + primitive + c + varName + csb #example [list, 10, (int), name]
containerM = Or([containerMSimple, containerMName])
containerM = Group(containerM)

#containers global
container = Or([containerI, containerM])

#dictionaries
dictionary = ocb + Or([primitive, containerI]) + c + Or([primitive, container]) + ccb #example {int, float} {str, list}
dictionary = Group(dictionary)


#grammar
grammar = Forward()
grammar = ZeroOrMore(primitive | container | dictionary)

#test
toParsePrimitive = """
(int)
(long, name)
(str, name)
(bool, result_best)
(str, 10)
(bytes, {n})
"""

toParseContainer = """
[list, 10, (str)]
[list, {n}, (int), name]
"""

toParseDictionary = """
{(int),(int)}
{(int, lol),(int)}
{(int, lol),[list, 10, (str, 2)]}
"""

toParse = toParsePrimitive + toParseContainer + toParseDictionary
print(grammar.parseString(toParse))

print(ZeroOrMore(primitive).parseString(toParsePrimitive))
print(ZeroOrMore(container).parseString(toParseContainer))
print(ZeroOrMore(dictionary).parseString(toParseDictionary))
