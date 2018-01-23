import re


def readFile(filename):  # read a file or print an error
    def readFile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()


def textToList(text, delimiter=None):
    temp = []
    for line in text.splitlines():
        parts = line.split(delimiter)
        for part in parts:
            if len(part) > 0:
                temp.append(part)
    return temp


# receives a random type container and adds a new element to it
def addElementToContainer(container, element, connector=" "):
    if type(container) == list or type(container) == bytearray:
        container.append(element)
    elif type(container) == tuple:
        container += (element,)
    elif type(container) == dict:
        container.update(element)

    elif type(container) == str:
        if len(container) == 0:
            container = element
        else:
            container += connector + element  # ads an extra connector

    elif type(container) == bytes:
        if len(container) == 0:
            container = bytes(element, 'utf8')
        else:
            # ads an extra connector
            container += bytes(connector + element, 'utf8')

    elif type(container) == set:  # convert to list -> add -> convert to set
        container = set(addElementToContainer(list(container), element))
    elif type(container) == frozenset:  # convert to list -> add -> convert to frozenset
        container = frozenset(addElementToContainer(list(container), element))
    return container


def cast(to, value=None):
    primitiveTypes = {'int': int, 'float': float, 'complex': complex, 'bool': bool, 'str': str, 'bytes': bytes,
                      'list': list, 'dict': dict, 'tuple': tuple, 'set': set, 'frozenset': frozenset, 'bytearray': bytearray}
    if value == None:
        return primitiveTypes[to]()
    if to == "bytes":
        return primitiveTypes[to](value, encoding="utf-8")
    return primitiveTypes[to](value)
