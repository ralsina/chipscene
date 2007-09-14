import sys, traceback

try:
    from PyQt4 import QtGui, QtCore,  QtOpenGL
except:
    print "Error loading PyQt4"
    sys.exit(1)

import chipscene as cs
try:
    import pymunk._chipmunk as cp
    import pymunk.util as cpu
    from pymunk.vec2d import vec2d
except:
    print "Error loading pymunk"
    sys.exit(1)

try:
    from Polygon import Polygon, polyStar
except:
    print "Error loading polygon. More info at http://www.dezentral.de/soft/Polygon/"
    sys.exit(1)


USEOPENGL=True


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        from Ui_main import Ui_Main
        QtGui.QMainWindow.__init__(self)
        self.scene=cs.ChipScene(rect=[0, 0, 500, 500], grav=[0, 900], dt=1.0/2000, vskip=10)
        # Set up the UI from designer
        self.ui=Ui_Main()
        self.ui.setupUi(self)
        self.ui.view.setScene(self.scene)
        self.scene.view=self.ui.view
        self.ui.view.ensureVisible(0, 0, 500, 500)
        QtCore.QObject.connect(self.ui.play, QtCore.SIGNAL("clicked()"), self.scene.start)
        if USEOPENGL:
            glw=QtOpenGL.QGLWidget()
            self.ui.view.setViewport(glw)
        self.debugColl = cp.cpCollFunc(debugColl)
        #cp.cpSpaceAddCollisionPairFunc(self.space, 0, 0, self.debugColl, None)

def fillWorld(scene):
    items=[]
    b1=cs.CPBodyItem(bpos=[50, 50],m=100)
    b2=cs.CPBodyItem(bpos=[100, 50],m=300)
    b3=cs.CPBodyItem(bpos=[150, 50],m=500)
    s1=cs.CPCircleShapeItem(20, b1, e=.5, offset=[0, 0])
    s2=cs.CPCircleShapeItem(20, b2, e=.5, offset=[0, 0])
    s3=cs.CPCircleShapeItem(20, b3, e=.5, offset=[0,0])
    p1=cs.CPSlideJoint([10, 0], [-10, 0],b1, b2, 20, 40)
    p2=cs.CPPinJoint([5, 5],[-10, 0], b2, b3)
    f1=cs.CPSegmentShapeItem([-200, 250], [400, 350], 1, None, e=.7, u=1)
    f2=cs.CPSegmentShapeItem([400, 150], [-200, 450], 1, None, e=.7, u=1)
    for i in b1, b2,b3,  s1, s2,s3,  p1, p2, f1, f2:
        scene.addItem(i)

    for x in range(1, 5):
        b=cs.CPBodyItem(bpos=[50+20*x, 10-50*x],m=1000)
        cs.CPCircleShapeItem(10, b, e=0, offset=[0, -60])
        s=cs.CPPolyShapeItem(polyStar(radius=20, nodes=4), b, e=.3, u=.5)
        QtGui.QGraphicsSimpleTextItem(str(x), s)
        items.append(b)
    for x in range(1, 10):
        items.append(cs.CPCircleShapeItem(10, None, e=.7, offset=[-120+x*95, 130]))
    for i in items:
        scene.addItem(i)

def main():
    app=QtGui.QApplication(sys.argv)
    install_handler()
    window=MainWindow()
    window.show()
    fillWorld(window.scene)
    r=app.exec_()

def debugColl(shape1, shape2, contact_points, num_contact_points, data):
    print "coll"
    return True


def my_excepthook(exc_type, exc_value, exc_traceback):
    app=QtCore.QCoreApplication.instance()
    msg = ' '.join(traceback.format_exception(exc_type,
                                                       exc_value,
                                                       exc_traceback,4))
    QtGui.QMessageBox.critical(None,
                         app.tr("Critical Error"),
                         app.tr("An unexpected Exception has occured!\n"
                                "%1").arg(msg),
                         QtGui.QMessageBox.Ok,
                         QtGui.QMessageBox.NoButton,
                         QtGui.QMessageBox.NoButton)

    # Call the default exception handler if you want
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def install_handler():
    sys.excepthook = my_excepthook

if __name__ == "__main__":
    main()
