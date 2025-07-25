"""
Language model configurations
"""
from langchain_openai import ChatOpenAI
from config.settings import MODEL_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

def get_chat_model():
    """
    Returns an instance of the main chat model specified in MODEL_CONFIG.
    """
    try:
        model = ChatOpenAI(
            model=MODEL_CONFIG["chat_model"],
            temperature=MODEL_CONFIG["temperature"],
            streaming=MODEL_CONFIG["streaming"]
        )
        logger.info("Chat model initialized successfully.")
        return model
    except Exception as e:
        logger.error(f"Failed to initialize chat model: {e}")
        raise

