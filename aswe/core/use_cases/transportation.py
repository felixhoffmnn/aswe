from datetime import datetime

from loguru import logger
from vvspy import get_trips

from aswe.api.calendar.calendar import get_next_event_today
from aswe.api.weather.weather import WeatherApi
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.core.data import BestMatch
from aswe.utils.classes import AbstractUseCase


class TransportationUseCase(AbstractUseCase):
    """Use case for transportation"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for transportation

        * TODO: Implement `quotes_key`

        Parameters
        ----------
        best_match : BestMatch
            An object containing the best match for the user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        end_location = ""

        match best_match.function_key:
            case "dhbw":
                end_location = "de:08111:6056"  # Stadtmitte
                # raise NotImplementedError
            case "hpe":
                raise NotImplementedError
            case "ibm":
                raise NotImplementedError
            case _:
                raise NotImplementedError

        min_temp = 8
        max_precipprob = 25
        bicycle_response = "The weather is not good enough for riding a bike. "

        crawler = WeatherApi()
        weather_today = crawler.dynamic_range(
            location="Stuttgart,DE",
            dynamic_period=DynamicPeriodEnum.TODAY,
            elements=[ElementsEnum.PRECIP_PROB, ElementsEnum.TEMP],
            include=[IncludeEnum.HOURS],
        )
        cur_hour = datetime.now().hour
        weather_now = weather_today["days"][0]["hours"][cur_hour]  # type: ignore
        weather_in_an_hour = weather_today["days"][0]["hours"][(cur_hour + 1) % 24]  # type: ignore
        logger.info(f"Weather: {weather_now} ; {weather_in_an_hour}")
        if (
            weather_now["temp"] >= min_temp
            and weather_in_an_hour["temp"] >= min_temp
            and weather_now["precipprob"] <= max_precipprob
            and weather_in_an_hour["precipprob"] <= max_precipprob
        ):
            # TODO: get bicycling time from google maps API
            minutes_bike = "20"
            bicycle_response = f"If you take the bike, you will need {minutes_bike} minutes. "

        # TODO: replace start_location with user preference
        start_location = "de:08111:6002"  # Vaihingen

        vvs_routes = get_trips(start_location, end_location, limit=10)
        logger.info(vvs_routes)
        # TODO: filter important information from vvs_routes

        start_loc = "Vaihingen"
        end_loc = "Stadtmitte"
        start_in_x_min = "5"
        arrive_after = "12"
        train_name = "S1"

        next_event = get_next_event_today()
        next_event_announcement = "You do not have any more events today. "
        if next_event:
            event_start_time = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00").strftime("%H:%M")
            next_event_announcement = f"Your next Event is {next_event.title} at {event_start_time}. "

        output = (
            bicycle_response
            + f"You can take the {train_name} in {start_in_x_min} minutes from {start_loc} to arrive at {end_loc} after {arrive_after} more minutes. "
            + next_event_announcement
        )
        self.tts.convert_text(output)
