# TKA template: Bahasa Inggris

Describes the TKA 2025 Bahasa Inggris papers (wajib, 25 items; pilihan, 40 items, of which 10 are duplicates) as 12 item types. Codes, levels and the full example lists are in `data/tka-types.json`; level names are in `specs/tka-item-types.md`.

## 1. The paper at a glance

- **Reading only.** Every item hangs on an English text; there are no grammar, vocabulary-cloze or listening items. Stems and options are in English; indicator boxes are in Indonesian.
- **Wajib: 5 texts, simple language.** Two fables ("The Lion and the Mouse", "The False Lion King"), a procedure infographic ("Effective Study Techniques"), a descriptive text (Great Barrier Reef) and an analytical exposition with a table (teen money management). Each text carries 5 items.
- **Pilihan: 6 texts, complex language.** Exposition and discussion texts on current issues: digital dissonance, Buy Now Pay Later, electric vehicles, finfluencers, vertical farming, fast fashion. Each carries 5 items. Several have a statistic or a cited study in the text but no table.
- **Formats.** Wajib: 10 `pilihan-ganda`, 13 `pilihan-ganda-kompleks`, 2 `benar-salah`. Pilihan: 16, 13 and 11 (12, 10 and 8 without the duplicates). Every choice item has 5 options. `pilihan-ganda-kompleks` stems say "There is more than one correct answer. Click on every correct answer" and never say how many; the proposed keys have 2 or 3.
- **`benar-salah` here means two named columns, not true/false.** Each table has 3 statements and two column headings stored in `kolom`; `kunci` true means the first column. Of the 10 distinct tables (2 wajib, 8 pilihan), only two use True / False (BINGP25-007, 017). The others: Time Management / Self Management (BINGW25-007A), Short-term / Long-term financial goals (BINGW25-016), Digital Dissonance / Mindful Digital Behavior (BINGP25-004A), Increased Stress / Loss of Authenticity (005B), Cause / Effect (010), Argument / Explanation (020), Agree / Disagree (005A), Suitable / Unsuitable (015). The paper calls the wajib ones "Pilihan Ganda Kompleks - Kategori". The column pair decides the item type: two categories taken from the text make ING-KLAS; Cause / Effect makes ING-SEBAB; True / False, Suitable / Unsuitable and Agree / Disagree put a judgement on each statement, and the type follows what is judged.
- **Alternative versions.** Wajib numbers 6–10 come in version A (infographic, P02) and version B (Hera and Shero fable, P03). Pilihan numbers 1–5 come in version A and B on two texts (P01 digital dissonance, P02 BNPL), and the text alternates: 1A, 3A, 4A on P01 but 2A, 5A on P02.
- **Duplicates.** Pilihan items 26A–30B (pages 32–41) repeat 001A–005B with the same item code, text, stem and options; only the indicator boxes of 27–30 differ. They are still mapped, each to the same type as its original (026A = 001A, 026B = 001B, and so on), so the pilihan counts below include them in brackets.
- **No missing numbers.** No "OTW" gaps; numbers are taken from the indicator boxes because the papers print none beside the items.

| Type | Level | Wajib | Pilihan (incl. duplicates 26–30) |
|---|---|---|---|
| ING-INFO | 1 | 3 | 7 (9) |
| ING-MAKNA | 1 | 1 | 0 |
| ING-KERANGKA | 1 | 3 | 1 |
| ING-KLAS | 2 | 2 | 3 (5) |
| ING-IDE | 2 | 1 | 2 |
| ING-TUJUAN | 2 | 2 | 4 (5) |
| ING-SEBAB | 2 | 2 | 2 (3) |
| ING-DUKUNG | 2 | 3 | 2 |
| ING-PREDIKSI | 2 | 2 | 0 |
| ING-PESAN | 2 | 3 | 1 |
| ING-TAMBAH | 3 | 2 | 4 (5) |
| ING-EVAL | 3 | 1 | 4 (7) |

Wajib leans on narrative comprehension (KERANGKA, PESAN, PREDIKSI, DUKUNG on characters). Pilihan leans on argument (INFO on claims, TUJUAN, TAMBAH, EVAL).

## 2. Rules for every Bahasa Inggris item

- **Quote the text exactly.** If an option is offered as a sentence "from the story", it must be in the story. BINGW25-005 quotes "amused", "nibbled", "immensely" and "in the bushes", none of which are in the printed text.
- **Every reference in the stem must be in the stem or the text.** BINGP25-025 asks for the fact that "best supports this opinion" without saying which opinion. BINGP25-003A introduces "Mrs Laurent" with no context.
- **Numbers in options must match the text unless the mismatch is the point.** BINGP25-018 option D says "up to 95% less water"; the text says 90%, so it is unclear whether D is a key or a trap.
- **One defensible key set.** For `pilihan-ganda-kompleks`, every option is clearly in or clearly out. Do not ask for "more than one" answer when the text supports only one (BINGP25-004B: only B is clearly supported, C is vague). Avoid two options that say the same thing (BINGP25-003A, A and C; BINGP25-010, statements 1 and 3).
- **`benar-salah`: name the columns in the stem exactly as in the table** (BINGP25-004A's stem says "DIGITAL BEHAVIOUR", the column says "Mindful Digital Behavior"), make each column meaningful for every statement, and record in `kolom` which heading is first. "Choose the correct category!" over True / False columns (BINGP25-017) is confusing.
- **Do not ask for an opinion and then key it.** BINGP25-005A ("decide whether you agree or disagree with the writer's arguments") has a key that depends on the reader's judgement. Ask instead whether a statement is supported by the text.
- **Options must fit the stem grammatically.** BINGW25-006A's stem ends "by ...." and options D and E begin with "by" again; the odd options stand out.
- **Proofread.** The papers carry typos into stems and options: "felling" (BINGW25-003), "kindnes" (004), "What would happened" (009B), "system o" (BINGP25-017), "quite" for *quiet* in the infographic. Generated items use correct English at the paper's level: simple and compound sentences for wajib, complex sentences for pilihan.
- **Fit the text type to the indicator.** The wajib version B items (BINGW25-006B to 010B) carry indicator boxes for "procedure text" on a narrative. A generated item's `tipe` decides; its text should be the genre the type section names.

## 3. Item types

### ING-INFO: Informasi tersurat dalam teks (level 1)

- **Asks:** which statement the text states: an effect, a benefit, a disadvantage, a detail.
- **Stimulus:** any text; works best on exposition and descriptive texts with several listed points.
- **Stem patterns:** "According to the text, which of the following is a major disadvantage of vertical farming?" · "Which of the following descriptions are mentioned clearly in the text? There are more than one correct answer." · "What are the negative effects of online life on a person's mental health?" · "Based on the information given, we can keep our mind focused and fresh by ...."
- **Key:** a close paraphrase of one sentence (or, for multiple answers, of separate sentences), each traceable to a paragraph.
- **Distractors:** the opposite of the text (BINGP25-016 A, "uses more land"); a benefit given as an environmental impact (BINGP25-021 A); a number or detail the text does not give (BINGW25-011 E, "more than 10,000 coral islands"); a true effect of a different kind (BINGP25-001A: distance from family is an effect on relationships, not mental health); a claim close to the text but with the wrong agent or reason (BINGP25-022 B and C).
- **Watch:** when the distractor differs from the text only by agent or cause, as in BINGP25-022, the key becomes arguable. Make the difference plain.
- **Examples:** BINGW25-006A, 011, 017; BINGP25-001A, 001B, 006, 011, 016, 021, 022 (and duplicates 026A, 026B).

### ING-MAKNA: Makna kata atau frasa dalam konteks (level 1)

- **Asks:** what a quoted phrase means in this text.
- **Stem pattern:** "The author mentioned "It feels like a different world under the sea". What does the phrase "a different world under the sea" most likely mean?"
- **Key:** the meaning the surrounding sentences give (here: beautiful and unlike the land).
- **Distractors:** a literal reading (people living underwater); a meaning that contradicts the text (looks the same as the land); a partial meaning made of words from nearby sentences ("bright", "quiet").
- **Watch:** BINGW25-012 is the only example and its key ("calm") is supported only loosely. Choose a word or phrase whose meaning the context fixes.
- **Example:** BINGW25-012.

### ING-KERANGKA: Ringkasan, urutan peristiwa, atau kerangka teks (level 1)

- **Asks:** the option that summarises the story, gives its events in order, or maps the paragraphs onto a frame.
- **Stimulus:** a narrative (events), a procedure (steps), or a discussion text (paragraph functions).
- **Stem patterns:** "Which option best summarizes the story?" (options labelled Beginning / Problem / Solution / Lesson) · "Which statement provides the most accurate chronological summary of the story's main events?" · "Which of the following flowcharts best reflects the structure of the text?" (boxes joined by →).
- **Key:** every element is in the text and in the text's order.
- **Distractors:** the right events shuffled (BINGW25-006B A); events, characters or steps that are not in the text; a frame that fits a different text type (BINGP25-023 D, impacts on retailers, economy, environment, society).
- **Watch:** for a list text such as the infographic, no "order" exists unless the text numbers its steps. BINGW25-008A has no option that follows the infographic and a key chosen only because the other options contain items not in it. Ask for the order only when the text has one.
- **Examples:** BINGW25-001, 008A, 006B; BINGP25-023.

### ING-KLAS: Mengelompokkan pernyataan ke dalam dua kategori (level 2)

- **Asks:** sort three statements into two categories named by the text or by a text concept.
- **Format:** always `benar-salah` with category columns (see section 1).
- **Stem patterns:** "Based on the infographic, determine whether each study technique listed on the left is categorized as Time Management or Self Management." · "Which of the following statements reflect digital dissonance or mindful digital behavior? For each statement, select ..." · "Read each statement below. Decide whether it is an argument or an explanation."
- **Key:** each statement belongs to exactly one category, by the text's own definition or example. Mix the columns (not all three in one).
- **Distractors:** a statement that sits in both categories is a flaw, not a distractor. BINGP25-005B statement 1 (an idealised persona) fits Increased Stress as well as Loss of Authenticity; BINGP25-020 statement 3 can be read as an argument.
- **Watch:** if the categories are not in the text (Time Management / Self Management in BINGW25-007A), they must be obvious from everyday meaning.
- **Examples:** BINGW25-007A, 016; BINGP25-004A, 005B, 020 (and duplicates 029A, 030B).

### ING-IDE: Topik atau gagasan utama teks (level 2)

- **Asks:** the main idea or focus of the whole text, which the text implies rather than states in one sentence.
- **Formats:** `pilihan-ganda`, or `benar-salah` True / False with three candidate statements.
- **Stem patterns:** "Which of the following best represents the main idea implied by the text?" · "What is mainly discussed in the text? Decide whether each statement is True or False according to the text!" · "What is the main focus of the text above?"
- **Key:** covers all paragraphs (for a discussion text: benefits and challenges).
- **Distractors:** a detail of one paragraph (BINGP25-007 statement 1); a topic the text touches but does not develop (BINGP25-017, "the advanced technology system"); a claim the text contradicts (BINGW25-013 B, "not important to people").
- **Watch:** with True / False columns, a true detail must not be keyed False. BINGP25-007 statement 1 is true of the text but keyed False because it is not the main idea. Either use pilihan-ganda or ask "Is this the main idea?" explicitly.
- **Examples:** BINGW25-013; BINGP25-007, 017.

### ING-TUJUAN: Tujuan penulisan dan sasaran pembaca (level 2)

- **Asks:** why the writer wrote the text or chose its structure, what the writer wants readers to do, or who the text is for.
- **Stem patterns:** "Which of the following statements best reflect the author's purpose in writing the text?" · "What is the implied purpose of the text?" · "Why did the writer choose to present both the benefits and drawbacks of ...?" · "From the text, the writer wants to convince people to ...." · "Who is most likely to be the target audience of this text?"
- **Key:** matches the text type: a discussion text informs about both sides and encourages balanced thinking (BINGP25-009); a hortatory exposition pushes an action stated in its last paragraph (BINGP25-013, "Start learning from finfluencers today").
- **Distractors:** a one-sided purpose for a two-sided text (BINGP25-003B B, BINGP25-009 A and B); a purpose for a different genre ("To describe how vertical farming works"); a too-broad or invented purpose (criticise governments); an audience the text never addresses (parents, bankers).
- **Watch:** in multiple-answer items, a third reasonable purpose is often left out of the key (BINGW25-009A option E). Make every wrong option clearly wrong.
- **Examples:** BINGW25-009A, 018; BINGP25-003B, 009, 013, 019 (and duplicate 028B).

### ING-SEBAB: Hubungan sebab-akibat dan alasan tindakan (level 2)

- **Asks:** why something happened or a character acted, how one thing affects another, or which of two linked statements is the cause.
- **Formats:** `pilihan-ganda`, `pilihan-ganda-kompleks`, or `benar-salah` Cause / Effect.
- **Stem patterns:** "Why did the lion trust the mouse and decide to let him go instead of eating him?" · "The hyenas laugh so much when Shero tries to roar like Hera because ...." · "How does BNPL affect shopping behaviour of certain gender?" · "Decide whether each statement is CAUSE or EFFECT according to the text!"
- **Key:** the cause the text gives for that event, not for a nearby one.
- **Distractors:** the cause of a different event in the same story (BINGW25-008B E: Shero trips, which is a later scene); a cause the text does not state (too tired, heard someone coming); the reversed relation.
- **Watch:** the stem must not assume what the text does not say. BINGW25-003 asks why the lion "trusted" the mouse, while the text says only that he "was feeling kind". For Cause / Effect tables, the two statements of a pair must not be paraphrases of each other (BINGP25-010, 1 and 3).
- **Examples:** BINGW25-003, 008B; BINGP25-004B, 010 (and duplicate 029B).

### ING-DUKUNG: Bagian teks yang mendukung watak tokoh, gagasan, atau pendapat penulis (level 2)

- **Asks:** which sentences or reasons show a character's trait, support a stated idea about the text, or support the writer's main opinion.
- **Formats:** `pilihan-ganda-kompleks`, or `benar-salah` Suitable / Unsuitable.
- **Stem patterns:** "Which of the following sentences from the story help you understand the lion's character?" · "Shero is clumsy and funny, this is shown when he ...." · "Which parts of the text best support the idea that the Great Barrier Reef is both beautiful and important?" · "What reasons does the writer give to support their main opinion?" · "In the text, the crucial role of finfluencers is well explained. Which statement best supports the idea above?"
- **Key:** each keyed option is a detail from the text that bears on the trait or claim.
- **Distractors:** a true detail about a different character (BINGW25-005 D, about the mouse) or a neutral habit (A); a claim the text contradicts (BINGW25-015 C, "cold, deep water"); facts not in the text (BINGW25-015 D, E); the reverse of a reason (BINGP25-014 B, openness "will damage" trust); a detail overstated as the main point (BINGP25-015 statement 2, "mainly focus on warning").
- **Watch:** the trait in the stem must be shown by the options. BINGW25-010B asks for "clumsy", but the scene where Shero trips is not among the options.
- **Examples:** BINGW25-005, 010B, 015; BINGP25-014, 015.

### ING-PREDIKSI: Prediksi akhir cerita atau akibat pengandaian (level 2)

- **Asks:** what would happen next, or how the story would end if one fact were changed.
- **Stimulus:** a fable or short narrative.
- **Stem patterns:** "As you read the part where the lion let the mouse go, which of the following endings do you anticipate?" · "If in the beginning of the story, Shero is a strong lion with a loud roar, just like Hera. What would happened in the end of the story?" (sic)
- **Key:** follows from the characters' stated traits and promises (for a changed fact, from what the story says that trait leads to: Hera is "loved and respected" because he is strong).
- **Distractors:** an ending that breaks a stated promise or trait (the mouse forgets); a dramatic twist the story does not prepare (one lion leaves the savannah); an outcome that ignores the changed fact (the hyenas still laugh).
- **Watch:** BINGW25-004 leaves the real ending (the mouse frees the lion from the net) out of the options, so the key rests on two speculative options. Include the ending the text supports.
- **Examples:** BINGW25-004, 009B.

### ING-PESAN: Pesan moral, nilai, dan penerapan isi teks (level 2)

- **Asks:** the lesson of a story, the values the writer wants readers to take away, or which tips from the text a reader can apply in a stated situation.
- **Format:** `pilihan-ganda-kompleks`.
- **Stem patterns:** "Which of the following statements best conveys the message of the story?" · "What can we learn from the story of Hera and Shero?" · "What important values about fast fashion does the writer want readers to understand from the text?" · "If you are preparing for an important exam ..., which of the following techniques do you think can be implemented effectively in your personal study time?"
- **Key:** messages the ending or closing paragraph states or clearly implies ("even small creatures can do great things, and we all need help sometimes").
- **Distractors:** a literal rule drawn from one event ("We should never wake up a sleeping animal"); a general truth the story does not show; a solution the text rejects (BINGP25-024 D, donating clothes, against "not all donated clothes are reused"); a tip made absolute ("Only study when ...", "during all study sessions").
- **Watch:** a reasonable message left out of the key makes the item unanswerable (BINGW25-007B C, BINGP25-024 E). State values close to the text's own words.
- **Examples:** BINGW25-002, 007B, 010A; BINGP25-024.

### ING-TAMBAH: Fakta atau gagasan tambahan yang memperkuat teks (level 3)

- **Asks:** which new fact, idea or piece of evidence, not in the text, would strengthen a named claim or make the text more informative or persuasive.
- **Stem patterns:** "Which additional facts would strengthen the writer's opinion that the limited availability of charging stations makes long-distance travel difficult?" · "Which of the following ideas could be effectively added before the conclusion to strengthen the writer's argument?" · "Which information would make the text more informative about student spending habits?" · "Which detail would best encourage people to visit the Great Barrier Reef?"
- **Key:** new information that bears directly on the named claim and points the same way.
- **Distractors:** a fact that weakens the claim (BINGP25-008 D, 10-minute charging; BINGP25-018 E, skills few people have); a related but irrelevant fact (rural drivers prefer gasoline); a restated definition (BINGP25-002A C, E); information about a different group or topic (BINGW25-019 C, teenagers vs adults).
- **Watch:** the key must be new. BINGW25-014's key (diving or swimming) is already in the text. Name the claim to be strengthened in the stem; "the point made in the text" (BINGP25-012) is too vague.
- **Examples:** BINGW25-014, 019; BINGP25-002A, 008, 012, 018 (and duplicate 027A).

### ING-EVAL: Menilai fakta, opini, kredibilitas, dan kekuatan argumen (level 3)

- **Asks:** which statements the text's data supports, whether the text is one-sided, whether its information can be verified, which fact supports an opinion, or how strong its arguments are.
- **Stimulus:** an exposition or discussion text, ideally with a table, a cited study or explicit statistics.
- **Stem patterns:** "Which of the following statements are supported by clear data or facts in the text and table?" · "Which option indicates that the text represents only a single viewpoint?" · "The text presents certain facts about the issue. ... Which statement below most strongly supports her claim?" · "Which fact in the text best supports this opinion?" · "Please decide whether you agree or disagree with the writer's arguments below."
- **Key:** follows from what the text does or does not contain: the numbers in the table (BINGW25-020 A, 45%), the absence of the other side (BINGP25-002B A), the absence of sources (BINGP25-003A).
- **Distractors:** an opinion presented as a fact ("Saving 10% of allowance is a good practice"); a claim about the text that is false (BINGP25-002B D, "presents problems without solutions", although it gives mindfulness as the solution); an overgeneralisation ("Most students do not care about money at all").
- **Watch:** this type has the most low-confidence keys (4 of 8, counting duplicates). Quote the opinion being evaluated (BINGP25-025 does not). Replace Agree / Disagree with Supported / Not supported by the text (BINGP25-005A).
- **Examples:** BINGW25-020; BINGP25-002B, 003A, 005A, 025 (and duplicates 027B, 028A, 030A).

## 4. Known weak spots in the 2025 papers

Avoid repeating these in generated items:

- Indicator boxes that do not match the item: BINGW25-006B to 010B (procedure-text indicators on a fable), BINGW25-019 (subkompetensi and indicator disagree), BINGP25-002, 003B, 007 to 010, 012 and 014 (subkompetensi, indicator and item disagree), BINGP25-027 to 030 (indicators differ from the items they duplicate).
- The same item code on two different items (BINGW25-006A/006B, 008A/008B, 009A/009B, 010A/010B).
- Whole items repeated under new numbers (BINGP25-026A to 030B).
- Options quoted as "from the story" that are not in it (BINGW25-005).
- Keys that rest on judgement or on options the text does not settle: 16 of the 65 keys are `rendah`, most in ING-EVAL, ING-SEBAB, ING-PESAN and ING-TAMBAH.
