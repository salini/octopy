
import common  # to load path to octopy package

import unittest

import time

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getFreeTree, getOccupiedTree, getUnknownTree, nodesToCubes


class TestNodeExploration(unittest.TestCase):

    def test_Depth(self):
        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
            octree = OctreeParser().readFile(inFileName)
            t = time.time()
            depth = octree.getDepth(octree.root)
            tdepth = time.time() - t
            print "=========>>>", inFileName
            print "time depth (s):", tdepth
            print "depth:", depth


    def test_createCoordinates(self):
        inFileName = common.getFromTestDir("../resources/simple.bt")
        octree = OctreeParser().readFile(inFileName)
        print "=========>>>", inFileName
        print "OCTREE rep:", octree.root

        print "FREE rep:", getFreeTree(octree.root)
        print "OCCUPIED rep:", getOccupiedTree(octree.root)
        print "UNKNOWN rep:", getUnknownTree(octree.root)
        print "OCCUPIED[1] rep:", getOccupiedTree(octree.root[1])

        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
            t = time.time()
            octree = OctreeParser().readFile(inFileName)
            tread = time.time() - t
            t = time.time()
            free = getFreeTree(octree.root)
            tfree = time.time() - t
            t = time.time()
            occupied = getOccupiedTree(octree.root)
            tocc = time.time() - t
            t = time.time()
            unknown = getUnknownTree(octree.root)
            tunknown = time.time() - t

            print "=========>>>", inFileName
            print "READ (s):", tread
            print "T free (s):", tfree,
            print "T occupied (s):",tocc
            print "T unknown (s):", tunknown
            print "nb node octree:", octree.size
            print "nb node free:", len(free)
            print "nb node occupied:",len(occupied)
            print "nb node unknown:", len(unknown)



if __name__ == "__main__":
    unittest.main(verbosity=2)
