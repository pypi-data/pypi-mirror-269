import pytest
from tdi_rust_python_tools import unescape_html_chars

from unescape_html import unescape_html_chars_python


@pytest.mark.parametrize(
    argnames=("value",),
    argvalues=(
        # No changes expected
        ("",),
        ("ABC Antibody",),
        # Value with escaped HTML characters
        ("&lt;95% purity",),
        ("5 &mu;g",),
        ("25 &micro;g",),
    ),
)
def test_unescape_html_chars(value: str) -> None:
    assert unescape_html_chars(value) == unescape_html_chars_python(value)
