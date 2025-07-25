"""
Simplified Chat service for single chat interface
"""
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from config.settings import CHAT_HISTORY_FILE
from utils.logger import get_logger

logger = get_logger(__name__)

class SimplifiedChatService:
    """Service to manage chat history with unique IDs for each session."""
    
    def __init__(self):
        self.chat_file = CHAT_HISTORY_FILE
        self.current_chat_id: Optional[str] = None
        self._ensure_data_directory()
        self._initialize_chat_file()
    
    def _ensure_data_directory(self):
        """Ensure the data directory for the chat history file exists."""
        data_dir = os.path.dirname(self.chat_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"Created data directory: {data_dir}")
    
    def _initialize_chat_file(self):
        """Ensure the chat history file exists and is a valid JSON dictionary."""
        try:
            if not os.path.exists(self.chat_file):
                self._create_empty_chat_file()
            else:
                with open(self.chat_file, 'r', encoding='utf-8') as f:
                    # Check if file is empty or not a dictionary
                    content = f.read()
                    if not content or not isinstance(json.loads(content), dict):
                        logger.warning("Chat history file is empty or malformed. Re-initializing.")
                        self._create_empty_chat_file()
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Error initializing chat file: {e}. Recreating it.")
            self._create_empty_chat_file()

    def _create_empty_chat_file(self):
        """Create an empty JSON object in the chat history file."""
        try:
            with open(self.chat_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            logger.info(f"Created empty chat file at: {self.chat_file}")
        except Exception as e:
            logger.error(f"Error creating empty chat file: {e}")
    
    def load_chat_messages(self, chat_id: str) -> List[Dict[str, Any]]:
        """Load messages for a specific chat ID."""
        try:
            with open(self.chat_file, 'r', encoding='utf-8') as f:
                all_chats = json.load(f)
            return all_chats.get(chat_id, {}).get("messages", [])
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error loading messages for chat {chat_id}: {e}")
            return []

    def save_message(self, chat_id: str, role: str, content: str) -> bool:
        """Save a message to a specific chat session identified by chat_id."""
        if not chat_id:
            logger.error("Cannot save message with empty chat_id.")
            return False
        try:
            with open(self.chat_file, 'r+', encoding='utf-8') as f:
                all_chats = json.load(f)
                
                # Create chat session if it doesn't exist
                if chat_id not in all_chats:
                    all_chats[chat_id] = {
                        "created_at": datetime.now().isoformat(),
                        "messages": []
                    }

                # Append new message
                message = {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }
                all_chats[chat_id]["messages"].append(message)
                
                # Write back to file
                f.seek(0)
                f.truncate()
                json.dump(all_chats, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Saved {role} message to chat {chat_id}")
            return True
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error saving message to chat {chat_id}: {e}")
            return False
    
    def create_new_chat(self) -> str:
        """Create a new chat session, assign a new UUID, and set it as current."""
        self.current_chat_id = str(uuid.uuid4())
        logger.info(f"New chat session created with ID: {self.current_chat_id}")
        # Ensure the new chat is initialized in the file right away
        self.save_message(self.current_chat_id, "system", "Chat session started.")
        return self.current_chat_id

    def get_current_chat_id(self) -> Optional[str]:
        """Get the ID of the current active chat session."""
        return self.current_chat_id


# Global simplified chat service instance
chat_service = SimplifiedChatService()