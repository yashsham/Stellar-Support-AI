# ✨ Stellar Support AI

A powerful, intelligent customer service chatbot powered by **Groq's Llama 3.3**, **FAISS vector storage**, **Tavily web search**, and **LangChain**, featuring a beautiful Streamlit interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.37+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-0.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

- **🤖 Advanced AI Chatbot** - Powered by Groq's Llama 3.3 70B Versatile model
- **🔍 Web Search Integration** - Real-time information retrieval using Tavily API
- **📚 Knowledge Base** - FAISS vector storage for custom knowledge injection
- **💬 Conversational Memory** - Maintains chat history for context-aware responses
- **🎨 Beautiful UI** - Modern, gradient-based Streamlit interface with typing animations
- **⚡ Lightning Fast** - Groq's LPU™ inference for ultra-fast responses

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get it here](https://console.groq.com/))
- Tavily API key ([Get it here](https://tavily.com/)) - Optional

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yashsham/Stellar-Support-AI.git
   cd Stellar-Support-AI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here  # Optional
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
Stellar-Support-AI/
├── app.py                  # Streamlit UI application
├── chatbot_backend.py      # ChatBot core logic
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Technologies Used

- **[Groq](https://groq.com/)** - Ultra-fast LLM inference with Llama 3.3 70B
- **[LangChain](https://langchain.com/)** - LLM application framework
- **[FAISS](https://github.com/facebookresearch/faiss)** - Vector similarity search
- **[Tavily](https://tavily.com/)** - AI-powered web search API
- **[Streamlit](https://streamlit.io/)** - Interactive web application framework
- **[HuggingFace](https://huggingface.co/)** - Embeddings for semantic search

## 💡 Usage

### Basic Chat

Simply type your question in the chat input and press Enter. The AI will respond based on its knowledge and the custom knowledge base.

### Web Search

To use web search for real-time information:
```python
# In the code, set use_search=True
response = bot.get_response("What's the latest news?", use_search=True)
```

### Custom Knowledge Base

Add your own knowledge to the chatbot:
```python
bot.create_knowledge_base([
    "Your custom information here",
    "Support hours: 24/7",
    "Return policy: 30 days"
])
```

## 🎨 UI Features

- **Gradient Backgrounds** - Modern, eye-catching design
- **Typing Animation** - Simulates natural conversation flow
- **Chat History** - Maintains conversation context
- **Responsive Design** - Works on desktop and mobile
- **Dark Theme** - Easy on the eyes

## 🔧 Configuration

### Model Selection

Change the LLM model in `chatbot_backend.py`:
```python
self.llm = ChatGroq(
    groq_api_key=self.groq_api_key,
    model_name="llama-3.3-70b-versatile",  # Change this
    temperature=0.7
)
```

Available Groq models:
- `llama-3.3-70b-versatile` (Recommended)
- `llama-3.1-8b-instant` (Faster, smaller)
- `mixtral-8x7b-32768` (Alternative)

### Embeddings Model

Change the embeddings model in `chatbot_backend.py`:
```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"  # Change this
)
```

## 📝 API Keys

### Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and paste into `.env`

### Tavily API Key (Optional)
1. Visit [Tavily](https://tavily.com/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Copy and paste into `.env`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing ultra-fast LLM inference
- **Meta** for the Llama 3.3 model
- **LangChain** for the excellent framework
- **Streamlit** for the amazing UI framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Groq, LangChain, and Streamlit**
