from __future__ import annotations

from .config import FonttoolsPreferences, ObjectViewPreferences, XmlViewPreferences
from .template import (
    OpenType_OTF_Template,
    OpenType_TTC_Template,
    OpenType_TTF_Template,
    WebFont_WOFF_2_Template,
    WebFont_WOFF_Template,
)
from .tools import AllFonts, CurrentFont, SelectFonts

__version__ = "0.2.6"


doctemplates = (
    OpenType_OTF_Template,
    OpenType_TTC_Template,
    OpenType_TTF_Template,
    WebFont_WOFF_2_Template,
    WebFont_WOFF_Template,
)

preferencepages = (FonttoolsPreferences, XmlViewPreferences, ObjectViewPreferences)

globalObjects = ("CurrentFont", "AllFonts", "SelectFonts")
