import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

class ChatBot:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.7
        )
        
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None
        self.chat_history = []
        self.search_tool = self._setup_search_tool()

    def _setup_search_tool(self):
        """Setup Tavily search tool if API key is available"""
        if self.tavily_api_key:
            return TavilySearchResults(api_key=self.tavily_api_key, max_results=3)
        return None

    def create_knowledge_base(self, texts: list[str]):
        """
        Creates a FAISS vector store from a list of texts.
        Useful for rule-based or specific knowledge injection.
        """
        if not texts:
            return
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = [Document(page_content=t) for t in texts]
        splits = text_splitter.split_documents(docs)
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(splits, self.embeddings)
        else:
            self.vector_store.add_documents(splits)

    def get_response(self, query: str, use_search: bool = False):
        """
        Generates a response using the LLM with optional context from knowledge base and search.
        
        Args:
            query: User's question
            use_search: Whether to use web search for additional context
        """
        context_parts = []
        
        # Get context from knowledge base if available
        if self.vector_store:
            docs = self.vector_store.similarity_search(query, k=2)
            if docs:
                kb_context = "\n".join([d.page_content for d in docs])
                context_parts.append(f"Knowledge Base Context:\n{kb_context}")
        
        # Get context from web search if requested and available
        if use_search and self.search_tool:
            try:
                search_results = self.search_tool.invoke({"query": query})
                if search_results:
                    search_context = "\n".join([f"- {result.get('content', '')[:200]}" for result in search_results if isinstance(result, dict)])
                    if search_context:
                        context_parts.append(f"Web Search Results:\n{search_context}")
            except Exception as e:
                print(f"Search error: {e}")
        
        # Build the prompt
        messages = [
            SystemMessage(content="You are a helpful customer service assistant. Use the provided context to answer questions accurately. If you don't know something, say so.")
        ]
        
        # Add chat history (keep last 10 messages)
        messages.extend(self.chat_history[-10:])
        
        # Add context and query
        if context_parts:
            context_message = "\n\n".join(context_parts)
            messages.append(HumanMessage(content=f"Context:\n{context_message}\n\nQuestion: {query}"))
        else:
            messages.append(HumanMessage(content=query))
        
        try:
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            # Update chat history
            self.chat_history.append(HumanMessage(content=query))
            self.chat_history.append(AIMessage(content=response.content))
            
            return response.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Simple usage example
if __name__ == "__main__":
    bot = ChatBot()
    # Example of adding some rules/knowledge
    bot.create_knowledge_base([
        "Return policy: Items can be returned within 30 days of purchase.",
        "Support hours: Mon-Fri 9am-5pm EST.",
        "Shipping: Free shipping on orders over $50."
    ])
    
    print("Bot initialized. Type 'quit' to exit.")
    print("Type 'search: <query>' to use web search.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        # Check if user wants to use search
        use_search = user_input.lower().startswith('search:')
        if use_search:
            user_input = user_input[7:].strip()
        
        response = bot.get_response(user_input, use_search=use_search)
        print(f"Bot: {response}\n")
