# Append list of elements in self.lines and check that everything is stored correctly 
# (use REGEX from COMPv1)

import re
from collections import deque

class Rules:
    def __init__(self):
        self.lines = []

    def display(self):
        for line in self.lines:
            print(line)

class Facts:
    def __init__(self):
        self.facts = {
            'A': {
                "value": False,
                "visited": False
            },
            'B': {
                "value": False,
                "visited": False
            },
            'C': {
                "value": False,
                "visited": False
            },
            'D': {
                "value": False,
                "visited": False
            },
            'E': {
                "value": False,
                "visited": False
            },
            'F': {
                "value": False,
                "visited": False
            },
            'G': {
                "value": False,
                "visited": False
            },
            'H': {
                "value": False,
                "visited": False
            },
            'I': {
                "value": False,
                "visited": False
            },
            'J': {
                "value": False,
                "visited": False
            },
            'K': {
                "value": False,
                "visited": False
            },
            'L': {
                "value": False,
                "visited": False
            },
            'M': {
                "value": False,
                "visited": False
            },
            'N': {
                "value": False,
                "visited": False
            },
            'O': {
                "value": False,
                "visited": False
            },
            'P': {
                "value": False,
                "visited": False
            },
            'Q': {
                "value": False,
                "visited": False
            },
            'R': {
                "value": False,
                "visited": False
            },
            'S': {
                "value": False,
                "visited": False
            },
            'T': {
                "value": False,
                "visited": False
            },
            'U': {
                "value": False,
                "visited": False
            },
            'V': {
                "value": False,
                "visited": False
            },
            'W': {
                "value": False,
                "visited": False
            },
            'X': {
                "value": False,
                "visited": False
            },
            'Y': {
                "value": False,
                "visited": False
            },
            'Z': {
                "value": False,
                "visited": False
            }
        }

    def display(self):
        print(self.facts)

class Query:
    def __init__(self):
        self.queriedFacts = []

    def display(self):
        for query in self.queriedFacts:
            print(query)

# Class used as a stack to store the current goal we are trying to evaluate
class Stack:
    def __init__(self):
        self.stack = deque()

    def push(self, value):
        self.stack.append(value)

    def top(self):
        if len(self.stack) > 0:
            return self.stack[len(self.stack) - 1]
        raise Exception("Stack is empty")

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        raise Exception("Stack is empty")

    def display(self):
        if len(self.stack) > 0:
            for goal in self.stack:
                print(goal)
        else:
            print("Stack is empty")

def isOperator(c):
    if (c is '+' or c is '-' or c is '|' or c is '!'):
        return 1

# Verifies line's validity and returns an error if invalid
def verifline(line):
    i = 0
    allowedChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZ=><!+-^()|"
    while (i < len(line)):
        if (i + 1 < len(line) and isOperator(line[i]) and isOperator(line[i + 1])):
            raise Exception(line, "is invalid.")
        if (line[i] not in allowedChar):
            raise Exception(line, "is invalid.")
        i += 1
            
# Removing whitespaces
def removeWs(line):
    line = line.strip()
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    verifline(line)
    return line

# Function called to set the facts
def setFacts(fact, initFacts):

    # We loop through each fact, check if it is in the range [A:Z], and set it to True if it is
    for f in initFacts:
        if (ord(f) < 65 or ord(f) > 90):
            raise Exception(f, " is invalid.")
        fact.facts[f]["value"] = True
    return fact

def setQuery(query, line):   
    for char in line:
        if (ord(char) < 65 or ord(char) > 90):
            raise Exception(char, " is invalid.")
        query.queriedFacts.append(char)
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
    
    # We read the file and store all the lines in a list of string
    with open(filename) as f:
        lineList = f.readlines()

    # Then we parse the strings, making a first clean
    lineList = parseLines(lineList)

    i = 0

    # Finally we loop through the list of strings and we fill the data in our classes
    for line in lineList:
        if line[0] == '=':
            fact = setFacts(fact, line[1:])
        elif (line[0] == '?'):
            query = setQuery(query, line[1:])
        else:
            r.lines.append(removeWs(line))

    # End we return the rules, facts and queries
    return r, fact, query, goal;
    
