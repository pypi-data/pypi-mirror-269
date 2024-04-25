import re

from tdi_rust_python_tools import clean_temperature

from shared.shared import timeit

TEST_VALUES: list[str] = [
    "10°C",
    "",
    "Store at -2.5 oc",
    "Store at 2-8oC for up to 6 months",
    "Store at -20℃ for a year",
]

TEMPERATURE_PATTERN = re.compile(
    r"""
    (-? # maybe a minus sign
    \d+ # a number
    \.? # maybe a dot
    \d*) # maybe another number
    (\s*[^°]C) # maybe a space, then any single character that is not a degree symbol and a C
    """,
    re.VERBOSE | re.IGNORECASE,
)


def clean_temperature_python(value: str) -> str:
    """Cleans common issues with 'Degrees Celsius' values."""
    # Changes any non ° characters to a °
    value = TEMPERATURE_PATTERN.sub(r"\1°C", value)

    # Fixes the combined degree C character
    return value.replace("℃", "°C")


@timeit
def process_python() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = clean_temperature_python(value)


@timeit
def process_rust() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = clean_temperature(value)


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
