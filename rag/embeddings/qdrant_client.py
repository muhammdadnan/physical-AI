from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import logging
from ..config import Config

logger = logging.getLogger(__name__)

class QdrantEmbeddingStore:
    """
    Qdrant vector storage for book content
    """
    def __init__(self):
        # Initialize Qdrant client
        if Config.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY,
                prefer_grpc=True
            )
        else:
            self.client = QdrantClient(host="localhost", port=6333)

        # Collection name for book content
        self.collection_name = "book_content"

        # Initialize the collection if it doesn't exist
        self._init_collection()

    def _init_collection(self):
        """Initialize the Qdrant collection for book content"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector size for OpenAI embeddings (1536 for text-embedding-ada-002)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    def store_embeddings(self, points: List[Dict[str, Any]]):
        """Store embeddings in Qdrant"""
        try:
            # Prepare points for insertion
            qdrant_points = []
            for point in points:
                qdrant_points.append(
                    models.PointStruct(
                        id=point["id"],
                        vector=point["vector"],
                        payload=point["metadata"]
                    )
                )

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points
            )
            logger.info(f"Stored {len(points)} embeddings in Qdrant")
        except Exception as e:
            logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise

    def search_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar content in Qdrant"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })

            logger.info(f"Found {len(formatted_results)} similar results")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {str(e)}")
            raise