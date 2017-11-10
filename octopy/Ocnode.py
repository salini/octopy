

_coord = [
"01010101",
"00110011",
"00001111",
]

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

def convertNodeToCube(node, resolutionTable):
    return (
        _computeCoord(node[0], resolutionTable),
        _computeCoord(node[1], resolutionTable),
        _computeCoord(node[2], resolutionTable),
        resolutionTable[len(node[0])-1]
    )

def convertNodesToCubes(nodes, resolutionTable):
    return [convertNodeToCube(n, resolutionTable) for n in nodes]


if __name__ == "__main__":
    import time
    from OctreeParser import OctreeParser

    inFileName = "../resources/simple.bt"
    octree = OctreeParser().readFile(inFileName)
    print octree.root

    print "FREE:", getFree(octree.root)
    print "OCCUPIED:", getOccupied(octree.root)
    print "UNKNOWN:", getUnknown(octree.root)
    print "OCCUPIED[1]:", getOccupied(octree.root[1])

    print "CUBES:", convertNodesToCubes(getOccupied(octree.root), octree.getResolutionTable())

    for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
        inFileName = "../resources/{0}.bt".format(n)
        t = time.time()
        octree = OctreeParser().readFile(inFileName)
        tread = time.time() - t
        t = time.time()
        free = getFree(octree.root)
        tfree = time.time() - t
        t = time.time()
        occupied = getOccupied(octree.root)
        tocc = time.time() - t
        t = time.time()
        unknown = getUnknown(octree.root)
        tunknown = time.time() - t
        print "READ:", inFileName, tread
        print "T free/occupied/unknown:", tfree, tocc, tunknown
        print "nb node/free/occupied/unknown", octree.size, len(free), len(occupied), len(unknown)


