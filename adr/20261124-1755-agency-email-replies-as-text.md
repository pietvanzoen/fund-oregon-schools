# An agency's email answer to the archive's question is archived as its reply text

Status: accepted (2026-11-24, PR #170)

## Context
Until now, emailed replies were left out as personal correspondence, and only their attachments were archived
(the Kotek letter, Baker SD 5J's service agreement). ODE's Nov. 24, 2026 answer on the "Charter Schools Rate" (#47)
is different: the email is the only source for what it says. Nothing published says which per-student figure
ORS 338.155's minimums use or that ODE publishes no virtual charter total. The emailed copy also carries the
maintainer's address and his quoted original message.

## Decision
When an official answers a question sent for the archive, save the reply as a `.txt` under
`sources/<agency>/correspondence/`: the header lines, the body and the signature's name and titles, verbatim. Leave
out the recipient's address, phone numbers and the quoted original. Add a manifest line by hand that says what was
asked, what was left out and that `fetched_at` is when the reply arrived.

## Options weighed
- **Reply text only** (chosen): citable, and the sender's words are kept exactly. Costs one judgement about what
  counts as the reply, which is set out in the manifest note.
- **The emailed PDF as-is**: the most original form, but it puts a private address and the quoted request in the
  public archive.
- **Not archiving it**: keeps to the earlier rule, but the claims would then rest on nothing citable.

## Revisit when
A reply's meaning depends on the question in ways the manifest note can't carry, or a sender asks that a reply not
be published.
