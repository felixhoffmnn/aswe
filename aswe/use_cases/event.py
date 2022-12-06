from datetime import datetime, timedelta
from typing import Any

from aswe.api.calendar.calendar import get_events_by_timeframe
from aswe.api.calendar.data import Event
from aswe.api.event import event as eventApi
from aswe.api.event.event_data import EventLocation, EventSummary, ReducedEvent
from aswe.api.event.event_params import EventApiEventParams
from aswe.api.navigation.maps import get_maps_connection
from aswe.api.navigation.trip_data import MapsTripMode
from aswe.api.weather import weather as weatherApi
from aswe.api.weather.weather_params import ElementsEnum, IncludeEnum
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase
from aswe.utils.date import get_next_saturday

# TODO add to calendar


class EventUseCase(AbstractUseCase):
    """Use case to handle events"""

    def check_proactivity(self) -> None:
        """Check if there are any events in the next 30 minutes and trigger the assistant

        * TODO: Implement proactivity
        """
        raise NotImplementedError

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
            case "thisWeekend":
                beginning_next_saturday = get_next_saturday()
                end_next_sunday = beginning_next_saturday + timedelta(days=1, hours=23, minutes=59, seconds=59)

                # TODO: Use user city
                events = eventApi.events(
                    EventApiEventParams(
                        city=["Berlin"],
                        radius=30,
                        start_date_time=beginning_next_saturday.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        end_date_time=end_next_sunday.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    )
                )

                calendar_events = get_events_by_timeframe(
                    min_timestamp=beginning_next_saturday.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    max_timestamp=end_next_sunday.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                )

                if events is None or len(events) == 0:
                    self.tts.convert_text("Looks like there are no events this weekend.")
                    return

                attendable_events_info = self._get_attendable_events(events[:3], calendar_events)

                if len(attendable_events_info) == 0:
                    self.tts.convert_text("There are no events this weekend that fit your weekend plans.")
                else:
                    if len(attendable_events_info) == 1:
                        self.tts.convert_text("There is one events you might want to attend to.")
                    else:
                        self.tts.convert_text("There are multiple events you might want to attend to.")

                    # TODO: Maybe put into a seperate function
                    for event_summary in attendable_events_info:
                        formatted_summary = self._format_event_summary(event_summary)
                        self.tts.convert_text(formatted_summary)
                        self.tts.convert_text("Do you want to attend?")

                        if self.stt.check_if_yes():
                            # TODO: Use user city
                            # create_event(
                            #     Event(
                            #         title=attendable_events_info[0]["name"],
                            #         description="",
                            #         full_day=False,
                            #         location="Stuttgart,DE",
                            #         date=attendable_events_info[0]["start"].strftime("%Y-%m-%d"),
                            #         start_time=attendable_events_info[0]["start"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                            #         end_time=(attendable_events_info[0]["start"] + timedelta(hours=2)).strftime(
                            #             "%Y-%m-%dT%H:%M:%SZ"
                            #         ),
                            #     )
                            # )
                            self.tts.convert_text("Great, the event was added to your calendar.")

            case _:
                raise NotImplementedError

    def _get_attendable_events(self, raw_events: list[ReducedEvent], calendar_events: list[Event]) -> list[Any]:
        """Checks whether or not given events can be attended depending on existing events in the users calenda.

        Parameters
        ----------
        raw_events : list[ReducedEvent]
            retrieved events from `aswe.api.event.event.events`
        calendar_events : list[Event]
            retrieved calendar events from `aswe.api.calendar.calendar.get_events_by_timeframe`

        Returns
        -------
        list[Any]
            List of short summaries of events that can be attended.
        """
        return [
            self._get_event_summary(event) for event in raw_events if self._event_is_attendable(event, calendar_events)
        ]

    def _event_is_attendable(self, event: ReducedEvent, calendar_events: list[Any]) -> bool:
        """Checks whether a single event can be attended

        * TODO: Fix typing for `calendar_events`, and `event`

        Parameters
        ----------
        event : ReducedEvent
            single event retrieved from `aswe.api.event.event.events`
        calendar_events : list[Any]
            retrieved calendar events from `aswe.api.calendar.calendar.get_events_by_timeframe`

        Returns
        -------
        bool
            whether event can be attended
        """
        event_start_datetime, event_end_datetime = self._get_event_times(event)

        for calendar_event in calendar_events:
            if calendar_event.start_time == "":
                continue

            calendar_event_start_datetime = datetime.fromisoformat(calendar_event.start_time) + timedelta(hours=1)
            calendar_event_end_datetime = datetime.fromisoformat(calendar_event.end_time) + timedelta(hours=1)

            if (calendar_event_start_datetime <= event_start_datetime <= calendar_event_end_datetime) or (
                calendar_event_start_datetime <= event_end_datetime <= calendar_event_end_datetime
            ):
                return False

        return True

    def _get_event_summary(self, event: ReducedEvent) -> EventSummary:
        """Collects short summary about event using weather & gmaps api

        * TODO: Fix typing for `event`

        Parameters
        ----------
        event : Any
            raw event information

        Returns
        -------
        dict[str, Any]
            short summary of given event which can be formatted to readable string
        """
        event_start_datetime, _ = self._get_event_times(event)

        event_summary = EventSummary(
            name=event.name,
            start=event_start_datetime,
            location=EventLocation(city=event.location.city, address=event.location.address),
            is_cold=False,
            is_rainy=False,
        )

        # TODO: Use user city
        weather_response = weatherApi.forecast(
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

            event_summary.is_cold = temperature < 5.0
            event_summary.is_rainy = precipitation_probability > 40.0

        # TODO: Ask user about preferred method (driving, walking, transit, bicycling)
        # TODO: Check which possessions the user has (bike, car, etc.)
        directions = get_maps_connection(
            f"{self.user.address.street},{self.user.address.city}",
            f"{event_summary.location.address},{event_summary.location.city}",
            MapsTripMode.BICYCLING,
        )

        event_summary.trip_mode = MapsTripMode.BICYCLING
        event_summary.trip_duration = directions.duration

        return event_summary

    def _get_event_times(self, event: ReducedEvent, event_duration: int = 2) -> tuple[datetime, datetime]:
        """Gets start and end time of event

        * TODO: Extract function as `util`

        Parameters
        ----------
        event : ReducedEvent
            single event
        event_duration : int, optional
            configurable duration event should have, by default 2

        Returns
        -------
        Tuple[datetime, datetime]
            start and end datetime of given event
        """
        event_start_datetime = datetime.fromisoformat(event.start.replace("T", " ").replace("Z", ""))
        event_end_datetime = event_start_datetime + timedelta(hours=event_duration)

        return (event_start_datetime, event_end_datetime)

    def _format_event_summary(self, event_summary: EventSummary) -> str:
        """Formats event summary to a readable string

        Parameters
        ----------
        event_summary : EventSummary
            Short event summary

        Returns
        -------
        str
            Single string that can be read by assistant
        """
        formatted_summary = (
            f"""The {event_summary.name} starts at {event_summary.start.hour}:"""
            f"""{str(event_summary.start.minute).zfill(2)}. """
            f"""It will take you {event_summary.trip_duration} minutes to get there. """
        )

        if event_summary.is_rainy:
            formatted_summary += "There is a high chance of rain, you might want to take an umbrella."

        if event_summary.is_cold:
            formatted_summary += "Additionally, you should prepare for chilly temperatures."

        return formatted_summary
