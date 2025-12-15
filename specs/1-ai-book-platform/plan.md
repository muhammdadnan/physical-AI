# Implementation Plan: AI Native Book Platform

**Branch**: `1-ai-book-platform` | **Date**: 2025-12-05 | **Spec**: [specs/1-ai-book-platform/spec.md](specs/1-ai-book-platform/spec.md)
**Input**: Feature specification from `/specs/1-ai-book-platform/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The AI Native Book Platform aims to create an interactive and personalized learning experience for users interested in Physical AI. Key features include dynamic chapter personalization based on user expertise, real-time Urdu translation, an embedded RAG chatbot for content querying, and a secure user authentication system to manage profiles and sessions. The platform will be deployed using free-tier cloud services.

## Technical Context

**Language/Version**: Python 3.10+ (for FastAPI backend), TypeScript/JavaScript (for Docusaurus frontend, React 18+)
**Primary Dependencies**: Docusaurus, FastAPI, OpenAI Agents/ChatKit SDK, Qdrant, Neon, Better-Auth.
**Storage**: Qdrant (vector database for RAG embeddings), Neon (PostgreSQL-compatible database for user profiles, session data, and RAG metadata).
**Testing**: Python: `pytest`, JavaScript/TypeScript: `Jest`, `React Testing Library`.
**Target Platform**: Web (Docusaurus frontend, FastAPI backend deployed on cloud platforms).
**Project Type**: Web application (frontend + backend).
**Performance Goals**:
- Users can successfully load a personalized chapter within 5 seconds of navigation.
- The RAG chatbot provides a relevant and accurate answer to 90% of "Ask based on selected text only" queries within 3 seconds.
- The RAG chatbot provides a relevant and accurate answer to 85% of "Ask whole book" queries within 5 seconds.
**Constraints**:
- Backend deployment to free-tier Fly.io, Render, or Railway.
- Frontend deployment to GitHub Pages or Vercel.
- Qdrant Cloud Free Tier.
- Neon Free Tier.
- OpenAI Agents for inference.
**Scale/Scope**: Support a multi-chapter book with features for personalization, translation, and interactive RAG chatbot, catering to individual learners.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Library-First**: Each major component (chatbot backend, Docusaurus frontend, auth module, personalization agent, translation agent) will be developed as a modular, independently testable unit.
- [x] **II. CLI Interface**: Backend services will expose well-defined API endpoints. Frontend components will interact via these APIs.
- [x] **III. Test-First (NON-NEGOTIABLE)**: All new code for the backend and frontend will be developed using Test-Driven Development (TDD) principles.
- [x] **IV. Integration Testing**: Critical integrations (Frontend-Backend API calls, Chatbot-Qdrant, Chatbot-OpenAI, Auth-Neon) will have dedicated integration tests.
- [x] **V. Observability**: Structured logging will be implemented for backend services. Frontend will use browser developer tools for debugging.
- [x] **VII. Simplicity**: Solutions will prioritize simplicity and avoid premature optimization, adhering to YAGNI principles.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-book-platform/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/            # Pydantic models for data (user, chapter, chatbot, embeddings)
│   ├── services/          # Business logic for auth, RAG, personalization, translation
│   └── api/               # FastAPI endpoints
└── tests/                 # Pytest unit and integration tests

frontend/
├── src/
│   ├── components/        # React components (Chatbot UI, Personalize button, Translate button)
│   ├── pages/             # Docusaurus chapter pages
│   ├── hooks/             # Custom React hooks for data fetching, state management
│   └── services/          # Frontend API interaction
└── tests/                 # Jest/React Testing Library unit and integration tests

docs/                     # Docusaurus generated static content
```

**Structure Decision**: The project will adopt a clear separation between `backend` (FastAPI) and `frontend` (Docusaurus/React) due to the nature of the application. This aligns with a standard web application architecture and facilitates independent development and deployment of each component. The `docs` directory will house the Docusaurus generated content.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
