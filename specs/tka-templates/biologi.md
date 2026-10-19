# TKA template: Biologi

Describes the TKA 2025 Biologi paper (pilihan, 27 of 30 items; numbers 25, 26 and 27 missing from the source) as 8 item types. Codes, levels and examples are in `data/tka-types.json`.

## 1. The paper at a glance

- **One stimulus per item.** No stimulus is shared. Most items open with a short case: a patient with symptoms and test results (BIO25-007, 010, 013, 016), a student's experiment (005, 006, 017–021), or an ecological report (001, 022, 023). 6 items carry a figure (004, 006, 008, 017, 018, 029) and 4 a table (005, 010, 020, 021).
- **Formats.** 20 `pilihan-ganda`, 3 `pilihan-ganda-kompleks` (001, 015, 018: "Jawaban benar lebih dari satu"), 4 `benar-salah` with three statements each (009, 012, 017 with columns Benar / Salah; 010 with Sesuai / Tidak Sesuai).
- **Content.** Each item names an *elemen*: Proses-Proses Pada Makhluk Hidup (13 items: circulation, respiration, excretion, coordination, immunity, reproduction), Keanekaragaman Hayati (5), Keterampilan Proses (5), Sel (4). The item type is independent of the topic: BIO-MEKANISME covers bacteria, sleep apnea, heat stroke, Alzheimer, diabetes, adrenaline and anaemia.
- **Source facts.** The PDF stops at 24 and resumes at 28; page 24 notes "25,26,27 Soal masih OTW". Item numbers come from the number in brackets at the end of each indicator. The source has typos copied verbatim ("mahluk", "kolestrol", "penyataan", "Resiko", "Kreb"); several stems are printed twice from overlapping screenshots and were copied once.
- **Keys.** None official. 19 keys are `tinggi`, 4 `sedang` (012, 014, 017, 018), 4 `rendah` (001, 004, 015, 021).

| Type | Level | Items |
|---|---|---|
| BIO-INFO | 1 | 1 |
| BIO-IDENT | 1 | 6 |
| BIO-MEKANISME | 2 | 7 |
| BIO-DATA | 2 | 3 |
| BIO-DAMPAK | 3 | 4 |
| BIO-EKSP | 3 | 3 |
| BIO-EVAL | 3 | 2 |
| BIO-SOLUSI | 3 | 1 |

## 2. Rules for every Biologi item

- **Exactly one defensible key, or exactly the keyed set in a multi-answer item.** Three of the four low-confidence keys fail here: in BIO25-001 option A (cula trade) is defensible because the text names hunting; in 015 option E (IVF) is a recognised later treatment for PCOS; in 021 option D (no replication) is methodologically sound. Every option in `pilihan-ganda-kompleks` and every `benar-salah` statement must be clearly true or clearly false given the stimulus and standard textbook biology.
- **Every option must be scientifically clean.** BIO25-004 has no fully correct option: B says glycolysis adds oxygen, E describes substrate-level phosphorylation loosely. The key option must contain no wrong clause; a distractor should be wrong for one named reason.
- **Statements must not bring in facts the stimulus lacks.** BIO25-017 statement 2 says "pisang matang", but neither text nor figure mentions ripeness.
- **The case must contain the evidence the key uses.** Good items put it in the stimulus: the irregular EKG in 007, anti-GAD antibodies in 013, raised IgE in 030, haemoglobin 7 g/dL with its normal value in 016. Give normal ranges with every lab value (010 does).
- **Experiments must change one variable.** BIO25-018's sample B combines running and drinking a lot of water, so the keyed questions (water drunk, sweat) cannot be separated by this design. BIO25-019 claims to study temperature but varies sun exposure. Generated experiments state the independent, dependent and controlled variables in the text, even if the item does not ask for them.
- **Figure and text must agree.** BIO25-006 states blue-black for the starch-positive part, but the figure's colours are schematic. Describe in `gambar` exactly what the student sees and make the text match it.
- **Check every number in Python** when the key depends on data (means, differences, percentages), and record it in `alasan`.
- **Spelling:** standard Indonesian (*makhluk*, *kolesterol*, *risiko*, *Krebs*). Scientific names as in the paper (Rhinoceros sondaicus, Clostridium botulinum); chemical formulas in Unicode (CO₂, FADH₂, NAD⁺).

## 3. Item types

### BIO-INFO: Informasi tersurat dalam teks kasus (level 1)

- **Asks:** which statements restate causes or facts given in the stimulus.
- **Stimulus:** a short factual text (a conservation case) that lists several causes.
- **Stem pattern:** "Dengan mencermati informasi tersebut, pernyataan manakah yang berkaitan dengan penurunan populasi Badak Jawa dan faktor penyebabnya?"
- **Key:** paraphrases of what the text says (infrastructure → deforestation and land conversion; low genetic diversity → poor adaptation).
- **Distractors:** plausible causes the text does not mention (migration, invasive competitors).
- **Watch:** a distractor must not follow from something the text does say. In BIO25-001, "perburuan" makes option A (cula trade) defensible. If a real-world cause is close to a stated one, leave it out.
- **Example:** BIO25-001 (`pilihan-ganda-kompleks`).

### BIO-IDENT: Mengenali struktur, tahap, atau jenis (level 1)

- **Asks:** identify a labelled structure, a process stage, a hormone, an interaction or an immune response type, and state its function or feature.
- **Stimulus:** a labelled figure (respiration scheme, blood components, neuron) or a short case that points to one category.
- **Stem patterns:** "... manakah dari proses berikut yang terjadi pada tahap berlabel A?" · "... pernyataan berikut yang menunjukkan persamaan komponen berlabel B dan C adalah ...." · "Hormon yang produksinya kemungkinan terganggu karena kebiasaan tersebut adalah ...." · "Kondisi tersebut merupakan contoh gangguan sistem imun yang melibatkan respons kekebalan tubuh secara ...."
- **Key:** the correct identity plus a function or feature that is true of it (B and C in 008: both irregular in shape and made in bone marrow).
- **Distractors:** the feature of a neighbouring label (A's lack of a nucleus in 008); the function of a nearby part (myelin sheath for the nucleus in 029); a category with the right first word but the wrong reason (030 option D, "spesifik alami, karena ... infeksi").
- **Watch:** for a "persamaan" item, the key must hold for both parts; check each option against each part. Use full, standard terms in figure labels ("Nodus Ranvier", not "Ranvier" as in 029).
- **Examples:** BIO25-003, 004, 008, 028, 029, 030.

### BIO-MEKANISME: Menjelaskan gejala dengan mekanisme (level 2)

- **Asks:** the physiological or biological mechanism that links a cause to the symptoms in a case.
- **Stimulus:** a person with named symptoms and, usually, a test result; the diagnosis is often given.
- **Stem patterns:** "... mekanisme utama peran Clostridium botulinum dalam menyebabkan keracunan ikan awetan adalah ...." · "Apa penyebab utama kegagalan tubuh Pak Junaidi dalam mempertahankan suhu normalnya?" · "Bagaimana mekanisme autoimun pada diabetes melitus yang diderita Alika dapat menyebabkan peningkatan kadar gula dalam darah?" · "Manakah mekanisme kerja hormon adrenalin yang paling tepat sesuai dengan gejala yang dialami Vito?"
- **Key:** names the mechanism and connects it to the symptoms in the stimulus (neurotoxin blocks nerve signals → vision problems and weak muscles; T cells destroy beta cells → no insulin).
- **Distractors:** the right organ with the wrong cell or direction (alpha cells instead of beta in 013; bronchi narrowing instead of widening in 014); a cause reversed into a cure (007 option B); a misconception (haemoglobin fights infection, 016 option E).
- **Watch:** the key's wording must be correct throughout; 014's key says "tekanan darah bertambah cepat", which is odd but kept because every other option has a clearer error. In `benar-salah` versions (012), the false statement differs from the true ones only in the brain region it names (hipotalamus); the region in a false statement must be clearly wrong in textbook terms.
- **Examples:** BIO25-002, 007, 011, 012, 013, 014, 016.

### BIO-DATA: Menafsirkan data pemeriksaan atau percobaan (level 2)

- **Asks:** read a table of results or an experiment outcome and state the factor or cause it shows.
- **Stimulus:** a described experiment with a result table or figure (enzyme tubes, Sachs leaf test), or lab results with normal values.
- **Stem patterns:** "Berdasarkan hasil percobaan ini, faktor utama yang mempengaruhi kerja enzim protease adalah ...." · "Berdasarkan percobaan tersebut, faktor yang memengaruhi fotosintesis pada daun tersebut adalah ...." · "... manakah aktivitas atau kebiasaan yang sering dilakukan oleh pria tersebut ...? Klik pilihan Sesuai atau Tidak Sesuai ..."
- **Key:** the one thing that differs between the conditions (pH in 005: HCl vs NaOH; light in 006: covered vs uncovered), or the habits consistent with each abnormal value (010: high LDL ↔ saturated fat; high blood pressure and pulse ↔ stress and poor sleep).
- **Distractors:** factors held constant in the design (temperature, time, substrate in 005); a real factor of the process that the experiment did not vary (CO₂ in 006); a healthy habit wrongly linked to a bad value (010 statement 2).
- **Watch:** every factor not varied must be stated as constant in the text, so a student can rule it out.
- **Examples:** BIO25-005, 006, 010.

### BIO-DAMPAK: Memprediksi dampak gangguan (level 3)

- **Asks:** predict what follows when one step of a process is blocked or one condition of an ecosystem changes.
- **Stimulus:** a named disruption (less thrombokinase, an enzyme inhibitor, more CO₂, an invasive species), often with numbers.
- **Stem patterns:** "Jika produksi trombokinase dalam tubuh murid tersebut berkurang secara signifikan, apa dampak yang terjadi?" · "Dampak langsung dari gangguan ini terhadap metabolisme sel adalah ...." · "... dampak yang paling mungkin terjadi akibat peningkatan CO₂ terhadap tumbuhan di wilayah tersebut adalah ...."
- **Key:** follows the chain one or two steps (no pyruvate dehydrogenase → no acetyl-CoA → less ATP in 024; CO₂ up → more biomass in tolerant species in 022), consistent with the observations in the stimulus.
- **Distractors:** the substance before the block said to accumulate after it (024 option A, acetyl-CoA accumulating); the opposite direction (009 statement 3, faster clotting); a wrong role in the pathway (009 statement 1, vitamin K becoming fibrin); "no change".
- **Watch:** when the stimulus already gives the outcome (pine leaf density rose in 022; 35% savanna cover and 40% pollinator loss in 023), the item tests reading rather than prediction; keep the outcome out of the text if the item is to be level 3. Real data (Taman Nasional Wasur, 2022) must be checked and cited before reuse; generated items use fictional places or checked figures.
- **Examples:** BIO25-009, 022, 023, 024.

### BIO-EKSP: Merancang penyelidikan (level 3)

- **Asks:** which scientific questions an experiment can answer, or the first step in collecting its data.
- **Stimulus:** a described or illustrated practical (iodine test on foods, urine samples before and after exercise, weeds in sunny and shaded spots).
- **Stem patterns:** "Pertanyaan apa yang ingin dijawab oleh murid melalui percobaan? Tentukan Benar atau Salah ..." · "Pertanyaan ilmiah mana yang paling tepat untuk dijadikan dasar penyelidikan dalam praktikum tersebut?" · "Langkah pertama yang harus dilakukan murid dalam proses pengumpulan data adalah...."
- **Key:** a question about the variable actually varied and the variable actually observed; a data-collection step that fixes locations and measures the independent variable first (019).
- **Distractors:** a question about something not observed (blood sugar, heart rate in 018); a question the observation contradicts (018 option D: urine after exercise is paler, not darker); the wrong reagent for the substance (017 statement 3: iodine for protein); concluding before collecting data (019 option D); changing natural conditions (019 options C and E).
- **Watch:** one variable at a time (section 2). 018 changes exercise and water intake together; 019 names temperature but varies light.
- **Examples:** BIO25-017 (`benar-salah`), 018 (`pilihan-ganda-kompleks`), 019.

### BIO-EVAL: Kualitas data dan hipotesis (level 3)

- **Asks:** whether results support a stated hypothesis, and why or why not.
- **Stimulus:** a hypothesis in quotation marks, the method, and a table of results (with replicates in 020).
- **Stem patterns:** "... guru menyampaikan bahwa data yang diperoleh kurang dapat mendukung hipotesis. Mengapa demikian?" · "... pernyataan yang paling tepat untuk menghubungkan hasil analisis data dengan hipotesis awal adalah ...."
- **Key:** names the data feature that decides: inconsistent replicates in 020 (B: 2,1; 5,5; 2,6 and D: 7,5; 1,5; 7,7); the consistent ranking across all days in 021.
- **Distractors:** complaints about the design that the data do not show (too many replicates, too little variation in concentration, extreme controls); rejecting a hypothesis because all groups grew at all (021 option B).
- **Watch:** compute the means first. In 020 the means rise with concentration (25%: 2,0; 50%: 3,4; 75%: 3,5; 100%: 5,57 mm), so the key holds only because of the scatter within treatments; say so in `alasan`. If the design lacks replicates (021), "belum dapat disimpulkan" becomes a defensible answer; either give replicates or make that option the key.
- **Examples:** BIO25-020, 021.

### BIO-SOLUSI: Menilai solusi (level 3)

- **Asks:** which actions solve the problem in a case (here, how a woman with PCOS can become pregnant).
- **Stimulus:** a case with symptoms, an exam finding and a diagnosis.
- **Stem pattern:** "Berdasarkan gejala yang dialami Dini, solusi mana saja yang tepat agar Dini dapat mengalami kehamilan? Klik pada semua jawaban yang benar!"
- **Key:** the actions that address the cause and keep the goal possible (lifestyle change to balance hormones; FSH/LH injections under supervision to induce ovulation).
- **Distractors:** an action that works against the goal (raising prolactin, which blocks ovulation; removing the ovary).
- **Watch:** a valid but later-stage option (IVF, option E) makes the keyed set arguable. State the constraint that rules it out ("langkah pertama", "tanpa prosedur medis invasif") or include it in the key.
- **Example:** BIO25-015 (`pilihan-ganda-kompleks`).

## 4. Known weak spots in the 2025 paper

Avoid repeating these in generated items:

- No fully correct option (BIO25-004).
- A distractor that the stimulus itself supports (BIO25-001 option A, 015 option E, 021 option D).
- A statement adding a detail the stimulus does not give (BIO25-017, "pisang matang").
- Two variables changed at once, or the named variable not the one varied (BIO25-018, 019).
- An indicator that overstates the item: BIO25-001's indicator says "Menjelaskan faktor penyebab", but the item only asks to find the causes the text states. Classify by what the item asks.
