from __future__ import print_function

import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]
MTG_SPREADSHEET_RANGE = "!A1:Z100"


class Client(object):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    credentials = None

    def __init__(self, client_id, client_secret, google_file_id) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.google_file_id = google_file_id
        self._set_credentials()
        self.service = build("drive", "v3", credentials=self.credentials)
        self.sheet_service = build("sheets", "v4", credentials=self.credentials)

    def _set_credentials(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if (
                self.credentials
                and self.credentials.expired
                and self.credentials.refresh_token
            ):
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": self.client_id,
                            "project_id": "ceasaro-sas",
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "client_secret": self.client_secret,
                            "redirect_uris": [
                                "urn:ietf:wg:oauth:2.0:oob",
                                "http://localhost",
                            ],
                        }
                    },
                    SCOPES,
                )
                self.credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self.credentials, token)

    def list_files(self):
        # Call the Drive v3 API
        results = (
            self.service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        return results.get("files", [])

    def get_file(self):
        result = (
            self.sheet_service.spreadsheets()
            .values()
            .get(spreadsheetId=self.google_file_id, range=MTG_SPREADSHEET_RANGE)
            .execute()
        )
        return result.get("values", [])

    def store_file(self, values):
        body = {"values": values}
        result = (
            self.sheet_service.spreadsheets()
            .values()
            .update(
                spreadsheetId=self.google_file_id,
                range=MTG_SPREADSHEET_RANGE,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )
        return result.get("values", [])
