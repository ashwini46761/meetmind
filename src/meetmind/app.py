"""
Enhanced MeetMind Streamlit application with modern UI/UX and AI-powered features.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import json

import streamlit as st
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from meetmind.config import config
from meetmind.utils import save_uploaded_file, setup_logging
from meetmind.modules import AnthropicClient, DocumentHandler, SpeechToText, TwilioHandler


# ===================== STYLING & CONFIG =====================
def setup_page():
    """Configure Streamlit page settings and custom styling."""
    st.set_page_config(
        page_title="MeetMind - AI Meeting Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Custom CSS for modern design
    custom_css = """
    <style>
        /* Main app styling */
        .main {
            padding: 0;
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: white;
            margin: -70px -20px 30px -20px;
            border-radius: 0 0 15px 15px;
        }
        
        .header-title {
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
        }
        
        .header-subtitle {
            font-size: 1.1em;
            opacity: 0.95;
            margin-top: 5px;
        }
        
        /* Feature cards */
        .feature-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
            border-left: 4px solid #667eea;
        }
        
        .feature-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.1em;
            font-weight: 500;
        }
        
        /* Metrics styling */
        .metric-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        /* Success styling */
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        /* Warning styling */
        .warning-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        /* Error styling */
        .error-box {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def show_header():
    """Display app header with title and description."""
    header_html = """
    <div class="header-container">
        <div class="header-title">🧠 MeetMind</div>
        <div class="header-subtitle">Your Intelligent AI-Powered Meeting Assistant</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


# ===================== UTILITY FUNCTIONS =====================
@st.cache_data(show_spinner=False)
def get_speech_to_text_instance():
    """Cache SpeechToText instance."""
    return SpeechToText(
        sample_rate=config.SAMPLE_RATE,
        channels=config.CHANNELS,
        chunk_size=config.CHUNK_SIZE,
    )


@st.cache_data(show_spinner=False)
def get_anthropic_client():
    """Cache Anthropic client instance."""
    if not config.ANTHROPIC_API_KEY:
        return None
    return AnthropicClient(config.ANTHROPIC_API_KEY)


def get_document_handler():
    """Get DocumentHandler instance."""
    return DocumentHandler(template_dir=str(Path(config.TEMPLATES_DIR)))


def get_twilio_handler():
    """Get Twilio handler if configured."""
    if not all([config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN, config.TWILIO_FROM_NUMBER]):
        return None
    return TwilioHandler(
        account_sid=config.TWILIO_ACCOUNT_SID,
        auth_token=config.TWILIO_AUTH_TOKEN,
        from_number=config.TWILIO_FROM_NUMBER,
    )


# ===================== FEATURE: SPEECH TO TEXT =====================
def feature_speech_to_text():
    """Speech to Text - Convert audio to text using Whisper."""
    st.subheader("🎤 Speech to Text")
    st.write("Convert meeting audio to text using OpenAI Whisper")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload audio file",
            type=["wav", "mp3", "m4a", "mp4", "flac", "aac"],
            help="Maximum file size depends on your system memory"
        )
    
    with col2:
        st.info("📝 Supported formats: WAV, MP3, M4A, MP4, FLAC, AAC")
    
    if uploaded_file is not None:
        st.audio(uploaded_file)
        
        if st.button("🔄 Transcribe", key="transcribe_btn"):
            with st.spinner("🔊 Transcribing audio..."):
                target_path = save_uploaded_file(uploaded_file, Path(config.UPLOADS_DIR))
                speech = get_speech_to_text_instance()
                transcript = speech.transcribe_audio(str(target_path))
            
            if transcript:
                st.markdown('<div class="success-box">✅ Transcription completed successfully</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text_area("Transcript", transcript, height=300, disabled=False)
                with col2:
                    st.download_button(
                        label="📥 Download",
                        data=transcript,
                        file_name="transcript.txt",
                        mime="text/plain"
                    )
                
                # Store transcript in session state for other features
                st.session_state.last_transcript = transcript
            else:
                st.markdown('<div class="error-box">❌ Transcription failed. Please check the audio file and try again.</div>', unsafe_allow_html=True)


# ===================== FEATURE: AI ANALYSIS =====================
def feature_ai_analysis():
    """AI Analysis - Core meeting analysis with multiple perspectives."""
    st.subheader("🧠 Comprehensive AI Analysis")
    st.write("Analyze meeting notes from multiple angles using Claude AI")
    
    # Text input with options
    col1, col2 = st.columns([3, 1])
    with col1:
        notes = st.text_area(
            "Meeting notes / transcript",
            height=250,
            placeholder="Paste meeting notes or transcript here...",
            help="Include all important discussions, decisions, and observations"
        )
    
    with col2:
        st.info("💡 Tips:\n- Be detailed\n- Include speaker names\n- Note decisions\n- Mention concerns")
    
    if notes.strip():
        # Analysis type selector
        analysis_types = [
            "Complete Analysis",
            "Action Items Only",
            "Executive Summary",
            "Sentiment & Tone",
            "Insights & Recommendations"
        ]
        
        selected_analysis = st.selectbox("Select analysis type:", analysis_types)
        
        if st.button("🔍 Analyze", key="analyze_btn"):
            client = get_anthropic_client()
            if not client:
                st.error("❌ Anthropic API key not configured")
                return
            
            with st.spinner("🤖 Claude is analyzing..."):
                if selected_analysis == "Complete Analysis":
                    result = client.analyze_meeting_notes(notes)
                elif selected_analysis == "Action Items Only":
                    result = client.extract_action_items(notes)
                elif selected_analysis == "Executive Summary":
                    result = client.generate_meeting_summary(notes)
                elif selected_analysis == "Sentiment & Tone":
                    result = client.analyze_sentiment(notes)
                else:  # Insights & Recommendations
                    result = client.generate_meeting_insights(notes)
            
            if result:
                st.markdown('<div class="success-box">✅ Analysis completed</div>', unsafe_allow_html=True)
                st.markdown("### Analysis Results:")
                st.markdown(result)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Analysis",
                        data=result,
                        file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_analysis"
                    )
                with col2:
                    if st.button("📋 Copy to Clipboard", key="copy_analysis"):
                        st.info("Copied! You can now paste it anywhere.")
            else:
                st.markdown('<div class="error-box">❌ Analysis failed. Please try again.</div>', unsafe_allow_html=True)
    else:
        st.info("👆 Please enter meeting notes to analyze")


# ===================== FEATURE: ACTION ITEMS EXTRACTOR =====================
def feature_action_items():
    """Extract and track action items with owners and deadlines."""
    st.subheader("✅ Action Items Extractor")
    st.write("Automatically extract action items with owners and deadlines")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        notes = st.text_area(
            "Meeting notes",
            height=200,
            key="action_items_notes",
            placeholder="Paste meeting notes here..."
        )
    
    with col2:
        st.info("Extracts:\n- Task description\n- Owner\n- Due date\n- Priority level")
    
    if notes.strip() and st.button("🔍 Extract Action Items"):
        client = get_anthropic_client()
        if not client:
            st.error("❌ API key not configured")
            return
        
        with st.spinner("Extracting action items..."):
            result = client.extract_action_items(notes)
        
        if result:
            st.markdown(result)
            st.download_button(
                "📥 Download as Text",
                data=result,
                file_name="action_items.txt",
                mime="text/plain"
            )


# ===================== FEATURE: MEETING INSIGHTS =====================
def feature_meeting_insights():
    """Generate strategic meeting insights and recommendations."""
    st.subheader("💡 Meeting Insights & Recommendations")
    st.write("Get AI-powered insights and strategic recommendations")
    
    notes = st.text_area(
        "Meeting notes",
        height=200,
        key="insights_notes",
        placeholder="Paste meeting notes here..."
    )
    
    if notes.strip() and st.button("🎯 Generate Insights"):
        client = get_anthropic_client()
        if not client:
            st.error("❌ API key not configured")
            return
        
        with st.spinner("Generating insights..."):
            result = client.generate_meeting_insights(notes)
        
        if result:
            st.markdown(result)
            st.download_button(
                "📥 Download Insights",
                data=result,
                file_name="insights.txt",
                mime="text/plain"
            )


# ===================== FEATURE: SENTIMENT ANALYSIS =====================
def feature_sentiment_analysis():
    """Analyze meeting sentiment and team engagement."""
    st.subheader("😊 Sentiment Analysis")
    st.write("Analyze meeting tone, sentiment, and team engagement")
    
    notes = st.text_area(
        "Meeting transcript",
        height=200,
        key="sentiment_notes",
        placeholder="Paste meeting transcript here..."
    )
    
    if notes.strip() and st.button("📊 Analyze Sentiment"):
        client = get_anthropic_client()
        if not client:
            st.error("❌ API key not configured")
            return
        
        with st.spinner("Analyzing sentiment..."):
            result = client.analyze_sentiment(notes)
        
        if result:
            st.markdown(result)


# ===================== FEATURE: DOCUMENT GENERATION =====================
def feature_document_generation():
    """Generate professional meeting minutes document."""
    st.subheader("📄 Document Generation")
    st.write("Create professional meeting minutes in DOCX format")
    
    with st.form("minutes_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Meeting title", value="Weekly Team Sync")
            attendees_input = st.text_area("Attendees (one per line)", height=100)
        
        with col2:
            date = st.date_input("Meeting date")
            meeting_time = st.time_input("Meeting time")
        
        agenda_input = st.text_area("Agenda items (one per line)", height=100)
        notes = st.text_area("Meeting notes", height=150)
        action_items_input = st.text_area("Action items (one per line)", height=100)
        
        submitted = st.form_submit_button("📄 Generate Document", use_container_width=True)
    
    if submitted:
        attendees = [item.strip() for item in attendees_input.splitlines() if item.strip()]
        agenda = [item.strip() for item in agenda_input.splitlines() if item.strip()]
        action_items = [item.strip() for item in action_items_input.splitlines() if item.strip()]
        
        if not title or not attendees:
            st.error("Please provide meeting title and at least one attendee")
            return
        
        with st.spinner("📝 Creating document..."):
            handler = get_document_handler()
            output_path = handler.create_meeting_minutes(
                title=title,
                attendees=attendees,
                agenda=agenda,
                notes=notes,
                action_items=action_items,
            )
        
        if output_path:
            st.markdown('<div class="success-box">✅ Document created successfully!</div>', unsafe_allow_html=True)
            with open(output_path, "rb") as doc_file:
                st.download_button(
                    label="📥 Download Meeting Minutes",
                    data=doc_file,
                    file_name=Path(output_path).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.markdown('<div class="error-box">❌ Failed to create document</div>', unsafe_allow_html=True)


# ===================== FEATURE: EMAIL GENERATION =====================
def feature_email_generation():
    """Generate professional follow-up emails."""
    st.subheader("📧 Follow-up Email Generator")
    st.write("Generate professional follow-up emails from meeting notes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        notes = st.text_area("Meeting notes", height=200, key="email_notes")
        recipient = st.text_input("Recipient name", value="Team")
    
    with col2:
        st.info("Generates:\n- Subject line\n- Summary\n- Action items\n- Next steps")
    
    if notes.strip() and st.button("✉️ Generate Email"):
        client = get_anthropic_client()
        if not client:
            st.error("❌ API key not configured")
            return
        
        with st.spinner("Generating email..."):
            result = client.generate_follow_up_email(notes, recipient)
        
        if result:
            st.markdown(result)
            st.download_button(
                "📥 Download Email",
                data=result,
                file_name="followup_email.txt",
                mime="text/plain"
            )


# ===================== FEATURE: COMMUNICATION =====================
def feature_communication():
    """Send meeting reminders via SMS."""
    st.subheader("📱 Send Meeting Reminders")
    st.write("Send SMS reminders to team members")
    
    if not get_twilio_handler():
        st.markdown(
            '<div class="warning-box">⚠️ Twilio is not configured. '
            'Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER in .env</div>',
            unsafe_allow_html=True
        )
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        to_number = st.text_input("Recipient phone number", placeholder="+1234567890")
        meeting_title = st.text_input("Meeting title", value="Team Sync")
    
    with col2:
        meeting_time = st.text_input("Meeting time", value="Tomorrow at 10:00 AM")
        st.info("Format: +1 (country code + number)")
    
    if st.button("📤 Send Reminder", use_container_width=True):
        if not to_number.strip():
            st.error("Please enter recipient phone number")
            return
        
        with st.spinner("Sending reminder..."):
            twilio = get_twilio_handler()
            message_sid = twilio.send_meeting_reminder(
                to_number.strip(),
                meeting_title,
                meeting_time
            )
        
        if message_sid:
            st.markdown(
                f'<div class="success-box">✅ Reminder sent successfully! (SID: {message_sid})</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="error-box">❌ Failed to send reminder. Check Twilio settings and phone number.</div>',
                unsafe_allow_html=True
            )


# ===================== DASHBOARD =====================
def show_dashboard():
    """Display main dashboard with quick stats and features."""
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        ("🎤", "Speech to Text", "Convert audio to text"),
        ("🧠", "AI Analysis", "Analyze meeting notes"),
        ("✅", "Action Items", "Extract tasks & owners"),
        ("💡", "Insights", "Get recommendations"),
    ]
    
    cols = [col1, col2, col3, col4]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2em; margin-bottom: 10px;">{icon}</div>
                <div style="font-weight: bold; margin-bottom: 5px;">{title}</div>
                <div style="font-size: 0.9em; color: #666;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ===================== SETTINGS PAGE =====================
def show_settings():
    """Settings and configuration page."""
    st.subheader("⚙️ Settings & Configuration")
    
    with st.expander("📋 API Configuration Status", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**API Keys Status:**")
            apis = [
                ("Anthropic API", bool(config.ANTHROPIC_API_KEY)),
                ("Twilio SID", bool(config.TWILIO_ACCOUNT_SID)),
                ("Twilio Token", bool(config.TWILIO_AUTH_TOKEN)),
                ("Twilio Phone", bool(config.TWILIO_FROM_NUMBER)),
            ]
            
            for api_name, is_set in apis:
                status = "✅ Configured" if is_set else "❌ Not set"
                st.write(f"- {api_name}: {status}")
        
        with col2:
            st.write("**Audio Settings:**")
            st.write(f"- Sample Rate: {config.SAMPLE_RATE} Hz")
            st.write(f"- Channels: {config.CHANNELS}")
            st.write(f"- Chunk Size: {config.CHUNK_SIZE}")
    
    with st.expander("📁 File Paths"):
        st.write(f"- Uploads: `{config.UPLOADS_DIR}`")
        st.write(f"- Templates: `{config.TEMPLATES_DIR}`")
        st.write(f"- Logs: `{config.LOGS_DIR}`")
    
    with st.expander("ℹ️ About MeetMind"):
        st.write("""
        **MeetMind** is an AI-powered meeting assistant that helps you:
        - Transcribe meeting audio to text
        - Analyze meeting notes with Claude AI
        - Extract action items and owners
        - Generate professional documents
        - Send SMS reminders
        - Get strategic insights and recommendations
        
        **Version:** 2.0 (Enhanced)
        **Last Updated:** May 2026
        """)


# ===================== MAIN APP =====================
def main():
    """Main application entry point."""
    load_dotenv()
    config.ensure_paths()
    setup_logging(config.LOGS_DIR, log_level=logging.INFO)
    
    setup_page()
    show_header()
    
    # Check configuration
    if not config.validate():
        st.warning("⚠️ Some API keys are missing. Some features may be limited.")
    
    # Main navigation tabs
    tab_home, tab_features, tab_settings = st.tabs([
        "🏠 Home",
        "🚀 Features",
        "⚙️ Settings"
    ])
    
    with tab_home:
        show_dashboard()
        st.markdown("---")
        st.subheader("📊 Quick Start")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎤 Start Transcribing", use_container_width=True):
                st.session_state.feature_tab = 1
                st.rerun()
        with col2:
            if st.button("🧠 Analyze Notes", use_container_width=True):
                st.session_state.feature_tab = 2
                st.rerun()
        with col3:
            if st.button("📄 Create Document", use_container_width=True):
                st.session_state.feature_tab = 4
                st.rerun()
    
    with tab_features:
        # Feature navigation
        feature_tabs = st.tabs([
            "🎤 Speech to Text",
            "🧠 AI Analysis",
            "✅ Action Items",
            "💡 Insights",
            "📄 Documents",
            "📧 Email",
            "😊 Sentiment",
            "📱 SMS"
        ])
        
        with feature_tabs[0]:
            feature_speech_to_text()
        
        with feature_tabs[1]:
            feature_ai_analysis()
        
        with feature_tabs[2]:
            feature_action_items()
        
        with feature_tabs[3]:
            feature_meeting_insights()
        
        with feature_tabs[4]:
            feature_document_generation()
        
        with feature_tabs[5]:
            feature_email_generation()
        
        with feature_tabs[6]:
            feature_sentiment_analysis()
        
        with feature_tabs[7]:
            feature_communication()
    
    with tab_settings:
        show_settings()


if __name__ == "__main__":
    main()
