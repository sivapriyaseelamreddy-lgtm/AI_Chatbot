
# AI_Chatbot


> A full-stack AI chatbot web application powered by **Groq** and built with **Flask + SQLite**.
> Features a stunning **Copilot-inspired dark UI** with conversation history, context memory, and stream-like animations.

---

## 🚀 Features

| Feature | Status |
| AI Chat (Groq API) | ✅ |
| Conversation History | ✅ |
| Context Memory | ✅ |
| New Chat | ✅ |
| View Previous Chats | ✅ |
| Delete Conversation | ✅ |
| SQLite Database | ✅ |
| Dark Copilot-Inspired UI | ✅ |
| Typing Animation | ✅ |
| Stream-like Response Animation | ✅ |
| Auto-Scroll | ✅ |
| Search Chats | ✅ |
| Responsive Design | ✅ |
| Error Handling | ✅ |
| Sidebar | ✅ |
| Auto-generated Chat Titles | ✅ |
| Markdown Rendering | ✅ |

## 📁 Project Structure
AI_Chatbot/
│
├── app.py               # Flask application & API routes
├── config.py            # Configuration (API keys, model, DB path)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this!)
├── README.md
│
├── database/
│   ├── database.py      # SQLite operations
│   └── chatbot.db       # Auto-created SQLite database
│
├── templates/
│   └── index.html       # Main HTML template
│
├── static/
│   ├── css/
│   │   └── style.css    # Copilot-inspired dark theme
│   └── js/
│       └── script.js    # Frontend logic
│
└── chat/
    └── groq_chat.py     # Groq API integration

## ⚙️ Installation & Setup

### 1. Clone / Download the project

```bash
cd "k hub chatbot"
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Your Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

Get your free API key at: https://console.groq.com

### 5. Run the Application

```bash
python app.py
```

### 6. Open in Browser

Navigate to: **http://127.0.0.1:5000**


## 🔌 API Endpoints

| Method | Endpoint | Description |
| `GET` | `/` | Serve the main UI |
| `POST` | `/api/new-chat` | Create a new conversation |
| `POST` | `/api/chat` | Send a message & get AI reply |
| `GET` | `/api/conversations` | Get all conversations |
| `GET` | `/api/conversation/<id>` | Get a specific conversation |
| `DELETE` | `/api/conversation/<id>` | Delete a conversation |


## 🗄️ Database Schema

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
);
```

## 🤖 AI Provider

- **Groq API** (AI model configurable through the backend)

## 📝 Environment Variables

| Variable | Description |
| `GROQ_API_KEY` | Your Groq API key (required) |


## 🛡️ Security Notes

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore`
- The API key is loaded securely via `python-dotenv`


*Built with ❤️ using Flask, Groq, and vanilla HTML/CSS/JS*
=======
# AI_Chatbot
>>>>>>> 54b15104c2bf64f57de4055570d40d9ef4399100
