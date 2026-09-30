"""
skill OVOS Morse Code
Copyright (C) 2026  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

---

Encodes text to International Morse Code, played as generated audible
beeps - "how do you say SOS in morse" beeps out ... --- ... . Same
generated-audio philosophy as ovos-skill-metronome/ovos-skill-tuning-
fork: nothing recorded, nothing to source or license, everything
built from a sine tone and precise silence gaps.

DECODE (morse -> text) IS NOT IMPLEMENTED
------------------------------------------------
This skill only ENCODES (text -> beeps). Decoding would require the
user to speak something like "dot dot dot dash dash dash dot dot dot"
and have that reliably transcribed by STT into literal "dot"/"dash"
words - a much less reliable path than encoding, and arguably a
different feature (parsing spoken morse-as-words) rather than a small
addition. Left out of this release rather than built on shaky ground.

TIMING
------
Uses standard relative Morse timing units (dot = 1 unit, dash = 3
units, gap within a character's own dots/dashes = 1 unit, gap between
characters = 3 units, gap between words = 7 units), but a fixed dot
duration (DOT_MS) rather than trying to hit a specific "words per
minute" convention real telegraphy uses - the goal here is a clearly
recognizable representation, not amateur-radio-accurate speed.
"""

import math
import re
import struct
import tempfile
import wave
from pathlib import Path

from ovos_utils.ocp import MediaEntry, MediaType, PlaybackType
from ovos_workshop.decorators import intent_handler
from ovos_workshop.decorators.ocp import ocp_search
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill

SAMPLE_RATE = 44100
TONE_FREQUENCY = 600  # Hz - standard-ish CW practice tone
DOT_MS = 80
DASH_MS = DOT_MS * 3
INTRA_CHAR_GAP_MS = DOT_MS       # gap between dots/dashes of the SAME character
INTER_CHAR_GAP_MS = DOT_MS * 3   # gap between characters
INTER_WORD_GAP_MS = DOT_MS * 7   # gap between words

CACHE_DIR = Path(tempfile.gettempdir()) / "ovos-skill-morse-code"

MORSE_CODE = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".",
    "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---",
    "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-",
    "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--",
    "z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}


def text_to_morse(text):
    """Returns a list of morse patterns (e.g. ['...', '---', '...']
    for 'SOS'), one per character, skipping any character not in
    MORSE_CODE (punctuation etc). A space in the input becomes a
    literal 'WORD_GAP' marker in the returned list, so the caller can
    tell "gap between letters" from "gap between words" apart."""
    patterns = []
    for char in text.lower():
        if char == " ":
            patterns.append("WORD_GAP")
        elif char in MORSE_CODE:
            patterns.append(MORSE_CODE[char])
    return patterns


def _append_tone(frames, duration_ms, freq=TONE_FREQUENCY, sample_rate=SAMPLE_RATE):
    n = int(sample_rate * duration_ms / 1000)
    fade_n = max(1, int(n * 0.1))  # short fade in/out avoids clicks between beeps
    for i in range(n):
        t = i / sample_rate
        amp = 0.6
        if i < fade_n:
            amp *= i / fade_n
        elif i > n - fade_n:
            amp *= (n - i) / fade_n
        sample = amp * math.sin(2 * math.pi * freq * t)
        frames.append(struct.pack("<h", int(sample * 32767)))


def _append_silence(frames, duration_ms, sample_rate=SAMPLE_RATE):
    n = int(sample_rate * duration_ms / 1000)
    frames.extend([struct.pack("<h", 0)] * n)


def _generate_morse_wav(path, patterns, sample_rate=SAMPLE_RATE):
    frames = []
    for i, pattern in enumerate(patterns):
        if pattern == "WORD_GAP":
            _append_silence(frames, INTER_WORD_GAP_MS, sample_rate)
            continue
        for j, symbol in enumerate(pattern):
            _append_tone(frames, DOT_MS if symbol == "." else DASH_MS, sample_rate=sample_rate)
            if j < len(pattern) - 1:
                _append_silence(frames, INTRA_CHAR_GAP_MS, sample_rate)
        if i < len(patterns) - 1 and patterns[i + 1] != "WORD_GAP":
            _append_silence(frames, INTER_CHAR_GAP_MS, sample_rate)
    with wave.open(str(path), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(b"".join(frames))


def _tone_path_for_text(text):
    """Cached by the exact input text, so repeat requests for the
    same word/phrase don't regenerate identical audio."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() else "_" for c in text.lower())[:80]
    path = CACHE_DIR / f"morse_{safe_name}.wav"
    if not path.exists():
        patterns = text_to_morse(text)
        _generate_morse_wav(path, patterns)
    return str(path)


# "play hello world in morse" is taken by the OCP pipeline before
# padatious, so the skill also answers OCP's search (issue #2). The morse
# is a generated wav, so OCP plays the file itself (PlaybackType.AUDIO)
# and handles stop. OCP only asks skills that support the media type it
# guessed, so AUDIO, MUSIC and GENERIC are accepted and the result echoes
# the query's type.
OCP_MEDIA = [MediaType.AUDIO, MediaType.MUSIC, MediaType.GENERIC]
OCP_CONFIDENCE = 100
SKILL_ROOT = Path(__file__).resolve().parent


class MorseCode(OVOSCommonPlaybackSkill):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, supported_media=OCP_MEDIA,
                         skill_icon=str(SKILL_ROOT / "icon.png"), **kwargs)

    def _ocp_text(self, phrase, lang):
        """The text in "hello world in morse (code)" - None unless the
        phrase ends with a morse suffix and has something to encode."""
        text = " ".join(re.findall(r"\w+", (phrase or "").lower()))
        for suffix in sorted(self.voc_list("morse_suffix", lang), key=len, reverse=True):
            suffix = suffix.lower().strip()
            if text.endswith(" " + suffix):
                text = text[: -len(suffix)].strip()
                patterns = text_to_morse(text)
                if patterns and not all(p == "WORD_GAP" for p in patterns):
                    return text
                return None
        return None

    @ocp_search()
    def search_morse(self, phrase, media_type=MediaType.GENERIC):
        text = self._ocp_text(phrase, self.lang)
        if not text:
            return []
        return [MediaEntry(
            uri=f"file://{_tone_path_for_text(text)}",
            title=f"{text} (morse)",
            artist="Morse Code",
            media_type=media_type if media_type in OCP_MEDIA else MediaType.AUDIO,
            playback=PlaybackType.AUDIO,
            match_confidence=OCP_CONFIDENCE,
            skill_icon=self.skill_icon,
            skill_id=self.skill_id,
        )]

    @intent_handler("play_morse.intent")
    def handle_play_morse(self, message):
        text = (message.data.get("text") or "").strip()
        if not text:
            self.speak_dialog("nothing_to_encode")
            return
        patterns = text_to_morse(text)
        if not patterns or all(p == "WORD_GAP" for p in patterns):
            self.speak_dialog("nothing_encodable", {"text": text})
            return
        self.play_audio(_tone_path_for_text(text), instant=True)
