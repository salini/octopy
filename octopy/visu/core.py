
from osgswig import osg, osgViewer


def getBoxDrawable(pos, dim):
    box = osg.Box(osg.Vec3(pos[0], pos[1], pos[2]), dim, dim, dim)
    return osg.ShapeDrawable(box)

def getBoxGeode(pos, dim):
    geode = osg.Geode()
    geode.addDrawable(getBoxDrawable(pos, dim))
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


def show(root):
    viewer = getViewer()
    viewer.setSceneData(root.__disown__())
    viewer.run()
    viewer.setSceneData(None)

