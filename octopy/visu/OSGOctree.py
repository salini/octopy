
from core import getBoxGeode, getBoxDrawable

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

_BOX = getBoxGeode((0,0,0), 1)
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



POWER2 = [2**idx for idx in range(24)]

def getPosFromCoordinate(coord, dim, depth):
    x = dim * 0.5 * sum([POWER2[idx] * (1 if testBit(coord, 3*idx  ) else -1) for idx in range(depth)])
    y = dim * 0.5 * sum([POWER2[idx] * (1 if testBit(coord, 3*idx+1) else -1) for idx in range(depth)])
    z = dim * 0.5 * sum([POWER2[idx] * (1 if testBit(coord, 3*idx+2) else -1) for idx in range(depth)])
    return (x,y,z)


def parseTreeList(fn_action, treeNode, dim, depth=1, parent_coordinate=0):
    for ccoord, value in treeNode:
        coordinate = (parent_coordinate<<3) | ccoord
        if not isinstance(value, list):
            pos = getPosFromCoordinate(coordinate, dim, depth)
            fn_action(pos, dim)
        else:
            parseTreeList(fn_action, value, dim*0.5, depth+1, coordinate)



def parseTreeOcnode(fn_action, treeNode, dim, depth=1, parent_coordinate=0):
    for child in treeNode.children:
        coordinate = (parent_coordinate<<3) | child.coordinate
        if child.isLeaf:
            pos = getPosFromCoordinate(coordinate, dim, depth)
            fn_action(pos, dim)
        else:
            parseTreeOcnode(fn_action, child, dim*0.5, depth+1, coordinate)


def parseTree(fn_action, treeRoot, dim):
    if isinstance(treeRoot, list):
        parseTreeList(fn_action, treeRoot, dim)
    elif isinstance(treeRoot, Ocnode):
        parseTreeOcnode(fn_action, treeRoot, dim)



def createOSGTree_flatRawCubes(treeRoot, dim0):
    print "start creating OSG tree as flat cubes"
    root = osg.Group()
    geode = osg.Geode()
    root.addChild(geode)
    fn_action = lambda pos, dim: geode.addDrawable(getBoxDrawable(pos, dim))
    parseTree(fn_action, treeRoot, dim0)
    print "end"
    return root






_unit_quads = [
    np.array( ((-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1)) ),
    np.array( ((1,-1,-1), (1,1,-1), (1,1,1), (1,-1,1)) ),
    np.array( ((1,1,-1), (-1,1,-1), (-1,1,1), (1,1,1)) ),
    np.array( ((-1,1,-1), (-1,-1,-1), (-1,-1,1), (-1,1,1)) ),
    np.array( ((-1,-1,-1), (-1,1,-1), (1,1,-1), (1,-1,-1)) ),
    np.array( ((-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)) ),
]

def nodeToQuad(pos, dim):
    Q = [np.array(pos) + dim*0.5*ui for ui in _unit_quads]
    return Q

def getAllQuads(treeRoot, dim0):
    Q = []
    fn_action = lambda pos, dim: Q.extend(q for q in nodeToQuad(pos, dim))
    parseTree(fn_action, treeRoot, dim0)
    return Q

def trimQuads(quads):
    registeredPos = {}
    for q in quads:
        pos = tuple(np.mean(q, 0))
        if pos in registeredPos:
            del registeredPos[pos]
            continue
        else:
            registeredPos[pos] = q

    return registeredPos.values()




from time import time

def createOSGTree_flatRawQuads(treeRoot, dim0):

    def _addQuadVertices(_vertices, _q):
        for v in _q:
            _vertices.push_back(osg.Vec3(*v))

    def _addQuadPrimitive(_geometry, _idx):
        primitive = osg.DrawElementsUInt(osg.PrimitiveSet.QUADS, 0)
        primitive.push_back(_idx+0)
        primitive.push_back(_idx+1)
        primitive.push_back(_idx+2)
        primitive.push_back(_idx+3)
        _geometry.addPrimitiveSet(primitive)



    print "get all quads..."
    t = time()
    quads = getAllQuads(treeRoot, dim0)
    print time() -t
    print "len", len(quads)

    print "trim quads..."
    t = time()
    quads = trimQuads(quads)
    print time() -t
    print "len", len(quads)

    print "start creating OSG quads"
    t = time()
    root = osg.Group()
    geode = osg.Geode()
    root.addChild(geode)
    geometry = osg.Geometry()
    geode.addDrawable(geometry)
    vertices = osg.Vec3Array()
    normals = osg.Vec3Array()
    geometry.setVertexArray(vertices)
    geometry.setNormalArray(normals)
    geometry.setNormalBinding(osg.Geometry.BIND_PER_PRIMITIVE_SET)


    idx = 0
    for q in quads:
        _addQuadVertices(vertices, q)
        _addQuadPrimitive(geometry, idx)
        idx +=4

    print time() -t

    print "smoothing..."
    t = time()
    sv = osgUtil.SmoothingVisitor() #to compute normals
    sv.setCreaseAngle(0.0)
    root.accept(sv)
    print time() -t


    return root




##def createOSGCubes(cubes):
##    print "start creating OSG cubes"
##    root = osg.Group()
##    for c in cubes:
##        pos = (c[0], c[1], c[2])
##        dim = (c[3], c[3], c[3])
##        root.addChild(getBox(pos, dim))
##    print "done"
##
##    return root
##
##
##
##def createOSGQuads(quads):
##    print "start creating OSG quads"
##    root = osg.Group()
##    geode = osg.Geode()
##    geometry = osg.Geometry()
##    vertices = osg.Vec3Array()
##    #colors = osg.Vec4Array()
##    #normals = osg.Vec3Array()
##
##    root.addChild(geode)
##    geode.addDrawable(geometry)
##    geometry.setVertexArray(vertices)
##    #geometry.setColorArray(colors)
##    #geometry.setNormalArray(normals)
##    #geometry.setColorBinding(osg.Geometry.BIND_OVERALL)
##    #geometry.setNormalBinding(osg.Geometry.BIND_PER_PRIMITIVE_SET)
##
##    #colors.push_back(osg.Vec4(1,1,1,1))
##
##    idx = 0
##    for q in quads:
##        for v in q:
##            vertices.push_back(osg.Vec3(*v))
##        primitive = osg.DrawElementsUInt(osg.PrimitiveSet.QUADS, 0)
##        primitive.push_back(idx+0)
##        primitive.push_back(idx+1)
##        primitive.push_back(idx+2)
##        primitive.push_back(idx+3)
##
##        #v0 = q[1] - q[0]
##        #v1 = q[-1] - q[0]
##        #n = np.cross(v0, v1)
##        #n /= np.linalg.norm(n)
##        #normals.push_back(osg.Vec3(*n))
##
##        geometry.addPrimitiveSet(primitive)
##
##        idx +=4
##
##    sv = osgUtil.SmoothingVisitor() #to compute normals
##    sv.setCreaseAngle(0.0)
##    root.accept(sv)
##
##    print "done"
##
##    return root
##
