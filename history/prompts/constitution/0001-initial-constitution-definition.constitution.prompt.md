---
id: 0001
title: Initial Constitution Definition
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.constitution project.title: "Physical AI & Humanoid Robotics – AI-Native Textbook"
project.type: "Docusaurus AI-Enhanced Technical Textbook"
project.goal:
  - Create a full technical textbook that teaches the "Physical AI & Humanoid Robotics" course using Docusaurus.
  - Deploy the book to GitHub Pages or Vercel.
  - Build and embed a RAG chatbot inside the book using OpenAI Agents/ChatKit SDK, FastAPI backend, Neon Serverless Postgres, and Qdrant Cloud.
  - Support contextual Q&A: Chatbot must answer questions based on the selected text inside chapters.
project.principles:
  - Everything must be AI-native and spec-driven.
  - Code generation, content writing, and component creation will be automated using Claude Code subagents.
  - Modular, reusable intelligence through subagents and agent skills.
  - Content must be high-quality, accurate, and accessible.
optional.bonus:
  - Implement Better-Auth signup/signin and gather user's hardware/software background.
  - Enable chapter-level personalization based on logged-in user.
  - Add “Translate to Urdu” button on each chapter for instant localized content.
tech.stack:
  frontend: "Docusaurus 3 + React + Tailwind"
  agent_sdk: "OpenAI Agents / ChatKit"
  backend: "FastAPI"
  database_main: "Neon Postgres"
  vector_search: "Qdrant Cloud Free Tier"
  deployment: "GitHub Pages / Vercel"
  auth: "Better-Auth"
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:

tests:

---

## Prompt

sp.constitution project.title: "Physical AI & Humanoid Robotics – AI-Native Textbook"
project.type: "Docusaurus AI-Enhanced Technical Textbook"
project.goal:
  - Create a full technical textbook that teaches the "Physical AI & Humanoid Robotics" course using Docusaurus.
  - Deploy the book to GitHub Pages or Vercel.
  - Build and embed a RAG chatbot inside the book using OpenAI Agents/ChatKit SDK, FastAPI backend, Neon Serverless Postgres, and Qdrant Cloud.
  - Support contextual Q&A: Chatbot must answer questions based on the selected text inside chapters.
project.principles:
  - Everything must be AI-native and spec-driven.
  - Code generation, content writing, and component creation will be automated using Claude Code subagents.
  - Modular, reusable intelligence through subagents and agent skills.
  - Content must be high-quality, accurate, and accessible.
optional.bonus:
  - Implement Better-Auth signup/signin and gather user's hardware/software background.
  - Enable chapter-level personalization based on logged-in user.
  - Add “Translate to Urdu” button on each chapter for instant localized content.
tech.stack:
  frontend: "Docusaurus 3 + React + Tailwind"
  agent_sdk: "OpenAI Agents / ChatKit"
  backend: "FastAPI"
  database_main: "Neon Postgres"
  vector_search: "Qdrant Cloud Free Tier"
  deployment: "GitHub Pages / Vercel"
  auth: "Better-Auth"

## Response snapshot


## Outcome

- ✅ Impact: Constitution defined.
- 🧪 Tests: n/a
- 📁 Files: ./history/prompts/constitution/0001-initial-constitution-definition.constitution.prompt.md
- 🔁 Next prompts: n/a
- 🧠 Reflection: Successfully recorded the initial project constitution.

## Evaluation notes (flywheel)

- Failure modes observed: n/a
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
