"""Shared pytest fixtures for the morse code skill test suite."""
import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_INIT_PATH = Path(__file__).resolve().parents[1] / "__init__.py"
_spec = importlib.util.spec_from_file_location("morse_skill", _INIT_PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules["morse_skill"] = _module
_spec.loader.exec_module(_module)

MorseCode = _module.MorseCode


@pytest.fixture
def skill(monkeypatch):
    s = MorseCode.__new__(MorseCode)
    s.log = MagicMock()
    s.skill_id = "ovos-skill-morse-code.test"
    s.status = MagicMock()
    s._bus = MagicMock()
    monkeypatch.setattr(MorseCode, "lang", "en-us", raising=False)
    s.res_dir = str(Path(__file__).resolve().parents[1])
    s._lang_resources = {}
    return s
