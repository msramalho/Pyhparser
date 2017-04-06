#this file has all the functions to help the user

def displayUsage():
    print("Master Parser Python")
    print("Parse input files (inputFile.txt) into python variables by specifying the layout of the variables (parserLayout.txt)")
    print("\nCommand line arguments (does not parse classes):")
    print("python mparserpython.py -flags inputeFile.txt parserLayout.txt")
    print("\nCommand line flags:")
    print("-h --help        display usage instructions")
    print("-v --verbose     increase verbosity")
    print("-u --unavailable list the variable names you cannot use in the parserText")
    print("\n\n\n-------------------------------------------")
    print("Module instructions (parses classes):")
    print(".Create parser file according to the format")
    print(".Have your input file name or content handy, code:\n\n")
    print("    import mparserpython\n")
    print('    mparserpython.mparse("parserFile.txt","inputFile.txt", False, [MyClass1, MyClass2]) #false means not verbose\n')
    print("    tempGlobals = mparserpython.getGlobals() #get the created variables")
    print("    for key, value in tempGlobals.items(): #iterate the created variables")
    print("        globals()[key] = value #include the created variables in your file as globals, locals() is also possible\n")
    print("    #use your variables as you would any other global :)")

