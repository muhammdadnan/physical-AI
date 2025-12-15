import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Qdrant Configuration
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    # Neon Postgres Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # Whisper Configuration
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")

    # LLM Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo")

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    @classmethod
    def validate(cls):
        """Validate that required environment variables are set"""
        required_vars = ['OPENAI_API_KEY']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")