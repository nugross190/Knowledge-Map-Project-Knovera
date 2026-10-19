# Generating and testing TKA items with agents

This spec is for agents that write new TKA-style items, and for the people who test those agents. It builds on `specs/tka-spec.md` (item format), `specs/tka-item-types.md` (item types) and the subject templates in `specs/tka-templates/`.

## 1. Where generated items go

- One file per batch: `data/tka-generated/<subject>-<batch>.json`, e.g. `data/tka-generated/fisika-001.json`.
- Same structure as a TKA bank (`specs/tka-spec.md`), with `id` equal to the file name and `sumber` describing the batch, e.g. `{"berkas": null, "halaman": 0, "bentuk": "dibuat agen"}`. Each item has these differences:

| Field | Rule |
|---|---|
| `id` | `<kode>-G<NNN>`, e.g. `FISG-G001`. The bank's `kode` ends in `G` (`BING`, `FISG`) so generated ids can never collide with transcribed ones. |
| `asal` | `"generated"`. |
| `tipe` | An item-type code from `data/tka-types.json`, e.g. `"FIS-HITUNG"`. |
| `acuan` | Ids of 1–3 transcribed items the agent used as models; each must be an example of the same type. |
| `status_kunci` | Always `"usulan"`. A generated key is never official. |
| `halaman` | `[]`, since there is no source page. |
| `kode_sumber`, `bentuk_sumber`, `elemen`, `subelemen` | Leave out. |

- Generated items are **not** built into the site. `python scripts/check_generated.py` validates them; `build.py` ignores the folder.

## 2. Generator agent: the task

Input: a subject, an item type, a count, and optionally a topic (for Fisika, an elemen and subelemen).

1. Read the subject template and the type's section. Read every example item listed for the type in `data/tka-types.json`.
2. For each item:
   - **Write the stimulus first.** Bahasa Indonesia: an original text of 150–350 words in the genre the type needs; never copy or lightly edit a paper's text. Fisika: a short everyday situation with all needed quantities and, if useful, a figure described in `gambar`.
   - **Write the stem** in the type's stem patterns.
   - **Fix the key**, then write each distractor from a named mistake or misreading. Record each in `catatan_transkripsi`, e.g. "C: arah gaya terbalik".
   - **Fisika:** compute the key and every numerical distractor in Python, and put the steps in `alasan`.
   - **Bahasa Indonesia:** quote in `alasan` the sentence that makes the key right.
3. Set `keyakinan_kunci` honestly. If another option is defensible, rewrite it until it is not; only then leave `tinggi`.
4. Run `python scripts/check_generated.py` until it prints OK.

The generator must not invent facts presented as real: no real people, institutions, statistics or dates unless they are checked and cited in the text's source line. Fictional names and invented data in clearly fictional settings are fine.

## 3. Reviewer agent: blind review

A second agent, which never sees `kunci` or `alasan`, answers each generated item, then compares with the key.

| Check | Pass when |
|---|---|
| Answerable | The reviewer reaches one answer from the stimulus alone |
| Agreement | The reviewer's answer equals `kunci` |
| One key | No distractor is defensible after reading the key's `alasan` |
| Type fit | The item asks what its `tipe` says (`specs/tka-templates/`) |
| Template rules | None of the subject template's section 2 rules is broken |
| Facts | For Fisika: physics and arithmetic are right; for Bahasa Indonesia: the text is original and its claims are fictional or checked |

The reviewer writes one line per item to `data/tka-generated/<file>.review.md`: the item id, pass or fail, and the reason for any failure. An item passes only if every check passes.

## 4. Answering test: measuring an agent on real items

Give the agent the transcribed items of one type with `kunci`, `alasan` and `catatan_transkripsi` removed. Score:

- **Agreement** with the proposed keys, per type.
- **Disagreements on high-confidence keys** (`keyakinan_kunci` = `tinggi`). These are either agent errors or key errors; each needs a human look.
- **Disagreements on low-confidence keys.** These are useful signals of which keys a teacher should review first.

The proposed keys are not official, so the agreement score is a consistency measure, not a grade.

## 5. A first exercise

1. Generate 5 `FIS-HITUNG` items (any elemen) and 5 `BIN-HUB` items (one new argumentative text, five items on it, like BINW25-012 and 024).
2. Run the checker.
3. Run a blind review with a different agent.
4. Run the answering test on the 5 `BIN-HUB` and 5 `FIS-HITUNG` transcribed items.
5. Compare: where did the generator break a template rule, and did the reviewer catch it?
