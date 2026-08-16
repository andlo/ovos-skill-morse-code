"""
skill OVOS MorseCode
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

SKELETON ONLY - not implemented yet.

Encodes/decodes text to and from Morse code, played as audible beeps. 'How do you say SOS in Morse' -> beeps out ... --- .... Niche but fully deterministic - a fixed character-to-signal lookup table, no ambiguity, appeals to the ham-radio/hobbyist crowd.

See README.md ("Why this exists") and DEVELOPMENT.md ("Design notes")
before starting real implementation - several open design questions
are noted there and should be resolved (ideally reviewed) before
writing the real intent logic, same process ovos-skill-convert and
ovos-skill-sound-like followed.
"""

from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler


class MorseCode(OVOSSkill):

    def initialize(self):
        # TODO: not implemented yet - see README.md and DEVELOPMENT.md
        pass

    @intent_handler("not_implemented.intent")
    def handle_not_implemented(self, message):
        """Placeholder so the skill installs and loads cleanly while
        real implementation is still pending."""
        self.speak_dialog("not_implemented_yet")
