import os
from datetime import datetime, timedelta

import googlemaps as gmaps
from loguru import logger

from aswe.api.calendar.calendar import get_events_by_timeframe
from aswe.api.event.event import EventApi
from aswe.api.event.event_data import EventTTSInfo, TripModeEnum
from aswe.api.event.event_params import EventApiEventParams
from aswe.api.weather.weather import WeatherApi
from aswe.api.weather.weather_params import ElementsEnum, IncludeEnum
from aswe.core.data import BestMatch
from aswe.utils.abstract import AbstractUseCase
from aswe.utils.date import get_next_saturday


class EventUseCase(AbstractUseCase):
    """Use case to handle events"""

    _EVENT_API = EventApi()
    _WEATHER_API = WeatherApi()
    _NAVIGATION_API = gmaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

    def trigger_assistant(self, best_match: BestMatch) -> None:
        """UseCase for events

        * TODO: Implement `quotes_key`
        * TODO: Outsource navigation api

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
                attendable_events_info: list[EventTTSInfo] = []

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

                    event_start_datetime = datetime.fromisoformat(event.start.replace("T", " ").replace("Z", ""))
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
                        event_tts_info = EventTTSInfo(name=event.name, start=event_start_datetime)

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

                        event_location = f"""{event.location.address},{event.location.city}"""

                        # TODO a user about preferred method (driving, walking, transit, bicycling)
                        directions = self._NAVIGATION_API.directions(
                            f"{self.user.street},{self.user.city}", event_location, mode="bicycling"
                        )

                        if temperature is not None:
                            event_tts_info.is_cold = temperature < 5.0

                        if precipitation_probability is not None:
                            event_tts_info.is_rainy = precipitation_probability > 40.0

                        event_tts_info.trip_mode = TripModeEnum.BICYCLING
                        event_tts_info.trip_duration = directions[0]["legs"][0]["duration"]["text"]

                        attendable_events_info.append(event_tts_info)

                # TODO add to calendar
                logger.debug("Count of attendable events:" + str(len(attendable_events_info)))
                logger.debug(attendable_events_info)

                if len(attendable_events_info) == 0:
                    self.tts.convert_text("There are no events this weekend that fit your weekend plans.")
                elif len(attendable_events_info) == 1:
                    self.tts.convert_text("There is one event that fits your weekend plans.")
                    self.tts.convert_text(f"""It is the {attendable_events_info[0].name} event.""")

                    self.tts.convert_text(
                        f"""The event starts at {attendable_events_info[0].start.hour}:"""
                        f"""{str(attendable_events_info[0].start.minute).zfill(2)}. """
                        f"""It will take you {attendable_events_info[0].trip_duration} to get there."""
                    )

                    if attendable_events_info[0].is_rainy:
                        self.tts.convert_text("There is a high chance of rain, you might want to take an umbrella.")
                    if attendable_events_info[0].is_cold:
                        self.tts.convert_text("Additionally, you should prepare for chilly temperatures.")
                else:
                    # TODO provide user with more information about multiple events
                    self.tts.convert_text("There are multiple events you might want to attend to.")

                    if (
                        attendable_events_info[0].start.weekday() == 5
                        and attendable_events_info[1].start.weekday() == 5
                    ):
                        self.tts.convert_text(
                            f"""Both events are coming Saturday, at {attendable_events_info[0].start.hour}"""
                            f""":{str(attendable_events_info[0].start.minute).zfill(2)} and """
                            f"""{attendable_events_info[1].start.hour}"""
                            f""":{str(attendable_events_info[1].start.minute).zfill(2)} respectively."""
                        )

            case _:
                raise NotImplementedError
