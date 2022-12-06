# pylint: disable=invalid-name

from dataclasses import dataclass
from datetime import datetime

from aswe.api.navigation.trip_data import MapsTripMode


@dataclass
class EventLocation:
    """Helper dataclass storing Event Location"""

    city: str
    """City the event is located in"""
    address: str
    """Street and house number of location"""
    name: str = ""
    """Name of location"""


@dataclass(eq=True)
class ReducedEvent:
    """Dataclass storing reduced Event data for `EventApi.events`"""

    id: str
    """Id of event"""
    name: str
    """Name / Title of event"""
    start: str
    """date or datetime as string. format for either `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ssZ`"""
    status: str
    """Status of event. Either `onsale`, `cancelled`, or `offsale`"""
    location: EventLocation
    """Location of event"""


@dataclass
class EventSummary:
    """Dataclass of Event info which is used for tts"""

    name: str
    """Name / Title of event"""
    start: datetime
    """Datetime of when event starts"""
    location: EventLocation
    """Location of event"""
    is_cold: bool = False
    """Whether or not temperature is below threshold. Defined in `use_cases.event`"""
    is_rainy: bool = False
    """Whether or not precipitation is above certain threshold. Defined in `use_cases.event`"""
    trip_mode: MapsTripMode = MapsTripMode.BICYCLING
    """Preferred trip mode to event"""
    trip_duration: int | None = None
    """Trip duration"""
