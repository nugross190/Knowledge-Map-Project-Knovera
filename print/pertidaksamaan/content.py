"""Content of the printable module "Pertidaksamaan" (Matematika kelas X).

Inequalities in one variable: properties and linear inequalities, quadratic, rational (fractional),
absolute-value and square-root inequalities, all solved with a sign chart on the number line.
check() re-derives every solution set by testing a dense grid of exact rational points, including
every critical value, against the original inequality.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import numline, plane  # noqa: E402
from kit import fr, Q  # noqa: E402

BLUE, RED = "#1f3a68", "#c0502a"

PRASYARAT = [
    ("P1", "Hitung −2 · (−3) − 4.", "2", "6 − 4."),
    ("P2", "Faktorkan x² − x − 6.", "(x − 3)(x + 2)", "Dua bilangan yang hasil kalinya −6 dan jumlahnya −1: −3 dan 2."),
    ("P3", "Tentukan akar-akar x² − 4x − 5 = 0.", "x = −1 atau x = 5", "(x − 5)(x + 1) = 0."),
    ("P4", "Tentukan tanda nilai 2x − 6 untuk x = 0 dan untuk x = 5.", "negatif (−6) dan positif (4)", "2 · 0 − 6 = −6; 2 · 5 − 6 = 4."),
    ("P5", "Hitung |−7| dan |3 − 8|.", "7 dan 5", "Nilai mutlak adalah jarak ke 0, selalu tidak negatif."),
    ("P6", "Sederhanakan " + fr("x + 1", "x − 2") + " − 1.", fr("3", "x − 2"), "(x + 1 − (x − 2)) : (x − 2)."),
    ("P7", "Hitung (√5)² dan √16.", "5 dan 4", "√16 = 4, bukan ±4."),
    ("P8", "Tulis \"x lebih dari −2 dan paling besar 3\" sebagai pertidaksamaan.", "−2 &lt; x ≤ 3", "\"Paling besar\" berarti boleh sama dengan."),
]

INGAT = [
    ("A", "Bilangan bertanda", "P1, P4", "Subbab 1–3", ["Negatif kali negatif hasilnya positif; negatif kali positif hasilnya negatif.",
                                                    "Tanda nilai sebuah bentuk pada suatu x diketahui dengan memasukkan x itu."]),
    ("B", "Pemfaktoran", "P2, P3", "Subbab 2, 3", ["x² + bx + c = (x + p)(x + q) dengan p + q = b dan pq = c.", "Jika (x − p)(x − q) = 0, maka x = p atau x = q."]),
    ("C", "Pecahan aljabar", "P6", "Subbab 3", ["Samakan penyebut sebelum mengurangkan: " + fr("A", "B") + " − k = " + fr("A − kB", "B") + "."]),
    ("D", "Nilai mutlak dan akar", "P5, P7", "Subbab 4, 5", ["|a| = a bila a ≥ 0 dan |a| = −a bila a &lt; 0.", "√a hanya terdefinisi untuk a ≥ 0 dan nilainya tidak pernah negatif."]),
    ("E", "Menulis himpunan penyelesaian", "P8", "Semua subbab", ["&lt;, &gt;: batas tidak termasuk (bulatan kosong ○); ≤, ≥: batas termasuk (bulatan penuh ●).",
                                                                 "\"Paling sedikit\" berarti ≥; \"paling banyak\" atau \"tidak lebih dari\" berarti ≤."]),
]

# Sign charts (not to scale).
NL_LIN = numline([("−4", True)], shade=[1])
NL_CHAIN = numline([("−2", False), ("3", True)], shade=[1])
NL_Q1 = numline([("−2", False), ("3", False)], shade=[1], signs=["+", "−", "+"])
NL_Q2 = numline([("−1", True), ("5", True)], shade=[0, 2], signs=["+", "−", "+"])
NL_R1 = numline([("−3", False), ("2", True)], shade=[1], signs=["+", "−", "+"])
NL_R2 = numline([("−2", False), ("1", False)], shade=[0, 2], signs=["+", "−", "+"])
NL_M1 = numline([("−1", True), ("4", True)], shade=[1])
NL_A1 = numline([("3", True), ("7", False)], shade=[1])
NL_T1 = plane((-4, 5, 1), (-7, 6, 1), curves=[(lambda x: x * x - x - 6, -2.9, 3.9, BLUE, "y = f(x)")], points=[(-2, 0, "(−2, 0)"), (3, 0, "(3, 0)"), (0, -6, "(0, −6)")])

SUB = []

# ================================================================== Subbab 1
SUB.append(dict(
    title="Sifat Pertidaksamaan dan Pertidaksamaan Linear",
    tujuan="Memakai sifat-sifat pertidaksamaan untuk menyelesaikan pertidaksamaan linear satu variabel, termasuk bentuk berantai dan soal cerita, serta menyajikan penyelesaiannya pada garis bilangan.",
    konsep=[
        "<b>Pertidaksamaan</b> adalah kalimat terbuka yang memakai tanda &lt;, ≤, &gt;, atau ≥. Penyelesaiannya biasanya berupa <b>selang</b> (interval) bilangan, digambar pada garis bilangan: bulatan penuh ● bila batasnya termasuk, bulatan kosong ○ bila tidak.",
        "Menambah atau mengurangi kedua ruas dengan bilangan yang sama tidak mengubah tanda. Mengalikan atau membagi kedua ruas dengan bilangan <b>positif</b> juga tidak mengubah tanda.",
        "Mengalikan atau membagi kedua ruas dengan bilangan <b>negatif membalik tanda</b>: dari 2 &lt; 5 diperoleh −2 &gt; −5. Inilah kesalahan yang paling sering terjadi.",
        "Pertidaksamaan berantai a &lt; px + q ≤ b dikerjakan pada ketiga bagian sekaligus. Dalam soal cerita, \"paling sedikit\" berarti ≥, \"paling banyak\" berarti ≤, dan \"lebih dari\" berarti &gt;.",
    ],
    rumus=["a &lt; b ⇒ a + c &lt; b + c", "a &lt; b dan c &gt; 0 ⇒ ac &lt; bc", "a &lt; b dan c &lt; 0 ⇒ ac &gt; bc (tanda dibalik)",
           "Selang: −2 &lt; x ≤ 3 ditulis (−2, 3]; x ≥ 4 ditulis [4, ∞)"],
    contoh=[
        ("Membagi dengan bilangan negatif", "Selesaikan 3 − 2x ≤ 11 dan gambarkan penyelesaiannya.", NL_LIN,
         ["Kurangi kedua ruas dengan 3: −2x ≤ 8.", "Bagi dengan −2 dan balik tandanya: x ≥ −4.", "Uji x = 0: 3 − 0 = 3 ≤ 11. Benar, dan 0 memang termasuk x ≥ −4."], "x ≥ −4"),
        ("Pertidaksamaan berantai", "Selesaikan −1 &lt; 2x + 3 ≤ 9.", NL_CHAIN,
         ["Kurangi ketiga bagian dengan 3: −4 &lt; 2x ≤ 6.", "Bagi ketiga bagian dengan 2 (positif, tanda tetap): −2 &lt; x ≤ 3."], "−2 &lt; x ≤ 3"),
    ],
    bertahap=dict(
        soal="Selesaikan " + fr("x + 1", "2") + " − " + fr("x − 2", "3") + " &gt; 1.",
        langkah=["Kalikan semua suku dengan KPK penyebut, yaitu ____: 3(x + 1) − 2(x − 2) &gt; ____.", "3x + 3 − 2x + ____ &gt; 6 → x + 7 &gt; 6.", "x &gt; ____."],
        cek="Tanda tidak dibalik saat mengalikan dengan 6 karena",
        opsi=["(a) 6 bilangan positif", "(b) penyebutnya sudah hilang"],
        kunci="6; 6; 4; x &gt; −1. Alasan: (a).",
    ),
    jebakan=["Membagi dengan bilangan negatif membalik tanda: −3x &lt; 9 memberi x &gt; −3, bukan x &lt; −3.",
             "Saat menghilangkan penyebut, kalikan <b>semua</b> suku, termasuk ruas kanan.",
             "Perhatikan tanda minus di depan pecahan: −2(x − 2) = −2x + 4.",
             "\"Paling sedikit 80\" berarti ≥ 80; batasnya termasuk."],
    latihan=[
        Q(1, "Selesaikan x + 5 &gt; 2.", "x &gt; −3", "Kurangi 5."),
        Q(1, "Selesaikan 4x ≤ 12.", "x ≤ 3", "Bagi 4 (positif)."),
        Q(1, "Selesaikan −3x &lt; 9.", "x &gt; −3", "Bagi −3 dan balik tandanya."),
        Q(1, "Selesaikan 2x − 1 ≥ 7.", "x ≥ 4", "2x ≥ 8."),
        Q(1, "Tulis penyelesaian x ≥ −2 dalam notasi selang dan sebutkan jenis bulatan di −2.", "[−2, ∞); bulatan penuh", "Batas −2 termasuk."),
        Q(2, "Selesaikan 5 − 2x &gt; 3x − 10.", "x &lt; 3", "−5x &gt; −15 → x &lt; 3."),
        Q(2, "Selesaikan " + fr("2x − 1", "3") + " ≤ " + fr("x + 4", "2") + ".", "x ≤ 14", "Kalikan 6: 4x − 2 ≤ 3x + 12."),
        Q(2, "Berapa banyak bilangan bulat yang memenuhi −4 ≤ 3x + 2 &lt; 11?", "5", "−6 ≤ 3x &lt; 9 → −2 ≤ x &lt; 3: −2, −1, 0, 1, 2."),
        Q(2, "Nilai tiga ulangan Dina 72, 85, dan 78. Berapa nilai ulangan keempat paling sedikit agar rata-ratanya minimal 80?", "85", "72 + 85 + 78 + x ≥ 320 → x ≥ 85."),
        Q(3, "Rental A memungut Rp50.000 ditambah Rp3.000 per km; rental B Rp20.000 ditambah Rp5.000 per km. Untuk jarak berapa rental A lebih murah?", "lebih dari 15 km",
          "50.000 + 3.000x &lt; 20.000 + 5.000x → 30.000 &lt; 2.000x → x &gt; 15."),
        Q(3, "Penyelesaian 3x − a ≤ 2x + 1 adalah x ≤ 5. Tentukan a.", "a = 4", "x ≤ 1 + a, jadi 1 + a = 5."),
        Q(3, "Selesaikan 1 − x &lt; 2x + 7 ≤ x + 10.", "−2 &lt; x ≤ 3", "Pisahkan: 1 − x &lt; 2x + 7 → x &gt; −2; 2x + 7 ≤ x + 10 → x ≤ 3. Ambil irisannya."),
    ],
))

# ================================================================== Subbab 2
SUB.append(dict(
    title="Pertidaksamaan Kuadrat",
    tujuan="Menyelesaikan pertidaksamaan kuadrat dengan pembuat nol dan garis bilangan, termasuk kasus diskriminan nol atau negatif.",
    konsep=[
        "Langkah: (1) pindahkan semua suku ke satu ruas sehingga ruas lain 0; (2) cari <b>pembuat nol</b> dengan memfaktorkan; (3) letakkan pembuat nol pada garis bilangan; (4) uji tanda satu titik di setiap selang; (5) ambil selang yang tandanya sesuai.",
        "Untuk a &gt; 0 dengan akar x₁ &lt; x₂, tanda ax² + bx + c berpola + − +: bernilai negatif di antara akar dan positif di luar akar. Grafiknya parabola terbuka ke atas yang berada di bawah sumbu x hanya di antara kedua akar.",
        "Jika D = b² − 4ac &lt; 0 dan a &gt; 0, bentuk itu selalu positif (<b>definit positif</b>): ax² + bx + c &gt; 0 dipenuhi semua x, sedangkan ax² + bx + c &lt; 0 tidak mempunyai penyelesaian.",
        "Jika D = 0, bentuknya a(x − p)². Karena (x − p)² ≥ 0, pertidaksamaan (x − p)² ≤ 0 hanya dipenuhi x = p, dan (x − p)² &gt; 0 dipenuhi semua x kecuali p.",
    ],
    rumus=["a &gt; 0, akar x₁ &lt; x₂: ax² + bx + c &lt; 0 ⇔ x₁ &lt; x &lt; x₂", "a &gt; 0, akar x₁ &lt; x₂: ax² + bx + c &gt; 0 ⇔ x &lt; x₁ atau x &gt; x₂",
           "a &gt; 0 dan D &lt; 0: ax² + bx + c &gt; 0 untuk semua x", "x² &gt; k² (k &gt; 0) ⇔ x &lt; −k atau x &gt; k"],
    contoh=[
        ("Di antara akar", "Selesaikan x² − x − 6 &lt; 0.", NL_Q1,
         ["(x − 3)(x + 2) &lt; 0; pembuat nol x = −2 dan x = 3.", "Uji x = 0: (−3)(2) = −6 &lt; 0, jadi selang tengah bertanda −; selang luar bertanda +.", "Ambil selang bertanda −."], "−2 &lt; x &lt; 3"),
        ("Koefisien x² negatif", "Selesaikan −x² + 4x + 5 ≤ 0.", NL_Q2,
         ["Kalikan −1 dan balik tandanya: x² − 4x − 5 ≥ 0.", "(x − 5)(x + 1) ≥ 0; pembuat nol −1 dan 5, tanda + − +.", "Ambil selang bertanda + beserta batasnya."], "x ≤ −1 atau x ≥ 5"),
    ],
    bertahap=dict(
        soal="Selesaikan 2x² ≥ x + 3.",
        langkah=["Pindahkan ke satu ruas: 2x² − x − ____ ≥ 0.", "Faktorkan: (2x − 3)(x + ____) ≥ 0; pembuat nol x = ____ dan x = ____.", "Tanda + − +, ambil yang +: x ≤ ____ atau x ≥ ____."],
        cek="Kedua ruas tidak boleh dibagi x karena",
        opsi=["(a) tanda x tidak diketahui, dan x bisa 0", "(b) x tidak muncul di ruas kanan"],
        kunci="3; 1; 3/2 dan −1; x ≤ −1 atau x ≥ 3/2. Alasan: (a).",
    ),
    jebakan=["x² &gt; 4 bukan \"x &gt; ±2\": penyelesaiannya x &lt; −2 atau x &gt; 2.",
             "Jangan membagi pertidaksamaan dengan x; pindahkan semua suku ke satu ruas lalu faktorkan.",
             "Bila koefisien x² negatif, kalikan −1 dulu dan balik tandanya, atau ujilah tandanya dengan teliti.",
             "\"Atau\" berarti dua selang terpisah; \"−2 &lt; x &lt; 3\" berarti satu selang. Jangan menulis 3 &lt; x &lt; −2."],
    latihan=[
        Q(1, "Selesaikan (x − 1)(x − 4) &lt; 0.", "1 &lt; x &lt; 4", "Negatif di antara akar."),
        Q(1, "Selesaikan x² − 9 ≥ 0.", "x ≤ −3 atau x ≥ 3", "(x − 3)(x + 3) ≥ 0."),
        Q(1, "Selesaikan x² + 5x ≤ 0.", "−5 ≤ x ≤ 0", "x(x + 5) ≤ 0."),
        Q(1, "Selesaikan x² − 7x + 10 &gt; 0.", "x &lt; 2 atau x &gt; 5", "(x − 2)(x − 5) &gt; 0."),
        Q(1, "Selesaikan x² + 1 &gt; 0.", "semua bilangan real", "x² ≥ 0, jadi x² + 1 ≥ 1 &gt; 0."),
        Q(2, "Selesaikan x² ≤ 2x + 8.", "−2 ≤ x ≤ 4", "x² − 2x − 8 = (x − 4)(x + 2) ≤ 0."),
        Q(2, "Selesaikan −x² + x + 12 &gt; 0.", "−3 &lt; x &lt; 4", "x² − x − 12 = (x − 4)(x + 3) &lt; 0."),
        Q(2, "Selesaikan 3x² + 5x − 2 ≥ 0.", "x ≤ −2 atau x ≥ ⅓", "(3x − 1)(x + 2) ≥ 0."),
        Q(2, "Selesaikan x² − 6x + 9 ≤ 0.", "x = 3", "(x − 3)² ≤ 0 hanya dipenuhi bila x − 3 = 0."),
        Q(3, "Tentukan nilai m agar x² + mx + 9 &gt; 0 untuk setiap bilangan real x.", "−6 &lt; m &lt; 6", "a = 1 &gt; 0, jadi syaratnya D = m² − 36 &lt; 0."),
        Q(3, "Kebun persegi panjang berkeliling 40 m dan luasnya harus paling sedikit 96 m². Tentukan batas-batas panjang kebun (panjang x m).", "8 ≤ x ≤ 12",
          "Lebar 20 − x; x(20 − x) ≥ 96 → x² − 20x + 96 ≤ 0 → (x − 8)(x − 12) ≤ 0."),
        Q(3, "Tinggi bola yang dilempar ke atas h(t) = 20t − 5t² meter setelah t detik. Kapan bola berada lebih tinggi dari 15 m?", "1 &lt; t &lt; 3", "20t − 5t² &gt; 15 → t² − 4t + 3 &lt; 0 → (t − 1)(t − 3) &lt; 0."),
    ],
))

# ================================================================== Subbab 3
SUB.append(dict(
    title="Pertidaksamaan Pecahan",
    tujuan="Menyelesaikan pertidaksamaan berbentuk pecahan aljabar dengan menyatukan pecahan, mencari pembuat nol pembilang dan penyebut, dan memakai garis bilangan.",
    konsep=[
        "Pertidaksamaan pecahan memuat variabel di penyebut, misalnya " + fr("x − 2", "x + 3") + " ≤ 0. <b>Jangan mengali silang</b>, karena tanda penyebut belum diketahui: bila penyebut negatif, tanda pertidaksamaan seharusnya dibalik.",
        "Langkah: (1) pindahkan semua suku ke satu ruas; (2) satukan menjadi satu pecahan " + fr("P(x)", "Q(x)") + "; (3) cari pembuat nol pembilang dan penyebut; (4) uji tanda setiap selang; (5) ambil selang yang sesuai.",
        "Pembuat nol <b>penyebut tidak pernah termasuk</b> penyelesaian (bulatan kosong), karena pecahan tidak terdefinisi di sana. Pembuat nol pembilang termasuk bila tandanya ≤ atau ≥.",
        "Penyebut yang selalu positif, seperti x² + 1, tidak mengubah tanda pecahan, sehingga boleh diabaikan. Faktor yang sama di pembilang dan penyebut boleh dicoret, tetapi nilai x yang membuatnya nol tetap dikeluarkan.",
    ],
    rumus=[fr("P", "Q") + " ≥ 0 ⇔ P · Q ≥ 0 dan Q ≠ 0", fr("P", "Q") + " &gt; k → " + fr("P − kQ", "Q") + " &gt; 0 (jangan kali silang)", "Pembuat nol penyebut: selalu bulatan kosong ○"],
    contoh=[
        ("Bentuk dasar", "Selesaikan " + fr("x − 2", "x + 3") + " ≤ 0.", NL_R1,
         ["Pembuat nol pembilang x = 2 (termasuk, karena ≤); pembuat nol penyebut x = −3 (tidak termasuk).", "Uji x = 0: (−2) : 3 &lt; 0, jadi selang tengah bertanda −; pola + − +.", "Ambil selang bertanda −."], "−3 &lt; x ≤ 2"),
        ("Ruas kanan bukan nol", "Selesaikan " + fr("2x + 1", "x − 1") + " &gt; 1.", NL_R2,
         [fr("2x + 1", "x − 1") + " − 1 &gt; 0 → " + fr("2x + 1 − (x − 1)", "x − 1") + " &gt; 0 → " + fr("x + 2", "x − 1") + " &gt; 0.", "Pembuat nol −2 dan 1; uji x = 0: 2 : (−1) &lt; 0, pola + − +.", "Ambil selang bertanda +."],
         "x &lt; −2 atau x &gt; 1"),
    ],
    bertahap=dict(
        soal="Selesaikan " + fr("x + 4", "x − 2") + " ≥ 3.",
        langkah=[fr("x + 4", "x − 2") + " − 3 ≥ 0 → " + fr("x + 4 − 3x + ____", "x − 2") + " ≥ 0 → " + fr("−2x + 10", "x − 2") + " ≥ 0.",
                 "Kalikan −1 (tanda dibalik): " + fr("x − 5", "x − 2") + " ____ 0.", "Pembuat nol 2 dan 5, pola + − +; penyelesaian: ____ &lt; x ≤ ____."],
        cek="Batas x = 2 memakai bulatan kosong karena",
        opsi=["(a) x = 2 membuat penyebut nol", "(b) tanda pertidaksamaannya ≥"],
        kunci="6; ≤; 2 &lt; x ≤ 5. Alasan: (a).",
    ),
    jebakan=["Mengali silang " + fr("2x + 1", "x − 1") + " &gt; 1 menjadi 2x + 1 &gt; x − 1 memberi x &gt; −2, yang salah untuk −2 &lt; x &lt; 1.",
             "Pembuat nol penyebut selalu bulatan kosong, walaupun tandanya ≤ atau ≥.",
             "Saat menyatukan pecahan, kurung seluruh bentuk yang dikurangkan: 2x + 1 − (x − 1) = x + 2."],
    latihan=[
        Q(1, "Selesaikan " + fr("x − 1", "x + 2") + " &gt; 0.", "x &lt; −2 atau x &gt; 1", "Pola + − + dengan batas −2 dan 1."),
        Q(1, "Selesaikan " + fr("x + 3", "x − 4") + " ≤ 0.", "−3 ≤ x &lt; 4", "x = 4 membuat penyebut nol."),
        Q(1, "Selesaikan " + fr("1", "x − 5") + " &lt; 0.", "x &lt; 5", "Pembilang positif, jadi penyebut harus negatif."),
        Q(1, "Selesaikan " + fr("x", "x + 1") + " ≥ 0.", "x &lt; −1 atau x ≥ 0", "Batas 0 termasuk, −1 tidak."),
        Q(1, "Mengapa x = 4 tidak termasuk penyelesaian " + fr("x + 3", "x − 4") + " ≥ 0?", "karena penyebutnya nol", "Pembagian dengan nol tidak terdefinisi."),
        Q(2, "Selesaikan " + fr("x + 1", "x − 3") + " &lt; 2.", "x &lt; 3 atau x &gt; 7", fr("x + 1 − 2x + 6", "x − 3") + " = " + fr("7 − x", "x − 3") + " &lt; 0 → " + fr("x − 7", "x − 3") + " &gt; 0."),
        Q(2, "Selesaikan " + fr("3x − 2", "x + 1") + " ≥ 2.", "x &lt; −1 atau x ≥ 4", fr("3x − 2 − 2x − 2", "x + 1") + " = " + fr("x − 4", "x + 1") + " ≥ 0."),
        Q(2, "Selesaikan " + fr("x² − 4", "x − 1") + " ≤ 0.", "x ≤ −2 atau 1 &lt; x ≤ 2", "Pembuat nol −2, 1, 2; pola − + − +; ambil selang bertanda −."),
        Q(2, "Selesaikan " + fr("x − 3", "x² + 1") + " ≥ 0.", "x ≥ 3", "x² + 1 selalu positif, jadi cukup x − 3 ≥ 0."),
        Q(3, "Selesaikan " + fr("2", "x − 1") + " &gt; " + fr("1", "x + 2") + ".", "−5 &lt; x &lt; −2 atau x &gt; 1",
          fr("2(x + 2) − (x − 1)", "(x − 1)(x + 2)") + " = " + fr("x + 5", "(x − 1)(x + 2)") + " &gt; 0; pembuat nol −5, −2, 1; pola − + − +."),
        Q(3, "Selesaikan " + fr("x² − x − 6", "x² + x − 2") + " ≥ 0.", "x &lt; −2 atau −2 &lt; x &lt; 1 atau x ≥ 3",
          fr("(x − 3)(x + 2)", "(x − 1)(x + 2)") + " = " + fr("x − 3", "x − 1") + " untuk x ≠ −2; " + fr("x − 3", "x − 1") + " ≥ 0 → x &lt; 1 atau x ≥ 3, lalu keluarkan x = −2."),
        Q(3, "Biaya rata-rata per unit untuk membuat x unit barang adalah " + fr("5.000x + 200.000", "x") + " rupiah. Paling sedikit berapa unit harus dibuat agar biaya rata-ratanya tidak lebih dari Rp9.000?", "50 unit",
          "x &gt; 0, jadi kedua ruas boleh dikali x: 5.000x + 200.000 ≤ 9.000x → x ≥ 50."),
    ],
))

# ================================================================== Subbab 4
SUB.append(dict(
    title="Pertidaksamaan Nilai Mutlak",
    tujuan="Menyelesaikan pertidaksamaan nilai mutlak dengan sifat jarak dan dengan mengkuadratkan kedua ruas, serta memakainya untuk masalah toleransi.",
    konsep=[
        "|x| adalah jarak x ke 0 pada garis bilangan, dan |x − a| adalah jarak x ke a. Jadi |x − 2| &lt; 3 berarti \"x berjarak kurang dari 3 dari 2\", yaitu −1 &lt; x &lt; 5.",
        "Untuk c &gt; 0: |u| &lt; c ⇔ −c &lt; u &lt; c (satu selang), dan |u| &gt; c ⇔ u &lt; −c atau u &gt; c (dua selang). Hal yang sama berlaku untuk ≤ dan ≥.",
        "Jika c &lt; 0, |u| &lt; c tidak mempunyai penyelesaian, sedangkan |u| &gt; c dipenuhi semua x, karena nilai mutlak tidak pernah negatif.",
        "Jika kedua ruas memuat nilai mutlak, kuadratkan kedua ruas (keduanya tidak negatif): |u| ≤ |v| ⇔ u² ≤ v² ⇔ (u − v)(u + v) ≤ 0.",
    ],
    rumus=["|u| ≤ c (c ≥ 0) ⇔ −c ≤ u ≤ c", "|u| ≥ c (c ≥ 0) ⇔ u ≤ −c atau u ≥ c", "|u| ≤ |v| ⇔ (u − v)(u + v) ≤ 0", "|u| &lt; c dengan c &lt; 0: tidak ada penyelesaian"],
    contoh=[
        ("Satu selang", "Selesaikan |2x − 3| ≤ 5.", NL_M1,
         ["−5 ≤ 2x − 3 ≤ 5.", "Tambah 3: −2 ≤ 2x ≤ 8; bagi 2: −1 ≤ x ≤ 4.", "Uji x = 4: |8 − 3| = 5 ≤ 5. Benar."], "−1 ≤ x ≤ 4"),
        ("Mutlak di kedua ruas", "Selesaikan |x + 1| &gt; |x − 3|.", None,
         ["Kuadratkan: (x + 1)² &gt; (x − 3)² ⇔ ((x + 1) − (x − 3))((x + 1) + (x − 3)) &gt; 0.", "4(2x − 2) &gt; 0 → x &gt; 1.",
          "Arti jarak: x lebih jauh dari −1 daripada dari 3, yaitu berada di kanan titik tengahnya, 1."], "x &gt; 1"),
    ],
    bertahap=dict(
        soal="Selesaikan |3 − x| ≥ 2.",
        langkah=["Pecah menjadi dua: 3 − x ≤ ____ atau 3 − x ≥ ____.", "3 − x ≤ −2 → −x ≤ −5 → x ≥ ____.", "3 − x ≥ 2 → −x ≥ −1 → x ≤ ____. Penyelesaian: x ≤ ____ atau x ≥ ____."],
        cek="Bentuk |u| ≥ c dipecah menjadi dua selang karena",
        opsi=["(a) u harus berjarak paling sedikit c dari 0, ke kiri atau ke kanan", "(b) nilai mutlak selalu menghasilkan dua jawaban"],
        kunci="−2; 2; 5; 1; x ≤ 1 atau x ≥ 5. Alasan: (a).",
    ),
    jebakan=["|u| &gt; c tidak boleh ditulis −c &gt; u &gt; c; tulis dua selang: u &lt; −c atau u &gt; c.",
             "Pada |3 − x|, membagi dengan −1 membalik tanda; atau tulis dulu |3 − x| = |x − 3|.",
             "|2x + 1| &lt; −3 tidak mempunyai penyelesaian; jangan langsung memakai rumus −c &lt; u &lt; c.",
             "Mengkuadratkan hanya sah bila kedua ruas tidak negatif, misalnya dua nilai mutlak."],
    latihan=[
        Q(1, "Selesaikan |x| &lt; 4.", "−4 &lt; x &lt; 4", "Jarak ke 0 kurang dari 4."),
        Q(1, "Selesaikan |x| ≥ 3.", "x ≤ −3 atau x ≥ 3", "Jarak ke 0 paling sedikit 3."),
        Q(1, "Selesaikan |x − 2| &lt; 3.", "−1 &lt; x &lt; 5", "−3 &lt; x − 2 &lt; 3."),
        Q(1, "Selesaikan |x + 5| ≤ 0.", "x = −5", "Nilai mutlak tidak negatif, jadi harus |x + 5| = 0."),
        Q(1, "Selesaikan |2x + 1| &lt; −3.", "tidak ada penyelesaian", "Nilai mutlak tidak pernah negatif."),
        Q(2, "Selesaikan |3x − 6| &gt; 9.", "x &lt; −1 atau x &gt; 5", "3x − 6 &lt; −9 atau 3x − 6 &gt; 9."),
        Q(2, "Selesaikan |5 − 2x| ≤ 7.", "−1 ≤ x ≤ 6", "−7 ≤ 5 − 2x ≤ 7 → −12 ≤ −2x ≤ 2 → 6 ≥ x ≥ −1."),
        Q(2, "Selesaikan |x − 1| ≤ |x + 3|.", "x ≥ −1", "(x − 1 − x − 3)(x − 1 + x + 3) ≤ 0 → −4(2x + 2) ≤ 0 → x ≥ −1."),
        Q(2, "Berat bersih kemasan gula ditetapkan 500 g dengan toleransi 8 g. Tulis syarat berat w dengan nilai mutlak, lalu selesaikan.", "|w − 500| ≤ 8; 492 ≤ w ≤ 508", "−8 ≤ w − 500 ≤ 8."),
        Q(3, "Selesaikan 1 &lt; |x − 2| ≤ 4.", "−2 ≤ x &lt; 1 atau 3 &lt; x ≤ 6", "|x − 2| ≤ 4 → −2 ≤ x ≤ 6; |x − 2| &gt; 1 → x &lt; 1 atau x &gt; 3; ambil irisannya."),
        Q(3, "Selesaikan |2x − 1| &lt; x + 3.", "−⅔ &lt; x &lt; 4", "−(x + 3) &lt; 2x − 1 &lt; x + 3: dari kiri x &gt; −⅔, dari kanan x &lt; 4. Ruas kanan positif pada selang itu."),
        Q(3, "Suhu ruang server harus memenuhi |T − 22| ≤ 3 (T dalam °C). Dengan F = 1,8T + 32, tentukan batas suhunya dalam °F.", "66,2 ≤ F ≤ 77", "19 ≤ T ≤ 25; 1,8 · 19 + 32 = 66,2 dan 1,8 · 25 + 32 = 77."),
    ],
))

# ================================================================== Subbab 5
SUB.append(dict(
    title="Pertidaksamaan Bentuk Akar",
    tujuan="Menyelesaikan pertidaksamaan yang memuat bentuk akar dengan memperhatikan syarat akar dan mengkuadratkan kedua ruas secara sah.",
    konsep=[
        "√u hanya terdefinisi bila u ≥ 0. Syarat ini (<b>syarat akar</b>) selalu ikut menentukan penyelesaian.",
        "Kedua ruas boleh dikuadratkan bila keduanya tidak negatif. √u &lt; √v ⇔ u ≥ 0 dan u &lt; v. √u &lt; c (c &gt; 0) ⇔ 0 ≤ u &lt; c². √u &gt; c (c ≥ 0) ⇔ u &gt; c².",
        "Jika ruas kanan negatif, jawabannya langsung: √u &gt; c dengan c &lt; 0 dipenuhi semua x yang memenuhi syarat akar, sedangkan √u &lt; c dengan c ≤ 0 tidak mempunyai penyelesaian.",
        "Penyelesaian akhir adalah <b>irisan</b> syarat akar dan hasil setelah dikuadratkan. Jika ruas kanan memuat x, pisahkan kasus menurut tanda ruas kanan.",
    ],
    rumus=["Syarat: √u terdefinisi ⇔ u ≥ 0", "√u &lt; √v ⇔ u ≥ 0 dan u &lt; v", "√u &lt; c (c &gt; 0) ⇔ 0 ≤ u &lt; c²", "√u &gt; c (c ≥ 0) ⇔ u &gt; c²"],
    contoh=[
        ("Akar kurang dari bilangan", "Selesaikan √(x − 3) &lt; 2.", NL_A1,
         ["Syarat akar: x − 3 ≥ 0 → x ≥ 3.", "Kuadratkan (kedua ruas tidak negatif): x − 3 &lt; 4 → x &lt; 7.", "Irisan: 3 ≤ x &lt; 7."], "3 ≤ x &lt; 7"),
        ("Akar di kedua ruas", "Selesaikan √(2x + 1) ≥ √(x + 4).", None,
         ["Syarat: 2x + 1 ≥ 0 → x ≥ −½ dan x + 4 ≥ 0 → x ≥ −4.", "Kuadratkan: 2x + 1 ≥ x + 4 → x ≥ 3.", "Irisan dengan syarat: x ≥ 3."], "x ≥ 3"),
    ],
    bertahap=dict(
        soal="Selesaikan √(6 − x) ≤ √(x + 2).",
        langkah=["Syarat akar: 6 − x ≥ 0 → x ≤ ____, dan x + 2 ≥ 0 → x ≥ ____.", "Kuadratkan: 6 − x ≤ x + 2 → x ≥ ____.", "Irisan: ____ ≤ x ≤ ____."],
        cek="Kedua ruas boleh dikuadratkan karena",
        opsi=["(a) keduanya bentuk akar, jadi tidak negatif", "(b) setiap pertidaksamaan boleh dikuadratkan"],
        kunci="6; −2; 2; 2 ≤ x ≤ 6. Alasan: (a).",
    ),
    jebakan=["Jangan lupa syarat akar: √(x − 3) &lt; 2 bukan hanya x &lt; 7, karena x = 0 membuat akarnya tidak terdefinisi.",
             "Mengkuadratkan dengan ruas negatif bisa salah: −3 &lt; 2, tetapi 9 &gt; 4.",
             "√16 = 4, bukan ±4; nilai akar tidak pernah negatif.",
             "Penyelesaian akhir adalah irisan, bukan gabungan, syarat akar dan hasil kuadrat."],
    latihan=[
        Q(1, "Selesaikan √x &lt; 3.", "0 ≤ x &lt; 9", "Syarat x ≥ 0; x &lt; 9."),
        Q(1, "Selesaikan √(x − 1) ≥ 2.", "x ≥ 5", "x − 1 ≥ 4; syarat x ≥ 1 sudah termuat."),
        Q(1, "Tentukan syarat agar √(4 − 2x) terdefinisi.", "x ≤ 2", "4 − 2x ≥ 0."),
        Q(1, "Selesaikan √(x + 2) &gt; −1.", "x ≥ −2", "Akar tidak negatif, jadi selalu &gt; −1; cukup syarat akar."),
        Q(1, "Selesaikan √(x + 3) &lt; 0.", "tidak ada penyelesaian", "Nilai akar tidak pernah negatif."),
        Q(2, "Selesaikan √(2x − 4) ≤ 4.", "2 ≤ x ≤ 10", "Syarat x ≥ 2; 2x − 4 ≤ 16 → x ≤ 10."),
        Q(2, "Selesaikan √(3x + 1) &gt; √(x + 5).", "x &gt; 2", "Syarat x ≥ −⅓; 3x + 1 &gt; x + 5 → x &gt; 2."),
        Q(2, "Selesaikan √(x² − 9) &lt; 4.", "−5 &lt; x ≤ −3 atau 3 ≤ x &lt; 5", "Syarat x² ≥ 9 → x ≤ −3 atau x ≥ 3; x² − 9 &lt; 16 → −5 &lt; x &lt; 5."),
        Q(2, "Berapa banyak bilangan asli yang memenuhi √(10 − x) ≥ 2?", "6", "10 − x ≥ 4 → x ≤ 6; bilangan asli 1 sampai 6."),
        Q(3, "Selesaikan √(x + 6) &gt; x.", "−6 ≤ x &lt; 3",
          "Kasus x &lt; 0 (dengan syarat x ≥ −6): ruas kiri ≥ 0 &gt; x, selalu benar. Kasus x ≥ 0: x + 6 &gt; x² → (x − 3)(x + 2) &lt; 0 → 0 ≤ x &lt; 3. Gabungkan."),
        Q(3, "Dengan model sederhana T = 2√L, periode ayunan T (detik) bergantung pada panjang tali L (meter). Tentukan panjang tali agar 2 ≤ T ≤ 3.", "1 ≤ L ≤ 2,25",
          "1 ≤ √L ≤ 1,5; kuadratkan (semua ruas positif)."),
        Q(3, "Selesaikan √(x² − 2x) ≤ √(x + 4).", "−1 ≤ x ≤ 0 atau 2 ≤ x ≤ 4",
          "Syarat x² − 2x ≥ 0 → x ≤ 0 atau x ≥ 2, dan x ≥ −4. Kuadratkan: x² − 3x − 4 ≤ 0 → −1 ≤ x ≤ 4. Ambil irisannya."),
    ],
))

CAMPURAN = [
    Q(1, "Selesaikan −2x + 7 ≥ 1.", "x ≤ 3", "−2x ≥ −6; tanda dibalik."),
    Q(1, "Selesaikan x² &lt; 16.", "−4 &lt; x &lt; 4", "(x − 4)(x + 4) &lt; 0."),
    Q(1, "Selesaikan |x + 2| ≥ 5.", "x ≤ −7 atau x ≥ 3", "x + 2 ≤ −5 atau x + 2 ≥ 5."),
    Q(2, "Selesaikan " + fr("x − 5", "x + 1") + " ≥ 0.", "x &lt; −1 atau x ≥ 5", "Pola + − +; −1 tidak termasuk."),
    Q(2, "Selesaikan 2x² − 5x − 3 &lt; 0.", "−½ &lt; x &lt; 3", "(2x + 1)(x − 3) &lt; 0."),
    Q(2, "Selesaikan √(5 − x) &lt; 3.", "−4 &lt; x ≤ 5", "Syarat x ≤ 5; 5 − x &lt; 9 → x &gt; −4."),
    Q(2, "Berapa banyak bilangan bulat yang memenuhi x² − 3x − 10 ≤ 0?", "8", "(x − 5)(x + 2) ≤ 0 → −2 ≤ x ≤ 5."),
    Q(2, "Tarif parkir Rp5.000 untuk jam pertama dan Rp3.000 untuk setiap jam berikutnya. Dengan uang Rp30.000, paling lama berapa jam seseorang dapat parkir?", "9 jam",
      "5.000 + 3.000(n − 1) ≤ 30.000 → n − 1 ≤ 8⅓; n bulat, jadi n ≤ 9."),
    Q(3, "Seorang siswa membagi kedua ruas x² &gt; 4x dengan x dan memperoleh x &gt; 4. Jelaskan kesalahannya dan tentukan penyelesaian yang benar.", "x &lt; 0 atau x &gt; 4",
      "Tanda x tidak diketahui (untuk x &lt; 0 tanda harus dibalik). x² − 4x = x(x − 4) &gt; 0."),
    Q(3, "Tentukan nilai k agar kx² − 4x + k &lt; 0 untuk setiap bilangan real x.", "k &lt; −2", "Perlu k &lt; 0 dan D = 16 − 4k² &lt; 0 → k² &gt; 4; digabung: k &lt; −2."),
]

TKA = [
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Grafik fungsi kuadrat y = f(x) ditunjukkan berikut. Grafik memotong sumbu x di (−2, 0) dan (3, 0).", fig=NL_T1,
         soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["f(x) &lt; 0 untuk −2 &lt; x &lt; 3", "f(0) &gt; 0", "f(4) &gt; 0", "penyelesaian f(x) ≥ 0 adalah x ≤ −2 atau x ≥ 3", "f(x) = 0 hanya untuk satu nilai x"], kunci=[0, 2, 3],
         bahas="Grafik berada di bawah sumbu x di antara −2 dan 3, dan di atasnya di luar selang itu. f(−2) = f(3) = 0, jadi batasnya termasuk pada f(x) ≥ 0.",
         salah="B: f(0) = −6 &lt; 0. E: f(x) = 0 untuk x = −2 dan x = 3."),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Himpunan penyelesaian " + fr("x − 1", "x + 3") + " ≤ 2 adalah ....",
         opsi=["x ≤ −7 atau x &gt; −3", "x ≥ −7", "x ≤ −7 atau x ≥ −3", "−7 ≤ x &lt; −3", "x ≤ −7"], kunci=0,
         bahas=fr("x − 1 − 2x − 6", "x + 3") + " = " + fr("−x − 7", "x + 3") + " ≤ 0 → " + fr("x + 7", "x + 3") + " ≥ 0; pembuat nol −7 dan −3, pola + − +.",
         salah="B: mengali silang (x − 1 ≤ 2x + 6). C: pembuat nol penyebut ikut termasuk. D: tanda tidak dibalik saat mengalikan −1. E: selang kanan terlupa."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Penyelesaian x² + bx + c &lt; 0 adalah −1 &lt; x &lt; 4. Nilai b + c adalah ....",
         opsi=["−7", "−1", "1", "7", "−3"], kunci=0,
         bahas="x² + bx + c = (x + 1)(x − 4) = x² − 3x − 4, jadi b = −3, c = −4, dan b + c = −7.",
         salah="B: tanda b salah (b = 3). C: tanda c salah (c = 4). D: kedua tanda salah. E: hanya b."),
    dict(tipe="MAT-MODEL", lv=2, fmt="pg", soal="Panjang sebuah kebun persegi panjang 4 m lebih dari lebarnya, dan luasnya tidak lebih dari 60 m². Batas-batas lebar kebun l (dalam meter) adalah ....",
         opsi=["0 &lt; l ≤ 6", "−10 ≤ l ≤ 6", "0 &lt; l ≤ 10", "l ≥ 6", "0 &lt; l &lt; 6"], kunci=0,
         bahas="l(l + 4) ≤ 60 → l² + 4l − 60 ≤ 0 → (l + 10)(l − 6) ≤ 0 → −10 ≤ l ≤ 6; lebar harus positif, jadi 0 &lt; l ≤ 6.",
         salah="B: lebar negatif ikut diterima. C: tanda akar tertukar. D: tanda pertidaksamaan dibalik. E: batas 6 tidak dimasukkan, padahal \"tidak lebih dari\" berarti ≤."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Keuntungan harian sebuah warung dimodelkan P(x) = −x² + 40x − 300 (ribu rupiah), dengan x banyak porsi terjual. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["Warung untung (P &gt; 0) bila 10 &lt; x &lt; 30.", "Menjual 35 porsi membuat warung rugi.", "Keuntungan paling sedikit Rp75.000 dicapai bila 15 ≤ x ≤ 25.", "Keuntungan maksimum dicapai saat x = 40."], kunci=[True, True, True, False],
         bahas="P &gt; 0 ⇔ x² − 40x + 300 = (x − 10)(x − 30) &lt; 0. P(35) = −125 &lt; 0. P ≥ 75 ⇔ (x − 15)(x − 25) ≤ 0. Puncak di x = 40 : 2 = 20.", salah=""),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pgk", soal="Nilai x yang memenuhi |2x − 5| &lt; 3 adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["2", "1", "3,5", "4", "1,5"], kunci=[0, 2, 4],
         bahas="−3 &lt; 2x − 5 &lt; 3 → 1 &lt; x &lt; 4. Nilai 2, 3,5, dan 1,5 terletak di dalam selang itu.",
         salah="B, D: x = 1 dan x = 4 adalah batas yang tidak termasuk (|2x − 5| = 3)."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Diketahui x² − 2mx + m + 6 &gt; 0 untuk setiap bilangan real x. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["m = 0 memenuhi.", "m = 3 memenuhi.", "Syaratnya −2 &lt; m &lt; 3.", "m = −1 memenuhi."], kunci=[True, False, True, True],
         bahas="Syarat D = 4m² − 4(m + 6) &lt; 0 → m² − m − 6 &lt; 0 → −2 &lt; m &lt; 3. Untuk m = 3, bentuknya (x − 3)², yang bernilai 0 saat x = 3.", salah=""),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg",
         soal="Sebuah pusat kebugaran menawarkan tiga paket bulanan. Paket A: iuran Rp150.000 ditambah Rp5.000 per kunjungan. Paket B: Rp20.000 per kunjungan tanpa iuran. Paket C: Rp250.000 untuk kunjungan tanpa batas. Paket A paling murah di antara ketiganya bila banyak kunjungan dalam sebulan ....",
         opsi=["11 sampai 19 kali", "10 sampai 20 kali", "lebih dari 10 kali", "kurang dari 20 kali", "11 sampai 20 kali"], kunci=0,
         bahas="A &lt; B: 150.000 + 5.000n &lt; 20.000n → n &gt; 10. A &lt; C: 150.000 + 5.000n &lt; 250.000 → n &lt; 20. Untuk n bulat: 11 ≤ n ≤ 19.",
         salah="B: pada n = 10 biaya A sama dengan B, dan pada n = 20 sama dengan C, jadi A tidak paling murah. C: paket C diabaikan. D: paket B diabaikan. E: pada n = 20 biaya A sama dengan C."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Diketahui a &lt; b &lt; 0. Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["a² &gt; b²", fr("1", "a") + " &gt; " + fr("1", "b"), "ab &gt; 0", "a + b &gt; 0", "−a &lt; −b"], kunci=[0, 1, 2],
         bahas="a &lt; b &lt; 0 berarti |a| &gt; |b|, jadi a² &gt; b². Membagi a &lt; b dengan ab &gt; 0: 1/b &lt; 1/a. Hasil kali dua bilangan negatif positif.",
         salah="D: jumlah dua bilangan negatif negatif. E: mengalikan dengan −1 membalik tanda, jadi −a &gt; −b."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Penyelesaian |x − a| ≤ 3 adalah −1 ≤ x ≤ 5. Nilai a adalah ....",
         opsi=["2", "−2", "3", "4", "6"], kunci=0,
         bahas="a − 3 ≤ x ≤ a + 3, jadi a − 3 = −1 dan a + 3 = 5: a = 2 (titik tengah selang).",
         salah="B: tanda a salah. C: nilai toleransi, bukan titik tengah. D: selisih 5 − 1. E: panjang selang."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Penyelesaian 3 − 4x &gt; 15 adalah ....", ["x &lt; −3", "x &gt; −3", "x &lt; 3", "x &gt; 3", "x &lt; −" + fr("9", "2")], 0, "−4x &gt; 12 → x &lt; −3.",
     "B: tanda tidak dibalik. C: tanda bilangan salah. D: dua kesalahan sekaligus. E: 3 ditambahkan, bukan dikurangkan."),
    ("Penyelesaian −2 &lt; 2x + 4 ≤ 10 adalah ....", ["−3 &lt; x ≤ 3", "−3 ≤ x ≤ 3", "−3 ≤ x &lt; 3", "−6 &lt; x ≤ 6", "1 &lt; x ≤ 7"], 0, "−6 &lt; 2x ≤ 6.",
     "B: batas kiri ikut termasuk. C: jenis batas tertukar. D: lupa membagi 2. E: 4 ditambahkan, bukan dikurangkan."),
    ("Penyelesaian x² − 5x + 6 ≤ 0 adalah ....", ["2 ≤ x ≤ 3", "x ≤ 2 atau x ≥ 3", "−3 ≤ x ≤ −2", "2 &lt; x &lt; 3", "x ≤ −3 atau x ≥ −2"], 0, "(x − 2)(x − 3) ≤ 0.",
     "B: selang luar dipilih. C: tanda akar salah. D: batas tidak dimasukkan. E: tanda akar dan selang salah."),
    ("Penyelesaian x² &gt; 9 adalah ....", ["x &lt; −3 atau x &gt; 3", "x &gt; 3", "−3 &lt; x &lt; 3", "x ≤ −3 atau x ≥ 3", "x &gt; 4,5"], 0, "(x − 3)(x + 3) &gt; 0.",
     "B: akar negatif terlupa. C: selang tengah dipilih. D: batas ikut termasuk. E: 9 dibagi 2, bukan diakarkan."),
    ("Penyelesaian −x² + 2x + 8 ≥ 0 adalah ....", ["−2 ≤ x ≤ 4", "x ≤ −2 atau x ≥ 4", "−4 ≤ x ≤ 2", "x ≤ −4 atau x ≥ 2", "−2 &lt; x &lt; 4"], 0, "x² − 2x − 8 = (x − 4)(x + 2) ≤ 0.",
     "B: tanda tidak dibalik saat mengalikan −1. C: tanda akar salah. D: dua kesalahan sekaligus. E: batas tidak dimasukkan."),
    ("Penyelesaian " + fr("x + 2", "x − 5") + " &lt; 0 adalah ....", ["−2 &lt; x &lt; 5", "x &lt; −2 atau x &gt; 5", "−5 &lt; x &lt; 2", "−2 ≤ x &lt; 5", "−2 ≤ x ≤ 5"], 0, "Pola + − +.",
     "B: selang luar dipilih. C: tanda pembuat nol salah. D: batas −2 dimasukkan padahal tanda &lt;. E: pembuat nol penyebut ikut dimasukkan."),
    ("Penyelesaian " + fr("2x − 1", "x + 2") + " ≥ 1 adalah ....", ["x &lt; −2 atau x ≥ 3", "x ≥ 3", "x ≤ −2 atau x ≥ 3", "−2 &lt; x ≤ 3", "x ≥ ½"], 0, fr("x − 3", "x + 2") + " ≥ 0.",
     "B: mengali silang. C: pembuat nol penyebut ikut termasuk. D: selang yang tandanya salah. E: hanya pembilang yang diperiksa."),
    ("Penyelesaian |x − 3| &lt; 5 adalah ....", ["−2 &lt; x &lt; 8", "x &lt; −2 atau x &gt; 8", "−8 &lt; x &lt; 2", "x &lt; 8", "−5 &lt; x &lt; 5"], 0, "−5 &lt; x − 3 &lt; 5.",
     "B: rumus |u| &gt; c dipakai. C: tanda 3 salah. D: hanya satu sisi. E: 3 diabaikan."),
    ("Penyelesaian |2x + 3| ≥ 7 adalah ....", ["x ≤ −5 atau x ≥ 2", "−5 ≤ x ≤ 2", "x ≥ 2", "x ≤ −2 atau x ≥ 5", "x ≥ −5"], 0, "2x + 3 ≤ −7 atau 2x + 3 ≥ 7.",
     "B: rumus |u| ≤ c dipakai. C: hanya satu sisi. D: tanda 3 salah. E: kedua sisi digabung menjadi −7 ≤ 2x + 3."),
    ("Penyelesaian √(x − 2) &lt; 3 adalah ....", ["2 ≤ x &lt; 11", "x &lt; 11", "x &lt; 5", "2 ≤ x &lt; 5", "−7 &lt; x &lt; 11"], 0, "Syarat x ≥ 2; x − 2 &lt; 9.",
     "B: syarat akar terlupa. C: tidak dikuadratkan. D: tidak dikuadratkan, tetapi syarat diingat. E: diperlakukan seperti |x − 2| &lt; 9."),
    ("Banyak bilangan bulat yang memenuhi x² − 2x − 15 &lt; 0 adalah ....", ["7", "9", "8", "6", "5"], 0, "(x − 5)(x + 3) &lt; 0 → −3 &lt; x &lt; 5: −2 sampai 4.",
     "B: kedua batas ikut dihitung. C: satu batas ikut dihitung. D: 0 tidak dihitung. E: hanya 0 sampai 4."),
    ("Agar x² − 4x + m &gt; 0 untuk setiap x real, nilai m haruslah ....", ["m &gt; 4", "m &lt; 4", "m ≥ 4", "m &gt; 16", "m &gt; 2"], 0, "D = 16 − 4m &lt; 0.",
     "B: tanda D dibalik. C: m = 4 memberi (x − 2)², yang bernilai 0 di x = 2. D: lupa faktor 4 pada 4ac. E: memakai b = −2."),
    ("Biaya tetap produksi Rp600.000 dan biaya Rp2.500 per unit; setiap unit dijual Rp4.000. Paling sedikit berapa unit harus terjual agar untung?", ["401", "400", "150", "240", "93"], 0,
     "4.000x &gt; 600.000 + 2.500x → x &gt; 400.", "B: pada 400 unit belum untung, baru impas. C: biaya per unit diabaikan. D: harga jual diabaikan. E: kedua harga dijumlahkan."),
    ("Penyelesaian " + fr("(x − 1)(x + 2)", "x − 4") + " ≥ 0 adalah ....", ["−2 ≤ x ≤ 1 atau x &gt; 4", "−2 ≤ x ≤ 1 atau x ≥ 4", "x ≤ −2 atau 1 ≤ x &lt; 4", "x &gt; 4", "−2 ≤ x ≤ 1"], 0,
     "Pembuat nol −2, 1, 4; pola − + − +.", "B: pembuat nol penyebut ikut termasuk. C: selang yang tandanya salah. D: selang tengah terlupa. E: selang kanan terlupa."),
    ("Penyelesaian |x − 1| &gt; |x + 3| adalah ....", ["x &lt; −1", "x &gt; −1", "x &lt; −3", "x &lt; 1", "−3 &lt; x &lt; 1"], 0,
     "(x − 1 − x − 3)(x − 1 + x + 3) &gt; 0 → −4(2x + 2) &gt; 0 → x &lt; −1.",
     "B: tanda −4 diabaikan. C: hanya titik −3 dipakai sebagai batas. D: hanya titik 1 dipakai sebagai batas. E: daerah di antara kedua titik."),
]
UJI_URAIAN = [
    ("Selesaikan " + fr("x − 2", "3") + " − " + fr("2x + 1", "4") + " ≤ 1, lalu gambarkan penyelesaiannya pada garis bilangan.", "x ≥ −" + fr("23", "2"),
     "Kalikan 12: 4x − 8 − 6x − 3 ≤ 12 → −2x ≤ 23 → x ≥ −23/2 (bulatan penuh di −11½)."),
    ("Selesaikan 2x² + x − 6 &gt; 0 dan tuliskan penyelesaiannya dalam notasi selang.", "x &lt; −2 atau x &gt; " + fr("3", "2") + "; (−∞, −2) ∪ (3/2, ∞)", "(2x − 3)(x + 2) &gt; 0; pola + − +."),
    ("Selesaikan " + fr("x² − 1", "x + 3") + " ≤ 0 dengan garis bilangan.", "x &lt; −3 atau −1 ≤ x ≤ 1", "Pembuat nol −3 (penyebut), −1, 1; uji x = −4, −2, 0, 2: tanda − + − +."),
    ("Selesaikan |x − 4| ≤ 2x − 2. Periksa jawabanmu dengan x = 2 dan x = 1,9.", "x ≥ 2",
     "−(2x − 2) ≤ x − 4 ≤ 2x − 2: kanan x ≥ −2; kiri 3x ≥ 6 → x ≥ 2. Cek: |−2| = 2 ≤ 2 benar; |−2,1| = 2,1 ≤ 1,8 salah."),
    ("Tinggi sebuah proyektil h(t) = 30t − 5t² meter setelah t detik. (a) Kapan tingginya paling sedikit 25 m? (b) Berapa lama proyektil berada pada ketinggian itu atau lebih? (c) Kapan proyektil kembali ke tanah? (d) Apakah proyektil pernah mencapai 50 m?",
     "(a) 1 ≤ t ≤ 5; (b) 4 detik; (c) t = 6; (d) tidak",
     "(a) t² − 6t + 5 ≤ 0 → (t − 1)(t − 5) ≤ 0. (c) 5t(6 − t) = 0. (d) t² − 6t + 10 ≤ 0 mempunyai D = 36 − 40 &lt; 0, jadi tidak pernah; tinggi maksimum h(3) = 45 m."),
]

META = dict(
    title="Modul Pertidaksamaan", kick="Modul belajar Matematika · Fase E · Kelas X", big="Pertidaksamaan",
    subtitle="Pertidaksamaan linear, kuadrat, pecahan, nilai mutlak, dan bentuk akar dengan garis bilangan",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat memakai sifat-sifat pertidaksamaan untuk menyelesaikan pertidaksamaan linear, kuadrat, pecahan, nilai mutlak, dan bentuk akar dalam satu variabel; menyajikan penyelesaiannya pada garis bilangan dan dalam notasi selang; serta memodelkan masalah sehari-hari dengan pertidaksamaan, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Satu cara untuk semua jenis</h2><table><tr><th>Langkah</th><th>Contoh: " + fr("x + 2", "x − 1") + " &gt; 0</th></tr>"
               "<tr><td>1. Jadikan satu ruas bernilai 0</td><td>sudah</td></tr><tr><td>2. Cari pembuat nol</td><td>x = −2 (pembilang), x = 1 (penyebut)</td></tr>"
               "<tr><td>3. Uji tanda tiap selang</td><td>+ − +</td></tr><tr><td>4. Ambil selang yang sesuai</td><td>x &lt; −2 atau x &gt; 1</td></tr></table>"
               '<div class="fig">' + NL_R2 + "</div>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit</b> tanpa kalkulator. Uji jawabanmu dengan satu bilangan di dalam penyelesaian dan satu di luarnya.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Pada garis bilangan, ● berarti batas termasuk dan ○ berarti tidak termasuk; garis bilangan tidak digambar berskala. Tanda + dan − di atas garis menunjukkan tanda bentuk aljabar pada selang itu. Desimal ditulis dengan koma, ribuan dengan titik.",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>linear, kuadrat, pecahan, nilai mutlak, atau bentuk akar?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025 (specs/tka-templates/matematika.md).",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-MODEL, MAT-FUNGSI): mengenali, menghitung, bekerja mundur, memodelkan, atau menafsirkan fungsi. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Mengapa membagi dengan bilangan negatif membalik tanda pertidaksamaan?", "Mengapa pertidaksamaan pecahan tidak boleh dikali silang?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Sifat</th><td>tambah/kurang: tanda tetap; kali/bagi positif: tetap; kali/bagi negatif: tanda dibalik</td></tr>"
        "<tr><th>Kuadrat</th><td>pembuat nol, garis bilangan, uji tanda; a &gt; 0: negatif di antara akar, positif di luar akar</td></tr>"
        "<tr><th>Definit</th><td>a &gt; 0 dan D &lt; 0: selalu positif; a &lt; 0 dan D &lt; 0: selalu negatif</td></tr>"
        "<tr><th>Pecahan</th><td>satu ruas 0, satukan pecahan, pembuat nol pembilang dan penyebut; penyebut selalu ○; jangan kali silang</td></tr>"
        "<tr><th>Nilai mutlak</th><td>|u| ≤ c ⇔ −c ≤ u ≤ c; |u| ≥ c ⇔ u ≤ −c atau u ≥ c; |u| ≤ |v| ⇔ (u − v)(u + v) ≤ 0</td></tr>"
        "<tr><th>Bentuk akar</th><td>syarat u ≥ 0; kuadratkan bila kedua ruas tidak negatif; jawaban = irisan</td></tr></table>"
        "<h2>Pola tanda bentuk kuadrat (a &gt; 0)</h2>" + '<div class="fig">' + NL_Q1 + "</div>"),
    jebakan5=["Membagi atau mengalikan dengan bilangan negatif membalik tanda.", "x² &gt; 4 berarti x &lt; −2 atau x &gt; 2, bukan x &gt; ±2.",
              "Jangan mengali silang pertidaksamaan pecahan; pembuat nol penyebut selalu bulatan kosong.", "|u| &gt; c memberi dua selang terpisah.",
              "Pada bentuk akar, syarat akar ikut menentukan penyelesaian."],
    guru=["Pertidaksamaan linear satu variabel termasuk capaian Fase D (SMP) dan diulang di Subbab 1. Pertidaksamaan kuadrat sejalan dengan fungsi kuadrat di Fase E (simpul FUN-01 pada peta Matematika).",
          "Pertidaksamaan pecahan, nilai mutlak, dan bentuk akar (Subbab 3–5) tidak disebut secara eksplisit dalam CP Fase E; bagian ini dapat dipakai sebagai pengayaan atau persiapan tes. Urutan dan cakupan bab dapat berbeda antarsekolah.",
          "Pertidaksamaan linear dua variabel dan program linear dibahas di modul Program Linear.",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


# ------------------------------------------------------------------ check
def _grid(extra=()):
    """Exact test points: every eighth from −20 to 20, plus extra points (critical values)."""
    pts = {F(k, 8) for k in range(-160, 161)}
    for e in extra:
        e = F(e)
        pts |= {e, e - F(1, 1000), e + F(1, 1000)}
    return sorted(pts)


def _sqrt_cmp(u, op, c):
    """Exact truth of √u op c for rational u, c (False when u < 0, as √u is undefined)."""
    if u < 0:
        return False
    if op in ("<", "<="):
        if c < 0:
            return False
        return u < c * c if op == "<" else u <= c * c
    if c < 0:
        return True
    return u > c * c if op == ">" else u >= c * c


def _same(pred, sol, extra=()):
    for x in _grid(extra):
        try:
            p = pred(x)
        except ZeroDivisionError:
            p = False
        if p != sol(x):
            raise AssertionError((x, p, sol(x)))
    return True


def check():
    S = _same
    # prasyarat
    assert -2 * -3 - 4 == 2 and all(x * x - x - 6 == (x - 3) * (x + 2) for x in range(-5, 6)) and all(x * x - 4 * x - 5 == 0 for x in (-1, 5))
    assert 2 * 0 - 6 == -6 and 2 * 5 - 6 == 4 and abs(-7) == 7 and abs(3 - 8) == 5
    assert all(F(x + 1, x - 2) - 1 == F(3, x - 2) for x in range(-5, 6) if x != 2)
    # subbab 1
    assert S(lambda x: 3 - 2 * x <= 11, lambda x: x >= -4, [-4])
    assert S(lambda x: -1 < 2 * x + 3 <= 9, lambda x: -2 < x <= 3, [-2, 3])
    assert S(lambda x: (x + 1) / 2 - (x - 2) / 3 > 1, lambda x: x > -1, [-1])
    assert S(lambda x: x + 5 > 2, lambda x: x > -3, [-3]) and S(lambda x: 4 * x <= 12, lambda x: x <= 3, [3])
    assert S(lambda x: -3 * x < 9, lambda x: x > -3, [-3]) and S(lambda x: 2 * x - 1 >= 7, lambda x: x >= 4, [4])
    assert S(lambda x: 5 - 2 * x > 3 * x - 10, lambda x: x < 3, [3]) and S(lambda x: (2 * x - 1) / 3 <= (x + 4) / 2, lambda x: x <= 14, [14])
    assert [x for x in range(-10, 10) if -4 <= 3 * x + 2 < 11] == [-2, -1, 0, 1, 2]
    assert 4 * 80 - (72 + 85 + 78) == 85
    assert S(lambda x: 50000 + 3000 * x < 20000 + 5000 * x, lambda x: x > 15, [15])
    assert S(lambda x: 3 * x - 4 <= 2 * x + 1, lambda x: x <= 5, [5])
    assert S(lambda x: 1 - x < 2 * x + 7 <= x + 10, lambda x: -2 < x <= 3, [-2, 3])
    # subbab 2
    assert S(lambda x: x * x - x - 6 < 0, lambda x: -2 < x < 3, [-2, 3])
    assert S(lambda x: -x * x + 4 * x + 5 <= 0, lambda x: x <= -1 or x >= 5, [-1, 5])
    assert S(lambda x: 2 * x * x >= x + 3, lambda x: x <= -1 or x >= F(3, 2), [-1, F(3, 2)])
    assert S(lambda x: (x - 1) * (x - 4) < 0, lambda x: 1 < x < 4, [1, 4]) and S(lambda x: x * x - 9 >= 0, lambda x: x <= -3 or x >= 3, [-3, 3])
    assert S(lambda x: x * x + 5 * x <= 0, lambda x: -5 <= x <= 0, [-5, 0]) and S(lambda x: x * x - 7 * x + 10 > 0, lambda x: x < 2 or x > 5, [2, 5])
    assert S(lambda x: x * x + 1 > 0, lambda x: True)
    assert S(lambda x: x * x <= 2 * x + 8, lambda x: -2 <= x <= 4, [-2, 4]) and S(lambda x: -x * x + x + 12 > 0, lambda x: -3 < x < 4, [-3, 4])
    assert S(lambda x: 3 * x * x + 5 * x - 2 >= 0, lambda x: x <= -2 or x >= F(1, 3), [-2, F(1, 3)]) and S(lambda x: x * x - 6 * x + 9 <= 0, lambda x: x == 3, [3])
    for m in [F(k, 4) for k in range(-40, 41)]:
        assert all(x * x + m * x + 9 > 0 for x in _grid([-m / 2])) == (-6 < m < 6)
    assert S(lambda x: 0 < x < 20 and x * (20 - x) >= 96, lambda x: 8 <= x <= 12, [8, 12])
    assert S(lambda t: 20 * t - 5 * t * t > 15, lambda t: 1 < t < 3, [1, 3])
    # subbab 3
    assert S(lambda x: (x - 2) / (x + 3) <= 0, lambda x: -3 < x <= 2, [-3, 2])
    assert S(lambda x: (2 * x + 1) / (x - 1) > 1, lambda x: x < -2 or x > 1, [-2, 1])
    assert S(lambda x: (x + 4) / (x - 2) >= 3, lambda x: 2 < x <= 5, [2, 5])
    assert 2 * 0 + 1 > 0 - 1 and not (2 * 0 + 1) / F(0 - 1) > 1  # cross-multiplying wrongly accepts x = 0
    assert S(lambda x: (x - 1) / (x + 2) > 0, lambda x: x < -2 or x > 1, [-2, 1]) and S(lambda x: (x + 3) / (x - 4) <= 0, lambda x: -3 <= x < 4, [-3, 4])
    assert S(lambda x: 1 / (x - 5) < 0, lambda x: x < 5, [5]) and S(lambda x: x / (x + 1) >= 0, lambda x: x < -1 or x >= 0, [-1, 0])
    assert S(lambda x: (x + 1) / (x - 3) < 2, lambda x: x < 3 or x > 7, [3, 7]) and S(lambda x: (3 * x - 2) / (x + 1) >= 2, lambda x: x < -1 or x >= 4, [-1, 4])
    assert S(lambda x: (x * x - 4) / (x - 1) <= 0, lambda x: x <= -2 or 1 < x <= 2, [-2, 1, 2]) and S(lambda x: (x - 3) / (x * x + 1) >= 0, lambda x: x >= 3, [3])
    assert S(lambda x: 2 / (x - 1) > 1 / (x + 2), lambda x: -5 < x < -2 or x > 1, [-5, -2, 1])
    assert S(lambda x: (x * x - x - 6) / (x * x + x - 2) >= 0, lambda x: x < -2 or -2 < x < 1 or x >= 3, [-2, 1, 3])
    assert S(lambda x: x > 0 and (5000 * x + 200000) / x <= 9000, lambda x: x >= 50, [50])
    # subbab 4
    assert S(lambda x: abs(2 * x - 3) <= 5, lambda x: -1 <= x <= 4, [-1, 4]) and S(lambda x: abs(x + 1) > abs(x - 3), lambda x: x > 1, [1])
    assert S(lambda x: abs(3 - x) >= 2, lambda x: x <= 1 or x >= 5, [1, 5])
    assert S(lambda x: abs(x) < 4, lambda x: -4 < x < 4, [-4, 4]) and S(lambda x: abs(x) >= 3, lambda x: x <= -3 or x >= 3, [-3, 3])
    assert S(lambda x: abs(x - 2) < 3, lambda x: -1 < x < 5, [-1, 5]) and S(lambda x: abs(x + 5) <= 0, lambda x: x == -5, [-5]) and S(lambda x: abs(2 * x + 1) < -3, lambda x: False)
    assert S(lambda x: abs(3 * x - 6) > 9, lambda x: x < -1 or x > 5, [-1, 5]) and S(lambda x: abs(5 - 2 * x) <= 7, lambda x: -1 <= x <= 6, [-1, 6])
    assert S(lambda x: abs(x - 1) <= abs(x + 3), lambda x: x >= -1, [-1])
    assert all((abs(w - 500) <= 8) == (492 <= w <= 508) for w in range(480, 521))
    assert S(lambda x: 1 < abs(x - 2) <= 4, lambda x: -2 <= x < 1 or 3 < x <= 6, [-2, 1, 3, 6])
    assert S(lambda x: abs(2 * x - 1) < x + 3, lambda x: F(-2, 3) < x < 4, [F(-2, 3), 4])
    assert F(9, 5) * 19 + 32 == F(331, 5) == F(662, 10) and F(9, 5) * 25 + 32 == 77
    # subbab 5
    assert S(lambda x: _sqrt_cmp(x - 3, "<", 2), lambda x: 3 <= x < 7, [3, 7])
    assert S(lambda x: x >= F(-1, 2) and x >= -4 and 2 * x + 1 >= x + 4, lambda x: x >= 3, [3])
    assert S(lambda x: 6 - x >= 0 and x + 2 >= 0 and 6 - x <= x + 2, lambda x: 2 <= x <= 6, [-2, 2, 6])
    assert S(lambda x: _sqrt_cmp(x, "<", 3), lambda x: 0 <= x < 9, [0, 9]) and S(lambda x: _sqrt_cmp(x - 1, ">=", 2), lambda x: x >= 5, [1, 5])
    assert S(lambda x: 4 - 2 * x >= 0, lambda x: x <= 2, [2]) and S(lambda x: _sqrt_cmp(x + 2, ">", -1), lambda x: x >= -2, [-2])
    assert S(lambda x: _sqrt_cmp(x + 3, "<", 0), lambda x: False, [-3])
    assert S(lambda x: _sqrt_cmp(2 * x - 4, "<=", 4), lambda x: 2 <= x <= 10, [2, 10])
    assert S(lambda x: 3 * x + 1 >= 0 and x + 5 >= 0 and 3 * x + 1 > x + 5, lambda x: x > 2, [F(-1, 3), 2])
    assert S(lambda x: _sqrt_cmp(x * x - 9, "<", 4), lambda x: -5 < x <= -3 or 3 <= x < 5, [-5, -3, 3, 5])
    assert [x for x in range(1, 20) if _sqrt_cmp(10 - x, ">=", 2)] == [1, 2, 3, 4, 5, 6]
    assert S(lambda x: _sqrt_cmp(x + 6, ">", x), lambda x: -6 <= x < 3, [-6, 0, 3])
    assert all((_sqrt_cmp(L, ">=", 1) and _sqrt_cmp(L, "<=", F(3, 2))) == (1 <= L <= F(9, 4)) for L in _grid([1, F(9, 4)]))
    assert S(lambda x: x * x - 2 * x >= 0 and x + 4 >= 0 and x * x - 2 * x <= x + 4, lambda x: -1 <= x <= 0 or 2 <= x <= 4, [-4, -1, 0, 2, 4])
    # campuran
    assert S(lambda x: -2 * x + 7 >= 1, lambda x: x <= 3, [3]) and S(lambda x: x * x < 16, lambda x: -4 < x < 4, [-4, 4])
    assert S(lambda x: abs(x + 2) >= 5, lambda x: x <= -7 or x >= 3, [-7, 3]) and S(lambda x: (x - 5) / (x + 1) >= 0, lambda x: x < -1 or x >= 5, [-1, 5])
    assert S(lambda x: 2 * x * x - 5 * x - 3 < 0, lambda x: F(-1, 2) < x < 3, [F(-1, 2), 3]) and S(lambda x: _sqrt_cmp(5 - x, "<", 3), lambda x: -4 < x <= 5, [-4, 5])
    assert len([x for x in range(-20, 20) if x * x - 3 * x - 10 <= 0]) == 8
    assert max(n for n in range(1, 50) if 5000 + 3000 * (n - 1) <= 30000) == 9
    assert S(lambda x: x * x > 4 * x, lambda x: x < 0 or x > 4, [0, 4])
    for k in [F(j, 4) for j in range(-40, 41)]:
        assert all(k * x * x - 4 * x + k < 0 for x in _grid([2 / k] if k else [])) == (k < -2)
    # TKA
    assert S(lambda x: x * x - x - 6 < 0, lambda x: -2 < x < 3, [-2, 3]) and 0 * 0 - 0 - 6 == -6 and 16 - 4 - 6 > 0
    assert S(lambda x: (x - 1) / (x + 3) <= 2, lambda x: x <= -7 or x > -3, [-7, -3])
    assert all((x + 1) * (x - 4) == x * x - 3 * x - 4 for x in range(-5, 6)) and -3 + -4 == -7
    assert S(lambda l: l > 0 and l * (l + 4) <= 60, lambda l: 0 < l <= 6, [0, 6])
    P = lambda x: -x * x + 40 * x - 300  # noqa: E731
    assert S(lambda x: P(x) > 0, lambda x: 10 < x < 30, [10, 30]) and P(35) == -125 and S(lambda x: P(x) >= 75, lambda x: 15 <= x <= 25, [15, 25]) and max(range(0, 41), key=P) == 20
    assert [abs(2 * x - 5) < 3 for x in (2, 1, F(7, 2), 4, F(3, 2))] == [True, False, True, False, True]
    D = lambda m: 4 * m * m - 4 * (m + 6)  # noqa: E731
    assert D(0) < 0 and D(3) == 0 and D(-1) < 0 and all((D(m) < 0) == (-2 < m < 3) for m in _grid([-2, 3]))
    cost = lambda n: (150000 + 5000 * n, 20000 * n, 250000)  # noqa: E731
    assert [n for n in range(0, 40) if cost(n)[0] < min(cost(n)[1:])] == list(range(11, 20)) and cost(10)[0] == cost(10)[1] and cost(20)[0] == cost(20)[2]
    for a, b in [(-3, -1), (F(-5, 2), F(-1, 3)), (-10, -9)]:
        assert a * a > b * b and 1 / F(a) > 1 / F(b) and a * b > 0 and a + b < 0 and -a > -b
    assert S(lambda x: abs(x - 2) <= 3, lambda x: -1 <= x <= 5, [-1, 5])
    # uji
    assert S(lambda x: 3 - 4 * x > 15, lambda x: x < -3, [-3]) and S(lambda x: -2 < 2 * x + 4 <= 10, lambda x: -3 < x <= 3, [-3, 3])
    assert S(lambda x: x * x - 5 * x + 6 <= 0, lambda x: 2 <= x <= 3, [2, 3]) and S(lambda x: x * x > 9, lambda x: x < -3 or x > 3, [-3, 3])
    assert S(lambda x: -x * x + 2 * x + 8 >= 0, lambda x: -2 <= x <= 4, [-2, 4]) and S(lambda x: (x + 2) / (x - 5) < 0, lambda x: -2 < x < 5, [-2, 5])
    assert S(lambda x: (2 * x - 1) / (x + 2) >= 1, lambda x: x < -2 or x >= 3, [-2, 3]) and S(lambda x: abs(x - 3) < 5, lambda x: -2 < x < 8, [-2, 8])
    assert S(lambda x: abs(2 * x + 3) >= 7, lambda x: x <= -5 or x >= 2, [-5, 2]) and S(lambda x: _sqrt_cmp(x - 2, "<", 3), lambda x: 2 <= x < 11, [2, 11])
    assert len([x for x in range(-20, 20) if x * x - 2 * x - 15 < 0]) == 7 and len(range(-3, 6)) == 9
    assert all((all(x * x - 4 * x + m > 0 for x in _grid([2]))) == (m > 4) for m in [F(k, 4) for k in range(0, 40)])
    assert min(x for x in range(0, 1000) if 4000 * x > 600000 + 2500 * x) == 401 and 4000 * 400 == 600000 + 2500 * 400
    assert 600000 // 4000 == 150 and 600000 // 2500 == 240 and -(-600000 // 6500) == 93
    assert S(lambda x: (x - 1) * (x + 2) / (x - 4) >= 0, lambda x: -2 <= x <= 1 or x > 4, [-2, 1, 4])
    assert S(lambda x: abs(x - 1) > abs(x + 3), lambda x: x < -1, [-1])
    # uraian
    assert S(lambda x: (x - 2) / 3 - (2 * x + 1) / 4 <= 1, lambda x: x >= F(-23, 2), [F(-23, 2)])
    assert S(lambda x: 2 * x * x + x - 6 > 0, lambda x: x < -2 or x > F(3, 2), [-2, F(3, 2)])
    assert S(lambda x: (x * x - 1) / (x + 3) <= 0, lambda x: x < -3 or -1 <= x <= 1, [-3, -1, 1])
    assert S(lambda x: abs(x - 4) <= 2 * x - 2, lambda x: x >= 2, [2]) and abs(F(19, 10) - 4) > 2 * F(19, 10) - 2
    h = lambda t: 30 * t - 5 * t * t  # noqa: E731
    assert S(lambda t: h(t) >= 25, lambda t: 1 <= t <= 5, [1, 5]) and h(6) == 0 and max(h(F(k, 8)) for k in range(0, 49)) == 45 == h(3)
    return True
