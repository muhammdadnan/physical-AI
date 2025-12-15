# Physical AI & Humanoid Robotics Book + RAG Chatbot

This repository contains a comprehensive textbook on Physical AI and Humanoid Robotics with an integrated RAG (Retrieval-Augmented Generation) chatbot system. The system combines Docusaurus-based documentation with FastAPI backend services for voice processing, LLM planning, vision processing, and ROS 2 action execution.

## 📚 Book Modules

The textbook is organized into four comprehensive modules:

1. **Module 1: ROS 2** - Fundamentals of ROS 2, nodes, topics, services, actions, and rclpy
2. **Module 2: Digital Twin** - Gazebo physics, Unity rendering, sensor integration
3. **Module 3: AI-Robot Brain (NVIDIA Isaac)** - Isaac Sim, synthetic data, VSLAM, Nav2
4. **Module 4: Vision-Language-Action (VLA)** - Voice-to-action pipeline, LLM planning, ROS 2 execution, perception (✅ **COMPLETED**)

## 🤖 VLA System Architecture

The VLA (Vision-Language-Action) system integrates multiple AI and robotics components:

```
Voice Command → Whisper STT → LLM Planning → ROS 2 Actions → Robot Action
     ↑                                           ↓
Camera Input ← Vision Processing ← Perception Integration
```

### Core Components

- **Voice Processing**: OpenAI Whisper for speech-to-text conversion
- **Cognitive Planning**: LLM-based task decomposition and action sequencing
- **Vision Processing**: Object detection and scene understanding
- **Action Execution**: ROS 2 action sequences with feedback and error handling
- **RAG System**: Vector storage with Qdrant Cloud and semantic search

## 🏗️ System Architecture

### Backend Services

The system includes multiple interconnected services:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend APIs   │    │   RAG Service   │
│  (Docusaurus)   │◄──►│   (FastAPI)      │◄──►│  (FastAPI)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                             │
                    ┌──────────────────┐
                    │  Database &      │
                    │  Vector Store    │
                    └──────────────────┘
```

### API Endpoints

#### Voice Processing
- `POST /voice/transcribe` - Transcribe voice commands using Whisper
- `POST /voice/upload-audio` - Upload and transcribe audio files
- `POST /voice/streaming` - Handle streaming voice input

#### Planning Service
- `POST /planning/create` - Create LLM plans from goals
- `POST /planning/validate` - Validate generated plans
- `POST /planning/refine` - Refine plans based on feedback

#### Vision Service
- `POST /vision/detect-objects` - Detect objects in images
- `POST /vision/get-object-location` - Get specific object location
- `POST /vision/analyze-scene` - Analyze scene context

#### Action Execution
- `POST /actions/map-plan` - Map LLM plans to ROS 2 actions
- `POST /actions/execute` - Execute ROS 2 action sequences
- `POST /actions/validate` - Validate action sequences

#### Capstone Integration
- `POST /capstone/create-project` - Create capstone projects
- `POST /capstone/start-session` - Start capstone sessions
- `POST /capstone/execute-task` - Execute capstone tasks

#### RAG Endpoints
- `POST /embed` - Embed content for vector storage
- `POST /query` - Query knowledge base
- `POST /answer_from_selected` - Answer from selected text only

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key
- Qdrant Cloud account (or local instance)
- PostgreSQL database (or Neon Serverless)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-native-book
   ```

2. **Set up backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up RAG service**
   ```bash
   cd rag
   pip install -r requirements.txt
   ```

4. **Set up frontend (Docusaurus)**
   ```bash
   cd frontend
   npm install
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Configuration
QDRANT_URL=https://your-cluster-url.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

# Database Configuration
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# Logging Configuration
LOG_LEVEL=INFO

# RAG Configuration
TOP_K=5
EMBEDDING_MODEL=text-embedding-ada-002

# LLM Configuration
LLM_MODEL=gpt-4-turbo

# Whisper Configuration
WHISPER_MODEL=whisper-1
```

### Running the Services

#### Backend API
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

#### RAG Service
```bash
cd rag
uvicorn api.main:app --reload --port 8001
```

#### Frontend (Docusaurus)
```bash
cd frontend
npm start
```

## 📖 Documentation Structure

The book content is organized in the `docs/module-4/` directory:

```
docs/module-4/
├── 01-introduction.mdx          # VLA fundamentals
├── 02-whisper-setup.mdx         # Whisper integration
├── 03-llm-planning.mdx          # LLM cognitive planning
├── 04-ros2-execution.mdx        # ROS 2 action execution
├── 05-vision-perception.mdx     # Vision processing
├── 06-mini-project.mdx          # Voice-controlled task runner
├── 07-capstone-project.mdx      # Autonomous humanoid capstone
├── action-examples.mdx          # Action execution examples
├── capstone-workflow.mdx        # Capstone workflow examples
├── planning-examples.mdx        # Planning examples
├── task-runner-code.mdx         # Task runner code
├── task-runner-example.mdx      # Task runner examples
├── whisper-examples.mdx         # Whisper examples
└── vision-examples.mdx          # Vision examples
```

## 🔧 Development

### Adding New Content

To add new book content, create MDX files in the `frontend/docs/module-4/` directory. The system supports:

- Markdown syntax
- JSX components
- Mermaid diagrams
- Code blocks with syntax highlighting

### Adding New API Endpoints

To add new backend endpoints:

1. Create a new service in `backend/src/services/`
2. Create a new API module in `backend/src/api/`
3. Register the routes in `backend/src/main.py`

### Testing

Run backend tests:
```bash
cd backend
python -m pytest tests/
```

## 🚀 Deployment

### GitHub Pages (Frontend)

The Docusaurus frontend is deployed to GitHub Pages. The workflow is configured in `.github/workflows/deploy.yml`.

### Backend Deployment

The backend services can be deployed to any cloud provider that supports Python applications (AWS, GCP, Azure, etc.).

## 🛡️ Security Considerations

- API keys are stored in environment variables
- Input validation is performed on all endpoints
- Rate limiting should be implemented in production
- HTTPS is required for production deployments

## 📊 Performance

- Qdrant Cloud queries optimized for < 2 sec latency
- Caching implemented for frequently accessed content
- Asynchronous processing for I/O operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Success Criteria Achieved

✅ All 4 modules complete with diagrams
✅ RAG chatbot answers accurately from book content
✅ "Selected text only" mode works reliably
✅ FastAPI + Qdrant + Neon stack stable in production
✅ All pages readable on mobile + desktop
✅ GitHub Pages site accessible publicly

The VLA (Vision-Language-Action) system provides a complete pipeline from voice commands to robot actions, with cognitive planning, perception integration, and robust execution capabilities.