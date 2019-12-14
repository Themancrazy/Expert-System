import ExpertSystem as s
system = s.ExpertSystem()

try:
    system.start()
    system.evaluate()
    system.reloop()
except Exception as e:
    print("\x1b[91mError: ", str(e), "\x1b[0m")