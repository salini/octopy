

class Octree(object):
    def __init__(self, resolution=1.0):
        self.root = [None]*8
        self.octreeId = "OcTree"
        self.size = 0
        self.resolution = resolution


    def getSize(self):
        return Octree.getNumberOfNodes(self.root)

    @staticmethod
    def getNumberOfNodes(node):
        val = 1
        for child in node:
            if child in [True, False]:
                val += 1
            elif isinstance(child, list):
                val += Octree.getNumberOfNodes(child)

        return val

    @staticmethod
    def getDepth(node):
        subnode = [c for c in node if isinstance(c, list)]
        if len(subnode) == 0:
            return 1
        else:
            return 1 + max([Octree.getDepth(c) for c in subnode])


    def getResolutionTable(self):
        depth = self.getDepth(self.root)
        return [self.resolution * 2**(depth-i-1) for i in range(depth)]

