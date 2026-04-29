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

    def send_message(self, message: str, model: str = "claude-3-opus-20240229") -> Optional[str]:
        if not self.client:
            logger.error("Anthropic client not initialized")
            return None

        try:
            if hasattr(self.client, "responses"):
                response = self.client.responses.create(model=model, input=message)
                if hasattr(response, "output"):
                    output = getattr(response.output, "text", None)
                    if output:
                        return output
                return str(response)

            if hasattr(self.client, "messages"):
                response = self.client.messages.create(
                    model=model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": message}]
                )
                if hasattr(response, "content") and response.content:
                    return response.content[0].text
                return str(response)

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
