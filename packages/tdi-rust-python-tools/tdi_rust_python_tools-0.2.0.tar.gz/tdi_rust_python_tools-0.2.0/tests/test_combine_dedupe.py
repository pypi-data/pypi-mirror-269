import pytest
from tdi_rust_python_tools import combine_dedupe_values

from combine_dedupe import combine_dedupe_values_python


@pytest.mark.parametrize(
    argnames=("values", "separator"),
    argvalues=(
        (["Hello", "Bob", "Is|Smelly"], "|"),
        (["Dog|Cat", "Lizard|Fish", "Bird", "Snake"], "|"),
        (["", "|", "Dog|Cat|Fish", "Bear"], "|"),
        ([], "|"),
        ([""], "|"),
        (["Hello", "World"], " "),
        (["Hello|World", "Python|Programming"], "|"),
        (["Apple", "Banana|Orange", "Grape|Peach"], "|"),
        (["1|2|3", "4|5|6", "7|8|9"], "|"),
        (["Python", "Java|C++", "JavaScript|Ruby"], "|"),
    ),
)
def test_combine_dedupe_values(values: list[str], separator: str) -> None:
    assert combine_dedupe_values(values, separator) == combine_dedupe_values_python(values, separator)
