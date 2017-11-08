
from osgswig import osg, osgViewer


def getBox(pos, dim):
    box = osg.Box(osg.Vec3(pos[0], pos[1], pos[2]), dim[0], dim[1], dim[2])
    boxDrawable = osg.ShapeDrawable(box)
    geode = osg.Geode()
    geode.addDrawable(boxDrawable)
    return geode


def getViewer(x=50,y=50,w=800,h=600):
    viewer = osgViewer.Viewer()
    viewer.setThreadingModel(osgViewer.Viewer.ThreadPerContext)
    viewer.addEventHandler(osgViewer.StatsHandler())
    viewer.addEventHandler(osgViewer.WindowSizeHandler())
    viewer.addEventHandler(osgViewer.ThreadingHandler())
    viewer.addEventHandler(osgViewer.HelpHandler())
    viewer.setUpViewInWindow(x,y,w,h)
    return viewer




