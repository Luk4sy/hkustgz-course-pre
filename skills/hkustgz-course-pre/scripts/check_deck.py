"""Check a finished .pptx before you present it.

Usage: python check_deck.py deck.pptx --minutes 8 [--wpm 140]

Checks, per slide:
  - [CLICK] markers in the notes = click steps in the animation sequence
  - the slide has speaker notes
Checks for the whole deck:
  - spoken time (English note words / wpm) fits in 90% of the time limit
Exit code 1 if anything fails, so it can run in a script.
"""
import argparse, re, sys, zipfile

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

if problems:
    print("\nFAIL"); [print(" -", p) for p in problems]; sys.exit(1)
print("\nOK")
