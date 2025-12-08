import asyncio
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
import logging
from ..config import Config
from ..embeddings.qdrant_client import QdrantEmbeddingStore
from ..performance import QdrantQueryOptimizer, performance_monitor, perf_middleware

logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    RAG pipeline with embeddings, metadata filtering, and top-k retrieval for VLA content
    """
    def __init__(self):
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.qdrant_store = QdrantEmbeddingStore()
        self.top_k = Config.TOP_K
        # Initialize the performance optimizer
        self.optimizer = QdrantQueryOptimizer(
            self.qdrant_store.client,
            self.qdrant_store.collection_name
        )

    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for the given text using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=Config.EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    async def store_document_chunks(self, chunks: List[Dict[str, Any]]):
        """Store document chunks with embeddings in Qdrant"""
        try:
            points = []
            for chunk in chunks:
                # Generate embedding for the chunk content
                embedding = await self.generate_embeddings(chunk["content"])

                # Create a point for Qdrant
                point = {
                    "id": chunk["id"],
                    "vector": embedding,
                    "metadata": {
                        "content": chunk["content"],
                        "title": chunk["title"],
                        "path": chunk["path"],
                        "source": chunk["source"],
                        "chunk_id": chunk["chunk_id"],
                        "created_at": chunk.get("created_at"),
                        **chunk.get("metadata", {})
                    }
                }
                points.append(point)

            # Store all points in Qdrant
            self.qdrant_store.store_embeddings(points)
            logger.info(f"Stored {len(points)} document chunks in vector store")
        except Exception as e:
            logger.error(f"Error storing document chunks: {str(e)}")
            raise

    @performance_monitor
    async def retrieve_relevant_content(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant content based on the query with performance optimization"""
        try:
            # Generate embedding for the query
            query_embedding = await self.generate_embeddings(query)

            # Use the optimized search method to achieve < 2 sec latency
            k = top_k or self.top_k
            results = await self.optimizer.optimized_search(query_embedding, k)

            # Format and return results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result["id"],
                    "score": result["score"],
                    "content": result["payload"]["content"],
                    "title": result["payload"]["title"],
                    "path": result["payload"]["path"],
                    "source": result["payload"]["source"],
                    "metadata": {k: v for k, v in result["payload"].items()
                               if k not in ["content", "title", "path", "source"]}
                })

            logger.info(f"Retrieved {len(formatted_results)} relevant content chunks in optimized search")
            return formatted_results
        except Exception as e:
            logger.error(f"Error retrieving relevant content: {str(e)}")
            raise

    @performance_monitor
    async def build_context_window(self, query: str, top_k: Optional[int] = None) -> str:
        """Build a context window from relevant content for LLM processing with performance optimization"""
        try:
            relevant_chunks = await self.retrieve_relevant_content(query, top_k)

            # Combine the most relevant chunks into a context string
            context_parts = []
            for chunk in relevant_chunks:
                context_parts.append(f"Title: {chunk['title']}\n")
                context_parts.append(f"Content: {chunk['content']}\n")
                context_parts.append("---\n")

            context = "".join(context_parts)
            logger.info(f"Built context window with {len(relevant_chunks)} chunks")
            return context
        except Exception as e:
            logger.error(f"Error building context window: {str(e)}")
            raise

    @performance_monitor
    async def hybrid_search(self, query: str, text_filter: str = "", top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Perform hybrid search combining semantic and keyword search"""
        try:
            # Generate embedding for the query
            query_embedding = await self.generate_embeddings(query)

            # Use the optimized hybrid search
            k = top_k or self.top_k
            results = await self.optimizer.hybrid_search(query_embedding, text_filter, k)

            # Format and return results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result["id"],
                    "score": result["score"],
                    "content": result["payload"]["content"],
                    "title": result["payload"]["title"],
                    "path": result["payload"]["path"],
                    "source": result["payload"]["source"],
                    "metadata": {k: v for k, v in result["payload"].items()
                               if k not in ["content", "title", "path", "source"]}
                })

            logger.info(f"Hybrid search retrieved {len(formatted_results)} relevant content chunks")
            return formatted_results
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            # Fall back to regular search
            return await self.retrieve_relevant_content(query, top_k)

    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        return perf_middleware.get_performance_stats()

    @performance_monitor
    async def batch_retrieve_content(self, queries: List[str], top_k: Optional[int] = None) -> List[List[Dict[str, Any]]]:
        """Retrieve content for multiple queries in a batch for better performance"""
        try:
            # Generate embeddings for all queries
            query_embeddings = []
            for query in queries:
                embedding = await self.generate_embeddings(query)
                query_embeddings.append(embedding)

            # Use batch search for better performance
            k = top_k or self.top_k
            batch_results = await self.optimizer.batch_search(query_embeddings, k)

            # Format all results
            formatted_batch_results = []
            for results in batch_results:
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        "id": result["id"],
                        "score": result["score"],
                        "content": result["payload"]["content"],
                        "title": result["payload"]["title"],
                        "path": result["payload"]["path"],
                        "source": result["payload"]["source"],
                        "metadata": {k: v for k, v in result["payload"].items()
                                   if k not in ["content", "title", "path", "source"]}
                    })
                formatted_batch_results.append(formatted_results)

            logger.info(f"Batch retrieval completed for {len(queries)} queries")
            return formatted_batch_results
        except Exception as e:
            logger.error(f"Error in batch retrieval: {str(e)}")
            # Fall back to individual queries
            results = []
            for query in queries:
                results.append(await self.retrieve_relevant_content(query, top_k))
            return results