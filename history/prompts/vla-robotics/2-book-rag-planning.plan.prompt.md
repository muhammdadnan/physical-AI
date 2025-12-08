---
id: 2
title: Book RAG Planning
stage: plan
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: vla-robotics
branch: 3-vla-robotics
user: DELL
command: /sp.plan
labels: [planning, rag, docusaurus, robotics]
links:
  spec: specs/3-vla-robotics/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/3-vla-robotics/plan.md
 - specs/3-vla-robotics/research.md
 - specs/3-vla-robotics/data-model.md
 - specs/3-vla-robotics/quickstart.md
 - specs/3-vla-robotics/contracts/openapi.yaml
tests:
 - null
---

## Prompt

/sp.plan Physical AI & Humanoid Robotics — Book + Integrated RAG Chatbot

Objective:
Create a full Docusaurus-based textbook covering four modules of Physical AI & Humanoid Robotics, and integrate a fully functional RAG Chatbot using OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud. Deploy the final site to GitHub Pages.

Overall Deliverables:
1. A complete multi-module book built with Docusaurus
2. Four fully developed modules:
   - Module 1: ROS 2 — Robotic Nervous System
   - Module 2: Digital Twin — Gazebo & Unity
   - Module 3: AI-Robot Brain — NVIDIA Isaac Sim & Isaac ROS
   - Module 4: VLA — Vision-Language-Action Pipeline
3. A RAG Chatbot embedded inside the book with:
   - Page-level retrieval
   - "Answer from selected text only" mode
4. Backend for RAG:
   - FastAPI server
   - Qdrant Cloud vector search
   - Neon Serverless PostgreSQL for metadata & logs
5. GitHub Pages deployment with CI/CD

====================================================
PHASE 1 — Project Setup & Architecture
====================================================

1. Create GitHub repository
2. Initialize Docusaurus project template
3. Establish directory structure:
   - /docs (modules)
   - /static (images, diagrams)
   - /rag (backend)
   - /scripts (automation)
4. Install dependencies:
   - Docusaurus plugins
   - MDX rendering tools
   - Mermaid/diagrams support
5. Define book theme, navigation, sidebar, global TOC
6. Set up GitHub Pages deployment workflow (Actions)

Outcome:
A skeleton book with CI/CD deployment ready.

====================================================
PHASE 2 — Module Content Production
====================================================

Module 1: ROS 2 — The Robotic Nervous System
- Write chapters on nodes, topics, services, actions, rclpy
- Build URDF humanoid examples
- Create diagrams for ROS Graph, URDF tree
- Add 2 mini-projects

Module 2: Digital Twin (Gazebo & Unity)
- Develop chapters on physics, simulation, sensor modeling
- Build Gazebo world + Unity scene examples
- Add LiDAR, Depth, IMU diagrams
- Add 2 mini-projects

Module 3: AI-Robot Brain (NVIDIA Isaac Sim)
- Add chapters on Isaac Sim, synthetic data, Isaac ROS VSLAM
- Develop Nav2 humanoid navigation chapter
- Add diagrams: VSLAM Pipeline, Nav2 Architecture
- Add 2 mini-projects

Module 4: Vision-Language-Action (VLA)
- Write chapters on Whisper, LLM planning, ROS action execution
- Integrate vision + navigation + manipulation workflow
- Add capstone project: Autonomous Humanoid
- Add pipeline diagrams (Voice → Plan → Navigate → Perceive → Act)

Outcome:
A full multi-module robotics textbook in MDX.

====================================================
PHASE 3 — RAG Chatbot Backend
====================================================

1. Create FastAPI backend
2. Create `/embed` pipeline:
   - Parse MDX → clean markdown
   - Generate embeddings via OpenAI
   - Store vectors in Qdrant Cloud
   - Store doc metadata in Neon Postgres

3. Create `/query` pipeline:
   - Retrieve from Qdrant
   - Context window assembly
   - Route to OpenAI Agent for completion

4. Implement "Answer from selected text only" mode:
   - Takes user-highlighted text
   - Disables RAG
   - Agent answers strictly from the provided text

5. Logging:
   - Store queries + timestamps in Neon

Outcome:
Fully functioning RAG backend ready for UI integration.

====================================================
PHASE 4 — Frontend Chatbot Integration
====================================================

1. Add Chat UI inside Docusaurus using ChatKit SDK
2. Embed a floating chatbot widget on all pages
3. Add "Ask about this chapter" button
4. Add "Answer based on selected text only" mode
5. Build search + history panel
6. Ensure mobile responsiveness

Outcome:
Interactive chatbot fully integrated into the book.

====================================================
PHASE 5 — Polishing, Testing, and Deployment
====================================================

1. Prototype tests:
   - RAG retrieval accuracy
   - Whisper pipeline test (mock demo)
   - LLM planning to ROS pseudo-examples
2. Validate navigation across all modules
3. Add diagrams, code blocks, animations where needed
4. Optimize build size and CDN assets
5. Final GitHub Pages deployment
6. Create version tag (v1.0)

====================================================
SUCCESS CRITERIA
====================================================

- All 4 modules written, illustrated, and published in Docusaurus
- RAG chatbot responds accurately using book content
- "Answer based on selected text only" works reliably
- FastAPI + Qdrant + Neon stack functioning in production
- Site deployed successfully to GitHub Pages
- All code, diagrams, and examples reproducible
- Book readable and navigable on desktop + mobile

====================================================
TIMELINE
====================================================

Total: 6–8 weeks recommended

Week 1:
- Project setup, Docusaurus, structure, deployment

Week 2–4:
- Write Module 1–4 chapters
- Add diagrams, examples, narrative

Week 5:
- Build RAG backend + embeddings

Week 6:
- Integrate chatbot UI + testing

Week 7–8:
- Final polishing, optimization, deployment

## Response snapshot

Created a comprehensive implementation plan for the Physical AI & Humanoid Robotics Book with Integrated RAG Chatbot. The plan includes:

- Technical Context with resolved clarifications for languages, dependencies, storage, testing, platform, performance goals, and constraints
- Constitution Check confirming compliance with project principles
- Project Structure defining the web application architecture with frontend (Docusaurus) and backend (FastAPI) components
- Research document resolving all "NEEDS CLARIFICATION" items with rationale and alternatives
- Data model defining core entities (Book Module, Chapter, Embedding, Query, Chat Session, User, Metadata Log) with relationships and validation rules
- Quickstart guide with setup instructions, development workflow, and deployment guidance
- OpenAPI contract specification for the RAG backend API with all endpoints and schemas

All Phase 0 and Phase 1 planning artifacts have been created and are ready for implementation.

## Outcome

- ✅ Impact: Created comprehensive implementation plan for book + RAG system
- 🧪 Tests: No tests run yet, planning artifacts created
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml
- 🔁 Next prompts: Ready for task generation phase (/sp.tasks)
- 🧠 Reflection: Planning successfully captures the complex architecture and integration requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable yet
- Prompt variant (if applicable): Original planning prompt
- Next experiment (smallest change to try): Proceed to task generation phase