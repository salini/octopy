

import numpy as np


class Ocnode(object):
    def __init__(self, parent=None, coordinate=0, isLeaf=False, value=False):
        self.parent = parent
        self.coordinate = coordinate
        self.isLeaf = isLeaf
        self.value = value
        self.children = []



def getOcnodeTree(node, value, parent=None, coordinate=None):
    """ recursive operation to extract tree with 'coordinates' with corresponding value, as Octonode.

    coordinates are integers that coorespond to position of the node based on parent location.
    if one node is the fifth child of a parent, its coordinate is 4 ==> 0b100
    this coordinate goes from 0 to 7.
    If we consider a frame with axes X, Y, Z, (front, left, up) then:
    coordinate | location | meaning
    -----------------------------------------
    0 : 000    | -X,-Y,-Z | back , right, down
    1 : 001    |  X,-Y,-Z | front, right, down
    2 : 010    | -X, Y,-Z | back , left , down
    3 : 011    |  X, Y,-Z | front, left , down
    4 : 100    | -X,-Y, Z | back , right, up
    5 : 101    |  X,-Y, Z | front, right, up
    6 : 110    | -X, Y, Z | back , left , up
    7 : 111    |  X, Y, Z | front, left , up

    TODO: the value should be replaced by a comparison function...
    """
    ocnode = Ocnode(parent, coordinate)

    for i in range(8):
        if node[i] is not None:
            if node[i] == value:
                cnode = Ocnode(ocnode, i, True, value)
                ocnode.children.append(cnode)
            elif isinstance(node[i], list):
                cnode = getOcnodeTree(node[i], value, ocnode, i)
                ocnode.children.append(cnode)

    return ocnode

def getFreeOcnodeTree(node):
    return getOcnodeTree(node, False)

def getOccupiedOcnodeTree(node):
    return getOcnodeTree(node, True)

def getUnknownOcnodeTree(node):
    return getOcnodeTree(node, None)




def getListTree(node, value):
    """ recursive operation to extract tree with 'coordinates' with corresponding value, as list of lists.

    coordinates are integers that coorespond to position of the node based on parent location.
    if one node is the fifth child of a parent, its coordinate is 4 ==> 0b100
    this coordinate goes from 0 to 7.
    If we consider a frame with axes X, Y, Z, (front, left, up) then:
    coordinate | location | meaning
    -----------------------------------------
    0 : 000    | -X,-Y,-Z | back , right, down
    1 : 001    |  X,-Y,-Z | front, right, down
    2 : 010    | -X, Y,-Z | back , left , down
    3 : 011    |  X, Y,-Z | front, left , down
    4 : 100    | -X,-Y, Z | back , right, up
    5 : 101    |  X,-Y, Z | front, right, up
    6 : 110    | -X, Y, Z | back , left , up
    7 : 111    |  X, Y, Z | front, left , up

    TODO: the value should be replaced by a comparison function...
    """
    cnode = []

    for i in range(8):
        if node[i] is not None:
            if node[i] == value:
                cnode.append([i, value])
            elif isinstance(node[i], list):
                cnode.append([i, getListTree(node[i], value)])
    return cnode


def getFreeListTree(node):
    return getListTree(node, False)

def getOccupiedListTree(node):
    return getListTree(node, True)

def getUnknownListTree(node):
    return getListTree(node, None)



##def _computeCoord(coord, resolutionTable):
##    return sum([0.5 * resolutionTable[i] * (1 if c=="1" else -1) for i, c in enumerate(coord)])
##
##def nodeToCube(node, resolutionTable):
##    return (
##        _computeCoord(node[0], resolutionTable),
##        _computeCoord(node[1], resolutionTable),
##        _computeCoord(node[2], resolutionTable),
##        resolutionTable[len(node[0])-1]
##    )
##
##def nodesToCubes(nodes, resolutionTable):
##    return [nodeToCube(n, resolutionTable) for n in nodes]


##_unit_quads = [
##    np.array( ((-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1)) ),
##    np.array( ((1,-1,-1), (1,1,-1), (1,1,1), (1,-1,1)) ),
##    np.array( ((1,1,-1), (-1,1,-1), (-1,1,1), (1,1,1)) ),
##    np.array( ((-1,1,-1), (-1,-1,-1), (-1,-1,1), (-1,1,1)) ),
##    np.array( ((-1,-1,-1), (-1,1,-1), (1,1,-1), (1,-1,-1)) ),
##    np.array( ((-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)) ),
##]
##def nodeToQuad(node, resolutionTable):
##    x0 = _computeCoord(node[0], resolutionTable)
##    y0 = _computeCoord(node[1], resolutionTable)
##    z0 = _computeCoord(node[2], resolutionTable)
##    P0 = np.array((x0, y0, z0))
##    l = resolutionTable[len(node[0])-1]
##    Q = [P0 + l*0.5*ui for ui in _unit_quads]
##    return Q
##
##
##def nodesToQuads(nodes, resolutionTable):
##    quads = [q for n in nodes for q in nodeToQuad(n, resolutionTable)]
##
##    registeredPos = {}
##
##    for q in quads:
##        pos = tuple(np.mean(q, 0))
##        if pos in registeredPos:
##            del registeredPos[pos]
##            continue
##        else:
##            registeredPos[pos] = q
##
##    return registeredPos.values()

