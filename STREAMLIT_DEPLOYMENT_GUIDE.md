# MeetMind - Streamlit Deployment Guide

## 📋 Table of Contents
1. [Project Architecture](#project-architecture)
2. [Backend Structure](#backend-structure)
3. [UI/UX Implementation](#uiux-implementation)
4. [Deployment Methods](#deployment-methods)
5. [Configuration & Setup](#configuration--setup)
6. [How to Run](#how-to-run)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ Project Architecture

### Overview
MeetMind is a **Streamlit-based web application** that helps users:
- Transcribe meeting audio → Speech to Text
- Analyze meeting notes → AI Analysis (Claude)
- Generate professional documents → Document Generation
- Send reminders → Communication (Twilio SMS)

### Tech Stack
```
Frontend: Streamlit (Python UI framework)
Backend: Python modules (Anthropic, Whisper, Twilio, Google Drive API)
Database: Local file system + YAML config
APIs: 
  - Anthropic Claude API (analysis)
  - OpenAI Whisper (transcription)
  - Twilio (SMS)
  - Google Drive API (optional auth)
```

---

## 💻 Backend Structure

### Core Modules (`src/meetmind/modules/`)

#### 1. **AnthropicClient** (`anthropic_client.py`)
- **Purpose**: Analyze meeting notes using Claude AI
- **Function**: `analyze_meeting_notes(notes: str) → str`
- **Features**:
  - Generates summaries
  - Extracts action items
  - Identifies key decisions
  - Suggests next steps

```python
# Example usage in backend
client = AnthropicClient(api_key="your-key")
analysis = client.analyze_meeting_notes("Meeting transcript here...")
```

#### 2. **SpeechToText** (`speech.py`)
- **Purpose**: Transcribe audio files to text
- **Model**: OpenAI Whisper
- **Supported Formats**: WAV, MP3, M4A, MP4, FLAC, AAC
- **Function**: `transcribe_audio(audio_path: str) → str`

```python
# Example usage
speech = SpeechToText(sample_rate=16000, channels=1)
transcript = speech.transcribe_audio("meeting.wav")
```

#### 3. **DocumentHandler** (`document_handler.py`)
- **Purpose**: Generate professional meeting minutes
- **Output Format**: DOCX (Word document)
- **Function**: `create_meeting_minutes(title, attendees, agenda, notes, action_items) → path`

```python
# Example usage
handler = DocumentHandler(template_dir="templates/")
doc_path = handler.create_meeting_minutes(
    title="Weekly Sync",
    attendees=["John", "Jane"],
    agenda=["Q1 Review", "Budget"],
    notes="...",
    action_items=["Item 1", "Item 2"]
)
```

#### 4. **TwilioHandler** (`twilio_handler.py`)
- **Purpose**: Send SMS reminders
- **Function**: `send_meeting_reminder(phone, title, time) → message_sid`

```python
# Example usage
twilio = TwilioHandler(account_sid, auth_token, from_number)
sid = twilio.send_meeting_reminder("+1234567890", "Team Sync", "Tomorrow 10AM")
```

#### 5. **GoogleAuth** (`google_auth.py`)
- **Purpose**: Optional Google Drive integration
- **Use Case**: Store generated documents to Drive

### Configuration (`config.py`)
Manages:
- API keys (from environment variables)
- File paths (uploads, templates, logs)
- Audio settings (sample rate, channels)
- Validation of required configs

### Utils (`utils.py`)
- File upload handling
- Logging setup
- Path creation

---

## 🎨 UI/UX Implementation

### Streamlit Structure

The UI is built using Streamlit's **widget-based approach** with a sidebar navigation pattern.

#### **Page Layout**

```
┌─────────────────────────────────────────────┐
│  🧠 MeetMind - Meeting Management Tool      │
├─────────────────────┬───────────────────────┤
│                     │                       │
│  SELECT MODE        │   MAIN CONTENT        │
│  ─────────────      │   ──────────────      │
│  • Speech to Text   │   (Dynamic based on   │
│  • AI Analysis      │    selected mode)     │
│  • Document Gen     │                       │
│  • Communication    │                       │
│                     │                       │
└─────────────────────┴───────────────────────┘
```

#### **Mode 1: Speech to Text** 
```python
┌─ Header: "Speech to Text"
├─ Description text
├─ File uploader widget
├─ Audio player (shows uploaded file)
├─ "Transcribe" button (with spinner)
└─ Text area (displays transcript)
```

**User Flow:**
1. Upload audio file (WAV, MP3, M4A, etc.)
2. File saved to `data/uploads/`
3. Click transcribe → Whisper API processes
4. Results displayed in expandable text area
5. Can copy text or download

#### **Mode 2: AI Analysis**
```python
┌─ Header: "AI Analysis"
├─ Text area for pasting notes
├─ "Analyze notes" button
├─ Results showing:
│  ├─ Summary
│  ├─ Action Items
│  ├─ Key Decisions
│  └─ Next Steps
```

**User Flow:**
1. Paste or type meeting transcript
2. Click "Analyze notes"
3. Claude AI processes (2-5 seconds)
4. Results displayed with formatting
5. User can copy/download results

#### **Mode 3: Document Generation**
```python
┌─ Form Elements:
├─ Meeting title (text input)
├─ Attendees (text area - one per line)
├─ Agenda items (text area - one per line)
├─ Meeting notes (text area)
├─ Action items (text area - one per line)
├─ Submit button
│
└─ Results:
   ├─ Success message
   └─ Download button (DOCX file)
```

**User Flow:**
1. Fill form with meeting details
2. Submit form
3. Python-docx generates DOCX file
4. Download button appears
5. User downloads professional document

#### **Mode 4: Communication**
```python
┌─ Twilio Configuration Check
├─ Recipient phone (text input)
├─ Meeting title (text input)
├─ Meeting time (text input)
├─ "Send reminder" button
│
└─ Status:
   ├─ Success: "Reminder sent (SID: ...)"
   └─ Error: "Failed to send..."
```

**User Flow:**
1. Verify Twilio is configured
2. Enter phone number, meeting details
3. Click send
4. SMS sent via Twilio API
5. Confirmation message

### Caching Strategy

```python
@st.cache_data(show_spinner=False)
def cached_transcribe(audio_path: str) → str:
    # Streamlit caches this result
    # Re-runs only if audio_path changes
    return speech.transcribe_audio(audio_path)

@st.cache_data(show_spinner=False)
def cached_analyze(notes: str) → str:
    # Caches analysis results
    # Prevents duplicate API calls
    return client.analyze_meeting_notes(notes)
```

### UI/UX Features

1. **Responsive Design**: Works on desktop, tablet, mobile
2. **Loading States**: Spinners show during processing
3. **Error Handling**: User-friendly error messages
4. **Success Feedback**: Green success banners
5. **Expandable Sections**: Better organization of content
6. **Form Validation**: Checks for empty inputs before processing
7. **Download Buttons**: Easy export of results

---

## 🚀 Deployment Methods

### **Method 1: Streamlit Cloud (RECOMMENDED)**

#### Pros:
- ✅ Free hosting (up to 3 apps)
- ✅ Automatic deployment from GitHub
- ✅ HTTPS by default
- ✅ Environment variables support
- ✅ Easy to scale

#### Cons:
- ❌ Limited to 1GB memory
- ❌ 30 minute timeout per request

#### Steps:

**1. Push code to GitHub** (Already done ✓)
```bash
git add .
git commit -m "Add Streamlit deployment files"
git push -u origin main
```

**2. Create Streamlit Cloud Account**
- Visit https://streamlit.io/cloud
- Sign up with GitHub account
- Authorize Streamlit access to repos

**3. Deploy App**
- Click "New app"
- Select your repo: `meetmind`
- Branch: `main`
- File path: `src/meetmind/app.py`
- Click "Deploy"

**4. Add Secrets** (Streamlit Cloud → App Settings → Secrets)
```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "sk-ant-..."
TWILIO_ACCOUNT_SID = "ACxxxxx"
TWILIO_AUTH_TOKEN = "xxxxx"
TWILIO_FROM_NUMBER = "+1234567890"
GOOGLE_API_KEY = "xxxxx"
```

---

### **Method 2: Local Execution**

#### Prerequisites:
- Python 3.9+
- Git
- Disk space (5+ GB for dependencies)

#### Steps:

**1. Free up disk space**
```powershell
# Check disk space
Get-Volume

# Clear temp files
Remove-Item -Path $env:TEMP -Recurse -Force
Remove-Item -Path $env:LocalAppData\Temp -Recurse -Force
```

**2. Clone repository**
```bash
git clone https://github.com/yourusername/meetmind.git
cd meetmind
```

**3. Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Create `.env` file**
```
ANTHROPIC_API_KEY=sk-ant-your-key
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_FROM_NUMBER=+1234567890
GOOGLE_API_KEY=your-key
APP_NAME=MeetMind
```

**6. Run Streamlit**
```bash
streamlit run src/meetmind/app.py
```

Opens at: `http://localhost:8501`

---

### **Method 3: Docker Containerization**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "src/meetmind/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t meetmind .
docker run -p 8501:8501 --env-file .env meetmind
```

---

## ⚙️ Configuration & Setup

### **1. Environment Variables**

Create `.env` file in project root:

```env
# Anthropic API (Required for AI Analysis)
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# Twilio (Required for Communication mode)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=+1234567890  # Your Twilio phone number

# Google Drive (Optional, for document storage)
GOOGLE_API_KEY=your-google-api-key

# App settings
APP_NAME=MeetMind
SAMPLE_RATE=16000
CHANNELS=1
CHUNK_SIZE=4096
```

### **2. Streamlit Config** (`~/.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[server]
maxUploadSize = 200  # MB
enableXsrfProtection = true
```

### **3. Getting API Keys**

#### Anthropic API:
1. Go to https://console.anthropic.com
2. Sign up / Login
3. Create new API key
4. Copy to `.env`

#### Twilio:
1. Go to https://www.twilio.com/console
2. Get Account SID and Auth Token
3. Get a Twilio phone number (free trial available)
4. Add to `.env`

#### Google API:
1. https://cloud.google.com/docs/authentication
2. Create service account
3. Download JSON key

---

## 🎯 How to Run

### **Quick Start (Local)**

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/meetmind.git
cd meetmind
python -m venv venv
venv\Scripts\activate

# 2. Install + Configure
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API keys

# 3. Run
streamlit run src/meetmind/app.py
```

### **Production Deployment**

```bash
# Deploy to Streamlit Cloud
streamlit run src/meetmind/app.py

# Or use Docker
docker build -t meetmind .
docker run -p 8501:8501 --env-file .env meetmind
```

---

## 🐛 Troubleshooting

### Issue: "No space left on device"
```bash
# Solution: Clean up and install in stages
pip install streamlit anthropic
pip install openai-whisper
pip install google-auth-oauthlib google-api-python-client
pip install pyyaml python-docx twilio python-dotenv requests
```

### Issue: Audio transcription slow
- Use smaller files (< 25MB)
- GPU acceleration helps (requires CUDA)
- Whisper API is faster than local

### Issue: Anthropic API timeout
- Check internet connection
- Verify API key validity
- Monitor API rate limits

### Issue: File uploads not working
- Check `data/uploads/` permissions
- Verify disk space available
- Check Streamlit `maxUploadSize` setting

### Issue: Secrets not working in Cloud
- Use `.streamlit/secrets.toml` for local testing
- Use Streamlit Cloud interface for production secrets
- Don't commit secrets.toml to GitHub

---

## 📊 Performance Tips

1. **Caching**: Already implemented with `@st.cache_data`
2. **Lazy Loading**: Load modules only when needed
3. **Async Operations**: Consider for file uploads
4. **Database**: Switch to SQLite/PostgreSQL if scaling
5. **CDN**: Use for static files

---

## 📱 Mobile Responsiveness

Streamlit apps are mobile-responsive by default, but optimize with:

```python
st.set_page_config(
    layout="wide",  # Takes full width
    initial_sidebar_state="expanded"  # Sidebar always visible
)
```

---

## 🔐 Security Best Practices

1. ✅ Never commit `.env` to Git
2. ✅ Use `.gitignore` to exclude secrets
3. ✅ Validate all file uploads
4. ✅ Use HTTPS in production
5. ✅ Implement rate limiting for APIs
6. ✅ Sanitize user input
7. ✅ Use secrets manager for API keys

---

## 📈 Scalability Roadmap

**Phase 1** (Current): Single-user web app
**Phase 2**: Database backend (PostgreSQL)
**Phase 3**: User authentication (OAuth)
**Phase 4**: Multi-user collaboration
**Phase 5**: Analytics dashboard
**Phase 6**: Mobile app (React Native)

---

## 🤝 Contributing

Submit issues and PRs to: `https://github.com/yourusername/meetmind`

---

## 📞 Support

For issues:
- Check Streamlit docs: https://docs.streamlit.io
- Anthropic docs: https://docs.anthropic.com
- Twilio docs: https://www.twilio.com/docs

---

**Last Updated**: April 29, 2026
**Version**: 1.0
