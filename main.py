from property import Rental, Location, EnergyEfficiency, Broker, Taker

if __name__ == "__main__":
    # create a rental object
    location_1 = Location(
        lat=1.0,
        long=4.5,
        city="Hamburg",
        postal_code="456",
        street="Test-strasse",
        street_number="14 a",
    )
    rental_1 = Rental(
        id=100,
        location=location_1,
        size=88.0,
        floor=3,
        rooms=2,
        year_of_construction=2000,
        energy_efficiency=EnergyEfficiency.B,
        is_furnished=False,
        is_kitchen_included=False,
        is_garden_available=True,
        is_balcony_available=True,
        base_rent=1011.0,
        additional_costs=230.2,
    )

    broker = Broker(first_name="John", last_name="Doe")
    broker.add_property(rental_1)

    taker = Taker(first_name="Sherlock", last_name="Holmes")
    taker.add_property(
        rental_1,
    )
