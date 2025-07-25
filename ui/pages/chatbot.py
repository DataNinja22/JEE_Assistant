"""
Simplified chatbot page for single chat interface
"""
import streamlit as st
from ui.components.sidebar import render_sidebar
from ui.components.chat_interface import render_chat_messages, render_chat_input
from services.chat_service import chat_service
from core.memory_manager import memory_manager
from utils.logger import get_logger

logger = get_logger(__name__)

def _initialize_session_state():
    """
    Initializes a fresh chat session on first run.
    This ensures the user gets a clean slate every time they open the app.
    """
    if "session_initialized" not in st.session_state:
        logger.info("New app session started. Initializing a fresh chat state.")

        # 1. Reset the conversation memory to ensure no carry-over from past runs.
        memory_manager.reset_memory()

        # 2. Create a new, unique chat ID for this session.
        new_chat_id = chat_service.create_new_chat()
        st.session_state.chat_id = new_chat_id

        # 3. Initialize the message list as empty for the new chat.
        st.session_state.chat_messages = []

        # 4. Set a flag to prevent this block from running again during this session.
        st.session_state.session_initialized = True
        
        logger.info(f"Initialized fresh chat session with ID: {st.session_state.chat_id}")

def show_chatbot_page():
    """Main chatbot page with simplified interface."""
    
    # Initialize a fresh session state on first load
    _initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    
    # Add a divider
    st.markdown("---")
    
    # Render main chat interface
    render_chat_messages()
    render_chat_input()
    