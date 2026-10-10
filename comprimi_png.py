# -*- coding: utf-8 -*-
"""Riduce il peso dei grafici (grafico_png, base64) in esercizi.json: quantizza a 64 colori.
Da lanciare dopo build_esame.py:  python3 comprimi_png.py"""
import base64, io, json, sys
from PIL import Image

def comprimi(b64):
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
    q = im.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out = io.BytesIO(); q.save(out, format="PNG", optimize=True)
    nuovo = base64.b64encode(out.getvalue()).decode("ascii")
    return nuovo if len(nuovo) < len(b64) else b64

def main(path):
    d = json.load(open(path, encoding="utf8"))
    prima = dopo = 0
    for banco in d["esercizi"].values():
        for lista in banco.values():
            for e in lista:
                g = e.get("grafico_png")
                if g:
                    prima += len(g); e["grafico_png"] = comprimi(g); dopo += len(e["grafico_png"])
    json.dump(d, open(path, "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
    print(f"grafici: {prima/1e6:.2f} MB -> {dopo/1e6:.2f} MB")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "esercizi.json")
