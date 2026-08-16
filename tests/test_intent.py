"""Tests for the intent handler and WAV generation/caching -
generation is real (writes actual audio), play_audio() is mocked."""
from pathlib import Path
from unittest.mock import MagicMock

import pytest


def test_handle_play_morse_generates_and_plays(skill):
    skill.play_audio = MagicMock()
    message = MagicMock()
    message.data = {"text": "SOS"}
    skill.handle_play_morse(message)
    skill.play_audio.assert_called_once()
    played_path = skill.play_audio.call_args[0][0]
    assert Path(played_path).exists()


def test_handle_play_morse_empty_input(skill):
    skill.play_audio = MagicMock()
    skill.speak_dialog = MagicMock()
    message = MagicMock()
    message.data = {"text": ""}
    skill.handle_play_morse(message)
    skill.play_audio.assert_not_called()
    skill.speak_dialog.assert_called_once_with("nothing_to_encode")


def test_handle_play_morse_no_encodable_characters(skill):
    skill.play_audio = MagicMock()
    skill.speak_dialog = MagicMock()
    message = MagicMock()
    message.data = {"text": "!!!"}
    skill.handle_play_morse(message)
    skill.play_audio.assert_not_called()
    skill.speak_dialog.assert_called_once_with("nothing_encodable", {"text": "!!!"})


def test_repeat_request_reuses_cached_file(skill):
    skill.play_audio = MagicMock()
    message = MagicMock()
    message.data = {"text": "SOS"}
    skill.handle_play_morse(message)
    first_path = skill.play_audio.call_args[0][0]
    first_mtime = Path(first_path).stat().st_mtime

    skill.handle_play_morse(message)
    second_path = skill.play_audio.call_args[0][0]
    second_mtime = Path(second_path).stat().st_mtime

    assert first_path == second_path
    assert first_mtime == second_mtime


def test_generated_wav_duration_matches_expected_timing():
    """SOS = ... --- ... with standard timing units should produce a
    predictable total duration, not just 'some' audio."""
    import importlib.util
    from pathlib import Path as P
    import wave
    spec = importlib.util.spec_from_file_location(
        "morse_check", P(__file__).resolve().parents[1] / "__init__.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    path = P(__file__).resolve().parent / "_test_sos.wav"
    m._generate_morse_wav(path, m.text_to_morse("SOS"))
    with wave.open(str(path)) as f:
        duration_ms = 1000 * f.getnframes() / f.getframerate()
    path.unlink()

    # S = 3 dots + 2 intra-gaps, O = 3 dashes + 2 intra-gaps, S = same as first S
    # plus 2 inter-character gaps between S-O and O-S
    dot, dash, intra, inter = m.DOT_MS, m.DASH_MS, m.INTRA_CHAR_GAP_MS, m.INTER_CHAR_GAP_MS
    s_duration = 3 * dot + 2 * intra
    o_duration = 3 * dash + 2 * intra
    expected = s_duration + inter + o_duration + inter + s_duration
    assert abs(duration_ms - expected) < 5  # allow for integer sample rounding
