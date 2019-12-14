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
        self.facts = {}
        for index in range(26):
            char = 'A'
            i = ord(char)
            i += index
            char = chr(i)
            self.facts[char] = {
                "value": False,
                "visited": False
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
    
    # --------------------------------
    # First I reset everything back to false
    # --------------------------------
    def reset(self, facts):
        for fact in self.facts:
            self.facts[fact]["value"] = False
            self.facts[fact]["visited"] = False
        for char in facts:
            if (ord(char) < 65 or ord(char) > 90):
                raise Exception(char + " is invalid.")
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
                raise Exception(char + " is invalid.")
        self.queriedFacts = fromStringToList(newQueries)

# --------------------------------
# Class used as a stack to store the current goal we are trying to evaluate
# --------------------------------
class Stack:
    def __init__(self):
        self.stack = deque()

    def push(self, value):
        self.stack.append(value)

    def top(self):
        if len(self.stack) > 0:
            return self.stack[len(self.stack) - 1]
        raise Exception('Stack is empty')

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        raise Exception('Stack is empty')

    def display(self):
        if len(self.stack) > 0:
            for goal in self.stack:
                print(goal)
        else:
            print('Stack is empty')

def isOperator(c):
    if (c is '+' or c is '-' or c is '|' or c is '^'):
        return 1

def fromStringToList(string):
    l = []
    for char in string:
        l.append(char)
    return l
            
# --------------------------------
# Removing whitespaces
# --------------------------------
def removeWs(line):
    line = line.strip()
    line = line.rstrip()
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace('\n', "")
    return line

# --------------------------------
# Function called to set the facts
# We loop through each fact, check if it is in the range [A:Z], and set it to True if it is
# --------------------------------
def setFacts(fact, initFacts):
    for f in initFacts:
        if (ord(f) < 65 or ord(f) > 90):
            raise Exception(f +  " is invalid.")
        fact.facts[f]["value"] = True
        fact.line += f
    return fact

def setQuery(query, line):   
    for char in line:
        if (ord(char) < 65 or ord(char) > 90):
            raise Exception(char + " is invalid.")
        query.queriedFacts.append(char)
    return query

# --------------------------------
# Function called to parse the list of lines
# --------------------------------

def parseLines(lineList):
    i = 0
    while (i < len(lineList)):
        lineList[i] = removeWs(lineList[i].rstrip())
        if ('#' in lineList[i]):
            lineList[i] = lineList[i][:lineList[i].find('#')]
        if (lineList[i] == "\n"):
            del lineList[i]
        i += 1
    i = 0
    while i < len(lineList):
        if "<=>" in lineList[i]:
            new = lineList[i].split("<=>")
            new.reverse()
            lineList[i] = new[0] + "=>" + new[1]
        i += 1
    return lineList

def verifLine(line):
    if "=>" not in line:
        raise Exception(line + " is invalid.")
        return False
    i = 0
    while (i < len(line)):
        if i + 1 < len(line) and isOperator(line[i]) and isOperator(line[i + 1]):
            raise Exception(line + " is invalid.")
            return False
        i += 1
            
    return True
        

# --------------------------------
# Handles the parsing of the file
# --------------------------------

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
        elif line[0] == '=' and len(line) >= 1:
            fact = setFacts(fact, line[1:])
        elif line[0] == '?' and len(line) >= 1:
            query = setQuery(query, line[1:])
        else:
            if verifLine(line) is True:
                r.lines.append(removeWs(line))
    return r, fact, query;