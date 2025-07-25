"""
Simplified Chat interface components for single chat interface
"""
import streamlit as st
from datetime import datetime
from core.rag_engine import rag_engine
from core.memory_manager import memory_manager
from services.chat_service import chat_service
from utils.logger import get_logger

logger = get_logger(__name__)

def _render_empty_chat_placeholder():
    """Render placeholder for empty chats."""
    st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <h3>📝 No messages yet</h3>
            <p>Start a conversation to see messages here</p>
        </div>
        """, unsafe_allow_html=True)

def render_chat_messages():
    """Render chat messages directly from the session state."""
    # Chat messages are managed entirely within st.session_state
    # for the duration of the user's session.
    messages = st.session_state.get('chat_messages', [])

    if messages:
        for message in messages:
            # Skip rendering system messages
            if message["role"] == "system":
                continue

            role = message["role"]
            content = message["content"]
            
            # Choose avatar based on role
            if role == "user":
                avatar = "👤"
                display_role = "user"
            elif role == "assistant":
                avatar = "🏛️"
                display_role = "assistant"
            else:
                avatar = "🤖"
                display_role = role

            with st.chat_message(display_role, avatar=avatar):
                st.write(content)
                # Show feedback buttons for assistant responses
                if role == "assistant":
                    col1, col2, col3 = st.columns([0.85, 0.07, 0.07])
                    with col2:
                        if st.button("👍", key=f"thumbs_up_{id(message)}", help="Thumbs up", use_container_width=True):
                            _save_feedback(message, "up")
                    with col3:
                        if st.button("👎", key=f"thumbs_down_{id(message)}", help="Thumbs down", use_container_width=True):
                            _save_feedback(message, "down")
    else:
        _render_empty_chat_placeholder()

def _save_feedback(message, feedback):
    """Save feedback for a specific assistant message in chat_history.json."""
    import json
    from services.chat_service import chat_service
    chat_id = st.session_state.get("chat_id")
    if not chat_id:
        st.error("No chat ID found.")
        return
    # Load all chats
    chat_file = chat_service.chat_file
    try:
        with open(chat_file, "r", encoding="utf-8") as f:
            all_chats = json.load(f)
        messages = all_chats.get(chat_id, {}).get("messages", [])
        # Find the matching assistant message by content and role
        for msg in messages:
            if msg["role"] == "assistant" and msg["content"] == message["content"]:
                msg["feedback"] = feedback
        # Write back to file
        with open(chat_file, "w", encoding="utf-8") as f:
            json.dump(all_chats, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error saving feedback: {e}")

def _handle_user_query(user_query):
    """Process user query, save messages with chat_id, and display response."""
    try:
        # Get the current chat ID from the session state.
        chat_id = st.session_state.chat_id
        
        # Save user message to the JSON file under the current chat_id.
        if not chat_service.save_message(chat_id, "user", user_query):
            st.error("Failed to save your message. Please try again.")
            return

        # Append user message to the session state for immediate display.
        user_message = {"role": "user", "content": user_query}
        st.session_state.chat_messages.append(user_message)

        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.write(user_query)

        # Process and display assistant response
        with st.chat_message("assistant", avatar="🏛️"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Get the response generator from the RAG engine
            response_generator = rag_engine.process_query(user_query)
            
            # Use the spinner only to wait for the first chunk of the response
            with st.spinner("🤔 Thinking..."):
                try:
                    # This blocks until the first chunk is received, then the spinner disappears
                    first_chunk = next(response_generator)
                    full_response += first_chunk
                    response_placeholder.markdown(full_response + "▌")
                except StopIteration:
                    # This happens if the RAG engine returns an empty response
                    logger.warning("RAG engine returned an empty response.")
                    full_response = "I don't have enough information to answer that. Please try rephrasing your question."
                    response_placeholder.markdown(full_response)
                    # Set the generator to an empty list so the next loop doesn't run
                    response_generator = []
                except Exception as e:
                    logger.error(f"RAG processing error on first chunk: {e}")
                    full_response = "I apologize, but I encountered an error while processing your question. Please try again."
                    response_placeholder.markdown(full_response)
                    # Set the generator to an empty list so the next loop doesn't run
                    response_generator = []
            
            # The spinner is gone now. Stream the rest of the response.
            for chunk in response_generator:
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            
            # Final render without the cursor
            response_placeholder.markdown(full_response)

            # Save assistant response to the JSON file under the current chat_id.
            if full_response and chat_service.save_message(chat_id, "assistant", full_response):
                assistant_message = {"role": "assistant", "content": full_response}
                st.session_state.chat_messages.append(assistant_message)
                logger.info("Saved assistant response to session and file.")
            else:
                logger.error("Failed to save assistant response or response was empty.")

        # Trigger re-render to ensure UI is in sync
        st.rerun()

    except Exception as e:
        logger.error(f"Error handling user query: {e}")
        st.error("⚠️ An error occurred while processing your query. Please try again.")

def render_chat_input():
    """Render chat input box and handle submission."""
    user_query = st.chat_input("💬 Ask your question about BSK services...")

    if user_query:
        _handle_user_query(user_query)