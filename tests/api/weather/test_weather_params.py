import pytest

from src.api.weather.weather_params import DynamicPeriod, Elements, Include


def test_include_enum_values() -> None:
    """Test values of `Include` Enum Class"""

    assert Include.DAYS == "days"
    assert Include.HOURS == "hours"
    assert Include.ALERTS == "alerts"
    assert Include.CURRENT == "current"
    assert Include.EVENTS == "events"
    assert Include.OBS == "obs"
    assert Include.REMOTE == "remote"
    assert Include.FORECAST == "fcst"
    assert Include.STATS == "stats"
    assert Include.STATS_FORECAST == "statsfcst"


def test_include_has_value() -> None:
    """Test `has_value` function of `Include` Class"""

    valid_value = "days"
    invalid_value = "lorem ipsum"

    assert Include.has_value(valid_value) is True
    assert Include.has_value(invalid_value) is False


def test_elements_enum_values() -> None:
    """Test values of `Elements` Enum Class"""

    assert Elements.CLOUDCOVER == "cloudcover"
    assert Elements.CONDITIONS == "conditions"
    assert Elements.DESCRIPTION == "description"
    assert Elements.DATETIME == "datetime"
    assert Elements.DATETIME_EPOCH == "datetimeEpoch"
    assert Elements.TZOFFSET == "tzoffset"
    assert Elements.DEW == "dew"
    assert Elements.FEELSLIKE == "feelslike"
    assert Elements.FEELSLIKE_MAX == "feelslikemax"
    assert Elements.FEELSLIKE_MIN == "feelslikemin"
    assert Elements.HOURS == "hours"
    assert Elements.HUMIDITY == "humidity"
    assert Elements.ICON == "icon"
    assert Elements.MOON_PHASE == "moonphase"
    assert Elements.NORMAL == "normal"
    assert Elements.OFFSET_SECONDS == "offsetseconds"
    assert Elements.PRECIP == "precip"
    assert Elements.PRECIP_COVER == "precipcover"
    assert Elements.PRECIP_PROB == "precipprob"
    assert Elements.PRECIP_TYPE == "preciptype"
    assert Elements.PRESSURE == "pressure"
    assert Elements.SNOW == "snow"
    assert Elements.SNOW_DEPTH == "snowdepth"
    assert Elements.SOURCE == "source"
    assert Elements.STATIONS == "stations"
    assert Elements.SUNRISE == "sunrise"
    assert Elements.SUNRISE_EPOCH == "sunriseEpoch"
    assert Elements.SUNSET == "sunset"
    assert Elements.SUNSET_EPOCH == "sunsetEpoch"
    assert Elements.MOONRISE == "moonrise"
    assert Elements.MOORISE_EPOCH == "moonriseEpoch"
    assert Elements.MOONSET == "moonset"
    assert Elements.MOONSET_EPOCH == "moonsetEpoch"
    assert Elements.TEMP == "temp"
    assert Elements.TEMP_MAX == "tempmax"
    assert Elements.TEMP_MIN == "tempmin"
    assert Elements.UV_INDEX == "uvindex"
    assert Elements.VISIBILITY == "visibility"
    assert Elements.WIND_DIR == "winddir"
    assert Elements.WIND_GUST == "windgust"
    assert Elements.WIND_SPEED == "windspeed"
    assert Elements.WIND_SPEED_MAX == "windspeedmax"
    assert Elements.WIND_SPEED_MEAN == "windspeedmean"
    assert Elements.WIND_SPEED_MIN == "windspeedmin"
    assert Elements.SOLAR_RADIATION == "solarradiation"
    assert Elements.SOLAR_ENERGY == "solarenergy"
    assert Elements.SEVERE_RISK == "severerisk"
    assert Elements.CAPE == "cape"
    assert Elements.CIN == "cin"
    assert Elements.DEGREE_DAYS == "degreedays"


def test_elements_has_value() -> None:
    """Test `has_value` function of `Elements` Class"""

    valid_value = "cloudcover"
    invalid_value = "lorem ipsum"

    assert Elements.has_value(valid_value) is True
    assert Elements.has_value(invalid_value) is False


def test_dynamic_period_enum_values() -> None:
    """Test values of `DynamicPeriod` Enum Class"""

    assert DynamicPeriod.TODAY == "today"
    assert DynamicPeriod.YESTERDAY == "yesterday"
    assert DynamicPeriod.YEART_TO_DATE == "yeartodate"
    assert DynamicPeriod.MONTH_TO_DATE == "monthtodate"
    assert DynamicPeriod.LAST_YEAR == "lastyear"
    assert DynamicPeriod.LAST_24_HOURS == "last24hours"
    assert DynamicPeriod.NEXT_WEEKEND == "nextweekend"
    assert DynamicPeriod.LAST_WEEKEND == "lastweekend"


def test_dynamic_period_has_value() -> None:
    """Test `has_value` function of `DynamicPeriod` Class"""

    valid_value = "today"
    invalid_value = "lorem ipsum"

    assert DynamicPeriod.has_value(valid_value) is True
    assert DynamicPeriod.has_value(invalid_value) is False


def test_dynamic_period_last_weekday() -> None:
    """Test `last_weekday` function of `DynamicPeriod` Class"""

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        assert DynamicPeriod.last_weekday(weekday) == f"last{weekday}"
        assert DynamicPeriod.last_weekday(weekday.upper()) == f"last{weekday}"

    with pytest.raises(Exception, match="Given weekday is invalid: lorem ipsum"):
        DynamicPeriod.last_weekday("lorem ipsum")


def test_dynamic_period_next_weekday() -> None:
    """Test `next_weekday` function of `DynamicPeriod` Class"""

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        assert DynamicPeriod.next_weekday(weekday) == f"next{weekday}"
        assert DynamicPeriod.next_weekday(weekday.upper()) == f"next{weekday}"

    with pytest.raises(Exception, match="Given weekday is invalid: lorem ipsum"):
        DynamicPeriod.next_weekday("lorem ipsum")


def test_dynamic_period_last_x_days() -> None:
    """Test `last_x_days` function of `DynamicPeriod` Class"""

    assert DynamicPeriod.last_x_days(10) == "last10days"

    with pytest.raises(Exception, match="Given day count is invalid: 0 <= 0"):
        DynamicPeriod.last_x_days(0)

    with pytest.raises(Exception, match="Given day count is invalid: -1 <= 0"):
        DynamicPeriod.last_x_days(-1)


def test_dynamic_period_next_x_days() -> None:
    """Test `next_x_days` function of `DynamicPeriod` Class"""

    assert DynamicPeriod.next_x_days(10) == "next10days"

    with pytest.raises(Exception, match="Given day count is invalid: 0 <= 0"):
        DynamicPeriod.next_x_days(0)

    with pytest.raises(Exception, match="Given day count is invalid: -1 <= 0"):
        DynamicPeriod.next_x_days(-1)
