"""CONFIRMED - RUST IS FASTER THAN PYTHON IN THIS EXAMPLE."""

from tdi_rust_python_tools import combine_dedupe_values

from shared.shared import timeit

TEST_VALUES: list[list[str]] = [
    ["Hello", "Bob", "Is|Smelly"],
    ["Dog|Cat", "Lizard|Fish", "Bird", "Snake"],
    ["", "|", "Dog|Cat|Fish", "Bear"],
    [],
    [""],
]


def combine_dedupe_values_python(values: list[str], separator: str) -> str:
    output: set[str] = set()

    for value in values:
        terms = set(value.split(separator))
        output.update(terms)

    return ", ".join(sorted(output))


@timeit
def process_python() -> None:
    for _ in range(10_000_000):
        for value in TEST_VALUES:
            _ = combine_dedupe_values_python(value, "|")


@timeit
def process_rust() -> None:
    for _ in range(10_000_000):
        for value in TEST_VALUES:
            _ = combine_dedupe_values(value, "|")


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
