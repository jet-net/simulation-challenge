from __future__ import annotations

import importlib.metadata

import cookiecutter_test as m


def test_version():
    assert importlib.metadata.version("cookiecutter_test") == m.__version__
