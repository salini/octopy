
from core import getBox

from osgswig import osg, osgUtil

import numpy as np




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