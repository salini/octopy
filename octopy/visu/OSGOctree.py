
from core import getBox

from osgswig import osg

import numpy as np

def createOSGOctree(octree):
    print "start creating OSG octree"
    root = osg.Group()
    nodes = octree.getAllNodes()
    for n in nodes:
            if n.isLeaf():
                if n.isOccupied():
                    pos = n.getCoordinate()
                    dim = np.ones(3)* n.getNodeSize()
                    root.addChild(getBox(pos, dim))
    print "done"

    return root