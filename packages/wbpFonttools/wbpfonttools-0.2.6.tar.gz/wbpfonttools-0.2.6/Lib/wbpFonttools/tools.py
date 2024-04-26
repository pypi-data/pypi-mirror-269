"""
tools
===============================================================================

Tools used by the wbpFonttools plugin.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional
from xml.parsers.expat import ParserCreate

import wx
from fontTools.ttLib import getTableClass
from fontTools.ttLib.tables.DefaultTable import DefaultTable

from .dialog import SelectFontsDialog
from .document import FontToolsDocument, TTFont

if TYPE_CHECKING:
    from wbBase.application import App


class TtxTableParser(object):
    def __init__(self, font: TTFont):
        self.font = font
        self.table: Optional[DefaultTable] = None
        self.root = None
        self.contentStack = []
        self.stackSize = 0

    def parse(self, tableData, tableTag):
        tableClass = getTableClass(tableTag)
        if tableClass is None:
            tableClass = DefaultTable
        self.table = tableClass(tableTag)
        self.font[tableTag] = self.table
        self.contentStack.append([])
        self.stackSize = 1
        parser = ParserCreate()
        parser.StartElementHandler = self.startElementHandler
        parser.EndElementHandler = self.endElementHandler
        parser.CharacterDataHandler = self.characterDataHandler
        parser.Parse(tableData, True)

    def startElementHandler(self, name, attrs):
        stackSize = self.stackSize
        self.stackSize = stackSize + 1
        if stackSize == 2:
            self.contentStack.append([])
            self.root = (name, attrs, self.contentStack[-1])
        else:
            list = []
            self.contentStack[-1].append((name, attrs, list))
            self.contentStack.append(list)

    def characterDataHandler(self, data):
        if self.stackSize > 1:
            self.contentStack[-1].append(data)

    def endElementHandler(self, name):
        self.stackSize = self.stackSize - 1
        del self.contentStack[-1]
        if self.stackSize == 1:
            self.root = None
        elif self.stackSize == 2:
            name, attrs, content = self.root
            self.table.fromXML(name, attrs, content, self.font)
            self.root = None


def CurrentFont() -> Optional[TTFont]:
    """
    Get the currently active font
    """
    app: App = wx.GetApp()
    doc = app.TopWindow.documentManager.currentDocument
    if isinstance(doc, FontToolsDocument):
        return doc.font
    return None


def AllFonts() -> Iterable[TTFont]:
    """
    Get all currently open fonts
    """
    app: App = wx.GetApp()
    for doc in app.TopWindow.documentManager.documents:
        if isinstance(doc, FontToolsDocument) and isinstance(doc.font, TTFont):
            yield doc.font


def SelectFonts(
    message: str = "Select fonts", allFonts: Optional[Iterable[TTFont]] = None
) -> List[TTFont]:
    """
    Show the :class:`~.dialog.SelectFontsDialog` and return the selected fonts.
    """
    if not allFonts:
        allFonts = AllFonts()
    fonts = []
    with SelectFontsDialog(message, allFonts) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            fonts = dlg.selectedFonts
    return fonts
