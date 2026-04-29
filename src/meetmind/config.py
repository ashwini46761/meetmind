"""
Configuration and settings for MeetMind application
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

try:
    import yaml
except ImportError:
    yaml = None

# Load environment variables from .env file
load_dotenv()

def load_yaml_config(config_path: Path) -> dict:
    if not config_path.exists() or yaml is None:
        return {}
    try:
        with config_path.open("r", encoding="utf-8") as stream:
            return yaml.safe_load(stream) or {}
    except Exception:
        return {}

class Config:
    """Base configuration"""

    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG_FILE = BASE_DIR / "config" / "app.yml"
    YAML_CONFIG = load_yaml_config(CONFIG_FILE)

    # API Keys
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY") or YAML_CONFIG.get("anthropic_api_key")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY") or YAML_CONFIG.get("openai_api_key")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY") or YAML_CONFIG.get("google_api_key")
    GOOGLE_CREDENTIALS_FILE: Optional[str] = os.getenv("GOOGLE_CREDENTIALS_FILE") or YAML_CONFIG.get("google_credentials_file")
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID") or YAML_CONFIG.get("twilio_account_sid")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN") or YAML_CONFIG.get("twilio_auth_token")
    TWILIO_FROM_NUMBER: Optional[str] = os.getenv("TWILIO_FROM_NUMBER") or YAML_CONFIG.get("twilio_from_number")

    # Application settings
    APP_NAME: str = os.getenv("APP_NAME") or YAML_CONFIG.get("app_name", "MeetMind")
    DEBUG: bool = (os.getenv("DEBUG", str(YAML_CONFIG.get("debug", "False"))).lower() == "true")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL") or YAML_CONFIG.get("anthropic_model", "claude-3-opus-20240229")

    # Audio settings
    SAMPLE_RATE: int = int(os.getenv("SAMPLE_RATE", YAML_CONFIG.get("sample_rate", 16000)))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", YAML_CONFIG.get("chunk_size", 1024)))
    CHANNELS: int = int(os.getenv("CHANNELS", YAML_CONFIG.get("channels", 1)))

    # File paths
    DATA_DIR = BASE_DIR / "data"
    UPLOADS_DIR = DATA_DIR / "uploads"
    TEMPLATES_DIR = DATA_DIR / "templates"
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"

    @classmethod
    def ensure_paths(cls) -> None:
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        cls.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls) -> bool:
        """Validate optional configuration warnings."""
        missing = []
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        if not cls.TWILIO_ACCOUNT_SID:
            missing.append("TWILIO_ACCOUNT_SID")
        if not cls.TWILIO_AUTH_TOKEN:
            missing.append("TWILIO_AUTH_TOKEN")
        if missing:
            print(f"Warning: Missing configuration keys: {missing}")
            return False
        return True

# Create instance
config = Config()
