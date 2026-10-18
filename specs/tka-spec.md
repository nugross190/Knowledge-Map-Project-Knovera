# TKA bank spec

A TKA bank is one JSON file, `data/tka/<id>.json`, holding the items of one *Tes Kemampuan Akademik* (TKA) paper, transcribed from the published question file. All banks are rendered by `templates/tka.html` into `docs/tka.html`.

TKA banks are not quiz banks. `question-spec.md` covers short-answer questions asked aloud; TKA items are multiple choice with a stimulus, often with a figure or table, and keep the wording of the official paper. So they have their own format and their own page, and do not use topic codes from the subject maps.

## 1. Structure

```
bank
├── id, kode, mapel, ujian, sumber{berkas, halaman, bentuk}
├── catatan[]          notes about the whole file (shown under "Tentang berkas soal ini")
├── teks[]             shared passages: id, teks, optional judul, jenis, halaman, catatan[]
└── soal[]             items
```

## 2. Fields

### Bank

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | Same as the file name: `tka-<subject>-<variant>-<year>`, e.g. `tka-kimia-pilihan-2025`. |
| `kode` | MUST | Short uppercase code + two-digit year: `KIM25`. Prefix of every item id. |
| `mapel` | MUST | Subject name shown on the page. |
| `ujian` | MUST | Which paper: `Tes Kemampuan Akademik (TKA) SMA/MA/SMK 2025, mata pelajaran pilihan`. |
| `sumber` | MUST | `berkas` (file name of the source PDF), `halaman` (page count), `bentuk`. The PDF itself is not committed. |
| `catatan` | SHOULD | Transcription conventions and file-level problems (missing "OTW" items, duplicates, page order). |
| `teks` | MAY | Passages used by more than one item. An item that uses one sets `passage` to its `id`. |

### Item

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | `<kode>-NNN`, NNN = item number; suffix `A`/`B`/`C` for alternative versions of one number. Permanent: saved progress is keyed by it. |
| `nomor` | MUST | Item number as a string. Taken from the "(n)" at the end of the indicator when the paper does not print numbers. |
| `format` | MUST | `pilihan-ganda` (one answer), `pilihan-ganda-kompleks` (several answers, "MCMA"), `benar-salah` (two-column table per statement, "Kategori"). |
| `passage` | MAY | Id of a `teks` entry, or `null`. |
| `kode_sumber`, `bentuk_sumber` | SHOULD | Item code and format label as printed. |
| `elemen`, `subelemen`, `kompetensi`, `subkompetensi`, `indikator` | MUST (`kompetensi`, `indikator`) | Copied verbatim from the indicator box, including its typos. `subkompetensi` is `null` when absent. |
| `soal` | MUST | Stimulus and question, verbatim. `[Gambar]` and `[Tabel]` mark where a figure or table stood. |
| `gambar` | MUST if `[Gambar]` appears | A text description of the figure, map, chart or photo, precise enough to answer from. Values read off a figure are marked as approximate. |
| `tabel` | MUST if `[Tabel]` appears | List of rows, each a list of strings; first row is the header. |
| `opsi` | MUST | Options (or statements for `benar-salah`) as strings, in printed order, without letters. |
| `kolom` | MUST for `benar-salah` | The two column headings, e.g. `["Benar", "Salah"]`, `["Fakta", "Opini"]`. |
| `kunci` | MUST | `pilihan-ganda`: index of the option (0 = A). `pilihan-ganda-kompleks`: sorted list of indexes. `benar-salah`: one boolean per statement, `true` = first column. `null` only when no key can be proposed. |
| `status_kunci` | MUST | `usulan` until checked against an official key, then `resmi`. |
| `keyakinan_kunci` | MUST | `tinggi`, `sedang`, `rendah`, or `tidak ada` (required when `kunci` is `null`). |
| `alasan` | MUST | Why the key is right, in Indonesian; for calculations, the worked steps. |
| `halaman` | MUST | PDF pages the item spans, as integers. |
| `catatan_transkripsi` | SHOULD | Problems: typos, cut-off text, contradictions with computed evidence, other defensible keys. |

## 3. Rules

- **Verbatim.** Text, options and indicator boxes are copied as printed, typos included; problems go into `catatan_transkripsi`, never silent fixes.
- **Keys are proposals.** No official key is published. Every calculation behind a key MUST be re-checked (for example in Python). When two options are defensible, pick one, lower `keyakinan_kunci`, and name the other in `catatan_transkripsi`.
- **Source errors are flagged, not fixed.** If printed numbers contradict each other, the note gives the computed values.
- **No invented content.** Missing items ("SOAL NO.2 OTW") are left out and listed in `catatan`; nothing is reconstructed.

## 4. Enforced by `build.py`

File name equals `id`; `kode` format; required bank and item fields; item id pattern and uniqueness; known `passage`; `format` and `keyakinan_kunci` values; at least two options; `kunci` shape for each format (and `null` only with `tidak ada`); `kolom` for `benar-salah`; `gambar`/`tabel` present when their markers are; `tabel` shape; `halaman` as a list of integers. It also prints, per bank, how many items have a low-confidence or missing key.
