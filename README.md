# MeetMind 🧠

Your intelligent meeting assistant powered by AI

## Features

- **Speech-to-Text**: Convert meeting audio to text using OpenAI Whisper
- **AI Analysis**: Analyze meeting notes with Claude AI
- **Document Generation**: Generate meeting minutes automatically
- **Communication**: Send reminders and updates via Twilio

## Project Structure

```
meetmind/
├── src/                      # Main application entry
│   ├── run.py               # Application launcher
│   └── meetmind/            # Application package
│       ├── __init__.py      # Package initializer
│       ├── app.py           # Streamlit application
│       ├── config.py        # Configuration settings loader
│       ├── utils.py         # Utility functions
│       └── modules/         # Feature modules
│           ├── __init__.py  # Module package initializer
│           ├── speech.py        # Speech-to-text
│           ├── anthropic_client.py  # Claude AI integration
│           ├── google_auth.py   # Google authentication
│           ├── document_handler.py  # Document generation
│           └── twilio_handler.py    # Communication
├── config/                  # Configuration files
├── data/                    # Data directory
│   ├── uploads/            # User uploads
│   └── templates/          # Document templates
├── logs/                   # Application logs
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example            # Example env file
└── README.md              # This file
```

## ⚡ Quick Start

### Windows Users
```bash
# Simply double-click:
run.bat
```

### macOS/Linux Users
```bash
chmod +x run.sh
./run.sh
```

### Manual Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows
   source venv/bin/activate     # On Linux/Mac
   ```

2. **Install Dependencies**
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run Application**
   ```bash
   streamlit run src/meetmind/app.py
   ```

Your app opens at: **http://localhost:8501**

## 🌐 Deployment

### Choose Your Method

- **[Streamlit Cloud](DEPLOYMENT.md#-option-1-streamlit-cloud-recommended)** (Free, recommended)
- **[Docker](DEPLOYMENT.md#-option-3-docker-production-ready)**
- **[Heroku](DEPLOYMENT.md#-option-4-heroku-deployment)**
- **[AWS App Runner](DEPLOYMENT.md#-option-6-aws-app-runner-recommended-for-aws)**
- **[Google Cloud Run](DEPLOYMENT.md#-option-7-google-cloud-run)**

**📖 Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

**📚 Detailed architecture guide:** See [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md)

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:

**Required:**
- `ANTHROPIC_API_KEY` - Claude AI API key (get from https://console.anthropic.com)
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_FROM_NUMBER` - Twilio sender phone number

**Optional:**
- `GOOGLE_API_KEY` - Google API key
- `APP_NAME` - Application name (default: MeetMind)
- `LOG_LEVEL` - Logging level (default: INFO)

## 🎯 Features & Usage

### 1. 🎤 Speech to Text
Convert meeting audio to text using OpenAI Whisper
- Upload audio files (WAV, MP3, M4A, MP4, FLAC, AAC)
- Automatic transcription
- Copy or download results

### 2. 🧠 AI Analysis
Analyze meeting notes with Claude AI
- Generate summaries
- Extract action items
- Identify key decisions
- Suggest next steps

### 3. 📄 Document Generation
Create professional meeting minutes
- Beautiful DOCX format
- Customizable templates
- Download directly

### 4. 📱 Communication
Send SMS reminders via Twilio
- Quick reminder setup
- Twilio integration
- Message tracking

## 📦 Dependencies

Main packages:
- **streamlit** - Web UI framework
- **anthropic** - Claude AI API
- **openai-whisper** - Speech-to-text
- **twilio** - SMS service
- **python-docx** - Document generation
- **google-auth-oauthlib** - Google authentication
- **pyaudio** - Audio input/output
- **python-dotenv** - Environment variable management
- **pyyaml** - Config file parsing
- **requests** - HTTP library

See [requirements.txt](requirements.txt) for complete list with versions.

## Development

### Adding New Features

1. Create module in `src/modules/`
2. Import in `src/app.py`
3. Add UI components in appropriate section
4. Update requirements.txt if needed

### Logging

Application logs are saved to `logs/app.log`

## 🔧 Troubleshooting

### Installation Issues
| Issue | Solution |
|-------|----------|
| Disk space error | `pip install --no-cache-dir -r requirements.txt` |
| PyAudio issues | Use Python 3.11+ or `pipwin install pyaudio` (Windows) |
| Missing modules | Run `pip list` to verify, then `pip install -r requirements.txt` |

### Runtime Issues
| Issue | Solution |
|-------|----------|
| "API key not found" | Check `.env` file is in project root and correctly set |
| Audio transcription fails | Verify Anthropic API key and file format |
| SMS won't send | Check Twilio credentials and phone number format |
| File uploads stuck | Check disk space and `maxUploadSize` in `.streamlit/config.toml` |

### Deployment Issues
See **[DEPLOYMENT.md](DEPLOYMENT.md)** → Troubleshooting section

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment methods & quick reference |
| [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md) | Detailed architecture & UI/UX |
| [TROUBLESHOOTING.md](#-troubleshooting) | Common issues & solutions |

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io
- **Anthropic API**: https://docs.anthropic.com
- **Twilio Docs**: https://www.twilio.com/docs
- **OpenAI Whisper**: https://openai.com/research/whisper
- **Streamlit Cloud**: https://streamlit.io/cloud

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 👥 Author

MeetMind Team

---

**Last Updated**: April 29, 2026  
**Version**: 1.0.0
