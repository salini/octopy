
from core import getBox

from osgswig import osg

import numpy as np




def createOSGCubes(cubes):
    print "start creating OSG cubes"
    root = osg.Group()
    for c in cubes:
        pos = (c[0], c[1], c[2])
        dim = (c[3], c[3], c[3])
        root.addChild(getBox(pos, dim))
    print "done"

    return root

