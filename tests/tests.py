import unittest
from pyhparser import Pyhparser, readFile


def getParseObject(inputs, parser, classes=[]):
    p = Pyhparser(inputs, parser, classes)
    p.parse()
    return p


def getParseVars(inputs, parser, classes=[]):
    return getParseObject(inputs, parser, classes).getVariables()


class BehaviouralTest(unittest.TestCase):
    def test_invalid_len(self):
        with self.assertRaises(Exception):
            t = getParseVars("my string", "(str, {notCreated})")

    def test_no_more_input(self):
        with self.assertRaises(Exception):
            t = getParseVars("my string", "(str, a, 10)")

    def test_fullParse(self):
        s = "my string is very long"
        t = getParseObject(s, "(str, 2)")
        self.assertFalse(t.fullParse())
        t = getParseObject(s, "(str, 5)")
        self.assertTrue(t.fullParse())

    def test_readFile(self):
        inputVar = readFile("fakeFile.txt")
        self.assertEqual(None, inputVar)

    def test_print_recursive(self):
        inputVar = readFile("tests/input.txt")
        parserVar = readFile("tests/parser.txt")
        p = Pyhparser(inputVar, parserVar, [Complex])
        p.parse()
        p.printRecursive(p.parserRead)


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

    def test_float(self):
        floats = [-10, -3.2, 0, 1.4, 12]
        for f in floats:
            s = "%s" % f
            t = getParseVars(s, "(float)")
            self.assertDictEqual(t, {})
            t = getParseVars(s, "(float,n)")
            self.assertDictEqual(t, {"n": f})

    def test_bytes(self):
        t = getParseVars("a", "(bytes)")
        self.assertDictEqual(t, {})
        t = getParseVars("a b", "(bytes, 2)")
        self.assertDictEqual(t, {})
        t = getParseVars("a b c", "(bytes, bb, 3)")
        self.assertDictEqual(t, {'bb': b'a b c'})


class ContainersTest(unittest.TestCase):
    def test_list(self):
        l = [10, 20, 30, 40]
        s = " ".join(str(x) for x in l)
        t = getParseVars(s, "[list, %d, (int), l1]" % len(l))
        self.assertDictEqual(t, {"l1": l})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")

    def test_set(self):
        t = getParseVars("10 20 30", "[set, 3, (int), s1]")
        self.assertDictEqual(t, {'s1': {10, 20, 30}})
        t = getParseVars("10 10 10 20 30", "[set, 5, (int), s2]")
        self.assertDictEqual(t, {'s2': {10, 20, 30}})

    def test_frozen_set(self):
        t = getParseVars("10 20 30", "[frozenset, 3, (int), fs1]")
        self.assertDictEqual(t, {'fs1': {10, 20, 30}})
        t = getParseVars("10 10 10 20 30", "[frozenset, 5, (int), fs2]")
        self.assertDictEqual(t, {'fs2': {10, 20, 30}})


class DictionaryTest(unittest.TestCase):
    def test_dict(self):
        t = getParseVars("10 blue 20 green", "{(int), (str), myDict2, 2}")
        self.assertDictEqual(t, {"myDict2": {10: "blue", 20: "green"}})
        with self.assertRaises(ValueError):
            t = getParseVars("10.12", "(int)")


class ClassTest(unittest.TestCase):
    def test_class_incomplete(self):
        t = getParseVars(
            "10.23 55", "[class, Complex, {realpart: (float), imagpart: (int)}, cn1]", [Complex])
        self.assertIsInstance(t["cn1"], Complex)
        self.assertEqual(t["cn1"].realpart, 10.23)
        self.assertEqual(t["cn1"].imagpart, 55)
        self.assertEqual(t["cn1"].special, "not special")

    def test_class_complete(self):
        t = getParseVars("3.141592653 70 1300     veryNice",
                         "[class, Complex, {realpart: (float), imagpart: (int), special: {(int), (str)}}, cn2]", [Complex])
        self.assertIsInstance(t["cn2"], Complex)
        self.assertEqual(t["cn2"].realpart, 3.141592653)
        self.assertEqual(t["cn2"].imagpart, 70)
        self.assertDictEqual(t["cn2"].special, {1300: "veryNice"})

    def test_class_complete_inner(self):
        t = getParseVars("3.141592653 70 4        string with four words",
                         "[class, Complex, {realpart: (float), imagpart: (int), special: {(int, myInt), (str, {myInt})}}, cn3]", [Complex])
        self.assertIsInstance(t["cn3"], Complex)
        self.assertEqual(t["cn3"].realpart, 3.141592653)
        self.assertEqual(t["cn3"].imagpart, 70)
        self.assertDictEqual(t["cn3"].special, {4: "string with four words"})

    def test_class_missing(self):  # class complex is unknown so it fails
        with self.assertRaises(Exception):
            t = getParseVars(
                "10.23 55", "[class, Complex, {realpart: (float), imagpart: (int)}, cn4]")


class Complex:
    def __init__(self, realpart, imagpart, special="not special"):
        self.realpart = realpart
        self.imagpart = imagpart
        self.special = special


class Dog:
    def __init__(self, nome, pesos, unidade):
        self.nome = nome
        self.pesos = pesos
        self.unidade = unidade


if __name__ == '__main__':
    unittest.main()
