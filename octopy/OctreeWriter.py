



from Node import TNode

from Parser import Parse


def _fromBitSetToChar(bs):
    bs.reverse()
    bsstring = "".join(["1" if b is True else "0" for b in bs])
    c = chr(int(bsstring, 2))
    return c

def _octreeWriteData(bstream, node):

    child1to4 = [None]*8
    child5to8 = [None]*8

    for i in range(4):
        child = node.getNodeChild(i)
        if child is None:
            child1to4[2*i] = False; child1to4[(2*i)+1] = False
        else:
            if child.isLeaf():
                if child.isOccupied():
                    child1to4[2*i] = False; child1to4[(2*i)+1] = True
                else:
                    child1to4[2*i] = True;  child1to4[(2*i)+1] = False
            else:
                child1to4[2*i] = True; child1to4[(2*i)+1] = True


    for i in range(4):
        child = node.getNodeChild(i+4)
        if child is None:
            child5to8[2*i] = False; child5to8[(2*i)+1] = False
        else:
            if child is not None and child.isLeaf():
                if child.isOccupied():
                    child5to8[2*i] = False; child5to8[(2*i)+1] = True
                else:
                    child5to8[2*i] = True;  child5to8[(2*i)+1] = False
            else:
                child5to8[2*i] = True; child5to8[(2*i)+1] = True

    child1to4_char = _fromBitSetToChar(child1to4)
    child5to8_char = _fromBitSetToChar(child5to8)

    bstream.write(child1to4_char)
    bstream.write(child5to8_char)


    for i in range(8):
        if node.nodeChildExists(i):
            child = node.getNodeChild(i)
            if not child.isLeaf():
                _octreeWriteData(bstream, child)



def _octreeWriteHeader(F, tree, res):
    treeId = "OcTree"
    size = tree.getNumberOfNodes()
    header="""# Octomap OcTree binary file
# (feel free to add / change comments, but leave the first line as it is!)
#
id {0}
size {1}
res {2}
data
""".format(treeId, size, res)
    F.write(header)



def OctreeWrite(fileName, tree, resolution=1.0):
    with open(fileName, "wb") as F:
        _octreeWriteHeader(F, tree, resolution)
        _octreeWriteData(F, tree)





if __name__ == "__main__":
    treeRep = [True, [True, True, True, True, False, False, True, False], True, True, False, False, True, False]

    tree = TNode()
    Parse(treeRep, tree)

    filename = "../resources/out.bt"
    OctreeWrite(filename, tree)
    print "end"

