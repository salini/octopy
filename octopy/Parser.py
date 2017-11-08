
from Node import TNode, CoordNode


def Serialize(tree):
    serialization = [None]*8
    for idx, child in enumerate(tree.children):
        if child is None:
            serialization[idx] = None
        else:
            if child.isLeaf():
                serialization[idx] = child.isOccupied()
            else:
                serialization[idx] = Serialize(child)
    return serialization


def Parse(tree_serialized, root):

    for idx, o in enumerate(tree_serialized):
        if o is not None:
            child = root.createNodeChild(idx)
            if o is True:
                child.setValid(True)
            elif o is False:
                child.setValid(False)
            elif isinstance(o, list) or isinstance(o, tuple):
                child.setValid(True)
                Parse(o, child)



if __name__ == "__main__":
    import visu
    treeRep = [True, [True, True, True, True, False, False, True, False], True, True, False, False, True, None]

    tree = CoordNode()
    Parse(treeRep, tree)
    tree.setNodeSizeRecursively()
    tree.setCoordinateRecursively()

    print Serialize(tree)

    visu.show(tree)
