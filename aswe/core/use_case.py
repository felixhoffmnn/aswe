import os
import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import googlemaps as gmaps
import pyjokes
from loguru import logger
from vvspy import get_trips

from aswe.api.calendar.calendar import get_events_by_timeframe, get_next_event_today
from aswe.api.event.event import EventApi
from aswe.api.event.event_params import EventApiEventParams
from aswe.api.weather.weather import WeatherApi
from aswe.api.weather.weather_params import DynamicPeriodEnum, ElementsEnum, IncludeEnum
from aswe.core.data import BestMatch, User
from aswe.core.user_interaction import SpeechToText, TextToSpeech
from aswe.utils.general import get_next_saturday


class AbstractUseCase(ABC):
    """Abstract class for use cases"""

    def __init__(self, stt: SpeechToText, tts: TextToSpeech, assistant_name: str, user: User) -> None:
        """Use case constructor to provide objects from the parent agent class

        * TODO: Add Attributes section

        Parameters
        ----------
        stt : SpeechToText
            The speech to text object
        tts : TextToSpeech
            The text to speech object
        assistant_name : str
            The name of the assistant
        user: User
            User preference information
        """
        self.stt = stt
        self.tts = tts
        self.assistant_name = assistant_name
        self.user = user

    @abstractmethod
    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for morning briefing

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


class MorningBriefingUseCase(AbstractUseCase):
    """ "Use case for the morning briefing"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for morning briefing

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
        match best_match.function_key:
            case "newsSummary":
                raise NotImplementedError
            case _:
                raise NotImplementedError


class SportUseCase(AbstractUseCase):
    """ "Use case for sports"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for sport

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
        match best_match.function_key:
            case "sportSummary":
                raise NotImplementedError
            case _:
                raise NotImplementedError


class EventUseCase(AbstractUseCase):
    """Use case to handle events"""

    _EVENT_API = EventApi()
    _WEATHER_API = WeatherApi()
    _NAVIGATION_API = gmaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for events

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
        match best_match.function_key:
            case "eventSummary":
                raise NotImplementedError
            case "thisWeekend":
                attendable_events_info = []

                beginning_next_saturday = get_next_saturday()
                end_next_sunday = beginning_next_saturday + timedelta(days=1, hours=23, minutes=59, seconds=59)

                event_params = EventApiEventParams(
                    city=["Stuttgart"],
                    radius=30,
                    start_date_time=beginning_next_saturday.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    end_date_time=end_next_sunday.strftime("%Y-%m-%dT%H:%M:%SZ"),
                )

                events = self._EVENT_API.events(event_params)

                if events is None or len(events) == 0:
                    self.tts.convert_text("Looks like there are no events this weekend.")
                    return

                calendar_events = get_events_by_timeframe(
                    min_timestamp=beginning_next_saturday.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    max_timestamp=end_next_sunday.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                )

                for event in events:
                    event_can_be_attended = True

                    event_start_datetime = datetime.fromisoformat(event["start"].replace("T", " ").replace("Z", ""))
                    event_end_datetime = event_start_datetime + timedelta(hours=2)

                    for calendar_event in calendar_events:
                        if calendar_event.start_time == "":
                            continue

                        calendar_event_start_datetime = datetime.fromisoformat(calendar_event.start_time) + timedelta(
                            hours=1
                        )
                        calendar_event_end_datetime = datetime.fromisoformat(calendar_event.end_time) + timedelta(
                            hours=1
                        )

                        if (calendar_event_start_datetime <= event_start_datetime <= calendar_event_end_datetime) or (
                            calendar_event_start_datetime <= event_end_datetime <= calendar_event_end_datetime
                        ):
                            event_can_be_attended = False
                            break

                    if event_can_be_attended:
                        event_tts_info = {"name": event["name"], "start": event_start_datetime}

                        weather_response = self._WEATHER_API.forecast(
                            location="Stuttgart,DE",
                            start_date=event_start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            elements=[ElementsEnum.DATETIME, ElementsEnum.PRECIP_PROB, ElementsEnum.TEMP],
                            include=[IncludeEnum.HOURS],
                        )
                        if weather_response:
                            temperature = float(weather_response["days"][0]["hours"][event_start_datetime.hour]["temp"])
                            precipitation_probability = float(
                                weather_response["days"][0]["hours"][event_start_datetime.hour]["precipprob"]
                            )
                        else:
                            temperature = None
                            precipitation_probability = None

                        event_location = f"""{event["location"]["address"]},{event["location"]["city"]}"""

                        # TODO ask user about preferred method (driving, walking, transit, bicycling)
                        directions = self._NAVIGATION_API.directions(
                            f"{self.user.street},{self.user.city}", event_location, mode="bicycling"
                        )

                        if temperature is not None:
                            event_tts_info["is_cold"] = temperature < 5.0

                        if precipitation_probability is not None:
                            event_tts_info["is_rainy"] = precipitation_probability > 40.0

                        event_tts_info["trip_mode"] = "bicycling"
                        event_tts_info["trip_duration"] = directions[0]["legs"][0]["duration"]["text"]

                        attendable_events_info.append(event_tts_info)

                # TODO add to calendar
                logger.debug("Count of attendable events:" + str(len(attendable_events_info)))
                logger.debug(attendable_events_info)

                if len(attendable_events_info) == 0:
                    self.tts.convert_text("There are no events this weekend that fit your weekend plans.")
                elif len(attendable_events_info) == 1:
                    self.tts.convert_text("There is one event that fits your weekend plans.")
                    self.tts.convert_text(f"""It is the {attendable_events_info[0]["name"]} event.""")

                    self.tts.convert_text(
                        f"""The event starts at {attendable_events_info[0]["start"].hour}:"""
                        f"""{str(attendable_events_info[0]["start"].minute).zfill(2)}. """
                        f"""It will take you {attendable_events_info[0]["trip_duration"]} to get there."""
                    )

                    if attendable_events_info[0].get("is_rainy", False):
                        self.tts.convert_text("There is a high chance of rain, you might want to take an umbrella.")
                    if attendable_events_info[0].get("is_cold", False):
                        self.tts.convert_text("Additionally, you should prepare for chilly temperatures.")
                else:
                    # TODO provide user with more information about multiple events
                    self.tts.convert_text("There are multiple events you might want to attend to.")

                    if (
                        attendable_events_info[0]["start"].weekday() == 5
                        and attendable_events_info[1]["start"].weekday() == 5
                    ):
                        self.tts.convert_text(
                            f"""Both events are coming Saturday, at {attendable_events_info[0]["start"].hour}"""
                            f""":{str(attendable_events_info[0]["start"].minute).zfill(2)} and """
                            f"""{attendable_events_info[1]["start"].hour}"""
                            f""":{str(attendable_events_info[1]["start"].minute).zfill(2)} respectively."""
                        )

            case _:
                raise NotImplementedError


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


class GeneralUseCase(AbstractUseCase):
    """Class for managing the general use case"""

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for general questions

        The general use case aims to answer general questions like the most popular
        ones asked Google assistant. This use case also includes the option to exit
        the assistant.

        Parameters
        ----------
        best_match : BestMatch
            The best matching key for the given user input.

        Raises
        ------
        NotImplementedError
            If the given key was not found in the match case statement for implemented functions,
            or if the function is not implemented yet.
        """
        match best_match.function_key:
            case "time":
                current_time = datetime.now().strftime("%H:%M")
                self.tts.convert_text(f"The current time is {current_time}")
            case "wellBeing":
                self.tts.convert_text("I am fine, Thank you")
            case "name":
                self.tts.convert_text("I am your digital assistant")
                self.tts.convert_text(f"Most of the time I am being called {self.assistant_name}")
            case "joke":
                self.tts.convert_text(pyjokes.get_joke())
            case "stopListening":
                self.tts.convert_text("For how long do you want me to stop listening (in seconds)?")

                sleep_time = 0
                while sleep_time == 0:
                    try:
                        sleep_time = int(input("Please enter the number of your choice: "))
                    except ValueError:
                        self.tts.convert_text("Sorry, I didn't get that. Please try again.")

                time.sleep(sleep_time)
                self.tts.convert_text("I am back again.")
            case "marryMe":
                self.tts.convert_text("I am sorry, I am already married to my job.")
            case "boyGirlFriend":
                self.tts.convert_text("I am sorry, I am not interested in any relationship with my customers.")
            case "exit":
                # TODO exit confirmation does not work
                self.tts.convert_text("Do you really want to exit?")
                response = self.stt.convert_speech()
                if response in ["yes", "yeah", "yep", "sure", "ok"]:
                    self.tts.convert_text("Thanks for using me, have a nice day.")
                    sys.exit()
            case _:
                raise NotImplementedError
