

import common  # to load path to octopy package

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getCoordTree_list, getCoordTree_string, getCoordTree_bit

import time


def compute_coordTree():
    for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
        inFileName = common.getFromTestDir("../resources/{0}.bt".format(n))
        t = time.time()
        octree = OctreeParser().readFile(inFileName)
        tread = time.time() - t
        t = time.time()
        getCoordTree_list(octree.root, True)
        tcoordlist = time.time() - t
        t = time.time()
        getCoordTree_string(octree.root, True)
        tcoordstring = time.time() - t
        t = time.time()
        getCoordTree_bit(octree.root, True)
        tcoordbit = time.time() - t

        print "=========>>>", inFileName
        print "READ:", tread
        print "COORD LIST:", tcoordlist
        print "COORD STRING:", tcoordstring
        print "COORD BIT:", tcoordbit

if __name__ == "__main__":
    compute_coordTree()


""" RESULTS (win10)
=========>>> D:\joe\dev\octopy\tests\../resources/simple.bt
READ: 0.0
COORD LIST: 0.0
COORD STRING: 0.0
COORD BIT: 0.0
=========>>> D:\joe\dev\octopy\tests\../resources/test.bt
READ: 0.388000011444
COORD LIST: 1.43099999428
COORD STRING: 0.523999929428
COORD BIT: 0.28200006485
=========>>> D:\joe\dev\octopy\tests\../resources/fr_078_tidyup.bt
READ: 1.97499990463
COORD LIST: 5.55599999428
COORD STRING: 2.09000015259
COORD BIT: 1.33599996567
=========>>> D:\joe\dev\octopy\tests\../resources/freiburg1_360.bt
READ: 2.74699997902
COORD LIST: 8.47500014305
COORD STRING: 3.33499979973
COORD BIT: 1.80300021172
"""
