# Append list of elements in self.lines and check that everything is stored correctly 
# (use REGEX from COMPv1)

class Rules:
    def __init__(self):
        self.lines = []

def parseLines(lineList):
    i = 0
    while (i < len(lineList)):
        lineList[i] = lineList[i].strip()
        if (lineList[i].find('#') != -1):
            lineList[i] = lineList[i][:lineList[i].find('#')]
        if (len(lineList[i]) == 0):
            del lineList[i]
        i += 1
    return lineList

def fileParsing(filename):
    with open(filename) as f:
        lineList = f.readlines()
    lineList = parseLines(lineList)
    