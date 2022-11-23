import pytest

from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum


def test_include_enum_values() -> None:
    """Test values of `Include` Enum Class"""

    assert IncludeEnum.DAYS.value == "days"
    assert IncludeEnum.HOURS.value == "hours"
    assert IncludeEnum.ALERTS.value == "alerts"
    assert IncludeEnum.CURRENT.value == "current"
    assert IncludeEnum.EVENTS.value == "events"
    assert IncludeEnum.OBS.value == "obs"
    assert IncludeEnum.REMOTE.value == "remote"
    assert IncludeEnum.FORECAST.value == "fcst"
    assert IncludeEnum.STATS.value == "stats"
    assert IncludeEnum.STATS_FORECAST.value == "statsfcst"


def test_include_has_value() -> None:
    """Test `has_value` function of `Include` Class"""

    valid_value = "days"
    invalid_value = "lorem ipsum"

    assert IncludeEnum.has_value(valid_value) is True
    assert IncludeEnum.has_value(invalid_value) is False


def test_elements_enum_values() -> None:
    """Test values of `Elements` Enum Class"""

    assert ElementsEnum.CLOUDCOVER.value == "cloudcover"
    assert ElementsEnum.CONDITIONS.value == "conditions"
    assert ElementsEnum.DESCRIPTION.value == "description"
    assert ElementsEnum.DATETIME.value == "datetime"
    assert ElementsEnum.DATETIME_EPOCH.value == "datetimeEpoch"
    assert ElementsEnum.TZOFFSET.value == "tzoffset"
    assert ElementsEnum.DEW.value == "dew"
    assert ElementsEnum.FEELSLIKE.value == "feelslike"
    assert ElementsEnum.FEELSLIKE_MAX.value == "feelslikemax"
    assert ElementsEnum.FEELSLIKE_MIN.value == "feelslikemin"
    assert ElementsEnum.HOURS.value == "hours"
    assert ElementsEnum.HUMIDITY.value == "humidity"
    assert ElementsEnum.ICON.value == "icon"
    assert ElementsEnum.MOON_PHASE.value == "moonphase"
    assert ElementsEnum.NORMAL.value == "normal"
    assert ElementsEnum.OFFSET_SECONDS.value == "offsetseconds"
    assert ElementsEnum.PRECIP.value == "precip"
    assert ElementsEnum.PRECIP_COVER.value == "precipcover"
    assert ElementsEnum.PRECIP_PROB.value == "precipprob"
    assert ElementsEnum.PRECIP_TYPE.value == "preciptype"
    assert ElementsEnum.PRESSURE.value == "pressure"
    assert ElementsEnum.SNOW.value == "snow"
    assert ElementsEnum.SNOW_DEPTH.value == "snowdepth"
    assert ElementsEnum.SOURCE.value == "source"
    assert ElementsEnum.STATIONS.value == "stations"
    assert ElementsEnum.SUNRISE.value == "sunrise"
    assert ElementsEnum.SUNRISE_EPOCH.value == "sunriseEpoch"
    assert ElementsEnum.SUNSET.value == "sunset"
    assert ElementsEnum.SUNSET_EPOCH.value == "sunsetEpoch"
    assert ElementsEnum.MOONRISE.value == "moonrise"
    assert ElementsEnum.MOORISE_EPOCH.value == "moonriseEpoch"
    assert ElementsEnum.MOONSET.value == "moonset"
    assert ElementsEnum.MOONSET_EPOCH.value == "moonsetEpoch"
    assert ElementsEnum.TEMP.value == "temp"
    assert ElementsEnum.TEMP_MAX.value == "tempmax"
    assert ElementsEnum.TEMP_MIN.value == "tempmin"
    assert ElementsEnum.UV_INDEX.value == "uvindex"
    assert ElementsEnum.VISIBILITY.value == "visibility"
    assert ElementsEnum.WIND_DIR.value == "winddir"
    assert ElementsEnum.WIND_GUST.value == "windgust"
    assert ElementsEnum.WIND_SPEED.value == "windspeed"
    assert ElementsEnum.WIND_SPEED_MAX.value == "windspeedmax"
    assert ElementsEnum.WIND_SPEED_MEAN.value == "windspeedmean"
    assert ElementsEnum.WIND_SPEED_MIN.value == "windspeedmin"
    assert ElementsEnum.SOLAR_RADIATION.value == "solarradiation"
    assert ElementsEnum.SOLAR_ENERGY.value == "solarenergy"
    assert ElementsEnum.SEVERE_RISK.value == "severerisk"
    assert ElementsEnum.CAPE.value == "cape"
    assert ElementsEnum.CIN.value == "cin"
    assert ElementsEnum.DEGREE_DAYS.value == "degreedays"


def test_elements_has_value() -> None:
    """Test `has_value` function of `Elements` Class"""

    valid_value = "cloudcover"
    invalid_value = "lorem ipsum"

    assert ElementsEnum.has_value(valid_value) is True
    assert ElementsEnum.has_value(invalid_value) is False


def test_dynamic_period_enum_values() -> None:
    """Test values of `_DynamicPeriod` Enum Class"""

    assert DynamicPeriodEnum.TODAY.value == "today"
    assert DynamicPeriodEnum.YESTERDAY.value == "yesterday"
    assert DynamicPeriodEnum.YEART_TO_DATE.value == "yeartodate"
    assert DynamicPeriodEnum.MONTH_TO_DATE.value == "monthtodate"
    assert DynamicPeriodEnum.LAST_YEAR.value == "lastyear"
    assert DynamicPeriodEnum.LAST_24_HOURS.value == "last24hours"
    assert DynamicPeriodEnum.NEXT_WEEKEND.value == "nextweekend"
    assert DynamicPeriodEnum.LAST_WEEKEND.value == "lastweekend"


def test_dynamic_period_has_value() -> None:
    """Test `has_value` function of `_DynamicPeriod` Class"""

    valid_value_1 = "today"
    valid_value_2 = "next0days"
    valid_value_3 = "nextmonday"
    invalid_value = "lorem ipsum"

    assert DynamicPeriodEnum.has_value(valid_value_1) is True
    assert DynamicPeriodEnum.has_value(valid_value_2) is True
    assert DynamicPeriodEnum.has_value(valid_value_3) is True
    assert DynamicPeriodEnum.has_value(invalid_value) is False


def test_dynamic_period_last_weekday() -> None:
    """Test `last_weekday` function of `_DynamicPeriod` Class"""

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        assert DynamicPeriodEnum.last_weekday(weekday) == f"last{weekday}"
        assert DynamicPeriodEnum.last_weekday(weekday.upper()) == f"last{weekday}"

    with pytest.raises(Exception, match="Given weekday is invalid: lorem ipsum"):
        DynamicPeriodEnum.last_weekday("lorem ipsum")


def test_dynamic_period_next_weekday() -> None:
    """Test `next_weekday` function of `_DynamicPeriod` Class"""

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    for weekday in weekdays:
        assert DynamicPeriodEnum.next_weekday(weekday) == f"next{weekday}"
        assert DynamicPeriodEnum.next_weekday(weekday.upper()) == f"next{weekday}"

    with pytest.raises(Exception, match="Given weekday is invalid: lorem ipsum"):
        DynamicPeriodEnum.next_weekday("lorem ipsum")


def test_dynamic_period_last_x_days() -> None:
    """Test `last_x_days` function of `_DynamicPeriod` Class"""

    assert DynamicPeriodEnum.last_x_days(10) == "last10days"

    with pytest.raises(Exception, match="Given day count is invalid: 0 <= 0"):
        DynamicPeriodEnum.last_x_days(0)

    with pytest.raises(Exception, match="Given day count is invalid: -1 <= 0"):
        DynamicPeriodEnum.last_x_days(-1)


def test_dynamic_period_next_x_days() -> None:
    """Test `next_x_days` function of `_DynamicPeriod` Class"""

    assert DynamicPeriodEnum.next_x_days(10) == "next10days"

    with pytest.raises(Exception, match="Given day count is invalid: 0 <= 0"):
        DynamicPeriodEnum.next_x_days(0)

    with pytest.raises(Exception, match="Given day count is invalid: -1 <= 0"):
        DynamicPeriodEnum.next_x_days(-1)
