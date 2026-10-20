# Module spec

A learning module (*modul belajar*) is one JSON file, `data/modules/<id>.json`, rendered by `templates/_modul.html` into `docs/modul-<id>.html`. A map summarises a whole subject; a module teaches one cross-cutting skill and drills it with staged exercises. `data/modules/vektor-gerak.json` is the reference example.

## 1. Structure

```
module
├── id, kode, subject, map, title, lead, blurb, src
├── tujuan[]                 learning goals
├── materi[]                 lessons
│   ├── id, judul, simpul[]
│   └── isi[]                blocks, each exactly one of: p, li[], tabel{cols, rows}, contoh{soal, langkah[]}, svg (+ cap), jebakan[]
├── tahap[]                  exercise stages, easiest first
│   ├── tahap (1, 2, 3, ...), nama, tujuan
│   └── soal[]               items
└── catatan[]                each: judul + items[]
```

## 2. Fields

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | Lowercase slug, identical to the file name. |
| `kode` | MUST | 2–5 uppercase letters; prefix of every item id (`VKG`). |
| `map` | SHOULD | Id of the subject map in `data/maps/`. Every `simpul` code in the module MUST exist in that map; the page links to those topics, and the map's home-page card links to the module. |
| `title`, `lead`, `blurb` | MUST, MUST, SHOULD | As in map-spec; `blurb` is shown on the home-page card. |
| `materi[].simpul` | SHOULD | Map topic codes the lesson draws on. |
| `materi[].isi` | MUST | Lesson blocks. Every lesson SHOULD end with a worked `contoh`; `svg` is an inline diagram that uses `currentColor` and `var(--accent)` so it works in both themes. |
| `tahap` | MUST | At least 3 stages (lint), numbered from 1 in order, each with at least 4 items (lint). Difficulty rises with the stage number; the last stage SHOULD be at TKA level 3. |

### Items

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | `<kode>-NNN`, unique. **Permanent**: saved progress is keyed by id. Add new items with the next free number; never renumber or reuse one. |
| `format` | MUST | `isian` (number), `pilihan-ganda`, `pilihan-ganda-kompleks`, or `benar-salah`. |
| `soal` | MUST | Stem. `\n` separates paragraphs; `[Tabel]` marks where `tabel` (a list of rows, first row = header) appears. |
| `opsi`, `kunci`, `kolom` | MUST | As in `specs/tka-spec.md` for the three TKA formats. For `isian`: `kunci` is a number and `satuan` the unit. |
| `toleransi` | MAY | `isian` only: accepted absolute error. Default: 1% of the key, at least 0,01. |
| `petunjuk` | MUST | One hint that names the first step without giving the answer. |
| `pembahasan` | MUST | Worked solution as a list of steps. For multiple choice, name the mistake behind each numerical distractor. |
| `simpul` | SHOULD | The map topic the item practises. |
| `tka` | MAY | `{"tipe": "<FIS-...>", "acuan": [ids]}` marks a TKA-style item. The type MUST exist in `data/tka-types.json`, the format MUST be one the type allows, and `acuan` MUST list transcribed examples of that type. |

## 3. Writing rules

- Compute every numeric key and every numerical distractor in a script before writing the item, and keep the story consistent with the numbers (`specs/tka-templates/<subject>.md` §2).
- State every quantity the solution needs: g, the sin and cos values of non-standard angles, which direction is positive, and from where an angle is measured.
- TKA-style items follow the subject template's type rules and are original; they are never presented as official items.
- Indonesian, decimal comma, Unicode formulas (converted to `<sup>`/`<sub>` on load, except inside `svg`).

## 4. Printable version

A module MAY have a printable PDF, `print/<id>.pdf`, made from `print/<id>/content.py` (see `print/README.md`). The build copies it to `docs/modul-<id>.pdf` and the page shows a "Versi cetak (PDF)" button. Its items follow the same writing rules (§3); `content.check()` MUST re-derive every numeric answer, and the tests run it.

## 5. What the build checks

`validate_module` in `scripts/build.py` stops the build on structural errors (fields, ids, stage numbering, keys per format, unknown map topics, TKA type, format and `acuan`). `lint_module` warns on fewer than 3 stages, a stage with fewer than 4 items, no TKA-style items, or no `blurb`.
