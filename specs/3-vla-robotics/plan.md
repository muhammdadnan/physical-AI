# Implementation Plan: Physical AI & Humanoid Robotics — Book + Integrated RAG Chatbot

**Branch**: `3-vla-robotics` | **Date**: 2025-12-07 | **Spec**: [link]
**Input**: Feature specification from `/specs/3-vla-robotics/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a full Docusaurus-based textbook covering four modules of Physical AI & Humanoid Robotics with an integrated RAG Chatbot using OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud. The system will include four modules (ROS 2, Digital Twin, AI-Robot Brain, VLA) with a backend RAG system and deployment to GitHub Pages.

## Technical Context

**Language/Version**: Python 3.10+, Node.js 18+
**Primary Dependencies**: Docusaurus v3, FastAPI, OpenAI SDK, Qdrant Cloud, Neon Serverless PostgreSQL, ChatKit SDK
**Storage**: Qdrant Cloud for vector storage, Neon Serverless PostgreSQL for metadata and logs
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web-based application deployed to GitHub Pages
**Project Type**: Web (determines source structure)
**Performance Goals**: < 2 sec latency on Qdrant Cloud Free Tier queries, ≥ 90% retrieval accuracy
**Constraints**: Open-source tools only, GitHub Pages deployment, Free Tier services
**Scale/Scope**: 4 learning modules, 150-250 pages equivalent, 10k+ users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Technical Accuracy Compliance
- All implementations must align with official ROS 2, Gazebo, Isaac Sim, Nav2, and VLA documentation
- Code examples must be verified to run in appropriate simulators (Gazebo/Isaac/ROS 2)

### Educational Clarity Verification
- Content must be designed for students with intermediate programming and AI backgrounds
- Modular structure aligned with 4 learning modules must be maintained

### Reproducibility Requirements
- All code examples must be reproducible using open-source tools (ROS 2 Humble, Python 3.10+, Isaac Sim latest stable)
- Docusaurus v3 book must build and deploy successfully on GitHub Pages

### Architecture Alignment
- FastAPI backend for chatbot following industry practices
- Qdrant Cloud (Free Tier) for vector storage with ≥ 90% retrieval accuracy
- Neon Serverless Postgres for metadata and logs
- RAG system must achieve < 2 sec latency on queries

## Project Structure

### Documentation (this feature)

```text
specs/3-vla-robotics/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── docs/                # Docusaurus documentation (modules)
├── static/              # Images, diagrams
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

rag/                    # RAG backend
├── api/
├── embeddings/
└── storage/

scripts/                # Automation scripts
└── [build, deploy, etc.]
```

**Structure Decision**: Web application with separate frontend (Docusaurus-based book) and backend (FastAPI RAG service) with additional rag/ directory for RAG-specific components and scripts/ for automation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |