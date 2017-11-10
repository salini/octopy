

from osgswig import osg

def createOSGGroup():
    return osg.Group()



def setMaterialColor(node, color):
    material = osg.Material()
    stateset = node.getOrCreateStateSet()
    stateset.setAttributeAndModes(material) #, osg.StateAttribute.OVERRIDE | osg.StateAttribute.ON)
    #stateset.setMode(osg.GL_LIGHTING, osg.StateAttribute.OVERRIDE | osg.StateAttribute.OFF | osg.StateAttribute.PROTECTED)

    material.setDiffuse(osg.Material.FRONT, osg.Vec4(*color))

    if color[3] < 1.0:
        stateset.setMode( osg.GL_BLEND, osg.StateAttribute.ON )
        stateset.setRenderingHint(osg.StateSet.TRANSPARENT_BIN)






def setWireframe(node):
    polygonMode = osg.PolygonMode()
    polygonMode.setMode(osg.PolygonMode.FRONT_AND_BACK, osg.PolygonMode.LINE)
    stateset = node.getOrCreateStateSet()
    stateset.setAttributeAndModes(polygonMode, osg.StateAttribute.OVERRIDE | osg.StateAttribute.ON)


