# 🚀 CODE GENAI: Chatbot with Gemini

**Submitted By:** A. Thanmai Sasidhar  
**Milestone 2:** Chatbot with Gemini  

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://your-app-link.streamlit.app)

---

## 📌 1. Setup Instructions

### 1.1 Getting Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).  
2. Sign in with your Google account.  
3. Navigate to **API Keys → Create API Key**.  
4. Copy the generated key.  
5. Configure it in your project:  


import google.generativeai as genai
genai.configure(api_key="YOUR_GEMINI_API_KEY")
1.2 Python Dependencies
Install the required packages:

pip install streamlit google-generativeai
1.3 Running the App
Run the chatbot locally:


streamlit run app.py
The app will open in your browser at:
👉 http://localhost:8501

⚙️ 2. Working
This project implements a chatbot system powered by Google’s Gemini API.
The app is built with Streamlit, providing a clean and interactive web interface.

The sidebar is used for navigation and chat history management.

The main area displays the conversation flow in a chat-like format.

Chat histories are stored in st.session_state, allowing multiple chats to coexist.

Users can export chats into a plain text file.

🔑 Key Features
✅ Built using Streamlit for an interactive UI

✅ Model: Google Gemini API (gemini-1.5-flash)

✅ Persistent chat history

✅ Multiple chats with rename & delete options

✅ Export chat history as .txt

✅ Streaming responses for better user experience

🧰 3. Technologies Used
Python Libraries: streamlit, google-generativeai, io

Model: Gemini API (gemini-1.5-flash)

Export Format: Plain text
