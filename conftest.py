"""
Global pytest configuration.

Ensures the repository root is available on sys.path so imports such as
`python.dashboard_engine...` resolve consistently regardless of the
working directory.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
