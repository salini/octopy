


def _fromCharToBitSet(c):
    bs = [(True if e=="1" else False) for e in '{0:08b}'.format(ord(c), 'b')]
    bs.reverse()
    return bs


def _octreeReadBinaryNode2(bstream, node):
    child1to4_char = bstream.read(1)
    child5to8_char = bstream.read(1)

    child1to4 = _fromCharToBitSet(child1to4_char)
    child5to8 = _fromCharToBitSet(child5to8_char)

    for i in range(4):
        if (child1to4[2*i] is True) and (child1to4[(2*i)+1] is False):
            # child is free leaf
            node[i] = False
        elif (child1to4[2*i] is False) and (child1to4[(2*i)+1] is True):
            # child is occupied leaf
           node[i] = True
        elif (child1to4[2*i] is True) and (child1to4[(2*i)+1] is True):
            node[i] = [None]*8

    for i in range(4):
        if (child5to8[2*i] is True) and (child5to8[(2*i)+1] is False):
            # child is free leaf
            node[i+4] = False
        elif (child5to8[2*i] is False) and (child5to8[(2*i)+1] is True):
            # child is occupied leaf
            node[i+4] = True
        elif (child5to8[2*i] is True) and (child5to8[(2*i)+1] is True):
            node[i+4] = [None]*8


    for i in range(8):
        if isinstance(node[i], list):
            _octreeReadBinaryNode2(bstream, node[i])



def _octreeReadHeader2(F):
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


def _octreeReadData2(F):
    n = [None]*8
    _octreeReadBinaryNode2(F, n)
    return n


def OctreeRead2(fileName):
    with open(fileName, "rb") as F:
        if F.readline().startswith("# Octomap OcTree binary file"):
            header = _octreeReadHeader2(F)
            ot = _octreeReadData2(F)
        else:
            raise RuntimeError()

    return header, ot






if __name__ == "__main__":
    from Parser import Serialize
    filename = "../resources/out.bt"
    header, octree = OctreeRead2(filename)
    print octree
    print header
    print "end"
