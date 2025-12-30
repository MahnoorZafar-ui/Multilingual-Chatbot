import streamlit as st
from backend import MultilingualChatbot
from datetime import datetime

st.title("Daeson Multilingual Chatbot")

# ---------------------------
# Initialize Session State
# ---------------------------
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.all_chats[st.session_state.current_chat_id] = []

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("### Settings")

    language = st.selectbox(
        "Select Language",
        ["English", "Spanish", "Turkish", "French", "Hindi", "Italian", "Chinese", "Arabic", "Japanese", "German"]
    )

    # New chat button
    if st.button("New Chat"):
        st.session_state.current_chat_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.all_chats[st.session_state.current_chat_id] = []
        st.rerun()

    # Previous chats
    st.markdown("---")
    st.markdown("### Previous Chats")

    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        chat_messages = st.session_state.all_chats[chat_id]

        label = "Empty Chat"
        if chat_messages:
            label = chat_messages[0]["content"][:30]

        is_current = chat_id == st.session_state.current_chat_id

        if st.button(
            f"{'👉' if is_current else ''} {label}...",
            key=chat_id,
            use_container_width=True
        ):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# ---------------------------
# MAIN CHAT AREA
# ---------------------------

current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

# Display existing chat messages
for msg in current_chat:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input field
prompt = st.chat_input("Type your message...")

if prompt:
    # Save + display user message
    st.chat_message("user").write(prompt)
    current_chat.append({"role": "user", "content": prompt})

    # Call chatbot API
    bot = MultilingualChatbot()
    response = bot.chat(
        message=prompt,
        language=language,
        history=current_chat
    )

    # Save + display assistant response
    st.chat_message("assistant").write(response)
    current_chat.append({"role": "assistant", "content": response})

    st.rerun()
