import re

from tdi_rust_python_tools import strip_html_tags

from shared.shared import timeit

HTML_PATTERN = re.compile(r"<.*?>")

TEST_VALUES: tuple[str, ...] = (
    "",
    "Normal text with no html tags",
    "N/A",
    "<p>Some text</p>",
    "<div>More text</div>",
    "<span>Even more text</span>",
    "<p>Text with < symbol</p>",
    "<div>Text with > symbol</div>",
    "<span>Text with < and > symbols</span>",
    "Lovely long text with no html tags",
    "<div>",
    "<p><span>Text with nested tags</span></p>",
    "<p>Text with <span>tags</span></p>",
)


def strip_html_tags_python(value: str) -> str:
    """Removes all HTML tags from `value`."""
    if "<" in value and ">" in value:
        return re.sub(HTML_PATTERN, "", value)
    else:
        return value


@timeit
def process_python() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = strip_html_tags_python(value)


@timeit
def process_rust() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = strip_html_tags(value)


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
