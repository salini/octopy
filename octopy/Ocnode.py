

import numpy as np

def getValueTree(node, value, coordinate=0):
    """ recursive operation to extract tree with 'coordinates' with corresponding value

    coordinates are integers that coorespond to the tree branches:
    if one node is the fifth child of a parent, its coordinate is 4 ==> 0b100
    again if there is two levels, 3child then 4th child, coordinate is:
    [2, 3] ==> [0b010, 0b011] ==> coord = 0b 010 011
    etc.

    TODO: the value should be replaced by a comparison function...
    """
    #cnode = [coordinate, []]
    cnode = []

    for i in range(8):
        if node[i] is not None:
            ci = (coordinate<<3) | i
            if node[i] == value:
                cnode.append([ci, value])
            elif isinstance(node[i], list):
                cnode.append([ci, getValueTree(node[i], value, ci)])
    return cnode


def getFreeTree(node, coordinate=0):
    return getValueTree(node, False, coordinate)

def getOccupiedTree(node, coordinate=0):
    return getValueTree(node, True, coordinate)

def getUnknownTree(node, coordinate=0):
    return getValueTree(node, None, coordinate)



def _computeCoord(coord, resolutionTable):
    return sum([0.5 * resolutionTable[i] * (1 if c=="1" else -1) for i, c in enumerate(coord)])

def nodeToCube(node, resolutionTable):
    return (
        _computeCoord(node[0], resolutionTable),
        _computeCoord(node[1], resolutionTable),
        _computeCoord(node[2], resolutionTable),
        resolutionTable[len(node[0])-1]
    )

def nodesToCubes(nodes, resolutionTable):
    return [nodeToCube(n, resolutionTable) for n in nodes]


_unit_quads = [
    np.array( ((-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1)) ),
    np.array( ((1,-1,-1), (1,1,-1), (1,1,1), (1,-1,1)) ),
    np.array( ((1,1,-1), (-1,1,-1), (-1,1,1), (1,1,1)) ),
    np.array( ((-1,1,-1), (-1,-1,-1), (-1,-1,1), (-1,1,1)) ),
    np.array( ((-1,-1,-1), (-1,1,-1), (1,1,-1), (1,-1,-1)) ),
    np.array( ((-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)) ),
]
def nodeToQuad(node, resolutionTable):
    x0 = _computeCoord(node[0], resolutionTable)
    y0 = _computeCoord(node[1], resolutionTable)
    z0 = _computeCoord(node[2], resolutionTable)
    P0 = np.array((x0, y0, z0))
    l = resolutionTable[len(node[0])-1]
    Q = [P0 + l*0.5*ui for ui in _unit_quads]
    return Q


def nodesToQuads(nodes, resolutionTable):
    quads = [q for n in nodes for q in nodeToQuad(n, resolutionTable)]

    registeredPos = {}

    for q in quads:
        pos = tuple(np.mean(q, 0))
        if pos in registeredPos:
            del registeredPos[pos]
            continue
        else:
            registeredPos[pos] = q

    return registeredPos.values()

