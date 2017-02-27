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

| Purpose  | Parser File  | Input File | Result |
| ---------| ------------ | ---------- | ------ |
| Simple int | `(x, int)`  | 3        | x = int("3")|
| Simple str | `(s, str)`  | MyString  | s = "MyString"|
| Str with 3 words | `(S, str, 3)`  | A b C  | S = "A b C"|
| list of 4 ints | `[myInts, list, 10, (int)]`  | 1 2 4 8  | myInts = [1,2,4,8]|
| list of 3 ints (see `x` above) | `[myInts2, list, {x}, (int)]`  | 10 11 99  | myInts2 = [10,11,99]|
| dict of 2 elements | `[myDict, dict, 2, {(int), (string)}]`  | 10 blue 20 green  | s = {{10:"blue"},{20:"green"}}|
| list of 2 different sized strings | `[sizes, list, 2, (int)] [myStrings, list, 2, (str, {sizes;myStrings})]`  | 1 3  lorem ipsum dolor sit* | sizes = [1,3]; myStrings = ["lorem", "ipsum dolor sit"]|

* the size of each string is in the corresponding index of the listSizes list

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