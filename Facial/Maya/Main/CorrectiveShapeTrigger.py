import sys
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as omanim
import maya.api.OpenMayaRender as omrender
import maya.api.OpenMayaUI as omui

import numpy

def maya_useNewAPI():
    pass


# -----------------------------------------------------------------------------
# Node Definition
# -----------------------------------------------------------------------------
class CorrectiveShapeTrigger(om.MPxNode):
    """
    A node to compute the arithmetic mean of two doubles.
    """
    ## the name of the nodeType
    kPluginNodeTypeName = 'CorrectiveShapeTrigger'
    ## the unique MTypeId for the node
    kPluginNodeId = om.MTypeId(0x0027516)

    inTriggerPoseWeightList = om.MObject()
    inTriggerPoseName = om.MObject()
    inTriggerWeight = om.MObject()
    inCurrentWeight = om.MObject()
    inRemapFromX = om.MObject()
    inRemapFromY = om.MObject()
    inRemapToX = om.MObject()
    inRemapToY = om.MObject()
    outWeight = om.MObject()

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def nodeCreator():
        return CorrectiveShapeTrigger()

    @staticmethod
    def initialize():
        nAttrAllPoseInfoList = om.MFnCompoundAttribute()
        CorrectiveShapeTrigger.inTriggerPoseWeightList = nAttrAllPoseInfoList.create('triggerPoseInfoList', 'pwl')
        nAttrAllPoseInfoList.keyable = True
        nAttrAllPoseInfoList.array = True
        nAttrAllPoseInfoList.storable = True
        nAttrAllPoseInfoList.indexMatters = False

        nAttrPoseName = om.MFnTypedAttribute()
        CorrectiveShapeTrigger.inTriggerPoseName = nAttrPoseName.create('triggerPoseName', 'tpn', om.MFnData.kString)
        nAttrPoseName.keyable = True

        nAttrInTriggerWeight = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.inTriggerWeight = nAttrInTriggerWeight.create('triggerWeight', 'tw', om.MFnNumericData.kFloat, 0.0)
        nAttrInTriggerWeight.keyable = True
        nAttrInTriggerWeight.storable = True

        nAttrInCurrentWeight = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.inCurrentWeight = nAttrInCurrentWeight.create('currentWeight', 'cw', om.MFnNumericData.kFloat, 0.0)
        nAttrInCurrentWeight.keyable = True
        nAttrInCurrentWeight.storable = True
        
        nAttrRemapFromX = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.inRemapFromX = nAttrRemapFromX.create('remapFromX', 'rfx', om.MFnNumericData.kFloat, 0.5)
        nAttrRemapFromX.keyable = True
        nAttrRemapFromX.storable = True

        nAttrRemapFromY = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.inRemapFromY = nAttrRemapFromY.create('remapFromY', 'rfy', om.MFnNumericData.kFloat, 1.0)
        nAttrRemapFromY.keyable = True
        nAttrRemapFromY.storable = True

        nAttrRemapToX = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.inRemapToX = nAttrRemapToX.create('remapToX', 'rtx', om.MFnNumericData.kFloat, 0.0)
        nAttrRemapToX.keyable = True
        nAttrRemapToX.storable = True

        nAttrRemapToY = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.inRemapToY = nAttrRemapToY.create('remapToY', 'rty', om.MFnNumericData.kFloat, 1.0)
        nAttrRemapToY.keyable = True
        nAttrRemapToY.storable = True

        nAttrAllPoseInfoList.addChild(CorrectiveShapeTrigger.inTriggerPoseName)
        nAttrAllPoseInfoList.addChild(CorrectiveShapeTrigger.inTriggerWeight)
        nAttrAllPoseInfoList.addChild(CorrectiveShapeTrigger.inCurrentWeight)


        nAttrOut = om.MFnNumericAttribute()
        CorrectiveShapeTrigger.outWeight = nAttrOut.create('outWeight', 'ow', om.MFnNumericData.kFloat, 0.0)


        # add the attributes
        om.MPxNode.addAttribute(CorrectiveShapeTrigger.inTriggerPoseWeightList)
        om.MPxNode.addAttribute(CorrectiveShapeTrigger.inRemapFromX)
        om.MPxNode.addAttribute(CorrectiveShapeTrigger.inRemapFromY)
        om.MPxNode.addAttribute(CorrectiveShapeTrigger.inRemapToX)
        om.MPxNode.addAttribute(CorrectiveShapeTrigger.inRemapToY)
        om.MPxNode.addAttribute(CorrectiveShapeTrigger.outWeight)

        om.MPxNode.attributeAffects(CorrectiveShapeTrigger.inTriggerPoseWeightList, CorrectiveShapeTrigger.outWeight)
        om.MPxNode.attributeAffects(CorrectiveShapeTrigger.inRemapFromX, CorrectiveShapeTrigger.outWeight)
        om.MPxNode.attributeAffects(CorrectiveShapeTrigger.inRemapFromY, CorrectiveShapeTrigger.outWeight)
        om.MPxNode.attributeAffects(CorrectiveShapeTrigger.inRemapToX, CorrectiveShapeTrigger.outWeight)
        om.MPxNode.attributeAffects(CorrectiveShapeTrigger.inRemapToY, CorrectiveShapeTrigger.outWeight)

    def compute(self, plug, dataBlock):
        # get the incoming data
        # print 'compute'
        inAllPoseWeightList_mArrayData = dataBlock.inputArrayValue(CorrectiveShapeTrigger.inTriggerPoseWeightList)

        poseNameList = []

        currentPoseWeightList = []

        triggerWeightList = []

        for i in range(len(inAllPoseWeightList_mArrayData)):
            inAllPoseWeightList_mArrayData.jumpToPhysicalElement(i)
            poseDataHandle = inAllPoseWeightList_mArrayData.inputValue()

            poseName = poseDataHandle.child(CorrectiveShapeTrigger.inTriggerPoseName).asString()
            poseNameList.append(poseName)

            triggerWeight = poseDataHandle.child(CorrectiveShapeTrigger.inTriggerWeight).asFloat()
            currentPoseWeight = poseDataHandle.child(CorrectiveShapeTrigger.inCurrentWeight).asFloat()
            # print 'triggerWeight', triggerWeight
            # print 'currentPoseWeight', currentPoseWeight

            triggerWeightList.append(triggerWeight)
            currentPoseWeightList.append(currentPoseWeight)



        triggerWeightList = numpy.array(triggerWeightList)
        currentPoseWeightList = numpy.array(currentPoseWeightList)

        offsetList = currentPoseWeightList - triggerWeightList
        # print 'offsetList', offsetList
        offsetFromTriggering = numpy.sum(numpy.abs(offsetList ))
        # print 'offsetFromTriggering', offsetFromTriggering

        remapFromX = dataBlock.inputValue(CorrectiveShapeTrigger.inRemapFromX).asFloat()
        remapFromY = dataBlock.inputValue(CorrectiveShapeTrigger.inRemapFromY).asFloat()
        # print 'remapFrom', remapFromX, remapFromY

        remapToX = dataBlock.inputValue(CorrectiveShapeTrigger.inRemapToX).asFloat()
        remapToY = dataBlock.inputValue(CorrectiveShapeTrigger.inRemapToY).asFloat()
        # print 'remapTo', remapToX, remapToY

        outWeight = 1.0 - offsetFromTriggering

        outWeight = remap(outWeight, remapFromX, remapFromY, remapToX, remapToY)
        # print 'outWeight', outWeight

        outWeightData = dataBlock.outputValue(CorrectiveShapeTrigger.outWeight)

        outWeightData.setFloat(outWeight)

        dataBlock.setClean(plug)

def remap(x, fromX, fromY, toX, toY):
    o = linearStep(x, fromX, fromY)
    o = lerp(o, toX, toY)
    return o

def clamp(x, clampMin, clampMax):
    return max(min(x, clampMax),clampMin)

def linearStep(x, clampMin, clampMax):
    return clamp((x - clampMin) / (clampMax - clampMin + 0.000001), 0.0, 1.0)

def lerp(x, a, b):
    return (1 - x) * a + x * b

# -----------------------------------------------------------------------------
# Initialize
# -----------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.registerNode(CorrectiveShapeTrigger.kPluginNodeTypeName, CorrectiveShapeTrigger.kPluginNodeId,
                            CorrectiveShapeTrigger.nodeCreator, CorrectiveShapeTrigger.initialize)
    except:
        raise Exception('Failed to register node: %s' % CorrectiveShapeTrigger.kPluginNodeTypeName)


# -----------------------------------------------------------------------------
# Uninitialize
# -----------------------------------------------------------------------------
def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.deregisterNode(CorrectiveShapeTrigger.kPluginNodeId)
    except:
        raise Exception('Failed to unregister node: %s' % CorrectiveShapeTrigger.kPluginNodeTypeName)
