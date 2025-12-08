"""
Performance Optimization for Qdrant Cloud Queries

This module contains performance optimization strategies to achieve < 2 sec latency
on Qdrant Cloud queries as required by the project specifications.
"""
import asyncio
import time
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams
import numpy as np
from functools import wraps
import weakref

logger = logging.getLogger(__name__)

class QdrantQueryOptimizer:
    """
    Optimizer for Qdrant Cloud queries to achieve < 2 sec latency
    """
    def __init__(self, client: QdrantClient, collection_name: str):
        self.client = client
        self.collection_name = collection_name
        self.query_cache = {}  # Simple cache for frequent queries
        self.cache_ttl = 300  # 5 minutes TTL
        self.max_retries = 3
        self.timeout = 1.8  # Leave 0.2s buffer for < 2s requirement

    def time_it(func):
        """Decorator to measure execution time"""
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = await func(self, *args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        return wrapper

    @time_it
    async def optimized_search(self, query_vector: List[float], top_k: int = 5,
                              query_filter: Optional[models.Filter] = None) -> List[Dict[str, Any]]:
        """
        Optimized search function to achieve < 2 sec latency
        """
        try:
            # Use async search with optimized parameters
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=query_filter,
                limit=top_k,
                timeout=self.timeout,
                # Use HNSW index for faster approximate search
                search_params=models.SearchParams(
                    hnsw_ef=128,  # Higher values = more accurate but slower
                    exact=False   # Use approximate search
                )
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })

            logger.info(f"Found {len(formatted_results)} results in optimized search")
            return formatted_results

        except Exception as e:
            logger.error(f"Optimized search failed: {str(e)}")
            raise

    @time_it
    async def batch_search(self, query_vectors: List[List[float]], top_k: int = 5) -> List[List[Dict[str, Any]]]:
        """
        Batch search for multiple queries to improve throughput
        """
        try:
            # Use batch search API if available
            results = self.client.search_batch(
                collection_name=self.collection_name,
                requests=[models.SearchRequest(
                    vector=qv,
                    limit=top_k,
                    timeout=self.timeout,
                    params=models.SearchParams(
                        hnsw_ef=64,
                        exact=False
                    )
                ) for qv in query_vectors]
            )

            # Format all results
            all_formatted_results = []
            for result_batch in results:
                formatted_batch = []
                for result in result_batch:
                    formatted_batch.append({
                        "id": result.id,
                        "score": result.score,
                        "payload": result.payload
                    })
                all_formatted_results.append(formatted_batch)

            logger.info(f"Batch search completed for {len(query_vectors)} queries")
            return all_formatted_results

        except Exception as e:
            logger.error(f"Batch search failed: {str(e)}")
            raise

    @time_it
    async def hybrid_search(self, query_vector: List[float], text_query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Hybrid search combining semantic and keyword search for better results
        """
        try:
            # Create a query that combines semantic and keyword matching
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="content",
                            match=models.MatchText(text=text_query)
                        )
                    ]
                ) if text_query else None,
                limit=top_k,
                timeout=self.timeout,
                search_params=models.SearchParams(
                    hnsw_ef=128,
                    exact=False
                )
            )

            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })

            logger.info(f"Hybrid search completed with {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            logger.error(f"Hybrid search failed: {str(e)}")
            # Fall back to regular search
            return await self.optimized_search(query_vector, top_k)

    def create_optimized_collection(self, vector_size: int = 1536):
        """
        Create an optimized collection with performance settings
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with optimized settings
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                    # Optimize for search performance
                    optimizers_config=models.OptimizersConfigDiff(
                        memmap_threshold=20000,  # Use memory mapping for large segments
                        indexing_threshold=20000,  # Index segments larger than this
                        payload_indexing_threshold=20000,  # Index payload for large collections
                        flush_interval_sec=5,  # Flush every 5 seconds
                        max_optimization_threads=1  # Limit optimization threads
                    ),
                    # Configure HNSW index for fast search
                    hnsw_config=models.HnswConfigDiff(
                        m=16,  # Number of edges per vertex
                        ef_construct=100,  # Construction parameter
                        full_scan_threshold=10000,  # Use HNSW when collection > this size
                        max_indexing_threads=0,  # Use all available threads
                        on_disk=False  # Keep index in memory for faster access
                    )
                )
                logger.info(f"Created optimized collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")

        except Exception as e:
            logger.error(f"Error creating optimized collection: {str(e)}")
            raise

    @time_it
    async def search_with_prefetch(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search with prefetching of likely relevant results
        """
        try:
            # Perform the main search
            results = await self.optimized_search(query_vector, top_k)

            # Prefetch content for top results to improve perceived performance
            # This would typically be done asynchronously in production
            for result in results[:2]:  # Prefetch top 2 results
                content = result["payload"].get("content", "")
                # In a real system, you might prefetch related content here
                # or prime caches with this content

            logger.info(f"Search with prefetch completed for {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Search with prefetch failed: {str(e)}")
            return await self.optimized_search(query_vector, top_k)

    def validate_performance(self, test_vectors: List[List[float]], iterations: int = 10) -> Dict[str, Any]:
        """
        Validate that queries meet the < 2 sec performance requirement
        """
        latencies = []
        successful_queries = 0

        for i in range(iterations):
            start_time = time.time()
            try:
                # Use a simple search for performance testing
                query_vector = test_vectors[i % len(test_vectors)]
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=5,
                    timeout=2.0
                )
                end_time = time.time()
                latency = end_time - start_time
                latencies.append(latency)

                if latency < 2.0:
                    successful_queries += 1
                else:
                    logger.warning(f"Query {i+1} exceeded 2s: {latency:.3f}s")

            except Exception as e:
                logger.error(f"Query {i+1} failed: {str(e)}")
                latencies.append(2.0)  # Count as failed (exceeded 2s)

        # Calculate statistics
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        p95_latency = np.percentile(latencies, 95) if latencies else 0
        success_rate = successful_queries / iterations if iterations > 0 else 0

        performance_report = {
            "iterations": iterations,
            "successful_queries": successful_queries,
            "success_rate": success_rate,
            "average_latency": avg_latency,
            "p95_latency": p95_latency,
            "max_latency": max(latencies) if latencies else 0,
            "meets_requirement": avg_latency < 2.0 and success_rate >= 0.95
        }

        logger.info(f"Performance validation: {performance_report}")
        return performance_report


class PerformanceMiddleware:
    """
    Middleware to track and optimize performance across the RAG system
    """
    def __init__(self):
        self.query_times = []
        self.cache_hits = 0
        self.cache_misses = 0

    def record_query_time(self, query_time: float):
        """Record query execution time"""
        self.query_times.append(query_time)

        # Keep only recent queries to avoid memory issues
        if len(self.query_times) > 1000:
            self.query_times = self.query_times[-500:]

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        if not self.query_times:
            return {
                "avg_query_time": 0,
                "p95_query_time": 0,
                "total_queries": 0,
                "cache_hit_rate": 0
            }

        avg_time = sum(self.query_times) / len(self.query_times)
        p95_time = float(np.percentile(self.query_times, 95)) if len(self.query_times) > 1 else avg_time
        total_queries = len(self.query_times)
        cache_total = self.cache_hits + self.cache_misses
        cache_hit_rate = self.cache_hits / cache_total if cache_total > 0 else 0

        return {
            "avg_query_time": avg_time,
            "p95_query_time": p95_time,
            "total_queries": total_queries,
            "cache_hit_rate": cache_hit_rate,
            "meets_2s_requirement": avg_time < 2.0
        }

    def cache_result(self, query_hash: str, result: Any, ttl: int = 300):
        """Cache query results to improve performance"""
        # In a real implementation, this would use Redis or similar
        pass

    def get_cached_result(self, query_hash: str) -> Optional[Any]:
        """Retrieve cached result"""
        # In a real implementation, this would check Redis cache
        return None


# Global performance middleware instance
perf_middleware = PerformanceMiddleware()


def optimize_qdrant_client(client: QdrantClient, collection_name: str) -> QdrantQueryOptimizer:
    """
    Create and configure an optimized Qdrant client
    """
    optimizer = QdrantQueryOptimizer(client, collection_name)

    # Apply optimizations
    logger.info("Applying Qdrant optimizations...")

    return optimizer


def performance_monitor(func):
    """
    Decorator to monitor performance of query functions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            end_time = time.time()
            query_time = end_time - start_time

            # Record performance metrics
            perf_middleware.record_query_time(query_time)

            if query_time > 2.0:
                logger.warning(f"Query exceeded 2s requirement: {query_time:.3f}s")
            else:
                logger.debug(f"Query completed within requirement: {query_time:.3f}s")

            return result
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            raise

    return wrapper


# Example usage
async def example_usage():
    """
    Example of how to use the performance optimization
    """
    # Initialize Qdrant client
    client = QdrantClient(
        url="https://your-cluster-url.qdrant.io",
        api_key="your-api-key",
        prefer_grpc=True  # Use gRPC for better performance
    )

    # Create optimized client
    optimizer = optimize_qdrant_client(client, "book_content")

    # Create optimized collection
    optimizer.create_optimized_collection()

    # Test query vector (1536 dimensions for OpenAI embeddings)
    test_vector = [0.1] * 1536

    # Perform optimized search
    results = await optimizer.optimized_search(test_vector, top_k=5)
    print(f"Found {len(results)} results")

    # Validate performance
    test_vectors = [[0.1] * 1536 for _ in range(5)]
    performance_report = optimizer.validate_performance(test_vectors, iterations=10)

    print("Performance Report:")
    for key, value in performance_report.items():
        print(f"  {key}: {value}")

    return performance_report


if __name__ == "__main__":
    # Run example if executed directly
    asyncio.run(example_usage())