from ctypes import *
### Modified code
from ctypes.util import find_library
import vec2d
cpVect = vec2d.vec2d

#TODO: Make the loading code better and figure out what works on *nix/macosx
lib_path = find_library("ChipmunkPyEd")
if lib_path is None:
    print "find_library could not find ChipmunkPyEd"
    try:
        print "Will try to load ChipmunkPyEd.dll"
        chiplib = CDLL('pymunk/ChipmunkPyEd.dll')
        print "ChipmunkPyEd.dll loaded"
    except:
        try:
            print "Loading ChipmunkPyEd.dll failed, will try to load libChipmunkPyEd.so"
            chiplib = CDLL('pymunk/libChipmunkPyEd.so')
            print 'libChipmunkPyEd.so loaded'
        except:
            print "Loading libChipmunkPyEd.so failed, will try with libChipmunkPyEd.dylib"
            chiplib = CDLL('pymunk/libChipmunkPyEd.dylib')
            print "libChipmunkPyEd.dylib loaded"
else:
    chiplib = CDLL(lib_path)    
_libraries = {}
_libraries['ChipmunkPyEd.dll'] = chiplib

### Modified code
STRING = c_char_p

CP_SEGMENT_SHAPE = 1
CP_NUM_SHAPES = 3
CP_CIRCLE_SHAPE = 0
# def CP_HASH_PAIR(A,B): return ((unsigned long)(A)*CP_HASH_COEF ^ (unsigned long)(B)*CP_HASH_COEF) # macro
CP_POLY_SHAPE = 2
CP_HASH_COEF = 3344921057L # Variable c_ulong
M_PI = 3.1415926500000002 # Variable c_double
cpFloat = c_float
cpInitChipmunk = _libraries['ChipmunkPyEd.dll'].cpInitChipmunk
cpInitChipmunk.restype = None
cpInitChipmunk.argtypes = []
#class cpVect(Structure):
    #def __add__(self, other):
    #    return cpVect(self.x+ other.x, self.y + other.y)
#    pass
cpMomentForCircle = _libraries['ChipmunkPyEd.dll'].cpMomentForCircle
cpMomentForCircle.restype = cpFloat
cpMomentForCircle.argtypes = [cpFloat, cpFloat, cpFloat, cpVect]
cpMomentForPoly = _libraries['ChipmunkPyEd.dll'].cpMomentForPoly
cpMomentForPoly.restype = cpFloat
cpMomentForPoly.argtypes = [cpFloat, c_int, POINTER(cpVect), cpVect]
class cpContact(Structure):
    pass
#cpVect._fields_ = [
#    ('x', cpFloat),
#    ('y', cpFloat),
#]
cpContact._fields_ = [
    ('p', cpVect),
    ('n', cpVect),
    ('dist', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('nMass', cpFloat),
    ('tMass', cpFloat),
    ('bounce', cpFloat),
    ('jnAcc', cpFloat),
    ('jtAcc', cpFloat),
    ('jBias', cpFloat),
    ('bias', cpFloat),
    ('hash', c_ulong),
]
cpContactInit = _libraries['ChipmunkPyEd.dll'].cpContactInit
cpContactInit.restype = POINTER(cpContact)
cpContactInit.argtypes = [POINTER(cpContact), cpVect, cpVect, cpFloat, c_uint]
cpContactsSumImpulses = _libraries['ChipmunkPyEd.dll'].cpContactsSumImpulses
cpContactsSumImpulses.restype = cpVect
cpContactsSumImpulses.argtypes = [POINTER(cpContact), c_int]
cpContactsSumImpulsesWithFriction = _libraries['ChipmunkPyEd.dll'].cpContactsSumImpulsesWithFriction
cpContactsSumImpulsesWithFriction.restype = cpVect
cpContactsSumImpulsesWithFriction.argtypes = [POINTER(cpContact), c_int]
class cpArbiter(Structure):
    pass
class cpShape(Structure):
    pass
cpArbiter._fields_ = [
    ('numContacts', c_int),
    ('contacts', POINTER(cpContact)),
    ('a', POINTER(cpShape)),
    ('b', POINTER(cpShape)),
    ('u', cpFloat),
    ('e', cpFloat),
    ('target_v', cpVect),
    ('stamp', c_int),
]
cpArbiterAlloc = _libraries['ChipmunkPyEd.dll'].cpArbiterAlloc
cpArbiterAlloc.restype = POINTER(cpArbiter)
cpArbiterAlloc.argtypes = []
cpArbiterInit = _libraries['ChipmunkPyEd.dll'].cpArbiterInit
cpArbiterInit.restype = POINTER(cpArbiter)
cpArbiterInit.argtypes = [POINTER(cpArbiter), POINTER(cpShape), POINTER(cpShape), c_int]
cpArbiterNew = _libraries['ChipmunkPyEd.dll'].cpArbiterNew
cpArbiterNew.restype = POINTER(cpArbiter)
cpArbiterNew.argtypes = [POINTER(cpShape), POINTER(cpShape), c_int]
cpArbiterDestroy = _libraries['ChipmunkPyEd.dll'].cpArbiterDestroy
cpArbiterDestroy.restype = None
cpArbiterDestroy.argtypes = [POINTER(cpArbiter)]
cpArbiterFree = _libraries['ChipmunkPyEd.dll'].cpArbiterFree
cpArbiterFree.restype = None
cpArbiterFree.argtypes = [POINTER(cpArbiter)]
cpArbiterInject = _libraries['ChipmunkPyEd.dll'].cpArbiterInject
cpArbiterInject.restype = None
cpArbiterInject.argtypes = [POINTER(cpArbiter), POINTER(cpContact), c_int]
cpArbiterPreStep = _libraries['ChipmunkPyEd.dll'].cpArbiterPreStep
cpArbiterPreStep.restype = None
cpArbiterPreStep.argtypes = [POINTER(cpArbiter), cpFloat]
cpArbiterApplyImpulse = _libraries['ChipmunkPyEd.dll'].cpArbiterApplyImpulse
cpArbiterApplyImpulse.restype = None
cpArbiterApplyImpulse.argtypes = [POINTER(cpArbiter)]
class cpArray(Structure):
    pass
cpArray._fields_ = [
    ('num', c_int),
    ('max', c_int),
    ('arr', POINTER(c_void_p)),
]
cpArrayIter = CFUNCTYPE(None, c_void_p, c_void_p)
cpArrayAlloc = _libraries['ChipmunkPyEd.dll'].cpArrayAlloc
cpArrayAlloc.restype = POINTER(cpArray)
cpArrayAlloc.argtypes = []
cpArrayInit = _libraries['ChipmunkPyEd.dll'].cpArrayInit
cpArrayInit.restype = POINTER(cpArray)
cpArrayInit.argtypes = [POINTER(cpArray), c_int]
cpArrayNew = _libraries['ChipmunkPyEd.dll'].cpArrayNew
cpArrayNew.restype = POINTER(cpArray)
cpArrayNew.argtypes = [c_int]
cpArrayDestroy = _libraries['ChipmunkPyEd.dll'].cpArrayDestroy
cpArrayDestroy.restype = None
cpArrayDestroy.argtypes = [POINTER(cpArray)]
cpArrayFree = _libraries['ChipmunkPyEd.dll'].cpArrayFree
cpArrayFree.restype = None
cpArrayFree.argtypes = [POINTER(cpArray)]
cpArrayPush = _libraries['ChipmunkPyEd.dll'].cpArrayPush
cpArrayPush.restype = None
cpArrayPush.argtypes = [POINTER(cpArray), c_void_p]
cpArrayDeleteIndex = _libraries['ChipmunkPyEd.dll'].cpArrayDeleteIndex
cpArrayDeleteIndex.restype = None
cpArrayDeleteIndex.argtypes = [POINTER(cpArray), c_int]
cpArrayDeleteObj = _libraries['ChipmunkPyEd.dll'].cpArrayDeleteObj
cpArrayDeleteObj.restype = None
cpArrayDeleteObj.argtypes = [POINTER(cpArray), c_void_p]
cpArrayEach = _libraries['ChipmunkPyEd.dll'].cpArrayEach
cpArrayEach.restype = None
cpArrayEach.argtypes = [POINTER(cpArray), cpArrayIter, c_void_p]
cpArrayContains = _libraries['ChipmunkPyEd.dll'].cpArrayContains
cpArrayContains.restype = c_int
cpArrayContains.argtypes = [POINTER(cpArray), c_void_p]
class cpBB(Structure):
    pass
cpBB._fields_ = [
    ('l', cpFloat),
    ('b', cpFloat),
    ('r', cpFloat),
    ('t', cpFloat),
]
cpBBClampVect = _libraries['ChipmunkPyEd.dll'].cpBBClampVect
cpBBClampVect.restype = cpVect
cpBBClampVect.argtypes = [cpBB, cpVect]
cpBBWrapVect = _libraries['ChipmunkPyEd.dll'].cpBBWrapVect
cpBBWrapVect.restype = cpVect
cpBBWrapVect.argtypes = [cpBB, cpVect]
class cpBody(Structure):
    pass
cpBody._fields_ = [
    ('m', cpFloat),
    ('m_inv', cpFloat),
    ('i', cpFloat),
    ('i_inv', cpFloat),
    ('p', cpVect),
    ('v', cpVect),
    ('f', cpVect),
    ('v_bias', cpVect),
    ('a', cpFloat),
    ('w', cpFloat),
    ('t', cpFloat),
    ('w_bias', cpFloat),
    ('rot', cpVect),
]
cpBodyAlloc = _libraries['ChipmunkPyEd.dll'].cpBodyAlloc
cpBodyAlloc.restype = POINTER(cpBody)
cpBodyAlloc.argtypes = []
cpBodyInit = _libraries['ChipmunkPyEd.dll'].cpBodyInit
cpBodyInit.restype = POINTER(cpBody)
cpBodyInit.argtypes = [POINTER(cpBody), cpFloat, cpFloat]
cpBodyNew = _libraries['ChipmunkPyEd.dll'].cpBodyNew
cpBodyNew.restype = POINTER(cpBody)
cpBodyNew.argtypes = [cpFloat, cpFloat]
cpBodyDestroy = _libraries['ChipmunkPyEd.dll'].cpBodyDestroy
cpBodyDestroy.restype = None
cpBodyDestroy.argtypes = [POINTER(cpBody)]
cpBodyFree = _libraries['ChipmunkPyEd.dll'].cpBodyFree
cpBodyFree.restype = None
cpBodyFree.argtypes = [POINTER(cpBody)]
cpBodySetMass = _libraries['ChipmunkPyEd.dll'].cpBodySetMass
cpBodySetMass.restype = None
cpBodySetMass.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetMoment = _libraries['ChipmunkPyEd.dll'].cpBodySetMoment
cpBodySetMoment.restype = None
cpBodySetMoment.argtypes = [POINTER(cpBody), cpFloat]
cpBodySetAngle = _libraries['ChipmunkPyEd.dll'].cpBodySetAngle
cpBodySetAngle.restype = None
cpBodySetAngle.argtypes = [POINTER(cpBody), cpFloat]
cpBodySlew = _libraries['ChipmunkPyEd.dll'].cpBodySlew
cpBodySlew.restype = None
cpBodySlew.argtypes = [POINTER(cpBody), cpVect, cpFloat]
cpBodyUpdateVelocity = _libraries['ChipmunkPyEd.dll'].cpBodyUpdateVelocity
cpBodyUpdateVelocity.restype = None
cpBodyUpdateVelocity.argtypes = [POINTER(cpBody), cpVect, cpFloat, cpFloat]
cpBodyUpdatePosition = _libraries['ChipmunkPyEd.dll'].cpBodyUpdatePosition
cpBodyUpdatePosition.restype = None
cpBodyUpdatePosition.argtypes = [POINTER(cpBody), cpFloat]
cpBodyResetForces = _libraries['ChipmunkPyEd.dll'].cpBodyResetForces
cpBodyResetForces.restype = None
cpBodyResetForces.argtypes = [POINTER(cpBody)]
cpBodyApplyForce = _libraries['ChipmunkPyEd.dll'].cpBodyApplyForce
cpBodyApplyForce.restype = None
cpBodyApplyForce.argtypes = [POINTER(cpBody), cpVect, cpVect]
cpDampedSpring = _libraries['ChipmunkPyEd.dll'].cpDampedSpring
cpDampedSpring.restype = None
cpDampedSpring.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat, cpFloat, cpFloat]
cpCollideShapes = _libraries['ChipmunkPyEd.dll'].cpCollideShapes
cpCollideShapes.restype = c_int
cpCollideShapes.argtypes = [POINTER(cpShape), POINTER(cpShape), POINTER(POINTER(cpContact))]
class cpHashSetBin(Structure):
    pass
cpHashSetBin._fields_ = [
    ('elt', c_void_p),
    ('hash', c_ulong),
    ('next', POINTER(cpHashSetBin)),
]
cpHashSetEqlFunc = CFUNCTYPE(c_int, c_void_p, c_void_p)
cpHashSetTransFunc = CFUNCTYPE(c_void_p, c_void_p, c_void_p)
cpHashSetIterFunc = CFUNCTYPE(None, c_void_p, c_void_p)
cpHashSetRejectFunc = CFUNCTYPE(c_int, c_void_p, c_void_p)
class cpHashSet(Structure):
    pass
cpHashSet._fields_ = [
    ('entries', c_int),
    ('size', c_int),
    ('eql', cpHashSetEqlFunc),
    ('trans', cpHashSetTransFunc),
    ('default_value', c_void_p),
    ('table', POINTER(POINTER(cpHashSetBin))),
]
cpHashSetDestroy = _libraries['ChipmunkPyEd.dll'].cpHashSetDestroy
cpHashSetDestroy.restype = None
cpHashSetDestroy.argtypes = [POINTER(cpHashSet)]
cpHashSetFree = _libraries['ChipmunkPyEd.dll'].cpHashSetFree
cpHashSetFree.restype = None
cpHashSetFree.argtypes = [POINTER(cpHashSet)]
cpHashSetAlloc = _libraries['ChipmunkPyEd.dll'].cpHashSetAlloc
cpHashSetAlloc.restype = POINTER(cpHashSet)
cpHashSetAlloc.argtypes = []
cpHashSetInit = _libraries['ChipmunkPyEd.dll'].cpHashSetInit
cpHashSetInit.restype = POINTER(cpHashSet)
cpHashSetInit.argtypes = [POINTER(cpHashSet), c_int, cpHashSetEqlFunc, cpHashSetTransFunc]
cpHashSetNew = _libraries['ChipmunkPyEd.dll'].cpHashSetNew
cpHashSetNew.restype = POINTER(cpHashSet)
cpHashSetNew.argtypes = [c_int, cpHashSetEqlFunc, cpHashSetTransFunc]
cpHashSetInsert = _libraries['ChipmunkPyEd.dll'].cpHashSetInsert
cpHashSetInsert.restype = c_void_p
cpHashSetInsert.argtypes = [POINTER(cpHashSet), c_ulong, c_void_p, c_void_p]
cpHashSetRemove = _libraries['ChipmunkPyEd.dll'].cpHashSetRemove
cpHashSetRemove.restype = c_void_p
cpHashSetRemove.argtypes = [POINTER(cpHashSet), c_ulong, c_void_p]
cpHashSetFind = _libraries['ChipmunkPyEd.dll'].cpHashSetFind
cpHashSetFind.restype = c_void_p
cpHashSetFind.argtypes = [POINTER(cpHashSet), c_ulong, c_void_p]
cpHashSetEach = _libraries['ChipmunkPyEd.dll'].cpHashSetEach
cpHashSetEach.restype = None
cpHashSetEach.argtypes = [POINTER(cpHashSet), cpHashSetIterFunc, c_void_p]
cpHashSetReject = _libraries['ChipmunkPyEd.dll'].cpHashSetReject
cpHashSetReject.restype = None
cpHashSetReject.argtypes = [POINTER(cpHashSet), cpHashSetRejectFunc, c_void_p]
class cpJoint(Structure):
    pass
cpJoint._fields_ = [
    ('a', POINTER(cpBody)),
    ('b', POINTER(cpBody)),
    ('preStep', CFUNCTYPE(None, POINTER(cpJoint), c_float)),
    ('applyImpulse', CFUNCTYPE(None, POINTER(cpJoint))),
]
cpJointDestroy = _libraries['ChipmunkPyEd.dll'].cpJointDestroy
cpJointDestroy.restype = None
cpJointDestroy.argtypes = [POINTER(cpJoint)]
cpJointFree = _libraries['ChipmunkPyEd.dll'].cpJointFree
cpJointFree.restype = None
cpJointFree.argtypes = [POINTER(cpJoint)]
class cpPinJoint(Structure):
    pass
cpPinJoint._fields_ = [
    ('joint', cpJoint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('dist', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('n', cpVect),
    ('nMass', cpFloat),
    ('jnAcc', cpFloat),
    ('jBias', cpFloat),
    ('bias', cpFloat),
]
cpPinJointAlloc = _libraries['ChipmunkPyEd.dll'].cpPinJointAlloc
cpPinJointAlloc.restype = POINTER(cpPinJoint)
cpPinJointAlloc.argtypes = []
cpPinJointInit = _libraries['ChipmunkPyEd.dll'].cpPinJointInit
cpPinJointInit.restype = POINTER(cpPinJoint)
cpPinJointInit.argtypes = [POINTER(cpPinJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
cpPinJointNew = _libraries['ChipmunkPyEd.dll'].cpPinJointNew
cpPinJointNew.restype = POINTER(cpJoint)
cpPinJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect]
class cpSlideJoint(Structure):
    pass
cpSlideJoint._fields_ = [
    ('joint', cpJoint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('min', cpFloat),
    ('max', cpFloat),
    ('r1', cpVect),
    ('r2', cpVect),
    ('n', cpVect),
    ('nMass', cpFloat),
    ('jnAcc', cpFloat),
    ('jBias', cpFloat),
    ('bias', cpFloat),
]
cpSlideJointAlloc = _libraries['ChipmunkPyEd.dll'].cpSlideJointAlloc
cpSlideJointAlloc.restype = POINTER(cpSlideJoint)
cpSlideJointAlloc.argtypes = []
cpSlideJointInit = _libraries['ChipmunkPyEd.dll'].cpSlideJointInit
cpSlideJointInit.restype = POINTER(cpSlideJoint)
cpSlideJointInit.argtypes = [POINTER(cpSlideJoint), POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
cpSlideJointNew = _libraries['ChipmunkPyEd.dll'].cpSlideJointNew
cpSlideJointNew.restype = POINTER(cpJoint)
cpSlideJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect, cpVect, cpFloat, cpFloat]
class cpPivotJoint(Structure):
    pass
cpPivotJoint._fields_ = [
    ('joint', cpJoint),
    ('anchr1', cpVect),
    ('anchr2', cpVect),
    ('r1', cpVect),
    ('r2', cpVect),
    ('k1', cpVect),
    ('k2', cpVect),
    ('jAcc', cpVect),
    ('jBias', cpVect),
    ('bias', cpVect),
]
cpPivotJointAlloc = _libraries['ChipmunkPyEd.dll'].cpPivotJointAlloc
cpPivotJointAlloc.restype = POINTER(cpPivotJoint)
cpPivotJointAlloc.argtypes = []
cpPivotJointInit = _libraries['ChipmunkPyEd.dll'].cpPivotJointInit
cpPivotJointInit.restype = POINTER(cpPivotJoint)
cpPivotJointInit.argtypes = [POINTER(cpPivotJoint), POINTER(cpBody), POINTER(cpBody), cpVect]
cpPivotJointNew = _libraries['ChipmunkPyEd.dll'].cpPivotJointNew
cpPivotJointNew.restype = POINTER(cpJoint)
cpPivotJointNew.argtypes = [POINTER(cpBody), POINTER(cpBody), cpVect]
class cpPolyShapeAxis(Structure):
    pass
cpPolyShapeAxis._fields_ = [
    ('n', cpVect),
    ('d', cpFloat),
]
class cpPolyShape(Structure):
    pass

# values for enumeration 'cpShapeType'
cpShapeType = c_int # enum
cpShape._fields_ = [
    ('type', cpShapeType),
    ('cacheData', CFUNCTYPE(cpBB, POINTER(cpShape), cpVect, cpVect)),
    ('destroy', CFUNCTYPE(None, POINTER(cpShape))),
    ('id', c_ulong),
    ('bb', cpBB),
    ('collision_type', c_ulong),
    ('group', c_ulong),
    ('layers', c_ulong),
    ('data', c_void_p),
    ('body', POINTER(cpBody)),
    ('e', cpFloat),
    ('u', cpFloat),
    ('surface_v', cpVect),
]
cpPolyShape._fields_ = [
    ('shape', cpShape),
    ('numVerts', c_int),
    ('verts', POINTER(cpVect)),
    ('axes', POINTER(cpPolyShapeAxis)),
    ('tVerts', POINTER(cpVect)),
    ('tAxes', POINTER(cpPolyShapeAxis)),
]
cpPolyShapeAlloc = _libraries['ChipmunkPyEd.dll'].cpPolyShapeAlloc
cpPolyShapeAlloc.restype = POINTER(cpPolyShape)
cpPolyShapeAlloc.argtypes = []
cpPolyShapeInit = _libraries['ChipmunkPyEd.dll'].cpPolyShapeInit
cpPolyShapeInit.restype = POINTER(cpPolyShape)
cpPolyShapeInit.argtypes = [POINTER(cpPolyShape), POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpPolyShapeNew = _libraries['ChipmunkPyEd.dll'].cpPolyShapeNew
cpPolyShapeNew.restype = POINTER(cpShape)
cpPolyShapeNew.argtypes = [POINTER(cpBody), c_int, POINTER(cpVect), cpVect]
cpPolyShapeValueOnAxis = _libraries['ChipmunkPyEd.dll'].cpPolyShapeValueOnAxis
cpPolyShapeValueOnAxis.restype = cpFloat
cpPolyShapeValueOnAxis.argtypes = [POINTER(cpPolyShape), cpVect, cpFloat]
cpPolyShapeContainsVert = _libraries['ChipmunkPyEd.dll'].cpPolyShapeContainsVert
cpPolyShapeContainsVert.restype = c_int
cpPolyShapeContainsVert.argtypes = [POINTER(cpPolyShape), cpVect]
cpResetShapeIdCounter = _libraries['ChipmunkPyEd.dll'].cpResetShapeIdCounter
cpResetShapeIdCounter.restype = None
cpResetShapeIdCounter.argtypes = []
cpShapeInit = _libraries['ChipmunkPyEd.dll'].cpShapeInit
cpShapeInit.restype = POINTER(cpShape)
cpShapeInit.argtypes = [POINTER(cpShape), cpShapeType, POINTER(cpBody)]
cpShapeDestroy = _libraries['ChipmunkPyEd.dll'].cpShapeDestroy
cpShapeDestroy.restype = None
cpShapeDestroy.argtypes = [POINTER(cpShape)]
cpShapeFree = _libraries['ChipmunkPyEd.dll'].cpShapeFree
cpShapeFree.restype = None
cpShapeFree.argtypes = [POINTER(cpShape)]
cpShapeCacheBB = _libraries['ChipmunkPyEd.dll'].cpShapeCacheBB
cpShapeCacheBB.restype = cpBB
cpShapeCacheBB.argtypes = [POINTER(cpShape)]
class cpCircleShape(Structure):
    pass
cpCircleShape._fields_ = [
    ('shape', cpShape),
    ('c', cpVect),
    ('r', cpFloat),
    ('tc', cpVect),
]
cpCircleShapeAlloc = _libraries['ChipmunkPyEd.dll'].cpCircleShapeAlloc
cpCircleShapeAlloc.restype = POINTER(cpCircleShape)
cpCircleShapeAlloc.argtypes = []
cpCircleShapeInit = _libraries['ChipmunkPyEd.dll'].cpCircleShapeInit
cpCircleShapeInit.restype = POINTER(cpCircleShape)
cpCircleShapeInit.argtypes = [POINTER(cpCircleShape), POINTER(cpBody), cpFloat, cpVect]
cpCircleShapeNew = _libraries['ChipmunkPyEd.dll'].cpCircleShapeNew
cpCircleShapeNew.restype = POINTER(cpShape)
cpCircleShapeNew.argtypes = [POINTER(cpBody), cpFloat, cpVect]
class cpSegmentShape(Structure):
    pass
cpSegmentShape._fields_ = [
    ('shape', cpShape),
    ('a', cpVect),
    ('b', cpVect),
    ('n', cpVect),
    ('r', cpFloat),
    ('ta', cpVect),
    ('tb', cpVect),
    ('tn', cpVect),
]
cpSegmentShapeAlloc = _libraries['ChipmunkPyEd.dll'].cpSegmentShapeAlloc
cpSegmentShapeAlloc.restype = POINTER(cpSegmentShape)
cpSegmentShapeAlloc.argtypes = []
cpSegmentShapeInit = _libraries['ChipmunkPyEd.dll'].cpSegmentShapeInit
cpSegmentShapeInit.restype = POINTER(cpSegmentShape)
cpSegmentShapeInit.argtypes = [POINTER(cpSegmentShape), POINTER(cpBody), cpVect, cpVect, cpFloat]
cpSegmentShapeNew = _libraries['ChipmunkPyEd.dll'].cpSegmentShapeNew
cpSegmentShapeNew.restype = POINTER(cpShape)
cpSegmentShapeNew.argtypes = [POINTER(cpBody), cpVect, cpVect, cpFloat]
cpCollFunc = CFUNCTYPE(c_int, POINTER(cpShape), POINTER(cpShape), POINTER(cpContact), c_int, c_void_p)
class cpCollPairFunc(Structure):
    pass
cpCollPairFunc._fields_ = [
    ('a', c_ulong),
    ('b', c_ulong),
    ('func', cpCollFunc),
    ('data', c_void_p),
]
class cpSpace(Structure):
    pass
class cpSpaceHash(Structure):
    pass
cpSpace._fields_ = [
    ('iterations', c_int),
    ('gravity', cpVect),
    ('damping', cpFloat),
    ('stamp', c_int),
    ('staticShapes', POINTER(cpSpaceHash)),
    ('activeShapes', POINTER(cpSpaceHash)),
    ('bodies', POINTER(cpArray)),
    ('arbiters', POINTER(cpArray)),
    ('contactSet', POINTER(cpHashSet)),
    ('joints', POINTER(cpArray)),
    ('collFuncSet', POINTER(cpHashSet)),
    ('defaultPairFunc', cpCollPairFunc),
]
cpSpaceAlloc = _libraries['ChipmunkPyEd.dll'].cpSpaceAlloc
cpSpaceAlloc.restype = POINTER(cpSpace)
cpSpaceAlloc.argtypes = []
cpSpaceInit = _libraries['ChipmunkPyEd.dll'].cpSpaceInit
cpSpaceInit.restype = POINTER(cpSpace)
cpSpaceInit.argtypes = [POINTER(cpSpace)]
cpSpaceNew = _libraries['ChipmunkPyEd.dll'].cpSpaceNew
cpSpaceNew.restype = POINTER(cpSpace)
cpSpaceNew.argtypes = []
cpSpaceDestroy = _libraries['ChipmunkPyEd.dll'].cpSpaceDestroy
cpSpaceDestroy.restype = None
cpSpaceDestroy.argtypes = [POINTER(cpSpace)]
cpSpaceFree = _libraries['ChipmunkPyEd.dll'].cpSpaceFree
cpSpaceFree.restype = None
cpSpaceFree.argtypes = [POINTER(cpSpace)]
cpSpaceFreeChildren = _libraries['ChipmunkPyEd.dll'].cpSpaceFreeChildren
cpSpaceFreeChildren.restype = None
cpSpaceFreeChildren.argtypes = [POINTER(cpSpace)]
cpSpaceAddCollisionPairFunc = _libraries['ChipmunkPyEd.dll'].cpSpaceAddCollisionPairFunc
cpSpaceAddCollisionPairFunc.restype = None
cpSpaceAddCollisionPairFunc.argtypes = [POINTER(cpSpace), c_ulong, c_ulong, cpCollFunc, c_void_p]
cpSpaceRemoveCollisionPairFunc = _libraries['ChipmunkPyEd.dll'].cpSpaceRemoveCollisionPairFunc
cpSpaceRemoveCollisionPairFunc.restype = None
cpSpaceRemoveCollisionPairFunc.argtypes = [POINTER(cpSpace), c_ulong, c_ulong]
cpSpaceSetDefaultCollisionPairFunc = _libraries['ChipmunkPyEd.dll'].cpSpaceSetDefaultCollisionPairFunc
cpSpaceSetDefaultCollisionPairFunc.restype = None
cpSpaceSetDefaultCollisionPairFunc.argtypes = [POINTER(cpSpace), cpCollFunc, c_void_p]
cpSpaceAddShape = _libraries['ChipmunkPyEd.dll'].cpSpaceAddShape
cpSpaceAddShape.restype = None
cpSpaceAddShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddStaticShape = _libraries['ChipmunkPyEd.dll'].cpSpaceAddStaticShape
cpSpaceAddStaticShape.restype = None
cpSpaceAddStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceAddBody = _libraries['ChipmunkPyEd.dll'].cpSpaceAddBody
cpSpaceAddBody.restype = None
cpSpaceAddBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceAddJoint = _libraries['ChipmunkPyEd.dll'].cpSpaceAddJoint
cpSpaceAddJoint.restype = None
cpSpaceAddJoint.argtypes = [POINTER(cpSpace), POINTER(cpJoint)]
cpSpaceRemoveShape = _libraries['ChipmunkPyEd.dll'].cpSpaceRemoveShape
cpSpaceRemoveShape.restype = None
cpSpaceRemoveShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveStaticShape = _libraries['ChipmunkPyEd.dll'].cpSpaceRemoveStaticShape
cpSpaceRemoveStaticShape.restype = None
cpSpaceRemoveStaticShape.argtypes = [POINTER(cpSpace), POINTER(cpShape)]
cpSpaceRemoveBody = _libraries['ChipmunkPyEd.dll'].cpSpaceRemoveBody
cpSpaceRemoveBody.restype = None
cpSpaceRemoveBody.argtypes = [POINTER(cpSpace), POINTER(cpBody)]
cpSpaceRemoveJoint = _libraries['ChipmunkPyEd.dll'].cpSpaceRemoveJoint
cpSpaceRemoveJoint.restype = None
cpSpaceRemoveJoint.argtypes = [POINTER(cpSpace), POINTER(cpJoint)]
cpSpaceBodyIterator = CFUNCTYPE(None, POINTER(cpBody), c_void_p)
cpSpaceEachBody = _libraries['ChipmunkPyEd.dll'].cpSpaceEachBody
cpSpaceEachBody.restype = None
cpSpaceEachBody.argtypes = [POINTER(cpSpace), cpSpaceBodyIterator, c_void_p]
cpSpaceResizeStaticHash = _libraries['ChipmunkPyEd.dll'].cpSpaceResizeStaticHash
cpSpaceResizeStaticHash.restype = None
cpSpaceResizeStaticHash.argtypes = [POINTER(cpSpace), cpFloat, c_int]
cpSpaceResizeActiveHash = _libraries['ChipmunkPyEd.dll'].cpSpaceResizeActiveHash
cpSpaceResizeActiveHash.restype = None
cpSpaceResizeActiveHash.argtypes = [POINTER(cpSpace), cpFloat, c_int]
cpSpaceRehashStatic = _libraries['ChipmunkPyEd.dll'].cpSpaceRehashStatic
cpSpaceRehashStatic.restype = None
cpSpaceRehashStatic.argtypes = [POINTER(cpSpace)]
cpSpaceStep = _libraries['ChipmunkPyEd.dll'].cpSpaceStep
cpSpaceStep.restype = None
cpSpaceStep.argtypes = [POINTER(cpSpace), cpFloat]
class cpHandle(Structure):
    pass
cpHandle._fields_ = [
    ('obj', c_void_p),
    ('retain', c_int),
    ('stamp', c_int),
]
class cpSpaceHashBin(Structure):
    pass
cpSpaceHashBin._fields_ = [
    ('handle', POINTER(cpHandle)),
    ('next', POINTER(cpSpaceHashBin)),
]
cpSpaceHashBBFunc = CFUNCTYPE(cpBB, c_void_p)
cpSpaceHash._fields_ = [
    ('numcells', c_int),
    ('celldim', cpFloat),
    ('bbfunc', cpSpaceHashBBFunc),
    ('handleSet', POINTER(cpHashSet)),
    ('table', POINTER(POINTER(cpSpaceHashBin))),
    ('bins', POINTER(cpSpaceHashBin)),
    ('stamp', c_int),
]
cpSpaceHashAlloc = _libraries['ChipmunkPyEd.dll'].cpSpaceHashAlloc
cpSpaceHashAlloc.restype = POINTER(cpSpaceHash)
cpSpaceHashAlloc.argtypes = []
cpSpaceHashInit = _libraries['ChipmunkPyEd.dll'].cpSpaceHashInit
cpSpaceHashInit.restype = POINTER(cpSpaceHash)
cpSpaceHashInit.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int, cpSpaceHashBBFunc]
cpSpaceHashNew = _libraries['ChipmunkPyEd.dll'].cpSpaceHashNew
cpSpaceHashNew.restype = POINTER(cpSpaceHash)
cpSpaceHashNew.argtypes = [cpFloat, c_int, cpSpaceHashBBFunc]
cpSpaceHashDestroy = _libraries['ChipmunkPyEd.dll'].cpSpaceHashDestroy
cpSpaceHashDestroy.restype = None
cpSpaceHashDestroy.argtypes = [POINTER(cpSpaceHash)]
cpSpaceHashFree = _libraries['ChipmunkPyEd.dll'].cpSpaceHashFree
cpSpaceHashFree.restype = None
cpSpaceHashFree.argtypes = [POINTER(cpSpaceHash)]
cpSpaceHashResize = _libraries['ChipmunkPyEd.dll'].cpSpaceHashResize
cpSpaceHashResize.restype = None
cpSpaceHashResize.argtypes = [POINTER(cpSpaceHash), cpFloat, c_int]
cpSpaceHashInsert = _libraries['ChipmunkPyEd.dll'].cpSpaceHashInsert
cpSpaceHashInsert.restype = None
cpSpaceHashInsert.argtypes = [POINTER(cpSpaceHash), c_void_p, c_ulong, cpBB]
cpSpaceHashRemove = _libraries['ChipmunkPyEd.dll'].cpSpaceHashRemove
cpSpaceHashRemove.restype = None
cpSpaceHashRemove.argtypes = [POINTER(cpSpaceHash), c_void_p, c_ulong]
cpSpaceHashIterator = CFUNCTYPE(None, c_void_p, c_void_p)
cpSpaceHashEach = _libraries['ChipmunkPyEd.dll'].cpSpaceHashEach
cpSpaceHashEach.restype = None
cpSpaceHashEach.argtypes = [POINTER(cpSpaceHash), cpSpaceHashIterator, c_void_p]
cpSpaceHashRehash = _libraries['ChipmunkPyEd.dll'].cpSpaceHashRehash
cpSpaceHashRehash.restype = None
cpSpaceHashRehash.argtypes = [POINTER(cpSpaceHash)]
cpSpaceHashRehashObject = _libraries['ChipmunkPyEd.dll'].cpSpaceHashRehashObject
cpSpaceHashRehashObject.restype = None
cpSpaceHashRehashObject.argtypes = [POINTER(cpSpaceHash), c_void_p, c_ulong]
cpSpaceHashQueryFunc = CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
cpSpaceHashQuery = _libraries['ChipmunkPyEd.dll'].cpSpaceHashQuery
cpSpaceHashQuery.restype = None
cpSpaceHashQuery.argtypes = [POINTER(cpSpaceHash), c_void_p, cpBB, cpSpaceHashQueryFunc, c_void_p]
cpSpaceHashQueryRehash = _libraries['ChipmunkPyEd.dll'].cpSpaceHashQueryRehash
cpSpaceHashQueryRehash.restype = None
cpSpaceHashQueryRehash.argtypes = [POINTER(cpSpaceHash), cpSpaceHashQueryFunc, c_void_p]
cpvlength = _libraries['ChipmunkPyEd.dll'].cpvlength
cpvlength.restype = cpFloat
cpvlength.argtypes = [cpVect]
cpvlengthsq = _libraries['ChipmunkPyEd.dll'].cpvlengthsq
cpvlengthsq.restype = cpFloat
cpvlengthsq.argtypes = [cpVect]
cpvnormalize = _libraries['ChipmunkPyEd.dll'].cpvnormalize
cpvnormalize.restype = cpVect
cpvnormalize.argtypes = [cpVect]
cpvforangle = _libraries['ChipmunkPyEd.dll'].cpvforangle
cpvforangle.restype = cpVect
cpvforangle.argtypes = [cpFloat]
cpvtoangle = _libraries['ChipmunkPyEd.dll'].cpvtoangle
cpvtoangle.restype = cpFloat
cpvtoangle.argtypes = [cpVect]
cpvstr = _libraries['ChipmunkPyEd.dll'].cpvstr
cpvstr.restype = STRING
cpvstr.argtypes = [cpVect]
__all__ = ['cpSpaceRehashStatic', 'cpSpaceAddCollisionPairFunc',
           'cpSpaceResizeStaticHash', 'cpHashSetReject',
           'cpBodySetAngle', 'cpSpaceRemoveCollisionPairFunc',
           'cpHashSetEach', 'cpContactInit', 'cpArrayIter',
           'cpSpaceHashRehash', 'cpHashSetRemove', 'cpArray',
           'cpSlideJointNew', 'cpHashSetIterFunc', 'cpShapeType',
           'cpArrayDeleteObj', 'cpPolyShapeAlloc', 'cpArbiterFree',
           'cpSpaceRemoveJoint', 'cpSpace', 'cpArbiterPreStep',
           'cpSpaceHashDestroy', 'cpBodyAlloc', 'cpSpaceHashAlloc',
           'cpBody', 'cpBodySetMass', 'cpvstr', 'cpMomentForPoly',
           'cpJointDestroy', 'cpSpaceHashNew', 'cpBodyDestroy',
           'M_PI', 'cpArrayPush', 'cpSpaceHashFree',
           'CP_SEGMENT_SHAPE', 'cpHashSetNew', 'cpVect',
           'cpSpaceHashRemove', 'cpSpaceHashInit', 'cpPivotJointNew',
           'cpSegmentShapeNew', 'cpPolyShapeInit', 'CP_HASH_COEF',
           'cpPolyShapeNew', 'cpArrayContains', 'cpHashSetRejectFunc',
           'cpSlideJoint', 'CP_POLY_SHAPE', 'cpBodyUpdateVelocity',
           'cpSpaceAlloc', 'cpCircleShapeAlloc', 'cpPinJointAlloc',
           'cpBodyUpdatePosition', 'cpSpaceDestroy', 'CP_NUM_SHAPES',
           'cpContact', 'cpDampedSpring', 'cpSegmentShape',
           'cpSlideJointAlloc', 'cpArbiter', 'cpSpaceNew',
           'cpCircleShape', 'cpSpaceFree', 'cpCircleShapeNew',
           'cpSpaceInit', 'cpArrayFree', 'cpSpaceHashBin',
           'cpBBClampVect', 'cpBodySlew', 'cpArrayEach', 'cpBodyFree',
           'cpPolyShapeContainsVert', 'cpPivotJointInit',
           'cpSpaceRemoveBody', 'cpSpaceHashBBFunc', 'cpHashSetInit',
           'cpArbiterDestroy', 'cpSpaceBodyIterator',
           'cpSpaceAddBody', 'cpBodySetMoment', 'cpHashSetInsert',
           'cpContactsSumImpulsesWithFriction', 'cpShapeFree',
           'cpHashSetBin', 'cpShape', 'cpSpaceRemoveShape',
           'CP_CIRCLE_SHAPE', 'cpSpaceHash', 'cpArbiterNew',
           'cpPinJoint', 'cpvlengthsq', 'cpBBWrapVect', 'cpJointFree',
           'cpArrayInit', 'cpPinJointInit', 'cpSpaceHashResize',
           'cpArbiterInject', 'cpSpaceAddShape', 'cpvnormalize',
           'cpArrayNew', 'cpHashSetDestroy', 'cpSpaceHashEach',
           'cpSpaceEachBody', 'cpPolyShapeValueOnAxis',
           'cpSpaceSetDefaultCollisionPairFunc', 'cpHashSetFind',
           'cpHashSetEqlFunc', 'cpPolyShapeAxis',
           'cpHashSetTransFunc', 'cpShapeCacheBB', 'cpShapeInit',
           'cpArrayAlloc', 'cpSpaceHashIterator', 'cpSpaceHashQuery',
           'cpMomentForCircle', 'cpvtoangle', 'cpSpaceAddJoint',
           'cpSpaceHashRehashObject', 'cpArbiterApplyImpulse',
           'cpHashSetFree', 'cpContactsSumImpulses',
           'cpCollideShapes', 'cpBodyInit', 'cpCollFunc', 'cpBodyNew',
           'cpSpaceStep', 'cpHashSet', 'cpArbiterAlloc', 'cpFloat',
           'cpPinJointNew', 'cpPolyShape', 'cpvforangle',
           'cpSpaceFreeChildren', 'cpCollPairFunc',
           'cpArrayDeleteIndex', 'cpBodyResetForces',
           'cpBodyApplyForce', 'cpSpaceHashQueryRehash',
           'cpArbiterInit', 'cpSpaceResizeActiveHash',
           'cpPivotJointAlloc', 'cpSpaceRemoveStaticShape', 'cpJoint',
           'cpResetShapeIdCounter', 'cpPivotJoint',
           'cpSegmentShapeInit', 'cpHashSetAlloc',
           'cpCircleShapeInit', 'cpBB', 'cpSlideJointInit',
           'cpArrayDestroy', 'cpSpaceHashQueryFunc',
           'cpSpaceAddStaticShape', 'cpSegmentShapeAlloc',
           'cpSpaceHashInsert', 'cpShapeDestroy', 'cpInitChipmunk',
           'cpHandle', 'cpvlength']
