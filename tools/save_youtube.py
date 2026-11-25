#!/usr/bin/env python3
"""Save a YouTube recording's audio under sources/ with a manifest line, and write its machine transcript.

The maintainer runs this on an Apple Silicon Mac: the fetch-sources bot and cloud sandboxes can't reach YouTube.
Needs yt-dlp, ffmpeg and mlx-whisper on PATH (RUNBOOK, "Hearing video").

    python3 tools/save_youtube.py URL PATH TITLE DATE
    python3 tools/save_youtube.py https://youtu.be/geKi7gkUryU ode/state-board/video/2026-05-21_regular-meeting.webm \\
        "Oregon State Board of Education: regular meeting of May 21, 2026 (recording)" 2026-05-21

Skips steps already done: an archived file isn't downloaded again, and an existing transcript is kept
(delete <file>.txt and rerun to redo it).
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MANIFEST, SOURCES  # noqa: E402

MODEL = "mlx-community/whisper-large-v3-turbo"
LIMIT = 100 * 1024 * 1024  # GitHub rejects files over 100 MB
LOOP = 5  # this many identical segments in a row is Whisper repeating itself, not the speaker
START = time.monotonic()


def log(msg):
    e = int(time.monotonic() - START)
    print(f"[{time.strftime('%H:%M:%S')} +{e // 60}:{e % 60:02}] {msg}", flush=True)


def lines(segments):
    """Whisper segments -> "H:MM:SS text" lines, the format the transcribe Action writes."""
    out = []
    for s in segments:
        t, text = int(s["start"]), s["text"].strip()
        if text:
            out.append(f"{t // 3600}:{t // 60 % 60:02}:{t % 60:02} {text}")
    return out


def compressed(text):
    """Whisper's own test for a stuck decode: text that zlib shrinks more than 2.4 times is one phrase repeated."""
    b = text.encode()
    return len(b) >= 40 and len(b) / len(zlib.compress(b)) > 2.4


def loops(segments):
    """(start seconds, lines, text) for each run of LOOP or more identical segments, and each run of segments
    that repeat a phrase inside themselves ("Mr. Richardson, Mr. Richardson, ...")."""
    out, i = [], 0
    while i < len(segments):
        j = i
        while j + 1 < len(segments) and segments[j + 1]["text"].strip() == segments[i]["text"].strip():
            j += 1
        if j - i + 1 >= LOOP:
            out.append((segments[i]["start"], j - i + 1, segments[i]["text"].strip()))
        i = j + 1
    i = 0
    while i < len(segments):
        j = i - 1
        while j + 1 < len(segments) and compressed(segments[j + 1]["text"].strip()):
            j += 1
        if j >= i:
            out.append((segments[i]["start"], j - i + 1, segments[i]["text"].strip()))
        i = max(j, i) + 1
    return sorted(out)


def download(url, rel, title, date, dest, tmp):
    log(f"downloading {url}")
    # the URL goes to a file: on stdout it's mixed in with yt-dlp's progress bar
    subprocess.run(["yt-dlp", "--no-playlist", "-f", "bestaudio", "-o", f"{tmp}/orig.%(ext)s",
                    "--print-to-file", "webpage_url", f"{tmp}/url.txt", url], check=True)
    final_url = open(f"{tmp}/url.txt", encoding="utf-8").read().strip()
    orig = next(os.path.join(tmp, f) for f in os.listdir(tmp) if f.startswith("orig."))
    log(f"downloaded {os.path.getsize(orig) / 1e6:.0f} MB from {final_url}")
    # shortcut: 32 kbps mono fits about 7 hours under 100 MB; split the file if a recording runs longer
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    log("re-encoding to 32 kbps mono Opus")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-stats", "-i", orig, "-vn", "-ac", "1", "-c:a", "libopus",
                    "-b:a", "32k", "-application", "voip", dest], check=True)
    size = os.path.getsize(dest)
    if size > LIMIT:
        os.remove(dest)
        raise SystemExit(f"{rel}: {size / 1e6:.0f} MB is over GitHub's 100 MB limit")
    rec = {"path": rel, "url": url, "final_url": final_url,
           "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "sha256": hashlib.sha256(open(dest, "rb").read()).hexdigest(), "bytes": size,
           "content_type": "audio/webm", "title": title, "date": date, "kind": rel.split("/")[0],
           "note": "Saved by tools/save_youtube.py: YouTube's audio re-encoded to 32 kbps mono Opus "
                   "to fit GitHub's 100 MB limit."}
    with open(MANIFEST, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    log(f"saved {rel} ({size / 1e6:.0f} MB) and its manifest line")


def transcribe(dest, tmp):
    # condition-on-previous-text off and the silence threshold stop the repeated-line loops Whisper falls into
    # on long meetings with quiet stretches (a 5-hour State Board meeting lost 146 minutes to them)
    log(f"transcribing with {MODEL} (prints each segment as it goes)")
    subprocess.run(["mlx_whisper", dest, "--model", MODEL, "--language", "en",
                    "--condition-on-previous-text", "False", "--word-timestamps", "True",
                    "--hallucination-silence-threshold", "2",
                    "--output-format", "json", "--output-dir", tmp, "--output-name", "t"], check=True)
    segments = json.load(open(os.path.join(tmp, "t.json"), encoding="utf-8"))["segments"]
    head = (f"# Machine transcript (mlx-whisper {MODEL.split('/')[-1]}), not checked by a person. "
            "Listen to the recording to verify any quote before citing it.")
    with open(dest + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join([head] + lines(segments)) + "\n")
    t = int(segments[-1]["end"]) if segments else 0
    log(f"wrote {os.path.relpath(dest, SOURCES)}.txt: {len(segments)} segments, "
        f"{t // 3600}:{t // 60 % 60:02}:{t % 60:02} of audio")
    found = loops(segments)
    for start, n, text in found:
        t = int(start)
        log(f"loop at {t // 3600}:{t // 60 % 60:02}:{t % 60:02}: {n} lines of {text[:60]!r}")
    if found:
        raise SystemExit(f"{len(found)} repeated-line loop(s): the transcript has gaps there")


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    url, rel, title, date = sys.argv[1:]
    if not rel.endswith(".webm"):
        raise SystemExit("PATH must end in .webm (the audio is saved as Opus in WebM)")
    dest = os.path.join(SOURCES, rel)
    with tempfile.TemporaryDirectory() as tmp:
        if os.path.exists(dest):
            log(f"{rel} already archived, not downloading")
        else:
            download(url, rel, title, date, dest, tmp)
        if os.path.exists(dest + ".txt"):
            log(f"{rel}.txt exists, not transcribing (delete it to redo)")
        else:
            transcribe(dest, tmp)
    log("done")


if __name__ == "__main__":
    main()
