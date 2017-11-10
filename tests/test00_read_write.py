
import common  # to load path to octopy package

import os
import time
import filecmp

import unittest

from octopy.OctreeParser import OctreeParser

class TestReadWriteFiles(unittest.TestCase):

    def test_readWriteFiles(self):
        try:
            print "create results folder"
            print common.getFromTestDir("./results")
            os.mkdir(common.getFromTestDir("./results"))
        except:
            print "WARNING: cannot create 'results' folder"

        for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
            inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
            outFileName = common.getFromTestDir("./results/_rewrite_{0}.bt".format(n))
            t = time.time()
            octree = OctreeParser().readFile(inFileName)
            tread = time.time() - t
            t = time.time()
            OctreeParser().writeFile(outFileName, octree)
            twrite = time.time() - t
            areSame = filecmp.cmp(inFileName, outFileName)
            print "READ:", inFileName, tread
            print "size from file:", octree.size
            print "size of octree:", octree.getSize()
            print "WRITE:", outFileName, twrite
            print "SAME?:", areSame

            self.assertTrue(areSame)



if __name__ == "__main__":
    unittest.main(verbosity=2)

