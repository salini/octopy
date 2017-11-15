
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


_unit_quads = np.array((
 ((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)),
 ((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)),
 ((1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1)),
 ((-1, 1, -1), (-1, -1, -1), (-1, -1, 1), (-1, 1, 1)),
 ((-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)),
 ((-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))
))


def nodeToQuad(pos, dim):
    return np.array(pos) + dim * 0.5 * _unit_quads


class QuadArray:
    def __init__(self, n):
        self.idx = 0
        self.Q = np.empty((6 * n, 4, 3))

    def addQuads(self, Q):
        self.Q[self.idx:self.idx + 6, :, :] = Q
        self.idx += 6


def getAllQuads(treeRoot, dim0):
    t = time()
    n = treeRoot.getNumberOfNodes(treeRoot)
    print n
    print 'get nb nodes...', time() - t
    QA = QuadArray(n)
    fn_action = lambda pos, dim: QA.addQuads(nodeToQuad(pos, dim))
    parseTree(fn_action, treeRoot, dim0)
    return QA.Q


def trimQuads(quads):
    registeredPos = {}
    positions = np.mean(quads, 1)
    for q, p in zip(quads, positions):
        p = tuple(p)
        if p in registeredPos:
            del registeredPos[p]
        else:
            registeredPos[p] = q

    return registeredPos.values()


from time import time

def createOSGTree_flatRawQuads(treeRoot, dim0):

    def _addQuadVertices(_vertices, _quads):
        for q in _quads:
            for v in q:
                _vertices.push_back(osg.Vec3(*v))

    def _addQuadPrimitive(_geometry, _quads):
        idx = 0
        for q in _quads:
            primitive = osg.DrawElementsUInt(osg.PrimitiveSet.QUADS, 0)
            for i in range(4):
                primitive.push_back(idx + i)

            _geometry.addPrimitiveSet(primitive)
            idx += 4

    print 'get all quads...'
    t = time()
    quads = getAllQuads(treeRoot, dim0)
    print time() - t
    print 'len', len(quads)
    print 'trim quads...'
    t = time()
    quads = trimQuads(quads)
    print time() - t
    N = len(quads)
    print "len trim quad;", N
    print 'start creating OSG quads'


    root = osg.Group()
    geode = osg.Geode()
    root.addChild(geode)
    
    MAXVERT = 2**18
    INDEX = 0
    while INDEX < N:
        QUADS = quads[INDEX:INDEX+MAXVERT]
        
        geometry = osg.Geometry()
        geode.addDrawable(geometry)
        vertices = osg.Vec3Array()
        geometry.setVertexArray(vertices)

        t = time()
        _addQuadVertices(vertices, QUADS)
        print "_addQuadVertices", time() - t
        t = time()
        _addQuadPrimitive(geometry, QUADS)
        print "_addQuadPrimitive", time() - t

        INDEX += MAXVERT
        
        
    print 'smoothing...'
    t = time()
    sv = osgUtil.SmoothingVisitor()
    sv.setCreaseAngle(0.0)
    root.accept(sv)
    print time() - t

    return root

