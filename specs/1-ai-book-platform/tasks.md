# Feature Tasks: AI Native Book Platform

**Feature Branch**: `1-ai-book-platform` | **Date**: 2025-12-05 | **Spec**: [specs/1-ai-book-platform/spec.md](specs/1-ai-book-platform/spec.md)
**Plan**: [specs/1-ai-book-platform/plan.md](specs/1-ai-book-platform/plan.md)
**Input**: User provided milestones

## Summary

This document outlines the detailed, ordered tasks for implementing the AI Native Book Platform, broken down from user-provided milestones. Each task includes dependencies, acceptance criteria, and refers to relevant specification and plan documents.

## Core Principles Check

- [x] **Library-First**: Tasks are structured to build modular components (frontend, backend services, agents).
- [x] **CLI Interface**: Backend tasks define clear API endpoints.
- [x] **Test-First (NON-NEGOTIABLE)**: Each task implicitly requires writing tests before implementation.
- [x] **Integration Testing**: Explicit tasks for integration testing are included where critical.
- [x] **Observability**: Logging and error handling considerations are part of API implementation.
- [x] **Simplicity**: Tasks aim for the simplest viable solution for each feature.

## Tasks

### Phase 1: Core Setup & Content Structure

1.  **Task**: Initialize Docusaurus project [x]
    *   **Description**: Set up a new Docusaurus project for the book's frontend.
    *   **Dependencies**: None
    *   **Acceptance Criteria**: Docusaurus project is created and runs successfully locally.
    *   **Relevant Spec**: FR-001

2.  **Task**: Configure Docusaurus for Tailwind CSS
    *   **Description**: Integrate Tailwind CSS into the Docusaurus project for streamlined styling.
    *   **Dependencies**: Task 1
    *   **Acceptance Criteria**: Tailwind CSS is correctly configured and applies styles in the Docusaurus project.

3.  **Task**: Set up Git repository for Docusaurus project (if not already done)
    *   **Description**: Initialize Git and make the initial commit for the Docusaurus frontend.
    *   **Dependencies**: Task 1
    *   **Acceptance Criteria**: Docusaurus project is under Git version control.

4.  **Task**: Define Docusaurus `sidebar.js` for book structure
    *   **Description**: Create the navigation structure for all chapters and appendices in `sidebar.js`.
    *   **Dependencies**: Task 1
    *   **Acceptance Criteria**: Sidebar correctly displays all book sections as outlined in `book.structure` from the Feature Specification.

5.  **Task**: Create markdown files for book content placeholders
    *   **Description**: Generate empty markdown files for all chapters and appendices in the `/docs` folder structure.
    *   **Dependencies**: Task 4
    *   **Acceptance Criteria**: All chapter and appendix markdown files exist and are accessible via the Docusaurus sidebar.

### Phase 2: Backend & Data Infrastructure

6.  **Task**: Create `backend/` directory structure
    *   **Description**: Set up the basic folder structure for the FastAPI backend.
    *   **Dependencies**: None
    *   **Acceptance Criteria**: `backend/src/models`, `backend/src/services`, `backend/src/api`, and `backend/tests` directories exist.

7.  **Task**: Initialize FastAPI project within `backend/`
    *   **Description**: Set up a basic FastAPI application within the `backend/` directory.
    *   **Dependencies**: Task 6
    *   **Acceptance Criteria**: FastAPI application runs successfully and serves a basic endpoint.

8.  **Task**: Define Neon database connection and ORM
    *   **Description**: Configure database connection to Neon (PostgreSQL-compatible) and set up an ORM (e.g., SQLAlchemy or Pydantic with asyncpg) in the FastAPI project.
    *   **Dependencies**: Task 7
    *   **Acceptance Criteria**: FastAPI application can connect to the Neon database instance.

9.  **Task**: Implement `backend/src/models/user.py` for User entity
    *   **Description**: Define the User data model, including attributes like `id`, `email`, `password_hash`, `coding_skill`, `hardware_available`, `robotics_experience_level`, and `preferences`.
    *   **Dependencies**: Task 8
    *   **Acceptance Criteria**: User model is defined and can be used to create and retrieve user records in Neon.
    *   **Relevant Spec**: FR-004, FR-005, Key Entities: User

10. **Task**: Implement `backend/src/models/chapter.py` for Chapter entity
    *   **Description**: Define the Chapter data model, including `id`, `title`, `original_content`.
    *   **Dependencies**: Task 8
    *   **Acceptance Criteria**: Chapter model is defined and can be used to create and retrieve chapter records in Neon.
    *   **Relevant Spec**: FR-001, Key Entities: Chapter

11. **Task**: Implement `backend/src/models/chat_session.py` for ChatbotSession entity
    *   **Description**: Define the ChatbotSession data model, including `session_id`, `user_id`, `start_time`, `last_active`, `conversation_history`.
    *   **Dependencies**: Task 8, Task 9
    *   **Acceptance Criteria**: ChatbotSession model is defined and can be used to manage chatbot session history in Neon.
    *   **Relevant Spec**: FR-005, Key Entities: Chatbot Session

12. **Task**: Implement `backend/src/models/text_chunk.py` for TextChunk metadata
    *   **Description**: Define the TextChunk data model for metadata (`id`, `chapter_id`, `chunk_index`, `original_text`). The `embedding_vector` will be handled directly by Qdrant.
    *   **Dependencies**: Task 8, Task 10
    *   **Acceptance Criteria**: TextChunk metadata model is defined and can store chunk-related information in Neon.
    *   **Relevant Spec**: FR-023, Key Entities: Text Chunk

13. **Task**: Integrate Qdrant client into FastAPI project
    *   **Description**: Set up the Qdrant client connection and configuration within the FastAPI application.
    *   **Dependencies**: Task 7
    *   **Acceptance Criteria**: FastAPI application can connect to the Qdrant instance.
    *   **Relevant Spec**: FR-017, FR-022

### Phase 3: Content Ingestion & RAG Pipeline

14. **Task**: Develop a markdown parser to extract text chunks from chapters
    *   **Description**: Create a utility to parse markdown content into smaller, manageable text chunks suitable for embedding.
    *   **Dependencies**: Task 10
    *   **Acceptance Criteria**: Parser can take a markdown string and return a list of text chunks.
    *   **Relevant Spec**: FR-020

15. **Task**: Implement text chunking strategy
    *   **Description**: Define and implement a robust strategy for splitting chapter text into meaningful chunks (e.g., by paragraph, section, or fixed size with overlap).
    *   **Dependencies**: Task 14
    *   **Acceptance Criteria**: Text chunking logic is implemented and produces appropriate chunks from various chapter structures.
    *   **Relevant Spec**: FR-020

16. **Task**: Integrate embedding model (e.g., OpenAI API) for text chunks
    *   **Description**: Set up the integration with an embedding service (e.g., OpenAI API) to generate vector embeddings from text chunks.
    *   **Dependencies**: Task 15
    *   **Acceptance Criteria**: Can successfully generate embeddings for a given text chunk.
    *   **Relevant Spec**: FR-021

17. **Task**: Develop ingestion script to parse markdown → embeddings → store
    *   **Description**: Create a script (`backend/src/services/ingestion.py`) that orchestrates the entire ingestion pipeline: reading markdown chapters, chunking, generating embeddings, and storing vectors in Qdrant and metadata in Neon.
    *   **Dependencies**: Tasks 5, 12, 13, 16
    *   **Acceptance Criteria**: Script can process a full chapter, storing its chunks and embeddings correctly in Qdrant and Neon.
    *   **Relevant Spec**: FR-020, FR-021, FR-022, FR-023

18. **Task**: Build RAG retrieval pipeline (cosine search)
    *   **Description**: Implement the retrieval logic in `backend/src/services/rag.py` to query Qdrant using cosine similarity to find relevant text chunks based on a user query embedding.
    *   **Dependencies**: Task 13, Task 16
    *   **Acceptance Criteria**: Retrieval pipeline can take a query embedding and return the top-N most similar text chunks.
    *   **Relevant Spec**: FR-024

19. **Task**: Implement ChatKit/OpenAI agent for reasoning
    *   **Description**: Integrate the OpenAI Agents/ChatKit SDK into `backend/src/services/rag.py` to orchestrate the final answer generation from retrieved text chunks.
    *   **Dependencies**: Task 18
    *   **Acceptance Criteria**: The agent can process a user query, retrieve relevant context, and generate a coherent answer.
    *   **Relevant Spec**: FR-016, FR-025

### Phase 4: Chatbot UI & API Integration

20. **Task**: Create Docusaurus sidebar chatbot component (`frontend/src/components/Chatbot.tsx`)
    *   **Description**: Develop the React component for the chatbot UI, including input field, message display, and buttons for query modes.
    *   **Dependencies**: Task 1, Task 2
    *   **Acceptance Criteria**: Chatbot UI component renders correctly in the Docusaurus sidebar.
    *   **Relevant Spec**: FR-011

21. **Task**: Develop `POST /embed-text` endpoint in `backend/src/api/chatbot.py`
    *   **Description**: Implement an API endpoint for ingesting text (e.g., for ad-hoc embedding generation).
    *   **Dependencies**: Task 7, Task 16
    *   **Acceptance Criteria**: Endpoint successfully receives text and returns embeddings.
    *   **Relevant Spec**: FR-013

22. **Task**: Develop `POST /query` endpoint in `backend/src/api/chatbot.py`
    *   **Description**: Implement the main API endpoint for general chatbot queries, using the RAG pipeline.
    *   **Dependencies**: Task 7, Task 19
    *   **Acceptance Criteria**: Endpoint receives a query and returns an answer from the ChatKit agent.
    *   **Relevant Spec**: FR-014, FR-019

23. **Task**: Add selection-based Q&A JS snippet to Docusaurus chapter pages
    *   **Description**: Implement JavaScript to detect selected text and trigger a contextual query to the chatbot.
    *   **Dependencies**: Task 5, Task 20
    *   **Acceptance Criteria**: User can select text, trigger a query, and see the chatbot respond with context-specific information.
    *   **Relevant Spec**: FR-018

24. **Task**: Develop `POST /selected-text-query` endpoint in `backend/src/api/chatbot.py`
    *   **Description**: Implement an API endpoint specifically for queries based on selected text, feeding the selected text as additional context to the RAG pipeline.
    *   **Dependencies**: Task 7, Task 19
    *   **Acceptance Criteria**: Endpoint receives selected text and a query, returning a highly relevant answer.
    *   **Relevant Spec**: FR-015

### Phase 5: Authentication & Personalization

25. **Task**: Install and configure Better-Auth
    *   **Description**: Integrate the Better-Auth library or framework into the FastAPI backend for secure authentication.
    *   **Dependencies**: Task 7
    *   **Acceptance Criteria**: Better-Auth is set up and ready to handle user registration and login.
    *   **Relevant Spec**: FR-003

26. **Task**: Implement `backend/src/api/auth.py` for user signup
    *   **Description**: Create the `POST /signup` endpoint to handle new user registration, including collecting coding skill, hardware, and robotics experience.
    *   **Dependencies**: Task 9, Task 25
    *   **Acceptance Criteria**: New users can successfully register, and their profile data is stored in Neon.
    *   **Relevant Spec**: FR-003, FR-004

27. **Task**: Implement `backend/src/api/auth.py` for user signin
    *   **Description**: Create the `POST /signin` endpoint for user login, including session/cookie management.
    *   **Dependencies**: Task 9, Task 25
    *   **Acceptance Criteria**: Registered users can successfully log in and establish a session.
    *   **Relevant Spec**: FR-003, FR-005

28. **Task**: Create `frontend/src/pages/signup.tsx` and `frontend/src/pages/signin.tsx` pages
    *   **Description**: Develop the frontend forms for user registration and login, handling user input and API calls.
    *   **Dependencies**: Task 1, Task 26, Task 27
    *   **Acceptance Criteria**: User can navigate to signup/signin pages, fill forms, and interact with the backend auth endpoints.

29. **Task**: Implement `backend/src/api/personalization.py` for `GET /personalize-chapter` endpoint
    *   **Description**: Develop an API endpoint that takes a chapter ID and user profile, and uses a Claude Code agent skill to rewrite the chapter content based on the user's robotics experience level.
    *   **Dependencies**: Task 10, Task 26
    *   **Acceptance Criteria**: Endpoint successfully receives a chapter request and returns personalized content.
    *   **Relevant Spec**: FR-006, FR-007

30. **Task**: Create `frontend/src/components/PersonalizeButton.tsx` and integrate into Docusaurus chapter layout
    *   **Description**: Develop a React button component that triggers the personalization API and dynamically renders the personalized chapter content.
    *   **Dependencies**: Task 5, Task 29
    *   **Acceptance Criteria**: User can click the personalize button and see the chapter content dynamically adjust based on their profile.
    *   **Relevant Spec**: FR-002, FR-008

### Phase 6: Translation & Deployment

31. **Task**: Implement `backend/src/api/translation.py` for `GET /translate-chapter` endpoint
    *   **Description**: Develop an API endpoint that takes a chapter ID and uses a subagent skill to translate the technical robotics content into clear Roman Urdu.
    *   **Dependencies**: Task 10
    *   **Acceptance Criteria**: Endpoint successfully receives a chapter request and returns Urdu translated content.
    *   **Relevant Spec**: FR-009

32. **Task**: Create `frontend/src/components/TranslateButton.tsx` and integrate into Docusaurus chapter layout
    *   **Description**: Develop a React button component that toggles the chapter content between English and Urdu translation.
    *   **Dependencies**: Task 5, Task 31
    *   **Acceptance Criteria**: User can click the translate button and see the chapter content dynamically switch between English and Urdu.
    *   **Relevant Spec**: FR-002, FR-010

33. **Task**: Test full flow (auth → read → ask → personalize → translate)
    *   **Description**: Conduct end-to-end testing to ensure all integrated features work seamlessly.
    *   **Dependencies**: All previous tasks
    *   **Acceptance Criteria**: All user stories and acceptance scenarios from `spec.md` pass successfully.
    *   **Relevant Spec**: All User Stories and SC-001 to SC-005

34. **Task**: Deploy book (frontend) to GitHub Pages or Vercel
    *   **Description**: Set up continuous deployment for the Docusaurus frontend.
    *   **Dependencies**: Task 33
    *   **Acceptance Criteria**: Frontend is successfully deployed and publicly accessible.
    *   **Relevant Spec**: SC-006

35. **Task**: Deploy backend to Fly.io, Render, or Railway
    *   **Description**: Set up continuous deployment for the FastAPI backend, including Qdrant and Neon configurations.
    *   **Dependencies**: Task 33
    *   **Acceptance Criteria**: Backend is successfully deployed, accessible by the frontend, and integrates with Qdrant/Neon.
    *   **Relevant Spec**: SC-006

## Tasks Quality Checklist: AI Native Book Platform

**Purpose**: Validate task list completeness and quality before proceeding to implementation
**Created**: 2025-12-05
**Feature**: [Link to spec.md](specs/1-ai-book-platform/spec.md)

## Task Completeness

- [ ] All user-provided milestones are covered by tasks.
- [ ] Tasks are granular and actionable.
- [ ] Dependencies between tasks are clearly defined.
- [ ] Each task has clear acceptance criteria.
- [ ] Tasks align with the Feature Specification requirements.
- [ ] Tasks align with the Implementation Plan structure.

## Testability

- [ ] Each task is independently testable or has clear testing steps as part of its acceptance criteria.
- [ ] Integration points have specific testing considerations.

## Notes

- Items marked incomplete require task list updates before `/sp.implement`.
