# pylint: disable=invalid-name

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class _UnitEnum(str, Enum):
    """Enum of possible radius values for Event API Params"""

    MILES = "miles"
    KILOMETER = "km"


class _SortEnum(str, Enum):
    """Enum of possible sort by values"""

    NAME_ASC = "name,asc"
    NAME_DESC = "name,desc"
    RELEVANCE_ASC = "relevance,asc"
    RELEVANCE_DESC = "relevance,desc"
    DISTANCE_ASC = "distance,asc"
    DISTANCE_DESC = "distance,desc"


@dataclass
class EventApiEnums:
    """Defines dataclass for possible EventApi request query enums"""

    UNIT: ClassVar[type[_UnitEnum]] = _UnitEnum
    SORT: ClassVar[type[_SortEnum]] = _SortEnum


# TODO add remaining query parameters from https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
# TODO write methods to concatenate list[str] values
# TODO write methods to cast int into str values to send request
# TODO write methods to validate values such as country_code, start_date, end_date, locale
# TODO write functionality, that Class EventApiPAram can not only be used for search-event endpoint but also for search-venue endpoint,
# TODO although not all params are compatible
@dataclass
class EventApiParams:
    """Query Params Dataclass for Event API requests"""

    id: str | None = None
    """Filter entities by its id"""

    keyword: str | None = None
    """Keyword to search on"""

    attraction_id: str | None = None
    """Filter by attraction id"""

    venue_id: str | None = None
    """Filter by venue id"""

    postal_code: str | None = None
    """Filter by postal code / zipcode"""

    radius: int | None = None
    """Radius of the area in which we want to search for events."""

    unit: _UnitEnum = _UnitEnum.KILOMETER
    """Unit of the radius. Defaults to \"km\""""

    locale: list[str] = ["de"]
    """The locale in ISO code format. Multiple comma-separated values can be provided.
    When omitting the country part of the code (e.g. only \"en\" or \"fr\") then the first matching locale is used.
    When using a \"*\" it matches all locales. \"*\" can only be used at the end (e.g. \"en-us,en,*\").
    Defaults to `[\"de\"]`."""

    start_date_time: str | None = None
    """Filter with a start date after this date"""

    end_date_time: str | None = None
    """Filter with a start date before this date"""

    size: int | None = None
    """Page size of the response. Defaults to 20."""

    page: int | None = None
    """Page number. Defaults to 0."""

    sort: _SortEnum | None = None
    """Sorting order of the search result. Allowable Values: \"name,asc\", \"name,desc\", \"relevance,asc\",
    \"relevance,desc\", \"distance,asc\", \"distance,desc\", \"random\".
    Defaults to \"relevance,desc\""""

    city: list[str] | None = None
    """Filter by city"""

    country_code: str | None = None
    """Filter by country code"""

    state_code: str | None = None
    """Filter by state code"""

    classification_name: list[str] | None = None
    """Filter by classification name: name of any segment, genre, sub-genre, type, sub-type.
    Negative filtering is supported by using the following format '-'.
    Be aware that negative filters may cause decreased performance."""

    classification_id: list[str] | None = None
    """Filter by classification id: id of any segment, genre, sub-genre, type, sub-type.
    Negative filtering is supported by using the following format '-'.
    Be aware that negative filters may cause decreased performance."""

    include_family: bool | None = None
    """Filter by classification that are family-friendly. Defaults to yes."""

    geo_point: str | None = None
    """Filter events by geoHash"""
