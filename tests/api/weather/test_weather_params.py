import pytest

from aswe.api.weather.weather_params import _DynamicPeriod, _Elements, _Include


def test_include_enum_values() -> None:
    """Test values of `Include` Enum Class"""

    assert _Include.DAYS == "days"
    assert _Include.HOURS == "hours"
    assert _Include.ALERTS == "alerts"
    assert _Include.CURRENT == "current"
    assert _Include.EVENTS == "events"
    assert _Include.OBS == "obs"
    assert _Include.REMOTE == "remote"
    assert _Include.FORECAST == "fcst"
    assert _Include.STATS == "stats"
    assert _Include.STATS_FORECAST == "statsfcst"


def test_include_has_value() -> None:
    """Test `has_value` function of `Include` Class"""

    valid_value = "days"
    invalid_value = "lorem ipsum"

    assert _Include.has_value(valid_value) is True
    assert _Include.has_value(invalid_value) is False


def test_elements_enum_values() -> None:
    """Test values of `Elements` Enum Class"""

    assert _Elements.CLOUDCOVER == "cloudcover"
    assert _Elements.CONDITIONS == "conditions"
    assert _Elements.DESCRIPTION == "description"
    assert _Elements.DATETIME == "datetime"
    assert _Elements.DATETIME_EPOCH == "datetimeEpoch"
    assert _Elements.TZOFFSET == "tzoffset"
    assert _Elements.DEW == "dew"
    assert _Elements.FEELSLIKE == "feelslike"
    assert _Elements.FEELSLIKE_MAX == "feelslikemax"
    assert _Elements.FEELSLIKE_MIN == "feelslikemin"
    assert _Elements.HOURS == "hours"
    assert _Elements.HUMIDITY == "humidity"
    assert _Elements.ICON == "icon"
    assert _Elements.MOON_PHASE == "moonphase"
    assert _Elements.NORMAL == "normal"
    assert _Elements.OFFSET_SECONDS == "offsetseconds"
    assert _Elements.PRECIP == "precip"
    assert _Elements.PRECIP_COVER == "precipcover"
    assert _Elements.PRECIP_PROB == "precipprob"
    assert _Elements.PRECIP_TYPE == "preciptype"
    assert _Elements.PRESSURE == "pressure"
    assert _Elements.SNOW == "snow"
    assert _Elements.SNOW_DEPTH == "snowdepth"
    assert _Elements.SOURCE == "source"
    assert _Elements.STATIONS == "stations"
    assert _Elements.SUNRISE == "sunrise"
    assert _Elements.SUNRISE_EPOCH == "sunriseEpoch"
    assert _Elements.SUNSET == "sunset"
    assert _Elements.SUNSET_EPOCH == "sunsetEpoch"
    assert _Elements.MOONRISE == "moonrise"
    assert _Elements.MOORISE_EPOCH == "moonriseEpoch"
    assert _Elements.MOONSET == "moonset"
    assert _Elements.MOONSET_EPOCH == "moonsetEpoch"
    assert _Elements.TEMP == "temp"
    assert _Elements.TEMP_MAX == "tempmax"
    assert _Elements.TEMP_MIN == "tempmin"
    assert _Elements.UV_INDEX == "uvindex"
    assert _Elements.VISIBILITY == "visibility"
    assert _Elements.WIND_DIR == "winddir"
    assert _Elements.WIND_GUST == "windgust"
    assert _Elements.WIND_SPEED == "windspeed"
    assert _Elements.WIND_SPEED_MAX == "windspeedmax"
    assert _Elements.WIND_SPEED_MEAN == "windspeedmean"
    assert _Elements.WIND_SPEED_MIN == "windspeedmin"
    assert _Elements.SOLAR_RADIATION == "solarradiation"
    assert _Elements.SOLAR_ENERGY == "solarenergy"
    assert _Elements.SEVERE_RISK == "severerisk"
    assert _Elements.CAPE == "cape"
    assert _Elements.CIN == "cin"
    assert _Elements.DEGREE_DAYS == "degreedays"


def test_elements_has_value() -> None:
    """Test `has_value` function of `Elements` Class"""

    valid_value = "cloudcover"
    invalid_value = "lorem ipsum"

    assert _Elements.has_value(valid_value) is True
    assert _Elements.has_value(invalid_value) is False


def test_dynamic_period_enum_values() -> None:
    """Test values of `_DynamicPeriod` Enum Class"""

    assert _DynamicPeriod.TODAY == "today"
    assert _DynamicPeriod.YESTERDAY == "yesterday"
    assert _DynamicPeriod.YEART_TO_DATE == "yeartodate"
    assert _DynamicPeriod.MONTH_TO_DATE == "monthtodate"
    assert _DynamicPeriod.LAST_YEAR == "lastyear"
    assert _DynamicPeriod.LAST_24_HOURS == "last24hours"
    assert _DynamicPeriod.NEXT_WEEKEND == "nextweekend"
    assert _DynamicPeriod.LAST_WEEKEND == "lastweekend"


def test_dynamic_period_has_value() -> None:
    """Test `has_value` function of `_DynamicPeriod` Class"""

    valid_value = "today"
    invalid_value = "lorem ipsum"

    assert _DynamicPeriod.has_value(valid_value) is True
    assert _DynamicPeriod.has_value(invalid_value) is False


def test_dynamic_period_last_weekday() -> None:
    """Test `last_weekday` function of `_DynamicPeriod` Class"""

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        assert _DynamicPeriod.last_weekday(weekday) == f"last{weekday}"
        assert _DynamicPeriod.last_weekday(weekday.upper()) == f"last{weekday}"

    with pytest.raises(Exception, match="Given weekday is invalid: lorem ipsum"):
        _DynamicPeriod.last_weekday("lorem ipsum")


def test_dynamic_period_next_weekday() -> None:
    """Test `next_weekday` function of `_DynamicPeriod` Class"""

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        assert _DynamicPeriod.next_weekday(weekday) == f"next{weekday}"
        assert _DynamicPeriod.next_weekday(weekday.upper()) == f"next{weekday}"

    with pytest.raises(Exception, match="Given weekday is invalid: lorem ipsum"):
        _DynamicPeriod.next_weekday("lorem ipsum")


def test_dynamic_period_last_x_days() -> None:
    """Test `last_x_days` function of `_DynamicPeriod` Class"""

    assert _DynamicPeriod.last_x_days(10) == "last10days"

    with pytest.raises(Exception, match="Given day count is invalid: 0 <= 0"):
        _DynamicPeriod.last_x_days(0)

    with pytest.raises(Exception, match="Given day count is invalid: -1 <= 0"):
        _DynamicPeriod.last_x_days(-1)


def test_dynamic_period_next_x_days() -> None:
    """Test `next_x_days` function of `_DynamicPeriod` Class"""

    assert _DynamicPeriod.next_x_days(10) == "next10days"

    with pytest.raises(Exception, match="Given day count is invalid: 0 <= 0"):
        _DynamicPeriod.next_x_days(0)

    with pytest.raises(Exception, match="Given day count is invalid: -1 <= 0"):
        _DynamicPeriod.next_x_days(-1)
