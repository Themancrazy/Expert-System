import ExpertSystem as s

system = s.ExpertSystem()

system.start()
system.toRPN()

# system.facts.display()

system.evaluate()

# system.evaluate(system.goals.top())

# system.facts.display()
# system.queries.queriedFacts[0]

# system.evaluateRule(system.findGoalInRules())

# Need to store all the goals, then start looping, look in facts, if true return true, else look for it in rules, set new goals, recurse