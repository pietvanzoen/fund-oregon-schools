"""Only the transcript helpers are tested: the download and transcription shell out to programs that run in
GitHub Actions only."""

import unittest

import helpers  # noqa: F401  (puts tools/ on the path)
from save_youtube import LOOP, lines, loops


class Transcript(unittest.TestCase):
    def test_lines_and_loops(self):
        segs = [{"start": 3725.6, "text": " Good morning. "}, {"start": 3730, "text": "  "}]
        assert lines(segs) == ["1:02:05 Good morning."]
        segs += [{"start": 3731 + i, "text": "And so we can do that."} for i in range(LOOP)]
        segs += [{"start": 3800, "text": "Adjourned."}, {"start": 3801, "text": "Adjourned."}]
        assert loops(segs) == [(3731, LOOP, "And so we can do that.")]
        stuck = "Mr. Richardson, " * 6
        segs += [
            {"start": 3900, "text": stuck},
            {"start": 3903, "text": stuck},
            {"start": 3910, "text": "Thank you, chair."},
        ]
        assert loops(segs) == [(3731, LOOP, "And so we can do that."), (3900, 2, stuck.strip())]


if __name__ == "__main__":
    unittest.main()
