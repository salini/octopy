
import common  # to load path to octopy package

import unittest

import octopy.OctreeReader
from octopy.Node import CoordNode
from octopy.visu.core import getViewer
from octopy.visu.OSGOctree import createOSGOctree

class OSGVisualization():
    def __init__(self, show=False):
        self.show = show

    def showTestFile(self, show=False):
        filename = common.getFromTestDir("../resources/test.bt")
        #filename = common.getFromTestDir("../resources/out.bt")
        header, octree = octopy.OctreeReader.OctreeRead(filename, CoordNode)
        octree.setNodeSizeRecursively()
        octree.setCoordinateRecursively()

        root = createOSGOctree(octree)

        viewer = getViewer()
        viewer.setSceneData(root.__disown__())
        if self.show:
            viewer.run()
        viewer.setSceneData(None)



class TestOSGVisualization(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._visu = OSGVisualization()

    def test_showTestFile(self):
        self._visu.showTestFile()



if __name__ == "__main__":

    c = OSGVisualization(True)
    c.showTestFile()
