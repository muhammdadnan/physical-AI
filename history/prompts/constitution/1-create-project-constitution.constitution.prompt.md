---
id: 1
title: "Create Project Constitution"
stage: constitution
date: 2025-12-07
model: claude-sonnet-4-5-20250929
feature: "Physical AI & Humanoid Robotics Book + RAG Chatbot"
branch: "master"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests: []
---

# Prompt History Record: Create Project Constitution

## Prompt Text

```
/sp.constitution

Project: Unified Book + RAG Chatbot for "Physical AI & Humanoid Robotics"

Core principles:
- Technical accuracy across robotics middleware (ROS 2), simulation (Gazebo/Unity/Isaac), and AI systems.
- Consistency and clarity for students with intermediate programming + AI background.
- Modular structure aligned with 4 learning modules.
- Hands-on reproducibility using open-source tools.
- High-level coherence between book content and chatbot knowledge base.

Key standards:
- All explanations must be correct according to official ROS 2, Gazebo, Isaac Sim, Nav2, and VLA (Vision-Language-Action) documentation.
- All code examples must run inside modern environments: ROS 2 Humble, Python 3.10+, Isaac Sim latest stable.
- Book format: Docusaurus v3, Markdown/MDX, fully deployable on GitHub Pages.
- Chatbot must answer:
  1. Questions based on full-book RAG.
  2. Questions based strictly on user-selected text.
- Chatbot architecture must follow industry practices:
  - FastAPI backend
  - OpenAI Agents/ChatKit SDK
  - Qdrant Cloud (Free Tier) for vector storage
  - Neon Serverless Postgres for metadata and logs

Constraints:
- Book length: minimum 150–250 pages (equivalent in Docusaurus MDX).
- Each module must include:
  - Concepts
  - Workflow diagrams
  - 5–10 runnable code samples
  - 2–3 mini-projects
- Capstone project chapter must include:
  - Voice-to-action pipeline
  - Navigation + VSLAM process
  - Object detection + manipulation steps
  - End-to-end ROS 2 action planning example
- RAG pipeline must support embeddings, metadata filtering, and top-k retrieval.
- All diagrams must be AI-generated or tool-generated with exportable sources.

Success criteria:
- Book successfully builds and deploys via GitHub Pages with no Docusaurus build errors.
- All code samples verified to run in appropriate simulators (Gazebo/Isaac/ROS 2).
- Chatbot embedded in the site with:
  - Accurate retrieval from the book
  - Ability to answer questions only from user-selected text
  - Streaming responses
- RAG evaluation:
  - ≥ 90% retrieval accuracy on test prompts
  - Latency < 2 sec on Qdrant Cloud Free Tier queries
- Users can learn and complete the final humanoid robotics capstone project solely from the book and chatbot.
```

## Response Text

Created the project constitution for the Physical AI & Humanoid Robotics Book + RAG Chatbot project, including:

- Core principles: Technical Accuracy, Educational Clarity, Hands-On Reproducibility, Modular Architecture, Open Source Compliance, and RAG Excellence
- Content Standards aligned with the project requirements
- Development Workflow guidelines
- Governance section

Updated dependent templates to align with the new constitution:
- Modified plan-template.md to include constitution checks for technical accuracy, educational clarity, reproducibility, and architecture alignment
- Updated spec-template.md with functional requirements related to ROS 2, Gazebo, Isaac Sim, and VLA compliance
- Enhanced tasks-template.md with specific tasks for Docusaurus book, FastAPI chatbot, Qdrant integration, and robotics simulation

## Outcome

The project constitution has been successfully created and saved to `.specify/memory/constitution.md` with version 1.1.0. All dependent templates have been updated to align with the new constitution's principles and requirements.

## Evaluation

The constitution accurately reflects the project requirements with specific focus on technical accuracy, educational clarity, reproducibility, and architectural excellence. The templates have been updated to ensure consistency across the development workflow.