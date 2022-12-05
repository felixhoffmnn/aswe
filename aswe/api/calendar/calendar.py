import os.path
import pickle
from datetime import datetime, timedelta
from typing import Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from loguru import logger

from aswe.api.calendar.data import Event

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "calendar_credentials.json"
PICKLE_FILE = "calendar_token.pickle"


def get_calendar_service() -> Any:
    """Provides a Resource object to interact with the Google Calendar API

    Returns
    -------
    Any
        Resource for interacting with Google Calendar
    """
    creds = None
    if os.path.exists(PICKLE_FILE):  # stores access tokens once created (automatically)
        with open(PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def get_events_by_timeframe(min_timestamp: str, max_timestamp: str) -> list[Event]:
    """Provides all events inside timeframe

    Parameters
    ----------
    min_timestamp : str
        Lower timestamp in timeframe with format "yyyy-MM-ddTHH:mm:ss.ffffffZ"
    max_timestamp : str
        Higher timestamp in timeframe with format "yyyy-MM-ddTHH:mm:ss.ffffffZ"

    Returns
    -------
    list[Event]
        List of all events inside timeframe
    """
    service = get_calendar_service()

    calendars = service.calendarList().list().execute().get("items", [])  # pylint: disable=no-member
    event_array = []
    for i, _ in enumerate(calendars):
        current_calendar = calendars[i].get("id", "")
        if current_calendar != "":

            events_result = (
                service.events()  # pylint: disable=no-member
                .list(
                    calendarId=current_calendar,
                    timeMin=min_timestamp,
                    timeMax=max_timestamp,
                    maxResults=100,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            for event_data in events:
                if "Kalenderwoche" not in event_data.get("summary", ""):
                    event = Event(
                        title=event_data.get("summary", ""),
                        description=event_data.get("description", ""),
                        location=event_data.get("location", ""),
                        full_day="date" in event_data.get("start", {}),
                        date=event_data.get("start", {}).get("date", ""),
                        start_time=event_data.get("start", {}).get("dateTime", ""),
                        end_time=event_data.get("end", {}).get("dateTime", ""),
                    )
                    event_array.append(event)

    logger.debug(f"All events: {event_array}")
    return event_array


def get_all_events_today() -> list[Event]:
    """Provides list of all events happening today

    Returns
    -------
    list[Event]
        List of all events happening today
    """
    today_min = datetime.today().strftime("%Y-%m-%dT00:00:00.000001Z")
    today_max = datetime.today().strftime("%Y-%m-%dT23:59:59.999999Z")

    return get_events_by_timeframe(today_min, today_max)


def get_next_event_today() -> Event | None:
    """Provides the next event happening today

    Returns
    -------
    Event|None
        Next event happening today if one exists
    """
    events = get_all_events_today()

    for event in events:
        if not event.full_day:
            start_time = datetime.strptime(event.start_time, "%Y-%m-%dT%H:%M:%S+01:00")
            if datetime.now() < start_time:
                logger.debug(f"Next event: {event}")
                return event
    return None


def create_event(event_info: Event) -> None:
    """Creates Event in Google Calendar

    Parameters
    ----------
    event_info : Event
        Information about the event that is created
    """
    if event_info.full_day:
        end_date = (datetime.fromisoformat(event_info.date) + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        end_date = ""

    event = {
        "summary": event_info.title,
        "location": event_info.location,
        "description": event_info.description,
        "start": {"date": event_info.date}
        if event_info.full_day
        else {"dateTime": event_info.start_time, "timeZone": "Europe/Berlin"},
        "end": {"date": end_date}
        if event_info.full_day
        else {"dateTime": event_info.end_time, "timeZone": "Europe/Berlin"},
    }

    service = get_calendar_service()
    service.events().insert(calendarId="primary", body=event).execute()  # pylint: disable=no-member

    logger.success(f"Created Event: {event}")
