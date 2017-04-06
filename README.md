# Python Hackathon Parser - The Hackathon Quintessence

## What is this?
Pyhparser is a tool that parses input files in *hackathons* by simply specifying the format the data is in.

## Why would you use it?
Because you don't want to waste time in time-sensitive competitions naming, casting, iterating and reading variables. You want to focus on challenge and not on data parsing!

## How do you use it?
#### 1 - Install it on your computer
`pip install https://github.com/msramalho/pyhparser`
#### 2 - Copy and paste this code where you want to parse the input data:
```python
from pyhparser import *

inputVar = "10"                                #if the data is in a file do readFile("inputFile.txt")
parserVar = "(n, int)"                         #if the parser is in a file do readFile("parserFile.txt")
classes = []                                   #list of classes you use, if they appear in the parser
p = pyhparser(inputVar, parserVar, classes)    #create a pyhparser instance
p.parse()                                      #execute the parsing
tempGlobals = p.getVariables()                 #get the values of the created variables
for key, value in tempGlobals.items():
    globals()[key] = value                     #make the created var acessible from every scope
globals() = p.appendVariables(globals())       #directly make the variables available by their name
print(n)
```
The above code can be translated to:

| Input File | Parser File  | Result |
|:----------:|:------------:|:------:|
| 10         | (x, int)     | x = 10, you can now use x in your script|

## Instructions

### Parsing format

- Single variables (int, str, bool, float, complex):

    | Parser Format   | Is Temp? | example |
    | ------------- |:-------------:| -------------| 
    | (type)      | `true` | `(bool)` |
    | (type, len)      | `true` | `(int, 10)` |
    | (varName, type)      | `false` | `(myInt, int)` |
    | (varName, type, len) | `false` | `(myStr, str, 3)` |
    | (varName, type, {lenVarName}) | `false` | `(myStr2, str, {myInt})` |
    
- Container variables (list, dict, tuple):
    
    | Parser Format   | example |
    | ------------- | -------------| 
    | [varName, typeContainer, length, unitType]      | `[L, list, 10, (int)]` |
    | [varName, class, className, params]      | `[C, class, MyClass, {x:(int)},{y:(bool)}]` |

---

### Examples

| Purpose  | Parser File  | Input File | Result |
| ---------| ------------ | ---------- | ------ |
| Simple int | `(x, int)`  | 3        | x = int("3")|
| Simple str | `(s, str)`  | MyString  | s = "MyString"|
| Str with 3 words | `(S, str, 3)`  | A b C  | S = "A b C"|
| list of 4 ints | `[myInts, list, 10, (int)]`  | 1 2 4 8  | myInts = [1,2,4,8]|
| list of 3 ints (see `x` above) | `[myInts2, list, {x}, (int)]`  | 10 11 99  | myInts2 = [10,11,99]|
| dict of 2 elements | `[myDict, dict, 2, {(int), (string)}]`  | 10 blue 20 green  | s = {{10:"blue"},{20:"green"}}|
| list of 2 different sized strings* | `[sizes, list, 2, (int)] [myStrings, list, 2, (str, {sizes;myStrings})]`  | 1 3  lorem ipsum dolor sit | sizes = [1,3]; myStrings = ["lorem", "ipsum dolor sit"]|
| class instance of MyClass | `[mc, class, MyClass, {x:(int)},{y:(str)}]`  | 10 Dez | mc = MyClass(x:10,y:'Dez')|

*the size of each string in the myStrings list is in the value of the corresponding index of the sizes list

#### More examples:
- See the [examples folder:](https://github.com/msramalho/pyhparser/tree/master/examples)
  - [Global example 01](https://github.com/msramalho/pyhparser/tree/master/examples/ex_01)
  - [Hashcode 2017 example](https://github.com/msramalho/pyhparser/tree/master/examples/ex_hashcode2017)
- Class instance with 4 parameters (one of which is a dict):
``` 
[peter, class, Person, {age:(int)}, {name:(str)}, {height:(float)}, {keyValue:{(int), (float)}}]
```

## Features:
- [x] Parse essential types: str, int, float, complex, bool
- [x] Parse container types: list, dict, tuple
- [x] Parse classes
- [x] Recursive parsing

## TODO

- [ ] Good wiki
- [ ] Implement set parsing


