

import core

import OSGOctree


def show(octree):
    root = OSGOctree.createOSGOctree(octree)
    viewer = core.getViewer()
    viewer.setSceneData(root.__disown__())
    viewer.run()
    viewer.setSceneData(None)