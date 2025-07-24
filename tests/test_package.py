from __future__ import annotations

import importlib.metadata

import estimark as m


def test_version() -> None:
    assert importlib.metadata.version("estimark") == m.__version__
