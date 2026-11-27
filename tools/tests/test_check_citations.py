import json
import subprocess
import unittest

from helpers import ArchiveTest


class CheckCitations(ArchiveTest):
    def test_src_and_news(self):
        self.write(
            "analysis/a.md", "Good [SRC:gov/test_page.html] pending [SRC:gov/not_fetched.pdf p.2] news [NEWS:NEWS-1]\n"
        )
        r = self.run_tool("check_citations.py")
        assert r.returncode == 0 and "1 warnings" in r.stdout and "pending (queued" in r.stdout, r.stdout
        self.write("analysis/b.md", "Bad [SRC:gov/nope.pdf p.1] [NEWS:NEWS-404]\n")
        self.write("analysis/c.csv", "year,amount,source\n2027,1,\n")
        r = self.run_tool("check_citations.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 3, r.stdout

    def test_updates_csv_and_pr(self):
        # What's new: updates.csv has its own columns (no source); --pr wants a row for a PR touching analysis/
        self.write("analysis/a.md", "Good [SRC:gov/test_page.html]\n")
        self.write(
            "analysis/updates.csv", "date,text,page,pr,kind\n2026-11-21,Ok,a.md,5,site\nNov 21,,nope.md,x,news\n"
        )
        r = self.run_tool("check_citations.py")
        assert r.returncode == 1 and r.stdout.count("ERROR") == 5 and "no 'source'" not in r.stdout, r.stdout
        self.write("analysis/updates.csv", "date,text,page,pr,kind\n2026-11-21,Ok,a.md,5,research\n")
        git = ["git", "-C", self.root, "-c", "user.email=t@t", "-c", "user.name=t"]
        subprocess.run(git + ["init", "-q", "-b", "main"], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "base"], check=True)
        subprocess.run(git + ["checkout", "-qb", "pr"], check=True)
        self.write("RESEARCH.md", "not under analysis/\n")
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "q"], check=True)
        assert self.run_tool("check_citations.py", "--pr", "7", "--base", "main").returncode == 0
        self.write("analysis/a.md", "More.\n", mode="a")
        subprocess.run(git + ["commit", "-qam", "a"], check=True)
        r = self.run_tool("check_citations.py", "--pr", "7", "--base", "main")
        assert r.returncode == 1 and "no row with pr 7" in r.stdout and "analysis/a.md" in r.stdout, r.stdout
        self.write("analysis/updates.csv", "2026-11-22,More,a.md,7,correction\n", mode="a")
        subprocess.run(git + ["commit", "-qam", "row"], check=True)
        assert self.run_tool("check_citations.py", "--pr", "7", "--base", "main").returncode == 0

    def test_decision_files(self):
        # decision files (RESEARCH.md): ids agree across files, a baseline per decision, known statuses.
        # people.csv area must be on the member page it cites (zero-width spaces ignored); no page, no check
        for m in ("doe", "roe"):
            self.write(f"sources/legislature/members/{m}.html", "x")
            self.write(f"sources/legislature/members/{m}.html.txt", "Democrat - District 22 - N/NE\u200b Portland\n")
        self.write(
            "analysis/people/people.csv",
            "id,name,area,source\nkotek,Tina Kotek,Statewide,[NEWS:NEWS-1]\n"
            "doe,Jane Doe,N/NE Portland,[SRC:legislature/members/doe.html]\n"
            "roe,Ray Roe,North and Northeast Portland,[SRC:legislature/members/roe.html]\n",
        )
        self.write(
            "analysis/decisions.csv",
            "id,decision,decided_by,due,status,related,outcome,outcome_source,source\n"
            "d1,D,Gov,2026-12-01,open,,,,[NEWS:NEWS-1]\nd2,D,Gov,Dec 1,done,zz,,,[NEWS:NEWS-1]\n",
        )
        self.write(
            "analysis/options.csv",
            "id,decision,kind,option,proposed_by,proposed_on,amount,formality,source\n"
            "o1,d1,baseline,B,,,,law,[NEWS:NEWS-1]\no2,nope,idea,X,,,,bill,[NEWS:NEWS-1]\n",
        )
        self.write(
            "analysis/positions.csv",
            "decision,option,actor,date,stance,source,replaces\nd1,,kotek,2026-11,s,[NEWS:NEWS-1],\n"
            "d1,o9,lieber,soon,s,[NEWS:NEWS-404],\nd1,,Portland Public Schools,2026,s,[NEWS:NEWS-1],\n"
            "d1,,kotek,2026-11-06,s,[NEWS:NEWS-1],2\nd1,,kotek,2026-11-06,s,[NEWS:NEWS-1],9\n",
        )
        self.write(
            "analysis/questions.csv",
            "id,question,decision,criterion,asked_by,needed_by,status,answer,issue\n"
            "q1,Q?,d1,c,a parent,2027-01-19,open,,\nq2,Q?,,c,a parent,,answered,,\n",
        )
        out = self.run_tool("check_citations.py").stdout
        for msg in (
            "decisions.csv:3: status must be",
            "decisions.csv:3: due must be",
            "related decision zz",
            "decision d2 has no baseline",
            "options.csv:3: decision nope",
            "options.csv:3: kind must be",
            "positions.csv:3: option o9",
            "actor lieber isn't an id",
            "positions.csv:3: date must be",
            "unknown NEWS id NEWS-404",
            "questions.csv:3: an answered question needs an answer",
            "a done decision needs an outcome",
            "positions.csv:6: replaces must be",
            "people.csv:4: area 'North and Northeast Portland' isn't on legislature/members/roe.html",
        ):
            assert msg in out, (msg, out)
        assert "Portland Public Schools" not in out and "questions.csv: no 'source'" not in out, out
        assert "people.csv:2" not in out and "people.csv:3" not in out, out
        r = self.run_tool("check_citations.py", "--measures")
        assert "1 open, 1 answered" in r.stdout and "d1 (due 2026-12-01): baseline yes" in r.stdout, r.stdout
        assert "proposals none, 4 stances" in r.stdout, r.stdout  # line 2 is replaced by line 5

    def test_glossary(self):
        # rule 11: unknown abbreviations warn; glossary terms, "(XYZ)" and tags don't
        self.write(
            "analysis/glossary.csv",
            "term,full_name,kind,tooltip,definition,source\nSSF,State School Fund,acronym,t,d,[NEWS:NEWS-1]\n",
        )
        self.write(
            "analysis/g.md",
            "The SSF and the QEM and ADMr. Written out: National Center (NCES). PDF.\n`ABC` [SRC:gov/test_page.html]\n"
            'The bill names "Representative WRIGHT".\n',
        )
        r = self.run_tool("check_citations.py")
        assert r.returncode == 0 and r.stdout.count("glossary.csv") == 2, r.stdout
        assert "QEM isn't in" in r.stdout and "ADMr isn't in" in r.stdout, r.stdout

    def test_derived_figures(self):
        # derived figures, DER tags, topic sections, the "our sum" rule outside topics/ and the number warning
        self.write(
            "analysis/derived/t.csv",
            "id,value,unit,kind,label,method,inputs,assumptions\n"
            "n,22110,students,derived,Students,sum,data/x.csv,\n"
            "share,3.97,percent,derived,Share,n / state total,data/x.csv,\n"
            "est,256.6,USD millions,est,Money,sum of x * y,data/x.csv,y is an average\n",
        )
        self.write(
            "analysis/topics/ok.md",
            "---\nsummary: >\n  About 4% of students.\ndescription: About 4% of students.\n---\n# OK topic\n\nIntro.\n\n"
            "## Analysis\n\nAbout 22,100 students, about 4% (our sum [DER:t/n] [DER:t/share]).\n\n"
            "## What the sources say\n\n- The fund is $13 billion\n  [SRC:gov/test_page.html].\n\n"
            "| Bill | Fund |\n|---|---|\n| State | $13 billion [SRC:gov/test_page.html] |\n\n"
            "## Derived figures\n\n| Figure | Value |\n|---|---|\n| Money | about $257M [DER:t/est] |\n",
        )
        self.write(
            "analysis/notes.md",
            "Enrolled about 22,100 students (our sum [DER:t/n]).\n| Money | ~257 | our estimate [DER:t/est] |\n",
        )
        r = self.run_tool("check_citations.py")
        assert r.returncode == 0 and "0 errors" in r.stdout and "not in the text" not in r.stdout, r.stdout

        self.write(
            "analysis/notes.md",
            "Enrolled about 22,200 students (our sum [DER:t/n]). About $257M of it [DER:t/est].\n"
            "Unknown [DER:t/nope] and [DER:zz/n].\n",
        )
        # front matter shifts the body down 6 lines; reported line numbers stay the file's
        self.write(
            "analysis/topics/bad.md",
            "---\nsummary: >\n  Short [SRC:gov/test_page.html].\ndescription: Bad.\ntags: Bad\n---\n"
            "# Bad, with a page title far too long to show whole in search results\n\n## Analysis\n\n"
            "No citation needed here.\n\n## What the sources say\n\n- No citation here.\n"
            "- Analysis: inference [SRC:gov/test_page.html].\n- It is $14 billion [SRC:gov/test_page.html].\n\n"
            "## Derived figures\n",
        )
        # the old order (sources first) is now an error
        self.write("analysis/topics/order.md", "# O\n\n## What the sources say\n\n## Derived figures\n\n## Analysis\n")
        self.write(
            "analysis/derived/u.csv", "id,value,unit,kind,label,method,inputs,assumptions\nx,abc,USD,guess,X,m,i,\n"
        )
        self.write("analysis/derived/v.csv", "id,value\nx,1\n")
        r = self.run_tool("check_citations.py")
        out = r.stdout
        assert r.returncode == 1 and out.count("ERROR") == 15, out
        assert "notes.md:1: [DER:t/n] is 22110 students; no number" in out, out  # 22,200 is not 22110 rounded
        assert 'notes.md:1: [DER:t/est] needs "our sum" or "our estimate"' in out, out
        assert "unknown derived figure t/nope" in out and "unknown derived figure zz/n" in out, out
        assert "order.md: no `summary` in front matter" in out and "front matter key tags isn't used" in out
        assert "order.md: no `description` in front matter" in out and "bad.md: page title is 67 characters" in out, out
        assert "bad.md: the summary carries no citations" in out, out
        assert 'bad.md:15: line under "What the sources say" has no source citation' in out, out
        assert 'bad.md:16: "Analysis:" under' in out and "order.md: needs exactly these sections" in out, out
        assert "u.csv:2: kind must be derived or est" in out and "u.csv:2: value 'abc' is not a number" in out, out
        assert "v.csv: columns must be" in out, out
        assert "warn  analysis/topics/bad.md:17: 14 is not in the text" in out, out

    def test_video_citation(self):
        self.write("sources/legislature/video/h.mp4", "x")
        self.write("sources/legislature/video/h.mp4.txt", "# Machine transcript, verify quotes\n1:02:05 Bold.\n")
        self.write("analysis/v.md", "Bold [VID:legislature/video/h@1:02:05], gone [VID:x/nope@0:01]\n")
        r = self.run_tool("check_citations.py")
        assert r.stdout.count("ERROR") == 1 and "unknown video x/nope" in r.stdout, r.stdout

    def test_visuals(self):
        # bars point to data rows by id or to derived rows; every note, box and arrow is cited or open
        self.write(
            "analysis/data/h.csv",
            "id,biennium,amount_billion,source\na,2025-27,11.36,[SRC:gov/test_page.html]\n"
            "b,2027-29,,[SRC:gov/test_page.html]\n",
        )
        self.write(
            "analysis/derived/z.csv",
            "id,value,unit,kind,label,method,inputs,assumptions\nn,12.5,USD billions,derived,N,a + 1,data/h.csv,\n",
        )
        bars = {
            "id": "ok-bars",
            "kind": "bars",
            "title": "T",
            "description": "D",
            "column": "amount_billion",
            "unit": "billion",
            "notes": ["Adopted [SRC:gov/test_page.html]."],
            "bars": [
                {"ref": "data/h/a", "label": "2025-27", "group": "Adopted"},
                {"ref": "derived/z/n", "label": "Ours", "group": "Our sum"},
            ],
        }
        flow = {
            "id": "ok-flow",
            "kind": "flow",
            "title": "T",
            "description": "D",
            "columns": 2,
            "rows": [
                {
                    "groups": [
                        {"name": "R", "span": 1, "boxes": [{"id": "a", "label": "A", "cite": "[NEWS:NEWS-1]"}]},
                        {"name": "Q", "span": 1, "boxes": [{"id": "b", "label": "B", "open": "no source yet"}]},
                    ]
                },
                {
                    "groups": [
                        {
                            "name": "S",
                            "span": 2,
                            "boxes": [{"id": "c", "label": "C", "cite": "[SRC:gov/test_page.html]"}],
                        }
                    ]
                },
            ],
            "arrows": [
                {"from": "a", "to": "c", "label": "x", "cite": "[NEWS:NEWS-1]"},
                {"from": "b", "to": "c", "label": "y", "open": "not yet confirmed"},
            ],
        }
        visual = lambda v, name=None: self.write(f"analysis/visuals/{name or v['id']}.json", json.dumps(v))
        visual(bars)
        visual(flow)
        self.write("analysis/m.md", "<!-- site: visual ok-bars -->\n")
        r = self.run_tool("check_citations.py")
        assert r.returncode == 0 and "0 errors" in r.stdout, r.stdout
        bad_bars = [
            {"ref": "data/h/b", "label": "L", "group": "G"},
            {"ref": "data/h/zz", "label": "L"},
            {"ref": "derived/z/q", "label": "L", "group": "G"},
        ]
        visual(dict(bars, id="bad", notes=["No citation."], bars=bad_bars))
        bad_arrows = [
            {"from": "a", "to": "nope", "label": "x", "cite": "[NEWS:NEWS-9]"},
            {"from": "a", "to": "c", "label": "y"},
        ]
        visual(dict(flow, id="bad-flow", arrows=bad_arrows))
        visual(dict(flow, kind="pie"), "renamed")
        visual(dict(flow, id="wide", columns=1))
        self.write("analysis/data/h.csv", "a,2029-31,13,[SRC:gov/test_page.html]\n", mode="a")
        self.write("analysis/m.md", "<!-- site: visual gone -->\n", mode="a")
        r = self.run_tool("check_citations.py")
        out = r.stdout
        assert r.returncode == 1 and out.count("ERROR") == 13, out
        assert "wide.json: row 1's groups span more than 1 columns" in out and "wide.json: row 2's" in out, out
        assert "h.csv:4: id 'a' is empty or used twice" in out and "m.md:2: no visual gone" in out, out
        assert "bad.json: note has no citation" in out and "bar 'data/h/b' doesn't point to a row with a number" in out
        assert "bar 'data/h/zz'" in out and "bar data/h/zz needs a label and a group" in out, out
        assert "bar 'derived/z/q'" in out, out
        assert "bad-flow.json: arrow a -> nope: no box nope" in out and "unknown NEWS id NEWS-9" in out, out
        assert "bad-flow.json: arrow 'y' has no citation" in out and "renamed.json: id must be 'renamed'" in out, out


if __name__ == "__main__":
    unittest.main()
