"""
Embedding models configuration
"""
from langchain_openai import OpenAIEmbeddings
from config.settings import MODEL_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

def get_embeddings():
    """
    Returns an instance of the OpenAI embedding model specified in MODEL_CONFIG.
    """
    try:
        embeddings = OpenAIEmbeddings(model=MODEL_CONFIG["embedding_model"])
        logger.info("Embeddings model initialized successfully.")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embeddings: {e}")
        raise