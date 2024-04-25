import pytest
from tdi_rust_python_tools import fix_lt_gt

from less_than_greater_than import fix_lt_gt_python


@pytest.mark.parametrize(
    argnames=("value",),
    argvalues=(
        ("<p>Some text</p>",),
        ("<div>More text</div>",),
        ("<span>Even more text</span>",),
        ("<p>Text with < symbol</p>",),
        ("<div>Text with > symbol</div>",),
        ("<span>Text with < and > symbols</span>",),
        ("Lovely long text with no html tags",),
        ("<div>",),
        ("",),
    ),
)
def test_fix_lt_gt(value: str) -> None:
    assert fix_lt_gt(value) == fix_lt_gt_python(value)
