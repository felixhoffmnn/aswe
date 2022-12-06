from enum import Enum


class IncludeEnum(str, Enum):
    """Enum of possible include parameters for weather API"""

    DAYS = "days"
    "daily data"

    HOURS = "hours"
    "hourly data"

    ALERTS = "alerts"
    "weather alerts"

    CURRENT = "current"
    "current conditions or conditions at requested time."

    EVENTS = "events"
    "historical events such as a hail, tornadoes, wind damage and earthquakes (not enabled by default)"

    OBS = "obs"
    "historical observations from weather stations"

    REMOTE = "remote"
    "historical observations from remote source such as satellite or radar"

    FORECAST = "fcst"
    "forecast based on 16 day models."

    STATS = "stats"
    "historical statistical normals and daily statistical forecast"

    STATS_FORECAST = "statsfcst"
    """use the full statistical forecast information for dates in the future beyond the current model forecast.
    Permits hourly statistical forecast."""


class ElementsEnum(str, Enum):
    """Enum of possible element parameters for weather API"""

    CLOUDCOVER = "cloudcover"
    "how much of the sky is covered in cloud ranging from 0-100%"

    CONDITIONS = "conditions"
    "textual representation of the weather conditions. See Weather Data Conditions."

    DESCRIPTION = "description"
    """longer text descriptions suitable for displaying in weather displays. The descriptions combine the main
    features of the weather for the day such as precipitation or amount of cloud cover. Daily descriptions are
    provided for historical and forecast days. When the timeline request includes the model forecast period, a
    seven day outlook description is provided at the root response level."""

    DATETIME = "datetime"
    """ISO formatted date, time or datetime value indicating the date and time of the weather data in the local
    time zone of the requested location"""

    DATETIME_EPOCH = "datetimeEpoch"
    "number of seconds since 1st January 1970 in UTC time"

    TZOFFSET = "tzoffset"
    """the time zone offset in hours. This will only occur in the data object if it is different from the global
    time zone offset."""

    DEW = "dew"
    "dew point temperature"

    FEELSLIKE = "feelslike"
    """what the temperature feels like accounting for heat index or wind chill. Daily values are average values
    (mean) for the day."""

    FEELSLIKE_MAX = "feelslikemax"
    " (day only) maximum feels like temperature at the location."

    FEELSLIKE_MIN = "feelslikemin"
    " (day only) minimum feels like temperature at the location."

    HOURS = "hours"
    "array of hourly weather data objects. This is a child of each of the daily weather object when hours are selected."

    HUMIDITY = "humidity"
    "relative humidity in %"

    ICON = "icon"
    "a fixed, machine readable summary that can be used to display an icon"

    MOON_PHASE = "moonphase"
    """represents the fractional portion through the current moon lunation cycle ranging from 0 (the new moon) to 0.5
    (the full moon) and back to 1 (the next new moon)"""

    NORMAL = "normal"
    """array of normal weather data values - Each weather data normal is an array of three values representing,
    in order, the minimum value over the statistical period, the mean value, and the maximum value over the
    statistical period."""

    OFFSET_SECONDS = "offsetseconds"
    """(hourly only) time zone offset for this weather data object in seconds - This value may change for
    a location based on daylight saving time observation."""

    PRECIP = "precip"
    """the amount of liquid precipitation that fell or is predicted to fall in the period. This includes
    the liquid-equivalent amount of any frozen precipitation such as a snow or ice."""

    PRECIP_COVER = "precipcover"
    "(days only) the proportion of hours where there was non-zero precipitation"

    PRECIP_PROB = "precipprob"
    " (forecast only) the likelihood of measurable precipitation ranging from 0% to 100%"

    PRECIP_TYPE = "preciptype"
    """an array indicating the type(s) of precipitation expected or that occurred. Possible values include rain, snow,
    freezingrain and ice."""

    PRESSURE = "pressure"
    "the sea level atmospheric or barometric pressure in millibars (or hectopascals)"

    SNOW = "snow"
    "the amount of snow that fell or is predicted to fall"

    SNOW_DEPTH = "snowdepth"
    "the depth of snow on the ground"

    SOURCE = "source"
    """the type of weather data used for this weather object. - Values include historical observation (“obs”), forecast
    (“fcst”), historical forecast (“histfcst”) or statistical forecast (“stats”). If multiple types are used in the
    same day, “comb” is used. Today a combination of historical observations and forecast data."""

    STATIONS = "stations"
    " (historical only) the weather stations used when collecting an historical observation record"

    SUNRISE = "sunrise"
    " (day only) The formatted time of the sunrise (For example “2022-05-23T05:50:40”)"

    SUNRISE_EPOCH = "sunriseEpoch"
    "sunrise time specified as number of seconds since 1st January 1970 in UTC time"

    SUNSET = "sunset"
    "The formatted time of the sunset (For example “2022-05-23T20:22:29”)"

    SUNSET_EPOCH = "sunsetEpoch"
    "sunset time specified as number of seconds since 1st January 1970 in UTC time"

    MOONRISE = "moonrise"
    "(day only, optional) The formatted time of the moonrise (For example “2022-05-23T02:38:10”)"

    MOORISE_EPOCH = "moonriseEpoch"
    "(day only, optional) moonrise time specified as number of seconds since 1st January 1970 in UTC time"

    MOONSET = "moonset"
    "(day only, optional) The formatted time of the moonset (For example “2022-05-23T13:40:07”)"

    MOONSET_EPOCH = "moonsetEpoch"
    "(day only, optional) moonset time specified as number of seconds since 1st January 1970 in UTC time"

    TEMP = "temp"
    "temperature at the location. Daily values are average values (mean) for the day."

    TEMP_MAX = "tempmax"
    "(day only) maximum temperature at the location."

    TEMP_MIN = "tempmin"
    "(day only) minimum temperature at the location."

    UV_INDEX = "uvindex"
    """a value between 0 and 10 indicating the level of ultra violet (UV) exposure for that hour or day. 10 represents
    high level of exposure, and 0 represents no exposure. The UV index is calculated based on amount of short wave
    solar radiation which in turn is a level the cloudiness, type of cloud, time of day, time of year and location
    altitude. Daily values represent the maximum value of the hourly values."""

    VISIBILITY = "visibility"
    "distance at which distant objects are visible"

    WIND_DIR = "winddir"
    "direction from which the wind is blowing"

    WIND_GUST = "windgust"
    """instantaneous wind speed at a location - May be empty if it is not significantly higher than the wind speed.
    Daily values are the maximum hourly value for the day."""

    WIND_SPEED = "windspeed"
    """the sustained wind speed measured as the average windspeed that occurs during the preceding one to two minutes.
    Daily values are the maximum hourly value for the day."""

    WIND_SPEED_MAX = "windspeedmax"
    "(day only, optional) maximum wind speed over the day."

    WIND_SPEED_MEAN = "windspeedmean"
    "(day only , optional ) average (mean) wind speed over the day."

    WIND_SPEED_MIN = "windspeedmin"
    "(day only , optional ) minimum wind speed over the day."

    SOLAR_RADIATION = "solarradiation"
    """(W/m2) the solar radiation power at the instantaneous moment of the observation (or forecast prediction).
    See the full solar radiation data documentation and Wind and Solar Energy pages ."""

    SOLAR_ENERGY = "solarenergy"
    """(MJ /m2 ) indicates the total energy from the sun that builds up over an hour or day. See the full solar
    radiation data documentation and Wind and Solar Energy pages ."""

    SEVERE_RISK = "severerisk"
    """(forecast only) a value between 0 and 100 representing the risk of convective storms
    (eg thunderstorms, hail and tornadoes). It is a scaled measure that combines a variety of other fields
    such as the convective available potential energy (CAPE) and convective inhibition (CIN), predicted rain and
    wind. Typically a value less than 30 indicates a low risk, between 30 and 70 a moderate risk and above 70 a
    high risk."""

    CAPE = "cape"
    """(forecast only) convective available potential energy. This is a numbering indicating amount of energy
    available to produce thunderstorms. A higher values indicates a more unstable atmosphere capable of creating
    stronger storms. Values lower than 1000 J/kg indicate generally low instability, between 1000-2500 J/kg medium
    instability and 2500-4000 J/kg high instability. Values greater than 4000 J/kg indicating an extremely unstable
    atmosphere."""

    CIN = "cin"
    """(forecast only) convective inhibition. A number representing the level of atmospheric tendency to
    prevent instability and therefore prevent thunderstorms."""

    DEGREE_DAYS = "degreedays"
    """(day only) optional elements indicating the number of degree days for this date. See the degree days API
    for more information on degree days. To turn degree days and degree day accumulation on, use the elements
    parameter. For example, elements=datetime,tempmax,tempmin,degreedays,accdegreedays."""


class DynamicPeriodEnum(str, Enum):
    """Enum of possible dynamic periods for weather API"""

    TODAY = "today"
    "from midnight to the current time at the requested location."

    YESTERDAY = "yesterday"
    "from midnight to midnight on yesterday's date."

    YEART_TO_DATE = "yeartodate"
    "from midnight of January 1st of the current year until the current date time."

    MONTH_TO_DATE = "monthtodate"
    "from midnight on the 1st of the current month until the current date time."

    LAST_YEAR = "lastyear"
    "the one year period ending on yesterday's date."

    LAST_24_HOURS = "last24hours"
    "the 24 hour period ending at the current time (rounded to the currenthour)."

    NEXT_WEEKEND = "nextweekend"
    """the next occurrence of the weekend after today's day.
    Weekend is defined as Saturday and Sunday.
    Please let us know if you would like additional weekend definitions added."""

    LAST_WEEKEND = "lastweekend"
    """the last occurrence of the weekend before today's day.
    Weekend is defined as Saturday and Sunday.
    Please let us know if you would like additional weekend definitions added."""

    @classmethod
    def last_weekday(cls, weekday: str) -> str:
        """the last occurrence of the named day of week before today’s day. For example lastsaturday"""
        if weekday.lower() not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            raise Exception(f"Given weekday is invalid: {weekday}")

        return f"last{weekday.lower()}"

    @classmethod
    def next_weekday(cls, weekday: str) -> str:
        """the next occurrence of the named day of week after today's day. For example nextsaturday"""
        if weekday.lower() not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            raise Exception(f"Given weekday is invalid: {weekday}")
        return f"next{weekday.lower()}"

    @classmethod
    def next_x_days(cls, days_count: int) -> str:
        """the period including and after today's date with a length on the number of days specified.
        For example next7days or next21days."""
        if days_count <= 0:
            raise Exception(f"Given day count is invalid: {days_count} <= 0")

        return f"next{days_count}days"

    @classmethod
    def last_x_days(cls, days_count: int) -> str:
        """the period before today's date with a length on the number of days specified.
        For example last7days or last21days."""
        if days_count <= 0:
            raise Exception(f"Given day count is invalid: {days_count} <= 0")

        return f"last{days_count}days"
