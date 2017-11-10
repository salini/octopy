
import common  # to load path to octopy package

import unittest

import time

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getFree, getOccupied, getUnknown, convertNodesToCubes


class TestNodeExploration(unittest.TestCase):

    def test_Depth(self):
        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
            octree = OctreeParser().readFile(inFileName)
            t = time.time()
            depth = octree.getDepth(octree.root)
            tdepth = time.time() - t
            print "DEPTH:", inFileName, tdepth, depth


    def test_createCoordinates(self):
        inFileName = common.getFromTestDir("../resources/simple.bt")
        octree = OctreeParser().readFile(inFileName)
        print "OCTREE:", octree.root

        print "FREE:", getFree(octree.root)
        print "OCCUPIED:", getOccupied(octree.root)
        print "UNKNOWN:", getUnknown(octree.root)
        print "OCCUPIED[1]:", getOccupied(octree.root[1])

        print "CUBES:", convertNodesToCubes(getOccupied(octree.root), octree.getResolutionTable())


        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
            t = time.time()
            octree = OctreeParser().readFile(inFileName)
            tread = time.time() - t
            t = time.time()
            free = getFree(octree.root)
            tfree = time.time() - t
            t = time.time()
            occupied = getOccupied(octree.root)
            tocc = time.time() - t
            t = time.time()
            unknown = getUnknown(octree.root)
            tunknown = time.time() - t
            print "READ:", inFileName, tread
            print "T free/occupied/unknown:", tfree, tocc, tunknown
            print "nb node/free/occupied/unknown", octree.size, len(free), len(occupied), len(unknown)



if __name__ == "__main__":
    unittest.main(verbosity=2)
