"""
dialog
===============================================================================

Controls used by the wbpFonttools plugin.
"""
from __future__ import annotations
import wx
from typing import TYPE_CHECKING, Optional, Iterable, List

from .selectFontsDialogUI import SelectFontsDialogUI

if TYPE_CHECKING:
    from wbBase.application import App
    from .document import TTFont


class SelectFontsDialog(SelectFontsDialogUI):
    """
    Dialog to select one or more fonts from the fonts open in the application.
    """

    def __init__(self, message: str = "Select fonts", allFonts:Optional[Iterable[TTFont]] = None):
        """
        :param message: Message shown in the dialog, defaults to 'Select fonts'
        """
        app:App = wx.GetApp()
        SelectFontsDialogUI.__init__(self, app.TopWindow)
        self.label_message.Label = message
        fontList = self.listCtrl_fonts
        if allFonts:
            fontDocs = [f.document for f in allFonts]
            fontList.allFonts = fontDocs
            fontList.allFonts.sort(key=lambda f: f.path)
            fontList.SetItemCount(len(fontDocs))
        currentDoc = app.documentManager.currentDocument
        for i in range(fontList.ItemCount):
            if fontList.allFonts[i] == currentDoc:
                fontList.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    @property
    def selectedFonts(self) -> List[TTFont]:
        return self.listCtrl_fonts.getSelectedFonts()

    def on_KEY_DOWN(self, event:wx.KeyEvent) -> None:
        unicodeKey = event.GetUnicodeKey()
        if unicodeKey != wx.WXK_NONE:
            key = chr(unicodeKey)
            if key == "A" and (event.ControlDown() or event.CmdDown()):
                fontList = self.listCtrl_fonts
                for i in range(fontList.ItemCount):
                    fontList.SetItemState(
                        i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED
                    )
        else:
            event.Skip()
