# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# [START drive_quickstart]
from __future__ import print_function
import os.path
from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        try:
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except FileExistsError as err:
            print(err)
        # If there are no (valid) credentials available, let the user log in.
        try:
            if not creds or not creds.valid:
                try:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                except Exception as err:
                    print('Invalid Grant', err)
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        except FileNotFoundError as err:
            print('File does not exist', err)

        finally:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

        try:
            if not events:
                print('No upcoming events found.')
        except FileNotFoundError as err:
            print('File does not exist', err)
        else:
            print('Events:')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
