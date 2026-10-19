# TKA template: Bahasa Indonesia

Describes the TKA 2025 Bahasa Indonesia papers (wajib and pilihan, 63 items) as 11 item types. Codes, levels and the full example lists are in `data/tka-types.json`; level names are in `specs/tka-item-types.md`.

## 1. The paper at a glance

- **Stimulus first.** Every item hangs on a text. A text carries 3–4 items. Wajib: 9 texts, 5 fiction and 4 nonfiction (argumentasi, opini, berita, eksposisi). Pilihan: 9 texts, including a hikayat, a poem, articles with tables, and three pairs of texts ("Wacana 1" and "Wacana 2").
- **Formats.** Mostly `pilihan-ganda` with 5 options. The pilihan paper adds `pilihan-ganda-kompleks` ("Jawaban benar lebih dari satu") and `benar-salah` tables.
- **Alternative versions.** One number can come in two or three versions with different texts (BINW25-018A/B/C, BINP25-023A/B/C). Same item type, different stimulus.
- **Wajib vs pilihan.** Wajib leans on comprehension (KOS, IDE, HUB, UNS, PRED, SIMP). Pilihan leans on language and data (BHS, DATA, LOGIKA).

| Type | Level | Wajib | Pilihan |
|---|---|---|---|
| BIN-KOS | 1 | 5 | 0 |
| BIN-IDE | 1 | 5 | 0 |
| BIN-URUT | 1 | 1 | 1 |
| BIN-HUB | 2 | 5 | 0 |
| BIN-UNS | 2 | 5 | 5 |
| BIN-PRED | 2 | 3 | 0 |
| BIN-BHS | 2 | 1 | 10 |
| BIN-SIMP | 3 | 4 | 0 |
| BIN-NILAI | 3 | 3 | 5 |
| BIN-DATA | 3 | 1 | 7 |
| BIN-LOGIKA | 3 | 0 | 2 |

## 2. Rules for every Bahasa Indonesia item

- **The key must be provable from the text.** A student who reads carefully must be able to point to the sentence that makes the key right and each distractor wrong. Background knowledge may help but must not decide the answer.
- **Name the paragraph or sentence when the stem refers to one,** and check that the text really has it. BINW25-003 asks about "paragraf kedua dan ketiga" of a text printed with two paragraphs.
- **Every word the stem asks about must occur in the text.** BINW25-018B asks for the meaning of *diunduh*, which does not appear in its text.
- **Five distinct options of similar length.** BINW25-017 (C and D) and BINP25-021 (D and E) have near-identical or identical options, so no single key exists.
- **Indonesian textbook terms.** Use *gagasan pokok*, *gagasan pendukung*, *latar*, *majas*, *citraan*, *afiks*, as the Kurikulum Merdeka books do.

## 3. Item types

### BIN-KOS: Makna kata atau istilah dalam konteks (level 1)

- **Asks:** the meaning of a loanword, regional word or term as used in this text.
- **Stimulus:** any text; the word should be one whose meaning the context makes clear.
- **Stem patterns:** "Apa makna kata *X* pada teks tersebut?" · "Makna dari istilah *X* dan *Y* dalam teks tersebut adalah ...." · "Fenomena yang menggambarkan "*X*" berdasarkan teks di atas adalah ..."
- **Key:** the contextual meaning, paraphrased, not copied word for word from the text.
- **Distractors:** other meanings of the word; a meaning of a word that sounds similar; an activity mentioned nearby in the text; a definition that is too broad or too narrow.
- **Examples:** BINW25-001 (*hajatan*), 022 (*sesepuh*), 018A (*Halaeng Hebeung*, *Selo Sen*), 015 (*inflasi*).

### BIN-IDE: Gagasan pokok, gagasan pendukung, dan informasi tersurat (level 1)

- **Asks:** which statement supports a given main idea, or what the text says about a point.
- **Stem patterns:** "Manakah gagasan yang mendukung ide pokok bahwa ...?" · "<Gagasan pokok>. Manakah gagasan penjelas yang mendukung gagasan pokok tersebut?"
- **Key:** a paraphrase of a supporting sentence in the text.
- **Distractors:** a true statement that supports a different idea; a statement that restates the main idea itself (BINW25-019B, option A); the right content attributed to the wrong party (BINW25-023, option B); an exaggeration of the text ("harus", "selalu", "tidak bisa digantikan").
- **Examples:** BINW25-002, 006, 019A, 019B, 023.

### BIN-URUT: Urutan peristiwa atau kerangka teks (level 1)

- **Asks:** the correct order of three events or parts.
- **Stem pattern:** "Manakah urutan peristiwa berikut yang paling sesuai dengan isi teks?" Options are chains joined by →.
- **Key:** the order in the story, which may differ from the order the text first mentions things.
- **Distractors:** the same three events in another order; a chain that starts with background information (a campaign, a setting) instead of an event.
- **Examples:** BINW25-009, BINP25-005.

### BIN-HUB: Hubungan makna antarkalimat atau antarparagraf (level 2)

- **Asks:** how two named paragraphs or sentences relate.
- **Stem patterns:** "Bagaimana hubungan makna antara paragraf 1 dan paragraf 2 dalam teks tersebut?" · "Bagaimana keterkaitan antara paragraf ketiga dengan paragraf keempat ...?"
- **Key:** one relation (sebab-akibat, contoh, penegasan, pertentangan, rincian, saling melengkapi argumen), stated with the content of both paragraphs.
- **Distractors:** the reversed relation (cause given as effect); a relation the paragraphs could have but do not; a correct relation with the wrong content.
- **Watch:** the item's signal words. BINW25-012's second paragraph opens with "Salah satu faktor penyebab ..."; BINW25-024's third opens with "Meskipun ...". Make sure exactly one relation fits; BINW25-020B is weak because "akibat" and "memperjelas" both fit.
- **Examples:** BINW25-003, 012, 020A, 020B, 024.

### BIN-UNS: Unsur intrinsik fiksi (level 2)

- **Asks:** a character's trait, the setting, the conflict and its cause, the mood, or a character's emotional response.
- **Stimulus:** a short story, novel excerpt or hikayat, with enough detail to infer from.
- **Stem patterns:** "Berdasarkan teks tersebut, bagaimana sifat yang dimiliki oleh <tokoh>?" · "Latar tempat yang tergambar dalam cerita tersebut adalah ...." · "Apa yang menyebabkan konflik dalam kutipan cerpen tersebut?" · "Respons emosional tokoh <X> terhadap peristiwa ... adalah ...."
- **Key:** an inference supported by at least two details in the text.
- **Distractors:** a trait that fits one moment but not the whole text; an emotion that is the opposite of the text's; an event that happens in the story but is not the cause asked about.
- **Examples:** BINW25-005, 008, 016, 018C, 019C; BINP25-006, 025A, 025B, 026A, 026B.

### BIN-PRED: Prediksi kelanjutan atau penutup teks (level 2)

- **Asks:** what comes next, or which sentence ends the text.
- **Stem patterns:** "Apa yang akan dilakukan tokoh utama setelah mengalami peristiwa tersebut?" · "Manakah pernyataan yang dapat menjadi kelanjutan teks tersebut?"
- **Key:** the continuation that follows from the last paragraph and the character's change.
- **Distractors:** a continuation that contradicts the ending; a plausible but unprompted twist; a continuation that repeats something already said.
- **Watch:** this type has the most doubtful keys (BINW25-007, 017). Write the stem so the text decides: ask what *fits* the character's stated decision rather than what *may* happen.
- **Examples:** BINW25-007, 017, 020C.

### BIN-BHS: Kebahasaan (level 2)

- **Asks:** why a word, phrase, clause, affix, figure of speech or image is used, or which sentence is correctly built.
- **Stimulus:** a poem, article or opinion text; the stem quotes the exact line or phrase.
- **Stem patterns:** "Mengapa larik "..." sudah tepat menguatkan gambaran tentang ...?" · "Makna simbolik pada larik "..." ... adalah ..." · "Mengapa frasa "..." tepat sebagai pengisi fungsi subjek?" · "Mengapa konstruksi frasa verba "..." tidak sesuai dengan konteks kalimat tersebut?"
- **Key:** names the device correctly and states its effect in this text.
- **Distractors:** the right device with the wrong effect; a neighbouring device (personifikasi vs hiperbola, citraan penglihatan vs pendengaran); a grammatical claim that is false (wrong sentence function, wrong affix meaning).
- **Watch:** quote the line exactly as it stands in the text. BINP25-008's poem prints "saying" for *sayang*.
- **Examples:** BINW25-014; BINP25-008, 009, 010, 011, 012, 013, 014, 017, 018, 020.

### BIN-SIMP: Ketepatan simpulan atau penutup (level 3)

- **Asks:** why a quoted sentence or the last paragraph is a fitting conclusion.
- **Stem pattern:** ""<kalimat>." Kalimat tersebut dapat menjadi kesimpulan yang sesuai teks argumentasi tersebut karena ...."
- **Key:** what the sentence does for the whole text (sums up the views, restates the thesis, gives the solution), in the text's own terms.
- **Distractors:** a function the sentence does not have (rejects, abolishes, praises); a correct function attached to only one part of the text; an overreach ("di seluruh wilayah Jawa").
- **Watch:** two functions often both fit (BINW25-025: "merangkum masalah" vs "menyimpulkan solusi"). Make the distractors clearly partial or false.
- **Examples:** BINW25-004, 021A, 021B, 025.

### BIN-NILAI: Nilai dan relevansinya (level 3)

- **Asks:** the value in a text, a shared value across two texts, or whether a character's action fits today's norms.
- **Formats:** `pilihan-ganda`, or `benar-salah` with 3 statements.
- **Stem patterns:** "Apa pesan moral yang disiratkan melalui dialog antara ...?" · "Persamaan nilai sosial yang terkandung dalam kedua kutipan wacana tersebut adalah ...." · "Mengapa tindakan tersebut relevan dengan norma sosial masyarakat saat ini? Klik pada pilihan Benar atau Salah ..."
- **Key:** a value the text shows through action or dialogue, not only through a narrator's comment.
- **Distractors:** a true general value the text does not show; a value from only one of the two texts; blaming a group the text does not blame.
- **Examples:** BINW25-010, 011, 021C; BINP25-007, 023A, 023B, 024A, 024B.

### BIN-DATA: Teks dan data visual (level 3)

- **Asks:** a paraphrase of a table or chart, the conclusion it supports, or whether a claim in the text matches the data.
- **Stimulus:** a text with a table or chart, or a pair of texts where one has the data.
- **Key:** a statement that is exactly true of the data. Compute every comparison before writing the options.
- **Distractors:** a true number with the wrong label; a trend reversed; a claim true of one row presented as true of all; data that is in the text but supports a different claim (BINW25-013, statement 3).
- **Watch:** check the table adds up. BINP25-021's weights sum to 89.95% and its text says 66 cities where the table has 64.
- **Examples:** BINW25-013; BINP25-015, 016, 021, 023C, 024C, 025C, 026C.

### BIN-LOGIKA: Kelogisan argumen (level 3)

- **Asks:** which statements follow logically from the text's argument.
- **Formats:** `pilihan-ganda-kompleks` or `benar-salah`.
- **Key:** statements entailed by the text; reject those that overgeneralise or reverse cause and effect.
- **Examples:** BINP25-019, 022.

## 4. Known weak spots in the 2025 papers

Avoid repeating these in generated items:

- An indicator box that does not match the item (BINP25-023A to 026B).
- Paragraph numbers that do not match the text (BINW25-003).
- A word asked about that is not in the text (BINW25-018B).
- Duplicate options (BINW25-017, BINP25-021).
- A source wrongly credited (BINP25 P07: a "Metamorfosis" excerpt that looks like Kafka's "Die Aeroplane in Brescia").
