from datetime import datetime, timedelta

from loguru import logger

from aswe.api.calendar import get_next_event_today
from aswe.api.navigation import MapsTripMode, get_maps_connection, get_next_connection
from aswe.api.weather import weather as weatherApi
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase


class NavigationUseCase(AbstractUseCase):
    """Use case for navigation"""

    def check_proactivity(self) -> None:
        """Trigger proactivity if the next event is between 40 and 45 minutes in the future"""

        logger.debug("Evaluate proactivity in Navigation use case")

        next_event = get_next_event_today()
        if next_event is not None:
            next_event_start_time = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
            time_to_next_event = (next_event_start_time - datetime.now()).seconds / 60
            if 40 <= time_to_next_event < 45:

                self.next_event_use_case()

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for navigation

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

        match best_match.function_key:
            case "dhbw":
                self.vvs_trip_use_case("de:08111:6056", "Rotebühlplatz 41")
            case "hpe":
                self.vvs_trip_use_case("de:08115:7115", "Herrenberger Straße 140")
            case "ibm":
                self.vvs_trip_use_case("de:08115:3218", "IBM-Allee 1")
            case "nextEvent":
                self.next_event_use_case()
            case _:
                raise NotImplementedError

    def vvs_trip_use_case(self, end_vvs_location: str, end_maps_location: str) -> None:
        """Execute use case with given end vvs-id

        Parameters
        ----------
        end_vvs_location : str
            vvs-id of end location
        end_maps_location : str
            name of end location
        """
        response = ""
        still_on_trip = []
        next_event = get_next_event_today()
        next_event_datetime = None
        if next_event is not None:
            next_event_datetime = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")

        if self.user.possessions.bike:
            if self.weather_good_enough_for_bike():
                response += "The weather is not good enough for the bike. "
            else:
                bike_trip = get_maps_connection(self.user.address.street, end_maps_location, MapsTripMode.BICYCLING)
                response += f"If you take the bike, you will need {bike_trip.duration} minutes for {round(bike_trip.distance / 1000, 1)} kilometers. "
                if next_event_datetime is not None and (
                    (next_event_datetime - timedelta(minutes=int(bike_trip.duration))) < datetime.now()
                ):
                    still_on_trip.append("bike")

        if self.user.possessions.car:
            car_trip = get_maps_connection(self.user.address.street, end_maps_location, MapsTripMode.DRIVING)
            response += f"If you take the car, you will need {car_trip.duration} minutes for {round(car_trip.distance / 1000, 1)} kilometers. "
            if next_event_datetime is not None and (
                (next_event_datetime - timedelta(minutes=int(car_trip.duration))) < datetime.now()
            ):
                still_on_trip.append("car")

        train_trip = get_next_connection(self.user.address.vvs_id, end_vvs_location)
        if train_trip is None:
            response += "No VVS connection could be found. "
        else:
            response += f"If you take the next train, you would arrive at {train_trip.connections[-1].end_time.strftime('%H:%M')} after {train_trip.duration} minutes. "
            if next_event_datetime is not None and (
                (next_event_datetime - timedelta(minutes=int(train_trip.duration))) < datetime.now()
            ):
                still_on_trip.append("train")

        if len(still_on_trip) == 1:
            response += f"If you take the {still_on_trip[0]}, you will not arrive before the next event starts. "
        if len(still_on_trip) == 2:
            response += f"If you take the {still_on_trip[0]} or {still_on_trip[1]}, you will not arrive before the next event starts. "
        if len(still_on_trip) == 3:
            response += f"If you take the {still_on_trip[0]}, {still_on_trip[1]} or {still_on_trip[2]}, you will not arrive before the next event starts. "

        self.tts.convert_text(response)

    def next_event_use_case(self) -> None:
        """Executes nextEvent use case"""
        next_event = get_next_event_today()

        if next_event is None:
            self.tts.convert_text("You do not have any more events today.")
            return
        elif next_event.location == "":
            event_datetime = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
            time_available = int((event_datetime - datetime.now()).seconds / 60)
            self.tts.convert_text(
                f"Your next event is {next_event.title} in {time_available} minutes. It does not provide a location. "
            )
        else:
            event_datetime = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
            time_available = int((event_datetime - datetime.now()).seconds / 60)
            response = f"Your next Event is {next_event.title} at {event_datetime.strftime('%H:%M')} at {next_event.location}. "
            not_fast_enough = []

            if self.user.possessions.bike:
                if self.weather_good_enough_for_bike():
                    response += "The weather is not good enough for the bike. "
                else:
                    bike_trip = get_maps_connection(
                        self.user.address.street, next_event.location, MapsTripMode.BICYCLING
                    )
                    if bike_trip.duration > time_available:
                        not_fast_enough.append("bike")
                    else:
                        bike_start = event_datetime - timedelta(minutes=bike_trip.duration)
                        response += f"With the bike, you have to start at {bike_start.strftime('%H:%M')}. "

            if self.user.possessions.car:
                car_trip = get_maps_connection(self.user.address.street, next_event.location, MapsTripMode.DRIVING)
                if car_trip.duration > time_available:
                    not_fast_enough.append("car")
                else:
                    car_start = event_datetime - timedelta(minutes=car_trip.duration)
                    response += f"With the car, you have to start at {car_start.strftime('%H:%M')}. "

            train_trip = get_maps_connection(self.user.address.street, next_event.location, MapsTripMode.TRANSIT)
            if train_trip.duration > time_available:
                not_fast_enough.append("train")
            else:
                train_start = event_datetime - timedelta(minutes=train_trip.duration)
                response += f"With the train, you have to start at {train_start.strftime('%H:%M')}. "

            if len(not_fast_enough) == 1:
                response += f"The {not_fast_enough[0]} is not fast enough."
            if len(not_fast_enough) == 2:
                response += f"The {not_fast_enough[0]} and {not_fast_enough[1]} are not fast enough."
            if len(not_fast_enough) == 3:
                response += f"The {not_fast_enough[0]}, {not_fast_enough[1]} and {not_fast_enough[2]} are all not fast enough. There is no way for you to reach the next event."

            self.tts.convert_text(response)

    def weather_good_enough_for_bike(self) -> bool:
        """Checks if the weather is good enough for the bike

        Returns
        -------
        bool
            if weather is good enough
        """
        min_temp = 8
        max_precipprob = 25

        weather_today = weatherApi.dynamic_range(
            location="Stuttgart,DE",
            dynamic_period=DynamicPeriodEnum.TODAY,
            elements=[ElementsEnum.PRECIP_PROB, ElementsEnum.TEMP],
            include=[IncludeEnum.HOURS],
        )
        cur_hour = datetime.now().hour
        weather_now = weather_today["days"][0]["hours"][cur_hour]  # type: ignore
        weather_in_an_hour = weather_today["days"][0]["hours"][(cur_hour + 1) % 24]  # type: ignore
        if (
            weather_now["temp"] >= min_temp
            and weather_in_an_hour["temp"] >= min_temp
            and weather_now["precipprob"] <= max_precipprob
            and weather_in_an_hour["precipprob"] <= max_precipprob
        ):
            return True
        return False
