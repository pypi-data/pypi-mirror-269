# -*- coding: utf-8 -*-
from bda.plone.productshop.interfaces import IProduct
from bda.plone.productshop.interfaces import IProductGroup
from bda.plone.productshop.interfaces import IVariant
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implementer


@implementer(IProduct)
class Product(Item):
    """Product Content.
    """


@implementer(IProductGroup)
class ProductGroup(Container):
    """Product Group content.
    """


@implementer(IVariant)
class Variant(Item):
    """Variant content.
    """
