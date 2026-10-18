"""Give Chinese text a real Chinese font, in slides and notes, for PowerPoint and WPS.

Usage: python fix_fonts.py in.pptx out.pptx [--cjk "Microsoft YaHei"]

pptxgenjs writes the same font for Latin and East Asian text, so Chinese in an
"Arial" box is left to each app's fallback, and PowerPoint and WPS fall back
differently. This sets every East Asian font that is not a Chinese font to --cjk,
including the theme fonts, so both apps show the same thing.
"""
import argparse, re, zipfile

CJK_FONTS = {"Microsoft YaHei", "微软雅黑", "DengXian", "等线", "PingFang SC", "SimHei", "黑体",
             "SimSun", "宋体", "Source Han Sans SC", "Noto Sans CJK SC", "Noto Sans SC", "Source Han Serif SC",
             "KaiTi", "楷体", "FangSong", "仿宋", "Hiragino Sans GB", "STHeiti", "STSong"}

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--cjk", default="Microsoft YaHei", help="font for Chinese text")
a = ap.parse_args()

pat = re.compile(r'<a:ea typeface="([^"]*)"')
changed = 0


def fix(m):
    global changed
    face = m.group(1)
    if face in CJK_FONTS or face.startswith("+"):
        return m.group(0)
    changed += 1
    return f'<a:ea typeface="{a.cjk}"'


zin = zipfile.ZipFile(a.src)
zout = zipfile.ZipFile(a.dst, "w", zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    d = zin.read(it.filename)
    if re.match(r"ppt/(slides/slide|notesSlides/notesSlide|slideLayouts/slideLayout|slideMasters/slideMaster|theme/theme)\d+\.xml$", it.filename):
        s = pat.sub(fix, d.decode("utf8"))
        if it.filename.startswith("ppt/theme/"):
            s = re.sub(r'(<a:(?:major|minor)Font>.*?)<a:ea typeface=""', lambda m: m.group(1) + f'<a:ea typeface="{a.cjk}"', s, flags=re.S)
        d = s.encode("utf8")
    zout.writestr(it, d)
zout.close()
print(f"set {changed} East Asian font entries to {a.cjk}")
