
# Mathongo AI Customer Support Agent for Edtech Platform

## AI Customer Support Agent for Edtech Platform

### 🎯 Goal
Build a working prototype of a Customer Support LLM Agent that answers student queries related to JEE (syllabus, paper pattern, exam dates, weightage topics, etc.) using a retrieval-augmented system.

### 🧩 Requirements
- Use any LLM + LangChain + FAISS/Chroma vector DB.
- Use a sample PDF/CSV knowledge base (dummy scraped data from jeemain.nta.ac.in, NCERT PDFs, etc. or provided data).
- User should be able to:
  - Ask questions like “What’s the syllabus for Complex Numbers?” or “How many attempts allowed in JEE Mains?”
  - Get answers with sources
- Agent must be modular enough to plug into a broader multi-agent CrewAI or LangGraph-based future system.

## 💡 Solution

This project uses Retrieval-Augmented Generation (RAG) with Large Language Models to answer student queries about JEE exams. The system indexes educational documents and provides accurate, source-cited answers using a vector database and modular RAG logic.

## 📄 Document Collection

The current vector store consists of documents from multiple sources:
- **JEE Main(2024) Brochure**: Split into different topics for better retrieval and source citation
- **Topic-wise Weightage and Insights**: Collected from Mathongo and other educational websites
- **JEE Previous Year Papers**: Response will include the link which has been scrapped from Mathongo using Firecrawl
- **NCERT**: Solutions to NCERT Class 11 and 12 Mathematics, Physics, and Chemistry textbooks, Response will include the link which has been scrapped from Mathongo using Firecrawl
- **Miscellaneous**: Gathered from Mathongo website and other sites using Firecrawl

All resources were curated, restructured, and combined to build a comprehensive knowledge base for the RAG, ensuring better retrieval and more accurate responses.


## 🚀 Features

- 🤖 AI-powered conversational chatb for student queries
- 📚 RAG engine for accurate information retrieval
- 🔍 Document upload, indexing, and similarity search
- 💾 Persistent chat memory and context management
- 🔄 Separate interface for knowledge base management
- 🎨 user-friendly UI (Streamlit)
- 🌐 Multilingual support for diverse student needs
- 🧩 Modular design

## 🛠️ Technology Stack

- **Backend**: Python 3.11+
- **UI Framework**: Streamlit
- **LLM Integration**: OpenAI GPT-4o-mini
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI text-embedding-3-small
- **Document Processing**: LangChain, PyMuPDF
- **Memory Management**: Custom conversation buffer
- **Logging**: Structured logging

## 📁 Project Structure

```
Mathongo_AI_Customer_Support/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .env.example                    # Environment variables template
├── config/                         # Configuration settings
│   ├── __init__.py
│   └── settings.py
├── core/                           # Core RAG functionality
│   ├── __init__.py
│   ├── memory_manager.py           # Conversation memory management
│   ├── rag_engine.py               # Main RAG orchestration
│   ├── vector_operations.py        # Vector database operations
│   └── vector_store.py             # Vector store implementation
├── models/                         # AI model integrations
│   ├── __init__.py
│   ├── embeddings.py               # Embedding models
│   └── llm_models.py               # Language model implementations
│   └── pydantic_models.py         # Pydantic data models
├── services/                       # Business logic services
│   ├── __init__.py
│   └── chat_service.py             # Chat orchestration service
├── ui/                             # User interface components
│   ├── __init__.py
│   ├── components/                 # Reusable UI components
│   │   ├── chat_interface.py
│   │   └── sidebar.py
│   ├── pages/                      # Application pages
│   │   ├── chatbot.py
│   │   └── vector_operations.py
│   └── styles/                     # UI styling
│       ├── sidebar.py
│       └── vectordb_page.py
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── helpers.py                  # General helper functions
│   └── logger.py                   # Logging configuration
├── data/                           # Data storage
│   ├── chat_history.json           # Persistent chat history
│   └── chroma_db/                  # Vector database files
├── assets/                         # Project images and screenshots
├── Docs/                          # Reference documents and PDFs
└── logs/                           # Application logs
    └── rag_chatbot.log
```


## 🏗️ Project Architecture and Process flow

### Core Architecture and Process Flow
<p align="center">
  <img src="assets\Project architecture and flow.jpg" alt="Main Chat Interface" width="600"/>
</p>

### Vector Database architecture
<p align="center">
  <img src="assets\vector_db architecture.jpg" alt="Main Chat Interface" width="600"/>
</p>


## 📸 Screenshots & Demos

### Main Chat Interface
<p align="center">
  <img src="assets\Chat_Interface.png" alt="Main Chat Interface" width="600"/>
</p>

### Vector Operations Dashboard
<p align="center">
  <img src="assets\Add_Docs.png" alt="Vector Operations Dashboard" width="600"/>

</p>

### Document Upload section
<p align="center">
  <img src="assets\doc_add.png" alt="Document Upload Process" width="500"/>
</p>

### Document list
<p align="center">
  <img src="assets\Doc list.png" alt="Document Upload Process" width="500"/>
  <img src="assets\Documents list.png" alt="Document Upload Process" width="500"/>
</p>

## 🧪 Testing

1. Test basic chat functionality with follow up question
<p align="center">
  <img src="assets\syllabus_1.png" alt="Sample Query Response" width="600"/>
  <img src="assets\syllabus_2.png" alt="Sample Query Response" width="600"/>
</p>

2. Eligibility 
<p align="center">
  <img src="assets\eligibility.png" alt="Sample Query Response" width="600"/>
</p>

3. Feedback and feedback check
<p align="center">
  <img src="assets\feedback.png" alt="Sample Query Response" width="600"/>
  <img src="assets\Feedback check.png" alt="Sample Query Response" width="600"/>
</p>

4. Answers involving links
<p align="center">
  <img src="assets\Previous_year_paper.png" alt="Sample Query Response" width="600"/>
  <img src="assets\pyq_follow up.png" alt="Sample Query Response" width="600"/>
</p>

5. Multilingual queries
<p align="center">
  <img src="assets\Multilingual_1.png" alt="Sample Query Response" width="600"/>
  <img src="assets\Multilingual_2.png" alt="Sample Query Response" width="600"/>
  <img src="assets\Multilingual_3.png" alt="Sample Query Response" width="600"/>
</p>

6. Out of context queries handling
<p align="center">
  <img src="assets\out of context.png" alt="Sample Query Response" width="600"/>
</p>


7. Miscellaneous queries
<p align="center">
  <img src="assets\Important topic_maths.png" alt="Sample Query Response" width="600"/>
  <img src="assets\Important_topic2.png" alt="Sample Query Response" width="600"/>
  <img src="assets\Important topic_3.png" alt="Sample Query Response" width="600"/>
  <img src="assets\Cities.png" alt="Sample Query Response" width="600"/>
</p>

10. Logs
<p align="center">
  <img src="assets\logs.png" alt="Sample Query Response" width="600"/>

</p>

11. Query reformatting proof using LangSmith
<p align="center">
  <img src="assets\query reformatting.png" alt="Sample Query Response" width="600"/>
  <img src="assets\query refomratting_2.png" alt="Sample Query Response" width="600"/>
</p>

12. Hindi Query reformatting proof using LangSmith
<p align="center">
  <img src="assets\hindi_query_refor.png" alt="Sample Query Response" width="600"/>
  <img src="assets\hindi_query_reform_2.png" alt="Sample Query Response" width="600"/>
</p>

13. Langsmith simulation stats
<p align="center">
  <img src="assets\Langsmith_simulation.png" alt="Sample Query Response" width="400" height="450"/>
</p>


## 🔧 Installation & Setup

### Prerequisites
- Python 3.11
- pip package manager
- Git (for cloning the repository)

### Step 1: Create Python Virtual Environment

#### Option A: Using Python venv (Standard)
```bash
# Create virtual environment with Python 3.11
python -m venv mathongo_env

# Activate the virtual environment
# On Windows:
mathongo_env\Scripts\activate
# On macOS/Linux:
source mathongo_env/bin/activate
```

#### Option B: Using Anaconda/Miniconda
```bash
# Create conda environment with Python 3.11
conda create -n mathongo_env python=3.11 -y

# Activate the conda environment
conda activate mathongo_env
```

### Step 2: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 3: Environment Configuration
1. Create a `.env` file in the project root directory
2. Add your API keys and configuration:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Step 4: Configure LLM Provider
- Ensure `OPENAI_API_KEY` is set in your `.env` file
- The application will automatically use the configured OpenAI model

## 🤖 LLM Provider Configuration

### OpenAI Models
- **Models**: GPT-4o-mini
- **Pros**: High quality, reliable, well-documented
- **Setup**: Requires OpenAI API key

### Configuration
1. **Update Environment Variables**:
   ```env
   # For OpenAI
   OPENAI_API_KEY=your_openai_key_here
   ```
2. **Restart the Application** for changes to take effect.

### Model Recommendations
- **For Production**: OpenAI GPT-4o-mini (balanced performance and cost)
- **For High Quality Responses**: OpenAI GPT-4o (best quality, higher cost)

### Step 5: Initialize the Application
```bash
# Run the Streamlit application
streamlit run app.py
```
The application will be available at `http://localhost:8501`

## 🚀 Usage Guide

### For Students
1. **Access the Chatbot**: Open the application and navigate to the chat interface
2. **Ask Questions**: Type queries about JEE syllabus, exam pattern, dates, or topics
3. **Review Responses**: Get answers with source citations


### For Administrators
1. **Document Management**: Use the Vector Operations page to upload/update knowledge base documents
2. **Monitor System**: Check logs and performance metrics
3. **Configuration Updates**: Modify settings in the config files as needed

## 🔮 Future Plans

- LangGraph-based multi-agent orchestration
- FastAPI backend for scalable deployment
- Full-fledged web interface (React.js frontend)
- Voice interface (speech-to-text/text-to-speech)
- Mobile application for students

---

**Build for Mathongo** - Empowering students with AI-powered support for JEE and beyond.
