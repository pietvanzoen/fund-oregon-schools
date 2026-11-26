# Agent rules are split by area: a short CLAUDE.md, rule files, and one file per work step

Status: accepted (2026-11-26, PR #N)

## Context
Every session, subagent and reviewer loaded all of CLAUDE.md (about 21 KB): citation rules in site work, code rules
in research, and reviewers were told to read it a second time. The fos-work-issue skill (about 32 KB) loaded whole,
so the review and PR steps, which run last, sat furthest from where they're used. Rules had drifted between copies:
the topic-file layout was written out six times, and the nightly prompt's issue picker missed the `blocked` label
the skill had. Sources: Böckeler, "Context Engineering for Coding Agents" (martinfowler.com, Feb 2026); Anthropic's
skill authoring best practices (progressive disclosure, references one level deep, contents for files over 100
lines); Thoughtworks Radar vol. 35, "progressive context disclosure" (Adopt).

## Decision
- CLAUDE.md keeps purpose, "Start here" and the rules every session needs (1, 7, 9).
- `.claude/rules/sources.md`, `analysis.md` and `code.md` hold the rest, with `paths:` so they load on their own when
  a session reads files in their folders. Skills and reviewer prompts also name the files they need, because a
  scheduled run or subagent may not load them on its own.
- fos-work-issue steps 3-7 are files in `steps/`, read when the step starts. SKILL.md lists each step with its files.
- One copy of each rule; where `tools/check_citations.py` enforces a limit, the rule says so.
- `tools/next_issue.py` picks the issue, so the skill and the nightly prompt can't drift apart.

## Options weighed
- **Keep one CLAUDE.md, trimmed:** fewest files, but every session still loads every area's rules.
- **Rule files by name only** (no `paths:`): works the same everywhere, but interactive sessions miss a rule
  nobody named.
- **Path-scoped rule files only:** least text, but scheduled runs and subagents may not load them (not verified).
- **Both: path-scoped and named where needed** (chosen): a session may read a file twice; that costs a few
  thousand tokens.
- **Reviewer agents with their own definitions** (`omitClaudeMd`, a tool allowlist): deferred. Plugin agents don't
  load in the scheduled run, which has no plugins enabled, and the core CLAUDE.md is now small.
- **Sparse or shallow reviewer clones:** not done. A full clone takes about 5 s and its `.git` is 178 MB against
  165 MB shallow; a sparse clone without `sources/` binaries breaks `tools/doc.py` and `check_citations.py`.

## Revisit when
The reviewer smoke test (kept outside the repo) catches fewer planted errors than its baseline, a rule turns out to
be missed because its file didn't load, or Claude Code merges rules into skills.
