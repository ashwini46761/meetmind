"""
Anthropic API client for Claude integration
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AnthropicClient:
    """Handle interactions with Anthropic Claude API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            logger.error("Anthropic library not installed")
        except Exception as exc:
            logger.error(f"Unable to initialize Anthropic client: {exc}")

    def send_message(self, message: str, model: str = "claude-3-5-sonnet-20241022", max_tokens: int = 2048) -> Optional[str]:
        if not self.client:
            logger.error("Anthropic client not initialized")
            return None

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": message}]
            )
            if response.content and len(response.content) > 0:
                return response.content[0].text
            return None
        except Exception as exc:
            logger.error(f"Error calling Anthropic API: {exc}")
        return None

    def analyze_meeting_notes(self, notes: str) -> Optional[str]:
        prompt = (
            "Analyze these meeting notes and provide:\n"
            "1. Key points discussed\n"
            "2. Action items with owners\n"
            "3. Next steps\n"
            "4. Summary\n\n"
            f"Meeting Notes:\n{notes}"
        )
        return self.send_message(prompt)

    def extract_action_items(self, notes: str) -> Optional[str]:
        prompt = (
            "Extract all action items from these meeting notes.\n"
            "For each action item, provide:\n"
            "- Task description\n"
            "- Owner (person responsible)\n"
            "- Due date (if mentioned)\n"
            "- Priority (High/Medium/Low)\n\n"
            f"Meeting Notes:\n{notes}\n\n"
            "Format as a structured list."
        )
        return self.send_message(prompt)

    def generate_meeting_summary(self, notes: str, meeting_title: str = "Meeting") -> Optional[str]:
        prompt = (
            f"Create a comprehensive summary for '{meeting_title}'.\n\n"
            "Include:\n"
            "1. Executive summary (2-3 sentences)\n"
            "2. Key discussions\n"
            "3. Decisions made\n"
            "4. Important metrics or numbers mentioned\n"
            "5. Follow-up items\n\n"
            f"Meeting Notes:\n{notes}"
        )
        return self.send_message(prompt)

    def analyze_sentiment(self, text: str) -> Optional[str]:
        prompt = (
            "Analyze the sentiment and tone of this meeting transcript.\n"
            "Provide:\n"
            "1. Overall sentiment (Positive/Neutral/Negative)\n"
            "2. Confidence level\n"
            "3. Key emotional themes\n"
            "4. Potential concerns or issues\n"
            "5. Team engagement level\n\n"
            f"Meeting Transcript:\n{text}"
        )
        return self.send_message(prompt)

    def generate_meeting_insights(self, notes: str) -> Optional[str]:
        prompt = (
            "Provide strategic insights and recommendations based on this meeting.\n\n"
            "Analyze:\n"
            "1. Potential risks or issues\n"
            "2. Opportunities to improve\n"
            "3. Efficiency improvements\n"
            "4. Next steps for maximum impact\n"
            "5. Success metrics to track\n\n"
            f"Meeting Notes:\n{notes}"
        )
        return self.send_message(prompt)

    def generate_follow_up_email(self, notes: str, recipient: str = "Team") -> Optional[str]:
        prompt = (
            f"Generate a professional follow-up email for {recipient} based on this meeting.\n"
            "Include:\n"
            "1. Brief meeting summary\n"
            "2. Key decisions and next steps\n"
            "3. Action items assigned\n"
            "4. Timeline for follow-ups\n\n"
            f"Meeting Notes:\n{notes}\n\n"
            "Format as a complete email with subject line."
        )
        return self.send_message(prompt)
