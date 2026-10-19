# TKA item types

An **item type** names what a TKA item asks the student to do. Every item type belongs to one subject template (`specs/tka-templates/<subject>.md`) and has a permanent code such as `BIN-HUB` or `FIS-GRAF`.

Item types are used for three things:

1. **Describing the papers.** Each transcribed item in `data/tka/` is assigned to exactly one item type in `data/tka-types.json`, so the share of each type in a paper can be counted.
2. **Generating new items.** A generator agent writes items for a chosen item type, following its template (`specs/tka-generation.md`).
3. **Testing agents.** Items of a type are the reference set for that type's answering and generation tests.

## 1. Why item types, not the printed indicators

The printed indicator boxes cannot be used as item types directly:

- Their wording differs from paper to paper. The Bahasa Indonesia papers use three short kompetensi names; the science papers use long sentences, often with an *elemen* and *subelemen* instead of a subkompetensi.
- Some boxes do not match their item. For example, BINP25-023A and 023B ask about social values in two novel excerpts, but carry the indicator box of version C, which is about a table. BINW25-020A asks how two paragraphs relate, under an indicator about predicting what comes next.

So an item's type follows **what the item actually asks**. The printed indicator stays in the item, verbatim.

## 2. Levels

Every item type has one of three levels, the same in every subject:

| Level | Name | The student must |
|---|---|---|
| 1 | Menemukan | find or read something stated in the stimulus: a word's meaning, a fact, an order, a value read off an instrument |
| 2 | Menerapkan | connect two pieces: relate paragraphs, interpret a graph, apply one concept or formula, explain a phenomenon |
| 3 | Menalar | judge or decide: evaluate a conclusion, an argument, a strategy, a procedure, or predict a result from several relations |

The level is a property of the type, not of a single item. Within a type, difficulty still varies with the stimulus and the distractors.

## 3. `data/tka-types.json`

```
{
  "<subject>": {
    "mapel": "Bahasa Indonesia",
    "banks": ["tka-bahasa-indonesia-wajib-2025", ...],   ids of the banks this template describes
    "types": [
      {
        "kode": "BIN-HUB",                                permanent; never renamed or reused
        "nama": "Hubungan makna antarkalimat atau antarparagraf",
        "level": 2,
        "format": ["pilihan-ganda"],                      formats this type may use
        "contoh": ["BINW25-003", ...]                     every transcribed item of this type
      }
    ]
  }
}
```

Rules, checked by the tests:

- Every item in each listed bank appears in exactly one type's `contoh`.
- Every id in `contoh` exists in one of the listed banks.
- Each example's `format` is one of its type's formats.
- Codes are unique across all subjects.

## 4. Adding a subject

1. Read every item of the subject's banks.
2. Group them by what the student has to do (section 1), aiming for 5–12 types. A type with one example is allowed when the action is clearly distinct.
3. Add the subject to `data/tka-types.json` and run the tests until coverage is complete.
4. Write `specs/tka-templates/<subject>.md` using the Bahasa Indonesia and Fisika templates as the pattern.
