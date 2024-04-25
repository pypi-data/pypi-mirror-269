import pytest
from tdi_rust_python_tools import remove_chinese_chars

from remove_chinese_chars import remove_chinese_chars_old_python


@pytest.mark.parametrize(
    argnames=("values",),
    argvalues=(
        ("",),
        ("ABC  Antibody",),
        ("ABC Antibody (兔抗體)",),
        ("Hello, 世界",),
        ("你好, World",),
        ("Rust语言",),
        ("我爱编程",),
        ("12345",),
        ("混合 English 和 中文",),
        ("NoChineseHere",),
    ),
)
def test_clean_values_1(values: str) -> None:
    assert remove_chinese_chars(values) == remove_chinese_chars_old_python(values)
