"""
BSK Assistant - Main Application Entry Point
"""
import streamlit as st
from ui.pages.chatbot import show_chatbot_page
from ui.pages.vector_operations import show_vector_operations_page
from config.settings import PAGE_CONFIG
from utils.logger import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Configure page settings
st.set_page_config(**PAGE_CONFIG)

def main():
    """
    Main application entry point for BSK Assistant.
    Initializes session state, determines current page, and routes to the appropriate page.
    """
    logger.debug("Entered main() function.")
    if "current_page" not in st.session_state:
        st.session_state.current_page = "chat"
        logger.info("Initialized session state with default page: chat")
    current_page = st.session_state.get("current_page", "chat")
    logger.debug(f"Current page: {current_page}")
    if current_page == "chat":
        logger.info("Rendering Chatbot page.")
        show_chatbot_page()
    elif current_page == "vector_ops":
        logger.info("Rendering Vector Operations page.")
        show_vector_operations_page()
    else:
        logger.warning(f"Unknown page: {current_page}, defaulting to chat")
        st.session_state.current_page = "chat"
        logger.info("Rendering Chatbot page due to unknown page.")
        show_chatbot_page()
    logger.debug("Exiting main() function.")

if __name__ == "__main__":
    logger.info("Application started.")
    main()