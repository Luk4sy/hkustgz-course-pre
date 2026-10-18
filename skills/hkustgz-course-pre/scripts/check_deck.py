"""Check a finished .pptx before you present it.

Usage: python check_deck.py deck.pptx --minutes 8 [--wpm 140]

Checks, per slide:
  - [CLICK] markers in the notes = click steps in the animation sequence
  - the slide has speaker notes
Checks for the whole deck:
  - spoken time (English note words / wpm) fits in 90% of the time limit
Compatibility warnings (PowerPoint + WPS):
  - Chinese text without a Chinese East Asian font (run fix_fonts.py)
  - images or video in formats one of the apps may not show (webp, svg, gif, heic; non-MP4 or non-H.264 video)
  - file size over 100 MB
Exit code 1 if anything fails, so it can run in a script. Warnings don't fail.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, zipfile

ap = argparse.ArgumentParser()
ap.add_argument("pptx")
ap.add_argument("--minutes", type=float, required=True, help="time limit of the talk")
ap.add_argument("--wpm", type=float, default=140, help="speaking speed, English words per minute")
a = ap.parse_args()

z = zipfile.ZipFile(a.pptx)
names = z.namelist()
slides = sorted((n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                key=lambda n: int(re.findall(r"\d+", n)[-1]))


def notes_text(slide_name):
    rels = slide_name.replace("slides/", "slides/_rels/") + ".rels"
    if rels not in names:
        return ""
    m = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', z.read(rels).decode("utf8"))
    if not m:
        return ""
    xml = z.read("ppt/notesSlides/" + m.group(1)).decode("utf8")
    paras = re.findall(r"<a:p>(.*?)</a:p>", xml, re.S)
    lines = ["".join(re.findall(r"<a:t>(.*?)</a:t>", p, re.S)) for p in paras]
    return "\n".join(l for l in lines if l.strip() and not l.strip().isdigit())


problems, total_words = [], 0
print(f"{'slide':>5}  {'clicks':>6}  {'[CLICK]':>7}  {'words':>5}")
for i, s in enumerate(slides, 1):
    xml = z.read(s).decode("utf8")
    clicks = xml.count('nodeType="clickEffect"')
    notes = notes_text(s)
    english = "\n".join(l for l in notes.splitlines() if not re.search(r"[\u4e00-\u9fff]", l))
    markers = len(re.findall(r"\[CLICK\]", english, re.I))
    words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\u2019\-]*", re.sub(r"\[CLICK\]", "", english, flags=re.I)))
    total_words += words
    flag = ""
    if not notes:
        flag = "  <- no speaker notes"; problems.append(f"slide {i}: no speaker notes")
    elif clicks != markers:
        flag = "  <- mismatch"; problems.append(f"slide {i}: {clicks} click steps but {markers} [CLICK] markers")
    print(f"{i:>5}  {clicks:>6}  {markers:>7}  {words:>5}{flag}")

spoken = total_words / a.wpm
budget = a.minutes * 0.9
print(f"\nspoken time ~ {spoken:.1f} min for {total_words} words at {a.wpm:.0f} wpm; "
      f"budget {budget:.1f} min (90% of {a.minutes:g})")
if spoken > budget:
    problems.append(f"too long: cut about {(spoken - budget) * a.wpm:.0f} words")
elif spoken < a.minutes * 0.55:
    print("note: well under the limit, check nothing is missing")

# ---- compatibility warnings ----
CJK_FONTS = {"Microsoft YaHei", "微软雅黑", "DengXian", "等线", "PingFang SC", "SimHei", "黑体", "SimSun", "宋体",
             "Source Han Sans SC", "Noto Sans CJK SC", "Noto Sans SC", "Source Han Serif SC", "KaiTi", "楷体",
             "FangSong", "仿宋", "Hiragino Sans GB", "STHeiti", "STSong"}
warnings = []
for i, s in enumerate(slides, 1):
    xml = z.read(s).decode("utf8")
    if re.search(r"<a:t>[^<]*[\u4e00-\u9fff]", xml):
        bad = {f for f in re.findall(r'<a:ea typeface="([^"]*)"', xml) if f not in CJK_FONTS and not f.startswith("+")}
        if bad:
            warnings.append(f"slide {i}: Chinese text may use non-Chinese font {sorted(bad)}; run fix_fonts.py")
media = [n for n in names if n.startswith("ppt/media/")]
for n in media:
    ext = n.rsplit(".", 1)[-1].lower()
    if ext in {"webp", "svg", "gif", "heic", "tif", "tiff"}:
        warnings.append(f"{n}: .{ext} may not show in WPS or older PowerPoint; use PNG or JPG")
    if ext in {"mov", "avi", "mkv", "wmv", "webm", "m4v"}:
        warnings.append(f"{n}: .{ext} video; use MP4 (H.264) for both apps")
    if ext == "mp4" and shutil.which("ffprobe"):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as t:
            t.write(z.read(n))
        try:
            info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                              "stream=codec_name", "-of", "json", t.name],
                                             capture_output=True, text=True).stdout or "{}")
            codec = (info.get("streams") or [{}])[0].get("codec_name", "?")
            if codec != "h264":
                warnings.append(f"{n}: video codec {codec}; re-encode to H.264 for WPS")
        finally:
            os.unlink(t.name)
size_mb = os.path.getsize(a.pptx) / 1e6
if size_mb > 100:
    warnings.append(f"file is {size_mb:.0f} MB; compress videos/images (large files open slowly in WPS)")
if warnings:
    print("\nWARNINGS (compatibility)"); [print(" -", w) for w in warnings]

if problems:
    print("\nFAIL"); [print(" -", p) for p in problems]; sys.exit(1)
print("\nOK")
