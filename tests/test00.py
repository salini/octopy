
import common  # to load path to octopy package

import unittest

import octopy.OctreeReader

class TestCaseCreation(unittest.TestCase):

    def test_readFile(self):
        filename = common.getFromTestDir("../resources/test.bt")
        header, octree = octopy.OctreeReader.OctreeRead(filename)
        print header


if __name__ == "__main__":
    print "end of test00 script"

