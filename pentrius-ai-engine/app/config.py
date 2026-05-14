"""Pentrius AI Engine configuration."""
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

CDE_MAX_SPAWN_CHILDREN = int(os.getenv("CDE_MAX_SPAWN_CHILDREN", "5"))

GEMINI_FAST_MODEL = "gemini-2.0-flash"
GEMINI_QUALITY_MODEL = "gemini-2.0-pro"
