# YouTube recordings are saved and transcribed on the maintainer's Mac

Status: accepted (2026-11-25, PR #200)

## Context
State Board of Education meetings and the Governor's press conferences are on YouTube, which the fetch-sources
bot and cloud sandboxes can't reach (#72, #106). The May 21, 2026 State Board meeting runs 5 hours 13 minutes:
its best audio stream is 234 MB, over GitHub's 100 MB limit. A trial transcript with mlx-whisper and default
settings lost 146 of its 313 minutes to loops of one repeated line.

## Decision
`tools/save_youtube.py`, run by the maintainer on an Apple Silicon Mac, downloads the audio with yt-dlp,
re-encodes it to 32 kbps mono Opus (`.webm`, about 75 MB for 5 hours), appends the manifest line and writes the
transcript with mlx-whisper `whisper-large-v3-turbo`, with conditioning on previous text off and a silence
threshold, then reports any remaining loops. The script itself is stdlib Python; yt-dlp, ffmpeg and mlx-whisper
are command-line tools on the Mac, not dependencies of `tools/`. The `transcribe` Action skips these files
because their transcript already exists.

## Options weighed
- **Save the audio by hand, let the Action transcribe it**: no new script, but `small.en` on a 4-CPU runner takes
  about 1.5 hours for this meeting and mishears more; each recording also means hand-writing the manifest line.
- **Keep YouTube's original audio stream**: the file as published, but too big to commit for long meetings.
- **Script on the Mac, re-encoded audio, local large-v3-turbo transcript** (chosen): one command per recording,
  fits under 100 MB, the GPU runs the larger model in about 20 minutes. Costs: the archived audio isn't
  byte-identical to YouTube's stream (the manifest note says so), and only the maintainer can run it.

## Revisit when
A recording runs past about 7 hours (32 kbps no longer fits), the loop check keeps firing with these settings, or
a second person needs to archive recordings without a Mac.
