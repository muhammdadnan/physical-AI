# Data Model: Physical AI & Humanoid Robotics — Book + Integrated RAG Chatbot

## Phase 1: Data Model Design

### Core Entities

#### 1. Book Module
- **id**: string (UUID)
- **title**: string (module title)
- **slug**: string (URL-friendly identifier)
- **content**: string (MDX content)
- **order**: integer (sequence in book)
- **createdAt**: datetime
- **updatedAt**: datetime
- **metadata**: JSON object (additional properties)

#### 2. Chapter
- **id**: string (UUID)
- **moduleId**: string (foreign key to Book Module)
- **title**: string (chapter title)
- **slug**: string (URL-friendly identifier)
- **content**: string (MDX content)
- **order**: integer (sequence in module)
- **wordCount**: integer
- **readingTime**: integer (minutes)
- **createdAt**: datetime
- **updatedAt**: datetime

#### 3. Embedding
- **id**: string (UUID)
- **documentId**: string (reference to source document)
- **chunkId**: string (identifier for text chunk)
- **content**: string (text chunk)
- **embedding**: array<float> (vector representation)
- **metadata**: JSON object (source, page, section info)
- **createdAt**: datetime

#### 4. Query
- **id**: string (UUID)
- **sessionId**: string (chat session identifier)
- **question**: string (user query)
- **response**: string (AI response)
- **contextUsed**: array<string> (retrieved document IDs)
- **timestamp**: datetime
- **userId**: string (optional, for analytics)

#### 5. Chat Session
- **id**: string (UUID)
- **userId**: string (optional, for persistence)
- **createdAt**: datetime
- **lastActive**: datetime
- **title**: string (auto-generated from first query)
- **messages**: array<JSON> (conversation history)

#### 6. User
- **id**: string (UUID)
- **email**: string (optional, for analytics)
- **createdAt**: datetime
- **lastSeen**: datetime
- **preferences**: JSON object (UI preferences, etc.)

#### 7. Metadata Log
- **id**: string (UUID)
- **documentId**: string (reference to source)
- **type**: string (module, chapter, etc.)
- **title**: string
- **path**: string (URL path)
- **version**: string
- **createdAt**: datetime
- **updatedAt**: datetime

### Relationships

```
Book Module (1) ←→ (N) Chapter
Book Module (1) ←→ (N) Embedding (via documentId)
Chapter (1) ←→ (N) Embedding (via documentId)
Query (N) ←→ (1) Chat Session
Query (N) ←→ (1) User (optional)
Embedding (N) ←→ (1) Metadata Log
```

### Validation Rules

#### Book Module
- title: Required, max 200 characters
- slug: Required, URL-safe, unique
- order: Required, positive integer, unique per book

#### Chapter
- title: Required, max 200 characters
- moduleId: Required, must reference existing module
- order: Required, positive integer, unique per module
- content: Required, valid MDX format

#### Embedding
- documentId: Required
- content: Required, max 8191 characters (for vector DB)
- embedding: Required, float array of correct dimension
- metadata: Must include source document reference

#### Query
- question: Required, max 1000 characters
- response: Required
- sessionId: Required, must reference existing session

#### Chat Session
- title: Required, max 100 characters

### State Transitions

#### Document Processing Pipeline
1. **Content Creation**: New module/chapter created
2. **Content Validation**: MDX content validated
3. **Embedding Generation**: Vector embeddings created
4. **Storage**: Embeddings stored in Qdrant, metadata in Neon
5. **Ready**: Available for RAG queries

#### Query Processing Pipeline
1. **Query Received**: User submits question
2. **Context Retrieval**: Relevant documents retrieved from Qdrant
3. **Response Generation**: OpenAI generates response with context
4. **Response Returned**: Answer delivered to user
5. **Log Entry**: Query and response logged in Neon