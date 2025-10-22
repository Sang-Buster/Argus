"""
Argus: A UAV Remote ID Spoofing Defense System

A research framework for simulating UAV swarms, injecting spoofing attacks,
and evaluating graph-theoretic and cryptographic defense mechanisms.
"""

__version__ = "0.1.0"
__author__ = "Sang Xing"

# Expose main classes for convenient imports
from argus.core.remote_id import RemoteIDMessage
from argus.core.swarm import Swarm
from argus.core.uav import UAV

__all__ = [
    "Swarm",
    "UAV",
    "RemoteIDMessage",
    "__version__",
]
