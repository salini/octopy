
import common  # to load path to octopy package

import unittest

import time

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getFree, getOccupied, getUnknown, nodesToCubes
from octopy.visu.core import getViewer
from octopy.visu.OSGOctree import createOSGCubes


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
            occupied = getOccupied(octree.root)
            cubes = nodesToCubes(occupied, octree.getResolutionTable())
            root = createOSGCubes(cubes)
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
