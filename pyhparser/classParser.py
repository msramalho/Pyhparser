#this class is used to create class instances from class names and an array of parameter

class classParser:#stores and manages a list of the classes used by the parser, also creates instances of them
    def __init__(self, classList):
        self.classList = classList
        self.classNames = list(map(lambda c: c.__name__, classList))
    def hasClass(self, className):
        return className in self.classNames
    def getClass(self, className):
        for c in self.classList:
            if c.__name__ == className:
                return c
        return None
    def initClass(self, className, parameters):#dict
        return self.getClass(className)(**parameters) if self.hasClass(className) else False