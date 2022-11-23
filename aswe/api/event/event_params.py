# pylint: disable=invalid-name

from dataclasses import dataclass, field
from enum import Enum

from loguru import logger

from aswe.utils.validate import validate_date


class UnitEnum(str, Enum):
    """Enum of possible radius values for Event API Params"""

    MILES = "miles"
    KILOMETER = "km"


class SortEnum(str, Enum):
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
class EventApiEventParams:
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

    unit: UnitEnum = UnitEnum.KILOMETER
    """Unit of the radius. Defaults to \"km\""""

    locale: list[str] = field(default_factory=lambda: ["de"])
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

    sort: SortEnum | None = None
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

    def validate_fields(self) -> bool:
        """Validates fields"""
        is_valid = True

        if self.radius is not None and self.radius <= 0:
            logger.error(f"Radius cannot be below or equal to 0. {self.radius} was given.")
            is_valid = False

        for index, locale_elmnt in enumerate(self.locale):
            try:
                lang, country = locale_elmnt.split("-")

                if len(lang) != 2 or len(country) != 2:
                    logger.error(f"Given local element is invalid: language: {lang}, country: {country}")
                    is_valid = False
            except ValueError:
                if len(locale_elmnt) != 2 and (locale_elmnt != "*" or index != len(self.locale) - 1):
                    logger.error(f"Given local element is invalid: locale_elmnt: {locale_elmnt}")
                    is_valid = False

        if self.start_date_time is not None and validate_date(self.start_date_time, True) is False:
            logger.error(f"Given start_date_time is invalid: {self.start_date_time}")
            is_valid = False

        if self.end_date_time is not None and validate_date(self.end_date_time, True) is False:
            logger.error(f"Given end_date_time is invalid: {self.end_date_time}")
            is_valid = False

        if (
            self.start_date_time is not None
            and self.end_date_time is not None
            and self.end_date_time <= self.start_date_time
        ):
            logger.error(
                f"start_date_time ({self.start_date_time}) must be before end_date_time ({self.end_date_time})."
            )
            is_valid = False

        if self.size is not None and self.size <= 0:
            logger.error(f"Size cannot be below or equal to 0. {self.size} was given.")
            is_valid = False

        if self.page is not None and self.page <= 0:
            logger.error(f"Page cannot be below or equal to 0. {self.page} was given.")
            is_valid = False

        if self.country_code is not None and len(self.country_code) != 2:
            logger.error(f"Country Code seems to be invaid: {self.country_code}. Should be of length 2.")
            is_valid = False

        return is_valid

    def concat_to_query(self) -> str:
        """
        Concatenates all fields to a string so that query can be appended to the request url
        Assumes all query fields were validated before, using `validate_fields` class method.
        """
        query = ""

        if self.id:
            query += f"id={self.id}&"
        if self.keyword:
            query += f"keyword={self.keyword}&"
        if self.attraction_id:
            query += f"attractionId={self.attraction_id}&"
        if self.venue_id:
            query += f"venueId={self.venue_id}&"
        if self.postal_code:
            query += f"postalCode={self.postal_code}&"
        if self.radius:
            query += f"radius={self.radius}&"
        if self.unit:
            query += f"unit={self.unit.value}&"
        if self.locale:
            query += f"""locale={",".join(self.locale)}&"""
        if self.start_date_time:
            query += f"startDateTime={self.start_date_time}&"
        if self.end_date_time:
            query += f"endDateTime={self.end_date_time}&"
        if self.size:
            query += f"size={self.size}&"
        if self.page:
            query += f"page={self.page}&"
        if self.sort:
            query += f"sort={self.sort.value}&"
        if self.city:
            query += f"""city={",".join(self.city)}&"""
        if self.country_code:
            query += f"countryCode={self.country_code}&"
        if self.classification_name:
            query += f"""classificationName={",".join(self.classification_name)}&"""
        if self.classification_id:
            query += f"""classificationId={",".join(self.classification_id)}&"""
        if self.include_family is not None:
            query += f"includeFamily={self.include_family}&"
        if self.geo_point:
            query += f"geoPoint={self.geo_point}&"

        return query[:-1]


@dataclass
class EventApiClassificationParams:
    """Query Params Dataclass for Event API Classification requests"""

    id: str | None = None
    """Filter entities by its id"""

    keyword: str | None = None
    """Keyword to search on"""

    size: int | None = None
    """Page size of the response. Defaults to 20."""

    sort: SortEnum | None = None
    """Sorting order of the search result. Allowable Values: \"name,asc\", \"name,desc\", \"relevance,asc\",
    \"relevance,desc\", \"distance,asc\", \"distance,desc\", \"random\".
    Defaults to \"relevance,desc\""""

    def validate_fields(self) -> bool:
        """Validates fields"""

        is_valid = True

        if self.size is not None and self.size <= 0:
            logger.error(f"Size cannot be below or equal to 0. {self.size} was given.")
            is_valid = False

        return is_valid

    def concat_to_query(self) -> str:
        """
        Concatenates all fields to a string so that query can be appended to the request url
        Assumes all query fields were validated before, using `validate_fields` class method.
        """
        query = ""

        if self.id:
            query += f"id={self.id}&"
        if self.keyword:
            query += f"keyword={self.keyword}&"
        if self.size:
            query += f"size={self.size}&"
        if self.sort:
            query += f"sort={self.sort.value}&"

        return query[:-1]
