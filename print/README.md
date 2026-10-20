# Printable modules

Printable (A4 PDF) versions of the learning modules, for students who work on paper. The layout follows the house style of the printed modules: study guide, prerequisite check with *Kotak Ingat* boxes, sub-chapters (Konsep, Rumus, Contoh, Contoh Bertahap, Jebakan, Latihan from Mudah to Sulit), mixed practice, *Soal Setara TKA*, Uji Kompetensi with confidence boxes, review schedule, formula summary, and a full answer key.

| File | What it is |
|---|---|
| `<id>/content.py` | The module's text and items. `check()` re-derives every numeric answer; the tests run it. |
| `<id>/render.py` | Lays the content out as print HTML (`<id>/modul.html`, not committed). |
| `print.mjs` | Prints that HTML to PDF with Chromium (Playwright). |
| `<id>.pdf` | The finished PDF. `scripts/build.py` copies it to `docs/modul-<id>.pdf`, and the module page links to it. |

To rebuild after editing `content.py` (from the repository root):

```bash
python print/vektor-gerak/render.py
NODE_PATH="$(npm root -g)" node print/print.mjs print/vektor-gerak/modul.html print/vektor-gerak.pdf "Modul Vektor dan Gerak · Fisika SMA Kelas X–XI"
python scripts/build.py
```

Playwright with Chromium is needed only for the PDF step (it is preinstalled in the cloud environment). The fonts are Inter and DejaVu Serif. CI does not rebuild the PDF, so commit the regenerated `<id>.pdf` together with the `content.py` change.

The printable module and the interactive page (`data/modules/<id>.json`) have separate item sets: the PDF has more practice and an Uji Kompetensi, the page has instant answer checking.
