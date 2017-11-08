


class TNode(object):
    def __init__(self):
        self._valid = None
        self.children = [None]*8

    def setValid(self, v):
        self._valid = v

    def getValid(self):
        return self._valid

    def createNode(self):
        return TNode()

    def createNodeChild(self, idx):
        nc = self.createNode()
        self.children[idx] = nc
        return nc

    def getNodeChild(self, idx):
        return self.children[idx]

    def nodeChildExists(self, idx):
        return True if self.children[idx] is not None else False

    def isLeaf(self):
        for c in self.children:
            if c is not None:
                return False
        return True

    def isOccupied(self):
        if self._valid == False:
            return False
        else:
            return True

    def getAllNodes(self):
        nodes = [self]
        for c in self.children:
            if c is not None:
                nodes.extend(c.getAllNodes())
        return nodes

    def getNumberOfNodes(self):
        val = 1
        val += sum([c.getNumberOfNodes() for c in self.children if c is not None])
        return val



import numpy as np

COORDUNIT = []
for z_ in [-1.0, 1.0]:
    for y_ in [-1.0, 1.0]:
        for x_ in [-1.0, 1.0]:
            COORDUNIT.append([x_,y_,z_])
COORDUNIT = np.array(COORDUNIT)

#print COORDUNIT


class CoordNode(TNode):
    def __init__(self):
        TNode.__init__(self)
        self.nodeSize = 0.0
        self.coordinate = np.zeros(3)

    def createNode(self):
        return CoordNode()

    def setNodeSize(self, size):
        self.nodeSize = size

    def setNodeSizeRecursively(self, size=1.0):
        self.setNodeSize(size)
        csize = size*0.5
        for c in self.children:
            if c is not None:
                c.setNodeSizeRecursively(csize)

    def getNodeSize(self):
        return self.nodeSize

    def setCoordinate(self, coordinate):
        self.coordinate = coordinate

    def setCoordinateRecursively(self, coordinate=None):
        if coordinate is None:
            coordinate = np.zeros(3)

        self.setCoordinate(coordinate)
        l = self.nodeSize * 0.25
        COORD = coordinate + (COORDUNIT*l)

        for i , c in enumerate(self.children):
            if c is not None:
                c.setCoordinateRecursively(COORD[i])

    def getCoordinate(self):
        return self.coordinate




