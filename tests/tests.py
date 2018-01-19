import unittest
import sys
sys.path.append("..")
from pyhparser import Pyhparser

def getParseVars(inputs, parser, classes=[]):
    p = Pyhparser(inputs, parser, classes)
    p.parse()
    return p.getVariables()

class PrimitivesTest(unittest.TestCase):
    def test_int(self):
        ints = [-10, 0, 10]
        for i in ints:
            s = "%s" % i
            t = getParseVars(s, "(int)")
            self.assertDictEqual(t, {})
            t = getParseVars(s, "(int,n)")
            self.assertDictEqual(t, {"n":i})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")


if __name__ == '__main__':
    unittest.main()