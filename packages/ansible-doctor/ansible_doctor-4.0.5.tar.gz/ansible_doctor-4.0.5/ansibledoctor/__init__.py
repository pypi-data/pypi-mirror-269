"""Provide version information."""

__version__ = "4.0.5"

import sys

try:
    import ansible  # noqa
except ImportError:
    sys.exit("ERROR: Python requirements are missing: 'ansible-core' not found.")
