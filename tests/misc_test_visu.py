
import common  # to load path to octopy package

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getFreeListTree, getOccupiedListTree, getUnknownListTree, getOccupiedOcnodeTree
from octopy.visu.core import show
from octopy.visu.OSGOctree import *
from octopy.visu.effects import setWireframe, setMaterialColor, createOSGGroup

from osgswig import osgUtil, osg
from time import time

#inFileName = common.getFromTestDir("../resources/simple.bt")
#inFileName = common.getFromTestDir("../resources/test.bt")
#inFileName = common.getFromTestDir("../resources/fr_078_tidyup.bt")
#inFileName = common.getFromTestDir("../resources/freiburg1_360.bt") # not working for now


def draw_recursiveRawCubes():
    """
    conclusion:
    osg tree building is quite quick, but, the osg structure has too many node;
    if osg stat, cull is fully loaded ==> heavy frame drop
    for test.bt:
        * cull = 178
        * draw = 66
        * gpu = 66
    """
    inFileName = common.getFromTestDir("../resources/test.bt")
    octree = OctreeParser().readFile(inFileName)
    occupied = getOccupiedListTree(octree.root)
    t = time()
    root = createOSGTree_recursiveRawCubes(occupied, octree.getResolutionTable()[0]) #NOT EFFICIENT
    loadTime = time() - t
    print "loading time:", loadTime # for test.bt: res = about 1.43099999428
    show(root)

def draw_recursiveRawCubes_with_optimization():
    """
    conclusion:
    osg tree building is quite quick, but, the osg structure has too many node;
    if osg stat, cull is fully loaded ==> heavy frame drop
    for test.bt:
        * cull = 178
        * draw = 66
        * gpu = 66

    So not interesting at all
    """
    inFileName = common.getFromTestDir("../resources/test.bt")
    octree = OctreeParser().readFile(inFileName)
    occupied = getOccupiedListTree(octree.root)
    t = time()
    root = createOSGTree_recursiveRawCubes(occupied, octree.getResolutionTable()[0]) #NOT EFFICIENT
    loadTime = time() - t
    print "loading time:", loadTime # for test.bt: res = about 1.43099999428
    optimizer = osgUtil.Optimizer()
    t = time()
    #optimizer.optimize(root, osgUtil.Optimizer.ALL_OPTIMIZATIONS)
    optimizer.optimize(root, osgUtil.Optimizer.FLATTEN_STATIC_TRANSFORMS)
    optimizeTime = time() - t
    print "optimize time:", optimizeTime # for test.bt: about 3.97799992561
    show(root)


def draw_flatRawCubes():
    """
    conclusion:
    osg tree building is slow, but less frame drop
    if osg stat, cull is fully loaded ==> frame drop
    for test.bt:
        * cull = 46
        * draw = 67
        * gpu = 65
    """
    #inFileName = common.getFromTestDir("../resources/simple.bt")
    #inFileName = common.getFromTestDir("../resources/test.bt")
    inFileName = common.getFromTestDir("../resources/fr_078_tidyup.bt")
    #inFileName = common.getFromTestDir("../resources/freiburg1_360.bt") #NOT WORKING
    octree = OctreeParser().readFile(inFileName)
    #occupied = getOccupiedListTree(octree.root)  # both can be used
    occupied = getOccupiedOcnodeTree(octree.root) # both can be used
    t = time()
    root = createOSGTree_flatRawCubes(occupied, octree.getResolutionTable()[0])
    loadTime = time() - t
    print "loading time:", loadTime  # for test.bt: res = about 5.69099998474
    show(root)


def draw_wireframe():
    inFileName = common.getFromTestDir("../resources/test.bt")
    octree = OctreeParser().readFile(inFileName)
    occupied = getOccupiedListTree(octree.root)
    root = createOSGTree_flatRawCubes(occupied, octree.getResolutionTable()[0])
    setWireframe(root)
    show(root)


def draw_colored_cubes():
    inFileName = common.getFromTestDir("../resources/test.bt")
    octree = OctreeParser().readFile(inFileName)

    f=getFreeListTree(octree.root)
    o=getOccupiedListTree(octree.root)
    u=getUnknownListTree(octree.root)

    cf = createOSGTree_flatRawCubes(f, octree.getResolutionTable()[0])
    co = createOSGTree_flatRawCubes(o, octree.getResolutionTable()[0])
    cu = createOSGTree_flatRawCubes(u, octree.getResolutionTable()[0])

    root = createOSGGroup()

    setMaterialColor(cf, (0,0.9,0,0.3))
    setMaterialColor(co, (1,0,0,1))
    setMaterialColor(cu, (1,1,0,1))
    setWireframe(cu)

    root.addChild(cf)
    root.addChild(co)
    root.addChild(cu)

    show(root)


def draw_with_quads():
    #inFileName = common.getFromTestDir("../resources/simple.bt")
    #inFileName = common.getFromTestDir("../resources/test.bt")
    inFileName = common.getFromTestDir("../resources/fr_078_tidyup.bt")
    #inFileName = common.getFromTestDir("../resources/freiburg1_360.bt") NOT WORKING
    octree = OctreeParser().readFile(inFileName)
    #o=getOccupiedListTree(octree.root)
    o=getOccupiedOcnodeTree(octree.root)
    t = time()
    root = createOSGTree_flatRawQuads(o, octree.getResolutionTable()[0])
    loadTime = time() - t
    print "loading time:", loadTime
    #setMaterialColor(root, (1,0,0,1))
    #setWireframe(root)
    show(root)



if __name__ == "__main__":
    #draw_recursiveRawCubes()
    #draw_recursiveRawCubes_with_optimization()
    draw_flatRawCubes()
    #draw_wireframe()
    #draw_colored_cubes()
    #draw_with_quads()
