# sources/

Primary material only. Never edit, paraphrase into, or overwrite anything here.

- `_queue.csv`: what to fetch. `_manifest.jsonl`: what was fetched (url, final_url, fetched_at, sha256, bytes).
- `_versions_log.csv` (created the first time a document changes upstream): what changed; old copies live in
  `<dir>/_prior/`.
- `<file>.mp4.txt` (and other audio/video): machine transcript by the `transcribe` Action, `H:MM:SS text`
  lines. Not checked by a person: verify quotes against the recording.
- `news/index.jsonl`: news metadata, own-words summaries and short quotes only.
- Folders: see the path conventions in `CLAUDE.md` rule 2 (the one list).
