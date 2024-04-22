# -*- coding: utf-8 -*-
from bda.plone.productshop.behaviors import IAngleBehavior
from bda.plone.productshop.behaviors import IColorBehavior
from bda.plone.productshop.behaviors import IDemandBehavior
from bda.plone.productshop.behaviors import IHeightBehavior
from bda.plone.productshop.behaviors import IIPCodeBehavior
from bda.plone.productshop.behaviors import ILengthBehavior
from bda.plone.productshop.behaviors import IMaterialBehavior
from bda.plone.productshop.behaviors import ISizeBehavior
from bda.plone.productshop.behaviors import IWeightBehavior
from bda.plone.productshop.behaviors import IWidthBehavior
from plone.indexer import indexer


@indexer(IColorBehavior)
def color_aspect(obj):
    return obj.color


@indexer(IWeightBehavior)
def weight_aspect(obj):
    return obj.weight


@indexer(ISizeBehavior)
def size_aspect(obj):
    return obj.size


@indexer(IDemandBehavior)
def demand_aspect(obj):
    return obj.demand


@indexer(ILengthBehavior)
def length_aspect(obj):
    return obj.length


@indexer(IWidthBehavior)
def width_aspect(obj):
    return obj.width


@indexer(IHeightBehavior)
def height_aspect(obj):
    return obj.height


@indexer(IIPCodeBehavior)
def ip_code_aspect(obj):
    return obj.ip_code


@indexer(IAngleBehavior)
def angle_aspect(obj):
    return obj.angle


@indexer(IMaterialBehavior)
def material_aspect(obj):
    return obj.material
