import os

import googlemaps as gmaps

from aswe.api.navigation.trip_data import MapsTrip, MapsTripMode


def get_maps_connection(start_location: str, end_location: str, mode: MapsTripMode) -> MapsTrip:
    """Provides the distance and duration for a trip with a specific transportation type

    Args:
        start_location (str): Name of the location the trip starts
        end_location (str): Name of the location the trip ends
        mode (str): Type of transportation. Possible values: 'driving', 'walking', 'bicycling' or 'transit'

    Returns:
        MapsTrip: _description_
    """
    client = gmaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
    directions_result = client.directions(start_location, end_location, mode=mode)

    return MapsTrip(
        distance=int(directions_result[0]["legs"][0]["distance"]["value"]),
        duration=int(directions_result[0]["legs"][0]["duration"]["value"] / 60),
    )
