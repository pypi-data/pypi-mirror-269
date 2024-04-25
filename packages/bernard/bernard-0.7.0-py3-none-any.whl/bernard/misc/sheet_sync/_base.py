import csv
from pathlib import Path

import keyring
import orjson
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from bernard.conf import settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class SheetDownloader:
    """
    Download Google sheets into CSV files.

    Follow the tutorial here:
    https://developers.google.com/sheets/api/quickstart/python

    You must take the JSON credential file's content and put it in the
    settings under GOOGLE_SHEET_SYNC['credentials'].

    In order to make the class usable, you need to call `init()` first, which
    might open your browser and open an OAuth screen.
    """

    def __init__(self, flags):
        self.flags = flags
        self.service = None

    def init(self):
        """
        Fetch the credentials (and cache them on disk).
        """

        creds = self._get_credentials()
        self.service = build("sheets", "v4", credentials=creds)

    def _get_credentials(self):
        creds = None

        if token := keyring.get_password("bernard", "google_sheet_token"):
            creds = Credentials.from_authorized_user_info(orjson.loads(token), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    settings.GOOGLE_SHEET_SYNC["credentials"],
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)
                keyring.set_password("bernard", "google_sheet_token", creds.to_json())

        return creds

    def download_sheet(self, file_path, sheet_id, cell_range):
        """
        Download the cell range from the sheet and store it as CSV in the
        `file_path` file.
        """

        result = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=sheet_id,
                range=cell_range,
            )
            .execute()
        )

        values = result.get("values", [])

        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open(newline="", encoding="utf-8", mode="w") as f:
            writer = csv.writer(f, lineterminator="\n")

            for row in values:
                writer.writerow(row)


def main(flags):
    """
    Download all sheets as configured.
    """

    dl = SheetDownloader(flags)
    dl.init()

    for file_info in settings.GOOGLE_SHEET_SYNC["files"]:
        print("Downloading {}".format(file_info["path"]))  # noqa: T201
        dl.download_sheet(
            file_info["path"],
            file_info["sheet"],
            file_info["range"],
        )
