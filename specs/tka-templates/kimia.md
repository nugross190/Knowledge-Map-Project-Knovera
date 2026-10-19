# TKA template: Kimia

Describes the TKA 2025 Kimia paper (pilihan, 23 of 25 items; numbers 2 and 16 missing from the source) as 6 item types. Codes, levels and examples are in `data/tka-types.json`.

## 1. The paper at a glance

- **One stimulus per item.** No stimulus is shared. Most items open with a short applied context (industry, pollution, medicine, household products) and end with the data needed: a reaction equation, Ar or Mr values, a table, or a graph. 15 items carry a figure or table: figures in 006, 007, 008 (a structure inside a statement), 009, 017, 020, 022, 023, 025; tables in 001, 009, 011, 012, 013, 014, 021.
- **Formats.** 19 `pilihan-ganda`, 1 `pilihan-ganda-kompleks` (007), 3 `benar-salah` with three statements each (006, 008, 009; columns Benar / Salah).
- **Content.** Each item names an *elemen*: Kimia Analitik (9 items), Kimia Fisik (6), Kimia Dasar (5, all stoikiometri), Kimia Organik (3, hydrocarbons). The item type is independent of the topic: KIM-KELAYAKAN covers stoichiometry, titration, concentration, colligative properties, thermochemistry and equilibrium.
- **Source facts.** The PDF holds one item per page; page 1 notes "SOAL NO.2 OTW" and page 14 "SOAL NO.16 OTW". Item numbers come from the number in brackets at the end of each indicator. Typos are copied verbatim ("dangat rendah", "makroskpis", "Tak berwana"), including broken formulas in options (010 option C "₃O⁺", 025 option A "X₂⁺", 024 option C "H2O").
- **Keys.** None official. 16 keys are `tinggi`, 6 `sedang` (006, 009, 012, 017, 022, 025), 1 `rendah` (007). Every calculation was re-checked in Python.

| Type | Level | Items |
|---|---|---|
| KIM-HITUNG | 2 | 5 |
| KIM-DATA | 2 | 3 |
| KIM-KONSEP | 2 | 5 |
| KIM-ANALISIS | 3 | 2 |
| KIM-PREDIKSI | 3 | 2 |
| KIM-KELAYAKAN | 3 | 6 |

## 2. Rules for every Kimia item

- **Give every constant the solution needs.** KIM25-004 asks for molecules at 25 °C and 1 atm but gives no R; the key needs R = 0,082 L atm mol⁻¹ K⁻¹. State R, Kf, Ksp, Ar and the temperature in kelvin or °C as the paper does.
- **Balance every equation you print** unless the item asks the student to balance it (003 marks "(belum setara)"). KIM25-024's equation has H 2 and O 5 on the left, H 4 and O 6 on the right.
- **Name the quantity exactly.** KIM25-012 gives "kadar 0,1%" without saying mass or volume percent, and no density; KIM25-017 dissolves the three solutes "dalam jumlah sama" without saying moles or mass. KIM25-014 shows the fix: "dalam persen massa per 100 mL" with density 1 g/mL.
- **The scenario must match the indicator's concept.** KIM25-005 is indicated as a limiting-reagent item, but 0,5 mol CuO and 0,25 mol C react exactly 2 : 1, so there is no limiting reagent. If the item is about a limiting reagent, make one reagent run out.
- **Stay inside the formula's range.** KIM25-019 uses ΔTf = Kf·m for a 15 molal solution, far outside the dilute range. Keep concentrations dilute (≤ 1 m) for colligative items.
- **One key.** In KIM25-022 options B and C are both thermodynamically right; in 007 the key depends on which fraction table the setter used. Either narrow the options until one is right, or give the reference data (boiling ranges of the fractions) in the stimulus.
- **Values read from a graph must be readable.** 007 and 017 rely on approximate point and needle readings. Print the needed values in the figure, and record them in `gambar`.
- **Compute the key and every numerical distractor in Python** and record the steps in `alasan`. Round the key correctly: 004's key is printed 2,95 × 10¹⁷ for 2,956 × 10¹⁷. Each distractor should come from a named mistake in `catatan_transkripsi` (for example "C: tanpa faktor van't Hoff").
- **Notation:** Unicode subscripts and superscripts (H₂SO₄, SO₄²⁻, 10⁻⁶), decimal commas, units as in the paper (M, mL, g/mL, kJ/mol, °C/molal, atm). Check every option for dropped characters.

## 3. Item types

### KIM-HITUNG: Menghitung besaran stoikiometri atau larutan (level 2)

- **Asks:** one result from mole relations: percent of an element, gas volume from two combustions, number of molecules, product mass, osmotic pressure.
- **Stimulus:** a short context, the reaction or data table, and the constants.
- **Stem patterns:** "Senyawa yang memiliki kandungan fosfor tertinggi adalah .... (diketahui Ar P = 31)" · "Berapakah volume total gas CO₂ yang dihasilkan dari pembakaran campuran tersebut jika semua gas diukur pada suhu dan tekanan yang sama?" · "Berapakah jumlah molekul SO₂ yang terdeteksi dalam sampel?" · "... berapa gram tembaga murni (Cu) maksimum yang dapat diperoleh?" · "Berapakah tekanan osmotik larutan KCl tersebut?"
- **Key:** one clean value with units. Checked: 001 kadar P = 31/Mr, highest for NaH₂PO₄ (25,8%); 003 x + y = 10 and 3x + 4y = 36 give 4 L ethane, 6 L propane, 26 L CO₂; 005 31,75 g; 018 π = MRTi = 0,2 × 0,082 × 300 × 2 = 9,84 atm.
- **Distractors:** each from one mistake: no van't Hoff factor (018: 4,92 atm); T in °C instead of K (018: 0,88 atm; 0,44 atm also without i); molar volume 22,4 L at a non-STP temperature (004: option C is ten times that result); the CO₂ of one gas only (003: 8 L, 18 L); mole ratio ignored (005: 16 g ≈ 0,25 mol × 63,5).
- **Watch:** give R and temperature; make sure each distractor's mistake is one a student actually makes, and write it down.
- **Examples:** KIM25-001, 003, 004, 005, 018.

### KIM-DATA: Menafsirkan grafik atau tabel percobaan (level 2)

- **Asks:** read a graph or observation table and name the substance, reactant or use it points to.
- **Stimulus:** a boiling point vs molecular mass graph (007), a conductivity table for melts and solutions (013), a concentration vs time graph (020).
- **Stem patterns:** "Berdasarkan grafik, tentukan pasangan senyawa hidrokarbon dengan potensi pemanfaatannya yang benar!" · "Berdasarkan data hasil percobaan, manakah kemungkinan pasangan zat/senyawa yang sesuai dengan hasil percobaan?" · "Berdasarkan grafik tersebut, reaktan dari reaksi tersebut adalah ...."
- **Key:** follows from one reading rule: a falling curve is a reactant (020); conducts as melt and solution → ionic, only in solution → polar covalent, weakly → weak electrolyte (013).
- **Distractors:** a mixed pair (one reactant, one product in 020); an ionic compound where the melt does not conduct (013 options A, D, E); a weak electrolyte where the solution conducts strongly (013 option C); a neighbouring fraction (007).
- **Watch:** 007 is `rendah` because the boiling ranges of fractions differ between textbooks. Give the fraction table in the stimulus when the key needs it.
- **Examples:** KIM25-007 (`pilihan-ganda-kompleks`), 013, 020.

### KIM-KONSEP: Menerapkan konsep (level 2)

- **Asks:** apply one definition or principle to name a species, predict an observation, or explain a phenomenon: a conjugate acid–base pair, indicator colours, oxidising agent, anode and cathode, vapour pressure lowering.
- **Stem patterns:** "Berdasarkan reaksi dan teori Bronsted-Lowry, manakah yang merupakan pasangan asam-basa konjugasi yang tepat?" · "... dugaan peneliti kemungkinan benar jika sampel tersebut ditetesi indikator fenolftalein menunjukkan warna ...." · "... zat apakah yang bertindak sebagai oksidator dalam reaksi pada baterai alkalin?" · "... manakah pernyataan berikut yang tepat mengenai reaksi reduksi dan oksidasi pada sel volta tersebut?" · "... pernyataan berikut yang benar terkait tekanan uap dari ketiga larutan adalah ...."
- **Key:** the definition applied correctly (NH₄⁺/NH₃ differ by one H⁺; Mn +4 → +3 so MnO₂ is the oxidiser; electrons leave Y, so Y is the anode and loses mass).
- **Distractors:** the two reactants (NH₄⁺ and H₂O) or the two products (NH₃ and H₃O⁺) as a pair; the reducing agent for the oxidising agent (Zn); the product for the reactant (Mn₂O₃); anode and cathode swapped (025 options A, C, D, E); the right observation with a wrong reason (017 options C, D).
- **Watch:** in 025 the key depends only on the direction of the electron arrow; describe it in words in `gambar`. In 017, a volatile solute (methanol) breaks the simple "more particles, lower vapour pressure" rule; if you use it, the key must say so, as 017 option B does.
- **Examples:** KIM25-010, 011, 017, 024, 025.

### KIM-ANALISIS: Rumus, struktur, dan sifat senyawa (level 3)

- **Asks:** judge statements about an organic compound from combined data: combustion products, carbon types, ΔHc of isomers.
- **Stimulus:** a description and numbers (2 mol → 8 mol CO₂ + 10 mol H₂O; 2 primary and 2 secondary C), or structures with a ΔHc table.
- **Stem pattern:** "Bagaimana hasil analisis terhadap senyawa hidrokarbon tersebut? Tentukan Benar atau Salah untuk setiap pernyataan berikut ..."
- **Key:** each statement checked separately: formula from combustion (C₄H₁₀); structure from carbon types (n-butana); straight chain boils higher than its branched isomer; the isomer releasing less heat is more stable; carbon in CO₂ is sp, not sp³.
- **Distractors (false statements):** a property reversed (008 statement 3); a property of the wrong substance (009 statement 3, hybridisation of the product's carbon).
- **Watch:** define loaded words. 009 statement 1 uses "efisiensi pembakaran", which the key reads as energy per mole; say that in the statement.
- **Examples:** KIM25-008, 009 (both `benar-salah`).

### KIM-PREDIKSI: Pergeseran kesetimbangan atau endapan (level 3)

- **Asks:** predict whether a precipitate forms, or which way an equilibrium shifts, after working out the needed relation.
- **Stimulus:** concentrations and volumes with Ksp (015); a concentration vs time graph from which the equation must be read (023).
- **Stem patterns:** "... manakah pernyataan yang tepat mengenai kemungkinan terbentuknya endapan CaSO₄ pada percobaan yang dilakukan?" · "Berdasarkan grafik reaksi kesetimbangan tersebut, apakah yang terjadi jika tekanan wadah dinaikkan dua kali lipat?"
- **Key:** computed first, then the rule. 015: after mixing to 200 mL, [Ca²⁺] = 0,005 M and [SO₄²⁻] = 0,01 M, Q = 5 × 10⁻⁵ > Ksp 2,4 × 10⁻⁶, so a precipitate forms. 023: A falls by 4, B by 2, A₂B rises by 2, so 2A + B ⇌ A₂B; higher pressure shifts to fewer gas moles, to the right.
- **Distractors:** the right outcome with the Q/Ksp comparison reversed (015 option D); the reverse outcome with a true-sounding reason (015 options B, E); the wrong direction or "no shift because all are gases" (023).
- **Watch:** remember the dilution on mixing; a distractor from forgetting it should be written down. Graph values must be exact (023 gives 6 → 2, 5 → 3, 0 → 2).
- **Examples:** KIM25-015, 023.

### KIM-KELAYAKAN: Menilai kelayakan terhadap standar atau tujuan (level 3)

- **Asks:** decide whether a product, formulation, mixture or decision meets a stated standard or goal, after a calculation: titration against a label, a syrup against safety limits, antifreeze against a temperature, the cleanest fuel, the best reactor temperature, compositions giving a target mass.
- **Stimulus:** the goal or standard as numbers, the data, and the constants.
- **Stem patterns:** "... manakah pernyataan yang tepat mengenai kadar NaOH dalam deterjen cair tersebut?" · "Pernyataan manakah yang paling tepat mengenai komposisi sirup tersebut?" · "... apakah larutan antibeku tersebut dapat mencegah pembentukan es ketika pesawat terbang di daerah dengan suhu −22,3°C?" · "... senyawa yang dapat dijadikan sebagai bahan bakar yang paling ramah lingkungan adalah ..." · "Agar gas etanol yang dihasilkan meningkat, upaya terbaik yang dapat dilakukan ... adalah ..." · "Secara teori, manakah komposisi berikut yang jika direaksikan akan menghasilkan tepat 29,8 gram kristal KCl?"
- **Key:** a verdict with the number that supports it. Checked: 012 mean V HCl 8,0 mL → 0,04 M diluted → 0,4 M → 1,6%; 014 dekstrometorfan 1,2%, gula 20%, perisa 0,4% (all over the limit; only option B states a right number); 019 15 molal, ΔTf 27,9 °C → −27,9 °C; 021 mol CO₂ per MJ: n-pentana 1,42, 1-pentena 1,49, siklopentana 1,52; 006 KCl from the limiting reagent: 14,9 g, 29,8 g, 29,8 g.
- **Distractors:** the right verdict with a wrong number (014 option A: 2% instead of 1,2%); the dilution factor forgotten (012: 0,16%); the molarity read as a percentage (012: 0,4%); a wrong verdict with a freezing point above 0 °C (019 options D, E); a true fact that does not answer the goal (021 option D: all give 5 mol CO₂ per mole); the right direction with the wrong Kc change (022 option A); the wrong direction (022 options D, E).
- **Watch:** the goal must decide one option. 022 keys B (300–400 °C) over C (25–400 °C) by appeal to reaction rate, which the stimulus never mentions; 006 leaves excess KOH, so "tepat 29,8 gram kristal" holds only for the KCl formed. State the extra constraint (rate, purity) in the stem or drop the option.
- **Examples:** KIM25-006 (`benar-salah`), 012, 014, 019, 021, 022.

## 4. Known weak spots in the 2025 paper

Avoid repeating these in generated items:

- An indicator box that does not match the item: 021 is labelled Elektrokimia but is about combustion enthalpy; 025 says "elektrolisis" for a voltaic cell; 005 says limiting reagent for exact stoichiometry.
- A missing constant (004, no R) and an unbalanced equation (024).
- Unclear quantities: percent type (012), "jumlah sama" (017).
- Two defensible options (022 B and C) and a key that depends on an unstated reference table (007).
- Dropped characters in options (010, 024, 025).
