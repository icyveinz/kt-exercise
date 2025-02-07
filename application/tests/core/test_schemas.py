import pytest
from core.schemas import luhn_check


# Valid IMEI numbers
@pytest.mark.parametrize("imei", [
    "490154203237518",
    "356938035643809"
])
def test_luhn_check_valid(imei):
    assert luhn_check(imei) is True

# Invalid IMEI numbers
@pytest.mark.parametrize("imei_false", [
    "490154203237519",  # Incorrect checksum
    "35693803564380",   # Too short
    "3570220116171311", # Too long
    "abcdefghijklmno"   # Non-numeric
])
def test_luhn_check_invalid(imei_false):
    assert luhn_check(imei_false) is False