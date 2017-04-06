#this file has all the functions to handle command line arguments
from parserTools.usage import *
from sys import argv
import getopt

def mparseCmd():#receives the input from the command line
    parserVerbosity = False
    try:
        options, remainder = getopt.getopt(argv[1:], 'hvu', ['help', 'verbose', 'unavailable'])
    except getopt.GetoptError as err:
        print('GETOPT ERROR:', err)
        displayUsage()
        exit(1)
    for opt, arg in options:
        if opt in ('-h', '--help'):
            displayUsage()
            exit()
        if opt in ('-v', '--verbose'):
            parserVerbosity = True
    ####Initial checks
    if len(remainder) != 2:
        print("Wrong number of arguments\n>>python %s -flags parseFile.txt inputFile.txt" % argv[0])
        exit()
    mparse(remainder[0], remainder[1], parserVerbosity)