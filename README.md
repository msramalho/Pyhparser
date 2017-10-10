# Python Hackathon Parser - The Hackathon Quintessence

## What is this?
Pyhparser is a tool that parses input files input by describing the format the data is in, and allowing you to use them as your own variables. Due to its simplicity and speed it is great for *hackathons*, *Data Mining* and day-to-day data tasks.
#### Built for Python3
## Why would you use it?
Because:

 1. You don't want to waste time during time-sensitive competitions in casting, iterating and reading variables;
 1. You want to focus on building better algorithms and not on data parsing;
 1. You can define your parser file and reuse it, share it, or perform all necessary data input tinckering through it;
 1. It is intuitive and robust;
 1. Suggestions and requests can be submited through the [Issues](https://github.com/msramalho/Pyhparser-A-Python-Hackathon-Tool/issues) section.

## How do you use it?
#### 1 - Install it on your computer
`pip install git+https://github.com/msramalho/pyhparser`
#### 2 - Copy and paste this code where you want to parse the input data:
```python
from pyhparser import Pyhparser, readFile

inputVar = "10"                                #if the data is in a file do readFile("input.txt")
parserVar = "(int, n)"                         #if the parser is in a file do readFile("parser.txt")

p = Pyhparser(inputVar, parserVar)             #create a pyhparser instance
p.parse()                                      #execute the parsing
tempGlobals = p.getVariables()                 #get the values of the created variables
for key, value in tempGlobals.items():
    globals()[key] = value                     #make the created var acessible from every scope
print(n)                                       #print the value of n, the parsed variable
```
The above code can be translated to:

| Input File | Parser File  | Result |
|:----------:|:------------:|:------:|
| 10         | (int, n)     | n = 10, you can now use n in your script|

---

## Instructions

### Constructor
#### `Pyhparser(inputText, parseText, classes = [], stringConnector = " ")`
 - `inputText` - the text where the input data is;
 - `parseText` - the text where the parser commands are;
 - `classes` - a list of classes needed to parse the `inputText` with this `parseText`;
 - `stringConnector` - the string used to glue `str` parts together, since the default is `" "` they are returned separated by spaces (`this is an example`), but you can also decide to glue them with `"_"` (`this_is_an_example`).
 
 ### Methods
 #### `.parse()`
 Executes the parsing. 
 #### `.getVariables()`
 Returns the parsed variables. 
 #### `.fullParse()`
 Returns `True` if all the input data was parsed and `False` otherwise. 
 #### `.printRecursive(element, index = 0)`
 Prints in a recursive and visually elegant manner the structure of the parsed format from the `parseText`, can be used for debug purposes. For example:  `[list, {total}, {(int, sizeOfLine), (str, {sizeOfLine})}, sizesList]` would be displayed as:
 ```
 container: ['list', '{total}', [['int', 'sizeOfLine'], ['str', '{sizeOfLine}']], 'sizesList']
    Leaf: list
    Leaf: {total}
    dictionary: [['int', 'sizeOfLine'], ['str', '{sizeOfLine}']]
        primitive: ['int', 'sizeOfLine']
            Leaf: int
            Leaf: sizeOfLine
        primitive: ['str', '{sizeOfLine}']
            Leaf: str
            Leaf: {sizeOfLine}
    Leaf: sizesList
 ```

---

Notation used for the the Parser Grammar (reference):
 - **\* temp** - the parser command creates a temporary variable (it is not added to Pyhparser parsed variables by name);
 - **\* varName** - this variable is accessible through `varName`;
 - **\* length** - the `length` attribute can be a number like `10` or a variable that has been declared previously in Pyhparser in the format: `{varName}` as long as it is a numeric variable (1 by default);
 - **\* elemType** - the parser command `elemType` means that any other element of the Parser Grammar can be in here. Example `(long)`, `(str, 10, sentence)`, `[list, 10, (int)]`, ...
 - **\* elemTypePrimitive** - the parser command `elemTypePrimitive` means that only the primitive elements of the Parser Grammar can be in here. Example `(long)`, `(str, 10, sentence)`, ...

### Parser Grammar
#### 1. Length 1 primitives: `int`, `long`, `float`, `bool`, `complex`:
##### `(type)` - **\* temp**
##### `(type, varName)` - **\* varName**



#### 2. Length > 1 primitives: `str`, `bytes`:
##### `(type)` - **\* temp**
##### `(type, varName)` - **\* varName**
##### `(type, length)` - **\* temp** **\* length**
##### `(type, varName, length)` - **\* varName** **\* length**
For **str** and **bytes** the `length` is measured as spaces in the input, but you can choose what appears between the words in a string by setting the `stringConnector` in the Pyhparser constructor - default is `" "`, a space.

#### 3. Containers: `list`, `set`, `bytearray`, `tuple`, `frozenset`:
##### `[type, length, elemType]` - **\* temp** **\* length** **\* elemType**
##### `[type, length, elemType, varName]` - **\* temp** **\* varName** **\* elemType**


#### 4. Dictionaries: `dict`:
##### `{elemTypePrimitive, elemType}` - **\* temp** **\* elemTypePrimitive** **\* elemType**
##### `{elemTypePrimitive, elemType, varName}` - **\* varName** **\* elemTypePrimitive** **\* elemType**
##### `{elemTypePrimitive, elemType, length}` - **\* length** **\* elemTypePrimitive** **\* elemType**
##### `{elemTypePrimitive, elemType, length, varName}` - **\* varName** **\* length** **\* elemTypePrimitive** **\* elemType**

#### 5. Classes: `class`:
##### `[class, className, structure]` - **\* temp**
##### `[class, className, structure, varName]` - **\* varName**
The `structure` parameter is of the type: `{property1: elemType, property2: elemType, ...}`

---

### Examples

| Purpose  | Parser File  | Input File | Result |
| ---------| ------------ | ---------- | ------ |
| Simple int | `(int, x)`  | 3        | x = int("3")|
| Simple str | `(str, x)`  | MyString  | s = "MyString"|
| Str with 3 words | `(str, S, 3)`  | A b C  | S = "A b C"|
| Str with `x` words | `(str, S, {x})`  | A b C  | S = "A b C"|
| list of 4 ints | `[list, 4, (int), myInts]`  | 1 2 4 8  | myInts = [1,2,4,8]|
| list of 3 ints (see `x` above) | `[list, {x}, (int), myInts2]`  | 10 11 99  | myInts2 = [10,11,99]|
| dict | `{(int), (str), myDict1}`  | 10 blue  | myDict1 = {10:"blue"}|
| dict of 2 elements | `{(int), (str), myDict2, 2}`  | 10 blue 20 green  | myDict2 = {10:"blue", 20:"green"}|
| class instance of MyClass | `[class, MyClass, {x:(int)},{y:(str)}, mc]`  | 10 Dez | mc = MyClass(x=10,y='Dez')|

#### More examples:
- See the [examples folder:](https://github.com/msramalho/pyhparser/tree/master/examples)
  - [Global example 01](https://github.com/msramalho/pyhparser/tree/master/examples/ex_01)
  - [Hashcode 2017 example](https://github.com/msramalho/pyhparser/tree/master/examples/ex_hashcode2017)
- Class instance with 4 parameters (one of which is a dict):
```
[class, Person, {age:(int), name:(str), height:(float), keyValue:{(int), (float)}}]
```
## Features:
- [x] Parse all python primitives;
- [x] Parse all container types;
- [x] Parse classes;
- [x] Recursive parsing;
- [x] Fast and robust;
- [x] Easily changed;

## Drawbacks
So far only **one** minor drawback exists, which is the `key` of a [dict](#4-dictionaries-dict), in python can be any [immutable](https://stackoverflow.com/questions/8056130/immutable-vs-mutable-types) variable. Of these, Pyhparser accepts all except `frozenset` as a key. Meaning you cannot have (in Pyhparser, but you can in Python) a `dict` like: `{frozenset([1,4,76]): 10}`. This is intentional and for Grammar simplicity purposes.


