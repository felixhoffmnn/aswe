from datetime import datetime, timedelta

from aswe.api.calendar.calendar import get_next_event_today
from aswe.api.navigation.maps import get_maps_connection
from aswe.api.navigation.trip_data import MapsTripMode
from aswe.api.navigation.vvs import get_next_connection
from aswe.api.weather import weather as weatherApi
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase


class TransportationUseCase(AbstractUseCase):
    """Use case for transportation"""

    def check_proactivity(self) -> None:
        """Check if there is a proactivity to be triggered

        * TODO: Implement proactivity
        """
        raise NotImplementedError

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for transportation

        * TODO: Implement `quotes_key`
        * TODO: Refactor this function into smaller functions

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
        end_vvs_location = ""
        end_location = ""
        reach_next_event = False
        next_event = None

        match best_match.function_key:
            case "dhbw":
                end_vvs_location = "de:08111:6056"  # Stadtmitte
                end_location = "Rotebühlplatz 41"
            case "hpe":
                end_vvs_location = "de:08115:7115"  # Hulb
                end_location = "Herrenberger Straße 140"
            case "ibm":
                end_vvs_location = "de:08115:3218"  # IBM
                end_location = "IBM-Allee 1"
            case "nextEvent":
                next_event = get_next_event_today()
                if not next_event:
                    self.tts.convert_text("You do not have any more events today.")
                    return
                if next_event.location == "":
                    self.tts.convert_text("Your next event does not provide a location.")
                    return
                end_location = next_event.location
                reach_next_event = True
            case _:
                raise NotImplementedError

        bicycle_response = ""
        bike_trip = None
        if self.user.possessions.bike:
            min_temp = 8
            max_precipprob = 25
            bicycle_response = "The weather is not good enough for riding a bike. "

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
                bike_trip = get_maps_connection(self.user.address.street, end_location, MapsTripMode.BICYCLING)
                bicycle_response = f"If you take the bike, you will need {bike_trip.duration} minutes for {round(bike_trip.distance / 1000, 1)} kilometers. "

        car_response = ""
        car_trip = None
        if self.user.possessions.car:
            car_trip = get_maps_connection(self.user.address.street, end_location, MapsTripMode.DRIVING)
            car_response = f"If you take the car, you will need {car_trip.duration} minutes for {round(car_trip.distance / 1000, 1)} kilometers. "

        vvs_response = "There seems to be no train connection. "
        train_trip = None
        if end_vvs_location != "":
            start_location = self.user.address.vvs_id

            train_trip = get_next_connection(start_location, end_vvs_location)
            if train_trip is not None:
                vvs_response = "You can take the"
                for i, con in enumerate(train_trip.connections):
                    if i != 0:
                        vvs_response += " then the"
                    vvs_response += f" {con.train_name} from {con.start_location} to {con.end_location} at {con.start_time.strftime('%H:%M')}"
                vvs_response += f". You would arrive at {train_trip.connections[-1].end_time.strftime('%H:%M')} after {train_trip.duration} minutes. "

        if not reach_next_event:
            next_event = get_next_event_today()
            next_event_announcement = "You do not have any more events today. "
            if next_event:
                event_start_time = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00").strftime("%H:%M")
                next_event_announcement = f"Your next Event is {next_event.title} at {event_start_time}. "
                still_on_trip = []
                if (
                    bike_trip is not None
                    and (
                        datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
                        - timedelta(minutes=bike_trip.duration)
                    )
                    < datetime.now()
                ):
                    still_on_trip.append("bike")
                if (
                    car_trip is not None
                    and (
                        datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
                        - timedelta(minutes=car_trip.duration)
                    )
                    < datetime.now()
                ):
                    still_on_trip.append("car")
                if (
                    train_trip is not None
                    and datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
                    < train_trip.connections[-1].end_time
                ):
                    still_on_trip.append("train")
                if len(still_on_trip) == 1:
                    next_event_announcement += (
                        f"If you take the {still_on_trip[0]}, you will not arrive before the next event starts. "
                    )
                if len(still_on_trip) == 2:
                    next_event_announcement += f"If you take the {still_on_trip[0]} or {still_on_trip[1]}, you will not arrive before the next event starts. "
                if len(still_on_trip) == 3:
                    next_event_announcement += f"If you take the {still_on_trip[0]}, {still_on_trip[1]} or {still_on_trip[2]}, you will not arrive before the next event starts. "

            output = bicycle_response + car_response + vvs_response + next_event_announcement
            self.tts.convert_text(output)
        elif next_event:
            event_datetime = datetime.strptime(next_event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
            time_available = int((event_datetime - datetime.now()).seconds / 60)
            response = f"Your next Event is {next_event.title} at {event_datetime.strftime('%H:%M')} at {next_event.location}. "
            not_fast_enough = []
            if self.user.possessions.bike:
                if not bike_trip:
                    response += "The weather is not good enough for the bike. "
                elif bike_trip.duration > time_available:
                    not_fast_enough.append("bike")
                else:
                    bike_start = event_datetime - timedelta(minutes=bike_trip.duration)
                    response += f"With the bike, you have to start at {bike_start.strftime('%H:%M')}. "
            if self.user.possessions.car:
                if car_trip is not None and car_trip.duration > time_available:
                    not_fast_enough.append("car")
                elif car_trip is not None:
                    car_start = event_datetime - timedelta(minutes=car_trip.duration)
                    response += f"With the car, you have to start at {car_start.strftime('%H:%M')}. "
            train_maps_trip = get_maps_connection(self.user.address.street, end_location, MapsTripMode.TRANSIT)
            if train_maps_trip.duration > time_available:
                not_fast_enough.append("train")
            elif car_trip is not None:
                train_start = event_datetime - timedelta(minutes=train_maps_trip.duration)
                response += f"With the train, you have to start at {train_start.strftime('%H:%M')}. "
            if len(not_fast_enough) == 1:
                response += f"The {not_fast_enough[0]} is not fast enough."
            if len(not_fast_enough) == 2:
                response += f"The {not_fast_enough[0]} and {not_fast_enough[1]} are not fast enough."
            if len(not_fast_enough) == 3:
                response += f"The {not_fast_enough[0]}, {not_fast_enough[1]} and {not_fast_enough[2]} are all not fast enough. There is no way to reach the next event."

            self.tts.convert_text(response)
