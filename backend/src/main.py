from fastapi import FastAPI
from .api.vla_overview import register_routes as register_vla_routes
from .api.voice import register_routes as register_voice_routes
from .api.planning import register_routes as register_planning_routes
from .api.actions import register_routes as register_actions_routes
from .api.vision import register_routes as register_vision_routes
from .api.integrated_workflow import register_routes as register_integrated_routes
from .api.capstone import register_routes as register_capstone_routes
from .db.database import init_db
from .logging_config import setup_logging
from .config import Config
from .security import setup_security_headers, initialize_security

# Setup logging
setup_logging()

# Validate configuration
Config.validate()

# Initialize security
try:
    initialize_security(Config)
    print("Security initialized successfully")
except Exception as e:
    print(f"Warning: Error initializing security: {e}")

app = FastAPI(title="VLA Robotics API", version="1.0.0")

# Setup security headers
setup_security_headers(app)

# Initialize database
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error initializing database: {e}")

# Register API routes
register_vla_routes(app)
register_voice_routes(app)
register_planning_routes(app)
register_actions_routes(app)
register_vision_routes(app)
register_integrated_routes(app)
register_capstone_routes(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the VLA Robotics API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return {"message": "No favicon"}

# Additional API endpoints will be added as we implement the VLA system