const state = {
  currentConvId: null,
  allConversations: [],
  isLoading: false,
};

async function loadConversations() {
  try {
    const response = await fetch("/api/conversations");
    if (!response.ok) throw new Error("Unable to load conversations");
    const conversations = await response.json();
    state.allConversations = conversations;
    renderConversationList(conversations);
    toggleEmptyState(conversations.length === 0);
  } catch (error) {
    console.error(error);
    showToast("Unable to load conversations.");
  }
}

function renderConversationList(conversations) {
  const list = document.getElementById("conversationList");
  list.querySelectorAll(".conv-item").forEach((item) => item.remove());
  conversations.forEach((conv) => {
    const item = document.createElement("div");
    item.className = `conv-item${conv.id === state.currentConvId ? " active" : ""}`;
    item.innerHTML = `
      <div>
        <div class="conv-item-title">${escapeHtml(conv.title || "New Chat")}</div>
      </div>
      <button class="conv-delete" type="button" aria-label="Delete conversation">×</button>
    `;
    item.addEventListener("click", (event) => {
      if (event.target.closest(".conv-delete")) return;
      openConversation(conv.id);
    });
    item.querySelector(".conv-delete").addEventListener("click", async (event) => {
      event.stopPropagation();
      await deleteConversation(conv.id);
    });
    list.appendChild(item);
  });
}

function toggleEmptyState(isEmpty) {
  document.getElementById("emptyState").classList.toggle("hidden", !isEmpty);
}

function moveConversationToTop(convId) {
  const index = state.allConversations.findIndex((conv) => conv.id === convId);
  if (index > 0) {
    const [conv] = state.allConversations.splice(index, 1);
    state.allConversations.unshift(conv);
    renderConversationList(state.allConversations);
  }
}

async function handleNewChat() {
  if (state.isLoading) return;
  try {
    const response = await fetch("/api/new-chat", { method: "POST" });
    if (!response.ok) throw new Error("Could not create chat");
    const data = await response.json();
    state.currentConvId = data.conversation_id;
    await loadConversations();
    moveConversationToTop(state.currentConvId);
    setChatTitle("New Chat", "Send your first message to begin.");
    showChatScreen();
    clearMessages();
    updateDeleteButton(true);
    focusInput();
  } catch (error) {
    console.error(error);
    showToast("Unable to create a new chat.");
  }
}

async function openConversation(convId) {
  if (state.isLoading) return;
  try {
    const response = await fetch(`/api/conversation/${convId}`);
    if (!response.ok) throw new Error("Could not open conversation");
    const data = await response.json();
    state.currentConvId = convId;
    moveConversationToTop(convId);
    setChatTitle(data.conversation.title || "K-Hub AI", "Ask anything from the assistant.");
    renderMessages(data.messages);
    showChatScreen();
    updateDeleteButton(true);
    focusInput();
  } catch (error) {
    console.error(error);
    showToast("Unable to open conversation.");
  }
}

async function handleSend() {
  const input = document.getElementById("messageInput");
  const text = input.value.trim();
  if (!text || state.isLoading) return;
  if (!state.currentConvId) {
    showToast("Create a chat first.");
    return;
  }
  input.value = "";
  resizeInput();
  document.getElementById("sendBtn").disabled = true;
  appendMessage("user", text, new Date().toISOString());
  scrollMessages();
  showTyping(true);
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conversation_id: state.currentConvId, message: text }),
    });
    const result = await response.json();
    showTyping(false);
    if (!response.ok) {
      throw new Error(result.error || "Unable to get reply");
    }
    if (result.title) {
      setChatTitle(result.title, "Continue the conversation.");
      await loadConversations();
    }
    appendMessage("assistant", result.reply, new Date().toISOString());
    scrollMessages();
  } catch (error) {
    console.error(error);
    showTyping(false);
    appendErrorMessage(error.message || "Chat failed.");
  } finally {
    state.isLoading = false;
    document.getElementById("sendBtn").disabled = document.getElementById("messageInput").value.trim() === "";
  }
}

function appendMessage(role, content) {
  const container = document.getElementById("messagesContainer");
  const message = document.createElement("div");
  message.className = `message-item ${role === "assistant" ? "message-ai" : "message-user"}`;
  message.innerHTML = `
    <div class="message-meta"><span>${role === "assistant" ? "K-Hub AI" : "You"}</span></div>
    <div class="message-content">${escapeHtml(content).replace(/\n/g, "<br>")}</div>
  `;
  container.appendChild(message);
}

function appendErrorMessage(message) {
  const container = document.getElementById("messagesContainer");
  const alert = document.createElement("div");
  alert.className = "message-item message-ai";
  alert.style.background = "rgba(220,38,38,0.18)";
  alert.innerHTML = `
    <div class="message-meta"><span>Error</span></div>
    <div class="message-content">${escapeHtml(message).replace(/\n/g, "<br>")}</div>
  `;
  container.appendChild(alert);
}

function renderMessages(messages) {
  clearMessages();
  messages.forEach((msg) => appendMessage(msg.role, msg.message, msg.timestamp));
}

function clearMessages() {
  document.getElementById("messagesContainer").innerHTML = "";
}

function setChatTitle(title, subtitle) {
  document.getElementById("chatTitle").textContent = title;
  document.getElementById("chatSubtitle").textContent = subtitle;
}

function showChatScreen() {
  document.getElementById("welcomeCard").classList.add("hidden");
  document.getElementById("chatScreen").classList.remove("hidden");
}

function showWelcomeScreen() {
  document.getElementById("welcomeCard").classList.remove("hidden");
  document.getElementById("chatScreen").classList.add("hidden");
  updateDeleteButton(false);
}

function showTyping(visible) {
  // Typing indicator removed; keep no-op to avoid runtime errors.
}

function scrollMessages() {
  const container = document.getElementById("messagesContainer");
  container.scrollTop = container.scrollHeight;
}

async function deleteConversation(convId) {
  if (!convId) return;
  if (!confirm("Delete this conversation?")) return;
  try {
    const response = await fetch(`/api/conversation/${convId}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Delete failed");
    showToast("Conversation deleted.");
    if (state.currentConvId === convId) {
      state.currentConvId = null;
      showWelcomeScreen();
      setChatTitle("Welcome to K-Hub AI", "This is your refreshed chat UI. Start a conversation now.");
      clearMessages();
    }
    await loadConversations();
  } catch (error) {
    console.error(error);
    showToast("Unable to delete conversation.");
  }
}

function handleSearch() {
  const query = document.getElementById("searchInput").value.trim().toLowerCase();
  const filtered = state.allConversations.filter((conv) => (conv.title || "").toLowerCase().includes(query));
  renderConversationList(filtered);
  toggleEmptyState(filtered.length === 0);
}

function updateDeleteButton(show) {
  document.getElementById("deleteChatBtn").classList.toggle("hidden", !show);
}

function focusInput() {
  const input = document.getElementById("messageInput");
  input.focus();
}

function resizeInput() {
  const input = document.getElementById("messageInput");
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 140)}px`;
}

function showToast(message, duration = 2800) {
  const toast = document.getElementById("toast");
  document.getElementById("toastMsg").textContent = message;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), duration);
}

function escapeHtml(text) {
  if (!text) return "";
  return text.replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function formatTime(isoString) {
  try {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("newChatBtn").addEventListener("click", handleNewChat);
  document.getElementById("sendBtn").addEventListener("click", handleSend);
  document.getElementById("messageInput").addEventListener("input", () => {
    resizeInput();
    document.getElementById("sendBtn").disabled = document.getElementById("messageInput").value.trim() === "";
  });
  document.getElementById("messageInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  });
  document.getElementById("searchInput").addEventListener("input", handleSearch);
  document.getElementById("deleteChatBtn").addEventListener("click", () => deleteConversation(state.currentConvId));
  loadConversations().then(() => {
    if (!state.currentConvId) {
      showWelcomeScreen();
    }
  });
});
