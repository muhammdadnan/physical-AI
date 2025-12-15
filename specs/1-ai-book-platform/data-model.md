# Data Model: AI Native Book Platform

This document outlines the key data entities and their relationships within the AI Native Book Platform.

## Entities

### User
Represents a registered user of the platform, including their authentication details and personalized profile information.

-   **id**: Unique identifier for the user (Primary Key).
-   **email**: User's email address (Unique, for authentication).
-   **password_hash**: Hashed password for secure authentication.
-   **coding_skill**: User's self-declared coding skill level (e.g., HTML/CSS/JS/React/Python/AI/Robotics).
-   **hardware_available**: Description of user's available hardware (e.g., PC specs, GPU, Jetson Kit, RealSense).
-   **robotics_experience_level**: User's self-declared robotics experience level (e.g., beginner, intermediate, advanced).
-   **preferences**: JSONB or similar field for additional user preferences.

### Chapter
Represents a chapter of the AI Native Book, storing its content and metadata.

-   **id**: Unique identifier for the chapter (Primary Key).
-   **title**: Title of the chapter.
-   **original_content**: The original English markdown content of the chapter.
-   **personalized_content**: Dynamically generated content based on user profile (may not be stored persistently, but rather generated on-demand or cached).
-   **urdu_translated_content**: Dynamically generated Roman Urdu content (may not be stored persistently, but rather generated on-demand or cached).

### ChatbotSession
Represents an ongoing conversation between a user and the RAG chatbot.

-   **session_id**: Unique identifier for the chatbot session (Primary Key).
-   **user_id**: Foreign Key referencing the User entity.
-   **start_time**: Timestamp when the session began.
-   **last_active**: Timestamp of the last user interaction.
-   **conversation_history**: Array of messages, including sender (user/chatbot), timestamp, and message content.

### TextChunk
Represents a small, searchable segment of a chapter's content, used by the RAG pipeline.

-   **id**: Unique identifier for the text chunk (Primary Key).
-   **chapter_id**: Foreign Key referencing the Chapter entity.
-   **chunk_index**: Order of the chunk within its chapter.
-   **original_text**: The raw text content of the chunk.
-   **embedding_vector**: High-dimensional vector representation of the text chunk, stored in Qdrant.
-   **metadata**: JSONB or similar field for additional metadata (e.g., section, paragraph).

## Relationships

-   **User** 1:N **ChatbotSession**: One user can have multiple chatbot sessions.
-   **Chapter** 1:N **TextChunk**: One chapter is broken down into multiple text chunks.

## Data Stores

-   **Neon**: Primary relational database for User, Chapter, and ChatbotSession entities, and TextChunk metadata. Chosen for its PostgreSQL compatibility and free-tier availability.
-   **Qdrant**: Vector database for storing `TextChunk.embedding_vector`. Chosen for efficient similarity search and free-tier availability.
