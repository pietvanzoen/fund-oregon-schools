"""Shared setup for the tool tests: a throwaway archive root and a local HTTP server for the fetcher."""

import csv
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)  # so tests can import tools' functions
PAGE_13 = b"<html><body><nav>menu</nav><h1>Budget</h1><p>State School Fund: $13 billion.</p></body></html>"
PAGE = {"body": PAGE_13}
FLAKY = {"left": 0}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
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


def run(root, *args, **env):
    env = (
        dict(
            os.environ,
            FOS_ROOT=root,
            NO_PROXY="127.0.0.1,localhost",
            no_proxy="127.0.0.1,localhost",
            FOS_RETRY_DELAY="0",
            FOS_REQUEST_DELAY="0",
            GITHUB_ACTIONS="",
            GITHUB_STEP_SUMMARY="",
        )
        | env
    )
    return subprocess.run(
        [sys.executable, os.path.join(TOOLS, args[0]), *args[1:]], env=env, capture_output=True, text=True, check=False
    )


class ArchiveTest(unittest.TestCase):
    """Each test gets its own root with a queue, a news record, and (unless fetch = False) gov/test_page.html
    fetched from the local server, saying "State School Fund: $13 billion."."""

    fetch = True

    def setUp(self):
        srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        self.url = f"http://127.0.0.1:{srv.server_port}/page"
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        PAGE["body"], FLAKY["left"] = PAGE_13, 0
        self.write(
            "sources/_queue.csv",
            f"url,path,title,date,kind,notes\n{self.url},gov/test_page.html,Test,2026-11-19,gov,\n"
            f"{self.url}/x,gov/not_fetched.pdf,Later,,gov,\n",
        )
        news = {
            "id": "NEWS-1",
            "date": "2026-11-19",
            "outlet": "X",
            "title": "T",
            "url": "https://e.x/a",
            "summary": "s",
        }
        self.write("sources/news/index.jsonl", json.dumps(news) + "\n")
        self.write("analysis/people/quotes_all.jsonl", "")
        if self.fetch:
            r = self.run_tool("fetch_sources.py", "--only", "gov/test")
            assert r.returncode == 0, r.stderr

    def write(self, rel, text, mode="w"):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, mode, encoding="utf-8") as f:
            f.write(text)
        return path

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as f:
            return f.read()

    def run_tool(self, *args, **env):
        return run(self.root, *args, **env)

    def derive(self, topic):
        """Run tools/derive_<topic>.py on this root; return its rows by id, with values as floats."""
        os.makedirs(f"{self.root}/analysis/derived", exist_ok=True)
        r = self.run_tool(f"derive_{topic}.py")
        assert r.returncode == 0, r.stderr
        with open(f"{self.root}/analysis/derived/{topic}.csv", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        assert list(rows[0]) == ["id", "value", "unit", "kind", "label", "method", "inputs", "assumptions"], rows[0]
        assert len({r["id"] for r in rows}) == len(rows), "ids must be unique"
        assert all(r["kind"] in ("derived", "est") for r in rows), rows
        return {r["id"]: dict(r, value=float(r["value"])) for r in rows}
