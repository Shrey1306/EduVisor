# EduVisor

**AI-powered lecture analysis platform for educators**

EduVisor helps teachers improve their lecturing skills by analyzing lecture videos using AI. Get insights on speech patterns, emotional engagement, and personalized feedback.

---

## Features

- **Video Upload** - Upload lecture videos for analysis
- **Emotion Recognition** - Detect speech emotions using wav2vec2
- **Transcription** - Automatic speech-to-text via Google Cloud
- **Analytics Dashboard**:
  - Engagement score (% of engaging segments)
  - Tone modulation (vocal variety)
  - Speaking pace (words per minute)
  - Question count
- **Visual Timeline** - Interactive engagement chart
- **AI Feedback** - Personalized improvement suggestions from GPT-3.5
- **History Tracking** - Track progress across lectures

---

## Project Structure

```
EduVisor/
├── src/                        # Source code
│   ├── config/                 # Django configuration
│   │   ├── settings.py         # Project settings
│   │   ├── urls.py             # Root URL routing
│   │   ├── wsgi.py             # WSGI entry point
│   │   └── asgi.py             # ASGI entry point
│   │
│   ├── apps/                   # Django applications
│   │   ├── uploads/            # Video upload handling
│   │   │   ├── models.py       # Video model
│   │   │   ├── views.py        # Upload/preview views
│   │   │   ├── forms.py        # Upload form
│   │   │   └── urls.py         # Upload routes
│   │   │
│   │   ├── analysis/           # Lecture analysis
│   │   │   ├── views.py        # Analysis views
│   │   │   └── urls.py         # Analysis routes
│   │   │
│   │   └── lectures/           # Lecture history
│   │       ├── models.py       # Lecture model
│   │       ├── views.py        # History views
│   │       └── urls.py         # History routes
│   │
│   ├── core/                   # Core business logic
│   │   └── services/           # Service modules
│   │       ├── analyzer.py     # Main orchestrator
│   │       ├── audio.py        # Audio extraction
│   │       ├── speech.py       # Speech-to-text
│   │       ├── emotion.py      # Emotion recognition
│   │       ├── metrics.py      # Metrics calculation
│   │       ├── visualization.py # Chart generation
│   │       ├── ai_feedback.py  # OpenAI integration
│   │       └── config.py       # Configuration
│   │
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── uploads/
│   │   ├── analysis/
│   │   └── lectures/
│   │
│   ├── static/                 # Static assets
│   │   └── css/main.css
│   │
│   └── manage.py               # Django CLI
│
├── data/                       # Runtime data (gitignored)
│   ├── audio/                  # Temporary audio files
│   ├── media/                  # Uploaded videos
│   └── config.json             # API keys (gitignored)
│
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- FFmpeg (for audio processing)

### 1. Clone & Setup Environment

```bash
git clone https://github.com/yourusername/EduVisor.git
cd EduVisor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `data/config.json`:

```json
{
  "google_cloud_key": "/path/to/your/google-cloud-key.json",
  "openai_key": "sk-your-openai-api-key",
  "hugging_face_key": "hf_your-huggingface-key"
}
```

**Or** use environment variables:

```bash
export GOOGLE_CLOUD_KEY_PATH=/path/to/google-cloud-key.json
export OPENAI_API_KEY=sk-your-openai-api-key
export HUGGINGFACE_API_KEY=hf_your-huggingface-key
```

### 3. Initialize Database

```bash
cd src
python manage.py migrate
```

### 4. Run the Server

```bash
python manage.py runserver
```

### 5. Open in Browser

Navigate to: **http://localhost:8000**

---

## Usage Guide

1. **Upload** - Go to the home page and upload your lecture video
2. **Preview** - Review the uploaded video
3. **Analyze** - Click "Analyze Lecture" to start AI processing
4. **View Results** - See metrics, timeline, and AI feedback
5. **Track History** - Access previous analyses from "Previous Lectures"

---

## API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| Google Cloud | Speech-to-Text | [Google Cloud Console](https://console.cloud.google.com/) |
| OpenAI | GPT-3.5 Feedback | [OpenAI Platform](https://platform.openai.com/) |
| Hugging Face | Model Downloads | [Hugging Face](https://huggingface.co/settings/tokens) |

---

## Tech Stack

- **Backend**: Django 4.2
- **ML/AI**: Transformers (wav2vec2), Google Cloud Speech, OpenAI GPT-3.5
- **Audio**: MoviePy, PyDub
- **Visualization**: Plotly
- **Frontend**: HTML, CSS, JavaScript

---

## Development

### Run Development Server

```bash
cd src
python manage.py runserver
```

### Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

---

## Screenshots

![Upload Page](https://github.com/sid0402/EduVisor/assets/36813259/35fd064a-a74a-4307-ba45-790459bf528d)

![Analysis Dashboard](https://github.com/sid0402/EduVisor/assets/36813259/318e7ae1-90cd-44fd-8ad7-15cf0bcaac7d)

---

## Demo Video

[Watch on YouTube](https://youtu.be/acVxFY_FH6o?si=EZ737nJ70-gSSzw-)

---

## License

MIT License

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request
