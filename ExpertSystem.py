import re
import sys

import Parser as parser
import InferenceEngine as ie

# rules is the list of rules: I need to convert them to NPI notation
# facts is an array of 26 elements set to True or False, it is our knowledge base
# queries are the facts elements we are asked to determine
# goals is a stack of elements, the element on top of the stack is the one we
#       are currently trying to determine, and we use it for the recursion

class ExpertSystem:
    def __init__(self):
        self.rules = parser.Rules()
        self.facts = parser.Facts()
        self.queries = parser.Query()
        self.goals = parser.Stack()

    def start(self):
        if (len(sys.argv) != 2):
            print("usage: python3 ExpertSystem.py <KnowledgeBaseFile>")
            exit(0)
        self.rules, self.facts, self.queries, self.goals = parser.fileParsing(sys.argv[1])
    
    def toRPN(self):
        stack = parser.Stack()
        newRules = []

        for rule in self.rules.lines:
            for char in rule:
                if (char.isalnum()):
                    print("IS ALNUM")