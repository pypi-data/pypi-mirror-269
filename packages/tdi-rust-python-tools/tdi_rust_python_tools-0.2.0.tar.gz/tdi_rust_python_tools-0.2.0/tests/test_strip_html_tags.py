import pytest
from tdi_rust_python_tools import strip_html_tags

from remove_html import strip_html_tags_python


@pytest.mark.parametrize(
    argnames=("value",),
    argvalues=(
        ("",),
        ("Normal text with no html tags",),
        ("N/A",),
        ("<p>Some text</p>",),
        ("<div>More text</div>",),
        ("<span>Even more text</span>",),
        ("<p>Text with < symbol</p>",),
        ("<div>Text with > symbol</div>",),
        ("<span>Text with < and > symbols</span>",),
        ("Lovely long text with no html tags",),
        ("<div>",),
        ("<p><span>Text with nested tags</span></p>",),
        ("<p>Text with <span>tags</span></p>",),
    ),
)
def test_clean_values_1(value: str) -> None:
    assert strip_html_tags(value) == strip_html_tags_python(value)
