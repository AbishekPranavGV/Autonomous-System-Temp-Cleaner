import sys
from pathlib import Path

# Add parent directory to path so app can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app

# Vercel WSGI entry point
handler = app
