# -*- coding: utf-8 -*-
from plone.supermodel import model
from redturtle.faq import _
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine


class IRedturtleFaqLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFaq(model.Schema):
    """ """


class IFaqFolder(model.Schema):
    """ """

    icon = TextLine(
        title=_("icon_label", default="Icon"),
        description=_(
            "icona_help",
            default="You can select an icon from select menu or set a "
            "FontAwesome icon name.",
        ),
        required=False,
        default="",
    )


class ISerializeFaqToJsonSummary(Interface):
    """
    custom interface to serialize faqs
    """
