# TKA template: Fisika

Describes the TKA 2025 Fisika paper (pilihan, 22 of 25 items; numbers 6, 13 and 14 missing from the source) as 7 item types. Codes, levels and examples are in `data/tka-types.json`.

## 1. The paper at a glance

- **One stimulus per item.** Almost every item is a short everyday situation, usually with a figure: a graph, circuit, instrument reading or diagram. Two stimuli are shared: "Uji Coba Mobil" (items 3–4) and "Percobaan Konduksi Kalor" (items 18–19).
- **Formats.** 19 `pilihan-ganda`, 2 `pilihan-ganda-kompleks`, 1 `benar-salah` (columns Tepat / Tidak Tepat).
- **Content.** Each item names an *elemen* (Kinematika, Dinamika, Fluida, Gelombang, Kalor dan Termodinamika, Kelistrikan) and a *subelemen*. The item type is independent of the topic: FIS-HITUNG appears in fluids, gases and electrostatics alike.

| Type | Level | Items |
|---|---|---|
| FIS-UKUR | 1 | 1 |
| FIS-GRAF | 2 | 4 |
| FIS-HITUNG | 2 | 5 |
| FIS-KONSEP | 2 | 4 |
| FIS-ANALISIS | 3 | 2 |
| FIS-STRATEGI | 3 | 4 |
| FIS-EKSP | 3 | 2 |

## 2. Rules for every Fisika item

- **Give every quantity the solution needs,** and nothing that contradicts it. State g (the paper uses 10 m/s²), trigonometric values for non-standard angles, and which way is positive. FIS25-002 gives no distance or departure time and cannot be solved.
- **The story must agree with the numbers.** FIS25-007 says a 7,5 m/s shot goes in, but the given numbers put it 0,6 m above the ring. Compute the scenario before writing the story around it.
- **Name the quantity exactly.** "Berukuran 0,5 cm" (FIS25-012) does not say diameter or radius, and the two readings give 15 N and 90 N.
- **Figure and text must match.** FIS25-023 labels charges +4 μC and +9 μC but draws them with minus signs.
- **Compute the key and every numerical distractor in Python** and record the steps in `alasan`. A distractor should come from a named mistake, written in `catatan_transkripsi` (for example "C: memakai cos 37° alih-alih sin 37°").
- **Notation:** Unicode with units as in the paper (m.s⁻¹, m.s⁻², km.jam⁻¹, μC, °C) and decimal commas.

## 3. Item types

### FIS-UKUR: Membaca alat ukur (level 1)

- **Asks:** read an instrument (micrometer, vernier caliper, meter) and use the reading.
- **Stimulus:** a precise figure of the scale; the description must give main-scale and thimble or vernier positions exactly.
- **Key:** follows from the reading with the instrument's precision (micrometer 0,01 mm, caliper 0,1 mm or 0,05 mm).
- **Distractors:** misreading the half-millimetre line; adding instead of subtracting thickness; a value just beyond the limit.
- **Example:** FIS25-001 (which beads fit inside a pipe measured with a micrometer; `pilihan-ganda-kompleks`).

### FIS-GRAF: Grafik atau tabel ke besaran (level 2)

- **Asks:** interpret a v–t graph, a data table or a wave diagram to get a quantity or describe the motion.
- **Stem patterns:** "Berdasarkan grafik, kondisi manakah yang menggambarkan gerak dari mobil A dan B?" · "Mobil A akan menyusul mobil B setelah menempuh jarak ...." · "... berapa frekuensi bunyi yang dihasilkan oleh pipa tersebut?"
- **Key:** use areas, slopes and intercepts correctly; state the graph values in the figure description.
- **Distractors:** slope read as area (or the reverse); the meeting time used as the meeting distance; closed pipe vs open pipe harmonic.
- **Examples:** FIS25-003, 004, 015, 021.

### FIS-HITUNG: Menghitung satu besaran (level 2)

- **Asks:** apply one law in context: vertical motion, Pascal, ideal gas, Coulomb, rotational dynamics.
- **Stem patterns:** "Berapakah perbedaan ketinggian kedua roket air setelah 3 detik diluncurkan?" · "... maka gaya terkecil yang digunakan pada piston kecil ... adalah..." · "... maka tekanan akhirnya adalah ...."
- **Key:** one clean result with consistent significant figures and units.
- **Distractors:** each from one mistake: ratio of radii instead of areas, forgetting to square, wrong axis for the moment of inertia (FIS25-011: 270 vs 1080), cos for sin.
- **Watch:** specify geometry fully (axis of rotation, diameter vs radius).
- **Examples:** FIS25-005, 011, 012, 020, 023.

### FIS-KONSEP: Menjelaskan fenomena (level 2)

- **Asks:** which concept explains an everyday phenomenon, or which phenomena share a law.
- **Stem patterns:** "Penjelasan yang paling tepat untuk fenomena ini adalah ..." · "Diantara beberapa fenomena berikut ini yang menunjukkan penerapan hukum yang sama ... adalah..."
- **Key:** names the concept and how it acts in this situation (impulse = force × short time; total internal reflection in a mirage).
- **Distractors:** the right law with the wrong direction (FIS25-008, option B); a real but irrelevant effect; a common misconception (heavier falls faster, heat as a substance).
- **Examples:** FIS25-008, 010, 016, 022.

### FIS-ANALISIS: Keterkaitan besaran atau prediksi (level 3)

- **Asks:** predict what happens when one quantity changes, combining two or more relations.
- **Stem patterns:** "Berdasarkan perubahan tersebut, kondisi apa yang akan terjadi ...?" · "Setelah 4 detik gaya arus bekerja, kondisi gerak perahu adalah..."
- **Key:** the outcome the numbers give, checked by computing both cases.
- **Distractors:** the intuitive but wrong outcome ("lebih lambat, jadi jatuh lebih cepat"); a correct direction with a wrong size.
- **Watch:** this is where FIS25-007 fails. Compute the scenario first; never assert an outcome the numbers contradict. State when forces stop acting (FIS25-009).
- **Examples:** FIS25-007, 009.

### FIS-STRATEGI: Mengevaluasi strategi atau keputusan (level 3)

- **Asks:** choose the best strategy or decision for a goal (arrive on time, keep a bill under a limit, make two currents equal), or judge listed strategies Tepat / Tidak Tepat.
- **Key:** meets the stated goal and constraint; compute each option's outcome.
- **Distractors:** meets the goal but breaks the constraint; meets neither; physically impossible.
- **Watch:** goals and constraints must be numbers, not judgments. FIS25-017's statement 2 ("membaca dengan jarak lebih dari 50 cm") is arguable because the goal is vague.
- **Examples:** FIS25-002, 017, 024, 025.

### FIS-EKSP: Rancangan percobaan (level 3)

- **Asks:** identify variables (bebas, terikat, kontrol), or a flaw in a procedure that makes the data inaccurate.
- **Stimulus:** a described experiment with apparatus and steps.
- **Key:** the variable roles exactly as the design sets them; the flaw that most directly affects the measured variable.
- **Distractors:** roles swapped; a control variable named as independent; a flaw that is real but minor (FIS25-019, option D).
- **Examples:** FIS25-018, 019.
