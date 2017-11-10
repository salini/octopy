
import os
import sys

cpath = os.path.realpath(os.path.dirname(__file__))
sys.path.append(cpath+"/..")

import octopy

def getFromTestDir(path=""):
    return os.path.join(cpath, path)

