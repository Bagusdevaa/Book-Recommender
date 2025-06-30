# 📚 AI-Powered Book Recommender System

> A sophisticated book recommendation system that combines **semantic search**, **emotion analysis**, and **AI embeddings** to deliver personalized book suggestions based on user preferences and emotional tone.

## Features
### **AI-Powered Recommendations**
- **Semantic Search**: Uses OpenAI embeddings for intelligent content understanding
- **Emotion-Based Filtering**: Recommends books based on desired emotional tone (Happy, Sad, Suspenseful, etc.)
- **Multi-Modal Search**: Supports natural language queries like "adventurous fantasy with strong characters"

### **Smart Filtering System**
- **Category Filtering**: Fiction, Non-fiction, Children's books
- **Tone Selection**: Happy, Surprising, Angry, Suspenseful, Sad
- **Flexible Limits**: Customizable result count (8-32 books)

### **Advanced Search**
- **Real-time Search**: Instant book search with autocomplete
- **Hybrid Approach**: Combines keyword matching with semantic understanding
- **Rich Metadata**: Displays ratings, categories, descriptions, and cover images


## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API Key

### 1. Clone Repository
```bash
git clone https://github.com/Bagusdevaa/Book-Recommender.git
cd book-recommender
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`


### Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Embeddings** | OpenAI text-embedding-ada-002 | Semantic understanding |
| **Vector Database** | ChromaDB + LangChain | Similarity search |
| **Emotions Classification** | Hunggingface j-hartmann/emotion-english-distilroberta-base | Tones filtering |
| **Categories Classification** | Hunggingface facebook/bart-large-mnli | Categories filtering |
| **Data Processing** | Pandas + NumPy | Data manipulation |
| **Backend** | FastAPI + Uvicorn | REST API |
| **Frontend** | React + Vite | Modern UI development |
| **Styling** | Tailwind CSS | Responsive design |

## Dataset & Features

### Book Dataset
- **Size**: 7,000 books with rich metadata
- **Sources**: [Kaggle - 7k Books](https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata/data)

### Emotion Analysis
Each book analyzed across 5 emotional dimensions:
- **Joy** (0.0-1.0): Happiness, hope, uplift
- **Sadness** (0.0-1.0): Melancholy, tragedy, loss  
- **Fear** (0.0-1.0): Suspense, tension, thriller elements
- **Anger** (0.0-1.0): Conflict, rage, social issues
- **Surprise** (0.0-1.0): Plot twists, unexpected elements

### Vector Embeddings
- **Model**: OpenAI text-embedding-ada-002
- **Storage**: ChromaDB for efficient similarity search
- **Persistence**: Local vector database for cost optimization


## Acknowledgments

- **OpenAI** for powerful embedding models
- **LangChain** for seamless AI integration  
- **FastAPI** for excellent async API framework
- **React & Tailwind** for modern frontend development
- **Book data sources**: Google Books API, Open Library


## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Guide](https://docs.langchain.com/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [React Best Practices](https://react.dev/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.