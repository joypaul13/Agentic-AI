"""
Configuration module for Research Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "anthropic"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # For web search

# Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
TEMPERATURE = 0.7
MAX_TOKENS = 4000

# Agent settings
MAX_ITERATIONS = 15
TIMEOUT = 60

# Report settings
REPORT_LENGTH = "detailed"  # "brief", "medium", "detailed"
