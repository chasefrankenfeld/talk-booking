from models import Address


def test_address_attributes():
    """
    GIVEN street, city, state, country
    WHEN Address is initialized
    THEN it has attributes with the same values as provided
    """

    address = Address(
        street="Sunny street 42",
        city="Awesome city",
        state="Best state",
        country="Ireland",
    )

    assert address.street == "Sunny street 42"
    assert address.city == "Awesome city"
    assert address.state == "Best state"
    assert address.country == "Ireland"
