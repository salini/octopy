

import common  # to load path to octopy package

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getValueTree

import time


def compute_coordTree():
    for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
        inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
        t = time.time()
        octree = OctreeParser().readFile(inFileName)
        tread = time.time() - t
        t = time.time()
        getValueTree(octree.root, True)
        tcoordbit = time.time() - t

        print "=========>>>", inFileName
        print "READ:", tread
        print "COORD BIT:", tcoordbit

if __name__ == "__main__":
    compute_coordTree()

