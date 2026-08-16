# <img src='icon.png' card_color='#40A0DB' width='50' height='50' style='vertical-align:bottom'/> Morse Code

Encodes text to International Morse Code, played as generated audible
beeps - "how do you say SOS in morse" beeps out `... --- ...`. Same
generated-audio philosophy as
[ovos-skill-metronome](https://github.com/andlo/ovos-skill-metronome)/
[ovos-skill-tuning-fork](https://github.com/andlo/ovos-skill-tuning-fork):
nothing recorded, nothing to source or license.

[![Tests](https://github.com/andlo/ovos-skill-morse-code/actions/workflows/test.yml/badge.svg)](https://github.com/andlo/ovos-skill-morse-code/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/ovos-skill-morse-code.svg)](https://pypi.org/project/ovos-skill-morse-code/)

## Usage
```
"how do you say SOS in morse code"
"play hello world in morse"
"hvordan siger man SOS på morse"    (Danish)
```

## Decode (morse -> text) is not implemented

This skill only *encodes* (text -> beeps). Decoding would require the
user to speak something like "dot dot dot dash dash dash dot dot dot"
and have that reliably transcribed by STT into literal "dot"/"dash"
words - a much less reliable path than encoding, and arguably a
different feature entirely, not a small addition. Left out of this
release rather than built on shaky ground.

## Timing

Standard relative Morse timing units (dash = 3× a dot, gap between
characters = 3× a dot, gap between words = 7× a dot), but a fixed,
short dot duration rather than trying to match a specific "words per
minute" telegraphy convention - the goal is a clearly recognizable
representation, not amateur-radio-accurate speed.

## Install
```bash
pip install ovos-skill-morse-code
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md).

## Category
**Utility**

## Tags
#morse-code #novelty #ham-radio
