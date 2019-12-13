import re
import sys

import Parser as parser
import InferenceEngine as ie

# rules is the list of rules: I need to convert them to NPI notation
# facts is an array of 26 elements set to True or False, it is our knowledge base
# queries are the facts elements we are asked to determine
# goals is a stack of elements, the element on top of the stack is the one we
#       are currently trying to determine, and we use it for the recursion

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ>"

def getWeight(char):
    if char is '!':
        return 5
    elif char is '+':
        return 4
    elif char is '|':
        return 3
    elif char is '^':
        return 2
    else:
        return 1


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
        for query in self.queries.queriedFacts:
            self.goals.push(query)

    def toRPN(self):
        stack = parser.Stack()

        # Adding an extra character to avoid underflow
        stack.push('#')
        newRules = []

        # Looping through all the rules
        for rule in self.rules.lines:
            str = ""

            # Looping through each character of the string
            for char in rule:

                # If the character is in the list of accepted char then I just add it to the new string
                if char in alphabet:
                    str += char

                # If the char is an opening parenthesis then I push it to the stack
                elif char is '(':
                    stack.push(char)

                # If the char is a closing parenthesis then I pop everything from the stack to add them in the new string
                # until I find the opening parenthesis
                elif char is ')':
                    while (stack.top() is not '#' and stack.top() is not '('):
                        str += stack.top()
                        stack.pop()
                    # Removing the '('
                    stack.pop()

                # If we reached the end of the LHS, then we pop everything out of the stack and add it to the string
                elif char is '=' or char is '<':
                    while (stack.top() is not '#'):
                        str += stack.top()
                        stack.pop()
                    str += char

                # If it is an operator, then I compare their importance, and based on that either I add them in the new string, or I push them in the stack
                else:
                    if (getWeight(char) > getWeight(stack.top())):
                        stack.push(char)
                    else:
                        while (stack.top() is not '#' and getWeight(char) <= getWeight(stack.top())):
                            str += stack.top()
                            stack.pop()
                        stack.push(char)

            # Then I pop all the values from the stack to empty it, and I add everything in the new string
            while (stack.top() is not '#'):
                str += stack.top()
                stack.pop()

            # Finally I append the newly created string to the new list of rules, and I keep looping in the old rules
            newRules.append(str)

        # And I create the new rules class, and add the new rules to our variables
        newClass = parser.Rules()
        newClass.lines = newRules
        del self.rules
        self.rules = newClass

        # Checking if it worked
        self.rules.display()

    # Method returning the index of the rule containing our goal in the RHS
    def findGoalInRules(self, char):
        i = -1
        for line in self.rules.lines:
            i += 1
            rhs = line[line.find('>') + 1:]
            if char in rhs:
                return i
        return -1

    # Main recursion
    def evaluate(self, goal):
        # If we already know the value for sure then we return True
        if (self.facts.facts[goal]["visited"] is True):
            return self.facts.facts[goal].value
        # Search for goal implied in the rules
        res = self.facts.facts[goal]["value"]
        index = self.findGoalInRules(goal)
        if index >= 0:
            # Getting the LHS
            rule = self.rules.lines[index][:self.rules.lines[index].find('=')]
            # Creating a stack to evaluate the LFS
            stack = parser.Stack()
            # Looping through each character of the expression and evaluating it
            for char in rule:
                if (char.isalnum()):
                    stack.push(char)
                else:
                    op1 = self.evaluate(stack.top())
                    stack.pop()
                    op2 = self.evaluate(stack.top())
                    stack.pop()
                    if (char is '+'):
                        stack.push(op1 & op2)
                    elif (char is '|'):
                        stack.push(op1 | op2)
            res = stack.top()
            stack.pop()
        self.facts.facts[goal]["value"] = res
        self.facts.facts[goal]["visited"] = True
        return res

    def recurse(self):
        if self.evaluate(self.queries.queriedFacts[0]):
            print("True")
        else:
            print("False")


































 # # Function evaluating the given rule, checking if we can get
    # # the value of the RHS based on the LHS, and adding new goals if necessary
    # def evaluateRule(self, i):
    #     # Getting the LHS
    #     rule = self.rules.lines[i][:self.rules.lines[i].find('=')]
    #     # Creating a stack to evaluate the LFS
    #     stack = parser.Stack()
    #     # Looping through each character of the expression and evaluating it
    #     for char in rule:
    #         if (char.isalnum()):
    #             stack.push(char)
    #         else:
    #             op1 = self.facts.facts[ord(stack.top()) - 65]
    #             stack.pop()
    #             op2 = self.facts.facts[ord(stack.top()) - 65]
    #             stack.pop()
    #             if (char is '&')
    #                 stack.push(op1 & op2)
    #             elif (char is '|')
    #                 stack.push(op1 | op2)
    #     res = stack.top()
    #     stack.pop()
    #     return res, 