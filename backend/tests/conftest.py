import sys
import os

# Make sure the backend package root is on sys.path so imports resolve
# when running pytest from the repository root or from backend/.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
