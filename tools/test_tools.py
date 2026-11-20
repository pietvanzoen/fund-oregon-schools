#!/usr/bin/env python3
"""Smoke tests for the tools, run against a throwaway repo copy and a local HTTP server.

    python3 tools/test_tools.py
"""
import functools
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = {"body": b"<html><body><nav>menu</nav><h1>Budget</h1><p>State School Fund: $12 billion.</p></body></html>"}


FLAKY = {"left": 0}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path.endswith("/gone"):
            self.send_error(404)
            return
        if self.path.endswith("/flaky") and FLAKY["left"] > 0:
            FLAKY["left"] -= 1
            self.send_error(503)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAGE["body"])

    def log_message(self, *a):
        pass


def run(root, *args):
    env = dict(os.environ, FOS_ROOT=root, NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost",
               FOS_RETRY_DELAY="0", FOS_REQUEST_DELAY="0", GITHUB_ACTIONS="", GITHUB_STEP_SUMMARY="")
    return subprocess.run([sys.executable, os.path.join(HERE, args[0]), *args[1:]], env=env,
                          capture_output=True, text=True)


def main():
    srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_port}/page"
    root = tempfile.mkdtemp()
    try:
        os.makedirs(f"{root}/sources/news")
        os.makedirs(f"{root}/analysis/people")
        open(f"{root}/sources/_queue.csv", "w").write(
            f"url,path,title,date,kind,notes\n{url},gov/test_page.html,Test,2026-11-19,gov,\n"
            f"{url}/x,gov/not_fetched.pdf,Later,,gov,\n")
        open(f"{root}/sources/news/index.jsonl", "w").write(json.dumps(
            {"id": "NEWS-1", "date": "2026-11-19", "outlet": "X", "title": "T", "url": "https://e.x/a",
             "summary": "s"}) + "\n")
        open(f"{root}/analysis/people/quotes_all.jsonl", "w").write("")

        r = run(root, "fetch_sources.py", "--only", "gov/test")
        assert r.returncode == 0, r.stderr
        txt = open(f"{root}/sources/gov/test_page.html.txt").read()
        assert "State School Fund" in txt and "menu" not in txt, txt
        man = [json.loads(l) for l in open(f"{root}/sources/_manifest.jsonl")]
        assert man[0]["path"] == "gov/test_page.html" and len(man[0]["sha256"]) == 64

        r = run(root, "fetch_sources.py", "--refresh", "--only", "gov/test")
        assert "unchanged/skipped 1" in r.stdout, r.stdout
        PAGE["body"] = b"<html><body><p>State School Fund: $13 billion.</p></body></html>"
        r = run(root, "fetch_sources.py", "--refresh", "--only", "gov/test")
        assert "fetched 1" in r.stdout, r.stdout
        prior = os.listdir(f"{root}/sources/gov/_prior")
        assert any(p.endswith(".html") for p in prior), prior
        assert "13 billion" in open(f"{root}/sources/gov/test_page.html.txt").read()
        assert "gov/test_page.html" in open(f"{root}/sources/_versions_log.csv").read()

        # retries: a 503 that clears on the 2nd attempt is fetched; a 404 fails at once and is reported
        q = open(f"{root}/sources/_queue.csv").read()
        open(f"{root}/sources/_queue.csv", "w").write(
            q + f"{url}/flaky,gov/retry_flaky.html,Flaky,,gov,\n{url}/gone,gov/retry_gone.html,Gone,,gov,\n")
        FLAKY["left"] = 1
        summary = f"{root}/summary.md"
        env_extra = {"GITHUB_STEP_SUMMARY": summary, "GITHUB_ACTIONS": "true"}
        r = subprocess.run([sys.executable, os.path.join(HERE, "fetch_sources.py"), "--only", "gov/retry"],
                           env={**dict(os.environ, FOS_ROOT=root, NO_PROXY="127.0.0.1,localhost",
                                       no_proxy="127.0.0.1,localhost", FOS_RETRY_DELAY="0",
                                       FOS_REQUEST_DELAY="0"), **env_extra},
                           capture_output=True, text=True)
        assert r.returncode == 1, (r.stdout, r.stderr)
        assert "fetched 1" in r.stdout and "failed 1" in r.stdout, r.stdout
        assert os.path.exists(f"{root}/sources/gov/retry_flaky.html"), r.stderr
        assert "attempt 1 failed (HTTP 503" in r.stderr, r.stderr
        assert "attempt 1 failed (HTTP 404" not in r.stderr, r.stderr  # 404 is not retried
        assert "::error title=Source not fetched::gov/retry_gone.html: HTTP 404" in r.stdout, r.stdout
        assert "`gov/retry_gone.html` | HTTP 404" in open(summary).read()
        q2 = open(f"{root}/sources/_queue.csv").read().replace(
            f"{url}/flaky,gov/retry_flaky.html,Flaky,,gov,\n{url}/gone,gov/retry_gone.html,Gone,,gov,\n", "")
        open(f"{root}/sources/_queue.csv", "w").write(q2)

        open(f"{root}/analysis/a.md", "w").write(
            "Good [SRC:gov/test_page.html] pending [SRC:gov/not_fetched.pdf p.2] news [NEWS:NEWS-1]\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 0 and "1 pending" in r.stdout, r.stdout
        open(f"{root}/analysis/b.md", "w").write("Bad [SRC:gov/nope.pdf p.1] [NEWS:NEWS-404]\n")
        open(f"{root}/analysis/c.csv", "w").write("year,amount,source\n2027,1,\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 3, r.stdout
        os.remove(f"{root}/analysis/b.md")
        os.remove(f"{root}/analysis/c.csv")

        r = run(root, "linkify.py", f"{root}/analysis/a.md")
        assert f"[SRC:gov/test_page.html]({url})" in r.stdout, r.stdout
        assert "[NEWS:NEWS-1](https://e.x/a)" in r.stdout and f"({url}/x#page=2)" in r.stdout, r.stdout

        r = run(root, "search.py", "school fund", "--kind", "src")
        assert "[SRC:gov/test_page.html]" in r.stdout, r.stdout + r.stderr
        r = run(root, "doc.py", "test_page", "--grep", "billion")
        assert "13 billion" in r.stdout, r.stdout + r.stderr
        print("all tool tests passed")
    finally:
        srv.shutdown()
        shutil.rmtree(root)


if __name__ == "__main__":
    main()
