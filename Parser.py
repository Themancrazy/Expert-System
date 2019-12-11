# Append list of elements in self.lines and check that everything is stored correctly 
# (use REGEX from COMPv1)

import re

class Rules:
    def __init__(self):
        self.lines = []

class Facts:
    def __init__(self):
        self.facts = []

class Query:
    def __init__(self):
        self.queriedFactNum = []

def removeWs(line):
    line = line.strip()
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    # print(line)
    return line

def setFacts(fact, initFacts):
    i = 0
    while (i < len(initFacts)):
        if (ord(initFacts[i]) < 65 or ord(initFacts[i]) > 90):
            raise Exception(initFacts[i], " is invalid.")
        fact.facts[ord(initFacts[i]) - 65] = True
        i += 1
    return fact      

def setQuery(query, queriedFact):
    i = 0
    while (i < len(queriedFact)):
        if (ord(queriedFact[i]) < 65 or ord(queriedFact[i]) > 90):
            raise Exception(queriedFact[i], " is invalid.")
        query.queriedFactNum.append(ord(queriedFact[i]) - 65)
        i += 1
    return query      

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
    r = Rules()
    fact = Facts()
    query = Query()
    i = 0
    while (i < 26):
        fact.facts.append(False)
        i += 1
    with open(filename) as f:
        lineList = f.readlines()
    lineList = parseLines(lineList)
    i = 0
    # while (i < len(lineList)):
    #     r.lines.append(re.split("[ |\t]+", lineList[i].strip()))
    #     if (r.lines[i][0][0] == '='):
    #         fact = setFacts(fact, r.lines[i][0][1:])
    #     elif (r.lines[i][0][0] == '?'):
    #         query = setQuery(query, r.lines[i][0][1:])
    #     i += 1
    while (i < len(lineList)):
        r.lines.append(removeWs(lineList[i]))
        if (r.lines[i][0] == '='):
            fact = setFacts(fact, r.lines[i][1:])
        elif (r.lines[i][0] == '?'):
            query = setQuery(query, r.lines[i][1:])
        i += 1
    return r, fact, query;
    