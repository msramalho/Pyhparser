import sys
sys.path.append('../../')
from pyhparser import *

def printStatus(myVars):
    for key, value in myVars.items():
        print("%20s:  %s" % (key, value))
    
p = pyhparser("4 Miguel Frase de tamanho quatro John Lajoie 12.12",
             "(n, int) (nome, str) (nome2, str, {n}) (nome3, str, 2) (temp, float)", [])

p.parse()
print("TOTAL VARS: %d" % len(p.getVariables()))
#to display our results
printStatus(p.getVariables())