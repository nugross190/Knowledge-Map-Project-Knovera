# Printable modules

Printable (A4 PDF) versions of the learning modules, for students who work on paper. The layout follows the house style of the printed modules: study guide, prerequisite check with *Kotak Ingat* boxes, sub-chapters (Konsep, Rumus, Contoh, Contoh Bertahap, Jebakan, Latihan from Mudah to Sulit), mixed practice, *Soal Setara TKA*, Uji Kompetensi with confidence boxes, review schedule, formula summary, and a full answer key.

| File | What it is |
|---|---|
| `<id>/content.py` | The module's text and items. `check()` re-derives every numeric answer; the tests run it. |
| `<id>/render.py` | Lays the content out as print HTML (`<id>/modul.html`, not committed). |
| `print.mjs` | Prints that HTML to PDF with Chromium (Playwright). |
| `modlib.py` | Shared page builder: a module's `render.py` calls `modlib.build(content, path)`, and `content.META` holds the module-specific text (cover, study guide, summary page, teacher's note). Used by `gerak-vertikal` and later modules; older modules keep their own `render.py`. |
| `kit.py` | Content helpers: Indonesian number format, item builder, seeded noisy data, least-squares slope, and `balance_keys`. |
| `graphs.py` | Shared motion model and the fixed graph templates (GLB, GLBB, combined motion, tracking data). An item adds a motion, data points or a line to a template; graphs and keys come from the same model, and every segment corner must sit on a gridline. |
| `<id>.pdf` | The finished PDF. `scripts/build.py` copies it to `docs/modul-<id>.pdf`, and the module page links to it. |

Modules: `vektor-gerak` (Vektor dan Gerak, kelas X–XI), `gerak-lurus` (Gerak Lurus, kelas X), `gerak-vertikal` (Gerak Vertikal, kelas X), `gerak-parabola` (Gerak Parabola, kelas X–XI), `eksponen-logaritma` (Eksponen dan Logaritma, Matematika kelas X), `vektor` (Vektor dan Operasinya, Matematika kelas X), `trigonometri` (Trigonometri, Matematika kelas X) and `fungsi-linear` (Fungsi Linear dan Persamaan Garis, Matematika kelas X).

Draft among sequence (see the among generator spec, not yet in `specs/`): `jembatan-gerak-lurus` (Jembatan ke Gerak Lurus, Fisika kelas X), a bridge booklet for classes with weak prerequisites, Steps 0–3 plus a praxis card. It has its own `render.py` layout (codification, translation drill, three support levels, product before discussion) and reuses `modlib.CSS`.

Content files list each multiple-choice item with its key first; at render time `kit.balance_keys` rotates the options so keys spread evenly over A–E and relabels the "pilihan salah" notes to match. Write those notes as letter groups followed by a colon ("B, C: …"); a letter used as a name (mobil A) is left alone. Only modules with an interactive page in `data/modules/` are copied to `docs/`.

To rebuild after editing `content.py` (from the repository root):

```bash
python print/vektor-gerak/render.py
NODE_PATH="$(npm root -g)" node print/print.mjs print/vektor-gerak/modul.html print/vektor-gerak.pdf "Modul Vektor dan Gerak · Fisika SMA Kelas X–XI"
python scripts/build.py
```

Playwright with Chromium is needed only for the PDF step (it is preinstalled in the cloud environment). The fonts are Inter and DejaVu Serif. CI does not rebuild the PDF, so commit the regenerated `<id>.pdf` together with the `content.py` change.

The printable module and the interactive page (`data/modules/<id>.json`) have separate item sets: the PDF has more practice and an Uji Kompetensi, the page has instant answer checking.
