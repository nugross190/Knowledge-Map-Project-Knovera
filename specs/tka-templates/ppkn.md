# TKA template: Pendidikan Pancasila (PPKn)

Describes the TKA 2025 Pendidikan Pancasila paper (pilihan, 28 of 30 items; numbers 8 and 21 missing from the source) as 7 item types. Codes, levels and examples are in `data/tka-types.json`.

## 1. The paper at a glance

- **One short "ilustrasi" per item.** Every item opens with a case of 30–91 words: a conflict of interests, a news-like event, a programme, or a quoted article of the UUD NRI 1945. There are no figures, no tables, no source lines and no shared stimuli. Stems nearly always say "Berdasarkan ilustrasi, ...".
- **Formats.** 20 `pilihan-ganda`, 3 `pilihan-ganda-kompleks` ("Jawaban benar lebih dari satu"), 5 `benar-salah` (columns Benar / Salah).
- **Missing items.** The PDF prints "SOAL NO.8 OTW" (page 7) and "SOAL NO.21 OTW" (page 17) in place of items 8 and 21.
- **Content.** Each item names an *elemen* (Pancasila, UUD NRI Tahun 1945, Bhinneka Tunggal Ika, NKRI) and a *subelemen*. The item type is independent of the elemen: PPK-UPAYA appears under NKRI and Bhinneka Tunggal Ika alike.
- **Keys are interpretive.** 11 of 28 proposed keys have `keyakinan_kunci` = `rendah`, 8 `sedang`, 9 `tinggi`. The 9 `tinggi` keys rest on a legal rule (PPKN25-002, 011, 015), on a textbook meaning (006 *dasar negara*, 010 *sila keempat*), or on one clear phrase in the case (005, 023, 025, 027).

| Type | Level | Items |
|---|---|---|
| PPK-NILAI | 2 | 2 |
| PPK-SIKAP | 2 | 5 |
| PPK-PASAL | 2 | 3 |
| PPK-PERAN | 2 | 5 |
| PPK-ALASAN | 2 | 4 |
| PPK-TANTANGAN | 2 | 3 |
| PPK-UPAYA | 3 | 6 |

## 2. Rules for every PPKn item

- **One option must be the only good one, not the best-sounding one.** Most weak keys in this paper come from several options that are all true, positive civic statements: PPKN25-007 (all five options describe real central or regional roles), 022 (three positive statements about Pancasila), 001 (C and E both name "keseimbangan hak dan kewajiban"). Make each distractor wrong for a stated reason: it serves only one party, puts private interest first, names the wrong sila, or names the wrong institution.
- **Tie the key to a phrase in the case.** Good items make the deciding detail explicit: "uang pelican" in PPKN25-027, the three triggers (ketidakadilan, diskriminasi, hoaks) in 005, "harga lebih murah" in statement 3 of 013. If the key cannot be pointed to in the ilustrasi or in a legal text, rewrite it.
- **A stem that says "Berdasarkan ilustrasi" needs an ilustrasi.** PPKN25-002 gives only the text of Pasal 27 ayat (3) and then says "Berdasarkan ilustrasi".
- **Legal facts must be exact and cited.** Name the article (Pasal 24C, Pasal 27 ayat (2)) and check its wording. Keys about institutions follow the UUD, not common belief: in PPKN25-015 judicial review of regulations below an undang-undang is Mahkamah Agung (Pasal 24A), not MK.
- **Date-sensitive facts state their year and are checked.** The paper's own numbers ("lebih dari 1.340 suku bangsa" in 020; "sejak 1957", "lebih dari 30.000 personel" in 030) are unchecked in the bank; a generator must not reuse them without a source.
- **Benar-salah statements should differ in one deciding word,** not in vague tone. Good: 017 statement 1 ("dengan menghilangkan segala bentuk perbedaan"). Weak: 016 statement 3 is false only because of its closing phrase "dengan menyesuaikan perkembangan budaya lain", which many students will not read as wrong.
- **Indonesian textbook terms.** Use *sila*, *nilai Pancasila*, *wawasan nusantara*, *gatra*, *integrasi nasional*, *modal sosial*, *bela negara*, *kewenangan*, as the Kurikulum Merdeka books do.

## 3. Item types

### PPK-NILAI: Nilai atau sila Pancasila dalam kasus (level 2)

- **Asks:** which Pancasila value or sila a described situation or activity shows.
- **Stimulus:** a community or national activity with one dominant feature (hidup rukun dalam keberagaman; pengiriman pasukan perdamaian).
- **Stem patterns:** "Berdasarkan ilustrasi, nilai Pancasila yang paling tepat telah diterapkan pada kondisi tersebut adalah ...." · "Keunggulan nilai Pancasila dalam peran tersebut adalah...."
- **Key:** the value plus a reason drawn from the case ("Nilai Persatuan, karena perbedaan yang ada tidak menjadi penghalang untuk hidup rukun dan harmonis").
- **Distractors:** another sila with a plausible but unstated reason; the right value with a wrong reason (PPKN25-018, option D: persatuan "sesuai peran kelompok budayanya"); national interest or geopolitics presented as a value (030, options D and E).
- **Watch:** the case should show one value clearly. In PPKN25-030 the stimulus itself names "perdamaian ... keadilan sosial", so option C competes with the proposed key A.
- **Examples:** PPKN25-018, 030.

### PPK-SIKAP: Perilaku atau sikap yang sesuai (level 2)

- **Asks:** which behaviours fit a named sila, value or citizen role; the reverse direction of PPK-NILAI.
- **Formats:** `pilihan-ganda`, `pilihan-ganda-kompleks` (choose 2–3 of 5), `benar-salah` (3 statements).
- **Stem patterns:** "Perilaku yang berhubungan dengan kedua sila Pancasila tersebut adalah ..." · "Perilaku yang mencerminkan hak asasi manusia sesuai dengan sila keempat Pancasila berdasarkan ilustrasi tersebut adalah ...." · "... pernyataan mana saja yang menunjukkan sikap positif sebagai modal sosial untuk pembangunan nasional?" · "... pernyataan manakah yang menunjukkan tujuan partisipasi pemilih pemula ...?"
- **Key:** a behaviour that contains every element asked for. PPKN25-014 asks for sila 2 and sila 4 together, and only option D has both (helping flood victims, decided by musyawarah).
- **Distractors:** a behaviour that fits only one of two named sila; handing one's choice to a party or group (010, option A; 029, option D "berdasarkan kepentingan kelompok"); the right act for the wrong motive (013, statement 3: buying local because it is cheaper); haste presented as a virtue (003, option E "agar keputusan segera terwujud").
- **Watch:** in `pilihan-ganda-kompleks` every non-key option must be clearly wrong. PPKN25-003 option D and 029 option B are positive behaviours that the proposed key leaves out.
- **Examples:** PPKN25-003, 010, 013, 014, 029.

### PPK-PASAL: Pasal UUD dan kewenangan lembaga negara (level 2)

- **Asks:** apply a quoted article to an example, or name which institution has authority in a case.
- **Stimulus:** the article quoted verbatim, or a constitutional dispute (a contested Pilkada result).
- **Stem patterns:** "Berdasarkan ilustrasi, hak warga negara yang mencerminkan pasal tersebut yaitu warga negara berhak ...." · "Berdasarkan sistem ketatanegaraan Indonesia, cara menyelesaikan permasalahan tersebut sesuai kewenangan lembaga negara adalah ..." · "Klik pada pilihan Benar atau Salah dari setiap pernyataan berikut berkaitan dengan Wewenang Mahkamah Konstitusi!"
- **Key:** what the article or the UUD actually says, with the article named in `alasan`.
- **Distractors:** a neighbouring institution's authority (MA for MK, MPR for MK, Bawaslu or KPU for MK); a right/obligation pair that is true but belongs to another article (PPKN25-002, options A–D); a body making a new rule instead of deciding the case (011, options A, C, E).
- **Examples:** PPKN25-002, 011, 015.

### PPK-PERAN: Peran atau fungsi Pancasila dan Bhinneka Tunggal Ika (level 2)

- **Asks:** what role Pancasila (as dasar negara or ideologi) or Bhinneka Tunggal Ika plays in resolving a stated problem.
- **Formats:** `pilihan-ganda` or `benar-salah`.
- **Stem patterns:** "Peran Pancasila dalam memastikan bahwa ... berdasarkan ilustrasi tersebut adalah ...." · "Berdasarkan ilustrasi, pentingnya Pancasila untuk memecahkan masalah tersebut karena ...." · "... pernyataan berikut yang menunjukkan bukti bahwa Bhinneka Tunggal Ika dapat mengatasi ancaman ...!"
- **Key:** Pancasila as a guide of values for weighing the problem (006, option A), or as the bond between the parties (026, option A); Bhinneka Tunggal Ika as recognising difference.
- **Distractors:** Pancasila described as a legal or technical instrument of one institution (006, options B–E); taking one side (001, options A and D); unity by erasing difference (017, statement 1); a function that praises the nation rather than answers the problem (022, statement 3).
- **Watch:** PPKN25-026 option B ("dialog sesama agama") is wrong only if "sesama" is read as intra-faith. Avoid wording whose correctness depends on one ambiguous word.
- **Examples:** PPKN25-001, 006, 017, 022, 026.

### PPK-ALASAN: Alasan atau arti penting suatu kegiatan atau kebijakan (level 2)

- **Asks:** why an activity or policy happens, or why it strengthens unity, social capital or NKRI.
- **Stem patterns:** "Bentuk kerja sama ini dilakukan karena ..." · "Pentingnya hal tersebut dalam menjaga keutuhan NKRI adalah ...." · "Alasan pelestarian Reog Ponorogo menjadi modal sosial pembangunan Indonesia adalah ...." · "Alasan kegiatan tersebut dapat memperkukuh persatuan dan kesatuan bangsa adalah ...."
- **Key:** the link between the activity and the goal named in the stem (persatuan, modal sosial, keutuhan NKRI), not a side benefit.
- **Distractors:** economic or tourism benefits (PPKN25-024, options A, B, E; 025, options A, C, D, E); a true description of one party's role that does not explain the cooperation (007, options B–E).
- **Watch:** keep "modal sosial" distinct from money. In PPKN25-024 option E (UNESCO recognition as "modal pembangunan") echoes the stimulus and competes with the key. In 009 options A and D both fit "demokrasi ekonomi".
- **Examples:** PPKN25-007, 009, 024, 025.

### PPK-TANTANGAN: Tantangan atau ancaman dalam kasus (level 2)

- **Asks:** the main challenge, obstacle or threat that the case shows.
- **Stem patterns:** "Berdasarkan ilustrasi tersebut, tantangan utama dalam penegakan hukum yang ditunjukkan adalah...." · "Tantangan yang dihadapi dalam mengimplementasikan pasal tersebut adalah ...." · "Berdasarkan ilustrasi, tantangan yang dihadapi dalam menjaga integrasi nasional dalam bingkai "Bhinneka Tunggal Ika" adalah ...."
- **Key:** the challenge that follows from the case's deciding detail: bribery from "uang pelican" (027), sukuisme from the number of suku bangsa (020), unequal access for the right to work (023).
- **Distractors:** a real problem the case does not show (027, option A); a condition that is actually the ideal (023, option C "merata dan setara"); a group that should not be involved at all (023, option E, pekerja anak); protection for the offender instead of the victim (027, option B).
- **Examples:** PPKN25-020, 023, 027.

### PPK-UPAYA: Upaya atau solusi yang paling tepat (level 3)

- **Asks:** the best effort or solution for a stated threat or violation, or which listed efforts are right.
- **Formats:** `pilihan-ganda`, `pilihan-ganda-kompleks`, `benar-salah`.
- **Stem patterns:** "Upaya terbaik untuk melindungi keutuhan NKRI dari dampak tersebut adalah..." · "Cara warga negara dalam mengatasi tantangan tersebut dapat dilakukan dengan ...." · "Berdasarkan ilustrasi, solusi untuk mengatasi pelanggaran tersebut yaitu ...." · "Klik Benar atau Salah dari setiap pernyataan berikut yang menunjukkan upaya menjaga integrasi nasional ...!"
- **Key:** the effort that answers every cause named in the case and involves both or all parties (005: correct information against hoaxes plus dialogue; 019: mediation so both sides understand their rights and obligations).
- **Distractors:** a reactive or one-sided measure (004, option C, surveillance and warnings); an effort that serves only one party (019, options A, B, D, E); an effort that hardens group lines (005, option C, groups of the same background); a risky compromise (004, option A, dialogue to find common ground with radical groups); a general development goal without the diversity element (028, options A and D).
- **Watch:** when two efforts both work, the case must say which cause matters most. PPKN25-012 asks how to face discrimination; option C (dialogue against prejudice) and E (mutual respect for equal dignity) both fit.
- **Examples:** PPKN25-004, 005, 012, 016, 019, 028.

## 4. Known weak spots in the 2025 paper

Avoid repeating these in generated items:

- Two missing items printed as "OTW" (numbers 8 and 21).
- An indicator that refers to "ideologi tersebut" with no antecedent (PPKN25-004).
- Options that are all true or all positive, so the key is a matter of emphasis (PPKN25-007, 022, 030).
- Unchecked numbers in the stimulus (PPKN25-020, 030).
- Typos in options and stems: "berpatisipasi" (013), "uang pelican" (027), "manakaah", "seseuai" (029).
