from dataclasses import dataclass
from enum import Enum


class UnitEnum(Enum):
    """Enum of possible radius values for Event API Params"""

    MILES = "miles"
    KILOMETER = "km"


class SortEnum(Enum):
    """Enum of possible sort by values"""

    NAME_ASC = "name,asc"
    NAME_DESC = "name,desc"
    RELEVANCE_ASC = "relevance,asc"
    RELEVANCE_DESC = "relevance,desc"
    DISTANCE_ASC = "distance,asc"
    DISTANCE_DESC = "distance,desc"


# TODO: Dont see the reason for wrapping enums in a class
# @dataclass
# class EventApiEnums:
#     """Defines dataclass for possible EventApi request query enums"""

#     UNIT: ClassVar[type[UnitEnum]] = UnitEnum
#     SORT: ClassVar[type[SortEnum]] = SortEnum


@dataclass
class EventApiParams:
    """Query Params Dataclass for Event API requests

    * TODO add remaining query parameters from
    https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
    * TODO write methods to concatenate list[str] values
    * TODO write methods to cast int into str values to send request
    * TODO write methods to validate values such as country_code, start_date, end_date, locale
    * TODO write functionality, that Class EventApiPAram can
    not only be used for search-event endpoint but also for search-venue endpoint,
    * TODO although not all params are compatible

    Parameters
    ----------
    id : str | None, optional
        Filter entities by its id. _By default `None`._
    keyword : str | None, optional
        Keyword to search on. _By default `None`._
    attraction_id : str | None, optional
        Filter by attraction id. _By default `None`._
    venue_id : str | None, optional
        Filter by venue id. _By default `None`._
    postal_code : str | None, optional
        Filter by postal code / zipcode. _By default `None`._
    radius : int | None, optional
        Radius of the area in which we want to search for events. _By default `None`._
    unit : UnitEnum, optional
        Unit of the radius. _By default `UnitEnum.KILOMETER`._
    locale : list[str], optional
        The locale in ISO code format. Multiple comma-separated values can be provided.
        When omitting the country part of the code (e.g. only `en` or `fr`) then
        the first matching locale is used. When using a `*` it matches all locales.
        can only be used at the end (e.g. `en-us`, `en`, `de`, `*`). _By default `["de"]`._
    start_date_time : str | None, optional
        Filter with a start date after this date. _By default `None`._
    end_date_time : str | None, optional
        Filter with a start date before this date. _By default `None`._
    size : int, optional
        Page size of the response. _By default `20`._
    page : int, optional
        Page number. _By default `0`._
    sort : SortEnum, optional
        Sorting order of the search result. Allowable Values: `name,asc`, `name,desc`, `relevance,asc`,
        `relevance,desc`, `distance,asc`, `distance,desc`, `random`. _By default `SortEnum.RELEVANCE_DESC`._
    city : list[str] | None, optional
        Filter by city. _By default `None`._
    country_code : str | None, optional
        Filter by country code. _By default `None`._
    state_code : str | None, optional
        Filter by state code. _By default `None`._
    classification_name : list[str] | None, optional
        Filter by classification name: name of any segment, genre, sub-genre, type, sub-type.
        Negative filtering is supported by using the following format '-'.
        Be aware that negative filters may cause decreased performance. _By default `None`._
    classification_id : list[str] | None, optional
        Filter by classification id: id of any segment, genre, sub-genre, type, sub-type.
        Negative filtering is supported by using the following format '-'.
        Be aware that negative filters may cause decreased performance. _By default `None`._
    include_family : bool, optional
        Filter by classification that are family-friendly. Defaults to yes. _By default `None`._
    geo_point : str | None, optional
        Filter events by geoHash. _By default `None`._
    """

    id: str | None = None
    keyword: str | None = None
    attraction_id: str | None = None
    venue_id: str | None = None
    postal_code: str | None = None
    radius: int | None = None
    unit: UnitEnum = UnitEnum.KILOMETER
    locale: list[str] = ["de"]
    start_date_time: str | None = None
    end_date_time: str | None = None
    size: int = 20
    page: int = 0
    sort: SortEnum = SortEnum.RELEVANCE_DESC
    city: list[str] | None = None
    country_code: str | None = None
    state_code: str | None = None
    classification_name: list[str] | None = None
    classification_id: list[str] | None = None
    include_family: bool | None = None
    geo_point: str | None = None
