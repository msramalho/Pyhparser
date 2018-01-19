import unittest
import sys
sys.path.append('../')
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
            self.assertDictEqual(t, {"n": i})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")


class ContainersTest(unittest.TestCase):
    def test_list(self):
        l = [10, 20, 30, 40]
        s = " ".join(str(x) for x in l)
        t = getParseVars(s, "[list, %d, (int), l1]" % len(l))
        self.assertDictEqual(t, {"l1": l})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")


class DictionaryTest(unittest.TestCase):
    def test_list(self):
        t = getParseVars("10 blue 20 green", "{(int), (str), myDict2, 2}")
        self.assertDictEqual(t, {"myDict2": {10: "blue", 20: "green"}})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")

class ClassTest(unittest.TestCase):
    def test_list(self):
        t = getParseVars("10 blue 20 green", "{(int), (str), myDict2, 2}")
        self.assertDictEqual(t, {"myDict2": {10: "blue", 20: "green"}})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")


if __name__ == '__main__':
    unittest.main()
