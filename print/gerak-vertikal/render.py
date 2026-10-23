"""Render content.py into modul.html; print/print.mjs turns it into print/gerak-vertikal.pdf.

Usage (from the repository root):
    python print/gerak-vertikal/render.py
    NODE_PATH="$(npm root -g)" node print/print.mjs print/gerak-vertikal/modul.html print/gerak-vertikal.pdf "Modul Gerak Vertikal · Fisika SMA Kelas X"
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import content as C  # noqa: E402
import modlib  # noqa: E402

assert C.check()
modlib.build(C, Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "modul.html")
