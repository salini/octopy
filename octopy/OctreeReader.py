

from Node import TNode



def _fromCharToBitSet(c):
    bs = [(True if e=="1" else False) for e in '{0:08b}'.format(ord(c), 'b')]
    bs.reverse()
    return bs


def _octreeReadBinaryNode(bstream, node):
    child1to4_char = bstream.read(1)
    child5to8_char = bstream.read(1)

    child1to4 = _fromCharToBitSet(child1to4_char)
    child5to8 = _fromCharToBitSet(child5to8_char)

    node.setValid(True)

    for i in range(4):
        if (child1to4[2*i] is True) and (child1to4[(2*i)+1] is False):
            # child is free leaf
            node.createNodeChild(i).setValid(False)
        elif (child1to4[2*i] is False) and (child1to4[(2*i)+1] is True):
            # child is occupied leaf
            node.createNodeChild(i).setValid(True)
        elif (child1to4[2*i] is True) and (child1to4[(2*i)+1] is True):
            node.createNodeChild(i).setValid(None) #child is unkown, we leave it uninitialized

    for i in range(4):
        if (child5to8[2*i] is True) and (child5to8[(2*i)+1] is False):
            # child is free leaf
            node.createNodeChild(i+4).setValid(False)
        elif (child5to8[2*i] is False) and (child5to8[(2*i)+1] is True):
            # child is occupied leaf
            node.createNodeChild(i+4).setValid(True)
        elif (child5to8[2*i] is True) and (child5to8[(2*i)+1] is True):
            node.createNodeChild(i+4).setValid(None) #child is unkown, we leave it uninitialized


    for i in range(8):
        if node.nodeChildExists(i):
            child = node.getNodeChild(i)
            if child.getValid() is None:
                _octreeReadBinaryNode(bstream, child)
                child.setValid(True)



def _octreeReadHeader(F):
    headerDict = {}
    headerRead = False

    while not headerRead:
        l = F.readline()
        elements = l.split()
        if len(elements):
            if elements[0][0:1] == "#":
                continue
            elif elements[0] == "id":
                headerDict["id"] = elements[1]
            elif elements[0] == "size":
                headerDict["size"] = int(elements[1])
            elif elements[0] == "res":
                headerDict["res"] = float(elements[1])
            elif elements[0] == "data":
                headerRead = True
            else:
                raise ValueError(l)

    return headerDict


def _octreeReadData(F, NodeType):
    n = NodeType()
    _octreeReadBinaryNode(F, n)
    return n


def OctreeRead(fileName, NodeType=None):
    NodeType = NodeType if NodeType is not None else TNode
    with open(fileName, "rb") as F:
        if F.readline().startswith("# Octomap OcTree binary file"):
            header = _octreeReadHeader(F)
            ot = _octreeReadData(F, NodeType)
        else:
            raise RuntimeError()

    return header, ot






if __name__ == "__main__":
    filename = "../resources/test.bt"
    header, octree = OctreeRead(filename)
    print header
    print "end"