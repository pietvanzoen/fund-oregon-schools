#!/usr/bin/env python3
"""Print the next issue a run should work: the first free one in the Research queue (fos-work-issue step 1).

    python3 tools/next_issue.py        # prints the number; prints nothing and exits 1 if nothing is free

Free: open, labelled `auto`, none of the labels in SKIP, no open PR that says "Closes #<n>", no
`claude/issue-<n>-*` branch. An issue split before runs stopped splitting gives its first free sub-issue instead.
Reads GitHub with `gh api` (REST; GraphQL isn't available in cloud sessions).
"""

import json
import re
import subprocess
import sys

REPO = "repos/pietvanzoen/fund-oregon-schools"
SKIP = {"needs-human", "needs-judgement", "manual", "in progress", "blocked"}
QUEUE_RE = re.compile(r"^\s*\d+\.\s+#(\d+)\b", re.MULTILINE)


def pick(queue_body, get_issue, get_subs, pr_bodies, branches):
    """First free issue number in queue order, or None. get_issue(n) -> {"state", "labels"}; get_subs(n) -> [n]."""

    def free(n):
        i = get_issue(n)
        labels = set(i["labels"])
        return (
            i["state"] == "open"
            and "auto" in labels
            and not labels & SKIP
            and not any(re.search(rf"\bcloses #{n}\b", b, re.IGNORECASE) for b in pr_bodies)
            and not any(b.startswith(f"claude/issue-{n}-") for b in branches)
        )

    for n in map(int, QUEUE_RE.findall(queue_body)):
        if not free(n):
            continue
        subs = get_subs(n)
        if not subs:
            return n
        for s in subs:
            if free(s):
                return s
    return None


def gh(path):
    out = subprocess.run(
        ["gh", "api", "--paginate", f"{REPO}/{path}"], check=True, text=True, capture_output=True
    ).stdout
    # --paginate joins pages as concatenated JSON arrays
    return json.loads(out.replace("][", ",")) if out.startswith("[") else json.loads(out)


def main():
    queue = gh("issues?state=open&labels=queue&per_page=100")
    if not queue:
        sys.exit("no open issue labelled `queue`")
    prs = [p.get("body") or "" for p in gh("pulls?state=open&per_page=100")]
    branches = [r["ref"].removeprefix("refs/heads/") for r in gh("git/matching-refs/heads/claude/issue-")]

    def get_issue(n):
        i = gh(f"issues/{n}")
        return {"state": i["state"], "labels": [lab["name"] for lab in i["labels"]]}

    n = pick(
        queue[0]["body"] or "", get_issue, lambda n: [s["number"] for s in gh(f"issues/{n}/sub_issues")], prs, branches
    )
    if n is None:
        sys.exit(1)
    print(n)


if __name__ == "__main__":
    main()
