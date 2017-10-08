from pyparsing import *

def Grammar():
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
    cType = Or([Literal("list"), Literal("set"), Literal("bytearray"), Literal("tuple"), Literal("frozenset")]) #container types

    #useful base constructs
    varName = Combine(OneOrMore(Word(alphas)) + ZeroOrMore(Word(alphanums + "_"))) #example n camelCase n1 with_underscore
    length = Or([Word(nums), Combine(Literal("{") + varName + Literal("}"))]) #example 10 {varName}
    comment = Suppress(Literal("#") + restOfLine)

    #set results name
    pType = pType.setResultsName("type")
    sType = sType.setResultsName("type")
    cType = cType.setResultsName("type")
    varName = varName.setResultsName("varName")
    length = length.setResultsName("len")

    #grammar start
    grammar = Forward()

    #primitives
    aType = Or([pType, sType]) # any type - primitive + sequences
    primitiveType = op + aType + cp #example (int) (str)
    primitiveTypeName = op + aType + c + varName + cp #example (int, name) (str, name)
    primitiveTypeLen = op + sType + c + length + cp #example (str, 3) (str, {n}) NOT (int, 3)
    primitiveTypeNameLen = op + sType + c + varName + c + length + cp #example (bytes, names, 3)
    primitive = Or([primitiveType, primitiveTypeName, primitiveTypeLen, primitiveTypeNameLen]) #one of the above
    primitive = Group(primitive.setResultsName("primitive"))

    #containers
    containerSimple = osb + cType + c + length + c + grammar.setResultsName("value") + csb #example [frozenset, 10, (int)]
    containerName = osb + cType + c + length + c + grammar.setResultsName("value") + c + varName + csb #example [tuple, 10, (int), name]
    container = Or([containerSimple, containerName])
    container = Group(container.setResultsName("container"))

    #dictionaries
    dictionaryFirst = primitive.setResultsName("left")
    dictionarySecond = grammar.setResultsName("right")
    dictionaryTypes = ocb + dictionaryFirst + c + dictionarySecond + ccb #example {int, float} {str, list}
    dictionaryTypesName = ocb + dictionaryFirst + c + dictionarySecond + c + varName + ccb #example {(int), (float), name}
    dictionaryTypesLen = ocb + dictionaryFirst + c + dictionarySecond + c + varName + ccb #example {(int), (float), 3} or {(int), (float), {lol}}
    dictionaryTypesNameLen = ocb + dictionaryFirst + c + dictionarySecond + c + varName+ c + length + ccb #example {(int), (float), name, 4}
    dictionary = Or([dictionaryTypes, dictionaryTypesName, dictionaryTypesLen, dictionaryTypesNameLen])
    dictionary = Group(dictionary.setResultsName("dictionary"))

    #grammar
    grammar<<= ZeroOrMore(primitive | container | dictionary)
    grammar.ignore(comment)
    return grammar