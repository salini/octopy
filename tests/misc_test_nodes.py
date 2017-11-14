

import common  # to load path to octopy package

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getListTree, getOcnodeTree

import time


def compute_coordTree():
    for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
        inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
        t = time.time()
        octree = OctreeParser().readFile(inFileName)
        tread = time.time() - t
        t = time.time()
        getListTree(octree.root, True)
        tlist = time.time() - t
        t = time.time()
        getOcnodeTree(octree.root, True)
        tocnode = time.time() - t

        print "=========>>>", inFileName
        print "READ:", tread
        print "COORD LIST:", tlist
        print "COORD OCNODE:", tocnode

if __name__ == "__main__":
    compute_coordTree()

