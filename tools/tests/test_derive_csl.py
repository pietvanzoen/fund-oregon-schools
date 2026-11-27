"""derive_csl.py reads no data files: every input is a constant copied from a source, so a value test would only
restate those constants. This checks the script runs and writes a well-formed file (helpers.ArchiveTest.derive)."""

import unittest

from helpers import ArchiveTest


class DeriveCsl(ArchiveTest):
    fetch = False

    def test_runs(self):
        rows = self.derive("csl")
        assert set(rows) == {"sia_seia_2027_29", "sia_seia_minus_non_ssf", "core_grants_cat"}, rows


if __name__ == "__main__":
    unittest.main()
