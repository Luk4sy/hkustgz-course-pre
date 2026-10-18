"""Cut a logo out of its white background.

Usage: python logo_cutout.py logo.png [--out-dir .]
Writes logo_color.png (transparent background) and logo_white.png (all-white, for dark slides).
"""
import argparse, os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("logo"); ap.add_argument("--out-dir", default=".")
a = ap.parse_args()

rgb = np.asarray(Image.open(a.logo).convert("RGB")).astype(float)
alpha = np.clip((255 - rgb.min(axis=2)) / 255 * 1.15, 0, 1)
safe = np.where(alpha > 0, alpha, 1)[..., None]
color = np.clip((rgb - 255 * (1 - alpha[..., None])) / safe, 0, 255)  # un-premultiply against white
a8 = (alpha * 255).astype(np.uint8)
Image.fromarray(np.dstack([color.astype(np.uint8), a8]), "RGBA").save(os.path.join(a.out_dir, "logo_color.png"))
white = np.full_like(rgb, 255).astype(np.uint8)
Image.fromarray(np.dstack([white, a8]), "RGBA").save(os.path.join(a.out_dir, "logo_white.png"))
print("wrote logo_color.png and logo_white.png")
