"""Split speaker-note text into one paragraph per line (WPS otherwise shows one block).

Usage: python fixnotes.py in.pptx out.pptx
Lines containing Chinese characters are tagged zh-CN so spell-check and fonts behave.
"""
import zipfile, re, sys

src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
pat = re.compile(r'<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>(.*?)</a:t></a:r>(.*?)</a:p>', re.S)


def rep(m):
    out = []
    for ln in m.group(1).split("\n"):
        if not ln.strip():
            out.append('<a:p><a:endParaRPr lang="en-US" dirty="0"/></a:p>')
        else:
            lang = "zh-CN" if re.search(r"[\u4e00-\u9fff]", ln) else "en-US"
            out.append(f'<a:p><a:r><a:rPr lang="{lang}" altLang="en-US" dirty="0"/><a:t>{ln}</a:t></a:r></a:p>')
    return "".join(out)


for it in zin.infolist():
    d = zin.read(it.filename)
    if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", it.filename):
        s, n = pat.subn(rep, d.decode("utf8"), count=1)
        if n:
            d = s.encode("utf8")
    zout.writestr(it, d)
zout.close()
