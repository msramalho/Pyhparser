# Master Parser Python

Python lib to avoid wasting time in parsing input files data in contents and challenges

---

## With explicit optionals

- Single variables:
(varName, typeUnit, [length])
- Container variables:
    (varName, typeContainer, length, unitType)

---

## With implicit optionals

- Single variables (int, float, bool, complex, str):
    (varName, typeUnit)
    (varName, typeUnit, length)
    
    (str, length)               *this can only be used inside container or class variables, never by itself
    (typeUnit)                  *this can only be used inside container or class variables, never by itself
- Container variables (str, list, dict, tuple, list):
    [varName, typeContainer, length, unitType]
- Classes variables (class):
    [varName, class, classname, param1type, param2type, ..., paramNtype] #ordered in constructor order

---

## Parameters

- length:
    Optional for int, str, float, complex
    - lengthNumber  ex: 10
    - {lengthVar}   ex: {num}

---

## Examples

- Simple int:
`(x, int)`
- String with 3 words:
`(name, str, 3)`
- Class instance with 4 parameters (one of which is a dict):
`[peter, class, person, (int), (str), (float), {(int), (float)}]`
- List of integers:
`[myInts, list, 10, (int)]`
- Dict with 10 elements:
`[myDict, dict, {lengthtVariableName}, {(int), (string)}]`
- List of pairs of dicts of int and string:
`[varName, list, 10, [tempDict, dict, 2, {int, float}]`
- List with variable lentgths:
`[listSizes, list, 3, (int)]`
`[lengthyStrings, list, 3, (str, {listSizes;lengthyStrings}), ]` the size of each string is in the corresponding index of the listSizes list

## Todo

https://stackoverflow.com/questions/3451779/how-to-dynamically-create-an-instance-of-a-class-in-python
klass = globals()["class_name"]
instance = klass()

https://stackoverflow.com/questions/2136760/creating-an-instance-of-a-class-with-a-variable-in-python
class Foo(object):
    pass

class Bar(object):
    pass

dispatch_dict = {"Foo": Foo, "Bar": Bar}
dispatch_dict["Foo"]() # returns an instance of Foo