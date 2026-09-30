"""OCP: "play hello world in morse" is taken by the OCP pipeline before
padatious, so the skill answers OCP's search (#2)."""
import pytest
from ovos_utils.ocp import MediaType, PlaybackType

import morse_skill as mc


@pytest.fixture(autouse=True)
def _setup(monkeypatch, tmp_path):
    monkeypatch.setattr(mc.MorseCode, "_auto_register_entity_files",
                        lambda *a, **k: None, raising=False)
    monkeypatch.setattr(mc, "CACHE_DIR", tmp_path)


@pytest.mark.parametrize("phrase,text", [
    ("hello world in morse", "hello world"),
    ("sos in morse code", "sos"),
])
def test_search_answers_morse(skill, phrase, text):
    [r] = skill.search_morse(phrase, MediaType.MUSIC)
    assert r.uri.startswith("file://") and r.uri.endswith(f"morse_{text.replace(' ', '_')}.wav")
    assert r.match_confidence == 100 and r.playback == PlaybackType.AUDIO
    assert r.media_type == MediaType.MUSIC


@pytest.mark.parametrize("phrase", [
    "morse code by some band",
    "in morse",
    "hello world",
    "",
])
def test_search_ignores_other_phrases(skill, phrase):
    assert skill.search_morse(phrase, MediaType.MUSIC) == []


def test_search_danish(skill, monkeypatch):
    monkeypatch.setattr(mc.MorseCode, "lang", "da-dk", raising=False)
    [r] = skill.search_morse("hej med dig på morse kode", MediaType.AUDIO)
    assert r.title == "hej med dig (morse)"
