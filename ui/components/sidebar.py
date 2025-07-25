"""
Simplified Sidebar components for single chat interface
"""
import streamlit as st
from services.chat_service import chat_service
from core.memory_manager import memory_manager
from utils.logger import get_logger
from ui.styles.sidebar import apply_sidebar_styles

logger = get_logger(__name__)

def render_sidebar():
    """Render the simplified sidebar."""
    # Apply sidebar styles
    apply_sidebar_styles()
    
    with st.sidebar:
        # Dynamic Title based on problem statement
        st.markdown("""
        <div class="sidebar-header">
            JEE ASSISTANT
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Section
        _render_navigation_section()
        
        st.markdown("---")
        
        # Clean Chat Section (only show in chat mode)
        if st.session_state.get('current_page', 'chat') == 'chat':
            _render_clean_chat_section()
        
        st.markdown("---")
        
        # About section
        _render_about_section()



def _render_navigation_section():
    """Render navigation section."""
    st.subheader("🧭 Navigation")
    
    current_page = st.session_state.get('current_page', 'chat')
    
    # Chat Page Button
    if st.button("💬 Chat Assistant", use_container_width=True, disabled=(current_page == 'chat')):
        st.session_state.current_page = 'chat'
        st.rerun()
    
    # Vector Operations Button
    if st.button("🗄️ Vector Database", use_container_width=True, disabled=(current_page == 'vector_ops')):
        st.session_state.current_page = 'vector_ops'
        st.rerun()

def _render_clean_chat_section():
    """Render section with a button to start a new, clean chat session."""
    st.subheader("🧹 New Chat")
    
    # Warning message
    st.warning("⚠️ This will start a new chat session. Your current conversation will be archived.")
    
    if st.button("✨ Start New Chat", use_container_width=True, type="primary"):
        try:
            # 1. Reset conversation memory for a fresh start.
            memory_manager.reset_memory()
            
            # 2. Create a new chat ID via the chat service.
            new_chat_id = chat_service.create_new_chat()
            
            # 3. Update the session state to reflect the new, empty chat.
            st.session_state.chat_id = new_chat_id
            st.session_state.chat_messages = []
            
            logger.info(f"Successfully started a new chat session with ID: {new_chat_id}")
            st.success("✅ New chat started!")
            
            # Rerun to refresh the interface to the clean state.
            st.rerun()
        except Exception as e:
            logger.error(f"Error starting new chat: {e}")
            st.error("❌ An error occurred while starting a new chat.")

def _render_about_section():
    """Render about section."""
    with st.expander("📋 About This Project", expanded=False):
        st.markdown("""
        An intelligent AI customer support agent for JEE-related queries, built with LangChain and vector retrieval technology.
        
        **What it does:**
        - Answers JEE syllabus, exam pattern, and preparation questions
        - Provides source-backed responses from official NTA documents
        - Handles natural language queries like "What's the syllabus for Complex Numbers?"

        **Tech Stack:**
        - **LLM**: GPT for intelligent responses
        - **Framework**: LangChain for orchestration
        - **Vector DB**: Chroma for semantic search
        - **Knowledge Base**: JEE official docs, NCERT materials

        **Key Features:**
        - Retrieval-augmented generation (RAG)
        - Source attribution for every answer
        - Modular design for multi-agent integration
        - Ready for CrewAI/LangGraph expansion
        - Unique chat sessions with persistent IDs

        Built as a prototype demonstrating modern AI techniques for educational support systems.
        """)