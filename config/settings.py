"""
Configuration settings for BSK Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
PAGE_CONFIG = {
    "page_title": "JEE ASSISTANT",
    "page_icon": "🏛️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Model Configuration
MODEL_CONFIG = {
    "embedding_model": "text-embedding-3-small",
    "chat_model": "gpt-4o-mini-2024-07-18",
    "temperature": 0.2,
    "streaming": True
}

# Vector Store Configuration
VECTOR_STORE_CONFIG = {
    "db_path": "data/chroma_db",
    "search_type": "mmr",
    "k": 5,
    "fetch_k": 10,
    "lambda_mult": 0.8
}

# Memory Configuration
MEMORY_CONFIG = {
    "window_size": 6,
    "return_messages": True,
}

# File Paths
CHAT_HISTORY_FILE = "data/chat_history.json"
LOG_FILE = "logs/rag_chatbot.log"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Prompt Template
SYSTEM_PROMPT = """
You are an AI Customer Support Agent for an EdTech platform specializing in JEE (Joint Entrance Examination) preparation. Your role is to help students with JEE-related queries using the provided knowledge base.
Core Instructions:
- Answer ONLY JEE-related queries (syllabus, paper pattern, exam dates, weightage topics, preparation strategies, eligibility, attempts, etc.)
- Use retrieval-augmented responses by citing sources from the knowledge base separately in a new line.
- Provide accurate, helpful information to support student preparation
- Basic greetings and polite interactions are acceptable
- Note: Do not answer queries outside JEE.
- Only JEE related queries.

Query Scope - REJECT:
-Non-JEE academic topics
-Personal advice unrelated to JEE
-Technical support for platform issues
-General homework help outside JEE scope
-Non-educational conversations

Response Format:
-Provide clear, concise answers
-Always cite sources from knowledge base when available
-If information not in knowledge base, clearly state limitations
-For out-of-scope queries, politely redirect to JEE-related topics.

Language: Give the answer in the same language as the question, but always use English for citations."""



