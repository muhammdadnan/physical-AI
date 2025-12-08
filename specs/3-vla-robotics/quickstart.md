# Quickstart Guide: Physical AI & Humanoid Robotics — Book + Integrated RAG Chatbot

## Phase 1: Quickstart Guide

### Prerequisites

- Node.js 18+ (for Docusaurus)
- Python 3.10+ (for FastAPI backend)
- Git
- Access to OpenAI API
- Access to Qdrant Cloud (Free Tier)
- Access to Neon Serverless PostgreSQL

### Setup Instructions

#### 1. Clone and Initialize Repository

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

#### 2. Environment Configuration

Create `.env` files for both frontend and backend:

**Backend (.env)**:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key
```

**Frontend (.env)**:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_OPENAI_API_KEY=your_openai_api_key
```

#### 3. Database Setup

```bash
# Set up Neon PostgreSQL database
# Create the required tables based on data model
psql $DATABASE_URL < backend/sql/schema.sql
```

#### 4. Run Development Servers

**Backend (RAG API)**:
```bash
cd backend
uvicorn src.api.main:app --reload --port 8000
```

**Frontend (Docusaurus Book)**:
```bash
cd frontend
npm run start
```

### Key Components

#### 1. Book Structure (Docusaurus)

- `/docs` - Contains MDX files for each module/chapter
- `/static` - Static assets (images, diagrams)
- `/src/components` - Custom React components including chatbot
- `/src/pages` - Additional pages if needed

#### 2. RAG Backend (FastAPI)

- `/api/v1/embed` - Endpoint for embedding new content
- `/api/v1/query` - Endpoint for RAG queries
- `/api/v1/chat` - Endpoint for chat sessions

#### 3. Chatbot Integration

- Floating widget on all pages
- "Ask about this chapter" button
- "Answer from selected text only" mode
- Conversation history panel

### Development Workflow

#### Adding New Content

1. Create new MDX file in `/docs/module-x/`
2. Add to sidebar configuration in `sidebars.js`
3. Run embedding pipeline to update vector store:
   ```bash
   python -m backend.src.embeddings.process_new_content
   ```

#### Testing RAG Functionality

1. Query the API directly:
   ```bash
   curl -X POST http://localhost:8000/api/v1/query \
     -H "Content-Type: application/json" \
     -d '{"question": "What is ROS 2?", "sessionId": "test-session"}'
   ```

2. Or use the frontend chat interface

#### Building for Production

```bash
# Build frontend
cd frontend
npm run build

# Backend runs separately in production
cd ../backend
# Deploy with your preferred Python hosting solution
```

### API Endpoints

#### Embedding API
- `POST /api/v1/embed` - Create embeddings from content
- `POST /api/v1/embed/chunk` - Create embeddings from text chunks

#### Query API
- `POST /api/v1/query` - RAG query with context
- `POST /api/v1/query/selected-text` - Query using only selected text

#### Chat API
- `POST /api/v1/chat/start` - Start new chat session
- `POST /api/v1/chat/message` - Add message to session
- `GET /api/v1/chat/session/{sessionId}` - Get session history

### Deployment

#### GitHub Pages (Frontend)
1. Configure GitHub Actions workflow
2. Build and deploy automatically on push to main
3. Static files hosted on GitHub Pages

#### Backend Hosting Options
1. Deploy FastAPI backend to:
   - AWS Lambda with API Gateway
   - Google Cloud Run
   - Railway
   - Render
   - Or self-hosted server

#### CI/CD Pipeline
- Frontend: Automatic build and deploy to GitHub Pages
- Backend: Automatic deployment to hosting provider
- Database migrations handled in deployment pipeline