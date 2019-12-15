import re
import sys

import Parser as parser

# rules is the list of rules: I need to convert them to NPI notation
# facts is an array of 26 elements set to True or False, it is our knowledge base
# queries are the facts elements we are asked to determine
# goals is a stack of elements, the element on top of the stack is the one we
#       are currently trying to determine, and we use it for the recursion

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ>"
globalFile = open("Logs", "w+")

black = lambda text: '\033[0;1;30m' + text + '\033[0m\x1b[1m'
red = lambda text: '\033[0;31m' + text + '\033[0m\x1b[1m'
green = lambda text: '\033[0;1;32m' + text + '\033[0m\x1b[1m'
yellow = lambda text: '\033[0;1;33m' + text + '\033[0m\x1b[1m'
cyan = lambda text: '\033[0;1;34m' + text + '\033[0m\x1b[1m'
magenta = lambda text: '\033[0;1;35m' + text + '\033[0m\x1b[1m'
blue = lambda text: '\033[0;1;36m' + text + '\033[0m\x1b[1m'
white = lambda text: '\033[0;1;37m' + text + '\033[0m\x1b[1m'

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

    def start(self):
        if (len(sys.argv) != 2):
            print("usage: python3 ExpertSystem.py <KnowledgeBaseFile>")
            exit(0)
        self.rules, self.facts, self.queries = parser.fileParsing(sys.argv[1])
        self.toRPN()

    # ---------------------------------------------------------------------------------------------------
    # Adding an extra character to avoid underflow
    # Looping through all the rules
    # Looping through each character of the string
    # If the character is in the list of accepted char then I just add it to the new string
    # If the char is an opening parenthesis then I push it to the stack
    # If the char is a closing parenthesis then I pop everything from the stack to add them in the new string
    # until I find the opening parenthesis
    # If we reached the end of the LHS, then we pop everything out of the stack and add it to the string
    # If it is an operator, then I compare their importance, and based on that either I add them in the new string, or I push them in the stack
    # Then I pop all the values from the stack to empty it, and I add everything in the new string
    # Finally I append the newly created string to the new list of rules, and I keep looping in the old rules
    # And I create the new rules class, and add the new rules to our variables
    # ---------------------------------------------------------------------------------------------------

    def toRPN(self):
        stack = parser.Stack()
        stack.push('#')
        newRules = []
        for rule in self.rules.lines:
            str = ""
            for char in rule:
                if char in alphabet:
                    str += char
                elif char is '(':
                    stack.push(char)
                elif char is ')':
                    while (stack.top() is not '#' and stack.top() is not '('):
                        str += stack.top()
                        stack.pop()
                    stack.pop()
                elif char is '=' or char is '<':
                    while (stack.top() is not '#'):
                        str += stack.top()
                        stack.pop()
                    str += char
                else:
                    if (getWeight(char) > getWeight(stack.top())):
                        stack.push(char)
                    else:
                        while (stack.top() is not '#' and getWeight(char) <= getWeight(stack.top())):
                            str += stack.top()
                            stack.pop()
                        stack.push(char)
            while (stack.top() is not '#'):
                str += stack.top()
                stack.pop()
            newRules.append(str)
        newClass = parser.Rules()
        newClass.lines = newRules
        del self.rules
        self.rules = newClass

    # Method returning the indexes of the rules containing our goal in the RHS
    def findGoalInRules(self, char):
        i = -1
        found = []
        otherGoal = [char]
        for line in self.rules.lines:
            i += 1
            rhs = line[line.find('>') + 1:]
            # print(rhs)
            if char in rhs:
                found.append(i)
            if '+' in rhs:
                for x in rhs:
                    if (ord(x) >= 65 and ord(x) <= 90) and (x is not char):
                        otherGoal.append(x)
        return found, otherGoal
    # ---------------------------------------------------------------------
    # Main recursion
    # print("Looking for " + goal)
    # If we already know the value for sure then we return True
    # Search for goal implied in the rules
    # Getting the LHS
    # Creating a stack to evaluate the LFS
    # print("Results" + str(results))
    # Looping through each character of the expression and evaluating it
    # ---------------------------------------------------------------------

    def recurse(self, goal):
        if (self.facts.facts[goal]["visited"] is True):
            globalFile.write(goal + " has already been visited so we know its value is " + blue(str(self.facts.facts[goal]["value"])) + "\n")
            return self.facts.facts[goal]["value"]
        globalFile.write("Trying to determine " + red(goal) + "\n")
        res = self.facts.facts[goal]["value"]
        results = []
        indexes, goals = self.findGoalInRules(goal)
        globalFile.write("We found " + str(len(indexes)) + " rule(s) implying " + red(goal) + "\n")
        if len(indexes) > 0:
            for index in indexes:
                rule = self.rules.lines[index][:self.rules.lines[index].find('=')]
                globalFile.write("\nWe need to evaluate " + green(rule) + "\n")
                stack = parser.Stack()
                for char in rule:
                    if (char.isalnum()):
                        stack.push(char)
                    elif char is '!':
                        if type(stack.top()) is not bool:
                            globalFile.write("We need to recurse to find " + red(stack.top()) + "\n\n")
                            op1 = self.recurse(stack.top())
                        else:
                            op1 = stack.top()
                        stack.pop()
                        if op1 == False:
                            stack.push(True)
                        elif op1 == True:
                            stack.push(False)
                    else:
                        if type(stack.top()) is not bool:
                            globalFile.write("We need to recurse to find " + red(stack.top()) + "\n\n")
                            op1 = self.recurse(stack.top())
                        else:
                            op1 = stack.top()
                        stack.pop()
                        if type(stack.top()) is not bool:
                            globalFile.write("We need to recurse to find " + red(stack.top()) + "\n\n")
                            op2 = self.recurse(stack.top())
                        else:
                            op2 = stack.top()
                        stack.pop()
                        if (char is '+'):
                            stack.push(op1 & op2)
                        elif (char is '|'):
                            stack.push(op1 | op2)
                        elif (char is '^'):
                            stack.push(op1 ^ op2)
                if type(stack.top()) is not bool:
                    res = self.recurse(stack.top())
                else:
                    res = stack.top()
                stack.pop()
                results.append(res)
        t = 0
        f = 0
        n = 0
        for result in results:
            if result is True:
                t += 1
            elif result is False:
                f += 1
            else:
                n += 1
        self.facts.facts[goal]["visited"] = True
        for g in goals:
            if ((t > 0 and f > 0) or (f > 0 and t > 0) or (n > 0)):
                globalFile.write("We have an undetermined value so we ask the user if he wants to set it up manually\n")
                line = input("The value of " + red(g) + " will be undetermined because the rules imply different results(" + red(str(t)) + blue(" True") + ", " + red(str(f)) + blue(" False") + " and " + red(str(n)) + blue(" Undetermined") + "). Do you want to set it up manually ? y/n")
                if line == "y":
                    while (True):
                        line = input("Value (T/F): ")
                        if (line == "T"):
                            globalFile.write("The user sets it to " + blue("True")+ "\n")
                            self.facts.facts[g]["value"] = True
                            break
                        elif line == "F":
                            globalFile.write("The user sets it to " + blue("False")+ "\n")
                            self.facts.facts[g]["value"] = False
                            break
                else:
                    globalFile.write("The user lets it be " + blue("Undetermined")+ "\n")
                    self.facts.facts[g]["value"] = None
            elif t > 0 and f == 0:
                self.facts.facts[g]["value"] = True
            elif t == 0 and f == 0:
                pass
            else:
                self.facts.facts[g]["value"] = False
        if len(indexes) == 0:
            globalFile.write("We know from the given facts that " + red(goal) + " is " + blue(str(self.facts.facts[goal]["value"])) + "\n")
        else:
            globalFile.write("We determined that " + red(goal) + " is " + blue(str(self.facts.facts[goal]["value"])) + "\n")
        globalFile.write("Returning " + red(goal) + " is " + blue(str(self.facts.facts[goal]["value"])) + "\n\n")
        return self.facts.facts[goal]["value"]

    # Printing the rules
    def evaluate(self):
        globalFile.write("\x1b[1m================================================================================================\n")
        globalFile.write("Starting a new program:")
        globalFile.write("\n================================================================================================\n")
        print(green("================================================================================================\n"))
        print(green("Result of queried fact(s):"))
        print(green("\n================================================================================================\n"))
        print(yellow("\x1b[4mRules:"))
        self.rules.display()
        print("\nWe are looking for " + str(self.queries.queriedFacts), end="\n\n")
        for query in self.queries.queriedFacts:
            v = self.recurse(query)
            if v is True:
                print(red(query) + " is " + blue("true"))
            elif v is None:
                print(red(query) + " is " + blue("undertermined"))
            else:
                print(red(query) + " is " + blue("false"))
        print()
        globalFile.write("\n================================================================================================\n")
        globalFile.write("End of the program:")
        globalFile.write("\n================================================================================================\n")

    # ----------------------------------------------------------------------------------
    # Function called at the end of the evaluation to allow the user to ask for new queries
    # Printing the previous facts
    # Getting the new facts and resetting them
    # Printing the previous query
    # Getting the new query and resetting them
    # Starting the main recursion again, with the new values
    # ----------------------------------------------------------------------------------

    def reloop(self):
        while (True):
            print("Try again? yes/no")
            line = input()

            if line == "yes":
                print("\nPrevious Facts:\n=", end="")
                print(self.facts.line, end="")
                
                line = input("\nNew facts:\n=")
                self.facts.reset(line)

                print("\nPrevious Query:\n?", end="")
                self.queries.display()

                line = input("\nNew Query:\n?")
                self.queries.reset(line)
                print()

                self.evaluate()

            elif line == "no":
                print(red("\n================================================================================================\n"))
                print(red("End of the program: You can check the historic of everything that was queried in the Logs file."))
                print(red("\n================================================================================================\n"))
                break

            else:
                print("We can't recognize the input\n")
