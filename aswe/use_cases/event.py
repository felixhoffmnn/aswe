from datetime import datetime, timedelta
from math import floor

from aswe.api.calendar.calendar import get_events_by_timeframe
from aswe.api.calendar.data import Event
from aswe.api.event import event as eventApi
from aswe.api.event.event_data import EventLocation, EventSummary, ReducedEvent
from aswe.api.event.event_params import EventApiEventParams
from aswe.api.navigation.maps import get_maps_connection
from aswe.api.navigation.trip_data import MapsTrip, MapsTripMode
from aswe.api.weather import weather as weatherApi
from aswe.api.weather.weather_params import ElementsEnum, IncludeEnum
from aswe.core.objects import BestMatch
from aswe.utils.abstract import AbstractUseCase
from aswe.utils.date import get_next_saturday
from aswe.utils.shell import get_int, print_options


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

                events = self._get_events_in_preferred_city(beginning_next_saturday, end_next_sunday)

                if len(events) == 0:
                    return

                calendar_events = get_events_by_timeframe(
                    min_timestamp=beginning_next_saturday.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    max_timestamp=end_next_sunday.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                )

                attendable_events_info = self._get_attendable_events(events[:3], calendar_events)

                if len(attendable_events_info) == 0:
                    self.tts.convert_text("There are no events this weekend that fit your weekend plans.")
                else:
                    if len(attendable_events_info) == 1:
                        self.tts.convert_text("There is one events you might want to attend to.")
                    else:
                        self.tts.convert_text("There are multiple events you might want to attend to.")

                    for event_summary in attendable_events_info:
                        formatted_summary = self._format_event_summary(event_summary)
                        self.tts.convert_text(formatted_summary)
                        self.tts.convert_text("Do you want to attend?")

                        if self.stt.check_if_yes():
                            # ! uncomment patch in test_use_case_event.py before uncommenting
                            # create_event(
                            #     Event(
                            #         title=attendable_events_info[0].name,
                            #         description="",
                            #         full_day=False,
                            #         location=attendable_events_info[0].location.city,
                            #         date=attendable_events_info[0].start.strftime("%Y-%m-%d"),
                            #         start_time=attendable_events_info[0].start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            #         end_time=(attendable_events_info[0].start + timedelta(hours=2)).strftime(
                            #             "%Y-%m-%dT%H:%M:%SZ"
                            #         ),
                            #     )
                            # )
                            self.tts.convert_text("Great, the event was added to your calendar.")

            case _:
                raise NotImplementedError

    def _get_attendable_events(
        self, raw_events: list[ReducedEvent], calendar_events: list[Event]
    ) -> list[EventSummary]:
        """Checks whether or not given events can be attended depending on existing events in the users calenda.

        Parameters
        ----------
        raw_events : list[ReducedEvent]
            retrieved events from `aswe.api.event.event.events`
        calendar_events : list[Event]
            retrieved calendar events from `aswe.api.calendar.calendar.get_events_by_timeframe`

        Returns
        -------
        list[EventSummary]
            List of short summaries of events that can be attended.
        """
        attendable_events_info: list[EventSummary] = []
        for event in raw_events:
            event_is_attendable = self._event_is_attendable(event, calendar_events)

            if event_is_attendable:
                event_summary = self._get_event_summary(event)
                attendable_events_info.append(event_summary)

        return attendable_events_info

    def _event_is_attendable(self, event: ReducedEvent, calendar_events: list[Event]) -> bool:
        """Checks whether a single event can be attended

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

            calendar_event_start_datetime = (
                datetime.fromisoformat(calendar_event.start_time) + timedelta(hours=1)
            ).replace(tzinfo=None)
            calendar_event_end_datetime = (
                datetime.fromisoformat(calendar_event.end_time) + timedelta(hours=1)
            ).replace(tzinfo=None)

            if (calendar_event_start_datetime <= event_start_datetime <= calendar_event_end_datetime) or (
                calendar_event_start_datetime <= event_end_datetime <= calendar_event_end_datetime
            ):
                return False

        return True

    def _get_event_summary(self, event: ReducedEvent) -> EventSummary:
        """Collects short summary about event using weather & gmaps api

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

        weather_response = weatherApi.forecast(
            location=f"{event_summary.location.city},DE",
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

        trip, mode = self._determine_trip_medium(event_summary)

        event_summary.trip_mode = mode
        event_summary.trip_duration = trip.duration

        return event_summary

    def _get_event_times(self, event: ReducedEvent, event_duration: int = 2) -> tuple[datetime, datetime]:
        """Gets start and end time of event

        Parameters
        ----------
        event : ReducedEvent
            single event
        event_duration : int, optional
            configurable duration in hours event should have, by default 2

        Returns
        -------
        Tuple[datetime, datetime]
            start and end datetime of given event
        """
        event_start_datetime = datetime.strptime(event.start, "%Y-%m-%dT%H:%M:%SZ")
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
        trip_hours = floor(event_summary.trip_duration / 60) if event_summary.trip_duration else 0
        trip_minutes = event_summary.trip_duration % 60 if event_summary.trip_duration else 0
        formatted_trip_duration = (
            f"{'1 hour and ' if trip_hours == 1 else str(trip_hours) + ' hours and ' if trip_hours > 1 else ''}"
            f"{'1 minute' if trip_minutes == 1 else str(trip_minutes) + ' minutes' if trip_minutes > 1 else ''}"
        )

        match event_summary.trip_mode:
            case MapsTripMode.WALKING:
                formatted_trip_mode = "foot"
            case MapsTripMode.BICYCLING:
                formatted_trip_mode = "bike"
            case MapsTripMode.TRANSIT:
                formatted_trip_mode = "transit"
            case MapsTripMode.DRIVING:
                formatted_trip_mode = "car"

        formatted_summary = (
            f"""The {event_summary.name} starts at {str(event_summary.start.hour).zfill(2)}:"""
            f"""{str(event_summary.start.minute).zfill(2)}. """
            f"""It will take you {formatted_trip_duration} to get there by {formatted_trip_mode}. """
        )

        if event_summary.is_rainy:
            formatted_summary += "There is a high chance of rain, you might want to take an umbrella. "

        if event_summary.is_cold:
            formatted_summary += "Additionally, you should prepare for chilly temperatures."

        return formatted_summary

    def _ask_for_event_city(self) -> str:
        """Ask user in which city to search for events

        Returns
        -------
        str
            Possible cities: ["Stuttgart", "Berlin", "Koeln", "Muenchen", "Dortmund"]
        """
        self.tts.convert_text("In which city should I search for events?")
        options: list[str | int] = ["Stuttgart", "Berlin", "Koeln", "Muenchen", "Dortmund"]
        print_options(options)
        city_index = get_int(options)

        while not city_index:
            self.tts.convert_text("Sorry I could not find given city. Please try again.")
            city_index = get_int(options)

        return str(options[city_index - 1])

    def _get_events_in_preferred_city(self, start_datetime: datetime, end_datetime: datetime) -> list[ReducedEvent]:
        """Asks user for preferred city and searches for events in given city.

        Parameters
        ----------
        start_datetime : datetime
            Start of timeframe assistant should look for events
        end_datetime : datetime
            End of timeframe assistant should look for events

        Returns
        -------
        list[ReducedEvent]
            List of events in given timeframe
        """
        city = self._ask_for_event_city()

        events = eventApi.events(
            EventApiEventParams(
                city=[city],
                radius=30,
                start_date_time=start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                end_date_time=end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
        )

        while events is None or len(events) == 0:
            self.tts.convert_text(
                f"Looks like there are no events in {city} this weekend. "
                "Do you want to look for events in another city?"
            )

            if not self.stt.check_if_yes():
                return []

            city = self._ask_for_event_city()

            events = eventApi.events(
                EventApiEventParams(
                    city=[city],
                    radius=30,
                    start_date_time=start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    end_date_time=end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                )
            )
        return events

    def _determine_trip_medium(self, event_summary: EventSummary) -> tuple[MapsTrip, MapsTripMode]:
        """Determines which `MapsTripMode to use depending on trip duration and user possessions.

        If the trip via walking is longer than 45 min then the user should, depending on possessions, use
        `MapsTripMode.DRIVING` or `MapsTripMode.TRANSIT`

        Parameters
        ----------
        event_summary : EventSummary
            Used event to determine trip duration

        Returns
        -------
        Tuple[MapsTrip, MapsTripMode]
            Trip and Medium user should use
        """
        trip = get_maps_connection(
            f"{self.user.address.street},{self.user.address.city}",
            f"{event_summary.location.address},{event_summary.location.city}",
            MapsTripMode.WALKING,
        )
        medium = MapsTripMode.WALKING

        if self.user.possessions.bike:
            trip = get_maps_connection(
                f"{self.user.address.street},{self.user.address.city}",
                f"{event_summary.location.address},{event_summary.location.city}",
                MapsTripMode.BICYCLING,
            )
            medium = MapsTripMode.BICYCLING

        if trip.duration > 45:
            if self.user.possessions.car:
                trip = get_maps_connection(
                    f"{self.user.address.street},{self.user.address.city}",
                    f"{event_summary.location.address},{event_summary.location.city}",
                    MapsTripMode.DRIVING,
                )
                medium = MapsTripMode.DRIVING
            else:
                trip = get_maps_connection(
                    f"{self.user.address.street},{self.user.address.city}",
                    f"{event_summary.location.address},{event_summary.location.city}",
                    MapsTripMode.TRANSIT,
                )
                medium = MapsTripMode.TRANSIT

        return trip, medium
