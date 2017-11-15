
import common  # to load path to octopy package

import unittest

import time

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getOccupiedListTree
from octopy.visu.core import getViewer
from octopy.visu.OSGOctree import createOSGTree_flatRawCubes


interactive = False


class TestOSGVisualization(unittest.TestCase):

    def test_showTestFile(self):
        #for n in ["simple", "test"]:
        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
            t = time.time()
            octree = OctreeParser().readFile(inFileName)
            tread = time.time() - t

            t = time.time()
            occupied = getOccupiedListTree(octree.root)
            root = createOSGTree_flatRawCubes(occupied, octree.getResolutionTable()[0])
            tconv = time.time() - t

            print "=========>>>", inFileName
            print "READ (s):", tread
            print "CONVERT IN CUBES (s):", tconv
            viewer = getViewer()
            viewer.setSceneData(root.__disown__())
            if interactive:
                viewer.run()
            viewer.setSceneData(None)



if __name__ == "__main__":
    interactive = True
    unittest.main(verbosity=2)
