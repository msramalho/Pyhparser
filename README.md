# Master Parser Python 
### The Hackahton Quintessence

Avoid wasting time parsing input files in **hackathons**. 
**mparser** (for short) parses input files (_inputFile.txt_) into python variables by specifying the layout of the variables (_parserFile.txt_):

| Parser File  | Input File | Result |
|:------------:|:----------:|:----------:|
| (x, int)     | 10         | x = 10, you can now use x in your script         |
## Instructions (no pip or easy_install)
1. Download [mparser.py](https://github.com/msramalho/masterParserPython/blob/master/mparser.py);
2. Include this file in your working dir;
3. Do `import mparser`;
4. Parse your files:
    ```python 
    def mparse(parserFile, inputFile, [verbose], [classesUsed])
   #Examples:
    mparser.mparse("fileParser.txt","fileInput.txt")
    mparser.mparse("fileParser.txt","fileInput.txt", True)
    mparser.mparse("fileParser.txt","fileInput.txt", False, [MyClass1, MyClass2])
     ```
5. If your content is in strings call the function `mparser.mparseContent` instead of `mparser.mparse` and replace the file names by your text values;
6. Now assign the parsed variables to your scope with:
```python
tempGlobals = mparser.getGlobals()
for key, value in tempGlobals.items():
    globals()[key] = value
```
### Full code example:
```python
#MyClass must be a class defined somewhere before you call mparse
mparser.mparse("fileParser.txt","fileInput.txt", False, [MyClass]) #not verbose
tempGlobals = mparser.getGlobals()
for key, value in tempGlobals.items():
    globals()[key] = value
```

## Parsing format

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

## Examples

| Purpose  | Parser File  | Input File | Result |
| ---------| ------------ | ---------- | ------ |
| Simple int | `(x, int)`  | 3        | x = int("3")|
| Simple str | `(s, str)`  | MyString  | s = "MyString"|
| Str with 3 words | `(S, str, 3)`  | A b C  | S = "A b C"|
| list of 4 ints | `[myInts, list, 10, (int)]`  | 1 2 4 8  | myInts = [1,2,4,8]|
| list of 3 ints (see `x` above) | `[myInts2, list, {x}, (int)]`  | 10 11 99  | myInts2 = [10,11,99]|
| dict of 2 elements | `[myDict, dict, 2, {(int), (string)}]`  | 10 blue 20 green  | s = {{10:"blue"},{20:"green"}}|
| list of 2 different sized strings* | `[sizes, list, 2, (int)] [myStrings, list, 2, (str, {sizes;myStrings})]`  | 1 3  lorem ipsum dolor sit | sizes = [1,3]; myStrings = ["lorem", "ipsum dolor sit"]|
| class instance of MyClass | `[mc, class, MyClass, {x:(int)},{y:(str)}] [myStrings, list, 2, (str, {sizes;myStrings})]`  | 10 Dez | mc = MyClass(x:10,y:'Dez')|

*the size of each string in the myStrings list is in the value of the corresponding index of the sizes list

#### More examples:
- See the [examples folder:](https://github.com/msramalho/masterParserPython/tree/master/examples)
  - [Global example 01](https://github.com/msramalho/masterParserPython/tree/master/examples/ex_01)
  - [Hashcode 2017 example](https://github.com/msramalho/masterParserPython/tree/master/examples/ex_hashcode2017)
- Class instance with 4 parameters (one of which is a dict):
``` 
[peter, class, Person, {age:(int)}, {name:(str)}, {height:(float)}, {keyValue:{(int), (float)}}]
```

## Features:
- [x] Parse essential types: str, int, float, complex, bool
- [x] Parse container types: list, dict, tuple
- [x] Parse classes
- [x] Recursive parsing


- [ ] Pip and easyinstall packages
- [ ] Implement set parsing
- [ ] Implement frozenset parsing


