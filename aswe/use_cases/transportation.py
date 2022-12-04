from datetime import datetime

from loguru import logger

from aswe.api.calendar.calendar import get_next_event_today
from aswe.api.navigation.vvs import get_next_connection
from aswe.api.weather.weather import WeatherApi
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase


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

        vvs_response = ""
        trip = None
        if end_location != "":
            start_location = self.user.address.vvs_id

            trip = get_next_connection(start_location, end_location)
            if trip is not None:
                vvs_response = "You can take the"
                for i, con in enumerate(trip.connections):
                    if i != 0:
                        vvs_response += " then the"
                    vvs_response += f" {con.train_name} from {con.start_location} to {con.end_location} at {con.start_time.strftime('%H:%M')}"
                vvs_response += f". You would arrive at {trip.connections[-1].end_time.strftime('%H:%M')} after {trip.duration} minutes. "

        next_event = get_next_event_today()
        next_event_announcement = "You do not have any more events today. "
        if next_event:
            event_start_time = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00").strftime("%H:%M")
            next_event_announcement = f"Your next Event is {next_event.title} at {event_start_time}. "
            if (
                trip is not None
                and datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00") < trip.connections[-1].end_time
            ):
                next_event_announcement += (
                    "If you take the train, you are still on a train when the next event starts. "
                )

        output = bicycle_response + vvs_response + next_event_announcement
        self.tts.convert_text(output)
