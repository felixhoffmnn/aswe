from aswe.api.event.event_params import EventApiEventParams, SortEnum, UnitEnum


def test_unit_enum_values() -> None:
    """Test values of `UnitEnum` Enum Class"""

    assert UnitEnum.MILES.value == "miles"
    assert UnitEnum.KILOMETER.value == "km"


def test_sort_enum_values() -> None:
    """Test values of `SortEnum` Enum Class"""

    assert SortEnum.NAME_ASC.value == "name,asc"
    assert SortEnum.NAME_DESC.value == "name,desc"
    assert SortEnum.RELEVANCE_ASC.value == "relevance,asc"
    assert SortEnum.RELEVANCE_DESC.value == "relevance,desc"
    assert SortEnum.DISTANCE_ASC.value == "distance,asc"
    assert SortEnum.DISTANCE_DESC.value == "distance,desc"


def test_event_params_validate_fields() -> None:
    """Test `aswe.api.event.event_params.EventApiEventParams.validate_fields` method"""

    default_params = EventApiEventParams()

    assert default_params.validate_fields() is True

    zero_integer = EventApiEventParams(radius=0, size=0, page=0)
    negative_integer = EventApiEventParams(radius=-1, size=-1, page=-1)

    assert zero_integer.validate_fields() is False
    assert negative_integer.validate_fields() is False

    too_long_locale_country = EventApiEventParams(locale=["en-usa"])
    too_long_locale_lang = EventApiEventParams(locale=["eng"])
    asterisk_wrong_pos = EventApiEventParams(locale=["de", "*", "de-at"])

    assert too_long_locale_country.validate_fields() is False
    assert too_long_locale_lang.validate_fields() is False
    assert asterisk_wrong_pos.validate_fields() is False

    invalid_start_date = EventApiEventParams(start_date_time="2020-12-12")
    invalid_end_date = EventApiEventParams(end_date_time="2020-12-12")
    end_before_start_date = EventApiEventParams(
        start_date_time="2021-12-12T00:00:00Z", end_date_time="2020-12-12T00:00:00Z"
    )

    assert invalid_start_date.validate_fields() is False
    assert invalid_end_date.validate_fields() is False
    assert end_before_start_date.validate_fields() is False

    invalid_country_code = EventApiEventParams(country_code="usa")

    assert invalid_country_code.validate_fields() is False


def test_event_params_concat_to_query() -> None:
    """Test `aswe.api.event.event_params.EventApiEventParams.concat_to_query` method"""

    full_query = EventApiEventParams(
        id="id",
        keyword="keyword",
        attraction_id="attraction_id",
        venue_id="venue_id",
        postal_code="postal_code",
        radius=10,
        unit=UnitEnum.KILOMETER,
        locale=["de", "en"],
        start_date_time="2020-12-12",
        end_date_time="2021-12-12",
        size=10,
        page=10,
        sort=SortEnum.DISTANCE_ASC,
        city=["Stuttgart", "Berlin"],
        country_code="DE",
        classification_name=["comedy"],
        classification_id=["some_id"],
        include_family=False,
        geo_point="some_hash",
    )

    assert full_query.concat_to_query() == (
        "id=id&keyword=keyword&attractionId=attraction_id&venueId=venue_id&postalCode=postal_code"
        "&radius=10&unit=km&locale=de,en&startDateTime=2020-12-12&endDateTime=2021-12-12&size=10&page=10"
        "&sort=distance,asc&city=Stuttgart,Berlin&countryCode=DE&classificationName=comedy"
        "&classificationId=some_id&includeFamily=False&geoPoint=some_hash"
    )
