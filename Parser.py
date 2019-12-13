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
        self.line = ""

    def display(self):
        for fact in self.facts:
            print(fact + "  ->  " + str(self.facts[fact]["value"]).ljust(len("False")) + "  ->  visited: " + str(self.facts[fact]["visited"]))
    
    def shortDisplay(self):
        print("=", end="")
        for fact in self.facts:
            if self.facts[fact]["value"] == True:
                print(fact, end="")
    
    def reset(self, facts):
        # First I reset everything back to false
        for fact in self.facts:
            self.facts[fact]["value"] = False
            self.facts[fact]["visited"] = False
        for char in facts:
            if (ord(char) < 65 or ord(char) > 90):
                raise Exception(char, " is invalid.")
            else:
                self.facts[char]["value"] = True
        self.line = facts


class Query:
    def __init__(self):
        self.queriedFacts = []

    def display(self):
        for query in self.queriedFacts:
            print(query, end="")
    
    def reset(self, newQueries):
        for char in newQueries:
            if (ord(char) < 65 or ord(char) > 90):
                raise Exception(char, " is invalid.")
        self.queriedFacts = fromStringToList(newQueries)

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

def fromStringToList(string):
    l = []
    for char in string:
        l.append(char)
    return l
            
# Removing whitespaces
def removeWs(line):
    line = line.strip()
    line = line.rstrip()
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace('\n', "")
    return line

# Function called to set the facts
def setFacts(fact, initFacts):

    # We loop through each fact, check if it is in the range [A:Z], and set it to True if it is
    for f in initFacts:
        if (ord(f) < 65 or ord(f) > 90):
            raise Exception(f, " is invalid.")
        fact.facts[f]["value"] = True
        fact.line += f
    return fact

def setQuery(query, line):   
    for char in line:
        if (ord(char) < 65 or ord(char) > 90):
            raise Exception(char, " is invalid.")
        query.queriedFacts.append(char)
    return query

# Function called to parse the list of lines
def parseLines(lineList):

    i = 0
    while (i < len(lineList)):
        lineList[i] = removeWs(lineList[i].rstrip())
        if ('#' in lineList[i]):
            lineList[i] = lineList[i][:lineList[i].find('#')]
        if (lineList[i] == "\n"):
            del lineList[i]
        i += 1
    return lineList

# Handles the parsing of the file
def fileParsing(filename):

    r = Rules()
    fact = Facts()
    query = Query()
    
    with open(filename) as f:
        lineList = f.readlines()
    lineList = parseLines(lineList)
    for line in lineList:
        if (len(line) is 0):
            pass
        elif line[0] == '=' and len(line) > 1:
            fact = setFacts(fact, line[1:])
        elif line[0] == '?' and len(line) > 1:
            query = setQuery(query, line[1:])
        else:
            r.lines.append(removeWs(line))
    return r, fact, query;