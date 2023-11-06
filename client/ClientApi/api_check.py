from __future__ import print_function

import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    time = '2023-11-06T16:34:00-17:34'
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': 'Meeting',
            'start': {
                'dateTime': time
            },
            'end': {
                'dateTime': time
            },
            "conferenceData": {
            "createRequest": {
            "requestId": "SecureRandom.uuid"
            }
            }
        }
        event = service.events().insert(calendarId="primary", sendNotifications=True, body=event, conferenceDataVersion=1).execute()
        print(event)
    except HttpError:
        pass

if __name__ == "__main__":
    main()
