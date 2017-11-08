import common  # to load path to octopy package

import unittest

from octopy.Node import CoordNode
from octopy.visu import show

import octopy.OctreeReader
import octopy.OctreeWriter

class TestOSGVisualization(unittest.TestCase):


    def test_Conversion(self):
        filenameIn = common.getFromTestDir("../resources/test.bt")
        header, octree = octopy.OctreeReader.OctreeRead(filenameIn)
        print header

        filenameOut = common.getFromTestDir("../resources/test_rewrite.bt")
        octopy.OctreeWriter.OctreeWrite(filenameOut, octree, header["res"])


if __name__ == "__main__":

    print "load"
    filenameIn = common.getFromTestDir("../resources/test.bt")
    header, octree = octopy.OctreeReader.OctreeRead(filenameIn)
    print header
    print "end loading"
    print "rewrite"
    filenameOut = common.getFromTestDir("../resources/test_rewrite.bt")
    octopy.OctreeWriter.OctreeWrite(filenameOut, octree, header["res"])
    print "end"

    print"reload to visu"
    header, octree2 = octopy.OctreeReader.OctreeRead(filenameOut, CoordNode)
    octree2.setNodeSizeRecursively()
    octree2.setCoordinateRecursively()

    show(octree2)
    print "end"


