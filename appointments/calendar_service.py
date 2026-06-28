import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


def get_calendar_service(user):

    if not user.google_credentials:
        return None

    credentials = Credentials.from_authorized_user_info(
        json.loads(user.google_credentials),
        SCOPES
    )

    service = build(
        "calendar",
        "v3",
        credentials=credentials
    )

    return service
def create_calendar_event(user, title, start_time, end_time, description=""):

    service = get_calendar_service(user)

    if service is None:
        return

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    service.events().insert(
        calendarId="primary",
        body=event
    ).execute()