"""
Utility functions for MeetMind application
"""
import logging
from pathlib import Path
from typing import Optional, List


def setup_logging(log_dir: Optional[str] = None, log_level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging for the application.
    """
    if log_dir is None:
        log_dir = Path(__file__).resolve().parent.parent / "logs"
    else:
        log_dir = Path(log_dir)

    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("meetmind")
    logger.setLevel(log_level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        file_handler.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def ensure_directories_exist(directories: List[Path]) -> None:
    """
    Ensure required directories exist.
    """
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    """Save an uploaded Streamlit file to disk."""
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / uploaded_file.name
    with target_path.open("wb") as output:
        output.write(uploaded_file.getbuffer())
    return target_path
