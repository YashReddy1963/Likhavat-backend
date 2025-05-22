# Likhavat-backend
This repo contains the backend code of the likhavat project

---
## 🚀 Features

- User authentication (JWT-based)
- Blog management: create, edit, delete, view
- **AI Writing Assistant**:
  - Grammar check via LanguageTool
  - Sentiment analysis using `TextBlob`
  - Keyword extraction and synonyms
- Blog-to-Audio (Text-to-Speech using `gTTS`)
- Analytics with daily/monthly views, likes, comments
- Real-time **Notifications**:
  - New followers
  - New blogs from followed authors
  - AI-powered blog recommendations
- Comments API
- Save blogs API
- Follow/unfollow authors
- Tag-based categorization for recommendations

---

## 📦 Tech Stack

- **Python 3.10+**
- **Django 4+**
- **Django REST Framework**
- **PostgreSQL**
- **gTTS** (Google Text-to-Speech)
- **TextBlob**, **nltk**, and **LanguageTool** (for AI features)

---
## 🔧 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/YashReddy1963/Likhavat-backend.git

2. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Apply migrations:
   ```bash
   python manage.py migrate

5. Start the development server:
   ```bash
   python manage.py runserver
