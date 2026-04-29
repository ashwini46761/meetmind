"""
Speech-to-text module using OpenAI Whisper and PyAudio
"""
from typing import Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SpeechToText:
    """Handle audio recording and transcription."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size

    def record_audio(self, duration: int, output_file: str) -> bool:
        try:
            import pyaudio
            import wave

            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )

            frames = []
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with wave.open(output_file, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b"".join(frames))

            logger.info(f"Audio recorded successfully: {output_file}")
            return True
        except ImportError:
            logger.error("PyAudio library not installed")
            return False
        except Exception as exc:
            logger.error(f"Error recording audio: {exc}")
            return False

    def transcribe_audio(self, audio_file: str) -> Optional[str]:
        try:
            import whisper

            model = whisper.load_model("base")
            result = model.transcribe(audio_file)
            text = result.get("text") if isinstance(result, dict) else None
            logger.info(f"Audio transcribed successfully: {audio_file}")
            return text
        except ImportError:
            logger.error("Whisper library not installed")
            return None
        except Exception as exc:
            logger.error(f"Error transcribing audio: {exc}")
            return None
