# TKA template: Geografi

Describes the TKA 2025 Geografi paper (pilihan, 30 items, numbers 1–30 complete on 49 pages) as 8 item types. Codes, levels and examples are in `data/tka-types.json`; level names are in `specs/tka-item-types.md`.

## 1. The paper at a glance

- **A figure for almost every item.** 26 of 30 items carry a map, satellite image, graph, photo or infographic; 4 carry a table (GEO25-006, 009, 017, 018). The figures are real and sourced: BMKG SPI and isoseismal maps, Ina-Geoportal, Google Earth, Sentinel-2, BPS tables, ANTARA and Mongabay infographics. Most items open with a title line ("Fenomena Alih Fungsi Lahan Banjarmasin") and a narrative; with the question, an item runs 27–220 words.
- **Shared figure.** The Kota Binjai spatial-plan map is used by GEO25-007 and 008.
- **Duplicate.** The Gunung Arjuno item (GEO25-012) is printed twice, on page 19 and again on pages 45–46 under item 28; it is recorded once.
- **Formats.** 13 `pilihan-ganda`, 5 `pilihan-ganda-kompleks`, 12 `benar-salah`. The two-column items use three pairs of headings: Benar / Salah (6), Sesuai / Tidak Sesuai (4: GEO25-007, 008, 012, 029), Fakta / Opini (2: GEO25-016, 020).
- **Content.** Each item names an *elemen* and *subelemen* (biogeography and natural resources, land-use change, population, spatial planning, disasters, maps and remote sensing). The item type is independent of the topic: GEO-RUANG uses a city plan, a forest map, a road network and contoured imagery.
- **Key confidence.** 14 proposed keys are `tinggi`, 12 `sedang`, 4 `rendah` (GEO25-009, 012, 025, 027). Several keys were read from small screenshots (GEO25-005, 007, 008).

| Type | Level | Items |
|---|---|---|
| GEO-CITRA | 1 | 5 |
| GEO-DATA | 2 | 5 |
| GEO-TEKNO | 2 | 2 |
| GEO-KONSEP | 2 | 4 |
| GEO-DAMPAK | 2 | 3 |
| GEO-FAKTA | 3 | 2 |
| GEO-RUANG | 3 | 5 |
| GEO-SOLUSI | 3 | 4 |

## 2. Rules for every Geografi item

- **The figure must carry the answer, and `gambar` must say so.** Write the decisive feature into the figure description (the class at the epicentre, the zone at point X, the land cover at A, B, C). GEO25-005's key (Papua selatan "Sangat Kering") and GEO25-008's (whether X lies in the trade corridor) depend on colours in a small screenshot.
- **Narrative, title and figure must name the same place and event.** GEO25-019's map and coordinates are the 2022 Tapanuli Utara earthquake, but the narrative describes Pasaman Barat with Talamau and Kinali. GEO25-023's title says Demak, its narrative Semarang. GEO25-024's text legend (merah/kuning/hijau) does not match the map's white–yellow–red–black scale.
- **Real data must be checked, cited with year, and add up.** GEO25-009's 2026 totals are printed 1995,3 and 3791,5, but the columns sum to 1955,3 and 3751,5; it also labels an age group "9-14". GEO25-010 gives 210.000 people but 105.300 + 104.600 = 209.900, and states the sex ratio as women per 100 men (99,34) where the convention is men per 100 women (100,67). GEO25-011 prints a 2025 total of 35,4 for 18,6 + 16,9 = 35,5. Generated items must not invent real statistics; use a clearly fictional region when inventing data (`specs/tka-generation.md`, section 2).
- **One claim per statement.** GEO25-012 statement 2 pairs a right action (drip irrigation at A) with a wrong reason ("guna penghematan energi"; drip irrigation saves water), and statement 3 says terracing "pada semua wilayah", which includes the forests at B and C.
- **In `pilihan-ganda-kompleks`, keep every option clearly in or out.** All five GEO25-027 statements on road feasibility are reasonable; GEO25-011 E (raising the retirement age), GEO25-025 C (coarse texture = dense vegetation) and GEO25-002 C are defensible but unkeyed. Do not combine "PALING TEPAT" with "Jawaban benar lebih dari satu" (GEO25-009).
- **Use Fakta / Opini only for real fact-versus-opinion pairs** (section 3, GEO-FAKTA).
- **The indicator box must match the item.** GEO25-012's indicator is about social research, its item about contoured imagery; GEO25-016's names "Gunung Apo" for a Marapi item; GEO25-030's elemen is a subelemen and its subelemen is "0".
- **Notation:** decimal commas, coordinates as in the paper (2,11° LU, 98,83° BT), magnitudes as "magnitudo 5,8", intensities in MMI. Indonesian textbook terms: *alih fungsi lahan*, *bonus demografi*, *rasio ketergantungan*, *mitigasi struktural/nonstruktural*, *unsur interpretasi citra* (rona, tekstur, pola, bentuk, bayangan), the ten *konsep dasar geografi*.

## 3. Item types

### GEO-CITRA: Membaca peta atau citra (level 1)

- **Asks:** read a map, satellite image or contoured image to identify a land cover, a change between two dates, a map class at a place, or an object by its interpretation elements.
- **Stimulus:** one figure (or two dates of the same area) with a legend, scale and, where used, labelled points A, B, C.
- **Stem patterns:** "Berdasarkan perbandingan citra satelit tahun 2007 dan 2024 ..., perubahan penggunaan lahan yang paling dominan adalah..." · "Berdasarkan peta SPI ..., manakah wilayah berikut yang kemungkinan besar mengalami risiko gagal panen akibat kekeringan ekstrem ...?" · "... bagaimana dampak yang kemungkinan terjadi ... di lokasi titik episenter?" · "Manakah pernyataan berikut yang menunjukkan interpretasi citra yang sesuai ...?"
- **Key:** what the figure shows at the named place, plus at most one fact the student must know (MMI VI = light damage, GEO25-019).
- **Distractors:** a neighbouring map class (GEO25-019 D, intensity VII–VIII damage for a VI zone); a change in the wrong direction ("Permukiman menjadi kawasan pertanian organik", GEO25-003 E); a look-alike object (C as forest when it is water, GEO25-029 statement 2; square dark plots as rice fields when they are fishponds, GEO25-025 D).
- **Watch:** labels must be legible at the size the student sees; GEO25-029's point D is drawn but never used.
- **Examples:** GEO25-003, 005, 019, 025, 029.

### GEO-DATA: Simpulan dari teks, tabel, grafik, atau infografis (level 2)

- **Asks:** the conclusion, reason or direct benefit that a text, table, population pyramid or infographic supports.
- **Stimulus:** a narrative with numbers, a table of indicators for two places or five destinations, a pyramid, or an infographic.
- **Stem patterns:** "... manakah dari pernyataan berikut yang merupakan manfaat atau implikasi langsung dari pembangunan pembangkit tersebut?" · "Berdasarkan data dalam tabel, mengapa pengembangan destinasi wisata super prioritas di wilayah seperti Labuan Bajo dan Likupang berpotensi menarik wisatawan internasional?" · "Berdasarkan struktur penduduk tersebut, simpulan yang tepat untuk menggambarkan kondisi demografi wilayah tersebut adalah?" · "... tentukan simpulan yang paling tepat dan logis dari pernyataan berikut!"
- **Key:** a statement every part of which the data support, including the exception (GEO25-018 B: Makassar ahead on four indicators "meskipun menghadapi tantangan lapangan kerja").
- **Distractors:** a conclusion from one indicator only (GEO25-018 A, Medan better because of lower unemployment); a reversed comparison (GEO25-018 D); a claim with a number or sector not in the stimulus (GEO25-002 A); a conclusion the data cannot show (migration from a pyramid, GEO25-010 E).
- **Examples:** GEO25-002, 006, 010, 018, 026.

### GEO-TEKNO: Kegunaan teknologi geospasial dan citra (level 2)

- **Asks:** what a geospatial tool (Windy.com) is for, or which thematic maps can be extracted from a given satellite image.
- **Stimulus:** a screenshot or image with a description of the data source (forecast models and satellites; Sentinel-2 natural colour).
- **Stem patterns:** "Aplikasi tersebut dapat berperan untuk ... ." · "... informasi spasial esensial apa yang dapat diekstraksi dan divisualisasikan menjadi peta tematik yang paling tepat dari pengolahan citra satelit ...?"
- **Key:** what the sensor or tool actually records (spatial and temporal atmospheric data; land cover, turbidity, shoreline).
- **Distractors:** information the image cannot show (population density, animal migration, sub-sea minerals, GEO25-023 A, B, D); a function of a different tool (historical disaster database, new instruments, GEO25-022 A, C).
- **Examples:** GEO25-022, 023.

### GEO-KONSEP: Menerapkan konsep geografi (level 2)

- **Asks:** apply one concept to cases: biogeographic regions to local flora, conservation vs restoration to listed actions, a *konsep dasar geografi* to a recurring event, plate boundaries to earthquake and tsunami risk.
- **Stimulus:** a map (Wallace–Weber lines, plate boundaries) or a case narrative.
- **Stem patterns:** "Tentukan penyataan Benar dan Salah mengenai pengelolaan flora lokal berikut!" · "Konsep geografi yang tepat untuk menjelaskan keteraturan terjadinya bencana tersebut adalah..." · "... manakah pernyataan yang benar dan salah berdasarkan analisis subduksi lempeng yang terjadi di Indonesia?"
- **Key:** the case placed by the concept's defining feature (recurrence = *pola*; matoa belongs east of the Weber line, not in Bangka).
- **Distractors:** another *konsep dasar* that sounds close (*diferensiasi area*, *interaksi*, *aglomerasi*, GEO25-015); a location on the wrong side of a boundary (Kalimantan "dekat dari batas lempeng aktif", GEO25-021 statement 3); an action given the wrong category (audit lingkungan "tidak berkaitan dengan konservasi", GEO25-013 statement 2).
- **Examples:** GEO25-001, 013, 015, 021.

### GEO-DAMPAK: Sebab dan dampak fenomena geosfer (level 2)

- **Asks:** the cause or environmental and social effect of land-use change, air pollution or deforestation shown in imagery.
- **Stimulus:** two-date imagery or a pollution map with a narrative.
- **Stem patterns:** "... konsep alih fungsi lahan dapat diterapkan untuk menjelaskan bahwa ... ." · "... pilih benar atau salah pernyataan dampak lingkungan dan sosial yang dapat terjadi di wilayah yang menunjukkan konsentrasi tinggi!" · "Bagaimana dampak fenomena tersebut terhadap lingkungannya?"
- **Key:** the direct, textbook mechanism (more buildings on vegetated land = population pressure; NO₂ → acid rain; primary-forest loss → carbon emissions).
- **Distractors:** an absolute claim ("kekeringan total", "tidak berdampak", "hanya terjadi pada daerah pegunungan"); a reversed effect (oil palm cools the ground, GEO25-030 B); a human change called natural (GEO25-004 A).
- **Watch:** GEO25-030 E (primary forest cannot recover quickly) is also true; only one option may be ecologically correct.
- **Examples:** GEO25-004, 024, 030.

### GEO-FAKTA: Membedakan fakta dan opini (level 3)

- **Asks:** label three statements about a volcano's soils or an earthquake Fakta or Opini.
- **Stimulus:** a photo or isoseismal map with a narrative.
- **Stem patterns:** "Pilih Fakta atau Opini tetang pernyataan yang berhubungan antara aktivitas Gunung Marapi dan kondisi lahan pertanian subur di sekitarnya !" · "Merujuk pada narasi dan data Gempa Sigi, tentukan Fakta atau Opini yang sesuai dari pernyataan berikut!"
- **Key, as the paper sets it:** Fakta = a statement in the data or established science; Opini = an overgeneralisation ("sepenuhnya bergantung", "hanya berdampak jika ... di atas 6,0").
- **Watch:** this mixes two questions. A false generalisation is not an opinion, and a scientific statement not in the stimulus (GEO25-020 statement 2) may be read as Opini. For new items, make each Opini a judgement or preference ("sebaiknya", "paling indah", "seharusnya"), make each Fakta checkable in the stimulus, and use Benar / Salah instead when the point is scientific accuracy.
- **Examples:** GEO25-016, 020.

### GEO-RUANG: Kesesuaian rencana ruang dengan peta (level 3)

- **Asks:** judge whether a planned use, development direction or infrastructure fits a location, using a spatial-plan map, forest-status map, road network or contoured imagery.
- **Stimulus:** a map with a legend of zones or forest classes, or imagery with contours and labelled points.
- **Stem patterns:** "Manakah pernyataan berikut yang menunjukkan arah perkembangan kota di Kota Binjai berdasarkan Peta Tata Ruang Wilayah tersebut?" · "Seorang pengusaha akan membangun sebuah bisnis properti komersial pada lokasi X, jenis usaha yang sesuai ... adalah..." · "Pilih pernyataan yang paling tepat yang menunjukkan kelayakan pembangunan jalan nasional berdasarkan pertimbangan spasial dan keberlanjutan!" · "... pilih benar atau salah infrastruktur pendukung yang paling tepat direncanakan ..."
- **Key:** follows from the zone at the place plus one planning rule (open-pit mining is not allowed in *hutan lindung*; roads follow contours to limit erosion; an R1 zone suits apartments).
- **Distractors:** a use that belongs to another zone (a mall outside the trade corridor, GEO25-008); an activity forbidden in the zone (GEO25-028 statement 2); a direction the plan does not support (south, a low-density R3 zone, GEO25-007 statement 1).
- **Watch:** this is where the paper's keys are weakest (GEO25-012 and 027 `rendah`). Give the zone at each named place in the stem or the figure description, and phrase each statement so one rule decides it.
- **Examples:** GEO25-007, 008, 012, 027, 028.

### GEO-SOLUSI: Upaya atau kebijakan untuk masalah wilayah (level 3)

- **Asks:** the best strategy for a population structure, ageing, peat fires, or earthquake risk, given its stated constraint (balance economy and conservation; a *structural* adaptation).
- **Stimulus:** a projection table, an infographic, a case narrative or a ShakeMap.
- **Stem patterns:** "Berdasarkan proyeksi penduduk tahun 2025, strategi pembangunan yang PALING TEPAT untuk 10 tahun mendatang adalah ... ." · "Apa saja upaya yang dapat dilakukan pemerintah untuk mengurangi dampak negatif dari penuaan penduduk di masa depan?" · "... bagaimana langkah yang tepat untuk menjaga keseimbangan antara pemanfaatan ekonomi dan pelestarian lahan gambut ...?" · "... salah satu bentuk adaptasi struktural yang paling tepat dilakukan untuk mengurangi risiko korban jiwa dan kerusakan adalah...."
- **Key:** meets the problem and the named constraint (GEO25-014 D: peat-friendly farming and non-timber forest products; GEO25-017 C: settlements planned with a microzonation map).
- **Distractors:** an extreme measure (a total ban on peatland activity, GEO25-014 B; postponing all building until the fault is inactive, GEO25-017 E); a measure of the wrong kind (evacuation drills are nonstructural, GEO25-017 B); one that ignores the data (transmigration out of Papua, GEO25-009 C; subsidies for every age group, GEO25-009 D); a physically wrong one (heavy concrete foundations, GEO25-017 A).
- **Watch:** check data claims behind the key. GEO25-009's table gives a young population (0–24 about 44% and 15–64 about 70% of the 2025 total, checked in Python); the key must follow from that, and "PALING TEPAT" must not sit on a multi-answer item.
- **Examples:** GEO25-009, 011, 014, 017.

## 4. Known weak spots in the 2025 paper

- **Four `rendah` keys** (GEO25-009, 012, 025, 027) and the colour-read keys (GEO25-005, 007, 008) need checking against the official key and the original figures before use as reference answers.
- **GEO25-019** has a scale bar of "0 350 700 1.400 2.100 2.800 Kilometers" on a map about 1,5° across, besides the place mismatch in section 2.
- **Typos in the source** ("Pillih", "entukan", "siginifikan", "Kapas" for Kapuas) are kept in the bank; generated items should not copy them.
