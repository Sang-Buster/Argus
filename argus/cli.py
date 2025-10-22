"""CLI wrapper for argus_cli.py in the root directory."""

import sys
from pathlib import Path

# Add project root to path so we can import argus_cli
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from argus_cli import main  # noqa: E402

__all__ = ["main"]
