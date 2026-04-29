# 🚀 MeetMind Deployment Quick Reference

## Choose Your Deployment Method

### 🌐 **Option 1: Streamlit Cloud (Recommended)**
**Best for**: Production, easy deployment, free tier available

```bash
# 1. Ensure code is pushed to GitHub
git add .
git commit -m "Ready for deployment"
git push -u origin main

# 2. Go to https://streamlit.io/cloud
# 3. Click "New app"
# 4. Connect your GitHub repo
# 5. Select: repo=meetmind, branch=main, file=src/meetmind/app.py
# 6. Add secrets via Streamlit Cloud dashboard (Settings → Secrets)

# 7. Your app is live at: https://meetmind-yourusername.streamlit.app
```

**Secrets Format** (in Streamlit Cloud):
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
TWILIO_ACCOUNT_SID = "AC..."
TWILIO_AUTH_TOKEN = "..."
TWILIO_FROM_NUMBER = "+1234567890"
GOOGLE_API_KEY = "..."
```

**Pros:**
- ✅ Free tier available
- ✅ Automatic updates from Git
- ✅ HTTPS by default
- ✅ No infrastructure management

**Cons:**
- ❌ 1GB RAM limit
- ❌ 30min timeout per request
- ❌ Community support only on free

---

### 💻 **Option 2: Local Execution (Development)**
**Best for**: Testing, development, debugging

#### Windows:
```bash
# Double-click this file:
run.bat

# OR manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API keys
streamlit run src\meetmind\app.py
```

#### macOS/Linux:
```bash
# Make script executable
chmod +x run.sh

# Run it
./run.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
streamlit run src/meetmind/app.py
```

**App runs at:** `http://localhost:8501`

---

### 🐳 **Option 3: Docker (Production-Ready)**
**Best for**: Containerized deployment, cloud platforms (AWS, GCP, Azure)

```bash
# Build image
docker build -t meetmind:latest .

# Run container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY="your-key" \
  -e TWILIO_ACCOUNT_SID="your-sid" \
  -e TWILIO_AUTH_TOKEN="your-token" \
  -e TWILIO_FROM_NUMBER="+1234567890" \
  meetmind:latest

# OR with docker-compose:
docker-compose up -d
```

**Access at:** `http://localhost:8501`

**For AWS ECS/Fargate:**
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin xxxxx.dkr.ecr.us-east-1.amazonaws.com
docker tag meetmind:latest xxxxx.dkr.ecr.us-east-1.amazonaws.com/meetmind:latest
docker push xxxxx.dkr.ecr.us-east-1.amazonaws.com/meetmind:latest

# Then deploy via ECS console or CLI
```

---

### ☁️ **Option 4: Heroku Deployment**
**Best for**: Quick production deployment

```bash
# 1. Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Create Heroku app
heroku create meetmind-yourname

# 3. Add buildpack
heroku buildpacks:set heroku/python

# 4. Set config variables
heroku config:set ANTHROPIC_API_KEY="sk-ant-..."
heroku config:set TWILIO_ACCOUNT_SID="AC..."
heroku config:set TWILIO_AUTH_TOKEN="..."
heroku config:set TWILIO_FROM_NUMBER="+1234567890"

# 5. Create Procfile (already included)
# web: streamlit run src/meetmind/app.py --server.port=$PORT

# 6. Deploy
git push heroku main

# 7. View logs
heroku logs --tail
```

**App URL:** `https://meetmind-yourname.herokuapp.com`

---

### ☁️ **Option 5: AWS Lambda + API Gateway (Serverless)**
**Best for**: Very low-cost, infrequent usage

```bash
# Not ideal for Streamlit (UI apps)
# Better suited for REST APIs
# Consider AWS Amplify or App Runner instead
```

---

### ☁️ **Option 6: AWS App Runner (Recommended for AWS)**
**Best for**: AWS users, easy scaling

```bash
# 1. Push Docker image to ECR
# (see Docker section above)

# 2. Go to AWS App Runner console
# 3. Create service
# 4. Select ECR image source
# 5. Configure environment variables
# 6. Deploy

# Auto-scaling, HTTPS, and monitoring included!
```

---

### ☁️ **Option 7: Google Cloud Run**
**Best for**: Google Cloud users, serverless containers

```bash
# 1. Push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/meetmind

# 2. Deploy to Cloud Run
gcloud run deploy meetmind \
  --image gcr.io/PROJECT-ID/meetmind \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY="sk-ant-...",TWILIO_ACCOUNT_SID="..."

# 3. Service URL: https://meetmind-xxxxx-uc.a.run.app
```

---

### ☁️ **Option 8: Azure Container Instances + App Service**
**Best for**: Azure ecosystem

```bash
# 1. Push to Azure Container Registry
az acr build --registry myregistry --image meetmind:latest .

# 2. Deploy to App Service
az container create \
  --resource-group myResourceGroup \
  --name meetmind \
  --image myregistry.azurecr.io/meetmind:latest \
  --ports 8501 \
  --environment-variables ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Configuration Files Provided

| File | Purpose |
|------|---------|
| `.env.example` | Template for environment variables |
| `.streamlit/config.toml` | Streamlit app configuration |
| `.streamlit/secrets.toml` | Local secrets (don't commit) |
| `Dockerfile` | Docker container definition |
| `docker-compose.yml` | Multi-container setup |
| `run.bat` | Windows quick start script |
| `run.sh` | macOS/Linux quick start script |
| `Procfile` | Heroku deployment configuration |
| `requirements.txt` | Python dependencies |

---

## Environment Variables Reference

```bash
# Required for AI Analysis
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Required for Communication mode
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token-here
TWILIO_FROM_NUMBER=+1234567890

# Optional: Google Drive integration
GOOGLE_API_KEY=your-google-api-key-here

# Optional: App configuration
APP_NAME=MeetMind
LOG_LEVEL=INFO
DEBUG=false
```

---

## Troubleshooting Deployments

### Streamlit Cloud Issues
```bash
# App won't load
- Check secrets are set correctly
- View logs in Streamlit Cloud dashboard
- Restart app (Settings → Reboot app)

# File uploads not working
- Check storage permissions in .streamlit/config.toml
- Reduce maxUploadSize if needed

# API calls timeout
- Streamlit Cloud has 30min timeout
- Consider using async for long operations
```

### Docker Issues
```bash
# Build fails
docker build --no-cache -t meetmind:latest .

# Container won't start
docker run --rm meetmind:latest bash
# Check for runtime errors

# Port already in use
docker run -p 8502:8501 meetmind:latest
```

### Local Execution Issues
```bash
# Disk space error during pip install
pip install --no-cache-dir -r requirements.txt

# Audio library issues
# Windows: Install PyAudio from wheel
# macOS: brew install portaudio && pip install pyaudio
# Linux: sudo apt-get install portaudio19-dev && pip install pyaudio

# Module not found
pip list  # Verify all packages installed
source venv/bin/activate  # Ensure venv activated
```

---

## Performance Tips

| Tip | Impact |
|-----|--------|
| Use Streamlit Cloud caching | 60% faster reruns |
| Compress audio before upload | 50% upload time savings |
| Cache AI analysis results | 90% faster for same queries |
| Use smaller models | Lower latency, lower cost |
| Enable CDN for static files | 3x faster delivery |

---

## Cost Comparison

| Platform | Cost | Pros | Cons |
|----------|------|------|------|
| Streamlit Cloud (Free) | $0 | Easy, free tier | 1GB RAM, 30min timeout |
| Streamlit Cloud (Pro) | $5/month | More resources, support | Still limited RAM |
| Docker + AWS App Runner | $5-20/month | Auto-scaling, HTTPS | Infrastructure management |
| Heroku | $7-50/month | Simple, auto-scaling | Limited free tier |
| Google Cloud Run | $0.15/req | Pay-per-use, serverless | Cold starts |
| AWS Lambda | Not ideal | - | - |

---

## Recommended Deployment Path

### Development → Production

1. **Development**: Local with `.env`
   ```bash
   streamlit run src/meetmind/app.py
   ```

2. **Testing**: Docker locally
   ```bash
   docker-compose up
   ```

3. **Staging**: Streamlit Cloud (free tier)
   - Test production environment
   - Verify all integrations
   - Load test with users

4. **Production**: Choose based on needs
   - **Free**: Streamlit Cloud free tier
   - **Paid/Scaling**: Docker + AWS App Runner
   - **Complex**: Kubernetes (EKS, GKE, AKS)

---

## Next Steps

1. Choose your deployment method above
2. Follow the steps for that method
3. Set up your environment variables/secrets
4. Deploy and test
5. Monitor logs and performance
6. Scale as needed

**Need help?** See [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md) for detailed explanations.

---

**Last Updated**: April 29, 2026
