import re
import sys

import Parser as parser
import InferenceEngine as ie

def ExpertSystem():
    if (len(sys.argv) != 2):
        print("usage: python3 ExpertSystem.py <KnowledgeBaseFile>")
        exit(0)
    r, fact, query = parser.fileParsing(sys.argv[1])
    print(r.lines[1])
    print(fact.facts)
    print(query.queriedFactNum[0])

ExpertSystem()