# Learning path spec (pilot)

Status: pilot, 2026-11. The first path is `data/jalur/pengukuran.json` (Fisika kelas X, Besaran dan Pengukuran). Expect the format to change after classroom use.

A learning path (*jalur belajar*) is one JSON file, `data/jalur/<id>.json`, rendered by `templates/_jalur.html` into `docs/jalur-<id>.html`. A module (`specs/module-spec.md`) is a lesson list plus staged exercises the student browses freely. A path is a self-paced sequence of short cards with support built in: a prerequisite check that routes to bridges, worked examples that fade into practice, a help ladder, feedback keyed to named mistakes, mastery on fresh numbers, and spaced review. The design follows the research summary that led to it: short units only work when they end in retrieval, return later, and keep a teacher in the loop.

## 1. Structure

```
path
├── id, kode, subject, map, src, title, lead, blurb
├── sesi_menit               session length before the page suggests stopping (default 15)
├── ulang_hari[]             review intervals in days for boxes 1, 2, 3, ... (default [1, 3, 7, 21])
├── prasyarat[]              prerequisite skills
│   ├── id (P1, P2, ...), judul, kenapa, untuk[] (unit ids)
│   ├── cek[]                two item ids; variant a is the first check, variant b the re-check after the bridge
│   └── jembatan             {isi[] blocks, soal: item id}
├── unit[]                   units in teaching order
│   ├── id (U1, U2, ...), judul, simpul[], butuh[] (prerequisite ids)
│   ├── kait                 {teks, soal: item id}: a scene and a prediction question
│   ├── media                {judul, alat[] widget names, data, isi[] blocks}
│   ├── lihat                {soal, langkah[], fig?, p?}: a worked example, revealed one step at a time
│   ├── bersama              item id of a "bertahap" item: the same task with blanks for each step
│   ├── sendiri[]            item ids of practice families, each mastered on fresh variants
│   ├── ringkas[]            the unit's main points
│   └── lanjut               the open question the next unit answers
├── akhir                    {judul, teks, soal[] item ids}: mixed practice and TKA-style items
├── miskonsepsi              {M01: {judul, teks}, ...}: named mistakes, shown when a wrong answer matches
├── soal[]                   every item (family); see 3
└── catatan[]                teacher notes: judul + items[]
```

Blocks (`isi`) are the module blocks: each exactly one of `p`, `li`, `tabel`, `contoh`, `jebakan`.

## 2. Widgets

`media.alat` names widgets drawn by the page. `media.data` holds the content-specific values a widget needs, so no subject text lives in the template.

| Widget | Shows | `data` keys |
|---|---|---|
| `satuan` | One desk measured in different non-standard units | `panjang_cm`, `satuan[]` ({nama, cm}) |
| `mistar` | A ruler, an object with movable ends, and a parallax toggle | none |
| `jangka-sorong` | Vernier caliper scales (main scale and 10-division vernier) at any opening | none |
| `mikrometer` | Micrometer sleeve and thimble at any reading | none |
| `angka-penting` | A number with each digit marked significant, not significant, or ambiguous | `contoh[]` |
| `geser-koma` | A number whose decimal comma moves while the power of ten keeps the value | `contoh[]` |
| `dimensi` | Candidate formulas and the dimensions of each side | `set[]` ({tanya, calon[]: {rumus, uraian, cocok}}) |

Item figures use the same drawings: an item with `fig` (`mistar`, `jangka-sorong`, `mikrometer`) is drawn from its variant's `p`.

## 3. Items

An item is a family of one or more variants that test the same thing with different numbers or contexts. Saved progress is keyed by the family id, so the family id is **permanent** (`<kode>-NNN`, never renumbered or reused). Variants are listed in order and keyed by position; add new variants at the end.

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | `<kode>-NNN`, unique. |
| `format` | MUST | `isian`, `bertahap`, `pilihan-ganda`, `pilihan-ganda-kompleks`, or `benar-salah`. |
| `simpul` | SHOULD | Map topic the item practises. |
| `bantuan` | MUST | One or two hints, from a nudge to the first step done. The third rung of the ladder is the worked solution of a sibling variant ("contoh kembar"), so a practice family needs at least two variants. |
| `gen` | MAY | Name of the generator in `scripts/jalur.py` that produced the variants. The build recomputes each variant from its `p` and stops on any difference in `kunci`, `opsi`, `langkah` keys or `salah` values. |
| `fig` | MAY | Figure drawn from each variant's `p`. |
| `tka` | MAY | As in the module spec: `{"tipe", "acuan"}`. |
| `varian[]` | MUST | At least one variant. |

Variant fields: `soal` (stem), `p` (generator parameters, with `gen` or `fig`), `pembahasan` (list of steps), and per format:

| Format | Fields |
|---|---|
| `isian` | `kunci` (number), `satuan`, optional `toleransi`, optional `cek_ap` (the answer must also have that many significant figures), optional `salah`: [{nilai, m}] |
| `bertahap` | `langkah`: [{teks, kunci, satuan?, toleransi?, salah?}], one numeric blank per step |
| `pilihan-ganda` | `opsi`, `kunci` (index), optional `salah`: {"<option index>": "<misconception id>"} |
| `pilihan-ganda-kompleks` | `opsi`, `kunci` (sorted index list), optional `salah` as above |
| `benar-salah` | `opsi` (statements), `kunci` (true/false per statement), `kolom` |

Default tolerance for a numeric key is 0,4 of its last decimal place (23,7 accepts 23,66 to 23,74), so readings must be exact to the instrument's precision. Answers may be typed with a comma or a point, and as a fraction (`1/2`).

## 4. Support rules (what the page does)

- **Prerequisite check.** Variant a of both check items per prerequisite. A prerequisite with a wrong answer gets its bridge as the first card of the first unit that needs it, followed by the re-check (variant b). The result is shown to the teacher; the path never locks.
- **Cards per unit:** kait → media → lihat → bersama → one card per practice family → ringkas.
- **Confidence before checking.** Yakin, ragu or nebak. A confident wrong answer is counted and reported.
- **Help ladder.** Bantuan 1, bantuan 2, then contoh kembar. The worked solution of the item itself opens after a correct answer or after two wrong tries; opening the twin or the solution marks the attempt as helped.
- **Keyed feedback.** A wrong answer that matches a `salah` entry shows that misconception's card and counts it.
- **Mastery.** Two correct answers in a row on fresh variants, without help, mark a family *bisa*. After three attempts the student may skip (*dibantu*); the family returns in review.
- **Spaced review.** A mastered family enters box 1 and returns after `ulang_hari[0]` days; a correct review moves it up a box, a wrong one sends it back. Box 3 or higher is *kuat*. Each session opens with up to three due reviews.
- **Bounded session.** After `sesi_menit` minutes the page suggests stopping at the next card boundary.
- **Teacher code.** The student types a name and gets one line of text: status per family, prerequisite results, top misconceptions and the confident-wrong count. The teacher pastes the lines of a class into the page's teacher view (`#guru`) and sees a table and the most common mistakes. The code is not secure; it is a reporting aid, not an exam record.

Progress lives in the student's browser (`localStorage`), like the other pages.

## 5. Writing rules

- Module-spec §3 applies: compute every key and numerical distractor in a script, state every quantity the solution needs, Indonesian with decimal commas, Unicode formulas.
- Every `salah` value or option names a real, common mistake, written in `miskonsepsi`.
- Avoid numbers whose rounding depends on the rule for a dropped digit of exactly 5 (textbooks disagree); the generators refuse them.
- Avoid integers with trailing zeros where significant figures matter; their count is ambiguous without scientific notation.

## 6. What the build checks

`validate_jalur` in `scripts/jalur.py` stops the build on: missing fields, an id that does not match the file name, item ids not `<kode>-NNN` or duplicated, references to unknown items, units, prerequisites, misconceptions or map topics, a practice family with fewer than two variants, keys that do not fit the format, unknown widgets or figures, a TKA type or `acuan` that does not exist, and any generated variant that differs from its generator's output.
