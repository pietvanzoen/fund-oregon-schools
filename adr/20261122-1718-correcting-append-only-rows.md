# A wrong append-only row is corrected by a new row that names the line it replaces

Status: accepted (2026-11-22, PR #115)

## Context
`analysis/positions.csv` is append-only (RESEARCH.md): a stance is recorded once and never edited, so the file is
a record of what the archive said and when. Row 5 (Kotek on reserves for PPS) was dated `2026-10`; the statement
was made on Nov. 6, 2026. PR #108's reviewers left it alone because there was no way to correct a row without
editing it.

## Decision
Append the corrected row with a `replaces` column holding the file line number of the row it replaces (the
number `check_citations.py` prints, header = line 1). The site hides any row another row replaces;
`check_citations.py` checks that `replaces` points at an earlier, existing row.

## Options weighed
- **`replaces` holding a line number (chosen)**: one column, no new ids; line numbers never change in a file
  whose rows are never edited or deleted, and they match the error messages reviewers already read.
- **Add an `id` column to every row and replace by id**: steadier if rows were ever reordered, but adds a column
  and back-filled ids to solve a problem the append-only rule already prevents.
- **Edit the row in place**: simplest, but loses the record of what the archive said before, which is why the
  file is append-only.
- **A separate corrections file**: keeps positions.csv untouched, but readers and tools would have to join two
  files to see one stance.

## Revisit when
Rows in an append-only file are reordered, deleted or merged by a tool, or a second file needs corrections.
