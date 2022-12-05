import os

import googlemaps as gmaps

from aswe.api.navigation.trip_data import MapsTrip, MapsTripMode

_GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_maps_connection(start_location: str, end_location: str, mode: MapsTripMode) -> MapsTrip:
    """Provides the distance and duration for a trip with a specific transportation type

    Parameters
    ----------
    start_location : str
        Name of the location the trip starts
    end_location : str
        Name of the location the trip ends
    mode : MapsTripMode
        Type of transportation. Possible values: 'driving', 'walking', 'bicycling' or 'transit'

    Returns
    -------
    MapsTrip
        A MapsTrip object containing the distance and duration of the trip
    """
    client = gmaps.Client(key=_GOOGLE_MAPS_API_KEY)
    directions_result = client.directions(start_location, end_location, mode=mode)  # type: ignore

    return MapsTrip(
        distance=int(directions_result[0]["legs"][0]["distance"]["value"]),
        duration=int(directions_result[0]["legs"][0]["duration"]["value"] / 60),
    )
