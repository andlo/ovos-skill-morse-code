# MorseCode

Encodes/decodes text to and from Morse code, played as audible beeps. 'How do you say SOS in Morse' -> beeps out ... --- .... Niche but fully deterministic - a fixed character-to-signal lookup table, no ambiguity, appeals to the ham-radio/hobbyist crowd.

> **This is a skeleton only - not implemented yet.** Repo, structure,
> and design notes are in place; the actual skill logic hasn't been
> written. See "Design notes" in [DEVELOPMENT.md](DEVELOPMENT.md).

## Why this exists

Nothing like this exists in the OVOS ecosystem yet (checked before starting). Fully deterministic character-lookup, same shape as the NATO alphabet skill - the two share very similar architecture.

## Planned usage (not yet functional)
```
"how do you say SOS in morse code"
"play SOS in morse"
```

## Install

Not yet published to PyPI.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md).

## Category
**Utility**

## Tags
#morse-code #novelty #ham-radio
