"""
Main Streamlit application entry point for MeetMind.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from meetmind.config import config
from meetmind.utils import save_uploaded_file, setup_logging
from meetmind.modules import AnthropicClient, DocumentHandler, SpeechToText, TwilioHandler

def main():
    load_dotenv()
    config.ensure_paths()
    logger = setup_logging(config.LOGS_DIR, log_level=logging.INFO)

    st.set_page_config(
        page_title=config.APP_NAME,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title(f"🧠 {config.APP_NAME}")
    st.markdown("MeetMind helps you capture meeting audio, analyze notes, generate minutes, and send reminders.")

    if not config.validate():
        st.warning("Some configuration values are missing. Features may be limited until the .env or config/app.yml is updated.")

    MODES = ["Speech to Text", "AI Analysis", "Document Generation", "Communication"]
    mode = st.sidebar.selectbox("Select mode", MODES)

    @st.cache_data(show_spinner=False)
    def cached_transcribe(audio_path: str) -> Optional[str]:
        speech = SpeechToText(
            sample_rate=config.SAMPLE_RATE,
            channels=config.CHANNELS,
            chunk_size=config.CHUNK_SIZE,
        )
        return speech.transcribe_audio(audio_path)

    @st.cache_data(show_spinner=False)
    def cached_analyze(notes: str) -> Optional[str]:
        client = AnthropicClient(config.ANTHROPIC_API_KEY)
        return client.analyze_meeting_notes(notes)

    def display_speech_to_text() -> None:
        st.header("Speech to Text")
        st.write("Upload a recorded meeting audio file and let MeetMind transcribe it.")

        uploaded_file = st.file_uploader(
            "Upload audio file",
            type=["wav", "mp3", "m4a", "mp4", "flac", "aac"],
        )

        if uploaded_file is not None:
            target_path = save_uploaded_file(uploaded_file, Path(config.UPLOADS_DIR))
            st.audio(target_path)
            with st.spinner("Transcribing audio..."):
                transcript = cached_transcribe(str(target_path))
            if transcript:
                st.success("Transcription completed")
                st.text_area("Transcript", transcript, height=250)
            else:
                st.error("Unable to transcribe audio. Check dependencies and the uploaded file.")

    def display_ai_analysis() -> None:
        st.header("AI Analysis")
        st.write("Paste meeting notes or a transcript and generate a summary, action items, and next steps.")

        notes = st.text_area("Meeting notes / transcript", height=250)
        if st.button("Analyze notes"):
            if not notes.strip():
                st.warning("Please provide meeting notes to analyze.")
                return

            with st.spinner("Analyzing notes with Claude..."):
                result = cached_analyze(notes)

            if result:
                st.success("Analysis complete")
                st.text_area("AI analysis", result, height=300)
            else:
                st.error("AI analysis failed. Verify your Anthropic API key and network connection.")

    def display_document_generation() -> None:
        st.header("Document Generation")
        st.write("Generate a professional meeting minutes document from notes and attendees.")

        with st.form("minutes_form"):
            title = st.text_input("Meeting title", "Weekly team sync")
            attendees_input = st.text_area("Attendees (one per line)", "")
            agenda_input = st.text_area("Agenda items (one per line)", "")
            notes = st.text_area("Meeting notes", "")
            action_items_input = st.text_area("Action items (one per line)", "")
            submitted = st.form_submit_button("Create document")

        if submitted:
            attendees = [item.strip() for item in attendees_input.splitlines() if item.strip()]
            agenda = [item.strip() for item in agenda_input.splitlines() if item.strip()]
            action_items = [item.strip() for item in action_items_input.splitlines() if item.strip()]

            handler = DocumentHandler(template_dir=str(Path(config.TEMPLATES_DIR)))
            output_path = handler.create_meeting_minutes(
                title=title,
                attendees=attendees,
                agenda=agenda,
                notes=notes,
                action_items=action_items,
            )

            if output_path:
                st.success("Meeting minutes document created")
                with open(output_path, "rb") as doc_file:
                    st.download_button(
                        label="Download meeting minutes",
                        data=doc_file,
                        file_name=Path(output_path).name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
            else:
                st.error("Failed to create meeting minutes document.")

    def display_communication() -> None:
        st.header("Communication")
        st.write("Send a meeting reminder via SMS using Twilio.")

        if not config.TWILIO_ACCOUNT_SID or not config.TWILIO_AUTH_TOKEN or not config.TWILIO_FROM_NUMBER:
            st.warning("Twilio configuration is incomplete. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER.")
            return

        to_number = st.text_input("Recipient phone number", "+1234567890")
        meeting_title = st.text_input("Meeting title", "Project sync")
        meeting_time = st.text_input("Meeting time", "Tomorrow at 10:00 AM")

        if st.button("Send reminder"):
            if not to_number.strip():
                st.warning("Enter a recipient phone number.")
                return

            twilio = TwilioHandler(
                account_sid=config.TWILIO_ACCOUNT_SID,
                auth_token=config.TWILIO_AUTH_TOKEN,
                from_number=config.TWILIO_FROM_NUMBER,
            )
            message_sid = twilio.send_meeting_reminder(to_number.strip(), meeting_title, meeting_time)
            if message_sid:
                st.success(f"Reminder sent successfully (SID: {message_sid})")
            else:
                st.error("Failed to send reminder. Check Twilio settings and phone number.")

    MODE_DISPATCH = {
        "Speech to Text": display_speech_to_text,
        "AI Analysis": display_ai_analysis,
        "Document Generation": display_document_generation,
        "Communication": display_communication,
    }

    if mode in MODE_DISPATCH:
        MODE_DISPATCH[mode]()
    else:
        st.info("Select a mode from the sidebar to begin.")

if __name__ == "__main__":
    main()