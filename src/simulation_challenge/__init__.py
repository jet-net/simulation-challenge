"""
Copyright (c) 2023 Raghav Kansal. All rights reserved.

simulation-challenge: Jet Simulation Challenge
"""


from __future__ import annotations

from . import data, evaluate, submission
from ._version import version as __version__

__all__ = ["__version__", "data", "evaluate", "submission"]
