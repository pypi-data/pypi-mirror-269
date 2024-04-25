import pytest
from tdi_rust_python_tools import clean_temperature

from clean_temperature import clean_temperature_python


@pytest.mark.parametrize(
    argnames=("values",),
    argvalues=(
        ("10°C",),
        ("",),
        ("Store at -2.5 oc",),
        ("Store at 2-8oC for up to 6 months",),
        ("Store at -20℃ for a year",),
    ),
)
def test_clean_values(values: str) -> None:
    assert clean_temperature(values) == clean_temperature_python(values)
