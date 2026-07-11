import os
from dotenv import load_dotenv

load_dotenv(override=True)

NEO4J_URI = os.environ.get("NEO4J_URI", "").strip()
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "").strip()
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "").strip()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()