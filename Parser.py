# Append list of elements in self.lines and check that everything is stored correctly 
# (use REGEX from COMPv1)

import re
from collections import deque

class Rules:
    def __init__(self):
        self.lines = []

    def display(self):
        for line in self.lines:
            print line

class Facts:
    def __init__(self):
        self.facts = []

    def display(self):
        print(self.facts)

class Query:
    def __init__(self):
        self.queriedFactNum = []

    def display(self):
        for query in self.queriedFactNum:
            print query

# Class used as a stack to store the current goal we are trying to evaluate
class Stack:
    def __init__(self):
        self.stack = deque()

    def push(self, value):
        self.stack.append(value)

    def top(self):
        return self.stack[len(self.stack) - 1]

    def pop(self):
        return self.stack.pop()

    def display(self):
        for goal in self.stack:
            print goal

# Removing whitespaces
def removeWs(line):
    line = line.strip()
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    return line

# Function called to set the facts
def setFacts(fact, initFacts):

    # We loop through each fact, check if it is in the range [A:Z], and set it to True if it is
    for f in initFacts:
        if (ord(f) < 65 or ord(f) > 90):
            raise Exception(f, " is invalid.")
        fact.facts[ord(f) - 65] = True
    return fact

def setQuery(query, queriedFact):   
    for q in queriedFact:
        if (ord(q) < 65 or ord(q) > 90):
            raise Exception(q, " is invalid.")
        query.queriedFactNum.append(ord(q) - 65)
    return query


# Function called to parse the list of lines
def parseLines(lineList):

    # We loop through the list, and delete any comment we don't want
    i = 0
    while (i < len(lineList)):
        lineList[i] = lineList[i].strip()
        if ('#' in lineList[i]):
            lineList[i] = lineList[i][:lineList[i].find('#')]
        if (len(lineList[i]) == 0):
            del lineList[i]
        i += 1
    return lineList

# Handles the parsing of the file
def fileParsing(filename):

    # Creating instances of the rules, facts, and query classes
    r = Rules()
    fact = Facts()
    query = Query()
    goal = Stack()
    i = 0

    # Initializing every facts to False
    while (i < 26):
        fact.facts.append(False)
        i += 1
    
    # We read the file and store all the lines in a list of string
    with open(filename) as f:
        lineList = f.readlines()

    # Then we parse the strings, making a first clean
    lineList = parseLines(lineList)

    i = 0

    # Finally we loop through the list of strings and we fill the data in our classes
    for line in lineList:
        r.lines.append(removeWs(line))
        if line[0] == '=':
            fact = setFacts(fact, line[1:])
        elif (line[0] == '?'):
            query = setQuery(query, line[1:])

    # End we return the rules, facts and queries
    return r, fact, query, goal;
    