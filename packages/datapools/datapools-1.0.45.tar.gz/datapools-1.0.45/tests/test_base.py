from datapools.worker.plugins.base_plugin import BasePlugin, BaseTag


def test_tag_parsing():
    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/t/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is False

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/n/asd")
    assert isinstance(t, BaseTag)
    assert str(t) == "asd"
    assert t.is_keepout() is True

    t = BasePlugin.parse_tag_in_str("https://openlicense.ai/xxx/asd")
    assert t is None
