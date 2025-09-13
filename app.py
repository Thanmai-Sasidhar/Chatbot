import streamlit as st
import google.generativeai as genai
import io
import os

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

# Load Gemini API key securely from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model
GEMINI_MODEL = "gemini-1.5-flash"

# ----------------- SESSION STATE -----------------
if "history" not in st.session_state:
    st.session_state.history = {}
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "rename_chat" not in st.session_state:
    st.session_state.rename_chat = None
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

# Initialize first chat
if not st.session_state.history:
    cid = f"chat_{st.session_state.chat_counter}"
    st.session_state.chat_counter += 1
    st.session_state.current_chat = cid
    st.session_state.history[cid] = {
        "name": "Default Chat",
        "messages": [{"role": "system", "content": st.session_state.system_prompt}],
    }
elif st.session_state.current_chat is None:
    st.session_state.current_chat = list(st.session_state.history.keys())[0]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    if st.button("➕ New Chat", use_container_width=True):
        cid = f"chat_{st.session_state.chat_counter}"
        st.session_state.chat_counter += 1
        st.session_state.current_chat = cid
        st.session_state.history[cid] = {
            "name": "New Chat",
            "messages": [{"role": "system", "content": st.session_state.system_prompt}],
        }

    st.markdown("## 💾 Chat History")
    for cid, chat in st.session_state.history.items():
        cols = st.columns([0.8, 0.2])
        if cols[0].button(chat["name"], key=f"chat_{cid}", use_container_width=True):
            st.session_state.current_chat = cid
        if cols[1].button("⋮", key=f"menu_{cid}"):
            st.session_state.rename_chat = cid

        if st.session_state.rename_chat == cid:
            new_name = st.text_input("Rename", chat["name"], key=f"rename_input_{cid}")
            if st.button("✅ Save", key=f"save_{cid}"):
                st.session_state.history[cid]["name"] = new_name or chat["name"]
                st.session_state.rename_chat = None
            if st.button("🗑 Delete", key=f"delete_{cid}"):
                del st.session_state.history[cid]
                st.session_state.rename_chat = None
                st.session_state.current_chat = (
                    list(st.session_state.history.keys())[0] if st.session_state.history else None
                )
                st.rerun()

# ----------------- MAIN CHAT AREA -----------------
st.title("💬 Chat with Gemini")

if st.session_state.current_chat:
    chat = st.session_state.history[st.session_state.current_chat]

    # Display existing messages
    for msg in chat["messages"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # User input
    prompt = st.chat_input("Ask something...")
    if prompt:
        # Rename default chats automatically
        if chat["name"] in ["New Chat", "Default Chat"]:
            chat["name"] = prompt[:40] + ("..." if len(prompt) > 40 else "")

        chat["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            placeholder, full_text = st.empty(), ""
            try:
                # ---- Gemini Response ----
                model = genai.GenerativeModel(GEMINI_MODEL)
                stream = model.generate_content(
                    [m["content"] for m in chat["messages"] if m["role"] in ("system", "user")],
                    stream=True,
                )
                for chunk in stream:
                    if chunk.text:
                        full_text += chunk.text
                        placeholder.markdown(full_text)

            except Exception as e:
                full_text = f"❌ Error: {e}"
                placeholder.error(full_text)

            chat["messages"].append({"role": "assistant", "content": full_text})

    # Export chat option
    if len(chat["messages"]) > 1:
        txt = "".join(
            [f"{m['role'].upper()}: {m['content']}\n\n" for m in chat["messages"] if m["role"] != "system"]
        )
        st.download_button(
            "📤 Share Current Chat",
            data=io.BytesIO(txt.encode()),
            file_name=f"{chat['name'].replace(' ', '_')}.txt",
            mime="text/plain",
        )

else:
    st.info("Start a new chat from the sidebar ➕")
