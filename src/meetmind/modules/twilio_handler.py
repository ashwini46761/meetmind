"""
Twilio integration for SMS and communication
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TwilioHandler:
    """Handle Twilio SMS and communication services"""
    
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Initialize Twilio handler
        
        Args:
            account_sid: Twilio account SID
            auth_token: Twilio authentication token
            from_number: Twilio phone number to send from
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        
        try:
            from twilio.rest import Client
            self.client = Client(account_sid, auth_token)
        except ImportError:
            logger.error("Twilio library not installed")
            self.client = None
    
    def send_sms(self, to_number: str, message: str) -> Optional[str]:
        """
        Send SMS message
        
        Args:
            to_number: Recipient phone number
            message: Message text
        
        Returns:
            Message SID or None if failed
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return None
        
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            logger.info(f"SMS sent successfully: {msg.sid}")
            return msg.sid
        
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return None
    
    def send_meeting_reminder(self, to_number: str, meeting_title: str, meeting_time: str) -> Optional[str]:
        """
        Send meeting reminder SMS
        
        Args:
            to_number: Recipient phone number
            meeting_title: Title of the meeting
            meeting_time: Time of the meeting
        
        Returns:
            Message SID or None if failed
        """
        message = f"Reminder: {meeting_title} at {meeting_time}"
        return self.send_sms(to_number, message)
