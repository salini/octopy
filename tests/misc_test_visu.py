
import common  # to load path to octopy package

from octopy.OctreeParser import OctreeParser
from octopy.Ocnode import getFree, getOccupied, getUnknown, nodesToCubes
from octopy.visu.core import show
from octopy.visu.OSGOctree import createOSGCubes
from octopy.visu.effects import setWireframe, setMaterialColor, createOSGGroup


inFileName = common.getFromTestDir("../resources/simple.bt")
#inFileName = common.getFromTestDir("../resources/test.bt")
octree = OctreeParser().readFile(inFileName)


def draw_wireframe():
    occupied = getOccupied(octree.root)
    cubes = nodesToCubes(occupied, octree.getResolutionTable())
    root = createOSGCubes(cubes)
    setWireframe(root)
    show(root)


def draw_colored_cubes():
    f=getFree(octree.root)
    o=getOccupied(octree.root)
    u=getUnknown(octree.root)

    cf = createOSGCubes(nodesToCubes(f, octree.getResolutionTable()))
    co = createOSGCubes(nodesToCubes(o, octree.getResolutionTable()))
    cu = createOSGCubes(nodesToCubes(u, octree.getResolutionTable()))

    root = createOSGGroup()

    setMaterialColor(cf, (0,0.9,0,0.3))
    setMaterialColor(co, (1,0,0,1))
    setMaterialColor(cu, (1,1,0,1))
    setWireframe(cu)

    root.addChild(cf)
    root.addChild(co)
    root.addChild(cu)

    show(root)

if __name__ == "__main__":
    draw_wireframe()
    draw_colored_cubes()

