#!/usr/bin/env python3
"""Compose header.png, works.png, and README.md from template/config.json."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "template" / "config.json").read_text(encoding="utf-8"))
BANNER = ROOT / "template" / "banner-source.png"
OUT_HEADER = ROOT / "assets" / "header.png"
OUT_WORKS = ROOT / "assets" / "works.png"
OUT_README = ROOT / "README.md"

SERIF_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

BONE = (236, 228, 214, 255)
MUTE = (196, 184, 164, 230)
RED = (194, 59, 34, 255)
GOLD = (196, 164, 106, 230)


def font(path: str, size: int, idxs=(3, 0, 1)) -> ImageFont.FreeTypeFont:
    if path.endswith(".ttf"):
        return ImageFont.truetype(path, size)
    for idx in idxs:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except Exception:
            continue
    return ImageFont.truetype(path, size)


def compose_header() -> None:
    banner = Image.open(BANNER).convert("RGBA")
    w, h = 1400, 520
    bw, bh = banner.size
    scale = max(w / bw, h / bh)
    nb = banner.resize((int(bw * scale), int(bh * scale)), Image.Resampling.LANCZOS)
    top = max(0, (nb.height - h) // 2)
    nb = nb.crop((0, top, w, top + h))

    grad = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(grad)
    for x in range(560):
        a = int(185 * (1 - x / 560) ** 1.1)
        gd.line([(x, 0), (x, h)], fill=a)
    veil = Image.new("RGBA", (w, h), (12, 10, 8, 0))
    veil.putalpha(grad)
    nb = Image.alpha_composite(nb, veil)

    draw = ImageDraw.Draw(nb)
    draw.text((72, 72), CFG["login"], font=font(SANS, 16), fill=GOLD)
    draw.rectangle([72, 102, 118, 106], fill=RED)
    draw.text((72, 122), CFG["name"], font=font(SERIF_BOLD, 92), fill=BONE)
    draw.text((76, 236), CFG["line1"], font=font(SERIF, 26), fill=BONE)
    draw.text((76, 280), CFG["line2"], font=font(SERIF, 26), fill=BONE)
    draw.text((76, 340), CFG["meta"], font=font(MONO, 14), fill=GOLD)
    draw.text((76, 378), CFG["place"], font=font(SANS, 16), fill=MUTE)

    OUT_HEADER.parent.mkdir(parents=True, exist_ok=True)
    nb.convert("RGB").save(OUT_HEADER, "PNG", optimize=True)


def compose_works() -> None:
    cw, ch = 1400, 280
    card = Image.new("RGBA", (cw, ch), (14, 12, 10, 255))
    cd = ImageDraw.Draw(card)
    cd.rectangle([0, 0, cw, 2], fill=GOLD)
    items = CFG["cards"]
    gap = 16
    x0, y0 = 24, 28
    box_w = (cw - 48 - gap * (len(items) - 1)) // len(items)
    box_h = 224
    f_k = font(SERIF_BOLD, 32)
    f_r = font(SANS, 17)
    f_d = font(MONO, 14)
    for i, item in enumerate(items):
        x = x0 + i * (box_w + gap)
        cd.rounded_rectangle(
            [x, y0, x + box_w, y0 + box_h],
            radius=10,
            fill=(22, 19, 16, 255),
            outline=(48, 40, 32, 255),
            width=1,
        )
        cd.rectangle([x, y0, x + 6, y0 + box_h], fill=RED)
        cd.text((x + 18, y0 + 28), item["title"], font=f_k, fill=BONE)
        cd.text((x + 18, y0 + 96), item["repo"], font=f_r, fill=GOLD)
        cd.text((x + 18, y0 + 168), item["note"], font=f_d, fill=MUTE)
    card.convert("RGB").save(OUT_WORKS, "PNG", optimize=True)


def write_readme() -> None:
    cards = CFG["cards"]
    nav = "\n  &nbsp;·&nbsp;\n  ".join(
        f'<a href="{c["url"]}">{c["title"]}</a>' for c in cards
    )
    alt = " ".join(c["title"] for c in cards)
    pages = "\n  ·\n  ".join(f'<a href="{p["url"]}">{p["label"]}</a>' for p in CFG["pages"])
    pages += f'\n  ·\n  <a href="https://github.com/{CFG["login"]}">@{CFG["login"]}</a>'
    blurbs = "\n".join(CFG["blurbs"][c["repo"]] for c in cards)
    also = " · ".join(f'[{a["label"]}]({a["url"]})' for a in CFG["also"])
    text = f'''<p align="center">
  <img src="assets/header.png" alt="{CFG["name"]}" width="900">
</p>

<p align="center">
  {nav}
</p>

<p align="center">
  <img src="assets/works.png" alt="{alt}" width="900">
</p>

<p align="center">
  {pages}
</p>

---

{blurbs}

Also: {also}
'''
    OUT_README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    compose_header()
    compose_works()
    write_readme()
    print(f"wrote {OUT_HEADER}")
    print(f"wrote {OUT_WORKS}")
    print(f"wrote {OUT_README}")
