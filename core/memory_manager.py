"""
Simplified Memory management for single chat interface
"""
from langchain.memory import ConversationBufferWindowMemory
from config.settings import MEMORY_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

class SimplifiedMemoryManager:
    """Simplified memory manager for single chat interface."""
    
    def __init__(self):
        self.memory = ConversationBufferWindowMemory(
            k=MEMORY_CONFIG.get("window_size", 10),
            return_messages=MEMORY_CONFIG.get("return_messages", True)
        )
        logger.info("Simplified Memory Manager initialized.")
    
    def get_memory(self) -> ConversationBufferWindowMemory:
        """
        Returns the current ConversationBufferWindowMemory instance.
        """
        return self.memory
    
    def save_context(self, input_data: dict, output_data: dict) -> bool:
        """
        Saves the conversation context to memory.
        Returns True if successful, False otherwise.
        """
        try:
            self.memory.save_context(input_data, output_data)
            logger.info("Context saved to memory")
            return True
        except Exception as e:
            logger.error(f"Error saving context to memory: {e}")
            return False
    
    def load_memory_variables(self) -> dict:
        """
        Loads and returns memory variables from the current memory instance.
        Returns a dictionary of memory variables.
        """
        try:
            memory_vars = self.memory.load_memory_variables({})
            logger.debug("Loaded memory variables")
            return memory_vars
        except Exception as e:
            logger.error(f"Error loading memory variables: {e}")
            return {"history": []}
    
    def reset_memory(self) -> bool:
        """
        Resets the memory, clearing all conversation history.
        Returns True if successful, False otherwise.
        """
        try:
            self.memory.clear()
            logger.info("Memory reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting memory: {e}")
            return False

# Global simplified memory manager instance
memory_manager = SimplifiedMemoryManager()