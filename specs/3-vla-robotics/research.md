# Research: Physical AI & Humanoid Robotics — Book + Integrated RAG Chatbot

## Phase 0: Research and Clarification Resolution

### Decision: Language/Version Selection
**Rationale**: Python 3.10+ and Node.js 18+ are chosen based on the requirements for ROS 2 Humble (Python 3.10+), Docusaurus v3 (Node.js 18+), and compatibility with OpenAI SDK, FastAPI, and other dependencies.

**Alternatives considered**:
- Python 3.9 or earlier: Not compatible with ROS 2 Humble requirements
- Node.js 16 or earlier: Not compatible with Docusaurus v3 requirements
- Other languages: Would not align with ROS 2 ecosystem requirements

### Decision: Primary Dependencies
**Rationale**: The selected dependencies align with the project requirements and industry standards:
- Docusaurus v3: Modern static site generator with MDX support for technical documentation
- FastAPI: High-performance Python web framework with excellent async support
- OpenAI SDK: Required for OpenAI Agents/ChatKit integration
- Qdrant Cloud: Vector database for RAG system with free tier available
- Neon Serverless PostgreSQL: Serverless PostgreSQL for metadata and logs
- ChatKit SDK: For chatbot UI integration

**Alternatives considered**:
- Gatsby instead of Docusaurus: Docusaurus is better for documentation sites
- Flask instead of FastAPI: FastAPI has better performance and modern async support
- Pinecone instead of Qdrant: Qdrant has better free tier and open-source option
- Supabase instead of Neon: Neon was specifically requested in requirements

### Decision: Storage Architecture
**Rationale**: Qdrant Cloud for vector storage and Neon Serverless PostgreSQL for metadata/logs provides the optimal combination of:
- Vector search capabilities for RAG system
- Serverless scalability
- Free tier availability
- Integration with Python/FastAPI backend
- Compliance with open-source requirements

**Alternatives considered**:
- Self-hosted PostgreSQL: Would not meet serverless requirement
- Elasticsearch: More complex setup than needed
- MongoDB: Not optimal for vector search
- Redis: Not ideal for metadata storage with complex relationships

### Decision: Testing Framework
**Rationale**:
- pytest for backend: Standard Python testing framework with excellent FastAPI integration
- Jest for frontend: Standard JavaScript testing framework with good Docusaurus compatibility

**Alternatives considered**:
- unittest instead of pytest: pytest has better fixtures and async support
- Mocha/Chai instead of Jest: Jest has better out-of-box configuration
- Cypress instead of Jest for frontend: Jest is better for unit/component testing

### Decision: Target Platform
**Rationale**: Web-based application deployed to GitHub Pages provides:
- Maximum accessibility for students and developers
- Cost-effective hosting solution
- Integration with existing GitHub workflows
- Static site generation for performance
- Compliance with open-source requirements

**Alternatives considered**:
- Desktop application: Would limit accessibility
- Mobile application: Would require separate codebases
- Other hosting (Netlify, Vercel): GitHub Pages is specifically requested

### Decision: Performance Goals
**Rationale**: < 2 sec latency on Qdrant Cloud Free Tier queries and ≥ 90% retrieval accuracy align with:
- User experience requirements for interactive chatbot
- Free Tier limitations and realistic expectations
- Industry standards for RAG systems
- Educational use case requirements

**Alternatives considered**:
- Lower latency: Would require paid tier or different infrastructure
- Higher accuracy: Would require more complex embeddings or larger models

### Decision: Constraints
**Rationale**: Open-source tools only and Free Tier services ensure:
- Accessibility for students and educational institutions
- Reproducibility without requiring paid services
- Compliance with project budget constraints
- Alignment with open-source principles

**Alternatives considered**:
- Paid services: Would limit accessibility
- Proprietary tools: Would violate open-source compliance requirement

### Decision: Scale/Scope
**Rationale**: 4 learning modules, 150-250 pages equivalent, and 10k+ users support:
- Comprehensive coverage of Physical AI & Humanoid Robotics
- Sufficient depth for educational purposes
- Scalable architecture for expected user base
- Alignment with content standards in constitution

**Alternatives considered**:
- Fewer modules: Would not cover all required topics
- More pages: Would exceed reasonable scope
- Higher user count: Would require different infrastructure approach