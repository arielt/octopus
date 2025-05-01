"""
This script is used to import events from the user's Google Calendar to the database.
"""

from datetime import datetime as dt, timezone as tz
import os.path
import pickle
import pandas as pd

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def get_calendar_events(service, max_results=10):
    """Get events from the primary calendar."""
    # Call the Calendar API
    now = dt.now(tz.utc).isoformat().replace("+00:00", "Z")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    print(events)

    df = pd.DataFrame(events)
    print(df)
    df.to_csv("output.csv", index=False)

    if not events:
        print("No upcoming events found.")
    else:
        print("Upcoming events:")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(f"{start} - {event['summary']}")


if __name__ == "__main__":
    calendar_service = get_calendar_service()
    get_calendar_events(calendar_service, 50)
