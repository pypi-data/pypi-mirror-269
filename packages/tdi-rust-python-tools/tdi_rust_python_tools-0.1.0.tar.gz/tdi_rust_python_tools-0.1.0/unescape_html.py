"""CONFIRMED - RUST IS FASTER THAN PYTHON IN THIS EXAMPLE."""

from html import unescape

from tdi_rust_python_tools import unescape_html_chars

from shared.shared import timeit

TEST_VALUES: list[str] = [
    "&lt;95% purity",
    "5 &mu;g",
    "25 &micro;g",
]


def unescape_html_chars_python(value: str) -> str:
    """Unescapes HTML characters from `value` (e.g. "100 &mu;g" returns "100 µg")."""
    return unescape(value)


@timeit
def process_python() -> None:
    for _ in range(10_000_000):
        for value in TEST_VALUES:
            _ = unescape_html_chars_python(value)


@timeit
def process_rust() -> None:
    for _ in range(10_000_000):
        for value in TEST_VALUES:
            _ = unescape_html_chars(value)


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
