

from Octree import Octree



def _fromCharToBitSet(c):
    bs = [(True if e=="1" else False) for e in '{0:08b}'.format(ord(c), 'b')]
    bs.reverse()
    return bs

def _fromBitSetToChar(bs):
    bs.reverse()
    bsstring = "".join(["1" if b is True else "0" for b in bs])
    c = chr(int(bsstring, 2))
    return c


class OctreeParser(object):
    def __init__(self):
        pass

    def parseFileHeader(self, fstream):
        headerDict = {}
        headerRead = False

        while not headerRead:
            l = fstream.readline()
            elements = l.split()
            if len(elements):
                if elements[0][0:1] == "#":
                    continue
                elif elements[0] == "id":
                    headerDict["octreeId"] = elements[1]
                elif elements[0] == "size":
                    headerDict["size"] = int(elements[1])
                elif elements[0] == "res":
                    headerDict["resolution"] = float(elements[1])
                elif elements[0] == "data":
                    headerRead = True
                else:
                    raise ValueError(l)

        return headerDict


    def parseBinaryData(self, bstream):
        octree = Octree()
        self.parseBinaryNode(bstream, octree.root)
        return octree


    def parseBinaryNode(self, bstream, node):
        child1to4_char = bstream.read(1)
        child5to8_char = bstream.read(1)

        child1to4 = _fromCharToBitSet(child1to4_char)
        child5to8 = _fromCharToBitSet(child5to8_char)

        for i in range(4):
            if (child1to4[2*i] is True) and (child1to4[(2*i)+1] is False):
                node[i] = False # child is free leaf
            elif (child1to4[2*i] is False) and (child1to4[(2*i)+1] is True):
               node[i] = True # child is occupied leaf
            elif (child1to4[2*i] is True) and (child1to4[(2*i)+1] is True):
                node[i] = [None]*8 # child have hildren

        for i in range(4):
            if (child5to8[2*i] is True) and (child5to8[(2*i)+1] is False):
                node[i+4] = False # child is free leaf
            elif (child5to8[2*i] is False) and (child5to8[(2*i)+1] is True):
                node[i+4] = True # child is occupied leaf
            elif (child5to8[2*i] is True) and (child5to8[(2*i)+1] is True):
                node[i+4] = [None]*8 # child have hildren

        for i in range(8):
            if isinstance(node[i], list):
                self.parseBinaryNode(bstream, node[i])


    def readFile(self, fileName):
        with open(fileName, "rb") as F:
            if F.readline().startswith("# Octomap OcTree binary file"):
                header = self.parseFileHeader(F)
                octree = self.parseBinaryData(F)
                octree.octreeId = header["octreeId"]
                octree.size = header["size"]
                octree.resolution = header["resolution"]
            else:
                raise RuntimeError()

        return octree




    def writeFileHeader(self, fstream, octree):
        octreeId = octree.octreeId
        size = octree.size
        resolution = octree.resolution
        header="""# Octomap OcTree binary file
# (feel free to add / change comments, but leave the first line as it is!)
#
id {0}
size {1}
res {2}
data
""".format(octreeId, size, resolution)
        fstream.write(header)

    def writeBinaryData(self, bstream, octree):
        self.writeBinaryNode(bstream, octree.root)


    def writeBinaryNode(self, bstream, node):
        child1to4 = [None]*8
        child5to8 = [None]*8

        for i in range(4):
            if node[i] is None:
                child1to4[2*i] = False; child1to4[(2*i)+1] = False
            elif node[i] is True:
                child1to4[2*i] = False; child1to4[(2*i)+1] = True
            elif node[i] is False:
                child1to4[2*i] = True;  child1to4[(2*i)+1] = False
            elif isinstance(node[i], list):
                child1to4[2*i] = True; child1to4[(2*i)+1] = True

        for i in range(4):
            if node[i+4] is None:
                child5to8[2*i] = False; child5to8[(2*i)+1] = False
            elif node[i+4] is True:
                child5to8[2*i] = False; child5to8[(2*i)+1] = True
            elif node[i+4] is False:
                child5to8[2*i] = True;  child5to8[(2*i)+1] = False
            elif isinstance(node[i+4], list):
                child5to8[2*i] = True; child5to8[(2*i)+1] = True

        child1to4_char = _fromBitSetToChar(child1to4)
        child5to8_char = _fromBitSetToChar(child5to8)

        bstream.write(child1to4_char)
        bstream.write(child5to8_char)

        for i in range(8):
            if isinstance(node[i], list):
                self.writeBinaryNode(bstream, node[i])



    def writeFile(self, fileName, octree):
        with open(fileName, "wb") as F:
            self.writeFileHeader(F, octree)
            self.writeBinaryData(F, octree)




if __name__ == "__main__":
    import time
    import filecmp

    for n in ["simple", "test", "fr_078_tidyup", "freiburg1_360"]:
        inFileName = "../resources/{0}.bt".format(n)
        outFileName = "../resources/_rewrite_{0}.bt".format(n)
        t = time.time()
        octree = OctreeParser().readFile(inFileName)
        tread = time.time() - t
        t = time.time()
        OctreeParser().writeFile(outFileName, octree)
        twrite = time.time() - t
        print "READ:", inFileName, tread
        print "size from file:", octree.size
        print "size of octree:", octree.getSize()
        print "WRITE:", outFileName, twrite
        print "SAME?:", filecmp.cmp(inFileName, outFileName, False)




