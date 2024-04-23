# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from redturtle.faq.interfaces import IFaq, IFaqFolder
from zope.interface import implementer


@implementer(IFaq)
class Faq(Container):
    """ """


@implementer(IFaqFolder)
class FaqFolder(Container):
    """ """
