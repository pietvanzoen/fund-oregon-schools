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

        # What's new: updates.csv has its own columns (no source); --pr wants a row for a PR touching analysis/
        open(f"{root}/analysis/updates.csv", "w").write(
            "date,text,page,pr,kind\n2026-11-21,Ok,a.md,5,site\nNov 21,,nope.md,x,news\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 5 and "no 'source'" not in r.stdout, r.stdout
        open(f"{root}/analysis/updates.csv", "w").write("date,text,page,pr,kind\n2026-11-21,Ok,a.md,5,research\n")
        git = ["git", "-C", root, "-c", "user.email=t@t", "-c", "user.name=t"]
        subprocess.run(git + ["init", "-q", "-b", "main"], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "base"], check=True)
        subprocess.run(git + ["checkout", "-qb", "pr"], check=True)
        open(f"{root}/RESEARCH.md", "w").write("not under analysis/\n")
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "q"], check=True)
        assert run(root, "check_citations.py", "--pr", "7", "--base", "main").returncode == 0
        open(f"{root}/analysis/a.md", "a").write("More.\n")
        subprocess.run(git + ["commit", "-qam", "a"], check=True)
        r = run(root, "check_citations.py", "--pr", "7", "--base", "main")
        assert r.returncode == 1 and "no row with pr 7" in r.stdout and "analysis/a.md" in r.stdout, r.stdout
        open(f"{root}/analysis/updates.csv", "a").write("2026-11-22,More,a.md,7,correction\n")
        subprocess.run(git + ["commit", "-qam", "row"], check=True)
        assert run(root, "check_citations.py", "--pr", "7", "--base", "main").returncode == 0
        shutil.rmtree(f"{root}/.git")
        os.remove(f"{root}/analysis/updates.csv")
        os.remove(f"{root}/RESEARCH.md")

        # decision files (RESEARCH.md): ids agree across files, a baseline per decision, known statuses
        os.makedirs(f"{root}/analysis/people", exist_ok=True)
        # people.csv area must be on the member page it cites (zero-width spaces ignored); no page, no check
        os.makedirs(f"{root}/sources/legislature/members")
        for m in ("doe", "roe"):
            open(f"{root}/sources/legislature/members/{m}.html", "w").write("x")
            open(f"{root}/sources/legislature/members/{m}.html.txt", "w").write(
                "Democrat - District 22 - N/NE\u200b Portland\n")
        open(f"{root}/analysis/people/people.csv", "w").write(
            "id,name,area,source\nkotek,Tina Kotek,Statewide,[NEWS:NEWS-1]\n"
            "doe,Jane Doe,N/NE Portland,[SRC:legislature/members/doe.html]\n"
            "roe,Ray Roe,North and Northeast Portland,[SRC:legislature/members/roe.html]\n")
        open(f"{root}/analysis/decisions.csv", "w").write(
            "id,decision,decided_by,due,status,related,outcome,outcome_source,source\n"
            "d1,D,Gov,2026-12-01,open,,,,[NEWS:NEWS-1]\nd2,D,Gov,Dec 1,done,zz,,,[NEWS:NEWS-1]\n")
        open(f"{root}/analysis/options.csv", "w").write(
            "id,decision,kind,option,proposed_by,proposed_on,amount,formality,source\n"
            "o1,d1,baseline,B,,,,law,[NEWS:NEWS-1]\no2,nope,idea,X,,,,bill,[NEWS:NEWS-1]\n")
        open(f"{root}/analysis/positions.csv", "w").write(
            "decision,option,actor,date,stance,source,replaces\nd1,,kotek,2026-11,s,[NEWS:NEWS-1],\n"
            "d1,o9,lieber,soon,s,[NEWS:NEWS-404],\nd1,,Portland Public Schools,2026,s,[NEWS:NEWS-1],\n"
            "d1,,kotek,2026-11-06,s,[NEWS:NEWS-1],2\nd1,,kotek,2026-11-06,s,[NEWS:NEWS-1],9\n")
        open(f"{root}/analysis/questions.csv", "w").write(
            "id,question,decision,criterion,asked_by,needed_by,status,answer,issue\n"
            "q1,Q?,d1,c,a parent,2027-01-19,open,,\nq2,Q?,,c,a parent,,answered,,\n")
        r = run(root, "check_citations.py")
        out = r.stdout
        for msg in ("decisions.csv:3: status must be", "decisions.csv:3: due must be", "related decision zz",
                    "decision d2 has no baseline", "options.csv:3: decision nope", "options.csv:3: kind must be",
                    "positions.csv:3: option o9", "actor lieber isn't an id", "positions.csv:3: date must be",
                    "unknown NEWS id NEWS-404", "questions.csv:3: an answered question needs an answer",
                    "a done decision needs an outcome", "positions.csv:6: replaces must be",
                    "people.csv:4: area 'North and Northeast Portland' isn't on legislature/members/roe.html"):
            assert msg in out, (msg, out)
        assert "Portland Public Schools" not in out and "questions.csv: no 'source'" not in out, out
        assert "people.csv:2" not in out and "people.csv:3" not in out, out
        r = run(root, "check_citations.py", "--measures")
        assert "1 open, 1 answered" in r.stdout and "d1 (due 2026-12-01): baseline yes" in r.stdout, r.stdout
        assert "proposals none, 4 stances" in r.stdout, r.stdout  # line 2 is replaced by line 5
        for f in ("decisions", "options", "positions", "questions"):
            os.remove(f"{root}/analysis/{f}.csv")
        shutil.rmtree(f"{root}/analysis/people")
        shutil.rmtree(f"{root}/sources/legislature")

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

        # derived figures, DER tags, topic sections, the \"our sum\" rule outside topics/ and the number warning
        os.makedirs(f"{root}/analysis/derived")
        os.makedirs(f"{root}/analysis/topics")
        open(f"{root}/analysis/derived/t.csv", "w").write(
            "id,value,unit,kind,label,method,inputs,assumptions\n"
            "n,22110,students,derived,Students,sum,data/x.csv,\n"
            "share,3.97,percent,derived,Share,n / state total,data/x.csv,\n"
            "est,256.6,USD millions,est,Money,sum of x * y,data/x.csv,y is an average\n")
        open(f"{root}/analysis/topics/ok.md", "w").write(
            "---\nsummary: >\n  About 4% of students.\ndescription: About 4% of students.\n---\n# OK topic\n\nIntro.\n\n## Analysis\n\nAbout 22,100 students, about 4% (our sum [DER:t/n] [DER:t/share]).\n\n"
            "## What the sources say\n\n- The fund is $13 billion\n  [SRC:gov/test_page.html].\n\n"
            "| Bill | Fund |\n|---|---|\n| State | $13 billion [SRC:gov/test_page.html] |\n\n"
            "## Derived figures\n\n| Figure | Value |\n|---|---|\n| Money | about $257M [DER:t/est] |\n")
        open(f"{root}/analysis/notes.md", "w").write(
            "Enrolled about 22,100 students (our sum [DER:t/n]).\n| Money | ~257 | our estimate [DER:t/est] |\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 0 and "0 errors" in r.stdout and "not in the text" not in r.stdout, r.stdout
        r = run(root, "linkify.py", f"{root}/analysis/notes.md")
        assert "[DER:t/n](https://github.com/pietvanzoen/fund-oregon-schools/blob/main/analysis/derived/t.csv)" \
            in r.stdout, r.stdout

        open(f"{root}/analysis/notes.md", "w").write(
            "Enrolled about 22,200 students (our sum [DER:t/n]). About $257M of it [DER:t/est].\n"
            "Unknown [DER:t/nope] and [DER:zz/n].\n")
        # front matter shifts the body down 6 lines; reported line numbers stay the file's
        open(f"{root}/analysis/topics/bad.md", "w").write(
            "---\nsummary: >\n  Short [SRC:gov/test_page.html].\ndescription: Bad.\ntags: Bad\n---\n# Bad, with a page title far too long to show whole in search results\n\n## Analysis\n\nNo citation needed here.\n\n## What the sources say\n\n- No citation here.\n"
            "- Analysis: inference [SRC:gov/test_page.html].\n- It is $14 billion [SRC:gov/test_page.html].\n\n"
            "## Derived figures\n")
        # the old order (sources first) is now an error
        open(f"{root}/analysis/topics/order.md", "w").write(
            "# O\n\n## What the sources say\n\n## Derived figures\n\n## Analysis\n")
        open(f"{root}/analysis/derived/u.csv", "w").write(
            "id,value,unit,kind,label,method,inputs,assumptions\nx,abc,USD,guess,X,m,i,\n")
        open(f"{root}/analysis/derived/v.csv", "w").write("id,value\nx,1\n")
        r = run(root, "check_citations.py")
        out = r.stdout
        assert r.returncode == 1 and out.count("ERROR") == 15, out
        assert "notes.md:1: [DER:t/n] is 22110 students; no number" in out, out  # 22,200 is not 22110 rounded
        assert "notes.md:1: [DER:t/est] needs \"our sum\" or \"our estimate\"" in out, out
        assert "unknown derived figure t/nope" in out and "unknown derived figure zz/n" in out, out
        assert "order.md: no `summary` in front matter" in out and "front matter key tags isn't used" in out
        assert "order.md: no `description` in front matter" in out and "bad.md: page title is 67 characters" in out, out
        assert "bad.md: the summary carries no citations" in out, out
        assert "bad.md:15: line under \"What the sources say\" has no source citation" in out, out
        assert "bad.md:16: \"Analysis:\" under" in out and "order.md: needs exactly these sections" in out, out
        assert "u.csv:2: kind must be derived or est" in out and "u.csv:2: value 'abc' is not a number" in out, out
        assert "v.csv: columns must be" in out, out
        assert "warn  analysis/topics/bad.md:17: 14 is not in the text" in out, out
        shutil.rmtree(f"{root}/analysis/derived")
        shutil.rmtree(f"{root}/analysis/topics")
        os.remove(f"{root}/analysis/notes.md")

        r = run(root, "linkify.py", f"{root}/analysis/a.md")
        assert f"[SRC:gov/test_page.html]({url})" in r.stdout, r.stdout
        assert "[NEWS:NEWS-1](https://e.x/a)" in r.stdout and f"({url}/x#page=2)" in r.stdout, r.stdout

        r = run(root, "search.py", "school fund", "--kind", "src")
        assert "[SRC:gov/test_page.html]" in r.stdout, r.stdout + r.stderr
        r = run(root, "doc.py", "test_page", "--grep", "billion")
        assert "13 billion" in r.stdout, r.stdout + r.stderr

        # a hand-saved hearing video with its machine transcript: search cites the line's timestamp, the
        # header isn't indexed, and a VID tag without the extension resolves
        os.makedirs(f"{root}/sources/legislature/video")
        open(f"{root}/sources/legislature/video/h.mp4", "w").write("x")
        open(f"{root}/sources/legislature/video/h.mp4.txt", "w").write(
            "# Machine transcript, verify quotes\n0:00:02 Good morning.\n1:02:05 We have to be bold on schools.\n")
        r = run(root, "search.py", "bold", "--kind", "src")
        assert "[VID:legislature/video/h@1:02:05]" in r.stdout and "@0:00:02" not in r.stdout, r.stdout
        assert run(root, "search.py", "verify").stdout.strip() == "no matches"
        open(f"{root}/analysis/v.md", "w").write("Bold [VID:legislature/video/h@1:02:05], gone [VID:x/nope@0:01]\n")
        r = run(root, "check_citations.py")
        assert r.stdout.count("ERROR") == 1 and "unknown video x/nope" in r.stdout, r.stdout
        os.remove(f"{root}/analysis/v.md")
        shutil.rmtree(f"{root}/sources/legislature")

        # visuals: bars point to data rows by id or to derived rows; every note, box and arrow is cited or open
        for d in ("data", "derived", "visuals"):
            os.makedirs(f"{root}/analysis/{d}")
        open(f"{root}/analysis/data/h.csv", "w").write(
            "id,biennium,amount_billion,source\na,2025-27,11.36,[SRC:gov/test_page.html]\nb,2027-29,,[SRC:gov/test_page.html]\n")
        open(f"{root}/analysis/derived/z.csv", "w").write(
            "id,value,unit,kind,label,method,inputs,assumptions\nn,12.5,USD billions,derived,N,a + 1,data/h.csv,\n")
        bars = {"id": "ok-bars", "kind": "bars", "title": "T", "description": "D", "column": "amount_billion",
                "unit": "billion", "notes": ["Adopted [SRC:gov/test_page.html]."],
                "bars": [{"ref": "data/h/a", "label": "2025-27", "group": "Adopted"},
                         {"ref": "derived/z/n", "label": "Ours", "group": "Our sum"}]}
        flow = {"id": "ok-flow", "kind": "flow", "title": "T", "description": "D", "columns": 2,
                "rows": [{"groups": [{"name": "R", "span": 1, "boxes": [{"id": "a", "label": "A", "cite": "[NEWS:NEWS-1]"}]},
                                     {"name": "Q", "span": 1, "boxes": [{"id": "b", "label": "B", "open": "no source yet"}]}]},
                         {"groups": [{"name": "S", "span": 2, "boxes": [{"id": "c", "label": "C", "cite": "[SRC:gov/test_page.html]"}]}]}],
                "arrows": [{"from": "a", "to": "c", "label": "x", "cite": "[NEWS:NEWS-1]"},
                           {"from": "b", "to": "c", "label": "y", "open": "not yet confirmed"}]}
        for v in (bars, flow):
            json.dump(v, open(f"{root}/analysis/visuals/{v['id']}.json", "w"))
        open(f"{root}/analysis/m.md", "w").write("<!-- site: visual ok-bars -->\n")
        r = run(root, "check_citations.py")
        assert r.returncode == 0 and "0 errors" in r.stdout, r.stdout
        bad = dict(bars, id="bad", notes=["No citation."], bars=[{"ref": "data/h/b", "label": "L", "group": "G"},
                                                                 {"ref": "data/h/zz", "label": "L"}, {"ref": "derived/z/q", "label": "L", "group": "G"}])
        json.dump(bad, open(f"{root}/analysis/visuals/bad.json", "w"))
        json.dump(dict(flow, id="bad-flow", arrows=[{"from": "a", "to": "nope", "label": "x", "cite": "[NEWS:NEWS-9]"},
                                                   {"from": "a", "to": "c", "label": "y"}]),
                  open(f"{root}/analysis/visuals/bad-flow.json", "w"))
        json.dump(dict(flow, kind="pie"), open(f"{root}/analysis/visuals/renamed.json", "w"))
        json.dump(dict(flow, id="wide", columns=1), open(f"{root}/analysis/visuals/wide.json", "w"))
        open(f"{root}/analysis/data/h.csv", "a").write("a,2029-31,13,[SRC:gov/test_page.html]\n")
        open(f"{root}/analysis/m.md", "a").write("<!-- site: visual gone -->\n")
        r = run(root, "check_citations.py")
        out = r.stdout
        assert r.returncode == 1 and out.count("ERROR") == 13, out
        assert "wide.json: row 1's groups span more than 1 columns" in out and "wide.json: row 2's" in out, out
        assert "h.csv:4: id 'a' is empty or used twice" in out and "m.md:2: no visual gone" in out, out
        assert "bad.json: note has no citation" in out and "bar 'data/h/b' doesn't point to a row with a number" in out, out
        assert "bar 'data/h/zz'" in out and "bar data/h/zz needs a label and a group" in out and "bar 'derived/z/q'" in out, out
        assert "bad-flow.json: arrow a -> nope: no box nope" in out and "unknown NEWS id NEWS-9" in out, out
        assert "bad-flow.json: arrow 'y' has no citation" in out and "renamed.json: id must be 'renamed'" in out, out
        for d in ("data", "derived", "visuals"):
            shutil.rmtree(f"{root}/analysis/{d}")
        os.remove(f"{root}/analysis/m.md")

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

        sys.path.insert(0, HERE)
        from common import front_matter
        assert front_matter("# T\n") == ({}, "# T\n")
        assert front_matter("---\nsummary: >\n  One two.\n  Three.\nk: v\n---\n# T\nx") == \
            ({"summary": "One two. Three.", "k": "v"}, "# T\nx")
        for bad in ("---\nk: v\n# T\n", "---\nk: \"q\"\n---\n", "---\nk: [a]\n---\n", "---\nk: a: b\n---\n",
                    "---\nk: |\n  x\n---\n", "---\nk: >\n---\n", "---\nk: >\n  a\n\n  b\n---\n",
                    "---\n- a\n---\n", "---\nk: v\nk: w\n---\n", "---\nk: v # c\n---\n"):
            try:
                front_matter(bad)
                raise AssertionError(f"accepted {bad!r}")
            except ValueError:
                pass
        from ocr_pdfs import MIN_CHARS, pages_to_ocr
        # p.1 picture-only slide, p.2 text-rich page with a logo, p.3 blank page without an image
        assert pages_to_ocr(["Title", "x" * MIN_CHARS, ""], {1, 2}) == [1]
        assert pages_to_ocr(["  a b  " * 5, ""], {1}) == [1]
        from save_youtube import LOOP, lines, loops
        segs = [{"start": 3725.6, "text": " Good morning. "}, {"start": 3730, "text": "  "}]
        assert lines(segs) == ["1:02:05 Good morning."]
        segs += [{"start": 3731 + i, "text": "And so we can do that."} for i in range(LOOP)]
        segs += [{"start": 3800, "text": "Adjourned."}, {"start": 3801, "text": "Adjourned."}]
        assert loops(segs) == [(3731, LOOP, "And so we can do that.")]
        stuck = "Mr. Richardson, " * 6
        segs += [{"start": 3900, "text": stuck}, {"start": 3903, "text": stuck}, {"start": 3910, "text": "Thank you, chair."}]
        assert loops(segs) == [(3731, LOOP, "And so we can do that."), (3900, 2, stuck.strip())]

        print("all tool tests passed")
    finally:
        srv.shutdown()
        shutil.rmtree(root)


if __name__ == "__main__":
    main()
