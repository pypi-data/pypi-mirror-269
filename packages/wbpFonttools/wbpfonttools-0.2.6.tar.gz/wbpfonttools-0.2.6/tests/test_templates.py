from wbBase.application import App
from wbBase.applicationInfo import ApplicationInfo, PluginInfo
from wbpFonttools.template import (
    OpenType_OTF_Template,
    OpenType_TTF_Template,
    WebFont_WOFF_2_Template,
    WebFont_WOFF_Template,
)

appinfo = ApplicationInfo(
    Plugins=[PluginInfo(Name="fonttools", Installation="default")]
)


def test_OpenType_OTF_Template():
    app = App(test=True, info=appinfo)
    assert any(
        isinstance(t, OpenType_OTF_Template) for t in app.documentManager.templates
    )
    assert any(
        isinstance(t, OpenType_OTF_Template)
        for t in app.documentManager.visibleTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(OpenType_OTF_Template),
        OpenType_OTF_Template,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.otf"), OpenType_OTF_Template
    )
    app.Destroy()


def test_OpenType_TTF_Template():
    app = App(test=True, info=appinfo)
    assert any(
        isinstance(t, OpenType_TTF_Template) for t in app.documentManager.templates
    )
    assert any(
        isinstance(t, OpenType_TTF_Template)
        for t in app.documentManager.visibleTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(OpenType_TTF_Template),
        OpenType_TTF_Template,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.ttf"), OpenType_TTF_Template
    )
    app.Destroy()


def test_WebFont_WOFF_Template():
    app = App(test=True, info=appinfo)
    assert any(
        isinstance(t, WebFont_WOFF_Template) for t in app.documentManager.templates
    )
    assert any(
        isinstance(t, WebFont_WOFF_Template)
        for t in app.documentManager.visibleTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(WebFont_WOFF_Template),
        WebFont_WOFF_Template,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.woff"), WebFont_WOFF_Template
    )
    app.Destroy()


def test_WebFont_WOFF_2_Template():
    app = App(test=True, info=appinfo)
    assert any(
        isinstance(t, WebFont_WOFF_2_Template) for t in app.documentManager.templates
    )
    assert any(
        isinstance(t, WebFont_WOFF_2_Template)
        for t in app.documentManager.visibleTemplates
    )
    assert isinstance(
        app.documentManager.FindTemplateByType(WebFont_WOFF_2_Template),
        WebFont_WOFF_2_Template,
    )
    assert isinstance(
        app.documentManager.FindTemplateForPath("test.woff2"), WebFont_WOFF_2_Template
    )
    app.Destroy()
