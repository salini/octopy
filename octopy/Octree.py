

class Octree(object):
    def __init__(self, resolution=1.0):
        self.root = [None]*8
        self.octreeId = "OcTree"
        self.size = 0
        self.resolution = resolution


    def getSize(self):
        return self.getNumberOfNodes(self.root)

    def getNumberOfNodes(self, node):
        val = 1
        for child in node:
            if child in [True, False]:
                val += 1
            elif isinstance(child, list):
                val += self.getNumberOfNodes(child)

        return val


    def getDepth(self, node):
        subnode = [c for c in node if isinstance(c, list)]
        if len(subnode) == 0:
            return 1
        else:
            return 1 + max([self.getDepth(c) for c in subnode])


    def getResolutionTable(self):
        depth = self.getDepth(self.root)
        return [self.resolution * 2**(depth-i-1) for i in range(depth)]




if __name__ == "__main__":
    import time
    from OctreeParser import OctreeParser

    for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
        inFileName = "../resources/{0}.bt".format(n)
        octree = OctreeParser().readFile(inFileName)
        t = time.time()
        depth = octree.getDepth(octree.root)
        tdepth = time.time() - t
        print "DEPTH:", inFileName, tdepth, depth
        print "Resolution Table:", octree.getResolutionTable()

