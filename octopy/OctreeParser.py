

from Octree import Octree



##def _fromCharToBitSet(c):
##    bs = [(True if e=="1" else False) for e in '{0:08b}'.format(ord(c), 'b')]
##    bs.reverse()
##    return bs
##
##def _fromBitSetToChar(bs):
##    bs.reverse()
##    bsstring = "".join(["1" if b is True else "0" for b in bs])
##    c = chr(int(bsstring, 2))
##    return c


### functions from: https://wiki.python.org/moin/BitManipulation
def testBit(int_type, offset):
    mask = 1 << offset
    return (int_type & mask)

def setBit(int_type, offset):
    mask = 1 << offset
    return (int_type | mask)

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return (int_type & mask)


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
        child1to4 = ord(bstream.read(1))
        child5to8 = ord(bstream.read(1))

        for i in range(4):
            if testBit(child1to4, 2*i) and not testBit(child1to4, 2*i+1):
                node[i] = False # child is free leaf
            elif not testBit(child1to4, 2*i) and testBit(child1to4, 2*i+1):
               node[i] = True # child is occupied leaf
            elif testBit(child1to4, 2*i) and testBit(child1to4, 2*i+1):
                node[i] = [None]*8 # child have hildren

        for i in range(4):
            if testBit(child5to8, 2*i) and not testBit(child5to8, 2*i+1):
                node[i+4] = False # child is free leaf
            elif not testBit(child5to8, 2*i) and testBit(child5to8, 2*i+1):
                node[i+4] = True # child is occupied leaf
            elif testBit(child5to8, 2*i) and testBit(child5to8, 2*i+1):
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
        child1to4 = 0
        child5to8 = 0

        for i in range(4):
            if node[i] is None:
                child1to4 = clearBit(child1to4, 2*i); child1to4 = clearBit(child1to4, 2*i+1)
            elif node[i] is True:
                child1to4 = clearBit(child1to4, 2*i); child1to4 = setBit(child1to4, 2*i+1)
            elif node[i] is False:
                child1to4 = setBit(child1to4, 2*i);  child1to4 = clearBit(child1to4, 2*i+1)
            elif isinstance(node[i], list):
                child1to4 = setBit(child1to4, 2*i); child1to4 = setBit(child1to4, 2*i+1)

        for i in range(4):
            if node[i+4] is None:
                child5to8 = clearBit(child5to8, 2*i); child5to8 = clearBit(child5to8, 2*i+1)
            elif node[i+4] is True:
                child5to8 = clearBit(child5to8, 2*i); child5to8 = setBit(child5to8, 2*i+1)
            elif node[i+4] is False:
                child5to8 = setBit(child5to8, 2*i);  child5to8 = clearBit(child5to8, 2*i+1)
            elif isinstance(node[i+4], list):
                child5to8 = setBit(child5to8, 2*i); child5to8 = setBit(child5to8, 2*i+1)

        child1to4_char = chr(child1to4)
        child5to8_char = chr(child5to8)

        bstream.write(child1to4_char)
        bstream.write(child5to8_char)

        for i in range(8):
            if isinstance(node[i], list):
                self.writeBinaryNode(bstream, node[i])


    def writeFile(self, fileName, octree):
        with open(fileName, "wb") as F:
            self.writeFileHeader(F, octree)
            self.writeBinaryData(F, octree)


