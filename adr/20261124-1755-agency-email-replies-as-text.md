# Email replies are archived as reply text, and only when nothing else can be cited

Status: accepted (2026-11-24, PR #170)

## Context
Until now, emailed replies were left out as personal correspondence, and only their attachments were archived
(the Kotek letter, Baker SD 5J's service agreement). ODE's Nov. 24, 2026 answer on the "Charter Schools Rate" (#47)
is different: the email is the only source for what it says. Nothing published says which per-student figure
ORS 338.155's minimums use or that ODE publishes no virtual charter total. The emailed copy also carries the
maintainer's address and their quoted original message.

## Decision
Archive a reply only when the analysis needs something it says and no other citable source says it. Attachments
are archived as their original files, as before; a reply that only covers them stays out, named in their manifest
note. When a reply is archived, save it as a `.txt` under
`sources/<agency or district folder>/correspondence/`: the header lines, the body and the signature's name and titles,
verbatim, then the quoted message it answers, so the reply can be read against the question as sent. Leave out
email addresses of members of the public (the maintainer's included), phone numbers, links and notices a mail
system added. Add a manifest line by hand that says what was
asked, what was left out and that `fetched_at` is when the reply arrived.

## Options weighed
- **Reply text only** (chosen): citable, and the sender's words are kept exactly. Costs one judgement about what
  counts as the reply, which is set out in the manifest note. The question is kept because the reply's answers
  ("You are correct", "This rate is not…") only make sense against it; the draft in the issue wasn't what was sent.
- **The emailed PDF as-is**: the most original form, but it puts private addresses and mail-system notices in the
  public archive.
- **Not archiving it**: keeps to the earlier rule, but the claims would then rest on nothing citable.
- **Archiving every reply**: simpler to follow, but adds private correspondence the analysis doesn't use. Baker
  SD 5J's Nov. 23 reply stays out for that reason: the topic cites only the agreement it came with.

## Consequence for outreach
Anything sent for the archive may be published in it. Draft emails and records requests to be read by the public:
no private details beyond what the About page already says about who runs the archive.

## Revisit when
A reply's meaning depends on the question in ways the manifest note can't carry, or a sender asks that a reply not
be published.
