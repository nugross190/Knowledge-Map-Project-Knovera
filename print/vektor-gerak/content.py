"""Content of the printable module "Vektor dan Gerak". Every numeric answer is asserted in check()."""
import math

def fr(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'

V = lambda s: f"<b>{s}</b>"      # vector symbol
i, j = V("i"), V("j")

# level: 1 Mudah, 2 Sedang, 3 Sulit
# item: (level, question_html, answer_short_html, explanation_html)

PRASYARAT = [
    ("P1", "Hitunglah √(6² + 8²) dan √(5² + 12²).", "10 dan 13", "√(36 + 64) = √100 = 10; √(25 + 144) = √169 = 13."),
    ("P2", "Tuliskan nilai sin 30°, cos 30°, sin 60°, dan cos 60°.", "½; ½√3; ½√3; ½", "sin 30° = cos 60° = ½ dan cos 30° = sin 60° = ½√3 ≈ 0,87."),
    ("P3", "Dengan sin 37° = 0,6 dan cos 37° = 0,8, hitunglah 20 sin 37° dan 20 cos 37°.", "12 dan 16", "20 × 0,6 = 12; 20 × 0,8 = 16."),
    ("P4", "Jika tan θ = 3/4, berapakah θ? (Petunjuk: segitiga 3-4-5.)", "θ ≈ 37°", "Sisi depan 3, sisi samping 4, sisi miring 5: sin θ = 0,6, jadi θ ≈ 37°."),
    ("P5", "Ubah 72 km/jam ke m/s.", "20 m/s", "72 × 1.000 m ÷ 3.600 s = 20 m/s (cara cepat: bagi 3,6)."),
    ("P6", "Ubah 15 menit dan 40 menit ke jam.", "0,25 jam dan ⅔ jam", "15/60 = 0,25 jam; 40/60 = ⅔ jam."),
    ("P7", "Hitunglah (−3) − 5 dan (−8) − (+10).", "−8 dan −18", "Mengurangkan bilangan positif menggeser ke kiri pada garis bilangan."),
    ("P8", "Tentukan t jika 20 = 5t².", "t = 2 (t positif)", "t² = 4, jadi t = 2."),
]

INGAT = [
    ("A", "Teorema Pythagoras", "P1, P4", "Subbab 1–3",
     ["Pada segitiga siku-siku: c² = a² + b², c sisi miring.",
      "Tripel yang sering muncul: 3-4-5, 6-8-10, 5-12-13, 7-24-25, 8-15-17."]),
    ("B", "Trigonometri sudut istimewa", "P2–P4", "Subbab 1, 2, 4, 5",
     ["sin θ = depan/miring, cos θ = samping/miring, tan θ = depan/samping.",
      "Sudut 37° dan 53° berasal dari segitiga 3-4-5: sin 37° = cos 53° ≈ 0,6 dan cos 37° = sin 53° ≈ 0,8. Nilai sebenarnya 36,87° dan 53,13°; soal selalu menuliskan nilai yang dipakai."]),
    ("C", "Konversi satuan waktu dan kecepatan", "P5–P6", "Subbab 3 dan 5",
     ["1 km/jam = 1.000 m / 3.600 s, jadi km/jam ÷ 3,6 = m/s dan m/s × 3,6 = km/jam.",
      "Menit ke jam: bagi 60. 30 menit = 0,5 jam; 20 menit = ⅓ jam."]),
    ("D", "Bilangan bertanda dan persamaan kuadrat sederhana", "P7–P8", "Subbab 3 dan 4",
     ["Pada gerak lurus, tanda + dan − menyatakan arah. Selisih = akhir − awal.",
      "ax² = c → x = √(c/a); dalam soal waktu, ambil akar yang positif."]),
]

SUB = []

# ------------------------------------------------------------------ Subbab 1
SUB.append(dict(
    title="Besaran Skalar dan Vektor",
    tujuan="Membedakan besaran skalar dan vektor, lalu menyatakan vektor dengan komponen, besar, dan arahnya.",
    konsep=[
        "<b>Besaran skalar</b> cukup dinyatakan dengan nilai dan satuan: massa 2 kg, waktu 5 s, jarak 100 m. <b>Besaran vektor</b> memerlukan nilai, satuan, <b>dan arah</b>: perpindahan 100 m ke timur, kecepatan 20 m/s ke utara.",
        f"Vektor ditulis tebal ({V('A')}) atau dengan panah di atas huruf. Besarnya ditulis |{V('A')}| atau A dan tidak pernah negatif. Vektor −{V('A')} sama besar dengan {V('A')} tetapi arahnya berlawanan.",
        f"Pada bidang, vektor diuraikan menjadi komponen pada sumbu x dan sumbu y. Dengan vektor satuan {i} (sumbu x) dan {j} (sumbu y): {V('A')} = A<sub>x</sub>{i} + A<sub>y</sub>{j}. Dalam modul ini sumbu x positif = <b>timur</b> dan sumbu y positif = <b>utara</b>.",
    ],
    rumus=[
        "Komponen: A<sub>x</sub> = A cos θ dan A<sub>y</sub> = A sin θ (θ diukur dari sumbu x positif)",
        "Besar: |" + V("A") + "| = √(A<sub>x</sub>² + A<sub>y</sub>²)",
        "Arah: tan θ = " + fr("A<sub>y</sub>", "A<sub>x</sub>") + " (perhatikan tanda komponen untuk menentukan kuadran)",
    ],
    contoh=[
        ("Besar dan arah dari komponen", f"Tentukan besar dan arah vektor {V('A')} = (6{i} + 8{j}) m.",
         ["|" + V("A") + "| = √(6² + 8²) = √100 = 10 m.", "tan θ = 8/6 = 4/3, sehingga θ ≈ 53° dari sumbu x positif (dari timur ke utara)."],
         "10 m, arah 53° dari timur ke utara"),
        ("Menguraikan kecepatan", "Bola ditendang dengan kecepatan 20 m/s membentuk sudut 37° di atas tanah (sin 37° = 0,6; cos 37° = 0,8). Tentukan komponen kecepatannya.",
         ["v<sub>x</sub> = 20 cos 37° = 20 × 0,8 = 16 m/s (mendatar).", "v<sub>y</sub> = 20 sin 37° = 20 × 0,6 = 12 m/s (tegak).", "Cek: √(16² + 12²) = √400 = 20 m/s."],
         "v<sub>x</sub> = 16 m/s, v<sub>y</sub> = 12 m/s"),
    ],
    bertahap=dict(
        soal=f"Tentukan besar dan letak vektor {V('B')} = (−5{i} + 12{j}) m.",
        langkah=["|" + V("B") + "| = √((−5)² + 12²) = √(____ + 144) = ____ m.",
                 "Komponen x bernilai ____ dan komponen y bernilai ____, jadi vektor berada di kuadran ____.",
                 "Arah: 12/5 = tan α, dengan α diukur dari sumbu x ____ (negatif/positif) menuju sumbu y positif."],
        cek="Mengapa besar vektor bernilai positif walaupun komponen x-nya negatif?",
        opsi=["(a) komponen dikuadratkan, sehingga tandanya hilang", "(b) tanda negatif dibuang saja karena tidak penting"],
        kunci="25; 13 m. Negatif dan positif; kuadran II. Sumbu x negatif (α ≈ 67°, jadi 113° dari sumbu x positif). Alasan: (a).",
    ),
    jebakan=[
        "Komponen yang <b>bersebelahan</b> dengan sudut memakai cos, yang <b>berhadapan</b> memakai sin. Jika sudut diukur dari sumbu y, peran sin dan cos bertukar.",
        "Besar vektor tidak pernah negatif. Tanda negatif hanya ada pada komponen dan menyatakan arah.",
        "37° dan 53° mudah tertukar. Periksa: komponen yang lebih besar (0,8) selalu berada pada sumbu yang lebih dekat dengan arah vektor.",
    ],
    latihan=[
        (1, "Dari besaran berikut, pilih yang merupakan vektor: massa, perpindahan, waktu, kecepatan, kelajuan, gaya.", "perpindahan, kecepatan, gaya", "Ketiganya memerlukan arah. Kelajuan adalah besar kecepatan tanpa arah, jadi skalar."),
        (1, f"Tentukan besar vektor {V('A')} = (3{i} + 4{j}) m.", "5 m", "√(9 + 16) = √25 = 5 m."),
        (1, f"Tentukan besar vektor {V('B')} = (−8{i} + 6{j}) m/s.", "10 m/s", "√(64 + 36) = √100 = 10 m/s. Tanda negatif hilang saat dikuadratkan."),
        (1, "Kecepatan 10 m/s berarah 60° terhadap sumbu x positif. Tentukan komponen x-nya (cos 60° = 0,5).", "5 m/s", "v<sub>x</sub> = 10 × 0,5 = 5 m/s."),
        (1, "Perpindahan 50 m berarah 37° di atas sumbu x positif (sin 37° = 0,6; cos 37° = 0,8). Tentukan komponen x dan y.", "40 m dan 30 m", "50 × 0,8 = 40 m; 50 × 0,6 = 30 m."),
        (2, f"Vektor kecepatan {V('v')} = (12{i} − 5{j}) m/s. Tentukan besarnya dan kuadran arahnya.", "13 m/s; kuadran IV", "√(144 + 25) = 13 m/s. x positif dan y negatif, jadi kuadran IV (ke timur dan sedikit ke selatan)."),
        (2, "Pesawat terbang 200 km/jam ke arah 30° dari timur ke utara. Tentukan komponen kecepatan ke timur dan ke utara (cos 30° ≈ 0,87).", "≈ 173 km/jam ke timur; 100 km/jam ke utara", "Timur: 200 cos 30° = 100√3 ≈ 173 km/jam. Utara: 200 sin 30° = 100 km/jam."),
        (2, f"Diketahui {V('A')} = (4{i} − 3{j}) m. Tuliskan vektor −{V('A')} dan tentukan besarnya.", f"−{V('A')} = (−4{i} + 3{j}) m; 5 m", "Semua komponen berganti tanda; besarnya tetap √(16 + 9) = 5 m."),
        (2, "Vektor C besarnya 25 m. Komponen x-nya 20 m dan komponen y-nya positif. Tentukan komponen y dan sudutnya terhadap sumbu x.", "15 m; 37°", "C<sub>y</sub> = √(25² − 20²) = 15 m. tan θ = 15/20 = 0,75, jadi θ ≈ 37°."),
        (3, "Bola ditendang dengan kelajuan 25 m/s. Komponen tegak kecepatannya 15 m/s. Tentukan komponen mendatar dan sudut tendangannya.", "20 m/s; 37°", "v<sub>x</sub> = √(625 − 225) = 20 m/s. sin θ = 15/25 = 0,6, jadi θ ≈ 37°."),
        (3, f"Vektor {V('A')} = (2p{i} + 6{j}) m besarnya 10 m. Tentukan p (p &gt; 0).", "p = 4", "(2p)² + 36 = 100 → 4p² = 64 → p² = 16 → p = 4."),
        (3, "Kecepatan sebuah drone (v<sub>x</sub>, v<sub>y</sub>) = (−6, −8) m/s, dengan x ke timur dan y ke utara. Tentukan kelajuannya dan nyatakan arahnya dengan arah mata angin.", "10 m/s; 53° dari barat ke selatan (barat daya)", "√(36 + 64) = 10 m/s. Kedua komponen negatif: ke barat dan ke selatan. tan α = 8/6 dari arah barat, α ≈ 53°."),
    ],
))

# ------------------------------------------------------------------ Subbab 2
SUB.append(dict(
    title="Penjumlahan dan Selisih Vektor",
    tujuan="Menjumlahkan dan mengurangkan vektor dengan cara grafis, rumus cosinus, dan cara komponen.",
    konsep=[
        "<b>Cara ujung–pangkal (poligon):</b> letakkan pangkal vektor kedua di ujung vektor pertama. Resultan ditarik dari pangkal vektor pertama ke ujung vektor terakhir. Urutan penjumlahan tidak mengubah hasil.",
        "<b>Rumus cosinus</b> dipakai untuk dua vektor yang sudut apitnya θ (sudut di antara keduanya saat pangkalnya disatukan).",
        "<b>Cara komponen</b> paling andal untuk tiga vektor atau lebih: uraikan setiap vektor, jumlahkan per sumbu, lalu cari besar dan arah resultannya.",
    ],
    rumus=[
        "R = √(A² + B² + 2AB cos θ)",
        "|" + V("A") + " − " + V("B") + "| = √(A² + B² − 2AB cos θ)",
        "R<sub>x</sub> = ΣA<sub>x</sub>, R<sub>y</sub> = ΣA<sub>y</sub>, R = √(R<sub>x</sub>² + R<sub>y</sub>²)",
        "Searah: R = A + B (terbesar). Berlawanan: R = |A − B| (terkecil). Tegak lurus: R = √(A² + B²)",
    ],
    contoh=[
        ("Rumus cosinus", "Dua kecepatan, 3 m/s dan 5 m/s, membentuk sudut apit 60°. Tentukan besar resultannya.",
         ["R = √(3² + 5² + 2 · 3 · 5 · cos 60°).", "R = √(9 + 25 + 15) = √49 = 7 m/s."], "7 m/s"),
        ("Cara komponen", "Perpindahan A = 10 m berarah 53° dari timur ke utara, lalu B = 6 m ke barat (sin 53° = 0,8; cos 53° = 0,6). Tentukan resultannya.",
         ["A: A<sub>x</sub> = 10 × 0,6 = 6 m, A<sub>y</sub> = 10 × 0,8 = 8 m. B: B<sub>x</sub> = −6 m, B<sub>y</sub> = 0.",
          "R<sub>x</sub> = 6 − 6 = 0; R<sub>y</sub> = 8 m.", "Resultan 8 m tepat ke utara."], "8 m ke utara"),
    ],
    bertahap=dict(
        soal="Seorang pejalan kaki bergerak 9 km ke timur, 5 km ke utara, 3 km ke barat, lalu 3 km ke utara. Tentukan besar perpindahannya.",
        langkah=["R<sub>x</sub> = 9 − 3 = ____ km.", "R<sub>y</sub> = 5 + 3 = ____ km.", "R = √(____² + ____²) = ____ km."],
        cek="Langkah pertama yang benar adalah",
        opsi=["(a) menjumlahkan komponen pada setiap sumbu", "(b) menjumlahkan semua panjang lintasan: 9 + 5 + 3 + 3"],
        kunci="R<sub>x</sub> = 6 km; R<sub>y</sub> = 8 km; R = √(36 + 64) = 10 km. Alasan: (a).",
    ),
    jebakan=[
        "Vektor 3 dan 4 tidak selalu menghasilkan 5. Itu hanya bila keduanya tegak lurus; resultannya bisa berapa saja dari 1 sampai 7.",
        "θ pada rumus cosinus adalah sudut <b>apit</b> kedua vektor, bukan sudut masing-masing terhadap sumbu x.",
        "Selisih vektor memakai tanda minus di depan 2AB cos θ. Untuk vektor sama besar bersudut 60°, selisihnya sama dengan besar masing-masing.",
    ],
    latihan=[
        (1, "Dua kecepatan 6 m/s dan 8 m/s <b>searah</b>. Berapa resultannya?", "14 m/s", "Searah: dijumlahkan langsung."),
        (1, "Dua kecepatan 6 m/s dan 8 m/s <b>berlawanan arah</b>. Berapa resultannya?", "2 m/s, searah vektor 8 m/s", "Berlawanan: 8 − 6 = 2 m/s."),
        (1, "Dua kecepatan 6 m/s dan 8 m/s <b>saling tegak lurus</b>. Berapa resultannya?", "10 m/s", "√(36 + 64) = 10 m/s."),
        (1, f"Diketahui {V('A')} = (2{i} + 3{j}) dan {V('B')} = (4{i} − 7{j}). Tentukan {V('A')} + {V('B')}.", f"(6{i} − 4{j})", "Jumlahkan per komponen: 2 + 4 = 6 dan 3 + (−7) = −4."),
        (1, f"Dengan {V('A')} dan {V('B')} pada soal sebelumnya, tentukan {V('A')} − {V('B')}.", f"(−2{i} + 10{j})", "2 − 4 = −2 dan 3 − (−7) = 10."),
        (2, "Dua vektor 5 satuan dan 8 satuan membentuk sudut apit 120° (cos 120° = −0,5). Tentukan besar resultannya.", "7 satuan", "R = √(25 + 64 + 2 · 5 · 8 · (−0,5)) = √(89 − 40) = √49 = 7."),
        (2, "Dua vektor masing-masing 6 satuan membentuk sudut apit 120°. Tentukan resultannya.", "6 satuan", "R = √(36 + 36 − 36) = 6. Dua vektor sama besar bersudut 120° menghasilkan resultan sebesar masing-masing."),
        (2, "Dua vektor masing-masing 10 satuan membentuk sudut apit 60°. Tentukan besar <b>selisih</b>nya.", "10 satuan", "|A − B| = √(100 + 100 − 2 · 100 · 0,5) = √100 = 10."),
        (2, "Perpindahan: 10 m berarah 37° dari timur ke utara, lalu 4 m ke timur, lalu 1 m ke selatan (sin 37° = 0,6; cos 37° = 0,8). Tentukan besar resultannya.", "13 m", "R<sub>x</sub> = 8 + 4 = 12 m; R<sub>y</sub> = 6 − 1 = 5 m; R = √(144 + 25) = 13 m."),
        (3, "Dua vektor sama besar, F, menghasilkan resultan yang juga sebesar F. Berapa sudut apit kedua vektor?", "120°", "F² = F² + F² + 2F² cos θ → cos θ = −½ → θ = 120°."),
        (3, "Vektor 5 satuan dan 3 satuan menghasilkan resultan 7 satuan. Tentukan sudut apitnya.", "60°", "49 = 25 + 9 + 30 cos θ → cos θ = 15/30 = 0,5 → θ = 60°."),
        (3, "Jika dua vektor A dan B searah, resultannya 17 satuan. Jika saling tegak lurus, resultannya 13 satuan. Tentukan A dan B.", "12 dan 5 satuan", "A + B = 17 dan A² + B² = 169. (A + B)² = 289 → 2AB = 120 → AB = 60. Bilangan yang jumlahnya 17 dan hasil kalinya 60: 12 dan 5."),
    ],
))

# ------------------------------------------------------------------ Subbab 3
SUB.append(dict(
    title="Jarak, Perpindahan, Kelajuan, dan Kecepatan",
    tujuan="Membedakan jarak dan perpindahan serta kelajuan dan kecepatan, lalu menghitungnya untuk gerak satu dan dua dimensi.",
    konsep=[
        f"<b>Posisi</b> adalah vektor dari titik acuan: {V('r')} = x{i} + y{j}. <b>Perpindahan</b> Δ{V('r')} adalah perubahan posisi, hanya ditentukan oleh posisi awal dan akhir. <b>Jarak</b> adalah panjang seluruh lintasan.",
        "<b>Kelajuan rata-rata</b> = jarak ÷ waktu (skalar). <b>Kecepatan rata-rata</b> = perpindahan ÷ waktu (vektor, searah perpindahan).",
        "Kecepatan <b>sesaat</b> adalah kecepatan pada satu saat. Besarnya sama dengan kelajuan sesaat (yang dibaca spidometer), dan arahnya menyinggung lintasan.",
    ],
    rumus=[
        "Δ" + V("r") + " = " + V("r") + "<sub>akhir</sub> − " + V("r") + "<sub>awal</sub>",
        V("v") + "<sub>rata-rata</sub> = " + fr("Δ" + V("r"), "Δt") + "; kelajuan rata-rata = " + fr("jarak", "Δt"),
        "Kelajuan dari komponen: |" + V("v") + "| = √(v<sub>x</sub>² + v<sub>y</sub>²)",
        "Selalu berlaku: |Δ" + V("r") + "| ≤ jarak, sehingga besar kecepatan rata-rata ≤ kelajuan rata-rata",
    ],
    contoh=[
        ("Jarak dan perpindahan", "Sebuah sepeda bergerak 8 km ke timur, 9 km ke utara, lalu 3 km ke selatan. Tentukan jarak dan besar perpindahannya.",
         ["Jarak = 8 + 9 + 3 = 20 km.", "Komponen: timur 8 km; utara 9 − 3 = 6 km.", "Perpindahan = √(8² + 6²) = 10 km."], "Jarak 20 km; perpindahan 10 km"),
        ("Kelajuan dan kecepatan rata-rata", "Seorang siswa berjalan 30 m ke timur lalu 40 m ke utara dalam 50 s. Tentukan kelajuan rata-rata dan kecepatan rata-ratanya.",
         ["Kelajuan rata-rata = (30 + 40) ÷ 50 = 1,4 m/s.", "Perpindahan = √(30² + 40²) = 50 m, jadi besar kecepatan rata-rata = 50 ÷ 50 = 1 m/s.", "Arah: tan θ = 40/30 → θ ≈ 53° dari timur ke utara."],
         "1,4 m/s; 1 m/s arah 53° dari timur ke utara"),
    ],
    bertahap=dict(
        soal=f"Posisi sebuah bola pada t = 0 adalah {V('r')} = (2{i} + 3{j}) m dan pada t = 4 s adalah {V('r')} = (14{i} + 19{j}) m. Tentukan besar kecepatan rata-ratanya.",
        langkah=["Δ" + V("r") + " = (14 − 2)" + i + " + (19 − 3)" + j + " = (____" + i + " + ____" + j + ") m.",
                 V("v") + "<sub>rata-rata</sub> = Δ" + V("r") + " ÷ 4 = (____" + i + " + ____" + j + ") m/s.",
                 "|" + V("v") + "| = √(____² + ____²) = ____ m/s."],
        cek="Perpindahan dihitung dengan",
        opsi=["(a) posisi akhir dikurangi posisi awal", "(b) posisi awal ditambah posisi akhir"],
        kunci="Δ" + V("r") + " = (12" + i + " + 16" + j + ") m; " + V("v") + " = (3" + i + " + 4" + j + ") m/s; |" + V("v") + "| = 5 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Kelajuan rata-rata bukan besar kecepatan rata-rata. Pada lintasan tertutup (kembali ke titik awal), kecepatan rata-rata nol tetapi kelajuan rata-ratanya tidak.",
        "Kecepatan rata-rata pergi–pulang bukan rata-rata dua kecepatan. Hitung dari perpindahan total dan waktu total.",
        "Waktu berhenti tetap termasuk dalam waktu total.",
    ],
    latihan=[
        (1, "Andi berjalan 4 m ke timur, lalu berbalik 3 m ke barat. Tentukan jarak dan perpindahannya.", "Jarak 7 m; perpindahan 1 m ke timur", "Dengan timur positif: +4 + (−3) = +1 m."),
        (1, "Pelari mengelilingi tepi lapangan persegi bersisi 100 m tepat satu kali dalam 80 s. Tentukan kelajuan rata-rata dan kecepatan rata-ratanya.", "5 m/s; 0 m/s", "Jarak 400 m → 400/80 = 5 m/s. Kembali ke titik awal → perpindahan 0, kecepatan rata-rata 0."),
        (1, "Mobil melaju lurus ke utara sejauh 90 km dalam 1,5 jam. Tentukan kecepatan rata-ratanya.", "60 km/jam ke utara", "90 ÷ 1,5 = 60 km/jam; arah ikut perpindahan."),
        (1, f"Robot berpindah dari {V('r')}<sub>1</sub> = (2{i} + {j}) m ke {V('r')}<sub>2</sub> = (8{i} + 9{j}) m. Tentukan vektor dan besar perpindahannya.", f"(6{i} + 8{j}) m; 10 m", "Δr = (8 − 2, 9 − 1) = (6, 8); √(36 + 64) = 10 m."),
        (1, f"Kecepatan sesaat sebuah benda {V('v')} = (3{i} + 4{j}) m/s. Berapa kelajuannya?", "5 m/s", "√(9 + 16) = 5 m/s."),
        (2, "Drone terbang 600 m ke timur, lalu 800 m ke utara, dalam 200 s. Tentukan kelajuan rata-rata dan besar kecepatan rata-ratanya.", "7 m/s; 5 m/s", "Jarak 1.400 m → 7 m/s. Perpindahan √(600² + 800²) = 1.000 m → 5 m/s."),
        (2, "Pendaki berjalan 12 km ke timur, 20 km ke utara, lalu 4 km ke selatan. Tentukan jarak dan besar perpindahannya.", "Jarak 36 km; perpindahan 20 km", "Utara bersih 20 − 4 = 16 km; √(12² + 16²) = 20 km."),
        (2, "Bus berangkat pukul 08.00, menempuh 30 km ke timur lalu 40 km ke utara, dan tiba pukul 09.15. Tentukan kelajuan rata-rata dan besar kecepatan rata-ratanya.", "56 km/jam; 40 km/jam", "Waktu 1,25 jam. 70 ÷ 1,25 = 56 km/jam; 50 ÷ 1,25 = 40 km/jam."),
        (2, "Pelari menempuh setengah lingkaran berjari-jari 14 m dalam 11 s (π = 22/7). Tentukan kelajuan rata-rata dan besar kecepatan rata-ratanya.", "4 m/s; ≈ 2,55 m/s", "Jarak = πr = 44 m → 4 m/s. Perpindahan = diameter 28 m → 28/11 ≈ 2,55 m/s."),
        (3, "Pengemudi ojek bergerak 6 km ke timur selama 15 menit, 8 km ke utara selama 15 menit, lalu berhenti 10 menit. Tentukan kelajuan rata-rata dan besar kecepatan rata-rata selama 40 menit itu.", "21 km/jam; 15 km/jam", "Waktu ⅔ jam. Jarak 14 km → 14 ÷ ⅔ = 21 km/jam. Perpindahan 10 km → 15 km/jam."),
        (3, "Mobil melaju ke timur 40 km/jam selama 1,5 jam, lalu ke utara 80 km/jam selama 1 jam. Tentukan besar kecepatan rata-ratanya. Apakah sama dengan (40 + 80)/2?", "40 km/jam; tidak sama dengan 60 km/jam", "Perpindahan √(60² + 80²) = 100 km dalam 2,5 jam → 40 km/jam. Rata-rata dua kecepatan tidak bermakna di sini."),
        (3, "Mobil pergi dari A ke B sejauh 120 km dengan 60 km/jam dan pulang dengan 40 km/jam. Tentukan kelajuan rata-rata dan kecepatan rata-rata pergi–pulang.", "48 km/jam; 0", "Waktu 2 + 3 = 5 jam, jarak 240 km → 48 km/jam (bukan 50). Kembali ke A → kecepatan rata-rata 0."),
    ],
))

# ------------------------------------------------------------------ Subbab 4
SUB.append(dict(
    title="Percepatan dan Gerak Dua Dimensi",
    tujuan="Menghitung percepatan sebagai vektor dan menganalisis gerak dua dimensi (gerak parabola) per komponen.",
    konsep=[
        "<b>Percepatan</b> adalah perubahan kecepatan tiap satuan waktu. Δ" + V("v") + " dihitung secara vektor, sehingga benda yang hanya berbelok (kelajuannya tetap) juga mengalami percepatan.",
        "Gerak pada sumbu x dan sumbu y <b>saling bebas</b>. Persamaan GLB atau GLBB dipakai terpisah pada tiap sumbu, lalu hasilnya digabungkan dengan vektor.",
        "<b>Gerak parabola</b> (hambatan udara diabaikan): pada sumbu x tidak ada percepatan (GLB), pada sumbu y percepatannya g ke bawah (GLBB).",
    ],
    rumus=[
        V("a") + " = " + fr("Δ" + V("v"), "Δt") + ", dengan Δ" + V("v") + " = " + V("v") + "<sub>akhir</sub> − " + V("v") + "<sub>awal</sub>",
        "Per sumbu: v = v₀ + at; s = v₀t + ½at²",
        "Parabola: v<sub>x</sub> = v₀ cos α (tetap); v<sub>y</sub> = v₀ sin α − gt; kelajuan = √(v<sub>x</sub>² + v<sub>y</sub>²)",
        "t<sub>puncak</sub> = " + fr("v₀ sin α", "g") + "; h<sub>maks</sub> = " + fr("(v₀ sin α)²", "2g") + "; jarak mendatar R = " + fr("v₀² sin 2α", "g"),
        "Lemparan mendatar dari ketinggian h: waktu jatuh t = √(2h/g), sama dengan jatuh bebas",
    ],
    contoh=[
        ("Lemparan mendatar", "Bola dilempar mendatar 10 m/s dari ketinggian 5 m (g = 10 m/s²). Tentukan kelajuannya saat menyentuh tanah.",
         ["Waktu jatuh: 5 = ½ · 10 · t² → t = 1 s.", "v<sub>x</sub> = 10 m/s; v<sub>y</sub> = 10 · 1 = 10 m/s.", "Kelajuan = √(10² + 10²) = 10√2 ≈ 14,1 m/s, arah 45° di bawah horizontal."],
         "≈ 14,1 m/s"),
        ("Kecepatan dengan tanda", "Troli bergerak ke kanan 12 m/s dan mendapat percepatan tetap 3 m/s² ke kiri. Tentukan kecepatannya setelah 6 s.",
         ["Ambil kanan positif: a = −3 m/s².", "v = 12 + (−3)(6) = −6 m/s.", "Tanda negatif: troli bergerak ke kiri (berhenti sesaat pada t = 4 s, lalu berbalik)."],
         "6 m/s ke kiri"),
    ],
    bertahap=dict(
        soal="Bola ditendang 20 m/s dengan sudut 53° (sin 53° = 0,8; cos 53° = 0,6; g = 10 m/s²). Tentukan kelajuannya 1 s setelah ditendang.",
        langkah=["v<sub>x</sub> = 20 × 0,6 = ____ m/s (tetap).", "v<sub>y</sub> = 20 × 0,8 − 10 × 1 = ____ m/s.", "Kelajuan = √(____² + ____²) = √____ ≈ ____ m/s."],
        cek="Mengapa v<sub>x</sub> tidak berubah?",
        opsi=["(a) tidak ada percepatan pada arah mendatar", "(b) bola belum mencapai titik tertinggi"],
        kunci="v<sub>x</sub> = 12 m/s; v<sub>y</sub> = 6 m/s; √(144 + 36) = √180 ≈ 13,4 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Di titik tertinggi lintasan parabola kecepatannya <b>tidak nol</b>: v<sub>y</sub> = 0 tetapi v<sub>x</sub> tetap ada.",
        "Bola yang menumbuk dinding 6 m/s lalu memantul 6 m/s mengalami Δv = 12 m/s, bukan nol, karena arahnya berbalik.",
        "Benda yang dilempar mendatar dan benda yang dijatuhkan dari ketinggian sama tiba di tanah bersamaan.",
    ],
    latihan=[
        (1, "Kecepatan mobil berubah dari 10 m/s menjadi 30 m/s dalam 5 s, arahnya tetap. Tentukan percepatannya.", "4 m/s²", "(30 − 10)/5 = 4 m/s²."),
        (1, "Bola dijatuhkan dari ketinggian 20 m (g = 10 m/s²). Berapa lama bola sampai di tanah?", "2 s", "20 = 5t² → t = 2 s."),
        (1, "Bola ditendang 20 m/s dengan sudut 37° (sin 37° = 0,6; cos 37° = 0,8). Tentukan komponen kecepatan awalnya.", "v<sub>x</sub> = 16 m/s; v<sub>y</sub> = 12 m/s", "20 × 0,8 dan 20 × 0,6."),
        (1, "Berapa kelajuan bola pada soal sebelumnya ketika berada di titik tertinggi?", "16 m/s", "Di puncak v<sub>y</sub> = 0, tinggal v<sub>x</sub> = 16 m/s."),
        (1, "Benda bergerak 8 m/s ke kanan dengan percepatan 2 m/s² ke kiri. Tentukan kecepatannya setelah 6 s.", "4 m/s ke kiri", "v = 8 − 2 · 6 = −4 m/s."),
        (2, "Bola tenis menumbuk dinding tegak lurus dengan 10 m/s dan memantul lurus kembali dengan 8 m/s. Tentukan besar perubahan kecepatannya.", "18 m/s", "Arah menuju dinding positif: Δv = (−8) − 10 = −18 m/s."),
        (2, "Mobil melaju 10 m/s ke timur, lalu berbelok sehingga 5 s kemudian melaju 10 m/s ke utara. Tentukan besar percepatan rata-ratanya (√2 ≈ 1,41).", "≈ 2,83 m/s²", "|Δv| = √(10² + 10²) = 10√2 ≈ 14,1 m/s; ÷ 5 s ≈ 2,83 m/s²."),
        (2, "Bola dilempar mendatar 15 m/s dari atap setinggi 20 m (g = 10 m/s²). Tentukan waktu jatuh, jarak mendatar, dan kelajuan saat menyentuh tanah.", "2 s; 30 m; 25 m/s", "t = √(2 · 20/10) = 2 s; x = 15 · 2 = 30 m; v<sub>y</sub> = 20 m/s; √(225 + 400) = 25 m/s."),
        (2, "Bola ditendang 20 m/s dengan sudut 37° (sin 37° = 0,6). Tentukan waktu mencapai puncak dan tinggi maksimumnya (g = 10 m/s²).", "1,2 s; 7,2 m", "t = 12/10 = 1,2 s; h = 12²/20 = 7,2 m."),
        (3, "Dua bola ditendang 30 m/s dengan sudut 30° dan 60° (sin 60° = ½√3). Tunjukkan bahwa jarak mendatarnya sama, lalu hitung jaraknya (√3 ≈ 1,73).", "Sama, R = 45√3 ≈ 77,9 m", "sin 60° = sin 120° = ½√3. R = 900 · ½√3 / 10 = 45√3 ≈ 77,9 m untuk keduanya."),
        (3, "Dari ketinggian 80 m, bola X dijatuhkan dan bola Y dilempar mendatar 15 m/s pada saat yang sama (g = 10 m/s²). Tentukan waktu jatuh masing-masing, jarak mendatar Y, dan kelajuan Y saat mendarat.", "4 s untuk keduanya; 60 m; ≈ 42,7 m/s", "t = √(160/10) = 4 s. x = 15 · 4 = 60 m. v<sub>y</sub> = 40 m/s; √(225 + 1.600) = √1.825 ≈ 42,7 m/s."),
        (3, f"Kecepatan partikel pada t = 0 adalah (3{i} + 4{j}) m/s dan pada t = 2 s adalah (9{i} + 12{j}) m/s. Tentukan vektor dan besar percepatan rata-ratanya.", f"(3{i} + 4{j}) m/s²; 5 m/s²", "Δv = (6, 8) m/s; a = Δv/2 = (3, 4) m/s²; |a| = 5 m/s²."),
    ],
))

# ------------------------------------------------------------------ Subbab 5
SUB.append(dict(
    title="Kecepatan Relatif",
    tujuan="Menghitung kecepatan relatif dan resultan kecepatan pada perahu, kapal, pesawat, dan hujan.",
    konsep=[
        "Kecepatan selalu diukur terhadap sesuatu. Kecepatan perahu terhadap air berbeda dengan kecepatannya terhadap tepi sungai bila airnya mengalir.",
        "<b>Kecepatan terhadap tanah</b> = kecepatan terhadap air (atau udara) + kecepatan arus (atau angin), dijumlahkan sebagai vektor.",
        "<b>Kecepatan A menurut B</b> diperoleh dengan mengurangkan kecepatan B dari kecepatan A. Mengurangkan sebuah vektor sama dengan menambahkan vektor yang arahnya berlawanan.",
    ],
    rumus=[
        V("v") + "<sub>AB</sub> = " + V("v") + "<sub>A</sub> − " + V("v") + "<sub>B</sub>",
        V("v") + "<sub>tanah</sub> = " + V("v") + "<sub>relatif terhadap air/udara</sub> + " + V("v") + "<sub>arus/angin</sub>",
        "Menyeberang tegak lurus tepi: t = d/v<sub>perahu</sub>; terbawa arus sejauh x = v<sub>arus</sub> · t",
        "Tiba tepat di seberang: arahkan ke hulu dengan sin θ = v<sub>arus</sub>/v<sub>perahu</sub> (θ dari garis tegak lurus tepi); laju menyeberang √(v<sub>perahu</sub>² − v<sub>arus</sub>²)",
    ],
    contoh=[
        ("Menyeberang sungai", "Sungai selebar 80 m berarus 6 m/s; perahu melaju 10 m/s relatif terhadap air. Bandingkan dua cara menyeberang.",
         ["Tegak lurus tepi: t = 80 ÷ 10 = 8 s, terbawa 6 × 8 = 48 m ke hilir.",
          "Tepat ke seberang: sin θ = 6/10 = 0,6 → θ = 37° ke hulu; laju menyeberang √(100 − 36) = 8 m/s; t = 80 ÷ 8 = 10 s."],
         "8 s (terbawa 48 m) atau 10 s (tepat di seberang)"),
        ("Hujan menurut pesepeda", "Hujan turun tegak 6 m/s (tanpa angin). Pesepeda melaju 8 m/s ke timur. Bagaimana hujan tampak menurut pesepeda?",
         ["v<sub>hujan, relatif</sub> = (0, −6) − (8, 0) = (−8, −6) m/s: 8 m/s ke barat dan 6 m/s ke bawah.",
          "Besarnya √(64 + 36) = 10 m/s. Sudut dari vertikal: tan θ = 8/6 → θ ≈ 53°.",
          "Tetes bergerak ke barat, menuju pesepeda yang menghadap timur, jadi hujan tampak datang dari depan."],
         "10 m/s, miring 53° dari vertikal, dari depan"),
    ],
    bertahap=dict(
        soal="Kapal berangkat dari Pulau A pukul 07.30 menuju Pulau B, 30 km tepat di timurnya, dan harus tiba pukul 09.00. Arus laut 2 km/jam ke timur. Berapa kecepatan kapal relatif terhadap air?",
        langkah=["Waktu tempuh = ____ jam.", "Kecepatan terhadap dasar laut = 30 ÷ ____ = ____ km/jam ke timur.",
                 "v<sub>kapal thd air</sub> = ____ − 2 = ____ km/jam ke timur."],
        cek="Arus yang searah dengan gerak kapal",
        opsi=["(a) ikut mendorong, jadi kapal cukup lebih lambat terhadap air", "(b) menghambat, jadi kapal harus lebih cepat"],
        kunci="1,5 jam; 20 km/jam; 18 km/jam ke timur. Alasan: (a).",
    ),
    jebakan=[
        "Bila perahu diarahkan tegak lurus tepi, arus tidak mengubah waktu menyeberang; arus hanya menggeser titik tiba.",
        "Kecepatan A menurut B adalah " + V("v") + "<sub>A</sub> <b>dikurangi</b> " + V("v") + "<sub>B</sub>. Dua mobil yang berpapasan saling melihat lebih cepat, bukan lebih lambat.",
        "Tiba tepat di seberang hanya mungkin bila perahu lebih cepat daripada arus.",
    ],
    latihan=[
        (1, "Perahu melaju 4 m/s ke utara relatif terhadap air; arus 3 m/s ke timur. Berapa kelajuan perahu terhadap tepi?", "5 m/s", "√(16 + 9) = 5 m/s."),
        (1, "Kereta melaju 20 m/s. Penumpang berjalan 2 m/s di dalamnya (a) searah kereta, (b) ke arah belakang. Tentukan kecepatan penumpang terhadap tanah.", "(a) 22 m/s; (b) 18 m/s, keduanya searah kereta", "Searah dijumlahkan; berlawanan dikurangkan."),
        (1, "Mobil A melaju 25 m/s dan mobil B 20 m/s ke arah yang sama. Berapa kecepatan A menurut B?", "5 m/s searah gerak", "25 − 20 = 5 m/s."),
        (1, "Mobil A (25 m/s) dan mobil B (20 m/s) bergerak berlawanan arah dan akan berpapasan. Berapa kelajuan A menurut B?", "45 m/s", "25 − (−20) = 45 m/s."),
        (1, "Pesawat diarahkan ke utara 240 km/jam relatif terhadap udara; angin 70 km/jam ke timur. Tentukan kelajuan pesawat terhadap tanah.", "250 km/jam", "√(240² + 70²) = √62.500 = 250 km/jam."),
        (2, "Sungai selebar 60 m berarus 3 m/s. Perahu 5 m/s relatif terhadap air diarahkan tegak lurus tepi. Tentukan waktu menyeberang dan pergeseran ke hilir.", "12 s; 36 m", "t = 60/5 = 12 s; x = 3 × 12 = 36 m."),
        (2, "Pada sungai yang sama (60 m, arus 3 m/s, perahu 5 m/s), ke mana perahu harus diarahkan agar tiba tepat di seberang, dan berapa lama? (sin 37° = 0,6)", "37° ke hulu dari garis tegak lurus tepi; 15 s", "5 sin θ = 3 → θ = 37°. Laju menyeberang 5 × 0,8 = 4 m/s; 60/4 = 15 s."),
        (2, "Pada pukul 10.00, kapal A dan B melewati pelampung yang sama. A berlayar 9 km/jam ke timur, B 12 km/jam ke utara. Berapa jarak keduanya pada pukul 10.20?", "5 km", "Setelah ⅓ jam: A 3 km, B 4 km dari pelampung; √(9 + 16) = 5 km."),
        (2, "Mobil P melaju 15 m/s ke timur, mobil Q 20 m/s ke utara. Tentukan kecepatan Q menurut P.", "25 m/s, arah 37° dari utara ke barat", "v<sub>QP</sub> = (−15, 20); √(225 + 400) = 25 m/s; tan θ = 15/20 dari utara ke barat, θ ≈ 37°."),
        (3, "Pesawat berkelajuan 250 km/jam relatif terhadap udara harus terbang ke kota 800 km tepat di utaranya. Angin bertiup 150 km/jam ke timur. Ke mana pesawat diarahkan dan berapa lama penerbangannya? (sin 37° = 0,6)", "37° dari utara ke barat; 4 jam", "250 sin θ = 150 → sin θ = 0,6 → θ = 37° ke barat. Komponen ke utara 250 × 0,8 = 200 km/jam; 800/200 = 4 jam."),
        (3, "Sungai selebar 100 m berarus 3 m/s; perahu 5 m/s relatif terhadap air. Berapa selisih waktu antara cara tercepat dan cara tiba tepat di seberang?", "5 s (20 s dan 25 s)", "Tercepat: 100/5 = 20 s. Tepat di seberang: laju menyeberang √(25 − 9) = 4 m/s; 100/4 = 25 s."),
        (3, "Ani diam di eskalator yang bergerak dan sampai di atas dalam 60 s. Saat eskalator mati, ia berjalan naik dalam 40 s. Berapa lama ia sampai di atas jika berjalan di eskalator yang bergerak?", "24 s", "Misalkan panjang L: v<sub>eskalator</sub> = L/60, v<sub>Ani</sub> = L/40. Jumlahnya L/60 + L/40 = L/24, jadi waktunya 24 s."),
    ],
))

CAMPURAN = [
    (1, "Mobil mengelilingi bundaran tepat satu putaran. Berapa perpindahannya?", "0", "Posisi akhir sama dengan posisi awal."),
    (1, "Dua kecepatan 9 m/s dan 12 m/s saling tegak lurus. Berapa resultannya?", "15 m/s", "√(81 + 144) = 15 m/s."),
    (1, "Kecepatan 50 m/s berarah 53° di atas horizontal (sin 53° = 0,8). Tentukan komponennya.", "v<sub>x</sub> = 30 m/s; v<sub>y</sub> = 40 m/s", "50 × 0,6 dan 50 × 0,8."),
    (1, "Pejalan kaki menempuh 3 km dalam 15 menit. Berapa kelajuan rata-ratanya dalam km/jam?", "12 km/jam", "3 ÷ 0,25 = 12 km/jam."),
    (2, "Siswa berjalan 5 m ke utara lalu 12 m ke timur dalam 10 s. Tentukan kelajuan rata-rata dan besar kecepatan rata-ratanya.", "1,7 m/s; 1,3 m/s", "17/10 = 1,7 m/s; perpindahan 13 m → 1,3 m/s."),
    (2, "Benda berpindah dari posisi (−2, 5) m ke (4, −3) m dalam 2 s. Tentukan perpindahan dan besar kecepatan rata-ratanya.", f"(6{i} − 8{j}) m; 5 m/s", "Δr = (6, −8), besarnya 10 m; 10/2 = 5 m/s."),
    (2, "Kelereng menggelinding keluar dari tepi meja setinggi 0,8 m dengan kecepatan mendatar 5 m/s (g = 10 m/s²). Seberapa jauh dari kaki meja kelereng mendarat?", "2 m", "t = √(1,6/10) = 0,4 s; x = 5 × 0,4 = 2 m."),
    (2, "Hujan turun tegak 8 m/s. Pengendara motor melaju 6 m/s. Berapa kelajuan hujan menurut pengendara dan berapa sudutnya dari vertikal?", "10 m/s; 37° (dari depan)", "√(64 + 36) = 10 m/s; tan θ = 6/8 → θ ≈ 37°."),
    (2, "Perahu 5 m/s relatif terhadap air menyusuri sungai berarus 2 m/s, 420 m ke hilir lalu kembali ke titik awal. Berapa waktu totalnya?", "200 s", "Hilir 7 m/s → 60 s; hulu 3 m/s → 140 s."),
    (3, "Roket air A dan B diluncurkan tegak bersamaan dengan 30 m/s dan 40 m/s (g = 10 m/s²). Berapa selisih ketinggian keduanya setelah 2 s?", "20 m", "h<sub>A</sub> = 60 − 20 = 40 m; h<sub>B</sub> = 80 − 20 = 60 m. Keduanya masih naik (t<sub>puncak</sub> A = 3 s)."),
    (3, "Bola menggelinding dari tepi meja setinggi 1,25 m dan mendarat 2 m dari kaki meja (g = 10 m/s²). Berapa kecepatan bola saat meninggalkan meja?", "4 m/s", "t = √(2,5/10) = 0,5 s; v = 2/0,5 = 4 m/s."),
    (3, "Sungai selebar 100 m berarus 4 m/s; perahu 5 m/s relatif terhadap air harus tiba tepat di seberang. Ke mana perahu diarahkan dan berapa lama? (sin 53° = 0,8)", "53° ke hulu dari garis tegak lurus tepi; ≈ 33,3 s", "5 sin θ = 4 → θ = 53°. Laju menyeberang 3 m/s; 100/3 ≈ 33,3 s."),
]

# ------------------------------------------------------------------ TKA-level items
# (type, level, format, stem, options, key, explanation, wrong-option notes)
TKA = [
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Seorang pendaki mengikuti jalur: 7 km ke utara, kemudian 12 km ke timur, lalu 2 km ke selatan menuju pos terakhir. Petugas ingin menarik kabel radio lurus dari titik awal ke pos terakhir. Panjang kabel minimum yang diperlukan adalah ....",
         opsi=["5 km", "13 km", "15 km", "17 km", "21 km"], kunci=1,
         bahas="Komponen utara 7 − 2 = 5 km, timur 12 km; √(144 + 25) = 13 km.",
         salah="A: hanya komponen utara. C: lupa mengurangkan 2 km (√(12² + 9²)). D: menjumlahkan komponen. E: itu jaraknya."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Sebuah robot pengintai bergerak di lantai datar. Sensornya mencatat komponen kecepatan pada sumbu x dan y yang saling tegak lurus.",
         tabel=[["t (s)", "0", "1", "2", "3"], ["v<sub>x</sub> (m/s)", "6", "6", "6", "6"], ["v<sub>y</sub> (m/s)", "0", "4", "8", "12"]],
         soal2="Kondisi gerak robot pada t = 2 s adalah ....",
         opsi=["kelajuan 10 m/s dan percepatan 4 m/s² searah sumbu y", "kelajuan 14 m/s dan percepatan 4 m/s² searah sumbu y",
               "kelajuan 10 m/s dan percepatan nol karena v<sub>x</sub> tetap", "kelajuan 8 m/s dan percepatan 4 m/s² searah sumbu y",
               "kelajuan 10 m/s dan percepatan 5 m/s² searah gerak robot"], kunci=0,
         bahas="Pada t = 2 s: √(6² + 8²) = 10 m/s. a<sub>x</sub> = 0, a<sub>y</sub> = 4 m/s².",
         salah="B: menjumlahkan komponen. C: hanya melihat sumbu x. D: hanya sumbu y. E: percepatan dihitung dari kelajuan."),
    dict(tipe="FIS-KONSEP", lv=2, fmt="pgk",
         soal="Seorang pembalap mengitari lintasan berbentuk lingkaran dengan kelajuan tetap 20 m/s dan kembali ke garis start setelah tepat satu putaran. Pernyataan yang benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["Kelajuan rata-rata satu putaran 20 m/s.", "Kecepatan rata-rata satu putaran nol.", "Percepatan pembalap nol karena kelajuannya tetap.",
               "Besar kecepatan sesaatnya selalu 20 m/s.", "Arah kecepatan sesaat selalu menuju pusat lingkaran."], kunci=[0, 1, 3],
         bahas="Kelajuan tetap → kelajuan rata-rata dan besar kecepatan sesaat 20 m/s. Satu putaran → perpindahan nol → kecepatan rata-rata nol.",
         salah="C: arah kecepatan berubah, jadi ada percepatan sentripetal. E: kecepatan sesaat menyinggung lingkaran; yang menuju pusat adalah percepatannya."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="pg",
         soal="Kapal penyeberangan berangkat dari Pulau A pukul 07.30 menuju Pulau B yang terletak 24 km tepat di sebelah timur Pulau A. Arus laut bergerak dari barat ke timur dengan kecepatan 3 km/jam. Kapal harus tiba tepat pukul 09.00. Strategi yang harus diterapkan nakhoda adalah ....",
         opsi=["bergerak ke timur dengan kecepatan 13 km/jam relatif terhadap air", "bergerak ke timur dengan kecepatan 16 km/jam relatif terhadap air",
               "bergerak ke timur dengan kecepatan 19 km/jam relatif terhadap air", "bergerak ke barat dengan kecepatan 13 km/jam relatif terhadap air",
               "bergerak ke tenggara dengan kecepatan 16 km/jam relatif terhadap air"], kunci=0,
         bahas="Waktu 1,5 jam → kecepatan terhadap dasar laut 24 ÷ 1,5 = 16 km/jam ke timur. Arus searah: 16 − 3 = 13 km/jam.",
         salah="B: lupa arus, tiba lebih awal. C: arus dikurangkan dengan arah terbalik. D: arah salah. E: kapal menyimpang ke selatan."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Catatan GPS seorang kurir motor ditunjukkan pada tabel berikut. Tiap ruas ditempuh lurus.",
         tabel=[["Waktu", "Gerak"], ["menit 0–10", "3 km ke timur"], ["menit 10–20", "4 km ke utara"], ["menit 20–30", "berhenti mengantar paket"]],
         soal2="Pernyataan yang tepat tentang gerak kurir selama 30 menit adalah ....",
         opsi=["Kelajuan rata-ratanya 14 km/jam, sedangkan besar kecepatan rata-ratanya 10 km/jam.", "Kelajuan rata-rata dan besar kecepatan rata-ratanya sama-sama 14 km/jam.",
               "Kelajuan rata-ratanya 21 km/jam, karena waktu berhenti tidak dihitung.", "Besar kecepatan rata-ratanya 15 km/jam, karena waktu berhenti tidak dihitung.",
               "Kelajuan rata-ratanya 10 km/jam, sedangkan besar kecepatan rata-ratanya 14 km/jam."], kunci=0,
         bahas="Jarak 7 km ÷ 0,5 jam = 14 km/jam. Perpindahan 5 km ÷ 0,5 jam = 10 km/jam.",
         salah="B: kecepatan disamakan dengan kelajuan. C dan D: hanya memakai 20 menit. E: keduanya tertukar."),
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Pada pukul 10.00, kapal A dan kapal B melewati pelampung yang sama. Kapal A berlayar lurus ke timur dengan kecepatan 12 km/jam, sedangkan kapal B berlayar lurus ke utara dengan kecepatan 16 km/jam. Jarak kedua kapal pada pukul 10.30 adalah ....",
         opsi=["2 km", "10 km", "14 km", "20 km", "28 km"], kunci=1,
         bahas="Setelah 0,5 jam: A 6 km, B 8 km dari pelampung; √(36 + 64) = 10 km.",
         salah="A: 8 − 6. C: 6 + 8. D: |v<sub>A</sub> − v<sub>B</sub>| = 20 km/jam, lupa dikali waktu. E: 12 + 16."),
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Sebuah bola dilempar mendatar dari tepi atap gedung setinggi 45 m dengan kecepatan 40 m/s (g = 10 m/s²; hambatan udara diabaikan). Kecepatan bola tepat sebelum menyentuh tanah adalah ....",
         opsi=["50 m/s, arah 37° di bawah horizontal", "50 m/s, arah 53° di bawah horizontal", "70 m/s, arah 37° di bawah horizontal",
               "30 m/s, arah tegak ke bawah", "40 m/s, arah mendatar"], kunci=0,
         bahas="45 = 5t² → t = 3 s; v<sub>y</sub> = 30 m/s, v<sub>x</sub> = 40 m/s; v = 50 m/s; tan θ = 30/40 → θ ≈ 37° di bawah horizontal.",
         salah="B: sudut tertukar (tan θ = 40/30). C: komponen dijumlahkan. D: hanya komponen tegak. E: hanya komponen mendatar."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Perahu motor bermassa total 100 kg melaju dengan kecepatan tetap 8 m/s ke utara. Ketika melewati muara, arus dari barat memberi gaya mendatar 200 N ke timur selama 3 s, lalu gaya arus itu hilang. Selama itu mesin menjaga kecepatan ke utara tetap 8 m/s, dan gaya lain pada arah timur–barat diabaikan. Kondisi gerak perahu setelah gaya arus hilang adalah ....",
         opsi=["kelajuan 10 m/s dengan arah 37° ke timur dari utara, lalu bergerak lurus dengan kecepatan tetap",
               "kelajuan 10 m/s dengan arah 53° ke timur dari utara, lalu bergerak lurus dengan kecepatan tetap",
               "kelajuan 14 m/s dengan arah 37° ke timur dari utara, lalu bergerak lurus dengan kecepatan tetap",
               "kelajuan 10 m/s dengan arah 37° ke timur dari utara, lalu terus dipercepat ke timur",
               "kelajuan 8 m/s ke utara, karena mesin menjaga kecepatan perahu"], kunci=0,
         bahas="a = 200/100 = 2 m/s²; v<sub>timur</sub> = 2 × 3 = 6 m/s. √(64 + 36) = 10 m/s; tan θ = 6/8 dari utara → 37°. Setelah gaya hilang, resultan gaya nol → kecepatan tetap.",
         salah="B: sudut diukur dari timur. C: komponen dijumlahkan. D: gaya sudah hilang, jadi tidak ada percepatan. E: mengabaikan komponen ke timur."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="bs",
         soal="Tim SAR harus membawa perahu karet ke titik yang tepat berada di seberang posko, menyeberangi sungai selebar 80 m yang arusnya 3 m/s. Perahu dapat melaju 5 m/s relatif terhadap air. Target: tiba di titik itu dalam waktu <b>tidak lebih dari 25 s</b>. (sin 37° = 0,6; cos 37° = 0,8; sudut diukur dari garis tegak lurus tepi.) Tentukan apakah setiap strategi berikut tepat untuk mencapai target.",
         opsi=["Mengarahkan perahu tegak lurus tepi sepanjang penyeberangan.", "Mengarahkan perahu 37° ke arah hulu sepanjang penyeberangan.",
               "Mengarahkan perahu 53° ke arah hulu sepanjang penyeberangan.",
               "Mengarahkan perahu tegak lurus tepi, lalu setelah tiba menyusuri tepi ke arah hulu dengan laju 5 m/s relatif terhadap air."],
         kunci=[False, True, False, False],
         bahas="1: 16 s tetapi terbawa 48 m ke hilir (Tidak Tepat). 2: komponen ke hulu 3 m/s meniadakan arus; laju menyeberang 4 m/s; 20 s (Tepat). 3: komponen ke hulu 4 m/s &gt; 3 m/s, perahu bergeser ke hulu, waktu ≈ 26,7 s (Tidak Tepat). 4: 16 s + 48 m ÷ 2 m/s = 40 s (Tidak Tepat).",
         salah=""),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Dua perenang, Dini dan Eka, sama-sama mampu berenang 1,5 m/s relatif terhadap air. Mereka mulai bersamaan dari titik yang sama di tepi sungai selebar 30 m yang arusnya 0,9 m/s. Dini selalu menghadap tegak lurus tepi. Eka menghadap ke arah hulu sehingga lintasannya lurus menuju titik tepat di seberang. Kondisi yang akan terjadi adalah ....",
         opsi=["Dini tiba lebih dulu, setelah 20 s, di titik 18 m ke hilir; Eka tiba tepat di seberang setelah 25 s.", "Eka tiba lebih dulu karena lintasannya lebih pendek.",
               "Keduanya tiba bersamaan karena kelajuan berenangnya sama.", "Dini tiba lebih dulu, setelah 20 s, tepat di seberang titik awal.",
               "Dini tiba lebih dulu, setelah sekitar 17 s, karena arus menambah kelajuannya."], kunci=0,
         bahas="Dini: 30/1,5 = 20 s, terbawa 0,9 × 20 = 18 m. Eka: komponen menyeberang √(2,25 − 0,81) = 1,2 m/s; 30/1,2 = 25 s.",
         salah="B: yang menentukan waktu adalah komponen menyeberang, bukan panjang lintasan. C: komponen menyeberang keduanya berbeda. D: Dini terbawa arus. E: membagi lebar sungai dengan kelajuan terhadap tanah (≈ 1,75 m/s)."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Dua siswa menendang bola dari tanah datar dengan kelajuan awal sama, 20 m/s. Bola P ditendang pada sudut 37° dan bola Q pada sudut 53° (sin 37° = 0,6; cos 37° = 0,8; g = 10 m/s²; hambatan udara diabaikan). Pernyataan yang tepat tentang kedua bola adalah ....",
         opsi=["Keduanya mendarat pada jarak mendatar yang sama, tetapi bola Q lebih lama berada di udara.", "Bola Q mendarat lebih jauh karena sudut tendangannya lebih besar.",
               "Kedua bola sama lama berada di udara karena kelajuan awalnya sama.", "Jarak mendatar kedua bola sama, dan kelajuan keduanya di titik tertinggi juga sama.",
               "Bola P mencapai titik lebih tinggi karena komponen mendatar kecepatannya lebih besar."], kunci=0,
         bahas="sin 2α = 2 × 0,6 × 0,8 = 0,96 untuk keduanya → R = 38,4 m. Waktu di udara: P 2,4 s, Q 3,2 s.",
         salah="B: jarak sama. C: P 2,4 s, Q 3,2 s. D: kelajuan di puncak P 16 m/s, Q 12 m/s. E: tinggi maksimum P 7,2 m, Q 12,8 m."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="pg",
         soal="Sebuah drone harus mengantar obat ke posko yang berada 1.600 m tepat di utara titik lepas landas, dalam waktu tidak lebih dari 4 menit. Laju drone 10 m/s relatif terhadap udara, dan angin bertiup ke timur 6 m/s. Strategi yang memenuhi tujuan dan batas waktu adalah .... (sin 37° = 0,6; cos 37° = 0,8)",
         opsi=["mengarahkan drone 37° ke barat dari utara; tiba setelah 200 s", "mengarahkan drone tepat ke utara; tiba setelah 160 s",
               "mengarahkan drone 37° ke timur dari utara; tiba setelah 200 s", "mengarahkan drone 53° ke barat dari utara; tiba setelah 160 s",
               "mengarahkan drone 37° ke barat dari utara; tiba setelah 160 s"], kunci=0,
         bahas="10 sin θ = 6 → θ = 37° ke barat. Komponen ke utara 8 m/s; 1.600/8 = 200 s ≤ 240 s.",
         salah="B: drone terbawa 960 m ke timur. C: menambah hanyutan. D: komponen ke barat 8 m/s melebihi angin. E: waktu dihitung dengan 10 m/s."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Dari jendela setinggi 45 m, bola X dijatuhkan bebas dan pada saat yang sama bola Y dilempar mendatar dengan kecepatan 10 m/s (g = 10 m/s²; hambatan udara diabaikan). Kondisi yang akan terjadi adalah ....",
         opsi=["Kedua bola menyentuh tanah bersamaan setelah 3 s; bola Y mendarat 30 m dari kaki gedung dengan kelajuan lebih besar.",
               "Bola X menyentuh tanah lebih dulu karena lintasannya lebih pendek.", "Bola Y menyentuh tanah lebih dulu karena kecepatan awalnya lebih besar.",
               "Kedua bola menyentuh tanah bersamaan setelah 3 s dengan kelajuan sama, 30 m/s.",
               "Kedua bola menyentuh tanah bersamaan setelah 4,5 s; bola Y mendarat 45 m dari kaki gedung."], kunci=0,
         bahas="45 = 5t² → t = 3 s untuk keduanya. Y: x = 30 m; kelajuan √(30² + 10²) ≈ 31,6 m/s &gt; 30 m/s.",
         salah="B dan C: dugaan intuitif; gerak tegak keduanya sama. D: lupa komponen mendatar Y. E: waktu dihitung 45/10."),
]

# ------------------------------------------------------------------ Uji kompetensi
UJI_PG = [
    ("Kelompok besaran yang semuanya vektor adalah ....", ["jarak, kelajuan, waktu", "perpindahan, kecepatan, percepatan", "massa, kecepatan, gaya", "perpindahan, kelajuan, percepatan", "energi, gaya, waktu"], 1,
     "Ketiganya berarah.", "A, E: semuanya atau sebagian skalar. C: massa skalar. D: kelajuan skalar."),
    (f"Besar vektor {V('v')} = (−9{i} + 12{j}) m/s adalah ....", ["3 m/s", "15 m/s", "21 m/s", "225 m/s", "108 m/s"], 1,
     "√(81 + 144) = 15 m/s.", "A: −9 + 12. C: 9 + 12. D: lupa diakar. E: 9 × 12."),
    ("Komponen tegak kecepatan 40 m/s yang berarah 37° di atas horizontal (sin 37° = 0,6; cos 37° = 0,8) adalah ....", ["32 m/s", "24 m/s", "40 m/s", "30 m/s", "20 m/s"], 1,
     "40 × 0,6 = 24 m/s.", "A: memakai cos (komponen mendatar). C: besar vektornya. D, E: tidak ada dasar perhitungan."),
    ("Resultan dua kecepatan 8 m/s dan 6 m/s yang saling tegak lurus adalah ....", ["2 m/s", "10 m/s", "14 m/s", "48 m/s", "7 m/s"], 1,
     "√(64 + 36) = 10 m/s.", "A: berlawanan arah. C: searah. D: dikalikan. E: dirata-rata."),
    ("Dua vektor masing-masing 10 satuan membentuk sudut apit 120°. Besar resultannya adalah ....", ["0", "10 satuan", "20 satuan", "17,3 satuan", "14,1 satuan"], 1,
     "R = √(100 + 100 + 200 cos 120°) = √100 = 10.", "A: menganggap berlawanan arah. C: searah. D: memakai 60°. E: memakai 90°."),
    ("Seseorang berjalan 6 m ke timur lalu 8 m ke barat. Jarak dan perpindahannya adalah ....", ["14 m dan 2 m ke barat", "14 m dan 2 m ke timur", "2 m dan 14 m ke barat", "10 m dan 10 m ke barat", "14 m dan 14 m ke barat"], 0,
     "Jarak 6 + 8 = 14 m; perpindahan 6 − 8 = −2 m (ke barat).", "B: arah terbalik. C: tertukar. D: dianggap tegak lurus. E: perpindahan disamakan dengan jarak."),
    ("Pelari menempuh satu putaran penuh lintasan 400 m dalam 50 s. Kelajuan rata-rata dan kecepatan rata-ratanya adalah ....", ["8 m/s dan 8 m/s", "8 m/s dan 0", "0 dan 8 m/s", "0 dan 0", "4 m/s dan 0"], 1,
     "400/50 = 8 m/s; kembali ke start → kecepatan rata-rata 0.", "A: kecepatan disamakan dengan kelajuan. C: tertukar. D: kelajuan tidak nol. E: salah hitung."),
    (f"Benda berpindah dari posisi (1{i} + 2{j}) m ke (7{i} + 10{j}) m. Besar perpindahannya adalah ....", ["10 m", "14 m", "6 m", "8 m", "14,4 m"], 0,
     "Δr = (6, 8); √(36 + 64) = 10 m.", "B: 6 + 8. C, D: satu komponen saja. E: menjumlahkan posisi (8, 12) lalu mencari besarnya."),
    ("Mobil melaju 20 m/s lalu direm dengan perlambatan tetap 4 m/s². Waktu sampai berhenti adalah ....", ["5 s", "80 s", "16 s", "24 s", "0,2 s"], 0,
     "0 = 20 − 4t → t = 5 s.", "B: dikalikan. C: 20 − 4. D: 20 + 4. E: 4/20."),
    ("Bola ditendang 50 m/s dengan sudut 53° (sin 53° = 0,8; cos 53° = 0,6). Kelajuan bola di titik tertinggi adalah ....", ["0", "30 m/s", "40 m/s", "50 m/s", "20 m/s"], 1,
     "Di puncak hanya v<sub>x</sub> = 50 × 0,6 = 30 m/s.", "A: miskonsepsi kecepatan nol di puncak. C: memakai sin. D: kelajuan awal. E: tidak ada dasar."),
    ("Bola dilempar mendatar 12 m/s dari ketinggian 45 m (g = 10 m/s²). Jarak mendatar tempat bola mendarat adalah ....", ["36 m", "54 m", "108 m", "24 m", "45 m"], 0,
     "t = √(90/10) = 3 s; x = 12 × 3 = 36 m.", "B: t = 45/10. C: t = 9 (lupa diakar). D: t = 2. E: disamakan dengan tinggi."),
    ("Sungai selebar 30 m berarus 4 m/s. Perahu 3 m/s relatif terhadap air diarahkan tegak lurus tepi. Kelajuan perahu terhadap tepi dan waktu menyeberang adalah ....", ["5 m/s; 10 s", "7 m/s; 4,3 s", "5 m/s; 6 s", "1 m/s; 30 s", "5 m/s; 7,5 s"], 0,
     "√(9 + 16) = 5 m/s; waktu ditentukan komponen menyeberang: 30/3 = 10 s.", "B: kecepatan dijumlahkan. C: 30/5. D: 4 − 3. E: 30/4."),
    ("Kereta melaju 30 m/s. Penumpang berjalan 2 m/s ke arah belakang kereta. Kecepatan penumpang terhadap tanah adalah ....", ["32 m/s searah kereta", "28 m/s searah kereta", "2 m/s ke belakang", "30 m/s searah kereta", "28 m/s ke belakang"], 1,
     "30 − 2 = 28 m/s, masih searah kereta.", "A: ditambahkan. C: kecepatan terhadap kereta. D: mengabaikan penumpang. E: arah salah."),
    ("Bola menumbuk dinding tegak lurus dengan 6 m/s dan memantul kembali dengan 4 m/s. Besar perubahan kecepatannya adalah ....", ["2 m/s", "10 m/s", "0", "7,2 m/s", "24 m/s"], 1,
     "(−4) − 6 = −10 m/s.", "A: selisih kelajuan. C: menganggap tidak berubah. D: √(36 + 16). E: dikalikan."),
    ("Hujan turun tegak 3 m/s. Pelari berlari 4 m/s ke utara. Menurut pelari, hujan datang dengan ....", ["5 m/s, miring 53° dari vertikal, dari depan", "5 m/s, miring 37° dari vertikal, dari depan", "5 m/s, miring 53° dari vertikal, dari belakang", "7 m/s, dari depan", "3 m/s, tegak"], 0,
     "v<sub>hujan, relatif</sub> = v<sub>hujan</sub> − v<sub>pelari</sub>: 4 m/s ke selatan (berlawanan arah lari) dan 3 m/s ke bawah. √(16 + 9) = 5 m/s; tan θ = 4/3 dari vertikal → 53°; datang dari depan.", "B: sudut tertukar. C: arah terbalik. D: dijumlahkan. E: mengabaikan gerak pelari."),
]
UJI_URAIAN = [
    ("Helikopter diarahkan ke utara dengan kelajuan 120 km/jam relatif terhadap udara. Angin bertiup ke timur 50 km/jam. (a) Berapa kelajuan helikopter terhadap tanah? (b) Berapa jarak yang ditempuhnya dalam 30 menit?",
     "(a) 130 km/jam; (b) 65 km", "(a) √(120² + 50²) = √16.900 = 130 km/jam. (b) 130 × 0,5 = 65 km."),
    (f"Posisi partikel pada t = 0 adalah (−3{i} + 4{j}) m dan pada t = 5 s adalah (9{i} + 9{j}) m. Tentukan perpindahan, besarnya, dan kecepatan rata-ratanya.",
     f"Δ{V('r')} = (12{i} + 5{j}) m; 13 m; (2,4{i} + {j}) m/s, besarnya 2,6 m/s", "Δr = (9 − (−3), 9 − 4) = (12, 5); √169 = 13 m; ÷ 5 s."),
    ("Bola ditendang 30 m/s dengan sudut 37° (sin 37° = 0,6; cos 37° = 0,8; g = 10 m/s²). Tentukan waktu mencapai puncak, tinggi maksimum, dan jarak mendatar.",
     "1,8 s; 16,2 m; 86,4 m", "v<sub>y</sub> = 18 m/s → t = 1,8 s; h = 18²/20 = 16,2 m; R = 900 × 0,96 / 10 = 86,4 m (atau 24 m/s × 3,6 s)."),
    ("Sungai selebar 120 m berarus 4 m/s; perahu 5 m/s relatif terhadap air. (a) Ke mana perahu diarahkan agar tiba tepat di seberang, dan berapa lama? (b) Berapa lama cara tercepat, dan seberapa jauh perahu terbawa? (sin 53° = 0,8)",
     "(a) 53° ke hulu dari garis tegak lurus tepi, 40 s; (b) 24 s, terbawa 96 m", "(a) 5 sin θ = 4 → θ = 53°; laju menyeberang 3 m/s; 120/3 = 40 s. (b) 120/5 = 24 s; 4 × 24 = 96 m."),
    ("Dua mobil meninggalkan perempatan pada saat yang sama: A ke utara 16 m/s, B ke timur 12 m/s. (a) Berapa kelajuan A menurut B? (b) Berapa jarak keduanya setelah 10 s?",
     "(a) 20 m/s; (b) 200 m", "(a) v<sub>AB</sub> = (−12, 16); √(144 + 256) = 20 m/s. (b) 20 × 10 = 200 m (atau √(160² + 120²))."),
]


def check():
    h, s = math.hypot, math.sqrt
    close = lambda a, b, t=1e-6: abs(a - b) <= t or (_ for _ in ()).throw(AssertionError((a, b)))
    # prasyarat
    close(h(6, 8), 10); close(h(5, 12), 13); close(72 / 3.6, 20)
    # subbab 1
    close(h(-5, 12), 13); close(math.degrees(math.atan2(12, 5)), 67.38, 0.01)
    close(h(12, -5), 13); close(200 * math.cos(math.radians(30)), 173.2, 0.1); close(s(625 - 400), 15); close(s(625 - 225), 20); close(h(-6, -8), 10)
    # subbab 2
    close(s(9 + 25 + 15), 7); close(h(9 - 3, 5 + 3), 10)
    close(s(25 + 64 + 2 * 5 * 8 * -0.5), 7); close(s(36 + 36 + 2 * 36 * -0.5), 6); close(s(200 - 200 * 0.5), 10); close(h(8 + 4, 6 - 1), 13)
    close(s(25 + 9 + 30 * 0.5), 7); assert 12 + 5 == 17 and 144 + 25 == 169
    # subbab 3
    close(h(8, 6), 10); close(70 / 50, 1.4); close(h(30, 40) / 50, 1)
    close(h(12, 16), 20); close(70 / 1.25, 56); close(50 / 1.25, 40); close(44 / 11, 4); close(28 / 11, 2.545, 0.001)
    close(14 / (2 / 3), 21); close(10 / (2 / 3), 15); close(h(60, 80) / 2.5, 40); close(240 / 5, 48)
    # subbab 4
    close(h(10, 10), 14.142, 0.001); close(h(12, 6), 13.416, 0.001); close(10 * math.sqrt(2) / 5, 2.828, 0.001)
    close(h(15, 20), 25); close(12 ** 2 / 20, 7.2); close(45 * math.sqrt(3), 77.94, 0.01); close(h(15, 40), 42.72, 0.01); close(h(6, 8), 10)
    # subbab 5
    close(s(100 - 36), 8); close(h(240, 70), 250); close(h(15, 20), 25); close(h(3, 4), 5); close(250 * 0.8, 200); close(100 / s(25 - 9), 25)
    close(1 / (1 / 60 + 1 / 40), 24)
    # campuran
    close(h(9, 12), 15); close(h(6, -8) / 2, 5); close(5 * s(1.6 / 10), 2); close(420 / 7 + 420 / 3, 200)
    close((30 * 2 - 20) - (40 * 2 - 20), -20); close(2 / s(2.5 / 10), 4); close(100 / 3, 33.33, 0.01)
    # TKA
    close(h(12, 5), 13); close(24 / 1.5 - 3, 13); close(h(6, 8), 10); close(h(40, 30), 50)
    close(h(8, 6), 10); close(80 / 4, 20); close(80 / (5 * 0.6), 26.67, 0.01); close(16 + 48 / 2, 40)
    close(s(1.5 ** 2 - 0.9 ** 2), 1.2); close(30 / 1.2, 25); close(30 / h(1.5, 0.9), 17.15, 0.01)
    close(400 * 0.96 / 10, 38.4); close(1600 / 8, 200); close(h(30, 10), 31.62, 0.01)
    # uji
    close(h(-9, 12), 15); close(s(200 + 200 * -0.5), 10); close(12 * s(90 / 10), 36); close(h(120, 50), 130)
    close(h(12, 5), 13); close(13 / 5, 2.6); close(18 ** 2 / 20, 16.2); close(900 * 0.96 / 10, 86.4); close(120 / 3, 40); close(h(16, 12), 20)
    return True
