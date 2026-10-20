# TKA template: Ekonomi

Describes the TKA 2025 Ekonomi paper (pilihan, 30 items, numbers 1–30 complete) as 6 item types. Codes, levels and examples are in `data/tka-types.json`; level names are in `specs/tka-item-types.md`.

## 1. The paper at a glance

- **One stimulus per item.** No stimulus is shared. Most items are a short case (50–125 words including the question) about a fictional firm, cooperative or person ("Adiwastra Jaya", "Koperasi Kilau Gemitang", Safia, Pak Faiz), or a real Indonesian situation (UMP 2025, BPS data, Hari Raya inflation, the 2023 US shrimp anti-dumping petition, a BI cut to the reserve ratio). 9 items carry a table (EKO25-005, 008, 010, 011, 013, 015, 016, 024, 030), 1 a graph (EKO25-007). EKO25-009 and 017 have only a one-sentence lead-in.
- **Formats.** 18 `pilihan-ganda`, 10 `pilihan-ganda-kompleks` ("Jawaban benar lebih dari satu"), 2 `benar-salah` (columns Benar / Salah: EKO25-010, 012).
- **Content.** Each item names an *elemen* (Konsep Dasar Ilmu Ekonomi; Ekonomi Mikro dan Makro; Ekonomi Internasional; Konsep Dasar Akuntansi) and a *subelemen*. The item type is independent of the topic: EKO-HITUNG covers opportunity cost, supply functions, tax equilibrium, national income, price indices, SHU and the accounting equation.
- **Key confidence.** 19 proposed keys are `tinggi`, 8 `sedang`, 3 `rendah` (EKO25-006, 011, 028). The weak keys cluster in `pilihan-ganda-kompleks` and in items judged against data.

| Type | Level | Items |
|---|---|---|
| EKO-IDEN | 1 | 3 |
| EKO-KLAS | 2 | 4 |
| EKO-HITUNG | 2 | 8 |
| EKO-DATA | 2 | 3 |
| EKO-DAMPAK | 2 | 4 |
| EKO-SOLUSI | 3 | 8 |

## 2. Rules for every Ekonomi item

- **Compute the scenario before writing the statements.** EKO25-006 prints a tax of Rp25,00 per unit, which moves the equilibrium from P = 16, Q = 180 to P = 21, Q = 80 (price +Rp5, quantity −100). No statement matches; statements C, D and E are true only for a tax of Rp15,00 (P = 19, Q = 120, +Rp3, −60). Compute the key and every numerical distractor in Python and record the steps in `alasan`.
- **Use the textbook definition, and only one.** EKO25-002 (opportunity cost) has both Rp10.000.000,00 (best forgone alternative, the textbook rule) and Rp12.000.000,00 (sum of all forgone alternatives) among its options. Do not offer the value from a rival convention.
- **One measure per claim.** EKO25-011 has statement C ("kesejahteraan Indonesia lebih tinggi", true by income per capita) and D ("kesejahteraan Vietnam lebih tinggi", true by IPM). Name the indicator in the statement ("berdasarkan IPM ...").
- **Label data correctly.** EKO25-011's row "Produk Domestik Bruto (PDB)" holds growth rates (7,09%, 5,03%). EKO25-016 asks which sector "paling berdampak terhadap tingkat inflasi" without sector weights, so only the index rise can be compared; ask for that.
- **Statements must be complete sentences and free of misprints that flip the meaning.** EKO25-010 statement 1 ends "menunjukkan bahwa ketimpangan pendapatan." with the verb missing; EKO25-019 statement E reads "dengan pengawasan alokasi kredit" where "tanpa" is almost certainly meant, which decides whether E is in the key.
- **Every part of a compound statement must hold.** EKO25-021 statement A says Ibu Rani pays an indirect tax, but she also pays PPh Final UMKM (direct). EKO25-018 statement B adds a fiscal purpose ("mendukung pembiayaan fiskal") to a monetary action.
- **In `pilihan-ganda-kompleks`, ask for one kind of thing.** EKO25-027 asks for impacts, but statement C ("harus meningkatkan sertifikasi") is a response. EKO25-028's "perubahan pada aset maupun kewajiban" can mean "either" or "both", and gives the transactions without the numbers the options use.
- **Names, numbers and facts consistent across stimulus and options.** EKO25-012 writes "Andi" in the stimulus and "Andy" in statement 3. Real data (BPS, BI, UMP) must state its year and source and be checked; the paper's Gini, TPT and growth figures are cited to BPS.
- **Notation:** Rupiah as in the paper (Rp10.000.000,00), decimal commas, functions as "Qd = -20P + 500". Indonesian textbook terms: *biaya peluang*, *pengangguran friksional/struktural/siklis*, *fungsi budgeter/regulerend*, *jasa modal*, *jasa usaha*, *prive*.

## 3. Item types

### EKO-IDEN: Mengenali konsep, faktor, atau fungsi ekonomi (level 1)

- **Asks:** which listed items are a named concept (factors of growth, functions of Bank Indonesia), or which cause the case states.
- **Stimulus:** none or one sentence (EKO25-009, 017), or a short case whose cause is written in it (EKO25-014: Ramadan demand up, harvest down).
- **Stem patterns:** "Berikut ini mana yang merupakan peran dan fungsi Bank Indonesia?" · "... manakah faktor yang dapat memengaruhi pertumbuhan ekonomi suatu negara?" · "Berdasarkan ilustrasi tersebut, faktor utama yang menyebabkan inflasi adalah ...."
- **Key:** the textbook list item, or a paraphrase of the cause stated in the case.
- **Distractors:** the function of a neighbouring institution (giro, tabungan and direct credit are commercial-bank functions, EKO25-017 B and D); a real cause not mentioned in the case (exchange rate, wages, fuel prices in EKO25-014); a policy that is distribution, not a growth factor (bantuan sosial, EKO25-009 D).
- **Watch:** keep borderline items out. EKO25-009 E (price stability) is arguably a growth factor.
- **Examples:** EKO25-009, 014, 017.

### EKO-KLAS: Menggolongkan kasus ke jenis atau konsep (level 2)

- **Asks:** sort several described cases into categories: types of unemployment, direct vs indirect tax and tax functions, bilateral/regional/multilateral cooperation, the effect of each transaction on the accounting equation.
- **Stimulus:** 3–5 short cases or transactions, each identifiable on its own.
- **Stem patterns:** "Tentukan Benar atau Salah pernyataan berikut ini terkait jenis pengangguran yang dialami oleh masing-masing individu." · "... apa jenis kerja sama internasional yang tepat?" · "... manakah pernyataan berikut yang benar terkait jenis pajak, peran, fungsi, dan prinsip pajak?"
- **Key:** each case placed by the defining feature the textbook uses (first job search = friksional; skills mismatch = struktural; layoff from falling demand = siklis).
- **Distractors:** categories swapped between two cases (EKO25-025 options rotate the three labels); a pair statement where one case fits and the other does not (EKO25-012 statement 1).
- **Watch:** number the cases if the options refer to numbers (EKO25-028 does not). Avoid cases the books classify differently (EKO25-012: Bagas is *sukarela* in some books, *friksional* in others).
- **Examples:** EKO25-012, 021, 025, 028.

### EKO-HITUNG: Menghitung dari data (level 2)

- **Asks:** compute one value with one procedure: opportunity cost, quantity supplied after a price change, equilibrium before and after a tax, Disposable Income, a simple aggregate price index, a member's SHU, the accounting equation after a transaction, opening capital.
- **Stimulus:** a table or a short list of values, with extra rows the student must ignore (EKO25-008 lists C, I, G, X, M that are not needed for DI).
- **Stem patterns:** "Berapakah jumlah biaya peluang yang dikorbankan oleh Safia apabila ...?" · "Berdasarkan data tersebut, besarnya Disposible Income (DI) adalah ...." · "Besarnya nilai Indeks Harga Konsumen (IHK) tahun 2025 dengan metode agregatif sederhana adalah ...." · "Berdasarkan data tersebut, besarnya modal awal adalah ...."
- **Key:** one clean result in the paper's units (Rp, kg, unit, %).
- **Distractors:** each from one mistake. Checked examples: EKO25-005 mixes quantities at the old price (tepung 2.500, telur 1.700, gula 4.800) with the new ones (3.250, 1.820, 5.700). EKO25-030 key 125.200.000 = 195.000.000 − 72.300.000 + 2.500.000; 122.700.000 ignores prive, 120.200.000 subtracts it, 267.300.000 and 269.800.000 add the profit. EKO25-002 adds both forgone alternatives (12.000.000).
- **Watch:** check that the data are consistent (EKO25-008: C + I + G + X − M = 1.200.000 = PDB, as it should be) and that the printed numbers give the intended key (EKO25-006 does not).
- **Examples:** EKO25-002, 005, 006, 008, 015, 024, 029, 030.

### EKO-DATA: Menafsirkan tabel atau data statistik (level 2)

- **Asks:** judge statements against a data table: growth vs Gini over years, two countries' indicators, price-index rises by sector.
- **Stimulus:** a table of 3–5 rows with its source and year (BPS 2020–2024 growth and Gini; Vietnam and Indonesia 2024; IHK by sector 2022–2025).
- **Stem patterns:** "Berdasarkan data di atas, lakukan analisis bagaimana keterkaitan pertumbuhan ekonomi dengan kesejahteraan masyarakat ..." · "Berdasarkan informasi tersebut manakah pernyataan yang tepat terkait kondisi pembangunan ekonomi di kedua negara?" · "Berdasarkan tabel tersebut, manakah sektor yang paling berdampak terhadap tingkat inflasi?"
- **Key:** a statement each part of which the table proves; quote the rows in `alasan`.
- **Distractors:** an "always/never" generalisation one row breaks (EKO25-010 statement 3, broken by 2021); the biggest single-year jump offered as the biggest overall rise (EKO25-016 B: transport 107 to 115, 7,48%, while health rises 18% overall); a comparison reversed (EKO25-011 B says Indonesia grew faster).
- **Watch:** a statement about a trend must match every year it names. EKO25-010 statement 1 calls 2021–2023 "peningkatan pertumbuhan", but 2023 (5,05) is below 2022 (5,31).
- **Examples:** EKO25-010, 011, 016.

### EKO-DAMPAK: Memprediksi dampak perubahan atau kebijakan (level 2)

- **Asks:** what one change does: a cost rise to market equilibrium, a complement's price to the demand curve, a regulatory tax to consumption, an anti-dumping duty to export competitiveness.
- **Stimulus:** a case naming the change; for curve shifts, a graph with labelled curves.
- **Stem patterns:** "Kenaikan biaya produksi tersebut akan berdampak pada keseimbangan pasar yaitu ...." · "... maka analisis perubahan permintaan sepeda motor yang baru adalah...." · "Berdasarkan ilustrasi tersebut, dampak yang paling tepat dari penerapan fungsi regulasi pajak adalah...." · "Manakah yang merupakan dampak logis terhadap daya saing ekspor udang Indonesia ...?"
- **Key:** the textbook chain in one step (cost up → supply left → price up, quantity down).
- **Distractors:** the opposite direction (EKO25-027 A and D: Indonesian shrimp cheaper); price and quantity both up (movement along vs shift confused); a second-order effect stated as the main one (EKO25-020 E).
- **Watch:** two options must not name the same point. EKO25-007 B ("bergerak kebawah (D3)") and D ("bergeser ke kiri (Q3)") both point to D3, and the figure has an unexplained thick curve. Use "bergeser ke kiri/kanan" for curve shifts and draw only the curves the item uses.
- **Examples:** EKO25-004, 007, 020, 027.

### EKO-SOLUSI: Memilih atau menilai solusi dan kebijakan (level 3)

- **Asks:** the best solution to a stated problem (land scarcity, rising input costs, youth unemployment, inflation, cash-flow mismanagement, a trade deficit), or which statements correctly judge a policy already taken (EKO25-019, BI lowers the reserve ratio).
- **Stimulus:** a case of 70–125 words that names the root cause and, often, the goal or constraint ("tanpa mengorbankan kualitas", "melindungi industri nasional").
- **Stem patterns:** "... manakah tindakan yang paling tepat diambil oleh perusahaan dengan mempertimbangkan prinsip ekonomi?" · "Berdasarkan informasi, solusi apa yang paling tepat untuk mengatasi permasalahan tersebut?" · "... kebijakan moneter apa yang sesuai untuk mengantisipasi kondisi tersebut?" · "Manakah pernyataan berikut yang tepat menggambarkan konsekuensi dan efektivitas dari kebijakan tersebut?"
- **Key:** acts on the root cause the case names and keeps its constraint (EKO25-023: plan cash flow and separate project funds; EKO25-013: skills training, since the case names a skills mismatch).
- **Distractors:** an extreme measure ("menghentikan seluruh pembangunan", "menaikkan harga jual dua kali lipat"); a measure that treats a symptom (a bank loan for a cash-flow problem); one that breaks the constraint (cheaper synthetic inputs that lower quality, EKO25-003 B and D); for monetary items, an expansionary tool offered against inflation (EKO25-018 C–E); an "otomatis" claim (EKO25-019 D).
- **Watch:** in `pilihan-ganda-kompleks`, every keyed option must be clearly better than every unkeyed one. EKO25-022 D (research into synthetic leather) needs the capital the firm lacks, yet is proposed as correct.
- **Examples:** EKO25-001, 003, 013, 018, 019, 022, 023, 026.

## 4. Known weak spots in the 2025 paper

- **EKO25-006** has no correct statement as printed (section 2). Its key (C, D, E) assumes a tax of Rp15,00. Option A reverses the order of the correct quantities (180 before, 80 after).
- **EKO25-001** option E is cut off in the source screenshot after "untuk".
- **Three `rendah` keys** (EKO25-006, 011, 028) and several `sedang` keys in `pilihan-ganda-kompleks` (009, 018, 019, 021, 022, 027) depend on what the item writer meant. Check them against the official key before using them as reference answers.
