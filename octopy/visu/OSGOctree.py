
from core import getBox

from osgswig import osg, osgUtil

import numpy as np

from ..bitOperation import testBit

from ..Ocnode import Ocnode

_POSITION = [
osg.Vec3d(-0.25,-0.25,-0.25),
osg.Vec3d( 0.25,-0.25,-0.25),
osg.Vec3d(-0.25, 0.25,-0.25),
osg.Vec3d( 0.25, 0.25,-0.25),
osg.Vec3d(-0.25,-0.25, 0.25),
osg.Vec3d( 0.25,-0.25, 0.25),
osg.Vec3d(-0.25, 0.25, 0.25),
osg.Vec3d( 0.25, 0.25, 0.25),
]

_BOX = getBox((0,0,0), (1,1,1))
_BOX.setDataVariance(osg.Object.STATIC)


def createOSGBranches(osgNode, treeNode):
    for coordinate, value in treeNode:
        osgn = osg.AutoTransform()
        osgn.setDataVariance(osg.Object.STATIC)
        osgNode.addChild(osgn)
        coord = coordinate & 7
        osgn.setPosition(_POSITION[coord])
        osgn.setScale(0.5)
        if isinstance(value, list):
            createOSGBranches(osgn, value)
        else:
            osgn.addChild(_BOX)


def createOSGTree_recursiveRawCubes(treeRoot, dim0):
    print "start creating OSG tree as flat cubes"
    osgRoot = osg.AutoTransform()
    osgRoot.setDataVariance(osg.Object.STATIC)
    osgRoot.setScale(dim0)
    createOSGBranches(osgRoot, treeRoot)
    print "end"
    return osgRoot





def getPosFromCoordinate(coord, table):
    x = sum([0.5*table[-idx-1] * (1 if testBit(coord, 3*idx  ) else -1) for idx in range(len(table))])
    y = sum([0.5*table[-idx-1] * (1 if testBit(coord, 3*idx+1) else -1) for idx in range(len(table))])
    z = sum([0.5*table[-idx-1] * (1 if testBit(coord, 3*idx+2) else -1) for idx in range(len(table))])
    return (x,y,z)


def parseTreeList(osgRootNode, treeNode, table, parent_coordinate=0):
    for ccoord, value in treeNode:
        coordinate = (parent_coordinate<<3) | ccoord
        if not isinstance(value, list):
            pos = getPosFromCoordinate(coordinate, table)
            extents = (table[-1], table[-1], table[-1])
            osgRootNode.addChild(getBox(pos, extents))
        else:
            subtable = list(table)
            subtable.append(subtable[-1]*0.5)
            parseTreeList(osgRootNode, value, subtable, coordinate)



def parseTreeOcnode(osgRootNode, treeNode, table, parent_coordinate=0):
    for child in treeNode.children:
        coordinate = (parent_coordinate<<3) | child.coordinate
        if child.isLeaf:
            pos = getPosFromCoordinate(coordinate, table)
            extents = (table[-1], table[-1], table[-1])
            osgRootNode.addChild(getBox(pos, extents))
        else:
            subtable = list(table)
            subtable.append(subtable[-1]*0.5)
            parseTreeOcnode(osgRootNode, child, subtable, coordinate)


def createOSGTree_flatRawCubes(treeRoot, dim0):
    table = [dim0]
    print "start creating OSG tree as flat cubes"
    root = osg.Group()
    if isinstance(treeRoot, list):
        parseTreeList(root, treeRoot, table)
    elif isinstance(treeRoot, Ocnode):
        parseTreeOcnode(root, treeRoot, table)
    print "end"
    return root



#def createOSGTree_flatRawQuads(treeRoot, dim0):


def createOSGCubes(cubes):
    print "start creating OSG cubes"
    root = osg.Group()
    for c in cubes:
        pos = (c[0], c[1], c[2])
        dim = (c[3], c[3], c[3])
        root.addChild(getBox(pos, dim))
    print "done"

    return root



def createOSGQuads(quads):
    print "start creating OSG quads"
    root = osg.Group()
    geode = osg.Geode()
    geometry = osg.Geometry()
    vertices = osg.Vec3Array()
    #colors = osg.Vec4Array()
    #normals = osg.Vec3Array()

    root.addChild(geode)
    geode.addDrawable(geometry)
    geometry.setVertexArray(vertices)
    #geometry.setColorArray(colors)
    #geometry.setNormalArray(normals)
    #geometry.setColorBinding(osg.Geometry.BIND_OVERALL)
    #geometry.setNormalBinding(osg.Geometry.BIND_PER_PRIMITIVE_SET)

    #colors.push_back(osg.Vec4(1,1,1,1))

    idx = 0
    for q in quads:
        for v in q:
            vertices.push_back(osg.Vec3(*v))
        primitive = osg.DrawElementsUInt(osg.PrimitiveSet.QUADS, 0)
        primitive.push_back(idx+0)
        primitive.push_back(idx+1)
        primitive.push_back(idx+2)
        primitive.push_back(idx+3)

        #v0 = q[1] - q[0]
        #v1 = q[-1] - q[0]
        #n = np.cross(v0, v1)
        #n /= np.linalg.norm(n)
        #normals.push_back(osg.Vec3(*n))

        geometry.addPrimitiveSet(primitive)

        idx +=4

    sv = osgUtil.SmoothingVisitor() #to compute normals
    sv.setCreaseAngle(0.0)
    root.accept(sv)

    print "done"

    return root