"""Check which tools this computer has, and say how to install the missing ones.

Usage: python check_env.py

Required:  Python 3.8+, python-pptx, Pillow, numpy, Node.js, pptxgenjs
Optional:  LibreOffice (soffice)  -> preview images, automatic logo colour
           poppler (pdftoppm)     -> preview images, automatic logo colour
           ffmpeg / ffprobe       -> convert videos to MP4, check video codec
Works the same under Claude, Codex and DeepSeek Harness: it only needs a shell.
"""
import importlib, platform, shutil, subprocess, sys

osname = platform.system()  # Darwin / Windows / Linux
ok = True


def line(status, name, note=""):
    print(f"  [{status}] {name}{(' - ' + note) if note else ''}")


def hint(mac, win, linux):
    return {"Darwin": mac, "Windows": win}.get(osname, linux)


print("Required")
if sys.version_info < (3, 8):
    ok = False; line("missing", "Python 3.8+", f"found {platform.python_version()}")
else:
    line("ok", f"Python {platform.python_version()}")
for mod, pkg in [("pptx", "python-pptx"), ("PIL", "Pillow"), ("numpy", "numpy")]:
    try:
        importlib.import_module(mod); line("ok", pkg)
    except ImportError:
        ok = False; line("missing", pkg, f"pip install {pkg}")

node = shutil.which("node")
if not node:
    ok = False; line("missing", "Node.js", hint("brew install node", "winget install OpenJS.NodeJS", "install Node.js 18+ from nodejs.org"))
else:
    line("ok", "Node.js " + subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip())
    found = subprocess.run([node, "-e", "require.resolve('pptxgenjs')"], capture_output=True).returncode == 0
    if not found:
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, shell=(osname == "Windows")).stdout.strip()
        found = bool(root) and subprocess.run([node, "-e", f"require.resolve('{root}/pptxgenjs'.replace(/\\\\/g,'/'))"],
                                              capture_output=True).returncode == 0
    if found:
        line("ok", "pptxgenjs")
    else:
        ok = False; line("missing", "pptxgenjs", "npm install -g pptxgenjs  (then run node with NODE_PATH=$(npm root -g))")

print("Optional")
soffice = shutil.which("soffice") or shutil.which("libreoffice")
if osname == "Darwin" and not soffice:
    import os
    mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    soffice = mac_path if os.path.exists(mac_path) else None
line("ok" if soffice else "skip", "LibreOffice",
     "" if soffice else "no previews; add_logo.py needs --dark to pick logo colours. " + hint("brew install --cask libreoffice", "winget install TheDocumentFoundation.LibreOffice", "apt install libreoffice"))
line("ok" if shutil.which("pdftoppm") else "skip", "poppler (pdftoppm)",
     "" if shutil.which("pdftoppm") else hint("brew install poppler", "install poppler and add it to PATH", "apt install poppler-utils"))
line("ok" if shutil.which("ffmpeg") else "skip", "ffmpeg",
     "" if shutil.which("ffmpeg") else hint("brew install ffmpeg", "winget install Gyan.FFmpeg", "apt install ffmpeg"))

print("\nReady to build decks." if ok else "\nInstall the missing required tools, then run this again.")
sys.exit(0 if ok else 1)
