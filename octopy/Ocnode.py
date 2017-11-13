

import numpy as np

#from bitarray import bitarray



_bitCoord = [
[False, True, False, True, False, True, False, True],
[False, False, True, True, False, False, True, True],
[False, False, False, False, True, True, True, True],
]

_coord = [
"01010101",
"00110011",
"00001111",
]


def getCoordTree_list(node, value, coordinate=None):
    if coordinate is None:
        #coordinate = [bitarray(), bitarray(), bitarray()]
        coordinate = [[], [], []]

    cnode = [coordinate, []]

    for i in range(8):
        if node[i] is not None:
            #ci = [bitarray(coordinate[0]), bitarray(coordinate[1]), bitarray(coordinate[2])]
            ci = [list(coordinate[0]), list(coordinate[1]), list(coordinate[2])]
            ci[0].append(_bitCoord[0][i]); ci[1].append(_bitCoord[1][i]); ci[2].append(_bitCoord[2][i])

            if node[i] == value:
                cnode[1].append([ci, value])
            elif isinstance(node[i], list):
                cnode[1].append([ci, getCoordTree_list(node[i], value, ci)])
    return cnode






def getCoordTree_string(node, value, coordinate=None):
    if coordinate is None:
        coordinate = ["", "", ""]

    cnode = [coordinate, []]

    for i in range(8):
        if node[i] is not None:
            ci = [coordinate[0] + _coord[0][i], coordinate[1] + _coord[1][i], coordinate[2] + _coord[2][i]]
            if node[i] == value:
                cnode[1].append([ci, value])
            elif isinstance(node[i], list):
                cnode[1].append([ci, getCoordTree_string(node[i], value, ci)])
    return cnode


def getCoordTree_bit(node, value, coordinate=0):
    cnode = [coordinate, []]

    for i in range(8):
        if node[i] is not None:
            ci = (coordinate<<3) | i
            if node[i] == value:
                cnode[1].append([ci, value])
            elif isinstance(node[i], list):
                cnode[1].append([ci, getCoordTree_bit(node[i], value, ci)])
    return cnode


def getLeaf(node, value, x="", y="", z=""):
    leaves = []
    for i in range(8):
        if node[i] == value:
            leaves.append( (x+_coord[0][i], y+_coord[1][i], z+_coord[2][i]) )
        elif isinstance(node[i], list):
            leaves.extend(getLeaf(node[i], value, x+_coord[0][i], y+_coord[1][i], z+_coord[2][i]))

    return leaves


def getFree(node, x="", y="", z=""):
    return getLeaf(node, False, x, y, z)

def getOccupied(node, x="", y="", z=""):
    return getLeaf(node, True, x, y, z)

def getUnknown(node, x="", y="", z=""):
    return getLeaf(node, None, x, y, z)



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

