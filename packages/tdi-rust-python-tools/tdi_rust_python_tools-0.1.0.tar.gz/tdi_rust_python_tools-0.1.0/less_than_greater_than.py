"""CONFIRMED - RUST IS FASTER THAN PYTHON IN THIS EXAMPLE."""

import re

from tdi_rust_python_tools import fix_lt_gt

from shared.shared import timeit

TEST_VALUES: list[str] = [
    "<p>Some text</p>",
    "<div>More text</div>",
    "<span>Even more text</span>",
    "<p>Text with < symbol</p>",
    "<div>Text with > symbol</div>",
    "<span>Text with < and > symbols</span>",
    "Lovely long text with no html tags",
    "<div>",
    "",
]

LT_GT_PATTERN = re.compile(
    r"""
    (?P<start>^|\s|>)  # Start of value, or a whitespace character, or a previous closing HTML tag ">"
    (?P<symbol>[<>])  # "<" or ">"
    (?P<matched_char>[^\s/])  # immediately followed by something that isn't whitespace or /
    # NOT followed by (optional alphanumeric characters and then) a ">", OR an HTML attribute "="
    # further values and ">"
    """,
    re.VERBOSE,
)


def fix_lt_gt_python(value: str) -> str:
    # Apply the regular expression without checking if "<" or ">" are in the string
    return LT_GT_PATTERN.sub(r"\g<start>\g<symbol> \g<matched_char>", value)


@timeit
def process_python() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = fix_lt_gt_python(value)


@timeit
def process_rust() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = fix_lt_gt(value)


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
