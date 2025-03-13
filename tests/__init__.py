"""
Tests for modmaker.
This file is used to modify sys.path to make the modmaker package importable.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)