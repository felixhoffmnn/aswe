from aswe.api.navigation.maps import get_maps_connection


def test_get_maps_connection() -> None:
    """Test `aswe.api.navigation.maps.get_maps_connection`"""
    maps_trip = get_maps_connection("Ernsthaldenstraße 43", "Rotebühlplatz 41", "driving")

    assert isinstance(maps_trip.duration, int)
    assert isinstance(maps_trip.distance, int)
