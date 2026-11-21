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
        assert r.returncode == 0 and "1 warnings" in r.stdout and "pending (queued" in r.stdout, r.stdout
        open(f"{root}/analysis/b.md", "w").write("Bad [SRC:gov/nope.pdf p.1] [NEWS:NEWS-404]\n")
        open(f"{root}/analysis/c.csv", "w").write("year,amount,source\n2027,1,\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 3, r.stdout
        os.remove(f"{root}/analysis/b.md")
        os.remove(f"{root}/analysis/c.csv")

        # glossary warning (rule 11): unknown abbreviations warn; glossary terms, "(XYZ)" and tags don't
        open(f"{root}/analysis/glossary.csv", "w").write(
            "term,full_name,kind,tooltip,definition,source\nSSF,State School Fund,acronym,t,d,[NEWS:NEWS-1]\n")
        open(f"{root}/analysis/g.md", "w").write(
            "The SSF and the QEM and ADMr. Written out: National Center (NCES). PDF.\n`ABC` [SRC:gov/test_page.html]\n"
            'The bill names "Representative WRIGHT".\n')
        r = run(root, "check_citations.py")
        assert r.returncode == 0 and r.stdout.count("glossary.csv") == 2, r.stdout
        assert "QEM isn't in" in r.stdout and "ADMr isn't in" in r.stdout, r.stdout
        os.remove(f"{root}/analysis/g.md")
        os.remove(f"{root}/analysis/glossary.csv")

        # derived figures, DER tags, topic sections, the BRIEFING marker and the number warning
        os.makedirs(f"{root}/analysis/derived")
        os.makedirs(f"{root}/analysis/topics")
        open(f"{root}/analysis/derived/t.csv", "w").write(
            "id,value,unit,kind,label,method,inputs,assumptions\n"
            "n,22110,students,derived,Students,sum,data/x.csv,\n"
            "share,3.97,percent,derived,Share,n / state total,data/x.csv,\n"
            "est,256.6,USD millions,est,Money,sum of x * y,data/x.csv,y is an average\n")
        open(f"{root}/analysis/topics/ok.md", "w").write(
            "# OK topic\n\nIntro.\n\n## What the sources say\n\n- The fund is $13 billion\n  [SRC:gov/test_page.html].\n\n"
            "| Bill | Fund |\n|---|---|\n| State | $13 billion [SRC:gov/test_page.html] |\n\n"
            "## Derived figures\n\n| Figure | Value |\n|---|---|\n| Money | about $257M [DER:t/est] |\n\n"
            "## Analysis\n\nAbout 22,100 students, about 4% (our sum [DER:t/n] [DER:t/share]).\n")
        open(f"{root}/analysis/BRIEFING.md", "w").write(
            "Enrolled about 22,100 students (our sum [DER:t/n]).\n| Money | ~257 | our estimate [DER:t/est] |\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 0 and "0 errors" in r.stdout and "not in the text" not in r.stdout, r.stdout
        r = run(root, "linkify.py", f"{root}/analysis/BRIEFING.md")
        assert "[DER:t/n](https://github.com/pietvanzoen/fund-oregon-schools/blob/main/analysis/derived/t.csv)" \
            in r.stdout, r.stdout

        open(f"{root}/analysis/BRIEFING.md", "w").write(
            "Enrolled about 22,200 students (our sum [DER:t/n]). About $257M of it [DER:t/est].\n"
            "Unknown [DER:t/nope] and [DER:zz/n].\n")
        open(f"{root}/analysis/topics/bad.md", "w").write(
            "# Bad\n\n## What the sources say\n\n- No citation here.\n- Analysis: inference [SRC:gov/test_page.html].\n"
            "- It is $14 billion [SRC:gov/test_page.html].\n\n## Derived figures\n\n## Analysis\n")
        open(f"{root}/analysis/topics/order.md", "w").write("# O\n\n## Analysis\n\n## Derived figures\n")
        open(f"{root}/analysis/derived/u.csv", "w").write(
            "id,value,unit,kind,label,method,inputs,assumptions\nx,abc,USD,guess,X,m,i,\n")
        open(f"{root}/analysis/derived/v.csv", "w").write("id,value\nx,1\n")
        r = run(root, "check_citations.py")
        out = r.stdout
        assert r.returncode == 1 and out.count("ERROR") == 10, out
        assert "BRIEFING.md:1: [DER:t/n] is 22110 students; no number" in out, out  # 22,200 is not 22110 rounded
        assert "BRIEFING.md:1: [DER:t/est] needs \"our sum\" or \"our estimate\"" in out, out
        assert "unknown derived figure t/nope" in out and "unknown derived figure zz/n" in out, out
        assert "bad.md:5: line under \"What the sources say\" has no source citation" in out, out
        assert "bad.md:6: \"Analysis:\" under" in out and "order.md: needs exactly these sections" in out, out
        assert "u.csv:2: kind must be derived or est" in out and "u.csv:2: value 'abc' is not a number" in out, out
        assert "v.csv: columns must be" in out, out
        assert "warn  analysis/topics/bad.md:7: 14 is not in the text" in out, out
        shutil.rmtree(f"{root}/analysis/derived")
        shutil.rmtree(f"{root}/analysis/topics")
        os.remove(f"{root}/analysis/BRIEFING.md")

        r = run(root, "linkify.py", f"{root}/analysis/a.md")
        assert f"[SRC:gov/test_page.html]({url})" in r.stdout, r.stdout
        assert "[NEWS:NEWS-1](https://e.x/a)" in r.stdout and f"({url}/x#page=2)" in r.stdout, r.stdout

        r = run(root, "search.py", "school fund", "--kind", "src")
        assert "[SRC:gov/test_page.html]" in r.stdout, r.stdout + r.stderr
        r = run(root, "doc.py", "test_page", "--grep", "billion")
        assert "13 billion" in r.stdout, r.stdout + r.stderr
        r = run(root, "check_sources.py")
        assert r.returncode == 0 and "0 errors" in r.stdout, r.stdout
        q3 = open(f"{root}/sources/_queue.csv").read()
        open(f"{root}/sources/_queue.csv", "w").write(
            q3 + "https://www.opb.org/article/x/,gov/news_copy.html,News,,gov,\n"
                 "https://www.oregon.gov/x.pdf,misc/x.pdf,Bad folder,,gov,\n")
        open(f"{root}/sources/gov/hand_added.pdf", "w").write("x")
        r = run(root, "check_sources.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 3, r.stdout
        assert "news site" in r.stdout and "must start with" in r.stdout and "no line in" in r.stdout, r.stdout
        open(f"{root}/sources/_queue.csv", "w").write(q3)
        os.remove(f"{root}/sources/gov/hand_added.pdf")

        print("all tool tests passed")
    finally:
        srv.shutdown()
        shutil.rmtree(root)


if __name__ == "__main__":
    main()
