import pytest


@pytest.fixture
def coords_to_h3():
    from datanonymizer.conversion import coords_to_h3

    return coords_to_h3


@pytest.fixture
def has_value():
    from datanonymizer.conversion import has_value

    return has_value


def test_coords_to_h3(coords_to_h3):
    assert coords_to_h3("[-3.7371831,-38.48810530000001]") == "8880104c07fffff"
    assert coords_to_h3("[-23.537066,-46.8329106]") == "88a810312dfffff"


def test_has_value(has_value):
    assert has_value("") is False
    assert has_value("  ") is True
    assert has_value("0") is True
    assert has_value(".") is True
    assert has_value("Frodo") is True
