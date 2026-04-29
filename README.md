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

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
source venv/bin/activate     # On Linux/Mac
```

### 2. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys. You may also set optional values in `config/app.yml` for defaults.

```bash
cp .env.example .env
```

Required keys:
- `ANTHROPIC_API_KEY` - Claude AI API key
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_FROM_NUMBER` - Twilio sender phone number

Optional keys:
- `OPENAI_API_KEY` - OpenAI API key (for Whisper, if needed)
- `GOOGLE_API_KEY` - Google API key
- `GOOGLE_CREDENTIALS_FILE` - Path to Google OAuth or service account credentials

### 4. Run Application

```bash
streamlit run src/run.py
```

## Dependencies

See `requirements.txt` for complete list. Main dependencies:
- streamlit - Web UI framework
- anthropic - Claude AI API
- openai-whisper - Speech-to-text
- google-auth-oauthlib - Google authentication
- python-docx - Document generation
- twilio - SMS/communication service
- pyaudio - Audio input/output
- python-dotenv - Environment variable management

## Usage

1. Activate virtual environment
2. Run: `streamlit run src/run.py`
3. Open browser to http://localhost:8501
4. Select mode from sidebar (Speech to Text, AI Analysis, etc.)

## Development

### Adding New Features

1. Create module in `src/modules/`
2. Import in `src/app.py`
3. Add UI components in appropriate section
4. Update requirements.txt if needed

### Logging

Application logs are saved to `logs/app.log`

## Troubleshooting

- **PyAudio issues on Windows**: Use `pipwin install pyaudio` or Python 3.11/3.12
- **Missing API keys**: Check `.env` file and ensure keys are set
- **Import errors**: Verify all packages installed with `pip list`

## License

MIT

## Author

MeetMind Team
