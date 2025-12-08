<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: None (new constitution)
Added sections: All principles and sections for Physical AI & Humanoid Robotics project
Removed sections: Template placeholders
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# AI-generated Docusaurus book + integrated  RAG Chatbot on Physical AI & Humanoid Robotics Constitution

## Core Principles

### Technical Accuracy
All explanations and code examples must be technically correct according to official ROS 2, Gazebo, Isaac Sim, Nav2, and VLA (Vision-Language-Action) documentation. Every concept, API usage, and implementation detail must align with current best practices and official specifications.

### Educational Clarity
Content must be designed for students with intermediate programming and AI backgrounds, emphasizing consistency and clarity. All materials should follow a modular structure aligned with 4 learning modules to facilitate progressive learning.

### Hands-On Reproducibility
All code examples and projects must be reproducible using open-source tools in modern environments: ROS 2 Humble, Python 3.10+, and Isaac Sim latest stable. Every example should be verified to run in appropriate simulators (Gazebo/Isaac/ROS 2).

### Modular Architecture
The book and chatbot must maintain high-level coherence with a modular structure that supports independent learning modules. Both the Docusaurus-based book (v3, Markdown/MDX) and the FastAPI-based chatbot backend must follow industry-standard architectural practices.

### Open Source Compliance
All components must use open-source tools and libraries wherever possible. The book must be fully deployable on GitHub Pages, and the chatbot architecture must follow industry practices using OpenAI Agents/ChatKit SDK, Qdrant Cloud (Free Tier) for vector storage, and Neon Serverless Postgres for metadata and logs.

### RAG Excellence
The Retrieval-Augmented Generation system must achieve high standards: ≥ 90% retrieval accuracy on test prompts with latency < 2 sec on Qdrant Cloud Free Tier queries. The system must support embeddings, metadata filtering, and top-k retrieval.

## Content Standards

Book length must be minimum 150–250 pages equivalent in Docusaurus MDX format. Each module must include concepts, workflow diagrams, 5–10 runnable code samples, and 2–3 mini-projects. The capstone project chapter must include voice-to-action pipeline, navigation + VSLAM process, object detection + manipulation steps, and end-to-end ROS 2 action planning example.

All diagrams must be AI-generated or tool-generated with exportable sources. The RAG pipeline must support embeddings, metadata filtering, and top-k retrieval with industry-standard practices.

## Development Workflow

All code samples must be verified to run in appropriate simulators (Gazebo/Isaac/ROS 2). The chatbot must be embedded in the site with accurate retrieval from the book, ability to answer questions only from user-selected text, and streaming responses. The book must successfully build and deploy via GitHub Pages with no Docusaurus build errors.

Each module must follow a consistent structure with concepts, diagrams, code samples, and mini-projects. The capstone project must integrate all key concepts from the four learning modules.

## Governance

This constitution governs all development decisions for the Physical AI & Humanoid Robotics book and RAG chatbot project. All implementations must comply with the technical accuracy, educational clarity, reproducibility, and architectural principles outlined above. Any deviation from these principles requires explicit justification and team approval.

Amendments to this constitution must document the rationale, impact assessment, and migration plan for existing code and documentation. All pull requests and reviews must verify compliance with these principles before merging.

**Version**: 1.1.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07