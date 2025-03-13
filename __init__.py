"""
PyGen - Python Project Skeleton Generator
"""

__version__ = "0.1.8"

# Make internal modules available for imports
from ._cli import main
from ._cli_core import CliCore
from ._common_utils import exit_with_code
from ._logger import init_modmaker_cli_logger