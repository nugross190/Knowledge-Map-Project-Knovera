# Question spec

Questions practise the facts in a map. There are two kinds of short-answer bank:

- **History competition kit:** `data/questions.csv`, with topic codes defined in `data/topics.json`. It feeds `docs/bank.html` and `docs/simulasi.html`.
- **Subject banks:** one CSV per subject map, `data/questions/<map id>.csv`, with topic codes taken from `data/maps/<map id>.json`. Each feeds `docs/bank-<map id>.html`, rendered through the same `templates/bank.html`; the map page and the home-page card link to it.

Transcribed TKA exam papers are a different kind of bank (multiple choice, verbatim official wording) and follow [`tka-spec.md`](tka-spec.md) instead.

## 1. Fields

One row per question in a UTF-8 CSV with exactly this header:

```
id,simpul,tingkat,soal,jawaban,catatan
```

Subject banks add one optional column, `konteks` (§6):

```
id,simpul,tingkat,soal,jawaban,catatan,konteks
```

| Column | Rule |
|---|---|
| `id` | `<topic code>-<three digits>`: `SNI-04-027`. Unique, permanent, never reused. New questions take the next free number for their topic. |
| `simpul` | The topic code the question tests. MUST exist in the subject's topics (`data/topics.json` for the kit, the subject's map otherwise). One question tests one topic. |
| `tingkat` | Difficulty: `1` mudah, `2` sedang, `3` sulit (see §3). |
| `soal` | The question, in Indonesian. |
| `jawaban` | The expected answer. |
| `catatan` | Optional. A one-line note shown after the answer: a related fact, the common wrong answer, or why. |

## 2. Writing rules

- **Short answer.** Questions are asked aloud in a quiz-competition format or answered alone in the bank page. The answer MUST fit in one line and be checkable without discussion: a name, number, date, term, or short list.
- **Self-contained.** Readable without seeing the map. No "seperti di atas", no references to figures.
- **One correct answer.** If several answers are acceptable, the question MUST say how many to give (*Sebutkan dua…*) and `jawaban` MUST list the accepted options (*Dua di antara: …*).
- **Phrasing.** End fill-in questions with `…` (*Pendiri Kerajaan Demak adalah…*). Direct questions end with `?`.
- **No trick wording.** Difficulty comes from the knowledge needed, not from ambiguous phrasing or double negatives.
- **Grounded.** Every answer MUST be supported by the subject's map or by a source cited in the pull request. Questions on facts the map marks as uncertain (`cek`) SHOULD be avoided.
- **Dated facts.** Questions about counts or "latest" items MUST name the year in the question (*…pada tahun 2025?*).
- **Calculations** (science and math): give all values with units, use round numbers, and put the final value with its unit in `jawaban` (*50%*, *4 m/s*). Put the key step in `catatan`.
- **No duplicates.** The build rejects identical questions (ignoring case). Near-duplicates testing the same fact the same way SHOULD be avoided; asking the same fact from the opposite direction is fine (*Who founded X?* / *What did Y found?*).

## 3. Difficulty

| Level | Meaning | Example |
|---|---|---|
| 1 mudah | A headline fact of the topic, in the map's summary or bold text | *Pendiri Kerajaan Demak adalah…* |
| 2 sedang | A specific detail from the topic's bullets or tables | *Prasasti Sriwijaya tahun 684 tentang taman Sriksetra adalah…* |
| 3 sulit | A precise date, number, minor figure, or a link between two topics | *Monumenten Ordonnantie dimuat dalam Staatsblad tahun 1931 nomor…* |

A bank SHOULD be roughly 45–55% level 1, 30–40% level 2, and 10–20% level 3. Subject banks with `konteks` items (§6) MAY run about 35–40% level 1 and 50–55% level 2: applying a concept to a scene is a level 2 task even when the concept is a headline fact. A subject bank MUST NOT fall below 35% level 1 (`build.py` warns and a test fails). Grade by the table above: a non-konteks question whose answer is the topic's summary fact or bold text is level 1.

## 4. Coverage

- Every topic MUST have at least 5 questions (`build.py` flags topics below this).
- Tier 1 topics SHOULD have at least 12. The first subject banks (2026-10-28) have about 8 per tier 1 topic; they are to be grown, not padded.
- When a competition gives weights per domain, the share of questions SHOULD roughly follow them; the practice mode applies the exact weights when drawing.

## 5. Enforced by `build.py`

Header exactness, empty or duplicate ids, ids not prefixed by their topic, unknown topics, difficulty outside 1–3, empty question or answer, and identical questions, for the kit and for every subject bank. A subject bank without a matching map is an error. `build.py` prints, per subject bank, the question count, the number of `konteks` items, the difficulty mix, and the topics below 5 questions. Everything else is checked through `quality-checklist.md`.

## 6. Konteks items (draft)

Status: draft, 2026-10-28. It applies Freire's ideas in a small, reversible way while the among generator spec is being reworked; expect it to change.

A `konteks` item opens with a scene from everyday life around the students, then asks for the subject concept that names or explains it. The idea comes from Freire's codification: the learner meets the concept inside a situation they recognise, and the concept becomes a tool for reading that situation. The item is still a short-answer question with one checkable answer.

| Rule | Check |
|---|---|
| **K1 Scene first.** The stem describes something observable (a market, a fishing trip, a flood, a bus route, a village meeting, a school election), then asks. | The scene comes before the question and contains no definition of the answer. |
| **K2 Answer is subject knowledge.** The key is a concept, term, formula result, or named fact from the map. | The answer would be accepted in a non-context version of the question. |
| **K3 Structures, not persons.** Describe things students can observe: prices, distances, rules, institutions, tools, who decides. | No item asks about or describes the student's own family income, debt or hardship, or calls anyone poor. |
| **K4 No fixed social verdict.** The question never asks whether something is fair, good or bad, and the key is never a moral or political judgement. | No key reads as an opinion about the scene. |
| **K5 Local and plausible.** Scenes are Indonesian and ordinary: pasar, warung, angkot, ojek daring, sawah, perahu nelayan, banjir, posyandu, rapat RT, pemilihan ketua OSIS. Figures are round, invented, and plausible, not presented as real data. | Numbers in a scene are not attributed to a real source unless they are one. |

The `konteks` column names the scene's theme in one or two words (`pasar`, `nelayan`, `banjir`); it is empty for ordinary items. The bank page shows the theme as a tag and offers a filter "Hanya soal konteks sehari-hari". Themes here are starting points chosen by the authors: a class that runs a dialogue phase (among generator spec, F1) should replace them with its own.

A subject bank MUST have at least 20% `konteks` items and SHOULD stay within about 20–30% (`build.py` warns below 20% and a test fails). Because konteks items are level 2, adding them lowers the level 1 share; top up level 1 at the same time so both floors hold. Ordinary recall items remain: K items practise applying a concept, not memorising it.
