from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from models.llm_models import get_chat_model
from core.vector_store import vector_store_manager
from core.memory_manager import memory_manager
from config.settings import SYSTEM_PROMPT, VECTOR_STORE_CONFIG
from utils.logger import get_logger
from typing import List, Any
from models.pydantic_models import StandaloneQuery

logger = get_logger(__name__)

class SimplifiedRAGEngine:
    """Simplified RAG engine for single chat interface."""
    
    def __init__(self):
        self.llm_model = get_chat_model()
        self.prompt_template = self._create_prompt_template()
        self.chain = None
        self.retrieval_config = VECTOR_STORE_CONFIG
        self._initialize_chain()
    
    def _create_prompt_template(self):
        """Create prompt template."""
        return ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "use this information to answer queries: \n{context}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "Current question: {input} \n "
             "Language in which response should be: {language}"),
        ])
    
    def _get_context(self, documents: List, query: str) -> str:
        """Get context from retrieved documents."""
        try:
            if not documents:
                logger.info(f"No documents retrieved for query: {query}")
                return "No specific BSK service information found for this query. Please try rephrasing your question or ask about available BSK services."

            logger.info(f"Processing {len(documents)} retrieved documents")

            context_parts = []
            for doc in documents:
                filename = getattr(doc, 'metadata', {}).get('filename', 'Unknown Document')
                formatted_content = f"Source: {filename}\n{doc.page_content}"
                context_parts.append(formatted_content)

            return "\n\n".join(context_parts) if context_parts else "No BSK service information found."

        except Exception as e:
            logger.error(f"Error in context retrieval: {e}")
            return "Error retrieving context. Please try again."
    
    def _initialize_chain(self):
        """Initialize the RAG chain."""
        try:
            self.chain = self._create_rag_chain()
            if self.chain:
                logger.info("RAG chain initialized successfully")
            else:
                logger.warning("Failed to initialize RAG chain")
        except Exception as e:
            logger.error(f"Error during chain initialization: {e}")
            self.chain = None
    
    def _create_rag_chain(self):
        """Create RAG chain."""
        try:
            # Check vector store availability
            if not vector_store_manager.is_available():
                logger.warning("Vector store unavailable. Attempting to reinitialize...")
                if not vector_store_manager.reinitialize_vector_store():
                    logger.error("Vector store still unavailable after reinitialization.")
                    return None
            
            # Get retriever
            retriever = vector_store_manager.get_retriever()
            if not retriever:
                logger.error("Failed to create retriever.")
                return None
            
            # Create reformulation chain
            reformulation_chain = self.llm_model.with_structured_output(StandaloneQuery)
            
            # Enhanced chain
            def get_context_and_history(x):
                """Get context and history for the query."""
                query = x["input"]
                
                # Load history from memory
                memory_vars = memory_manager.load_memory_variables()
                history = memory_vars.get("history", [])
                
                # Use only the last two messages from history if available
                if len(history) >= 2:
                    last_pair = history[-2:]
                    history_str = "\n".join([f"{msg.type}: {msg.content}" for msg in last_pair])
                else:
                    history_str = ""
                
                # Reformulate query
                reformulation_input = f"Conversation history:\n{history_str}\n\nCurrent query: {query}"
                standalone_query_obj = reformulation_chain.invoke(reformulation_input)
                standalone_query = standalone_query_obj.query
                
                # Retrieve documents
                try:
                    documents = retriever.invoke(standalone_query)
                    context = self._get_context(documents, standalone_query)
                except Exception as e:
                    logger.error(f"Error retrieving documents: {e}")
                    context = "Error retrieving documents. Please try again."
                
                return {
                    "context": context,
                    "history": history,
                    "input": standalone_query,
                    "language": standalone_query_obj.language
                }
            
            # Create the chain
            chain = (
                RunnablePassthrough() 
                | get_context_and_history
                | self.prompt_template
                | self.llm_model
                | StrOutputParser()
            )
            
            logger.info("RAG chain created successfully.")
            return chain
            
        except Exception as e:
            logger.error(f"Failed to create RAG chain: {e}")
            return None
    
    
    def _ensure_chain_availability(self) -> bool:
        """Ensure the RAG chain is available."""
        if not self.chain:
            logger.info("Chain not available. Attempting to recreate...")
            self._initialize_chain()
        
        if not self.chain:
            logger.error("Failed to create or recreate chain")
            return False
        
        return True
    
    def process_query(self, query: str) -> Any:
        """Process query with simplified interface."""
        
        # Ensure chain availability
        if not self._ensure_chain_availability():
            error_msg = "RAG system is currently unavailable. Please ensure documents are loaded and try again."
            logger.error(error_msg)
            yield error_msg
            return
        
        # Process query
        try:
            full_response = ""
            chunk_count = 0

            chain_input = {"input": query}
            for chunk in self.chain.stream(chain_input):
                if chunk:
                    full_response += chunk
                    chunk_count += 1
                    yield chunk

            logger.info(f"Query processed successfully ")

            # Save context to memory
            if full_response.strip():
                save_success = memory_manager.save_context(
                    {"input": query},
                    {"output": full_response}
                )
                
                if save_success:
                    logger.info("Context saved to memory")
                else:
                    logger.warning("Failed to save context to memory")
            else:
                logger.warning("Empty response generated, not saving to memory")
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            logger.error(error_msg)

# Global simplified RAG engine instance
rag_engine = SimplifiedRAGEngine()