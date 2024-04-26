"""
Very simple test, just check that all modules are importable
"""
from types import ModuleType

from wbBase.application import App
from wbBase.applicationInfo import ApplicationInfo, PluginInfo

appinfo = ApplicationInfo(
    Plugins=[PluginInfo(Name="fonttools", Installation="default")]
)


def test_plugin():
    app = App(test=True, info=appinfo)
    assert "fonttools" in app.pluginManager
    app.Destroy()


def test_config():
    from wbpFonttools import config

    assert isinstance(config, ModuleType)


def test_control():
    from wbpFonttools import control

    assert isinstance(control, ModuleType)


def test_dialog():
    from wbpFonttools import dialog

    assert isinstance(dialog, ModuleType)


def test_document():
    from wbpFonttools import document

    assert isinstance(document, ModuleType)
