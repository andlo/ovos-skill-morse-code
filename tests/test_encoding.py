"""Tests for text-to-morse encoding logic - pure lookups, no mocking
needed."""
import pytest


def test_sos_is_the_classic_pattern(skill):
    from morse_skill import text_to_morse
    assert text_to_morse("SOS") == ["...", "---", "..."]


def test_lowercase_and_uppercase_produce_same_result(skill):
    from morse_skill import text_to_morse
    assert text_to_morse("sos") == text_to_morse("SOS")


def test_space_becomes_word_gap_marker(skill):
    from morse_skill import text_to_morse
    result = text_to_morse("hi there")
    assert "WORD_GAP" in result


def test_digits_are_encoded(skill):
    from morse_skill import text_to_morse, MORSE_CODE
    assert text_to_morse("5") == [MORSE_CODE["5"]]


def test_unsupported_characters_are_skipped(skill):
    from morse_skill import text_to_morse
    # punctuation not in MORSE_CODE is silently skipped, not a crash
    result = text_to_morse("a!b")
    assert result == [".-", "-..."]


def test_dash_is_three_times_dot_duration():
    from morse_skill import DOT_MS, DASH_MS
    assert DASH_MS == DOT_MS * 3
