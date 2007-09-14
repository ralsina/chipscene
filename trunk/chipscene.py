import sys, traceback

try:
    from PyQt4 import QtGui, QtCore,  QtOpenGL
except:
    print "Error loading PyQt4"
    sys.exit(1)
try:
    import ctypes as ct
except:
    print "Error loading ctypes"
    sys.exit(1)
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
    
from math import *

def cpvrotate(v1, v2):
    return vec2d(v1.x*v2.x - v1.y*v2.y, v1.x*v2.y + v1.y*v2.x)
def cpvadd(v1, v2):
    return vec2d(v1.x + v2.x, v1.y + v2.y)
def cpvzero():
    return vec2d(0,0)


class ChipScene(QtGui.QGraphicsScene):
    objects=[]
    def __init__(self, parent=None, grav=[0, 900], rect=None,  dt=1.0/2000, vskip=50):
        '''A QGraphicsScene with Chipmunk physics:
            * grav is [gravx,gravy] the gravity vector of the scene (for chipmunk).

            * dt is the time delta: time step for the physics simulation.

            * vskip is "update the QGraphicsItems every vskip steps of the simulation"

            * rect is [x,y,w,h] for QGraphicsScene
        
            * parent is for QGraphicsScene
        '''
        if rect:
            QtGui.QGraphicsScene.__init__(self,rect[0],rect[1],rect[2],rect[3], parent )
        else:
            QtGui.QGraphicsScene.__init__(self,parent )

        ### Physics stuff
        cp.cpInitChipmunk()
        self.space = cp.cpSpaceNew(10)
        self.space.contents.gravity = vec2d(grav[0], grav[1])

        ### An immovile object, necessary for static shapes
        self.immovile=cp.cpBodyNew(1e100, 1e100)

        ### Timer for animation
        self.dt=dt
        self.vskip=vskip
        self.stepTimer=QtCore.QTimer(self)
        QtCore.QObject.connect(self.stepTimer, QtCore.SIGNAL("timeout()"), self.update)
        


    def addItem(self, item):
        if isinstance(item, CPShape): 
            # Shapes added directly are static shapes
            item.createShape(self.immovile, static=True)
            item.addToSpace(self.space)
            
        elif isinstance(item, CPBody): 
            # Bodies need to be added to the scene
            self.objects.append(item)
            cp.cpSpaceAddBody(self.space, item.body)
            # And so do trheir shapes
            for shape in item.shapes:
                shape.createShape(item.body)
                shape.addToSpace(self.space)
        elif isinstance(item, CPAbstractJoint):
            item.addToSpace(self.space)

        return QtGui.QGraphicsScene.addItem(self, item)

    def update(self):
        cp.cpSpaceStep(self.space, self.dt)
        if 0==self.space.contents.stamp%self.vskip:
            for obj in self.objects:
                obj.update()
                #cp.cpBodyResetForces(obj.body)
                
    def start(self):
        self.stepTimer.start(self.dt*1000)
    def endLevel(self):
        self.stepTimer.stop()

class CPBody:
    def __init__(self,_bpos=[0, 0],_bm=0,_bi=100,_bv=None, _bf=None,_ba=None,_bw=None,_bt=None):
        '''
        _bpos[x,y] is the position.
        _bm is the mass
        _bi is the moment of inertia
        _bv[x,y] is the velocity
        _bf[x,y] is the force
        _ba is the angle
        _bw is the angular velocity
        _bt is the torque
        
        You should really only set _bpos,_bm, and MAYBE _ba or _bi.
        '''
        self.shapes=[]
        
        self.body = cp.cpBodyNew(_bm, _bi)
        self._bpos = _bpos
        
        if _bv: self._bv=_bv
        if _bf: self._bf=_bf
        if _ba: self._ba=_ba
        if _bw: self._bw=_bw
        if _bt: self._bt=_bt
        
    def get_pos(self):
        return [self.body.contents.p.x,self.body.contents.p.y]
    def set_pos(self, pos):
        self.body.contents.p=apply(vec2d, pos)
    _bpos=property(get_pos, set_pos, None, "Position of the object")
    
    def get_m(self):
        return self.body.contents.m
    def set_m(self, m):
        cp.cpBodySetMass(self.body, m)
    _bm=property(get_m, set_m, None, "Mass of the object")
        
    def get_i(self):
        return self.body.contents.i
    def set_i(self, i):
        cp.cpBodySetMoment(self.body, i)
    _bi=property(get_i, set_i, None, "Moment of inertia of the object")
        
    def get_v(self):
        return [self.body.contents.v.x,self.body.contents.v.y]
    def set_v(self, v):
        self.body.contents.v=apply(vec2d, v)
    _bv=property(get_v, set_v, None, "Velocity of the object")

    def get_f(self):
        return [self.body.contents.f.x,self.body.contents.f.y]
    def set_f(self, f):
        self.body.contents.f=apply(vec2d, f)
    _bf=property(get_f, set_f, None, "Force of the object")

    def get_a(self):
        return self.body.contents.a
    def set_a(self, a):
        cp.cpBodySetAngle(self.body, a)
    _ba=property(get_a, set_a, None, "Angle of the object")
    
    def get_w(self):
        return self.body.contents.w
    def set_w(self, w):
        self.body.contents.w=w
    _bw=property(get_w, set_w, None, "Angular velocity of the object")
    
    def get_t(self):
        return self.body.contents.t
    def set_t(self, t):
        self.body.contents.t=t
    _bt=property(get_t, set_t, None, "Torque of the object")

    def applyImpulse(self, j, r):
        cp.cpBodyApplyImpulse(self.body, vec2d(j[0], j[1]) , vec2d(r[0], r[1]))

    def applyForce(self, f, r):
        cp.cpBodyApplyForce(self.body, vec2d(f[0], f[1]) , vec2d(r[0], r[1]))

class CPShape:
    '''You really should never instantiate one of these, it will fail'''
    delayed={}
    def __init__(self, body, e=.6, u=.1, offset=[0, 0], surface_v=[0, 0], collision_type=None, 
                 group=None, layers=None):
        self.body=body
        self.offset=offset
        self.added=False
        self._shape=None
        self.e=e
        self.u=u
        self.surface_v=surface_v
        if collision_type: self.collision_type=collision_type
        if group: self.group=group
        if layers: self.layers=layers

    def addToSpace(self, space):
        if self.body:
            cp.cpSpaceAddShape(space, self._shape)
        else:
            cp.cpSpaceAddStaticShape(space, self._shape)

    def recover_delayed(self):
        for n in self.delayed:
            eval ("self.set_%s(self.delayed['%s'])"%(n, n))
    def set_e(self, e):
        if self._shape: self._shape.contents.e=e
        else: self.delayed['e']=e
    def get_e(self):
        if self._shape: return self._shape.contents.e
        else: return self.delayed['e']
    e=property(get_e, set_e, None, "Elasticity of the shape")
    def set_u(self, u):
        if self._shape: self._shape.contents.u=u
        else: self.delayed['u']=u
    def get_u(self):
        if self._shape: return self._shape.contents.u
        else: return self.delayed['u']
    u=property(get_u, set_u, None, "Friction coeficient of the shape")
    def get_surface_v(self):
        if self._shape: return [self._shape.contents.surface_v.x,self._shape.contents.surface_v.y]
        else: return self.delayed['surface_v']
    def set_surface_v(self, v):
        if self._shape: self._shape.contents.surface_v=apply(vec2d, v)
        else: self.delayed['surface_v']=v
    surface_v=property(get_surface_v, set_surface_v, None, "Surface Velocity of the shape")
    def set_collision_type(self, t):
        if self._shape: self._shape.contents.collision_type=t
        else: self.delayed['collision_type']=t
    def get_collision_type(self):
        if self._shape: return self._shape.contents.collision_type
        else: return self.delayed['collision_type']
    collision_type=property(get_u, set_u, None, "Collision Type of the shape")
    
class CPBasicPolyShapeItem(QtGui.QGraphicsItem, CPShape):
    '''A basic polygon shape. The polygon needs to be convex and CCW-winding.
    Use CPPolyShapeItem instead, which is much more powerful, as soon as it stops
    being so buggy ;-)'''
    def __init__(self, poly, parent, e=.6, u=.1, offset=[0, 0], surface_v=[0, 0], 
                 collision_type=None, group=None, layers=None):
        '''poly is a list of points describing a closed convex polygon 
           [[x1,y1],[x2,y2],...,[xn,yn],[x1,y1]])'''
        if not cpu.is_clockwise(poly):
            poly.reverse()
        self.poly=poly
        if parent and isinstance(parent, CPBodyItem):
            b=parent.body
            parent.shapes.append(self)
        else:
            b=None
        CPShape.__init__(self, b, e, u, offset, surface_v, 
                               collision_type, group, layers)
        QtGui.QGraphicsItem.__init__(self, parent)
    def createShape(self, body, static=False):
        if self._shape: return
        if not static:
            cp.cpBodySetMoment(body, 10000)

        #Now, the polygon sprite will be all relative to the center
        self.qtpoly=QtGui.QPolygonF()
        for p in self.poly:
            self.qtpoly.append(QtCore.QPointF(p[0]+self.offset[0], 
                                              p[1]+self.offset[1]))
                
        #The chipmunk polygon
        p_num = len(self.poly)
        P_ARR = vec2d * p_num
        p_arr = P_ARR(vec2d(0,0))
        for i in range(p_num):
            p_arr[i].x=self.poly[i][0]
            p_arr[i].y=self.poly[i][1]

        self._shape = cp.cpPolyShapeNew(body, p_num, p_arr, vec2d(self.offset[0],self.offset[1]))
    def boundingRect(self):
        return self.qtpoly.boundingRect()        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPolygon(self.qtpoly)        
    
class CPPolyShapeItem(QtGui.QGraphicsItem, CPShape):
    '''A polygon shaped item. If the parent is a CPBodyItem, it will attach to it.
    if it's None, it will be a static shape.'''
    
    def __init__(self, poly, parent, e=.6, u=.1, offset=[0, 0], surface_v=[0, 0], 
                 collision_type=None, group=None, layers=None):
        '''poly is a Polygon object as defined by the Polygon module:
        http://www.dezentral.de/soft/Polygon/'''
        self.poly=poly
        self.tristrips=poly.triStrip()
        bb=poly.boundingBox()
        self.bb=QtCore.QRectF(bb[0]+offset[0],  bb[2]+offset[1], bb[1]-bb[0], bb[3]-bb[2])
        self._shape=None
        self.trishapes=[]
        self.qtpolys=[]
        for i in range(0, len(self.poly)):
            qp=QtGui.QPolygonF()
            for p in self.poly[i]:
                qp.append(QtCore.QPointF(p[0]+offset[0], p[1]+offset[1]))
            self.qtpolys.append(qp)
        if parent and isinstance(parent, CPBodyItem):
            b=parent.body
            parent.shapes.append(self)
        else:
            b=None
        CPShape.__init__(self, b, e, u, offset, surface_v, 
                               collision_type, group, layers)
        QtGui.QGraphicsItem.__init__(self, parent)

    def addToSpace(self, space):
        if self.body:
            for s in self.trishapes:
                cp.cpSpaceAddShape(space, s)
        else:
            for s in self.trishapes:
                cp.cpSpaceAddStaticShape(space, s)
    def createShape(self, body, static=False):
        if self._shape: return
        if not static:
            cp.cpBodySetMoment(body, 10000)
        # First, we create a chipmunk shape for each of the triangles
        # forming the polygon, and keep them.
        P_ARR = vec2d * 4
        p_arr = P_ARR(vec2d(0,0))
        self.tristrips=list(self.tristrips)
        for strip in self.tristrips:
            strip=list(strip)
            for i in range(0, len(strip)):
                strip[i]=list(strip[i])
                strip[i][0]+=self.offset[0]
                strip[i][1]+=self.offset[1]
            for i in range(0, len(strip)-2):
                p=[strip[i], strip[i+1], strip[i+2], strip[i]]
                if not cpu.is_clockwise(p):
                    p.reverse()
                for i in range(4):
                    p_arr[i].x=p[i][0]
                    p_arr[i].y=p[i][1]
                self.trishapes.append(cp.cpPolyShapeNew(body, 4, p_arr, vec2d(0, 0)))
        self.recover_delayed()
    def boundingRect(self):
        return self.bb        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for p in self.qtpolys:
            painter.drawPolygon(p)
    
class CPSegmentShapeItem(QtGui.QGraphicsItem, CPShape):
    '''A segment shaped item. If the parent is a CPBodyItem, it will attach to it.
    if it's None, it will be a static shape.'''
    def __init__(self, p1, p2, radius, parent, e=.6, u=.1, offset=[0, 0], surface_v=[0, 0], 
                 collision_type=None, group=None, layers=None):
        self.p1=p1
        self.p2=p2
        self.radius = radius
        if parent and isinstance(parent, CPBodyItem):
            b=parent.body
            parent.shapes.append(self)
        else:
            b=None
        CPShape.__init__(self, b, e, u, offset, surface_v, 
                               collision_type, group, layers)
        QtGui.QGraphicsItem.__init__(self, parent)
    def createShape(self, body, static=False):
        if self._shape: return
        if not static:
            pass
            #cp.cpBodySetMoment(body, cp.cpMomentForCircle(body.contents.m, self.radius, 0.0, cpvzero()))
        self._shape = cp.cpSegmentShapeNew(body,vec2d(self.p1[0],self.p1[1]), 
                            vec2d(self.p2[0],self.p2[1]), 
                            self.radius,vec2d(float(self.offset[0]), 
                            float(self.offset[1])))
        self.recover_delayed()
    def boundingRect(self):
        return QtCore.QRectF(self.p1[0]+self.offset[0],self.p1[1]+self.offset[1],
                   self.p2[0]-self.p1[0],self.p2[1]-self.p1[1])        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawLine(self.p1[0], self.p1[1], self.p2[0], self.p2[1] )
                         
class CPCircleShapeItem(QtGui.QGraphicsItem, CPShape):
    '''A circle shaped item. If the parent is a CPBodyItem, it will attach to it.
    if it's None, it will be a static shape.'''
    def __init__(self, radius, parent, e=.6, u=.1, offset=[0, 0], surface_v=[0, 0], 
                 collision_type=None, group=None, layers=None):
        self.radius = radius
        if parent:
            b=parent.body
            parent.shapes.append(self)
        else:
            b=None
        CPShape.__init__(self, b, e, u, offset, surface_v, 
                               collision_type, group, layers)
        QtGui.QGraphicsItem.__init__(self, parent)
    def createShape(self, body, static=False):
        if self._shape: return
        if not static:
            cp.cpBodySetMoment(body, cp.cpMomentForCircle(body.contents.m, self.radius, 0.0, cpvzero()))
        self._shape = cp.cpCircleShapeNew(body,self.radius,vec2d(float(self.offset[0]), float(self.offset[1])))
        self.recover_delayed()
    def boundingRect(self):
        return QtCore.QRectF(-self.radius+self.offset[0], -self.radius+self.offset[1],
                   self.radius*2, self.radius*2)        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawEllipse(-self.radius+self.offset[0], -self.radius+self.offset[1],
                   self.radius*2, self.radius*2)

class CPAbstractJoint:
    def addToSpace(self, space):
        cp.cpSpaceAddJoint(space, self.joint)

class CPPivotJoint(QtGui.QGraphicsItem, CPAbstractJoint):
    '''A Pivot Joint.'''
    def __init__(self, pos, b1, b2):
        '''pos is the pivot position [x,y]
           b1 and b2 are the joined bodies (should have a .body member that's a cpBody).
           '''
        self.joint=cp.cpPivotJointNew(b1.body, b2.body, vec2d(pos[0], pos[1]))
        QtGui.QGraphicsItem.__init__(self, b1)
        self.offset=[pos[0]-b1.body.contents.p.x,pos[1]-b1.body.contents.p.y ]
    def boundingRect(self):
        return QtCore.QRectF(self.offset[0]-1, self.offset[1]-1, 2, 2)        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))
        painter.drawEllipse(self.offset[0]-1, self.offset[1]-1, 2, 2)

class CPPinJoint(QtGui.QGraphicsEllipseItem, CPAbstractJoint):
    '''A Pin Joint.'''
    def __init__(self, anchor1, anchor2, b1, b2):
        '''anchor1 is the anchor in body b1, anchor2 is the anchor in body b2
           b1 and b2 are the joined bodies (should have a .body member that's a cpBody).
           '''
        self.joint=cp.cpPinJointNew(b1.body, b2.body, 
                                    vec2d(anchor1[0], anchor1[1]),
                                    vec2d(anchor2[0], anchor2[1]) )
        #Fixme this is weird, I have no idea why I need to /2
        QtGui.QGraphicsEllipseItem.__init__(self, b1 )
        self.setRect(anchor1[0]-1, anchor1[1]-1, 2, 2)
        self.setPos(anchor1[0],anchor1[1] )
        self.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))
        self.itemanchor2=QtGui.QGraphicsEllipseItem(anchor2[0]-1, anchor2[1]-1, 2, 2, b2 )
        self.itemanchor2.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))

class CPSlideJoint(QtGui.QGraphicsEllipseItem, CPAbstractJoint):
    '''A Slide Joint.'''
    def __init__(self, anchor1, anchor2, b1, b2, min, max):
        '''anchor1 is the anchor in body b1, anchor2 is the anchor in body b2
           b1 and b2 are the joined bodies (should have a .body member that's a cpBody).
           min and max are the min and max distances between the anchors.
           '''
        self.joint=cp.cpSlideJointNew(b1.body, b2.body, 
                                    vec2d(anchor1[0], anchor1[1]),
                                    vec2d(anchor2[0], anchor2[1]), min, max )
        #Fixme this is weird, I have no idea why I need to /2
        QtGui.QGraphicsEllipseItem.__init__(self, b1 )
        self.setRect(anchor1[0]-1, anchor1[1]-1, 2, 2)
        self.setPos(anchor1[0],anchor1[1] )
        self.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))
        self.itemanchor2=QtGui.QGraphicsEllipseItem(anchor2[0]-1, anchor2[1]-1, 2, 2, b2 )
        self.itemanchor2.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))
  
class CPBodyItem(QtGui.QGraphicsItem, CPBody):
    ca=0.0
    def __init__(self, bpos=[0, 0],m=0,i=0,v=None, f=None,a=None,w=None,t=None, parent=None):
        CPBody.__init__(self,bpos, m, i, v, f, a, w, t )
        QtGui.QGraphicsItem.__init__(self, parent)
        self.update()
            
    def setPos(self, pos):
        self.set_pos([pos.x(), pos.y()])
        QtGui.QGraphicsItem.setPos(self, pos)
        
    # Make it act as a simple QGraphicsItem with a small red
    # circle at the object's center
    
    def boundingRect(self):
        return QtCore.QRectF(-2, -2, 4, 4)
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0)))
        painter.drawEllipse(-2, -2, 4, 4)

    def update(self):
        '''Make the QGraphicsItem side follow the Chipmunk Object side's position and angle.
        Should only be called by ChipScene.update() but it should be harmless anyway.'''
        
        # In some cases position can become nan. Better to freeze it than to make it 
        # disappear, I guess.
        
        if self.body.contents.p.x<>self.body.contents.p.x or \
           self.body.contents.p.y<>self.body.contents.p.y or \
           self.body.contents.a<>self.body.contents.a:
               self.body.contents.p.x=self.x()
               self.body.contents.p.y=self.y()
               self.body.contents.a=self.ca
               print "Something in a cpBody became NaN"
        
        self.setPos(QtCore.QPointF(self.body.contents.p.x, self.body.contents.p.y))
        if  self.ca-self.body.contents.a and (self.body.contents.a==self.body.contents.a): # Ugly NaN protection!
            self.rotate(degrees(self.body.contents.a-self.ca))
            self.ca=float(self.body.contents.a)
