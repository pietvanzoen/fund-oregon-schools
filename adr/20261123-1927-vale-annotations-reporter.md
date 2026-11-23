# Vale findings are annotations on the style job, not a separate check run

Status: accepted (2026-11-23, PR #N)

## Context
The `style` workflow used reviewdog's `github-pr-check` reporter, which creates its own check run (also named
`vale`) and then updates it through the Checks API. On PR #137 that update got `404 Not Found` twice, right after
the check run was created. The job failed and reviewdog's check stayed `in_progress`, though Vale itself found
only suggestions (#140). PRs with no findings on added lines (#125, #126) never make that update, so they passed.
#122 had 13 findings and posted them fine, so the failure is intermittent, not about the number of annotations
(#137 had 9).

## Decision
Use the `github-pr-annotations` reporter: reviewdog writes the findings as annotations on the `vale` job itself,
so there is no second check run to update. `fail_level: none` and `continue-on-error` on the step keep a posting
failure from turning the check red, as `20261122-1551-vale-in-ci-stdlib-in-tools.md` requires.

## Options weighed
- **`github-pr-annotations`** (chosen): no Checks API update to fail and no check left `in_progress`. The
  `fos-work-issue` skill's command still finds the findings on the check run named `vale`. Cost: GitHub shows at
  most 10 annotations of each level per step.
- **Rename reviewdog's check run**: vale-action v3 hardcodes `-name=vale`, so this isn't available.
- **Upgrade reviewdog or vale-action**: we already pin v3 and reviewdog 0.21.0, the action's current default.
  There's no known upstream fix.
- **`continue-on-error` alone**: keeps the check green but leaves reviewdog's check `in_progress` and the findings
  unposted.

## Revisit when
A PR has more than 10 findings of one level and some get hidden, or annotations stop showing on the PR.
