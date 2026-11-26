import json
import os
import unittest

from helpers import FLAKY, PAGE, ArchiveTest


class FetchSources(ArchiveTest):
    fetch = False

    def test_fetch_refresh_and_prior(self):
        PAGE["body"] = b"<html><body><nav>menu</nav><h1>Budget</h1><p>State School Fund: $12 billion.</p></body></html>"
        r = self.run_tool("fetch_sources.py", "--only", "gov/test")
        assert r.returncode == 0, r.stderr
        txt = self.read("sources/gov/test_page.html.txt")
        assert "State School Fund" in txt and "menu" not in txt, txt
        man = [json.loads(line) for line in self.read("sources/_manifest.jsonl").splitlines()]
        assert man[0]["path"] == "gov/test_page.html" and len(man[0]["sha256"]) == 64

        r = self.run_tool("fetch_sources.py", "--refresh", "--only", "gov/test")
        assert "unchanged/skipped 1" in r.stdout, r.stdout
        PAGE["body"] = b"<html><body><p>State School Fund: $13 billion.</p></body></html>"
        r = self.run_tool("fetch_sources.py", "--refresh", "--only", "gov/test")
        assert "fetched 1" in r.stdout, r.stdout
        prior = os.listdir(f"{self.root}/sources/gov/_prior")
        assert any(p.endswith(".html") for p in prior), prior
        assert "13 billion" in self.read("sources/gov/test_page.html.txt")
        assert "gov/test_page.html" in self.read("sources/_versions_log.csv")

    def test_retries(self):
        # a 503 that clears on the 2nd attempt is fetched; a 404 fails at once and is reported
        self.write(
            "sources/_queue.csv",
            f"{self.url}/flaky,gov/retry_flaky.html,Flaky,,gov,\n{self.url}/gone,gov/retry_gone.html,Gone,,gov,\n",
            mode="a",
        )
        FLAKY["left"] = 1
        summary = f"{self.root}/summary.md"
        r = self.run_tool("fetch_sources.py", "--only", "gov/retry", GITHUB_STEP_SUMMARY=summary, GITHUB_ACTIONS="true")
        assert r.returncode == 1, (r.stdout, r.stderr)
        assert "fetched 1" in r.stdout and "failed 1" in r.stdout, r.stdout
        assert os.path.exists(f"{self.root}/sources/gov/retry_flaky.html"), r.stderr
        assert "attempt 1 failed (HTTP 503" in r.stderr, r.stderr
        assert "attempt 1 failed (HTTP 404" not in r.stderr, r.stderr  # 404 is not retried
        assert "::error title=Source not fetched::gov/retry_gone.html: HTTP 404" in r.stdout, r.stdout
        assert "`gov/retry_gone.html` | HTTP 404" in self.read("summary.md")


if __name__ == "__main__":
    unittest.main()
