# Vale findings are review comments on the PR, not a separate check run

Status: accepted (2026-11-23, PR #141)

## Context
The `style` workflow used reviewdog's `github-pr-check` reporter. That reporter creates its own check run (also
named `vale`), then updates it through the Checks API. On PR #137 the update sometimes got `404 Not Found` right
after the check run was created. When it did, the job failed and reviewdog's check stayed `in_progress`, though
Vale found only suggestions (#140). A re-run of #137 with the same content passed. Throwaway PR #142 (about 60
fake findings) reproduced the 404. So the failure is intermittent and depends on timing, not content. PRs with
no findings on added lines (#125, #126) never make the update, which is why they always passed.

## Decision
Use the `github-pr-review` reporter: reviewdog posts the findings as one PR review, with a comment on each line.
There's no check run to update. `fail_level: none` and `continue-on-error` on the step keep a posting failure
from turning the check red, as `20261122-1551-vale-in-ci-stdlib-in-tools.md` requires. The workflow needs
`pull-requests: write` instead of `checks: write`.

## Options weighed
- **`github-pr-review`** (chosen): tested on throwaway PR #143 with the same fake findings. The check passed and
  nothing stayed `in_progress`. Comments keep Vale's severity (📝 suggestion, ⚠️ warning, 🚫 error) and the rule
  name. reviewdog posts at most 30 line comments per run and lists the rest in the review's summary. On a later
  push it skips findings it has already posted. Cost: comments on a big PR can be noisy.
- **`github-pr-annotations`**: tested on #143 first. GitHub shows only 10 annotations per step, and it added a
  red "Too many results" annotation. Every finding came through as a warning, so the skill couldn't tell
  warnings from suggestions. Not adopted.
- **Keep `github-pr-check` and only add `continue-on-error`**: the check stays green, but a check can still hang
  `in_progress` and findings sometimes go unposted. Not adopted.
- **Rename reviewdog's check run**: vale-action v3 hardcodes `-name=vale`. Not available.
- **Upgrade reviewdog or vale-action**: v3 and reviewdog 0.21.0 are already the action's defaults, and there's no
  known upstream fix.

## Revisit when
Review comments get too noisy for research PRs, or reviewdog fixes the check-run update and the Checks view is
wanted back.
