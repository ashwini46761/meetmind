"""
Google authentication and API integration
"""
from typing import Optional, Dict, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GoogleAuthHandler:
    """Handle Google authentication and API access."""

    def __init__(self, credentials_file: Optional[str] = None, scopes: Optional[List[str]] = None):
        self.credentials_file = credentials_file
        self.scopes = scopes or [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/drive",
        ]
        self.credentials = None

    def authenticate(self) -> Optional[object]:
        try:
            if not self.credentials_file:
                logger.error("Google credentials file is required")
                return None

            if Path(self.credentials_file).exists():
                from google.oauth2.service_account import Credentials

                self.credentials = Credentials.from_service_account_file(
                    self.credentials_file,
                    scopes=self.scopes,
                )
                logger.info("Authenticated with Google service account credentials")
                return self.credentials

            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file,
                self.scopes,
            )
            self.credentials = flow.run_local_server(port=0)
            logger.info("Successfully authenticated with Google")
            return self.credentials
        except Exception as exc:
            logger.error(f"Error authenticating with Google: {exc}")
            return None

    def create_calendar_event(self, event_details: Dict) -> Optional[str]:
        if not self.credentials:
            logger.error("Not authenticated with Google")
            return None

        try:
            from googleapiclient.discovery import build

            service = build("calendar", "v3", credentials=self.credentials)
            event = service.events().insert(calendarId="primary", body=event_details).execute()
            logger.info(f"Calendar event created: {event.get('id')}")
            return event.get("id")
        except Exception as exc:
            logger.error(f"Error creating calendar event: {exc}")
            return None
