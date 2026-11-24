# sources/

Primary material only. Never edit, paraphrase into, or overwrite anything here.

- `_queue.csv`: what to fetch. `_manifest.jsonl`: what was fetched (url, final_url, fetched_at, sha256, bytes).
- `_versions_log.csv` (created the first time a document changes upstream): what changed; old copies live in
  `<dir>/_prior/`.
- `<file>.mp4.txt` (and other audio/video): machine transcript by the `transcribe` Action, `H:MM:SS text`
  lines. Not checked by a person: verify quotes against the recording.
- `news/index.jsonl`: news metadata, own-words summaries and short quotes only.
- Rights: these are copies of other publishers' documents, kept so citations still work when originals change or
  disappear. The repo's licenses don't cover them (`LICENSE-content.md`). A publisher who wants a file removed can
  email hello@fundoregonschools.org.
- Folders: see the path conventions in `CLAUDE.md` rule 2 (the one list).
