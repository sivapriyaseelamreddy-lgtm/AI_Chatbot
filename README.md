# AI_Chatbot

> A full-stack AI chatbot web application built using **Flask + SQLite + Groq API**.  
> It provides a Copilot-inspired dark UI with conversation history, context memory, and smooth chat interactions.

---


# 📁 Project Structure

```
AI_Chatbot/
│
├── app.py                  # Flask application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create manually)
├── README.md
│
├── database/
│   ├── database.py         # SQLite database operations
│   └── chatbot.db          # Auto-created database
│
├── templates/
│   └── index.html          # Main chatbot UI
│
├── static/
│   ├── css/
│   │   └── style.css       # UI styling
│   │
│   └── js/
│       └── script.js       # Frontend JavaScript logic
│
└── chat/
    └── groq_chat.py        # Groq API integration
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/sivapriyaseelamreddy-lgtm/AI_Chatbot.git
```

Move into the project folder:

```bash
cd AI_Chatbot
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 4. Configure API Key

Create a `.env` file inside the project root directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_actual_api_key_here
```

Get your API key from:

https://console.groq.com

---

# ▶️ 5. Run the Application

Start Flask server:

```bash
python app.py
```

---

# 🌐 6. Open Application

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Load chatbot interface |
| POST | `/api/new-chat` | Create new conversation |
| POST | `/api/chat` | Send message and receive AI response |
| GET | `/api/conversations` | Get chat history |
| GET | `/api/conversation/<id>` | View specific conversation |
| DELETE | `/api/conversation/<id>` | Delete conversation |

---

# 🗄️ Database

This project uses SQLite database.

Tables:

### Conversations

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Messages

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

# 🤖 AI Technology

- Groq API
- Large Language Model Integration
- Context-aware conversations

---

# 🛡️ Security Notes

- Never upload `.env` file to GitHub
- Keep API keys private
- Add sensitive files to `.gitignore`

---

# 🛠️ Technologies Used

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS
- JavaScript

### AI
- Groq API

---

## 👩‍💻 Author

Built with ❤️ using Flask, Groq API, SQLite, HTML, CSS and JavaScript.
