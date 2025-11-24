import streamlit as st
from chatbot_backend import ChatBot
import time

# Page Config
st.set_page_config(
    page_title="Customer Service AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Advanced Creative Interface
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: #ffffff;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #252538;
        border-right: 1px solid #3f3f5f;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* User Message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
    }
    
    /* Assistant Message - Force white text */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
    }
    
    /* Force white color on assistant message content */
    .stChatMessage[data-testid="assistant-message"] p,
    .stChatMessage[data-testid="assistant-message"] span,
    .stChatMessage[data-testid="assistant-message"] div,
    .stChatMessage[data-testid="assistant-message"] .stMarkdown,
    .stChatMessage[data-testid="assistant-message"] [class*="st"] {
        color: white !important;
    }
    
    /* Input Box */
    .stTextInput > div > div > input {
        background-color: #2d2d44;
        color: white;
        border-radius: 20px;
        border: 1px solid #555;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 25px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize ChatBot
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = ChatBot()
        # Add some dummy knowledge for demo
        st.session_state.chatbot.create_knowledge_base([
            "Our support hours are 24/7 for premium members, and 9-5 for free users.",
            "You can reset your password by clicking 'Forgot Password' on the login page.",
            "Refunds are processed within 5-7 business days.",
            "We offer a 30-day money-back guarantee on all subscriptions."
        ])
    except Exception as e:
        st.error(f"Failed to initialize ChatBot: {e}. Please check your .env file.")

# Title and Header
st.title("✨ Stellar Support AI")
st.markdown("### *Your intelligent customer service companion*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    st.info("This chatbot uses Groq Llama 3 & Tavily Search.")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chatbot.memory.clear()
        st.rerun()

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            # Force white text for assistant messages
            st.markdown(f'<span style="color: white;">{message["content"]}</span>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        if "chatbot" in st.session_state:
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.get_response(prompt)
                    
                    # Simulate typing effect
                    for chunk in response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(f'<span style="color: white;">{full_response}▌</span>', unsafe_allow_html=True)
                    message_placeholder.markdown(f'<span style="color: white;">{full_response}</span>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
                    full_response = "I encountered an error. Please check your API keys."
                    message_placeholder.markdown(full_response)
        else:
             st.error("Chatbot not initialized.")
             full_response = "System Error."

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": full_response})

