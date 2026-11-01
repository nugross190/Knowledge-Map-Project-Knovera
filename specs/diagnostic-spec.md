# Diagnostic item spec (literacy and numeracy)

Status: draft, 2026-11-01. No items have been written to it yet. The first items and the HADIR changes (§14) follow once the owner approves the direction. Values marked *(proposal)* are starting points to test in the pilot; they come from no official source.

The diagnostic runs in HADIR's exam module. For each student it shows the fase at which they read and do mathematics, and where the gaps are. It replaces HADIR's 18 fixed subtests (R1–R6, M1–M7, S1–S5 in `services/ujian_diagnostik.py`). Those mixed three different things in one list: basic fluency, thinking process, and content. Here those become separate tags on each item (§4), placed on one fase ladder (§5).

## 1. Sources

| Source | Used for | Status |
|---|---|---|
| [`data/cp/`](../data/cp/): CP 2025 (Keputusan Kepala BSKAP 046/H/KR/2025, 16 July 2025) | The official wording per fase and element; every item cites one capaian (§2) | Copied verbatim from the official PDF and checked word for word against it |
| AKM (Asesmen Kompetensi Minimum, Kemendikbud) | The three item tags (content, process, context), the five item forms, the four result-level names | From secondary sources ([akupintar](https://akupintar.id/info-pintar/-/blogs/komponen-asesmen-kompetensi-minimum), [quipper](https://www.quipper.com/id/blog/tips-trick/school-life/akm/)); the official AKM framework document was not read |
| PISA (OECD) | Units: one stimulus with several items; result levels described by what students can do | [PISA 2018 frameworks](https://t4.oecd.org/pisa/pisaproducts/PISA-2018-draft-frameworks.pdf) |
| EGRA / EGMA (RTI, USAID) | The subtasks behind the basic-skills screener (§9) | [UNESCO GAML 2023](https://tcg.uis.unesco.org/wp-content/uploads/sites/4/2023/12/9.-GAML_2023_USAID-presentation_final.pdf) |
| NWEA MAP Growth | One vertical scale across grades; adaptive delivery as a later goal (§11) | [Family guide](https://www.nwea.org/uploads/FamilyGuidetoMAPGrowth.pdf) |

## 2. The CP files

`data/cp/<subject id>.json`, one per subject. The file name is the subject's id in `data/subjects.json`. Bahasa Indonesia and Matematika exist; others are added the same way when a diagnostic needs them.

| Field | Meaning |
|---|---|
| `id`, `mapel`, `prefix` | Subject id, name, and the code prefix of its capaian (`BIN`, `MAT`) |
| `sumber` | The decree, its date, the part copied (Lampiran II, section and letter), and how the text was copied |
| `fase[]` | `fase` (A–F), `kelas` (grades as Roman numerals), `kelas_teks` (the decree's own wording) |
| `elemen[]` | `kode`, `nama`, `jenis` (`konten`, or `proses` for Matematika's process elements), `deskripsi` |
| `capaian[]` | One per fase × element: `id`, `fase`, `elemen`, `nomor` (the decree's numbering, `4.2`), `teks` (verbatim; paragraphs separated by a blank line), `butir[]`, and `nama_elemen` when the decree names the element differently in that fase |
| `butir[]` | The capaian split at semicolons and paragraph breaks: `id` and `teks`. A leading *dan* or *serta* is dropped; nothing else is changed |
| `catatan[]` | Known oddities in the source: conflicts, typos, an image that was not copied |

**Ids.** A capaian is `<prefix>.<fase>.<elemen>` (`MAT.D.ALJ`) and a butir is `<capaian id>.<n>` (`MAT.D.ALJ.8`). Ids are permanent (CLAUDE.md rule 5). Items cite them, and saved results will depend on them. If a later decree replaces this one, its text goes in new files with a new prefix; existing ids are never reused for different wording.

| Subject | Element codes |
|---|---|
| Bahasa Indonesia (`BIN`) | `SIM` Menyimak · `BAC` Membaca dan Memirsa · `BIC` Berbicara dan Mempresentasikan · `TUL` Menulis |
| Matematika (`MAT`), content | `BIL` Bilangan · `ALJ` Aljabar (named *Aljabar dan Fungsi* in Fase E–F) · `UKR` Pengukuran (Fase A–D only) · `GEO` Geometri · `DAT` Analisis Data dan Peluang |
| Matematika (`MAT`), process | `PNL` Penalaran dan Pembuktian Matematis · `PMS` Pemecahan Masalah Matematis · `KOM` Komunikasi · `REP` Representasi Matematis · `KNK` Koneksi Matematis |

**Known conflict.** The Matematika section labels Fase E "Kelas X dan XI" and Fase F "Kelas XI dan XII". The Bahasa Indonesia section of the same decree gives Fase E as Kelas X only. This project keeps Fase E = kelas X and Fase F = kelas XI–XII (`specs/map-spec.md`). The conflict is recorded in `matematika.json`, not resolved.

`build.py` checks every CP file's structure: id format, known fase and element, one capaian per fase × element, consecutive butir numbers, and the subject listed in the roster.

## 3. What is tested

| Domain | Code | CP basis | In scope |
|---|---|---|---|
| Literasi membaca | `LIT` | Bahasa Indonesia, element Membaca dan Memirsa (`BIN.*.BAC`) | Yes, Fase A–F |
| Numerasi | `NUM` | Matematika, all content elements (`MAT.*.*`) | Yes, Fase A–F |
| Menyimak | — | `BIN.*.SIM` | No. It needs audio items; HADIR shows images only |
| Berbicara, Menulis | — | `BIN.*.BIC`, `BIN.*.TUL` | No. They need spoken or written answers marked with a rubric |
| Sains | — | — | Later, with its own CP file. HADIR's S1–S5 stay until then |

Numeracy in AKM means using mathematics in a situation. The CP also covers mathematics for its own sake. The diagnostic uses both (see `konteks_akm` in §4).

## 4. Item tags

Every item carries these tags. The fase and element come from `cp` and are not entered separately.

| Tag | Values | Rule |
|---|---|---|
| `cp` | A capaian id: `BIN.<fase>.BAC` or `MAT.<fase>.<elemen>` | MUST. Sets the item's domain, fase and content element (§5) |
| `butir` | One or more butir ids of that capaian | SHOULD. MUST for NUM, so coverage can be counted per butir |
| `proses` | LIT: `menemukan`, `interpretasi`, `evaluasi`. NUM: `pemahaman`, `penerapan`, `penalaran` | MUST. AKM's process levels, defined below |
| `proses_cp` | NUM only: `PNL`, `PMS`, `KOM`, `REP`, `KNK` | MAY. The CP's process element when one clearly dominates. One multiple-choice item rarely shows `KOM` or `KNK` well |
| `teks` | `sastra`, `nonsastra` | MUST for LIT, on the unit. The CP's own words; AKM calls them teks fiksi and teks informasi |
| `konteks_akm` | `personal`, `sosial-budaya`, `saintifik`, or `tanpa` (NUM only: no situation) | MUST. AKM's context. Not the `konteks` scene theme of `question-spec.md` §6; an item may carry both |
| `bentuk` | `PG`, `PG_KOMPLEKS`, `BENAR_SALAH`, `MENJODOHKAN`, `ISIAN`, `URAIAN` | MUST. See §7 |
| `unit` | A unit id (§6) | MUST for LIT, SHOULD for NUM when several items share a table or graph |
| `tingkat` | `1`, `2`, `3` | MUST. The author's difficulty guess *within the item's fase*. Replaced by pilot statistics (§11) |
| `pengecoh` | For each wrong option, the misconception that leads to it | SHOULD for PG at NUM. Untagged distractors are allowed but report nothing (§12) |

**LIT processes.**
- `menemukan`: finds information stated in the text (*makna tersurat*).
- `interpretasi`: works out implied meaning (*makna tersirat*), the main idea, the message, or a link between parts. Comparing texts (*membandingkan isi teks*) belongs here.
- `evaluasi`: judges the quality or credibility of a text or claim, reflects on its ideas against reasoning or other sources, or appreciates a literary text.

These are AKM's names, and CP 2025 uses the same verbs. Fase D–F of `BIN.*.BAC` name *makna yang tersurat dan tersirat*, *menginterpretasi*, *mengevaluasi kualitas dan/atau kredibilitas*, *membandingkan isi teks*, *merefleksi* and *mengapresiasi*.

**NUM processes.**
- `pemahaman`: knows a fact, concept or procedure and carries it out.
- `penerapan`: chooses and uses mathematics to solve a routine problem.
- `penalaran`: solves a non-routine problem, generalizes, justifies, or judges a claim.

## 5. Placing an item in a fase

- **P1. Lowest fase that covers it.** Tag the item with the lowest fase whose CP text covers what the item needs. Comparing 3/4 with 2/3 is `MAT.C.BIL`. Fase C has *membandingkan dan mengurutkan berbagai pecahan*, while Fase B only compares unit fractions and fractions with the same denominator.
- **P2. Number ranges are limits (NUM).** Whole numbers to 100 (A), to 10.000 (B), to 1.000.000 (C), then integers, rationals, powers and roots (D). An item whose numbers go past its fase's range moves up a fase.
- **P3. Only what the CP names.** A topic absent from the 2025 CP text gets no capaian, and stays out of the diagnostic even if schools teach it. For example, the Fase E text names exponents but not logarithms.
- **P4. Reading: the CP's demand sets the fase (LIT).** This table is the project's reading of `BIN.*.BAC`. The CP lists no processes per fase; the "processes that fit" column is derived from its verbs.

| Fase | What the CP asks (Membaca dan Memirsa) | Processes that fit |
|---|---|---|
| A | *Membaca kata-kata sederhana dengan fasih*; *memahami isi bacaan* about self, family, health, surroundings | `menemukan` |
| B | *Membaca kata-kata baru dengan fasih*; *memahami ide pokok, ide pendukung, pesan, dan informasi* in sastra and nonsastra | `menemukan`, `interpretasi` |
| C | *Membaca kata-kata dengan berbagai pola kombinasi huruf dengan fasih*; *menganalisis informasi serta nilai-nilai*; visual and audiovisual texts appear | `menemukan`, `interpretasi` |
| D | *makna yang tersurat dan tersirat*; *menginterpretasi* (care, pro/contra); *mengevaluasi kualitas dan/atau kredibilitas … menggunakan sumber informasi lain* | all three |
| E | as D, plus *membandingkan isi teks*; interpreting ideas and feelings (*simpati, peduli, dan empati*) | all three, including items across two texts |
| F | evaluating stated and implied meaning *berdasarkan kaidah logika berpikir*; *merefleksi*; *mengapresiasi* | all three; `evaluasi` items judge the reasoning in a text |

- **P5. Text length (LIT, proposal).** The CP sets no text length. Until the pilot gives data, a unit's main text is about: A up to 50 words; B 50–150; C 150–300; D 250–450; E–F 300–600.
- **P6. Process is not difficulty.** An `evaluasi` item can be easy and a `menemukan` item in a dense text can be hard. Fase, process and `tingkat` are tagged separately.

## 6. Units

A unit is one stimulus with the items about it, as in AKM and PISA.

- **Id.** `<domain>-U<three digits>` (`LIT-U001`), permanent.
- **Size.** 3–5 items *(proposal)*, covering at least two processes. LIT units at Fase D and above SHOULD cover all three.
- **Stimulus types.** A text (`sastra` or `nonsastra`), a table, a graph or diagram, an image, or a combination. The CP stresses visual texts from Fase C, so LIT SHOULD include some non-continuous texts: tables, infographics, schedules, forms.
- **Origin.** Original writing, or a published text with its source and permission noted. Figures in a scene are round, invented and plausible, and are never presented as real data. No real private persons.
- **Independence.** Items in a unit MUST NOT give each other away. The stem of one item never contains the answer to another.
- **LIT needs only the text.** Every LIT item MUST be answerable from the stimulus with the reading skill of its fase; outside knowledge never decides the key.
- **In HADIR.** The stimulus is a passage (`QbPassage`); tables use `stimulus_table`; images use `QbMedia`, which holds images only (no audio or video).

## 7. Item forms and scoring

| Form | AKM form | In HADIR now | HADIR scoring | Notes |
|---|---|---|---|---|
| `PG` | Pilihan ganda | Yes | Right or wrong | 4 options *(proposal)*, one key |
| `PG_KOMPLEKS` | Pilihan ganda kompleks | Yes | Exactly the right set, else wrong | The stem says the number of answers is more than one, or *pilih semua yang benar* |
| `BENAR_SALAH` | — | Yes | Every statement right, else wrong | A table of statements with two columns (*Benar/Salah*, *Sesuai/Tidak sesuai*). HADIR keeps it as its own type |
| `MENJODOHKAN` | Menjodohkan | **No**, needed | Every pair right, else wrong, at first | 3–5 pairs, with one extra option on the right side so the last pair is not free |
| `ISIAN` | Isian | Yes | Matches an accepted answer | Short answer: a number, a word or a short phrase. List every accepted spelling and form (`0,5`, `1/2`) |
| `URAIAN` | Uraian | **No**, needed | Marked by hand with a rubric | Left out of v1 so there is nothing to mark by hand; later for `penalaran` and `KOM` |

Form mix per test *(proposal)*: `PG` at least 50%; `PG_KOMPLEKS` and `BENAR_SALAH` together 25–30%; `ISIAN` 15–20%; `MENJODOHKAN` up to 10% once HADIR has it.

## 8. Writing rules

- **One task per item.** The stem asks exactly one thing and is answerable without reading the options.
- **Grounded in the CP.** The item tests its `butir`, not something next to it. A reviewer who reads only the butir and the item should agree they match.
- **Plausible distractors.** Each wrong option comes from a real misconception or a typical slip, and the `pengecoh` tag names it. No joke options; no *semua benar* or *semua salah*.
- **Fair options.** Options are parallel in grammar and similar in length. Keys are spread evenly over positions across a test.
- **No traps in the wording.** Avoid negative stems. If one is unavoidable, write *bukan* or *tidak* in capitals (*BUKAN*). No double negatives.
- **Plain Indonesian.** The vocabulary in NUM items stays at or below the item's fase, so reading load does not decide a numeracy item.
- **Numbers.** Round values, units on every quantity, Indonesian notation (comma decimals: *0,5*; dot thousands: *10.000*).
- **Respectful scenes.** The rules K3–K5 of `question-spec.md` §6 apply. Describe things students can observe; never the student's own family hardship; no moral verdict as a key; ordinary Indonesian settings.
- **Unverified keys.** An item whose key the author is not sure of is not added. Ask, or leave it out.

## 9. The basic-skills screener (Fondasi)

The CP sets fluent word reading as a goal only for Fase A–C (`BIN.A.BAC.1`, `BIN.B.BAC.1`, `BIN.C.BAC.1`). The screener checks those foundations for students who land below Fase C in the main test. It is a separate short test of about 10 minutes, with its own report. Its tasks are silent and phone-friendly, modelled on EGRA and EGMA subtasks:

| Task | Modelled on | CP butir |
|---|---|---|
| Pick the word that matches a picture | EGRA familiar word reading | `BIN.A.BAC.1` |
| True or false for short sentences | EGRA reading comprehension, at sentence level | `BIN.A.BAC.2`, `BIN.B.BAC.2` |
| A short passage with 3 questions | EGRA reading comprehension | `BIN.B.BAC.2` |
| Read a number; which is bigger | EGMA number identification, quantity discrimination | `MAT.A.BIL.1`, `MAT.B.BIL.1` |
| Missing number in a sentence or pattern | EGMA missing number | `MAT.B.ALJ.1`, `MAT.B.ALJ.2` |
| Addition, subtraction and multiplication facts | EGMA addition/subtraction | `MAT.A.BIL.3`, `MAT.B.BIL.5`, `MAT.B.BIL.6` |
| One-step word problems | EGMA word problems | `MAT.B.BIL.5`, `MAT.B.BIL.6` |

- **Timed sets.** EGRA and EGMA count correct answers per minute. A timed set needs a per-section timer, which HADIR does not have. Until it does, the sets run untimed and the report shows accuracy only.
- **Reading aloud.** Oral reading fluency (words correct per minute) cannot be measured on a phone. A teacher can do it one to one if needed; it is not part of this test.

## 10. Test grid for the first SMA diagnostic (proposal)

One form per domain, about 40 minutes each, for SMA students of all grades. The ladder runs from Fase C to F so that it can show students who work below their grade's fase.

| | LIT (30 items, 6–8 units) | NUM (30 items) |
|---|---|---|
| Fase C / D / E / F | 6 / 12 / 9 / 3 | 6 / 12 / 9 / 3 |
| Process | `menemukan` 30% · `interpretasi` 40% · `evaluasi` 30% (no `evaluasi` below Fase D) | `pemahaman` 30% · `penerapan` 45% · `penalaran` 25% |
| Content | `nonsastra` 60% · `sastra` 40% | `BIL` 25% · `ALJ` 25% · `GEO`+`UKR` 25% · `DAT` 25% |
| Context | each of the three at least 20% | at least two thirds in a situation; at most one third `tanpa` |

Fase D carries the most items because it is the broad base that Fase E–F mathematics and SMA texts build on. With 30 items per domain, results are reliable for each tag on its own, not for combinations (`ALJ` × `penalaran`): each cell would hold only one or two items.

## 11. Delivery and pilot

- **v1 (pilot).** One fixed form per domain; everyone gets the same items, with options shuffled. After the pilot, compute for each item the proportion correct (*p*), its correlation with the total score (point-biserial), and how often each distractor was chosen. Items with *p* below 0.20 or above 0.95, or a correlation below 0.20, are reviewed and fixed or dropped *(proposal; common classical test theory rules of thumb)*. Measured *p* replaces the author's `tingkat`.
- **v2 (two stages).** A 10-item routing block spanning Fase C–E sends each student to one of three 20-item blocks: low (B–D), middle (C–E) or high (D–F). This needs routing support in HADIR.
- **Not planned.** Fully adaptive testing, which needs a large bank of items calibrated on real students.

## 12. Reporting

Per student and domain:

1. **Fase placement** *(proposal)*. Walk up from the lowest fase on the form. A fase counts as passed when the student gets at least two thirds of its items right, and only fases with at least 3 items count. The placement is the last fase passed before the first one failed: *bekerja di Fase D*.
2. **Level for the student's own grade.** The AKM level names *Perlu Intervensi Khusus*, *Dasar*, *Cakap*, *Mahir*. Cut points on the items of the student's grade fase (E for kelas X, F for XI–XII): 0–39%, 40–59%, 60–79%, 80–100% *(proposal; HADIR's current values)*. These are not AKM's official cut scores, which this project has not seen.
3. **Breakdowns.** Percent correct by process and by content element, each on its own, with at least 4 items behind each number *(proposal)*. A number with fewer items is shown greyed out with *sedikit soal*.
4. **Misconceptions.** The tagged distractors the student chose (`pengecoh`).
5. **Fondasi.** The screener's results, when taken, as a separate block.

Per class: how students spread over fase placements, the weakest process and content element, and the most chosen misconceptions.

Before the pilot, placements rest on the authors' fase tags. The report says so: *hasil awal, belum dikalibrasi*.

## 13. Item files

Items carry answer keys and this repository is public, so they live in the private HADIR repository (`nugross190/V2HADIR`, decided by the owner on 2026-11-01). The files are `content/diagnostik/<domain>.json` (`lit.json`, `num.json`), with their pictures in `content/diagnostik/img/`. That folder's README gives the full format. Its test, `tests/test_diagnostik_items.py`, checks ids, CP references, forms and keys, distractor tags and pictures. This repository keeps the rules and the CP text, and nothing here reads the items.

A file has `unit[]` and, for NUM only, `soal[]` of single items outside any unit. Item ids are `<domain>-<four digits>` (`NUM-0001`) and unit ids `<domain>-U<three digits>` (`LIT-U001`), both permanent. One single item:

```json
{
  "id": "NUM-0001",
  "cp": "MAT.C.BIL",
  "butir": ["MAT.C.BIL.6"],
  "proses": "penerapan",
  "konteks_akm": "personal",
  "bentuk": "PG",
  "tingkat": 1,
  "soal": "Ibu membeli 3/4 kg gula dan 2/3 kg tepung. Manakah pernyataan yang benar?",
  "opsi": ["Gula lebih berat daripada tepung.", "Tepung lebih berat daripada gula.", "Gula dan tepung sama berat.", "Keduanya tidak dapat dibandingkan karena penyebutnya berbeda."],
  "kunci": 0,
  "pengecoh": {
    "1": "Mengira pecahan dengan penyebut lebih kecil selalu lebih besar, tanpa melihat pembilang.",
    "2": "Mengira kedua pecahan sama karena sama-sama kurang satu bagian dari satu utuh.",
    "3": "Mengira pecahan berpenyebut beda tidak dapat dibandingkan."
  },
  "pembahasan": "3/4 = 9/12 dan 2/3 = 8/12, jadi 3/4 kg lebih berat."
}
```

A unit adds `id`, `judul`, `teks` (LIT), `konteks_akm`, `stimulus`, `sumber` and its `soal[]`. Items inside a unit take their `unit` and `konteks_akm` from it.

A `stimulus` has:
- `teks`: paragraphs separated by a blank line
- optional `tabel` (`judul`, `kolom`, `baris`), placed where `teks` has the marker `[TABEL]`
- optional `gambar`, a picture path, which then requires `deskripsi_gambar`. HADIR shows that description as the figure description.

A single item with a picture carries its own `stimulus` and `sumber`.

## 14. Changes this needs in HADIR

These are listed for the HADIR phase document; none of them are made by this spec.

- **New item fields:** `cp`, `butir`, fase and element (derived from `cp`), `proses`, `proses_cp`, `teks`, `konteks_akm`, and `unit` (`QbPassage`). They replace `subtest`. `subtest` came in with migration `3ba5c7823f82` (nugross190/V2HADIR#83, merged 2026-11-01) and may already hold data. So the new fields come in a new migration, and `subtest` is dropped only after its values have been mapped where an equivalent exists: R4–R6 to the three LIT processes, M3–M6 to content elements, M7 to `penalaran`.
- **Reports:** the report in `services/ujian_diagnostik.py` is rebuilt on these tags (§12). `SUBTESTS` goes.
- **Item types:** `MENJODOHKAN` now; `URAIAN` with rubric marking later.
- **Later features:** per-section timers (screener, §9), routing (v2, §11), audio items (Menyimak).
- **Moving items into HADIR:** the items now sit in the same repository as HADIR (`content/diagnostik/`). An import script reads them straight into the question bank with the new fields and stores their pictures as `QbMedia`.

## 15. Open decisions

1. The *(proposal)* values: grid, cut points, text lengths, option count.
2. Which fase is the target for kelas XI in mathematics, given the conflict in §2.
3. Whether Menyimak joins once HADIR can play audio.
4. Whether science follows the same model, with its own CP file.
