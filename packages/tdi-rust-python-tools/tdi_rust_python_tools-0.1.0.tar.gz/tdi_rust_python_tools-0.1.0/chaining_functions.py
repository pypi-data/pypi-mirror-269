from tdi_rust_python_tools import (
    clean_temperature,
    combine_dedupe_values,
    fix_lt_gt,
    remove_chinese_chars,
    unescape_html_chars,
)

from clean_temperature import clean_temperature_python
from combine_dedupe import combine_dedupe_values_python
from less_than_greater_than import fix_lt_gt_python
from remove_chinese_chars import remove_chinese_chars_old_python
from shared.shared import timeit
from unescape_html import unescape_html_chars_python

TEST_SINGLE_VALUES: list[str] = [
    # values with encoded chars
    "&lt;95% purity",
    "5 &mu;g",
    "25 &micro;g",
    # values with html tags
    "<p>Some text</p>",
    "<div>More text</div>",
    "<span>Even more text</span>",
    "<p>Text with < symbol</p>",
    "<div>Text with > symbol</div>",
    "<span>Text with < and > symbols</span>",
    "Lovely long text with no html tags",
    "<div>",
    "",
    # temperature values
    "10°C",
    "",
    "Store at -2.5 oc",
    "Store at 2-8oC for up to 6 months",
    "Store at -20℃ for a year",
    # values with chinese characters
    "",
    "ABC  Antibody",
    "ABC Antibody (兔抗體)",
    "Hello, 世界",
    "你好, World",
    "Rust语言",
    "我爱编程",
    "12345",
    "混合 English 和 中文",
    "NoChineseHere",
    # combined issues
    "Store at 2-8oC for up to 6 months, 25 &micro;g, 混合 English 和 中文, <div>Text with > symbol</div> ",
    "Store at -20℃ for a year, 5 &mu;g, 你好, World, <span>Text with < and > symbols</span>",
    "Store at -2.5 oc, &lt;95% purity, Rust语言, <p>Text with < symbol</p>",
]

TEST_MULTI_VALUES: list[list[str]] = [
    # values with joined values
    ["Hello", "Bob", "Is|Smelly"],
    ["Dog|Cat", "Lizard|Fish", "Bird", "Snake"],
    ["", "|", "Dog|Cat|Fish", "Bear"],
    [],
    [""],
    # combined issues
    ["Hello<p>", "Bob", "<div>Is|Smelly"],
    ["Dog|&lt;Cat", "Lizard|Fish&mu;g", "Bird", "Snake"],
    ["", "|", "Dog|Cat2-8oC|Fish", "Bear"],
    ["Dog|Cat", "Lizard你好|Fish", "Bird", "Snake", "我爱编程"],
]


def python_functions(sinlge_values: list[str], multi_values: list[list[str]]) -> None:
    for value in sinlge_values:
        value = unescape_html_chars_python(value)
        value = fix_lt_gt_python(value)
        value = clean_temperature_python(value)
        value = remove_chinese_chars_old_python(value)

    for values in multi_values:
        for value in values:
            value = unescape_html_chars_python(value)
            value = fix_lt_gt_python(value)
            value = clean_temperature_python(value)
            value = remove_chinese_chars_old_python(value)
        values = combine_dedupe_values_python(values, "|")


def rust_functions(sinlge_values: list[str], multi_values: list[list[str]]) -> None:
    for value in sinlge_values:
        value = unescape_html_chars(value)
        value = fix_lt_gt(value)
        value = clean_temperature(value)
        value = remove_chinese_chars(value)
    for values in multi_values:
        for value in values:
            value = unescape_html_chars(value)
            value = fix_lt_gt(value)
            value = clean_temperature(value)
            value = remove_chinese_chars(value)
        values = combine_dedupe_values(values, "|")


@timeit
def process_python() -> None:
    for _ in range(1_000_000):
        _ = python_functions(TEST_SINGLE_VALUES, TEST_MULTI_VALUES)


@timeit
def process_rust() -> None:
    for _ in range(1_000_000):
        _ = rust_functions(TEST_SINGLE_VALUES, TEST_MULTI_VALUES)


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
