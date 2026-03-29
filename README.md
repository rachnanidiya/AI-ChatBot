# 🤖 AI Chatbot (Django + Gemini API)

A full-stack AI chatbot built using Django with modern UI and real-time features.

---

## 🚀 Features

- 🔐 User Authentication (Login/Logout)
- 💬 Chat History with Sidebar
- 🔍 Chat Search
- ✏️ Message Editing
- 🔁 Regenerate Response
- 📋 Copy Responses
- ⚡ Streaming Typing Effect
- 🎨 Modern UI (Bootstrap + Custom CSS)


## 🛠️ Tech Stack

- Django
- JavaScript (Fetch API)
- Bootstrap
- Google Gemini API
- PostgreSQL / Supabase (optional)



## ⚙️ Setup Instructions

### 1. Clone Repo

```bash
git clone https://github.com/your-username/ai-chatbot.git
cd ai-chatbot
```

2. Create Virtual Environment
```python -m venv venv```
```venv\Scripts\activate ```  # Windows

4. Install Dependencies
```pip install -r requirements.txt```

5. Add Environment Variables

```Create a .env file:```
```GEMINI_API_KEY=your_api_key_here```

5. Run Migrations
```python manage.py migrate```

7. Create Superuser
```python manage.py createsuperuser```

9. Run Server
```python manage.py runserver```
