def test_get_report_renderer_returns_json_renderer():
    from dataguard.reporter import get_report_renderer

    renderer = get_report_renderer("json")
    assert renderer.__name__ == "render_json_report"


def test_get_report_renderer_returns_text_renderer():
    from dataguard.reporter import get_report_renderer

    renderer = get_report_renderer("text")
    assert renderer.__name__ == "render_text_report"


def test_get_report_renderer_raises_on_unknown_format():
    import pytest

    from dataguard.reporter import get_report_renderer

    with pytest.raises(ValueError, match="Unknown report format: xml"):
        get_report_renderer("xml")


def test_get_report_renderer_raises_on_invalid_format():
    import pytest

    from dataguard.reporter import get_report_renderer

    with pytest.raises(ValueError, match="Unknown report format: invalid"):
        get_report_renderer("invalid")
