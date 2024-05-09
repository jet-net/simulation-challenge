from __future__ import annotations

import importlib.metadata

import simulation_challenge as m


def test_version():
    assert importlib.metadata.version("simulation_challenge") == m.__version__
