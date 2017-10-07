from pyparsing import *

#elementary operators
type = Word("int") | Word("long") | Word("float") | Word("bool") | Word("complex") | Word("str")

variableName = Word(alphanums + "_") # example n camelCase n1 with_underscore

c = Suppress(",")	# comma
op = Suppress("(")	# open parentheses
cp = Suppress(")")	# close parentheses
ob = Suppress("[")	# open brackets
cb = Suppress("]")	# close brackets

#primitives
primitiveType = op + type + cp	# example (int)
primitiveNameType = op + type + c + variableName + cp	# example (str, name)
primitiveNameTypeLen = op + type + c + variableName + c + Word(alphas) + cp	# example (str, names, 3)
primitive = Group(primitiveType | primitiveNameType | primitiveNameTypeLen)

#containers


#grammar
grammar = Forward()
grammar << ZeroOrMore(primitive)

#test
toParse = "(int) (str, name) (str, 100) (bool, result_best)"
res = grammar.parseString(toParse)

print(res)
