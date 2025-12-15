# Feature Specification: AI Native Book Platform

**Feature Branch**: `1-ai-book-platform`
**Created**: 2025-12-05
**Status**: Draft
**Input**: User description: """
book.structure:
  - Introduction to Physical AI
  - Part 1: ROS 2 Foundations
  - Part 2: Digital Twin Simulation (Gazebo + Unity)
  - Part 3: NVIDIA Isaac Platform
  - Part 4: Vision-Language-Action (VLA)
  - Part 5: Humanoid Robotics (Kinematics, Control, Interaction)
  - Part 6: Capstone – Autonomous Humanoid Robot
  - Appendices: Hardware Guide, Lab Setup, Cloud Setup

pages.features:
  - Each chapter page includes:
      - Personalize button
      - Translate to Urdu button
      - Right sidebar embedded RAG chatbot

chatbot.spec:
  - Chatbot component embedded in Docusaurus layout
  - Uses FastAPI backend with routes:
      - POST /embed-text
      - POST /query
      - POST /selected-text-query
  - Uses OpenAI Agents/ChatKit SDK for reasoning
  - Uses Qdrant for vector storage
  - Uses Neon for user/session/history data
  - Supports "Ask based on selected text only"
  - Supports "Ask whole book"

rag.pipeline:
  ingestion:
    - Convert all markdown Chapters → text chunks → embeddings
    - Store vectors in Qdrant
    - Store metadata in Neon
  retrieval:
    - cosine search for similarity
  reasoning:
    - ChatKit agent orchestrates final answers

auth.spec:
  - Better-auth signup/signin
  - Signup form asks:
      - Coding skill (HTML/CSS/JS/React/Python/AI/Robotics)
      - Hardware available (PC specs, GPU, Jetson Kit, RealSense)
      - Robotics experience level
  - Store user profile in Neon + cookies/session

personalization.spec:
  - On chapter load, check user profile
  - Transform chapter text using Claude Code agent skill:
       "Rewrite chapter for beginner/intermediate/advanced robotics"
  - Render personalized version dynamically

translation.spec:
  - Urdu translation using subagent:
       "Translate technical robotics content to clear Roman Urdu"
  - Render toggle (English/Urdu)

deployment.spec:
  - Book deployed to GitHub Pages or Vercel
  - Backend deployed to free-tier Fly.io, Render, or Railway
  - Qdrant Cloud Free Tier
  - Neon Free Tier
  - OpenAI Agents for inference
"""

## User Scenarios & Testing

### User Story 1 - Personalized Chapter Viewing (Priority: P1)

A user loads a chapter page and sees the content rewritten to match their specified robotics experience level (beginner, intermediate, or advanced) from their profile.

**Why this priority**: Core value proposition, enhances user engagement and learning effectiveness.

**Independent Test**: A user can fully test this by setting their experience level in their profile, navigating to a chapter, and verifying the content reflects the chosen level. This delivers immediate value by tailoring the learning experience.

**Acceptance Scenarios**:

1.  **Given** a user is logged in with a "beginner" robotics experience, **When** they navigate to "Part 1: ROS 2 Foundations", **Then** the chapter content is rewritten for a beginner audience.
2.  **Given** a user is logged in with an "advanced" robotics experience, **When** they navigate to "Part 4: Vision-Language-Action (VLA)", **Then** the chapter content is rewritten for an advanced audience.

---

### User Story 2 - Interactive RAG Chatbot (Priority: P1)

A user views a chapter page and can interact with an embedded chatbot. They can ask questions based on selected text within the chapter or query the entire book's content. The chatbot provides relevant and accurate answers.

**Why this priority**: Provides immediate assistance and deepens understanding, crucial for an AI-native educational book.

**Independent Test**: A user can ask a question about a specific paragraph (selected text) or a general topic covered in the book. The chatbot's ability to provide accurate and contextually relevant answers demonstrates its value.

**Acceptance Scenarios**:

1.  **Given** a user is viewing "Part 1: ROS 2 Foundations" and selects a paragraph on "ROS Nodes", **When** they click "Ask based on selected text only" and type "What is a ROS Node?", **Then** the chatbot provides a concise explanation of ROS Nodes based on the selected text.
2.  **Given** a user is on any chapter page, **When** they click "Ask whole book" and type "How does inverse kinematics work?", **Then** the chatbot provides a detailed explanation of inverse kinematics from the book's content.

---

### User Story 3 - Multilingual Chapter Access (Priority: P2)

A user viewing any chapter page can toggle a button to switch the chapter content between English and a clear Roman Urdu translation.

**Why this priority**: Expands accessibility and caters to a broader audience, increasing the book's reach.

**Independent Test**: A user can navigate to any chapter, toggle the language button to Urdu, and verify that the technical content is accurately translated into understandable Roman Urdu.

**Acceptance Scenarios**:

1.  **Given** a user is viewing "Introduction to Physical AI" in English, **When** they click the "Translate to Urdu" button, **Then** the chapter content is dynamically re-rendered in Roman Urdu.
2.  **Given** a user is viewing "Part 3: NVIDIA Isaac Platform" in Roman Urdu, **When** they click the "Translate to English" button, **Then** the chapter content is dynamically re-rendered in English.

---

### User Story 4 - User Account Management (Priority: P2)

A new user can sign up for an account, providing details about their coding skills, available hardware, and robotics experience. Existing users can sign in securely.

**Why this priority**: Essential for enabling personalization and other user-specific features.

**Independent Test**: A new user can successfully create an account, provide their profile details, and then log in. An existing user can successfully log in with their credentials.

**Acceptance Scenarios**:

1.  **Given** a new user visits the signup page, **When** they fill out the form (coding skill, hardware, robotics experience) and submit, **Then** their profile is stored in Neon and they are logged in.
2.  **Given** a returning user visits the signin page, **When** they enter their credentials and submit, **Then** they are successfully authenticated and their session is maintained via cookies.

---

### Edge Cases

-   What happens if the personalization agent fails to rewrite a chapter? (Fallback to original English text)
-   How does the chatbot handle queries that are completely outside the scope of the book's content? (Inform user that it cannot answer)
-   What happens if the Urdu translation subagent encounters an error? (Fallback to English text)
-   What happens if a user's profile is incomplete or missing experience levels during personalization? (Default to "intermediate" level)
-   How does the system handle network errors during API calls for chatbot or personalization? (Display user-friendly error message, retry mechanism)

## Requirements

### Functional Requirements

-   **FR-001**: System MUST display an AI-native book with a defined structure including chapters and appendices.
-   **FR-002**: Each chapter page MUST include a "Personalize" button, a "Translate to Urdu" button, and a right sidebar embedded RAG chatbot.
-   **FR-003**: System MUST allow users to sign up and sign in using a "better-auth" solution.
-   **FR-004**: Signup form MUST collect user's coding skill (HTML/CSS/JS/React/Python/AI/Robotics), hardware available (PC specs, GPU, Jetson Kit, RealSense), and robotics experience level.
-   **FR-005**: System MUST store user profiles, session data, and chatbot history data in Neon.
-   **FR-006**: On chapter load, System MUST check the user's profile for their robotics experience level.
-   **FR-007**: System MUST transform chapter text based on the user's robotics experience using a Claude Code agent skill "Rewrite chapter for beginner/intermediate/advanced robotics".
-   **FR-008**: System MUST dynamically render the personalized version of the chapter.
-   **FR-009**: System MUST provide Urdu translation for technical robotics content using a subagent skill "Translate technical robotics content to clear Roman Urdu".
-   **FR-010**: System MUST dynamically render a toggle (English/Urdu) for translation.
-   **FR-011**: Chatbot component MUST be embedded within the Docusaurus layout.
-   **FR-012**: Chatbot backend MUST be a FastAPI application.
-   **FR-013**: Chatbot FastAPI backend MUST expose a `POST /embed-text` route for text ingestion.
-   **FR-014**: Chatbot FastAPI backend MUST expose a `POST /query` route for general book queries.
-   **FR-015**: Chatbot FastAPI backend MUST expose a `POST /selected-text-query` route for queries based on selected text.
-   **FR-016**: Chatbot MUST use OpenAI Agents/ChatKit SDK for reasoning.
-   **FR-017**: Chatbot MUST use Qdrant for vector storage.
-   **FR-018**: Chatbot MUST support "Ask based on selected text only" functionality.
-   **FR-019**: Chatbot MUST support "Ask whole book" functionality.
-   **FR-020**: Ingestion pipeline MUST convert all markdown chapters to text chunks.
-   **FR-021**: Ingestion pipeline MUST generate embeddings from text chunks.
-   **FR-022**: Ingestion pipeline MUST store generated vectors in Qdrant.
-   **FR-023**: Ingestion pipeline MUST store metadata (chapter, chunk ID, etc.) in Neon.
-   **FR-024**: Retrieval pipeline MUST use cosine search for similarity to find relevant text chunks.
-   **FR-025**: Reasoning pipeline MUST use a ChatKit agent to orchestrate final answers from retrieved information.

### Key Entities

-   **User**: Represents a registered user of the platform. Attributes include: unique ID, authentication credentials, coding skill level, hardware available, robotics experience level, and preferences.
-   **Chapter**: A discrete section of the AI Native Book content. Attributes include: ID, title, original English content, personalized content (dynamic based on user profile), Urdu translated content (dynamic based on user selection).
-   **Chatbot Session**: Represents an ongoing conversation with the RAG chatbot. Attributes include: session ID, user ID, conversation history (turns), context.
-   **Text Chunk**: A small, digestible segment of chapter content used for RAG. Attributes include: ID, source chapter ID, original text, embedding vector.
-   **User Profile**: Stores user-specific information for personalization and authentication. Attributes include: user ID, coding skill, hardware available, robotics experience level.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: Users can successfully load a personalized chapter within 5 seconds of navigation.
-   **SC-002**: The RAG chatbot provides a relevant and accurate answer to 90% of "Ask based on selected text only" queries.
-   **SC-003**: The RAG chatbot provides a relevant and accurate answer to 85% of "Ask whole book" queries.
-   **SC-004**: Urdu translation of technical robotics content is deemed "clear and understandable" by 95% of native Urdu speakers in user acceptance testing.
-   **SC-005**: User signup and signin processes are completed within 10 seconds (from form submission to successful authentication).
-   **SC-006**: The AI-native book frontend successfully deploys to GitHub Pages or Vercel, and the backend to Fly.io, Render, or Railway, utilizing Qdrant Cloud Free Tier and Neon Free Tier.
-   **SC-007**: The ingestion pipeline successfully processes all book chapters into Qdrant and Neon within 24 hours for a book of 50 chapters.
