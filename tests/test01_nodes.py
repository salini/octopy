
import common  # to load path to octopy package

import unittest

import time

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getFreeListTree, getOccupiedListTree, getUnknownListTree
from octopy.Ocnode import getFreeOcnodeTree, getOccupiedOcnodeTree, getUnknownOcnodeTree

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

        print "FREE rep:", getFreeListTree(octree.root)
        print "OCCUPIED rep:", getOccupiedListTree(octree.root)
        print "UNKNOWN rep:", getUnknownListTree(octree.root)
        print "OCCUPIED[1] rep:", getOccupiedListTree(octree.root[1])

        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))

            t = time.time()
            octree = OctreeParser().readFile(inFileName)
            tread = time.time() - t
            t = time.time()
            free = getFreeListTree(octree.root)
            tfree = time.time() - t
            t = time.time()
            occupied = getOccupiedListTree(octree.root)
            tocc = time.time() - t
            t = time.time()
            unknown = getUnknownListTree(octree.root)
            tunknown = time.time() - t

            t = time.time()
            free = getFreeOcnodeTree(octree.root)
            tocnodefree = time.time() - t
            t = time.time()
            occupied = getOccupiedOcnodeTree(octree.root)
            tocnodeocc = time.time() - t
            t = time.time()
            unknown = getUnknownOcnodeTree(octree.root)
            tocnodeunknown = time.time() - t

            print "=========>>>", inFileName
            print "READ (s):", tread
            print "nb node octree:", octree.size
            print "T list free (s):", tfree
            print "T list occupied (s):",tocc
            print "T list unknown (s):", tunknown
            print "T ocnode free (s):", tocnodefree
            print "T ocnode occupied (s):",tocnodeocc
            print "T ocnode unknown (s):", tocnodeunknown



if __name__ == "__main__":
    unittest.main(verbosity=2)
