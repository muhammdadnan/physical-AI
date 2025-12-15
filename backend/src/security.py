"""
Security Hardening for VLA System and Chatbot

This module provides security measures for the VLA system and chatbot,
including input validation, authentication, authorization, and protection
against common vulnerabilities.
"""
import re
import logging
import secrets
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import asyncio

logger = logging.getLogger(__name__)

class SecurityConfig:
    """
    Security configuration for the VLA system
    """
    # JWT Configuration
    JWT_SECRET_KEY = None  # Will be loaded from environment
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

    # Rate limiting
    RATE_LIMIT_REQUESTS = 100  # requests per minute per IP
    RATE_LIMIT_WINDOW = 60  # seconds

    # Input validation
    MAX_INPUT_LENGTH = 10000  # Maximum length for user inputs
    ALLOWED_FILE_EXTENSIONS = {'.txt', '.md', '.mdx', '.pdf', '.docx', '.doc'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    # Security headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;"
    }

    @classmethod
    def load_from_config(cls, config):
        """Load security settings from configuration"""
        cls.JWT_SECRET_KEY = config.JWT_SECRET_KEY or secrets.token_urlsafe(32)
        cls.RATE_LIMIT_REQUESTS = getattr(config, 'RATE_LIMIT_REQUESTS', cls.RATE_LIMIT_REQUESTS)
        cls.MAX_INPUT_LENGTH = getattr(config, 'MAX_INPUT_LENGTH', cls.MAX_INPUT_LENGTH)


class RateLimiter:
    """
    Simple rate limiter to prevent abuse
    """
    def __init__(self):
        self.requests = {}  # ip -> [(timestamp, count), ...]
        self.window_size = SecurityConfig.RATE_LIMIT_WINDOW
        self.max_requests = SecurityConfig.RATE_LIMIT_REQUESTS

    def is_allowed(self, ip: str) -> bool:
        """Check if request from IP is allowed"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_size)

        # Clean old entries
        if ip in self.requests:
            self.requests[ip] = [
                (timestamp, count) for timestamp, count in self.requests[ip]
                if timestamp > window_start
            ]

        # Count requests in current window
        if ip not in self.requests:
            self.requests[ip] = [(now, 1)]
            return True

        current_requests = sum(count for _, count in self.requests[ip])

        if current_requests >= self.max_requests:
            return False

        # Add this request
        if self.requests[ip] and self.requests[ip][-1][0] == now:
            # Same second, increment count
            self.requests[ip][-1] = (now, self.requests[ip][-1][1] + 1)
        else:
            self.requests[ip].append((now, 1))

        return True

    def get_reset_time(self, ip: str) -> Optional[datetime]:
        """Get time when rate limit resets for IP"""
        if ip not in self.requests:
            return None

        now = datetime.utcnow()
        oldest_time = min(timestamp for timestamp, _ in self.requests[ip])
        reset_time = oldest_time + timedelta(seconds=self.window_size)

        return reset_time if reset_time > now else None


class InputValidator:
    """
    Input validation to prevent injection attacks and invalid data
    """
    @staticmethod
    def validate_text_input(text: str) -> bool:
        """Validate text input for safety"""
        if not text or not isinstance(text, str):
            return False

        if len(text) > SecurityConfig.MAX_INPUT_LENGTH:
            return False

        # Check for potential injection patterns
        dangerous_patterns = [
            r'<script',  # XSS
            r'javascript:',  # XSS
            r'on\w+\s*=',  # Event handlers
            r'eval\s*\(',  # Code execution
            r'exec\s*\(',  # Code execution
        ]

        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, text_lower):
                return False

        return True

    @staticmethod
    def validate_file_upload(filename: str, file_size: int) -> bool:
        """Validate file upload"""
        if file_size > SecurityConfig.MAX_FILE_SIZE:
            return False

        # Check file extension
        import os
        _, ext = os.path.splitext(filename.lower())
        if ext not in SecurityConfig.ALLOWED_FILE_EXTENSIONS:
            return False

        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False

        return True

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input to remove dangerous content"""
        if not text:
            return text

        # Remove potential script tags (basic)
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)

        # Remove javascript: and vbscript: protocols
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'vbscript:', '', text, flags=re.IGNORECASE)

        return text


class AuthenticationManager:
    """
    Authentication manager for the VLA system
    """
    def __init__(self):
        self.security = HTTPBearer()
        self.rate_limiter = RateLimiter()

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=SecurityConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SecurityConfig.JWT_SECRET_KEY, algorithm=SecurityConfig.JWT_ALGORITHM)
        return encoded_jwt

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SecurityConfig.JWT_SECRET_KEY, algorithms=[SecurityConfig.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token attempted")
            return None
        except jwt.JWTError as e:
            logger.warning(f"Invalid token: {e}")
            return None

    async def authenticate_request(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate incoming request"""
        # Check rate limit
        client_ip = self._get_client_ip(request)
        if not self.rate_limiter.is_allowed(client_ip):
            reset_time = self.rate_limiter.get_reset_time(client_ip)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "reset_time": reset_time.isoformat() if reset_time else None
                }
            )

        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            # For public endpoints, return None
            return None

        try:
            # Extract token
            scheme, token = auth_header.split(" ")
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme"
                )

            # Verify token
            payload = await self.verify_token(token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )

            return payload

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for proxy headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to client host
        return request.client.host if request.client else "127.0.0.1"


class SecurityMiddleware:
    """
    Security middleware to apply security measures to all requests
    """
    def __init__(self):
        self.auth_manager = AuthenticationManager()
        self.input_validator = InputValidator()

    async def process_request(self, request: Request) -> Dict[str, Any]:
        """Process request for security"""
        # Add security headers
        self._add_security_headers(request)

        # Validate content type for POST requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "").lower()
            if not content_type.startswith(('application/json', 'application/x-www-form-urlencoded', 'multipart/form-data')):
                if content_type:  # Only raise error if content-type was specified
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid content type"
                    )

        # Authenticate request
        auth_result = await self.auth_manager.authenticate_request(request)

        # Validate input data
        if request.method in ["POST", "PUT", "PATCH"]:
            body_bytes = await request.body()
            if body_bytes:
                body_str = body_bytes.decode('utf-8')
                if not self.input_validator.validate_text_input(body_str):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid input data"
                    )

        return {
            "authenticated_user": auth_result,
            "client_ip": self.auth_manager._get_client_ip(request),
            "security_ok": True
        }

    def _add_security_headers(self, request: Request):
        """Add security headers to response (this would be handled by middleware in real app)"""
        pass  # In FastAPI, this would be handled by middleware


class VLAChatbotSecurity:
    """
    Security measures specific to the VLA chatbot
    """
    def __init__(self):
        self.security_middleware = SecurityMiddleware()
        self.input_validator = InputValidator()

    async def validate_chat_input(self, user_input: str) -> Dict[str, Any]:
        """Validate chat input for security"""
        validation_result = {
            "is_valid": True,
            "sanitized_input": user_input,
            "security_issues": []
        }

        # Check for command injection patterns
        command_patterns = [
            r'\|\s*\w+',  # Pipe commands
            r';\s*\w+',   # Semicolon commands
            r'&&\s*\w+',  # AND commands
            r'\|\|',      # OR commands
            r'`.*`',      # Command substitution
            r'\$\(.*\)',  # Command substitution
        ]

        for pattern in command_patterns:
            if re.search(pattern, user_input):
                validation_result["security_issues"].append("Command injection attempt detected")
                validation_result["is_valid"] = False

        # Check for prompt injection patterns
        prompt_injection_patterns = [
            r'Ignore.*previous',  # Ignore previous instructions
            r'Forget.*previous',  # Forget previous instructions
            r'System.*:',        # System message impersonation
            r'<.*>',             # HTML-like tags
        ]

        for pattern in prompt_injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                validation_result["security_issues"].append("Prompt injection attempt detected")
                validation_result["is_valid"] = False

        # Validate length
        if len(user_input) > SecurityConfig.MAX_INPUT_LENGTH:
            validation_result["security_issues"].append("Input too long")
            validation_result["is_valid"] = False

        # Sanitize input
        validation_result["sanitized_input"] = self.input_validator.sanitize_input(user_input)

        return validation_result

    async def validate_voice_input(self, audio_data: str) -> Dict[str, Any]:
        """Validate voice input data"""
        validation_result = {
            "is_valid": True,
            "security_issues": []
        }

        # Check if audio data is properly formatted
        if not audio_data.startswith("data:audio/"):
            validation_result["security_issues"].append("Invalid audio data format")
            validation_result["is_valid"] = False

        # Check for potential data injection in base64
        if "javascript:" in audio_data.lower() or "script" in audio_data.lower():
            validation_result["security_issues"].append("Potential script injection in audio data")
            validation_result["is_valid"] = False

        # Check data size (base64 can be large)
        if len(audio_data) > SecurityConfig.MAX_INPUT_LENGTH * 4:  # Rough estimate
            validation_result["security_issues"].append("Audio data too large")
            validation_result["is_valid"] = False

        return validation_result

    async def validate_image_input(self, image_data: str) -> Dict[str, Any]:
        """Validate image input data"""
        validation_result = {
            "is_valid": True,
            "security_issues": []
        }

        # Check if image data is properly formatted
        if not image_data.startswith("data:image/"):
            validation_result["security_issues"].append("Invalid image data format")
            validation_result["is_valid"] = False

        # Check for potential data injection
        if "javascript:" in image_data.lower() or "script" in image_data.lower():
            validation_result["security_issues"].append("Potential script injection in image data")
            validation_result["is_valid"] = False

        # Check data size
        if len(image_data) > SecurityConfig.MAX_INPUT_LENGTH * 4:  # Rough estimate
            validation_result["security_issues"].append("Image data too large")
            validation_result["is_valid"] = False

        return validation_result


# Global security instances
security_middleware = SecurityMiddleware()
chatbot_security = VLAChatbotSecurity()
auth_manager = AuthenticationManager()


def security_check(func):
    """Decorator to add security checks to API endpoints"""
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request') or (args[0] if args and hasattr(args[0], 'headers') else None)

        if request:
            # Perform security checks
            security_result = await security_middleware.process_request(request)

            # Add security result to kwargs for use in the function
            kwargs['security_context'] = security_result

        return await func(*args, **kwargs)
    return wrapper


# Example usage in API endpoints
async def example_secure_endpoint(request: Request):
    """
    Example of how to use security in an endpoint
    """
    # Security is automatically applied via middleware in FastAPI
    security_result = await security_middleware.process_request(request)

    if not security_result["security_ok"]:
        raise HTTPException(status_code=401, detail="Security check failed")

    # Process authenticated user if present
    user = security_result["authenticated_user"]
    if user:
        print(f"Request from authenticated user: {user.get('sub', 'unknown')}")

    return {"message": "Secure endpoint accessed successfully", "user": user}


def setup_security_headers(app):
    """
    Setup security headers for FastAPI app
    """
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)

        # Add security headers
        for header, value in SecurityConfig.SECURITY_HEADERS.items():
            response.headers[header] = value

        # Remove server header to hide server information
        response.headers.pop("server", None)

        return response


# Initialize security configuration
def initialize_security(config):
    """
    Initialize security with configuration
    """
    SecurityConfig.load_from_config(config)
    logger.info("Security configuration initialized")


if __name__ == "__main__":
    # Example usage
    print("Security module loaded successfully")
    print(f"Security headers configured: {len(SecurityConfig.SECURITY_HEADERS)} headers")