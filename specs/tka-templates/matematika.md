# TKA template: Matematika

Describes the TKA 2025 Matematika papers (Umum, the compulsory paper, and Tingkat Lanjut, the elective paper; 50 items, 25 each) as 8 item types. Codes, levels and the full example lists are in `data/tka-types.json`; level names are in `specs/tka-item-types.md`.

## 1. The papers at a glance

- **One item, one stimulus.** No stimulus is shared between items. About half the items are bare mathematics (an expression, a matrix, a limit, a figure on a grid); the rest wrap one computation in an everyday story (a course fee, a hotel, a drum of fuel, a stained-glass door), usually with a figure or table. Umum has 16 items with a figure and 2 with a table; Tingkat Lanjut has 10 with a figure and 3 with a table.
- **Formats.** Umum: 17 `pilihan-ganda`, 4 `pilihan-ganda-kompleks`, 4 `benar-salah` (all Benar / Salah). Tingkat Lanjut: 14 `pilihan-ganda`, 8 `pilihan-ganda-kompleks`, 3 `benar-salah` with three different column pairs: Mungkin / Tidak Mungkin (MATL25-007), Benar / Salah (009), Pas / Tidak Pas (018).
- **Content.** Each item names an *elemen* and *subelemen*. Umum: Bilangan 3, Aljabar 6, Geometri dan Pengukuran 11, Data dan Peluang 5. Tingkat Lanjut: Aljabar 11 (matriks, polinomial, fungsi eksponen and trigonometri), Geometri dan Pengukuran 10 (vektor, lingkaran, transformasi), Kalkulus 4 (limit). The item type is independent of the topic: MAT-PARAM covers a binary operation, a polynomial remainder, a vector and two transformations.
- **Source facts.** Both PDFs have all 25 numbers; no "OTW" gaps, no duplicates, no alternative versions. Tingkat Lanjut's pages are out of order (pages 2–8 hold numbers 3, 4, 2, 5, 8, 6, 7). Item numbers come from the "(n)" at the end of each indicator. MATW25-015 shows only 4 options (the fifth is cut off in the screenshot); MATL25-012 has only 4 options in the source. In MATW25-008 and MATL25-003 the options are laid out in two uneven columns, so the transcribed letter of the key may differ from the official one.
- **No official key.** All keys are proposed. 34 are `tinggi`, 12 `sedang`, 4 `rendah` (MATW25-011, 015; MATL25-017, 024).

| Type | Level | Umum | Tingkat Lanjut |
|---|---|---|---|
| MAT-KENAL | 1 | 3 | 1 |
| MAT-HITUNG | 2 | 2 | 6 |
| MAT-PARAM | 2 | 2 | 5 |
| MAT-MODEL | 2 | 6 | 3 |
| MAT-FUNGSI | 2 | 1 | 6 |
| MAT-UKUR | 2 | 5 | 2 |
| MAT-KEPUTUSAN | 3 | 2 | 1 |
| MAT-NALAR | 3 | 4 | 1 |

Umum leans on contextual geometry and modelling (MODEL, UKUR, NALAR); Tingkat Lanjut leans on symbolic procedure (HITUNG, PARAM) and given function models (FUNGSI).

## 2. Rules for every Matematika item

- **The story must ask for what the numbers give.** MATW25-006 gives sheets of paper per row (400, 550, ...) but asks how many *people* hold them; the key assumes one sheet per person. MATW25-015 gives a 20 m roll and asks what is left without saying whether the first rope is cut from the same roll (10 m vs 15 m).
- **Every given number must agree with every other.** MATL25-004 prints ingredient totals 4.360 g jahe and 4.960 g gula merah, but its own matrix and order give 4.160 and 5.140; only the water row is consistent, so only it can be used. Compute every printed total from the model before writing the item.
- **State every constant and convention the solution needs.** π (MATW25-016 and 019 need 3,14 or 22/7 but do not say so; MATL25-018 does, and gives √2 ≈ 1,4), whether day 1 is before or after the first decrease (MATW25-007: day 4–5 or day 3–4), whether a centre lies exactly on a base (MATW25-016).
- **One reading of the words.** "C di antara A dan D" (MATW25-022) gives 12 if adjacent and 40 if not; only 12 is an option. "Bisa ditanam" (MATW25-013) can mean the maximum number of pots or any number that fits. "Tidak diletakkan pada dinding yang sejajar dengan rak buku" (MATW25-011) leaves open whether the rack's own wall counts. Write "tepat bersebelahan", "paling banyak", "selain dinding tempat rak".
- **Figures must carry every length the solution uses, and be labelled.** MATL25-017 gives only "14 cm" and two "10 cm" labels for a plus sign whose arm width decides the red area; MATL25-016 never labels which line is f; MATW25-009's bouquet contents must be counted from small pictures. Name every point, line and length in the `gambar` description.
- **Every listed correct answer must appear, and the options must be complete.** MATL25-005 asks for the x-intercepts of a cubic with roots −4, −2, 3 but offers only (−2, 0) and (3, 0). MATL25-024 says "jawaban benar lebih dari satu" but, as printed (θ → π/6), only option E is true.
- **Match the indicator to the item, or leave it verbatim and note it.** MATL25-007 (indicator: dimensions of a solid; item: share capital) and MATL25-012 (indicator: diagonals of a cuboid; item: length of a vector) do not match.
- **Compute the key and every numerical distractor in Python** and record the steps in `alasan`. A distractor should come from a named mistake, written in `catatan_transkripsi` (for example "A: semua kardus diputar 90°, 336").
- **Notation:** as in `data/tka/` banks: Unicode superscripts, fractional powers as 3^(2/3), matrices as [a b; c d], column vectors as [x; y], limits as lim(x→a), systems in braces separated by semicolons, decimal commas, Rp12.000,00.

## 3. Item types

### MAT-KENAL: Mengenali hubungan atau data pada gambar (level 1)

- **Asks:** pick out what a figure, graph or diagram shows: angle pairs formed by parallel lines, parallel or perpendicular faces of a cube, trends in a line graph, the centre of a drawn circle.
- **Stimulus:** a labelled figure; for a graph, every plotted value must be readable (state them in `gambar`).
- **Stem patterns:** "Berdasarkan gambar tersebut, pasangan sudut manakah yang membentuk sudut 180°?" · "Berdasarkan grafik tersebut, berikut ini pernyataan mana saja yang tepat mendeskripsikan ...?" · "... persamaan lingkaran yang sepusat dengan lingkaran pada gambar di atas"
- **Key:** follows from one reading or one named relation (sehadap, berpelurus, sejajar); usually `pilihan-ganda-kompleks`.
- **Distractors:** a pair that is equal instead of supplementary; a trend true for most years but not all ("selalu bertambah" with one dip, MATW25-021 option B); a centre with a sign flipped or coordinates swapped (MATL25-015: (3, 4), (−3, −4), (4, 3), (−4, 3)).
- **Watch:** words such as "selalu", "konsisten", "tetap" must be checked year by year. In MATL25-015 the key (A) has radius 3, while the wrong-centre options B and E have the drawn radius 2; that is correct for "sepusat" but punishes a student who also matches the radius, so say so in `alasan`. MATW25-011 is ambiguous (section 2).
- **Examples:** MATW25-010, 011, 021; MATL25-015.

### MAT-HITUNG: Menghitung bentuk matematis tanpa konteks (level 2)

- **Asks:** carry out one procedure on a given expression: set operations, simplifying powers, a matrix inverse, roots of a cubic, a limit by substitution or by a standard trigonometric limit, the image of a line under a rotation, tangent points on a circle.
- **Stem patterns:** "Bentuk sederhana dari ... adalah ...." · "Invers dari matrik F adalah ...." · "Di manakah koordinat titik perpotongan grafik fungsi f(x) = ... terhadap sumbu X?" · "Nilai dari lim(x→3) ... = ...." · "Manakah koordinat titik yang terletak pada garis l?"
- **Key:** one exact value or set; for `pilihan-ganda-kompleks`, every correct point listed.
- **Distractors:** each from one slip: the intersection skipped (MATW25-001, A: {2, 3, 5, 7}) or 0 counted as a natural number (D: {0, 2, 3, 4, 5, 7}); the sign of each entry flipped in an inverse (MATL25-001, D); the reciprocal of the answer (MATL25-025, D: 2/3 for 3/2); the denominator 76 instead of 67 (MATL25-022); a rotation in the wrong direction.
- **Watch:** list every root or point among the options (MATL25-005 omits (−4, 0)). Check a limit numerically on both sides (MATL25-025: 1,5000 from both sides).
- **Examples:** MATW25-001, 002; MATL25-001, 005, 016, 021, 022, 025.

### MAT-PARAM: Menentukan unsur yang belum diketahui (level 2)

- **Asks:** work backwards from a condition or an image to an unknown: a value in a defined operation, a pre-image point, polynomial coefficients from a remainder, a vector parameter from its length, a missing vertex, line coefficients or a translation and scale factor from the images.
- **Stem patterns:** "Jika a ⊙ 2 = 5, tentukan Benar atau Salah ..." · "Titik B' pada gambar merupakan bayangan titik B ... Gambar titik B yang sesuai adalah ...." · "... menghasilkan sisa 5x − 1, Nilai dari a + b = ..." · "Jika nilai vektor AB = 9 satuan panjang, maka nilai m yang memenuhi ... adalah" · "Pernyataan yang benar mengenai translasi T dan faktor skala dilatasi ... adalah ...."
- **Key:** the unknown that satisfies every condition, with rejected roots stated (MATW25-003 rejects a = −1 because a ≥ 0; MATL25-020 notes that scale −2 gives T = (7, −5), not an option).
- **Distractors:** transformations undone in the wrong order (MATW25-014); one root with the wrong sign (MATL25-012: "−4 atau −3", "−3 atau 4"); the right translation with a wrong scale (MATL25-020: 4, the area ratio, and 8); the other translation T = [1; 1].
- **Watch:** say "panjang vektor" or |AB|, not "nilai vektor" (MATL25-012). Put the unknown's domain in the stem when it rejects a root.
- **Examples:** MATW25-003, 014; MATL25-008, 012, 013, 019, 020.

### MAT-MODEL: Memodelkan situasi ke bentuk matematis (level 2)

- **Asks:** turn a story, table or figure into a sequence, a system of equations or inequalities, a matrix product, a counting rule or a probability, then solve it.
- **Stimulus:** a short everyday situation with all quantities; a table or figure when the data are many (hotel rooms, bouquets, feed per animal).
- **Stem patterns:** "... maka berapa banyak penonton yang memegang kertas koreo di baris ke-5?" · "Pada hari keberapa pasien merasa nyaman namun belum dianggap sembuh secara klinis?" · "Daerah yang diarsir pada gambar tersebut merupakan himpunan penyelesaian dari sistem pertidaksamaan ...." · "Jika banyaknya sapi dan kambing ... berturut-turut adalah x dan y, maka [x; y] = ..." · "Berapakah peluang Rini mengambil angpao yang kosong?"
- **Key:** the solution of the model; when the options are models (MATW25-008, MATL25-003), the one model that is both correctly set up and correctly evaluated.
- **Distractors:** an extra constraint that cuts the region (MATW25-008: x ≥ 0 when the region reaches x = −4); a reversed inequality; a matrix product written in the wrong order or with the vector swapped (MATL25-003, option C gives [30; 40] and D gives [21/5; −4]); the nth term for the (n−1)th; counting a block without its two internal orders (6 instead of 12, MATW25-022).
- **Watch:** check the printed totals against the model (MATL25-004, section 2). Fix the starting term of a sequence (MATW25-007). Every number the model needs must be printed, not counted from a small picture (MATW25-009).
- **Examples:** MATW25-006, 007, 008, 009, 022, 024; MATL25-002, 003, 004.

### MAT-FUNGSI: Menafsirkan model fungsi yang diberikan (level 2)

- **Asks:** use a function the stem gives (linear, polynomial, exponential, trigonometric, rational) to find an input, an output, a parameter read from its graph, a long-run value, or to judge what the model says.
- **Stimulus:** the function in the text, or its graph with marked points (MATL25-010: (0, 10), (1, 70), (2, 490); MATL25-011: 14,3 m at t = 0, 10,3 m at t = 6).
- **Stem patterns:** "Pada tahun berapakah peningkatan suhu diperkirakan mencapai 0,7°C?" · "Bagaimana interpretasi yang tepat mengenai model eksponensial populasi kelinci tersebut?" · "Waktu saat kedalaman air laut mencapai 12,3 meter untuk ketiga kalinya setelah pukul 00.00 adalah ...." · "Keuntungan yang akan diperoleh Roni, apabila dia menjual nasi goreng dengan porsi sangat banyak adalah ...." · "... tentukan Mungkin atau Tidak Mungkin perusahaan dapat menjual sejumlah unit saham berikut!"
- **Key:** the value or statement the model gives; check every candidate input in the function (MATL25-007: f(40) = f(60) = 2.000, f(30) = 20.000).
- **Distractors:** the base of a power taken as the growth per period of the exponent's denominator ("setiap 4 tahun ... 4 kalinya", MATL25-009); the first or second crossing instead of the third (MATL25-011: 3 and 9 for 15); the ratio of constant terms instead of leading coefficients in a limit at infinity (MATL25-023: 5 instead of 3); the scalar applied to only some terms (MATL25-006); a root whose sign was dropped (MATL25-007: 30 for the root −30).
- **Watch:** the context must make the function's domain sensible (a "year" model y = 0,02x − 39,9; shares as a cubic with a negative root). Say "p menuju tak hingga" as a limit when that is meant.
- **Examples:** MATW25-004; MATL25-006, 007, 009, 010, 011, 023.

### MAT-UKUR: Menghitung ukuran bangun (level 2)

- **Asks:** a length, angle ratio, perimeter, area or count along a length, using similarity, Pythagoras, trigonometric ratios, distance in space or composite areas.
- **Stimulus:** a figure with every length labelled; a context (garden, classroom, clock ornament, train line, road sign) when the type is applied.
- **Stem patterns:** "Diketahui trapesium KLMN dan NMPO sebangun. ... berapakah panjang sisi LM?" · "... tentukan benar atau salah pernyataan berkaitan dengan ukuran sisi kebun ..." · "... berapa panjang kayu tipis yang ia perlukan?" · "Manakah stasiun-stasiun yang jaraknya kurang dari 3,5 km?"
- **Key:** one length or area, exact (8√5 cm) or with the stated π; check Pythagorean triples are intended (MATW25-013: 150, 360, 390; MATW25-016: 25, 60, 65).
- **Distractors:** the corresponding side of the other figure (MATW25-012, A: MP = 6√5 cm); the full circle instead of the visible half (MATW25-016, E: 445,6 cm); a sine and cosine swapped (MATW25-020: sin β = √7/4 is cos β); a distance in proportion to the wrong time.
- **Watch:** give π and the position of every part (MATW25-016). Give every length a composite area needs (MATL25-017). Option wording must say what is compared: MATL25-017's "Setengah hitam dan biru" is unreadable; write "cat biru lebih banyak daripada setengah cat hitam".
- **Examples:** MATW25-012, 013, 015, 016, 020; MATL25-014, 017.

### MAT-KEPUTUSAN: Memilih yang terbaik dengan batasan (level 3)

- **Asks:** decide the maximum, the minimum cost, or the choice that "pas" a stated tolerance, after computing a length, area or volume.
- **Stem patterns:** "... berapa paling banyak kardus helm yang dapat dimuat di truk tersebut?" · "... berapakah biaya minimal yang harus dikeluarkan Bu Sita untuk membeli stiker vinil tersebut?" · "Tentukan apakah pilihan logam yang akan dibeli Pak Baskara berikut ini Pas atau Tidak Pas!"
- **Key:** the option that meets the goal and the constraint, found by computing every option: MATW25-018 360 boxes (20 cm sides along 240 cm, 30 cm sides along 150 cm); MATW25-019 30 sheets (8.800/300 = 29,3, rounded up) = Rp270.000,00; MATL25-018 frame 635,2 cm, so 6,5 m leaves 0,15 m (Pas), 8 m leaves 1,65 m (Tidak Pas), 5 m is short.
- **Distractors:** the other orientation (MATW25-018, 336); rounding per object instead of in total (MATW25-019, 4 sheets × 8 = 32 = Rp288.000,00); meets the length but breaks the tolerance (2 logam A).
- **Watch:** state the constraint as a number ("sisa tidak lebih dari 1 m" is good). Say whether leftover material may be shared between objects (MATW25-019) and which parts belong to the frame (MATL25-018: without the diagonals it is 475,2 cm and logam B becomes Pas).
- **Examples:** MATW25-018, 019; MATL25-018.

### MAT-NALAR: Menalar dari syarat (level 3)

- **Asks:** decide what must, may or cannot be true given conditions (a mean, a median, bounds, unknown discounts, papers returned to a box), whether given statements are sufficient to answer a question, or which general claims about a result hold.
- **Formats:** `pilihan-ganda` (including the sufficiency format with five fixed options), `pilihan-ganda-kompleks`, `benar-salah` with "pasti" / "mungkin" statements.
- **Stem patterns:** "Dengan uang yang dimiliki, siapakah siswa yang pasti dapat mengikuti kursus?" · "Putuskan apakah pernyataan (1) dan pernyataan (2) berikut cukup untuk menjawab permasalahan dalam kotak tersebut!" · "Banyak pengunjung pada hari Kamis pasti lebih dari 5 orang." · "Kertas apa sajakah yang mungkin sudah terambil oleh orang-orang sebelumnya sehingga peluang Ani ... adalah 2/3?" · "... manakah pernyataan yang benar tentang nilai lim(θ→a) X/Y?"
- **Key:** found by listing every case the conditions allow: MATW25-023 has (p, r) = (6, 9), (7, 8), (8, 7), (9, 6); MATW25-025 needs all 10 prize papers left, so the four earlier draws were all blank (10/15 = 2/3; other options give 8/13 or 6/11); MATW25-005 bounds Fira's base price between Rp200.000 and about Rp285.714, so the highest fee is about Rp228.571 and all four can enrol.
- **Distractors:** true in one case but not all ("pasti" claims); a statement that is possible but offered as impossible; the "one statement alone is enough" option when a hidden position is still free (MATW25-017).
- **Watch:** list the cases in `alasan`. In a sufficiency item, check both statements alone and together, including degenerate figures. Make "pasti" and "mungkin" explicit in every statement. For general claims about a formula (MATL25-024), compute the formula (X/Y = 2cot(θ/2)/π) and check every option against it; as printed, θ → π/6 gives about 2,38, not 2/π.
- **Examples:** MATW25-005, 017, 023, 025; MATL25-024.

## 4. Known weak spots in the 2025 papers

Avoid repeating these in generated items:

- Inconsistent printed data (MATL25-004).
- A correct answer missing from the options (MATL25-005), or a "more than one answer" item with one true option (MATL25-024, probably π/2 misprinted as π/6).
- Ambiguous wording that changes the key (MATW25-007, 011, 013, 015, 022; MATL25-018).
- Units of the question differing from the units of the data (MATW25-006: sheets vs people).
- Unreadable or incomplete figures and options (MATW25-009, 015; MATL25-016, 017).
- Indicators that do not match their item (MATL25-007, 012).
- A truncated stem (MATL25-015, no "adalah ....") and an item with 4 options (MATL25-012).
