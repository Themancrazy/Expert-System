import re
import sys

import Parser as parser
import InferenceEngine as ie

def ExpertSystem():
    if (len(sys.argv) != 2):
        print("usage: python3 ExpertSystem.py <KnowledgeBaseFile>")
        exit(0)
    parser.fileParsing(sys.argv[1])

ExpertSystem()