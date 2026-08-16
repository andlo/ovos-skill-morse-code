# Development

## Setup
```bash
git clone https://github.com/andlo/ovos-skill-morse-code.git
cd ovos-skill-morse-code
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -r requirements-test.txt
```

## Running tests
```bash
pytest tests/ -v
```
`tests/test_encoding.py` is pure lookup logic, no mocking.
`tests/test_intent.py` covers the actual WAV generation/caching
(real files written to a temp dir) and checks the generated audio's
duration against the expected timing math for "SOS" specifically, not
just that *some* audio got produced.

## Adding morse-to-text decoding

Deliberately not implemented (see README). If picked up, the real
design question is how the user would actually SAY morse code to be
decoded - "dot dot dot dash dash dash" relies on STT reliably
transcribing exactly those words in exactly that order, which is a
much less forgiving input surface than free-form encode requests.
Worth sketching a few realistic STT transcription failure modes
before committing to that approach, rather than assuming it'll work.

## Adjusting timing/tone

`TONE_FREQUENCY`, `DOT_MS`, and the derived `DASH_MS`/`*_GAP_MS`
constants are all in `__init__.py`. Changing `DOT_MS` rescales
everything else automatically (dash/gaps are all defined relative to
it).

## Versioning

`version.py` follows `VERSION_MAJOR.VERSION_MINOR.VERSION_BUILD[aVERSION_ALPHA]`.

## Releasing

Releases are tag-triggered (`v*`):
```bash
git add version.py
git commit -m "chore: bump version to 0.0.X"
git tag vX.Y.Z
git push && git push --tags
```
Triggers `.github/workflows/test.yml` then `.github/workflows/publish.yml`
(PyPI via trusted publishing - see `ovos-skill-convert`'s
DEVELOPMENT.md for the one-time PyPI setup needed before the first
tagged release).

## Style / conventions

- License: GPL-3.0-or-later (matches the other `andlo` skill repos).
- `locale/<lang-code>/` layout, `skill.json` inside each locale folder.
- Present design changes for review before implementing.
