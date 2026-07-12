from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Ensure project root is in the path
sys.path.insert(0, os.path.dirname(__file__))

from database.database import (
    init_db, create_conversation, get_all_conversations,
    get_conversation_messages, save_message, delete_conversation,
    get_conversation_by_id, update_conversation_title
)
from chat.groq_chat import chat_with_groq, generate_title

app = Flask(__name__)
CORS(app)

# Initialize the database on startup
with app.app_context():
    init_db()


# ─────────────────────────── Routes ───────────────────────────

@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/api/new-chat", methods=["POST"])
def new_chat():
    """Create a new conversation."""
    try:
        conv_id = create_conversation("New Chat")
        return jsonify({"conversation_id": conv_id, "title": "New Chat"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """Send a message and get an AI response."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        conv_id = data.get("conversation_id")
        user_message = data.get("message", "").strip()

        if not conv_id:
            return jsonify({"error": "conversation_id is required"}), 400
        if not user_message:
            return jsonify({"error": "message cannot be empty"}), 400

        # Verify conversation exists
        conversation = get_conversation_by_id(conv_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        # Load conversation history for context
        history = get_conversation_messages(conv_id)

        # Auto-generate title from first user message
        if len(history) == 0:
            try:
                title = generate_title(user_message)
                update_conversation_title(conv_id, title)
            except Exception:
                title = user_message[:50]
                update_conversation_title(conv_id, title)
        else:
            title = conversation["title"]

        # Save user message
        save_message(conv_id, "user", user_message)

        # Get AI response
        ai_reply = chat_with_groq(history, user_message)

        # Save AI response
        save_message(conv_id, "assistant", ai_reply)

        return jsonify({
            "reply": ai_reply,
            "title": title,
            "conversation_id": conv_id
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/api/conversations", methods=["GET"])
def get_conversations():
    """Get all conversations."""
    try:
        conversations = get_all_conversations()
        return jsonify(conversations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/conversation/<int:conv_id>", methods=["GET"])
def get_conversation(conv_id):
    """Get a specific conversation with all its messages."""
    try:
        conversation = get_conversation_by_id(conv_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        messages = get_conversation_messages(conv_id)
        return jsonify({
            "conversation": conversation,
            "messages": messages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/conversation/<int:conv_id>", methods=["DELETE"])
def delete_conv(conv_id):
    """Delete a conversation and all its messages."""
    try:
        conversation = get_conversation_by_id(conv_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        delete_conversation(conv_id)
        return jsonify({"message": "Conversation deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Keep legacy route for compatibility
@app.route("/api/delete/<int:conv_id>", methods=["DELETE"])
def delete_conv_legacy(conv_id):
    return delete_conv(conv_id)


if __name__ == "__main__":
    print("Starting K-Hub AI Chatbot...")
    print("Running at http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
