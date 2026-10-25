"""Content of the printable module "Fungsi Linear dan Persamaan Garis" (Matematika kelas X).

Lines are written as y = mx + c or ax + by + c = 0; a line through two points has gradient Δy/Δx.
Every numeric answer is re-derived in check() with exact fractions.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import plane  # noqa: E402
from kit import fr, Q, close  # noqa: E402

BLUE, RED, GREEN = "#1f3a68", "#c0502a", "#2e6b32"

PRASYARAT = [
    ("P1", "Hitung −3 − (−7) dan (−2) · (−5).", "4 dan 10", "−3 + 7 = 4; negatif kali negatif positif."),
    ("P2", "Hitung (5 − (−1)) : (2 − 4).", "−3", "6 : (−2)."),
    ("P3", "Hitung ⅔ · (−9/4).", "−3/2", "−18/12 = −3/2."),
    ("P4", "Bilangan berapa yang jika dikalikan dengan −⅔ hasilnya 1?", "−3/2", "Kebalikan −⅔ adalah −3/2; tandanya tetap."),
    ("P5", "Selesaikan 3x − 5 = 10.", "x = 5", "3x = 15."),
    ("P6", "Jika y = 2x − 3, tentukan y saat x = −1.", "y = −5", "2 · (−1) − 3."),
    ("P7", "Ubah 2x + 3y = 6 ke bentuk y = ....", "y = −⅔x + 2", "3y = −2x + 6, lalu semua suku dibagi 3."),
    ("P8", "Di kuadran berapa letak titik A(2, −3) dan B(−1, 4)?", "A di kuadran IV, B di kuadran II", "A: x positif, y negatif; B: x negatif, y positif."),
]

INGAT = [
    ("A", "Bilangan bulat dan pecahan", "P1–P4", "Subbab 2, 5", ["a − (−b) = a + b; hasil bagi dua bilangan berbeda tanda adalah negatif.",
                                                              "Kebalikan p/q adalah q/p; tandanya tidak berubah."]),
    ("B", "Persamaan linear satu variabel", "P5, P6", "Subbab 1, 3, 4", ["Pindahkan suku ke ruas lain dengan mengganti tandanya, lalu bagi dengan koefisien x.", "Substitusi: ganti x dengan bilangannya, pakai tanda kurung bila negatif."]),
    ("C", "Mengubah bentuk persamaan", "P7", "Subbab 2–5", ["Sisakan suku y di satu ruas, lalu bagi <b>semua</b> suku dengan koefisien y."]),
    ("D", "Bidang koordinat", "P8", "Subbab 1–3", ["Titik (x, y); kuadran I (+, +), II (−, +), III (−, −), IV (+, −)."]),
]

# Figures. Every marked point and every line in a figure passes through grid points.
FIG_F1 = plane((-2, 4, 1), (-6, 4, 1), curves=[(lambda x: 2 * x - 4, -1, 4, BLUE, "y = 2x − 4")], points=[(0, -4, "(0, −4)"), (2, 0, "(2, 0)")])
FIG_L1 = plane((-2, 4, 1), (-3, 6, 1), curves=[(lambda x: 2 * x - 1, -1, 3.5, BLUE, "")], points=[(0, -1, "(0, −1)"), (2, 3, "(2, 3)")])
BLANK_G = plane((-1, 6, 1), (-1, 7, 1))
KEY_G = plane((-1, 6, 1), (-1, 7, 1), curves=[(lambda x: (12 - 3 * x) / 2, -0.5, 5, BLUE, "")], points=[(4, 0, "(4, 0)"), (0, 6, "(0, 6)")])
FIG_L2 = plane((-4, 4, 1), (-3, 5, 1), curves=[(lambda x: 2 * x / 3 + 1, -4, 4, BLUE, "")], points=[(-3, -1, "(−3, −1)"), (3, 3, "(3, 3)")])
FIG_L3 = plane((-4, 3, 1), (-2, 6, 1), curves=[(lambda x: 1.5 * x + 3, -3.3, 2, BLUE, "")], points=[(-2, 0, "(−2, 0)"), (0, 3, "(0, 3)")])
FIG_TEMU = plane((-2, 5, 1), (-1, 7, 1), curves=[(lambda x: x + 1, -2, 5, BLUE, "y = x + 1"), (lambda x: -2 * x + 7, 4, 0, RED, "y = −2x + 7")], points=[(2, 3, "(2, 3)")])
FIG_L4 = plane((-2, 6, 1), (-1, 6, 1), curves=[(lambda x: -x + 4, -2, 5, BLUE, "g"), (lambda x: x / 2 + 1, -2, 6, RED, "h")])
FIG_SEJ = plane((-2, 5, 1), (-6, 8, 2), curves=[(lambda x: 2 * x - 3, -1.5, 5, BLUE, "y = 2x − 3"), (lambda x: 2 * x + 2, -2, 3, GREEN, "y = 2x + 2"),
                                               (lambda x: -x / 2 + 4.5, -2, 5, RED, "")], points=[(1, 4, "(1, 4)")], labels=[(3.3, 1.2, "y = −½x + 4½", RED)])
FIG_T1 = plane((-4, 4, 1), (-4, 5, 1), curves=[(lambda x: x + 2, -4, 3, BLUE, "g"), (lambda x: x - 1, -3, 4, GREEN, "h"), (lambda x: -x + 1, -3.5, 4, RED, "k")])

SUB = []

# ================================================================== Subbab 1
SUB.append(dict(
    title="Fungsi Linear dan Grafiknya",
    tujuan="Menyatakan fungsi linear dalam rumus, tabel, dan grafik, serta menafsirkan m dan c dalam konteks.",
    konsep=[
        "<b>Fungsi linear</b> adalah fungsi berbentuk f(x) = mx + c dengan m dan c bilangan real. Grafiknya berupa garis lurus, sehingga cukup dua titik untuk menggambarnya.",
        "Konstanta c = f(0) adalah nilai fungsi saat x = 0; grafik memotong <b>sumbu y</b> di (0, c). Grafik memotong <b>sumbu x</b> saat f(x) = 0, yaitu di x = −c/m (bila m ≠ 0).",
        "Setiap kali x bertambah 1, nilai f(x) berubah sebesar m. Dalam soal cerita, m adalah <b>laju perubahan</b> (misalnya rupiah per km) dan c adalah <b>nilai awal</b> (misalnya biaya tetap).",
        "Bila m = 0, f(x) = c disebut fungsi konstan dan grafiknya garis mendatar. Garis tegak x = k bukan grafik fungsi, karena satu nilai x dipasangkan dengan banyak nilai y.",
    ],
    rumus=["f(x) = mx + c; f(0) = c", "Potong sumbu y: (0, c); potong sumbu x: (−" + fr("c", "m") + ", 0), m ≠ 0", "f(x + 1) − f(x) = m"],
    contoh=[
        ("Menggambar grafik", "Gambarkan grafik f(x) = 2x − 4 dengan memakai titik potong kedua sumbu.", FIG_F1,
         ["Potong sumbu y: f(0) = −4, jadi (0, −4).", "Potong sumbu x: 2x − 4 = 0 → x = 2, jadi (2, 0).", "Tarik garis lurus melalui kedua titik. Cek dengan titik ketiga: f(3) = 2, dan (3, 2) memang terletak pada garis."],
         "garis melalui (0, −4) dan (2, 0)"),
        ("Tarif taksi", "Tarif taksi terdiri atas Rp7.000 saat naik ditambah Rp4.500 per km. Tulis biaya f(x) untuk x km, hitung biaya 12 km, dan tentukan jarak bila penumpang membayar Rp52.000.", None,
         ["Biaya tetap c = 7.000 dan laju m = 4.500 per km: f(x) = 4.500x + 7.000.", "f(12) = 54.000 + 7.000 = 61.000.", "4.500x + 7.000 = 52.000 → 4.500x = 45.000 → x = 10."],
         "f(x) = 4.500x + 7.000; Rp61.000; 10 km"),
    ],
    bertahap=dict(
        soal="Fungsi linear f memenuhi f(0) = 5 dan f(2) = 11. Tentukan rumus f(x) dan nilai f(−3).",
        langkah=["c = f(0) = ____.", "f(2) = 2m + 5 = 11, jadi m = ____.", "f(x) = ____, sehingga f(−3) = ____."],
        cek="Nilai c langsung diketahui karena",
        opsi=["(a) c = f(0)", "(b) c = f(1)"],
        kunci="c = 5; m = 3; f(x) = 3x + 5; f(−3) = −4. Alasan: (a).",
    ),
    jebakan=["Untuk y = 2x − 4, titik potong sumbu x adalah (2, 0), bukan (−4, 0); −4 adalah potongan sumbu y.",
             "Pada f(x) = 5 − 3x, gradiennya −3 dan c = 5: urutan penulisan suku tidak mengubah peran m dan c.",
             "Cek grafik dengan satu titik ketiga; dua titik yang salah hitung tetap menghasilkan garis lurus."],
    latihan=[
        Q(1, "Diketahui f(x) = 3x − 2. Hitung f(4) dan f(−1).", "10 dan −5", "12 − 2; −3 − 2."),
        Q(1, "Tentukan titik potong grafik y = −2x + 6 dengan sumbu y.", "(0, 6)", "x = 0 memberi y = 6."),
        Q(1, "Tentukan titik potong grafik y = −2x + 6 dengan sumbu x.", "(3, 0)", "−2x + 6 = 0 → x = 3."),
        Q(1, "Manakah yang merupakan fungsi linear: f(x) = 4 − x, g(x) = x² + 1, h(x) = " + fr("2", "x") + "?", "f saja", "f berbentuk mx + c dengan m = −1, c = 4; g memuat x², h memuat x di penyebut."),
        Q(1, "Apakah titik (2, 7) terletak pada garis y = 3x + 1?", "ya", "3 · 2 + 1 = 7."),
        Q(2, "Fungsi linear f memenuhi f(1) = 4 dan f(3) = 10. Tentukan f(x).", "f(x) = 3x + 1", "m = (10 − 4) : (3 − 1) = 3; 3 · 1 + c = 4 → c = 1."),
        Q(2, "Gambarlah grafik 3x + 2y = 12 pada bidang berikut dengan menentukan titik potong kedua sumbu.", "melalui (4, 0) dan (0, 6)", "y = 0 → x = 4; x = 0 → y = 6.", fig=BLANK_G, kfig=KEY_G),
        Q(2, "Lilin yang panjangnya 24 cm memendek 1,5 cm setiap jam. Tulis panjangnya P(t) setelah t jam, lalu tentukan kapan lilin habis.", "P(t) = 24 − 1,5t; setelah 16 jam", "Nilai awal 24, laju −1,5; 24 − 1,5t = 0 → t = 16."),
        Q(2, "Grafik fungsi linear di bawah melalui dua titik yang ditandai. Tentukan rumus fungsinya.", "f(x) = 2x − 1", "c = −1; dari (0, −1) ke (2, 3), y naik 4 saat x naik 2, jadi m = 2.", fig=FIG_L1),
        Q(3, "Biaya membuat x kue adalah B(x) = 2.500x + 150.000 rupiah, dan setiap kue dijual Rp4.000. Paling sedikit berapa kue harus terjual agar tidak rugi?", "100 kue", "4.000x ≥ 2.500x + 150.000 → 1.500x ≥ 150.000 → x ≥ 100."),
        Q(3, "Suhu air mula-mula 20 °C. Ketika dipanaskan, suhunya dianggap naik secara linear dan mencapai 65 °C setelah 9 menit. Tentukan suhu setelah 4 menit dan kapan suhunya mencapai 100 °C.", "40 °C; menit ke-16",
          "m = (65 − 20) : 9 = 5 °C per menit; T(t) = 5t + 20; T(4) = 40; 5t + 20 = 100 → t = 16."),
        Q(3, "Fungsi linear f memenuhi f(x + 2) − f(x) = 6 untuk setiap x, dan f(0) = −1. Tentukan f(5).", "14", "m(x + 2) − mx = 2m = 6 → m = 3; f(x) = 3x − 1; f(5) = 14."),
    ],
))

# ================================================================== Subbab 2
SUB.append(dict(
    title="Gradien Garis",
    tujuan="Menentukan gradien garis dari dua titik, dari persamaannya, dan dari grafiknya, serta menafsirkan tanda dan besarnya.",
    konsep=[
        "<b>Gradien</b> (kemiringan) m adalah perbandingan perubahan y terhadap perubahan x antara dua titik pada garis: m = Δy/Δx. Pada garis lurus, nilai ini sama untuk setiap pasang titik.",
        "m &gt; 0: garis naik dari kiri ke kanan; m &lt; 0: garis turun; m = 0: garis mendatar (y = k). Garis tegak x = k tidak mempunyai gradien, karena Δx = 0. Makin besar |m|, makin curam garisnya.",
        "Dari persamaan: pada y = mx + c gradiennya langsung m. Pada ax + by + c = 0 (b ≠ 0), ubah ke y = −" + fr("a", "b") + "x − " + fr("c", "b") + ", jadi m = −" + fr("a", "b") + ".",
        "Tiga titik <b>segaris</b> (kolinear) bila gradien setiap pasang titiknya sama.",
    ],
    rumus=["m = " + fr("y₂ − y₁", "x₂ − x₁") + " (x₁ ≠ x₂)", "y = mx + c → gradien m", "ax + by + c = 0 → m = −" + fr("a", "b"), "Garis y = k: m = 0; garis x = k: gradien tidak terdefinisi"],
    contoh=[
        ("Dari dua titik", "Tentukan gradien garis yang melalui A(−1, 5) dan B(3, −3).", None,
         ["Δy = −3 − 5 = −8; Δx = 3 − (−1) = 4.", "m = −8 : 4 = −2. Gradien negatif, jadi garis turun."], "m = −2"),
        ("Dari persamaan", "Tentukan gradien garis 4x − 6y + 9 = 0.", None,
         ["−6y = −4x − 9 → y = " + fr("2", "3") + "x + " + fr("3", "2") + ".", "Cek dengan rumus: m = −a/b = −4 : (−6) = " + fr("2", "3") + "."], "m = ⅔"),
    ],
    bertahap=dict(
        soal="Titik P(2, k) terletak pada garis yang melalui A(−1, 1) dan B(1, 5). Tentukan k.",
        langkah=["m<sub>AB</sub> = (5 − 1) : (1 − (−1)) = ____.", "Gradien AP harus sama: (k − 1) : (2 − (−1)) = ____.", "Jadi k − 1 = ____ dan k = ____."],
        cek="Gradien AP disamakan dengan gradien AB karena",
        opsi=["(a) tiga titik segaris mempunyai gradien yang sama untuk setiap pasang titik", "(b) jarak AP sama dengan jarak AB"],
        kunci="m<sub>AB</sub> = 2; (k − 1) : 3 = 2; k − 1 = 6, k = 7. Alasan: (a).",
    ),
    jebakan=["Urutan titik di pembilang dan penyebut harus sama: (y₂ − y₁) : (x₂ − x₁). Menulis (y₂ − y₁) : (x₁ − x₂) membalik tandanya.",
             "Gradien adalah Δy : Δx, bukan Δx : Δy.",
             "Gradien 2x + 3y = 6 adalah −⅔, bukan 2 atau ⅔. Jika ragu, ubah dulu ke bentuk y = mx + c.",
             "Garis y = 4 bergradien 0; garis x = 4 tidak mempunyai gradien."],
    latihan=[
        Q(1, "Tentukan gradien garis yang melalui (1, 2) dan (4, 11).", "3", "9 : 3."),
        Q(1, "Tentukan gradien garis yang melalui (−2, 3) dan (2, 1).", "−½", "(1 − 3) : (2 + 2) = −2 : 4."),
        Q(1, "Tentukan gradien garis y = −4x + 7.", "−4", "Koefisien x pada bentuk y = mx + c."),
        Q(1, "Tentukan gradien garis 3x + y − 5 = 0.", "−3", "y = −3x + 5."),
        Q(1, "Tentukan gradien garis y = 6 dan garis x = −2.", "0; tidak terdefinisi", "y = 6 mendatar; x = −2 tegak (Δx = 0)."),
        Q(2, "Tentukan gradien garis 2x − 5y = 10.", "⅖", "−5y = −2x + 10 → y = ⅖x − 2."),
        Q(2, "Tentukan gradien garis pada grafik berikut.", "⅔", "Dari (−3, −1) ke (3, 3): Δy = 4, Δx = 6.", fig=FIG_L2),
        Q(2, "Garis yang melalui (a, 3) dan (2, −5) bergradien 4. Tentukan a.", "a = 4", "(−5 − 3) : (2 − a) = 4 → −8 = 8 − 4a → a = 4."),
        Q(2, "Urutkan dari yang paling landai sampai yang paling curam: y = 3x, y = −5x + 1, y = ½x − 2.", "y = ½x − 2, y = 3x, y = −5x + 1", "Bandingkan |m|: ½ &lt; 3 &lt; 5. Tanda hanya menunjukkan naik atau turun."),
        Q(3, "Periksa apakah titik A(−1, −4), B(1, 2), dan C(4, 11) segaris.", "segaris", "m<sub>AB</sub> = 6 : 2 = 3 dan m<sub>BC</sub> = 9 : 3 = 3; gradiennya sama dan B dipakai bersama."),
        Q(3, "Sebuah jalan naik 12 m untuk setiap 200 m jarak mendatar. Tentukan gradiennya dan nyatakan sebagai persen kemiringan.", "0,06 atau 6%", "12 : 200 = 0,06; dikali 100%."),
        Q(3, "Grafik biaya langganan internet B terhadap kuota x (GB) berupa garis yang melalui (10, 85.000) dan (25, 160.000). Tentukan gradien beserta artinya, dan biaya saat x = 0.", "m = 5.000, yaitu Rp5.000 per GB; Rp35.000",
          "m = 75.000 : 15 = 5.000; B = 85.000 − 10 · 5.000 = 35.000 saat x = 0 (biaya tetap)."),
    ],
))

# ================================================================== Subbab 3
SUB.append(dict(
    title="Menyusun Persamaan Garis Lurus",
    tujuan="Menyusun persamaan garis dari satu titik dan gradien, dari dua titik, atau dari titik potong kedua sumbu, dan mengubah bentuk persamaannya.",
    konsep=[
        "Sebuah garis tertentu bila diketahui (i) satu titik yang dilaluinya dan gradiennya, atau (ii) dua titik yang dilaluinya.",
        "Garis melalui (x₁, y₁) dengan gradien m: y − y₁ = m(x − x₁). Rumus ini berasal dari definisi gradien: untuk setiap titik (x, y) pada garis, (y − y₁) : (x − x₁) = m.",
        "Garis melalui dua titik: hitung dulu m dari kedua titik, lalu pakai rumus di atas dengan salah satu titik. Garis yang memotong sumbu x di (a, 0) dan sumbu y di (0, b) mempunyai persamaan " + fr("x", "a") + " + " + fr("y", "b") + " = 1, atau bx + ay = ab.",
        "Persamaan yang sama dapat ditulis sebagai y = mx + c atau ax + by + c = 0. Uji hasilnya dengan memasukkan titik yang diketahui.",
    ],
    rumus=["y − y₁ = m(x − x₁)", fr("y − y₁", "y₂ − y₁") + " = " + fr("x − x₁", "x₂ − x₁"), "Potong sumbu di (a, 0) dan (0, b): bx + ay = ab", "Garis tegak melalui (k, y₁): x = k"],
    contoh=[
        ("Titik dan gradien", "Tentukan persamaan garis yang melalui (2, −1) dengan gradien 3.", None,
         ["y − (−1) = 3(x − 2) → y + 1 = 3x − 6.", "y = 3x − 7. Uji: 3 · 2 − 7 = −1. Benar."], "y = 3x − 7"),
        ("Dua titik", "Tentukan persamaan garis yang melalui A(−2, 5) dan B(4, 2) dalam bentuk ax + by + c = 0.", None,
         ["m = (2 − 5) : (4 − (−2)) = −3 : 6 = −½.", "y − 5 = −½(x + 2). Kalikan 2: 2y − 10 = −x − 2.", "x + 2y − 8 = 0. Uji B: 4 + 4 − 8 = 0. Benar."], "x + 2y − 8 = 0"),
    ],
    bertahap=dict(
        soal="Tentukan persamaan garis yang memotong sumbu x di (6, 0) dan sumbu y di (0, −4).",
        langkah=["a = ____ dan b = ____.", "bx + ay = ab: ____x + ____y = ____.", "Dalam bentuk y = mx + c: y = ____."],
        cek="Gradien garis ini positif karena",
        opsi=["(a) dari (0, −4) ke (6, 0), nilai y naik ketika x naik", "(b) potongan sumbu x bernilai positif"],
        kunci="a = 6, b = −4; −4x + 6y = −24 (atau 2x − 3y = 12); y = ⅔x − 4. Alasan: (a).",
    ),
    jebakan=["Perhatikan tanda pada y − y₁ = m(x − x₁): untuk titik (−3, 2) ditulis y − 2 = m(x + 3), bukan m(x − 3).",
             "Pada bx + ay = ab, a adalah potongan sumbu x dan b potongan sumbu y; jangan tertukar.",
             "Dua titik dengan x yang sama membentuk garis tegak x = k, yang tidak dapat ditulis sebagai y = mx + c."],
    latihan=[
        Q(1, "Tentukan persamaan garis bergradien 2 yang melalui (0, −3).", "y = 2x − 3", "c = −3 karena titiknya di sumbu y."),
        Q(1, "Tentukan persamaan garis bergradien −1 yang melalui (4, 1).", "y = −x + 5", "y − 1 = −(x − 4)."),
        Q(1, "Tentukan persamaan garis yang melalui (1, 1) dan (3, 7).", "y = 3x − 2", "m = 6 : 2 = 3; y − 1 = 3(x − 1)."),
        Q(1, "Tentukan persamaan garis yang memotong sumbu x di (3, 0) dan sumbu y di (0, 6).", "2x + y = 6", "6x + 3y = 18, lalu dibagi 3."),
        Q(1, "Ubah y = −⅔x + 4 ke bentuk ax + by + c = 0 dengan a, b, c bulat.", "2x + 3y − 12 = 0", "Kalikan 3: 3y = −2x + 12."),
        Q(2, "Tentukan persamaan garis yang melalui (−3, 2) dengan gradien ½.", "x − 2y + 7 = 0 (y = ½x + 3½)", "y − 2 = ½(x + 3) → 2y − 4 = x + 3."),
        Q(2, "Tentukan persamaan garis yang melalui P(−1, −2) dan Q(3, 6).", "y = 2x", "m = 8 : 4 = 2; y + 2 = 2(x + 1)."),
        Q(2, "Tentukan persamaan garis pada grafik berikut.", "3x − 2y = −6 (y = 1½x + 3)", "a = −2, b = 3: 3x + (−2)y = 3 · (−2).", fig=FIG_L3),
        Q(2, "Garis y = mx + 5 melalui titik (2, −1). Tentukan m dan titik potong garis itu dengan sumbu x.", "m = −3; (" + fr("5", "3") + ", 0)", "2m + 5 = −1 → m = −3; −3x + 5 = 0 → x = 5/3."),
        Q(3, "Titik A(1, 3), B(5, 5), dan C(3, −1) adalah titik sudut segitiga. Tentukan persamaan garis berat dari C ke sisi AB (garis dari C ke titik tengah AB).", "x = 3",
          "Titik tengah AB = ((1 + 5) : 2, (3 + 5) : 2) = (3, 4). Garis melalui (3, −1) dan (3, 4) tegak, jadi x = 3."),
        Q(3, "Sewa sepeda 2 jam Rp35.000 dan 5 jam Rp65.000, dengan tarif per jam tetap. Tulis biaya B terhadap lama sewa t, lalu tentukan biaya 8 jam.", "B = 10.000t + 15.000; Rp95.000",
          "m = 30.000 : 3 = 10.000; 35.000 − 20.000 = 15.000; B(8) = 95.000."),
        Q(3, "Sebuah garis melalui (2, 3) dan memotong sumbu x dan sumbu y positif dengan potongan yang sama panjang. Tentukan persamaannya.", "x + y = 5", fr("x", "a") + " + " + fr("y", "a") + " = 1 → 2 + 3 = a → a = 5."),
    ],
))

# ================================================================== Subbab 4
SUB.append(dict(
    title="Titik Temu Dua Garis",
    tujuan="Menentukan titik temu dua garis sebagai penyelesaian sistem persamaan linear dua variabel dengan grafik, substitusi, dan eliminasi.",
    konsep=[
        "<b>Titik temu</b> (titik potong) dua garis adalah titik yang memenuhi kedua persamaan sekaligus. Mencarinya sama dengan menyelesaikan <b>sistem persamaan linear dua variabel</b> (SPLDV).",
        "Cara <b>grafik</b>: gambar kedua garis dan baca perpotongannya (tepat hanya bila titiknya jatuh di kisi). Cara <b>substitusi</b>: nyatakan satu variabel dari satu persamaan, lalu masukkan ke persamaan lain. Cara <b>eliminasi</b>: samakan koefisien satu variabel, lalu jumlahkan atau kurangkan kedua persamaan.",
        "Banyak penyelesaian dilihat dari gradien. Gradien berbeda: tepat satu titik temu. Gradien sama tetapi c berbeda: garis <b>sejajar</b>, tidak ada penyelesaian. Kedua persamaan setara: garis <b>berimpit</b>, tak hingga banyak penyelesaian.",
        "Untuk a₁x + b₁y = c₁ dan a₂x + b₂y = c₂: satu penyelesaian bila " + fr("a₁", "a₂") + " ≠ " + fr("b₁", "b₂") + "; tidak ada bila " + fr("a₁", "a₂") + " = " + fr("b₁", "b₂") + " ≠ " + fr("c₁", "c₂") + "; tak hingga bila ketiganya sama.",
    ],
    rumus=["y = m₁x + c₁ dan y = m₂x + c₂: m₁x + c₁ = m₂x + c₂ → x = " + fr("c₂ − c₁", "m₁ − m₂") + " (m₁ ≠ m₂)",
           "Satu penyelesaian: " + fr("a₁", "a₂") + " ≠ " + fr("b₁", "b₂"), "Tidak ada: " + fr("a₁", "a₂") + " = " + fr("b₁", "b₂") + " ≠ " + fr("c₁", "c₂") + "; tak hingga: ketiganya sama",
           "Selalu uji (x, y) pada <b>kedua</b> persamaan"],
    contoh=[
        ("Grafik dan substitusi", "Tentukan titik temu garis y = x + 1 dan y = −2x + 7.", FIG_TEMU,
         ["Pada titik temu nilai y-nya sama: x + 1 = −2x + 7.", "3x = 6 → x = 2, lalu y = 2 + 1 = 3.", "Uji pada garis kedua: −2 · 2 + 7 = 3. Benar, dan sesuai grafik."], "(2, 3)"),
        ("Eliminasi", "Selesaikan 2x + 3y = 12 dan 5x − 2y = 11.", None,
         ["Samakan koefisien y: kalikan persamaan pertama dengan 2 dan kedua dengan 3: 4x + 6y = 24 dan 15x − 6y = 33.", "Jumlahkan: 19x = 57 → x = 3.", "2 · 3 + 3y = 12 → y = 2. Uji: 5 · 3 − 2 · 2 = 11. Benar."], "x = 3, y = 2"),
    ],
    bertahap=dict(
        soal="Paket A berisi 2 buku dan 3 pensil seharga Rp31.000. Paket B berisi 1 buku dan 2 pensil seharga Rp18.000. Tentukan harga satu buku dan satu pensil.",
        langkah=["Misalkan harga buku b dan harga pensil p: 2b + 3p = 31.000 dan b + 2p = ____.", "Dari persamaan kedua: b = ____ − 2p.", "Substitusi: 2(18.000 − 2p) + 3p = 31.000 → 36.000 − p = 31.000 → p = ____.", "b = ____."],
        cek="Variabel b dinyatakan dari persamaan kedua karena",
        opsi=["(a) koefisien b di sana 1, sehingga tidak muncul pecahan", "(b) persamaan kedua memuat harga yang lebih kecil"],
        kunci="b + 2p = 18.000; b = 18.000 − 2p; p = 5.000; b = 8.000 (buku Rp8.000, pensil Rp5.000). Alasan: (a).",
    ),
    jebakan=["Saat mengalikan persamaan untuk eliminasi, kalikan <b>semua</b> suku, termasuk ruas kanan.",
             "Hati-hati mengurangkan suku negatif: 3y − (−2y) = 5y.",
             "Titik temu adalah pasangan (x, y); setelah x ditemukan, y juga harus dihitung.",
             "Jika perhitungan berakhir pada pernyataan salah seperti 0 = 5, garisnya sejajar dan tidak ada penyelesaian; itu bukan salah hitung."],
    latihan=[
        Q(1, "Tentukan titik temu garis y = 2x dan y = x + 3.", "(3, 6)", "2x = x + 3 → x = 3."),
        Q(1, "Tentukan titik temu garis y = 3x − 1 dan y = 5.", "(2, 5)", "3x − 1 = 5 → x = 2."),
        Q(1, "Selesaikan x + y = 10 dan x − y = 4.", "x = 7, y = 3", "Jumlahkan: 2x = 14."),
        Q(1, "Selesaikan 2x + y = 7 dan y = x + 1.", "x = 2, y = 3", "2x + x + 1 = 7 → 3x = 6."),
        Q(1, "Baca titik temu garis g dan h pada grafik berikut, lalu ujilah dengan persamaan g: y = −x + 4 dan h: y = ½x + 1.", "(2, 2)", "−2 + 4 = 2 dan ½ · 2 + 1 = 2.", fig=FIG_L4),
        Q(2, "Selesaikan 3x + 2y = 16 dan x − 4y = −4.", "x = 4, y = 2", "x = 4y − 4; 3(4y − 4) + 2y = 16 → 14y = 28 → y = 2."),
        Q(2, "Selesaikan 4x − 3y = 1 dan 3x + 2y = 22.", "x = 4, y = 5", "Kalikan 2 dan 3: 8x − 6y = 2, 9x + 6y = 66; 17x = 68."),
        Q(2, "Tentukan banyak penyelesaian (a) 2x − y = 3 dan 4x − 2y = 6; (b) 2x − y = 3 dan 4x − 2y = 1.", "(a) tak hingga banyak; (b) tidak ada",
          "(a) Persamaan kedua = 2 × persamaan pertama: berimpit. (b) Gradien sama (2), tetapi 4x − 2y = 6 ≠ 1: sejajar."),
        Q(2, "Harga 3 kg apel dan 2 kg jeruk Rp96.000, sedangkan 1 kg apel dan 4 kg jeruk Rp72.000. Berapa harga 2 kg apel dan 1 kg jeruk?", "Rp60.000",
          "a = 72.000 − 4j; 3(72.000 − 4j) + 2j = 96.000 → 10j = 120.000 → j = 12.000, a = 24.000; 2a + j = 60.000."),
        Q(3, "Garis ax + 2y = 8 dan 3x − y = 1 berpotongan di titik yang absisnya x = 2. Tentukan titik temu dan nilai a.", "(2, 5); a = −1", "3 · 2 − y = 1 → y = 5; 2a + 10 = 8 → a = −1."),
        Q(3, "Ojek P bertarif Rp5.000 + Rp2.500 per km; ojek Q bertarif Rp8.000 + Rp2.000 per km. Pada jarak berapa tarif keduanya sama? Untuk jarak 10 km, mana yang lebih murah?", "6 km (keduanya Rp20.000); untuk 10 km ojek Q lebih murah",
          "5.000 + 2.500x = 8.000 + 2.000x → x = 6. Pada 10 km: P = 30.000, Q = 28.000."),
        Q(3, "Tentukan nilai k agar sistem 2x + ky = 5 dan 6x + 9y = 4 tidak mempunyai penyelesaian.", "k = 3", "Syarat sejajar: 2/6 = k/9 → k = 3; dan 2/6 ≠ 5/4, jadi tidak berimpit."),
    ],
))

# ================================================================== Subbab 5
SUB.append(dict(
    title="Garis Sejajar dan Tegak Lurus",
    tujuan="Memakai syarat garis sejajar (m₁ = m₂) dan tegak lurus (m₁ · m₂ = −1) untuk menyusun persamaan garis, menentukan parameter, dan menghitung jarak titik ke garis.",
    konsep=[
        "Dua garis (yang tidak tegak) <b>sejajar</b> jika dan hanya jika gradiennya sama: m₁ = m₂. Jika konstantanya juga sama, kedua garis berimpit.",
        "Dua garis <b>tegak lurus</b> jika dan hanya jika m₁ · m₂ = −1, yaitu m₂ = −1/m₁ (negatif kebalikan). Alasannya: putar segitiga gradien 90°. Langkah 1 ke kanan dan m ke atas berubah menjadi m ke kiri dan 1 ke atas, sehingga gradiennya 1 : (−m) = −1/m.",
        "Pengecualian: garis mendatar (m = 0) tegak lurus garis tegak x = k; rumus m₁ · m₂ = −1 tidak dapat dipakai untuk pasangan ini.",
        "Jarak terpendek dari titik P ke garis g diukur sepanjang garis yang melalui P dan tegak lurus g. Titik temunya disebut <b>kaki garis tegak lurus</b>; jaraknya dihitung dengan teorema Pythagoras.",
    ],
    rumus=["Sejajar: m₁ = m₂; tegak lurus: m₁ · m₂ = −1", "Sejajar ax + by + c = 0 melalui (x₁, y₁): ax + by = ax₁ + by₁",
           "Tegak lurus ax + by + c = 0 melalui (x₁, y₁): bx − ay = bx₁ − ay₁", "Jarak dua titik: √((x₂ − x₁)² + (y₂ − y₁)²)"],
    contoh=[
        ("Sejajar dan tegak lurus", "Tentukan persamaan garis melalui (1, 4) yang (a) sejajar dan (b) tegak lurus garis y = 2x − 3.", FIG_SEJ,
         ["(a) Gradien sama, m = 2: y − 4 = 2(x − 1) → y = 2x + 2.", "(b) m = −½: y − 4 = −½(x − 1) → 2y − 8 = −x + 1 → x + 2y = 9, atau y = −½x + 4½.", "Uji (1, 4) pada x + 2y = 9: 1 + 8 = 9. Benar."],
         "(a) y = 2x + 2; (b) x + 2y = 9"),
        ("Jarak titik ke garis", "Tentukan titik Q pada garis y = 2x − 3 yang paling dekat dengan P(7, 1), lalu hitung jarak P ke garis itu.", None,
         ["Garis melalui P yang tegak lurus y = 2x − 3 bergradien −½: y − 1 = −½(x − 7) → y = −½x + 4½.", "Titik temu: 2x − 3 = −½x + 4½ → 2½x = 7½ → x = 3, y = 3. Jadi Q(3, 3).",
          "PQ = √((7 − 3)² + (1 − 3)²) = √(16 + 4) = √20 = 2√5."], "Q(3, 3); jarak 2√5 ≈ 4,47"),
    ],
    bertahap=dict(
        soal="Garis g: 3x + ky = 6 tegak lurus garis h: 2x − 3y = 5. Tentukan k.",
        langkah=["Gradien h: m<sub>h</sub> = −2 : (−3) = ____.", "Gradien g: m<sub>g</sub> = −3 : k.", "(−3 : k) · ____ = −1 → −2 : k = −1 → k = ____."],
        cek="Syarat yang dipakai adalah",
        opsi=["(a) hasil kali gradien sama dengan −1", "(b) gradien kedua garis sama"],
        kunci="m<sub>h</sub> = ⅔; (−3/k) · ⅔ = −1; k = 2. Alasan: (a).",
    ),
    jebakan=["Gradien yang tegak lurus gradien 2 adalah −½, bukan −2 (hanya tanda dibalik) dan bukan ½ (hanya dibalik).",
             "Sejajar berarti gradiennya sama; konstanta c tidak perlu sama.",
             "Bandingkan gradien setelah setiap garis ditulis dalam bentuk y = mx + c atau dengan m = −a/b.",
             "Garis yang tegak lurus x = k adalah garis mendatar y = ...; jangan memakai m₁ · m₂ = −1 di sini."],
    latihan=[
        Q(1, "Tentukan gradien garis yang sejajar dan gradien garis yang tegak lurus garis y = 4x + 1.", "4 dan −¼", "Sejajar: sama; tegak lurus: −1/4."),
        Q(1, "Berapa gradien garis yang tegak lurus garis bergradien −⅔?", fr("3", "2"), "−1 : (−⅔) = 3/2."),
        Q(1, "Apakah garis y = 3x + 2 dan 6x − 2y = 5 sejajar?", "ya", "6x − 2y = 5 → y = 3x − 2½; gradien keduanya 3."),
        Q(1, "Apakah garis y = ½x − 1 dan y = −2x + 3 tegak lurus?", "ya", "½ · (−2) = −1."),
        Q(1, "Tentukan persamaan garis melalui (0, 5) yang sejajar garis y = −3x + 1.", "y = −3x + 5", "m = −3, c = 5."),
        Q(2, "Tentukan persamaan garis melalui (2, −1) yang tegak lurus garis y = 4x − 7.", "x + 4y + 2 = 0 (y = −¼x − ½)", "m = −¼: y + 1 = −¼(x − 2) → 4y + 4 = −x + 2."),
        Q(2, "Tentukan persamaan garis melalui (−1, 3) yang sejajar garis 2x + 5y = 10.", "2x + 5y = 13", "2x + 5y = 2 · (−1) + 5 · 3."),
        Q(2, "Tentukan nilai p agar garis px + 2y = 7 sejajar garis 3x − y = 4.", "p = −6", "−p/2 = 3."),
        Q(2, "Dari garis (1) y = 2x + 1, (2) x + 2y = 4, (3) 4x − 2y = 3, (4) y = −½x, pasangan mana yang sejajar dan mana yang tegak lurus?", "sejajar: (1) dan (3), (2) dan (4); tegak lurus: (1) atau (3) dengan (2) atau (4)",
          "Gradiennya 2, −½, 2, −½; 2 · (−½) = −1."),
        Q(3, "Tentukan persamaan garis sumbu ruas garis AB dengan A(1, 2) dan B(5, 6), yaitu garis yang tegak lurus AB dan melalui titik tengahnya.", "x + y = 7", "Titik tengah (3, 4); m<sub>AB</sub> = 1, jadi m = −1: y − 4 = −(x − 3)."),
        Q(3, "Diketahui A(−2, 1), B(4, 3), dan C(2, k). Tentukan k agar sudut ABC siku-siku di B.", "k = 9", "m<sub>AB</sub> = 2 : 6 = ⅓, jadi m<sub>BC</sub> = −3: (k − 3) : (2 − 4) = −3 → k − 3 = 6."),
        Q(3, "Tentukan jarak titik P(4, 5) ke garis y = x − 3 dengan mencari kaki garis tegak lurusnya.", "2√2 (kaki di (6, 3))", "Garis tegak lurus melalui P: y = −x + 9; x − 3 = −x + 9 → (6, 3); √(2² + 2²) = 2√2."),
    ],
))

CAMPURAN = [
    Q(1, "Tentukan gradien dan titik potong sumbu y garis 5x + 2y = 8.", "m = −" + fr("5", "2") + "; (0, 4)", "y = −5/2 x + 4."),
    Q(1, "Tentukan titik temu garis y = 4 − x dan y = x − 2.", "(3, 1)", "4 − x = x − 2 → x = 3."),
    Q(1, "Tentukan persamaan garis yang melalui (2, 3) dan (2, −5).", "x = 2", "Kedua titik ber-x sama: garis tegak."),
    Q(2, "Garis yang melalui (−2, k) dan (3, 7) sejajar garis y = 2x − 1. Tentukan k.", "k = −3", "(7 − k) : 5 = 2 → 7 − k = 10."),
    Q(2, "Tentukan persamaan garis yang melalui titik temu x + y = 5 dan 2x − y = 1 serta tegak lurus garis y = 3x.", "x + 3y = 11", "Titik temu (2, 3); m = −⅓: y − 3 = −⅓(x − 2) → 3y − 9 = −x + 2."),
    Q(2, "Fungsi linear f memenuhi f(2) = 1 dan f(−4) = 10. Tentukan f(0) dan nilai x yang membuat f(x) = 0.", "f(0) = 4; x = " + fr("8", "3"), "m = 9 : (−6) = −3/2; f(x) = −3/2 x + 4; −3/2 x + 4 = 0 → x = 8/3."),
    Q(2, "Operator A menjual paket data Rp20.000 + Rp4.000 per GB, operator B Rp32.000 + Rp2.500 per GB. Untuk kuota berapa GB biaya keduanya sama?", "8 GB (Rp52.000)", "1.500x = 12.000 → x = 8."),
    Q(2, "Tentukan luas segitiga yang dibatasi sumbu x, sumbu y, dan garis 3x + 4y = 24.", "24 satuan luas", "Titik potong (8, 0) dan (0, 6); ½ · 8 · 6."),
    Q(3, "Garis y = 2x + 1, garis y = −x + 7, dan sumbu x membentuk sebuah segitiga. Tentukan luasnya.", "18,75 satuan luas", "Titik temu kedua garis (2, 5); keduanya memotong sumbu x di x = −½ dan x = 7; ½ · 7½ · 5."),
    Q(3, "Segitiga ABC mempunyai A(0, 0), B(6, 0), dan C(2, 4). Tentukan titik potong garis tinggi dari A dan garis tinggi dari B.", "(2, 2)",
      "m<sub>BC</sub> = −1, jadi garis tinggi dari A: y = x. m<sub>AC</sub> = 2, jadi garis tinggi dari B: y = −½(x − 6). x = −½x + 3 → x = 2. Garis tinggi dari C (x = 2) juga melalui (2, 2)."),
]

TKA = [
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Perhatikan garis g, h, dan k pada grafik berikut. Setiap garis melalui titik-titik kisi.", fig=FIG_T1, soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["g sejajar h", "g dan k berpotongan di (0, 2)", "g tegak lurus k", "k memotong sumbu x di (−1, 0)", "h dan k berpotongan di (1, 0)"], kunci=[0, 2, 4],
         bahas="Dari grafik: g: y = x + 2, h: y = x − 1, k: y = −x + 1. Gradien g dan h sama (1); 1 · (−1) = −1; x − 1 = −x + 1 → (1, 0).",
         salah="B: g dan k berpotongan di (−½, 1½); (0, 2) hanya potongan sumbu y garis g. D: k memotong sumbu x di (1, 0)."),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Persamaan garis yang melalui (3, −2) dan tegak lurus garis 3x − 2y = 6 adalah ....",
         opsi=["2x + 3y = 0", "3x − 2y = 13", "2x − 3y = 12", "3x + 2y = 5", "2x + 3y = 12"], kunci=0,
         bahas="Gradien garis 3x − 2y = 6 adalah 3/2, jadi gradien tegak lurusnya −2/3: y + 2 = −⅔(x − 3) → 3y + 6 = −2x + 6 → 2x + 3y = 0.",
         salah="B: garis sejajar. C: tanda negatif lupa (gradien ⅔). D: hanya tanda yang dibalik (gradien −3/2). E: memakai titik (3, 2)."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Garis (a − 1)x + 4y = 8 sejajar garis yang melalui (−1, 5) dan (3, −1). Nilai a adalah ....",
         opsi=["7", "−5", "6", "−5/3", "11/3"], kunci=0,
         bahas="Gradien garis kedua (−1 − 5) : (3 + 1) = −3/2. Gradien garis pertama −(a − 1)/4 = −3/2 → a − 1 = 6 → a = 7.",
         salah="B: tanda minus pada −a/b terlupa. C: lupa mengurangkan 1. D: memakai syarat tegak lurus. E: gradien dihitung Δx : Δy."),
    dict(tipe="MAT-MODEL", lv=2, fmt="pg", soal="Kolam A berisi 1.200 L air dan dikuras 40 L per menit. Pada saat yang sama, kolam B yang berisi 300 L diisi 50 L per menit. Volume air kedua kolam sama ....",
         opsi=["setelah 10 menit, yaitu 800 L", "setelah 90 menit, yaitu 4.800 L", "setelah 10 menit, yaitu 700 L", "setelah 18 menit, yaitu 480 L", "setelah 22,5 menit, yaitu 300 L"], kunci=0,
         bahas="1.200 − 40t = 300 + 50t → 90t = 900 → t = 10; V = 1.200 − 400 = 800 L (cek: 300 + 500 = 800).",
         salah="B: laju dikurangkan (50 − 40), padahal satu kolam berkurang dan yang lain bertambah. C: volume dihitung 300 + 40 · 10. D: 900 dibagi 50 saja. E: 900 dibagi 40 saja."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Biaya mencetak n lembar brosur di sebuah percetakan dimodelkan B(n) = 750n + 60.000 rupiah. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["Biaya tetap yang tidak bergantung pada banyak brosur adalah Rp60.000.", "Setiap tambahan 100 lembar menambah biaya Rp75.000.", "Biaya mencetak 400 lembar dua kali biaya mencetak 200 lembar.",
               "Dengan uang Rp300.000, paling banyak 320 lembar dapat dicetak."], kunci=[True, True, False, True],
         bahas="B(0) = 60.000; 750 · 100 = 75.000; B(400) = 360.000, sedangkan 2 · B(200) = 2 · 210.000 = 420.000; 750n + 60.000 ≤ 300.000 → n ≤ 320.", salah=""),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pgk", soal="Titik yang terletak pada garis yang melalui (−2, 7) dan (4, −2) adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["(0, 4)", "(1, 3)", "(2, 1)", "(6, −5)", "(−4, 9)"], kunci=[0, 2, 3],
         bahas="m = −9 : 6 = −3/2; y − 7 = −3/2 (x + 2) → y = −3/2 x + 4. Uji: (0, 4), (2, 1), (6, −5) memenuhi.", salah="B: x = 1 memberi y = 2½. E: x = −4 memberi y = 10."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Diketahui garis g: y = 2x + 3 dan garis h: kx − y = 1. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["Jika k = 2, garis g dan h sejajar.", "Jika k = −½, garis g dan h tegak lurus.", "Jika k = 4, titik temu g dan h adalah (2, 5).", "Ada nilai k yang membuat g dan h berimpit."], kunci=[True, True, False, False],
         bahas="h: y = kx − 1, gradien k. k = 2: gradien sama, c berbeda. 2 · (−½) = −1. k = 4: 2x + 3 = 4x − 1 → (2, 7), bukan (2, 5). Berimpit perlu c = 3, padahal c garis h selalu −1.", salah=""),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg",
         soal="Panitia sekolah menyewa bus. Jarak perjalanan belum pasti, antara 120 km dan 240 km. Tarif yang ditawarkan: P Rp1.200.000 + Rp8.000 per km; Q Rp600.000 + Rp11.000 per km; S Rp15.000 per km tanpa biaya tetap; T Rp1.800.000 + Rp4.000 per km. Panitia memilih tarif yang biayanya pasti tidak lebih dari Rp2.800.000 berapa pun jaraknya dalam rentang itu. Tarif yang memenuhi adalah ....",
         opsi=["T saja", "S saja", "P dan T", "Q saja", "tidak ada"], kunci=0,
         bahas="Semua biaya naik terhadap jarak, jadi cukup diperiksa pada 240 km: P = 3.120.000; Q = 3.240.000; S = 3.600.000; T = 2.760.000. Hanya T yang tidak lebih dari Rp2.800.000.",
         salah="B: hanya diperiksa pada 120 km, tempat S termurah (Rp1.800.000). C: P hanya memenuhi sampai 200 km. D: Q Rp3.240.000 pada 240 km. E: T memenuhi."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Garis g: y = mx + c mempunyai m &lt; 0 dan c &gt; 0. Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["g melalui kuadran III", "g memotong sumbu x di titik yang absisnya positif", "g melalui kuadran I, II, dan IV", "g sejajar garis y = −mx + c", "setiap garis yang tegak lurus g mempunyai gradien positif"],
         kunci=[1, 2, 4],
         bahas="Potongan sumbu x: −c/m &gt; 0. Garis turun, memotong sumbu y positif dan sumbu x positif, sehingga melalui kuadran II, I, lalu IV. Gradien tegak lurus −1/m &gt; 0.",
         salah="A: untuk x &lt; 0 nilai y &gt; c &gt; 0, jadi g tidak pernah di kuadran III. D: gradien −m berbeda tanda dengan m."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Garis x + y = 6, 2x − y = 3, dan ax + y = 8 melalui satu titik yang sama. Nilai a adalah ....",
         opsi=["5/3", "11/3", "8/3", "5", "3"], kunci=0,
         bahas="Titik temu dua garis pertama: 3x = 9 → (3, 3). Garis ketiga melalui (3, 3): 3a + 3 = 8 → a = 5/3.",
         salah="B: tanda y salah (3a − 3 = 8). C: suku y diabaikan (3a = 8). D: lupa membagi 5 dengan x = 3. E: nilai x titik temu, bukan a."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Gradien garis yang melalui (2, −3) dan (5, 6) adalah ....", ["3", "1/3", "−3", "1", "9"], 0, "9 : 3.", "B: Δx : Δy. C: urutan titik tidak sama di pembilang dan penyebut. D: −3 dibaca 3 (6 − 3 = 3). E: lupa membagi dengan Δx."),
    ("Gradien garis 6x − 2y + 5 = 0 adalah ....", ["3", "−3", "6", "1/3", "−1/3"], 0, "−a/b = −6 : (−2).", "B: memakai a/b tanpa tanda minus. C: koefisien x. D: memakai −b/a. E: memakai b/a."),
    ("Titik potong garis 4x − 3y = 12 dengan sumbu x dan sumbu y adalah ....", ["(3, 0) dan (0, −4)", "(4, 0) dan (0, −3)", "(3, 0) dan (0, 4)", "(−3, 0) dan (0, 4)", "(0, 3) dan (−4, 0)"], 0,
     "y = 0 → x = 3; x = 0 → y = −4.", "B: koefisien tertukar. C: tanda y salah. D: kedua tanda salah. E: urutan koordinat terbalik."),
    ("Persamaan garis bergradien −2 yang melalui (3, 1) adalah ....", ["y = −2x + 7", "y = −2x − 5", "y = −2x + 5", "y = 2x − 5", "y = −2x + 1"], 0, "y − 1 = −2(x − 3).",
     "B: memakai (x + 3). C: memakai (y + 1). D: gradien 2. E: c dianggap sama dengan y₁."),
    ("Persamaan garis yang melalui (−1, 4) dan (2, −2) adalah ....", ["2x + y = 2", "2x + y = 6", "x + 2y = 7", "2x − y = −6", "x − 2y = −9"], 0, "m = −6 : 3 = −2; y − 4 = −2(x + 1).",
     "B: memakai (x − 1). C: gradien Δx : Δy = −½. D: tanda gradien salah (2). E: gradien ½."),
    ("Garis yang sejajar garis 3x − y = 4 adalah ....", ["6x − 2y = 1", "x + 3y = 4", "3x + y = 4", "x − 3y = 2", "y = −3x"], 0, "Gradien 3x − y = 4 adalah 3; gradien 6x − 2y = 1 juga 3.",
     "B: tegak lurus (gradien −⅓). C, E: gradien −3. D: gradien ⅓."),
    ("Gradien garis yang tegak lurus garis 2x + 5y = 1 adalah ....", ["5/2", "−5/2", "−2/5", "2/5", "5"], 0, "Gradien garis itu −2/5; negatif kebaliknya 5/2.",
     "B: hanya dibalik. C: gradien garis itu sendiri. D: hanya tanda dibalik. E: memakai koefisien y."),
    ("Titik temu garis y = 3x − 2 dan y = −x + 6 adalah ....", ["(2, 4)", "(4, 10)", "(4, 2)", "(2, 8)", "(1, 5)"], 0, "3x − 2 = −x + 6 → 4x = 8 → x = 2; y = 4.",
     "B: −x dibaca x. C: koordinat tertukar. D: y dihitung dari y = x + 6. E: tanda −2 tidak diganti saat pindah ruas."),
    ("Penyelesaian sistem 2x + y = 8 dan x − y = 1 adalah ....", ["x = 3, y = 2", "x = 2, y = 3", "x = 3, y = −2", "x = 7/3, y = 10/3", "x = 9, y = 8"], 0, "Jumlahkan: 3x = 9; y = 3 − 1.",
     "B: x dan y tertukar. C: x − y = 1 dibaca x + y = 1. D: ruas kanan dikurangkan padahal persamaan dijumlahkan. E: lupa membagi 3x = 9 dengan 3."),
    ("Sistem 3x − 6y = 9 dan x − 2y = k mempunyai tak hingga banyak penyelesaian bila k = ....", ["3", "9", "−3", "1/3", "27"], 0, "3x − 6y = 9 sama dengan x − 2y = 3.",
     "B: tidak dibagi 3. C: tanda salah. D: kebalikan. E: dikali 3."),
    ("Harga 2 roti dan 1 susu Rp19.000, sedangkan 1 roti dan 3 susu Rp22.000. Harga 1 roti dan 1 susu adalah ....", ["Rp12.000", "Rp7.000", "Rp5.000", "Rp41.000", "Rp14.000"], 0,
     "r = 22.000 − 3s; 2(22.000 − 3s) + s = 19.000 → s = 5.000, r = 7.000.", "B: harga roti saja. C: harga susu saja. D: harga kedua paket dijumlahkan. E: harga 2 roti."),
    ("Garis kx + 3y = 6 tegak lurus garis y = 2x + 1. Nilai k adalah ....", ["3/2", "−3/2", "−6", "6", "2/3"], 0, "(−k/3) · 2 = −1 → k = 3/2.",
     "B: tanda salah. C: syarat sejajar. D: syarat sejajar dengan tanda salah. E: kebalikan jawaban."),
    ("Garis g melalui (1, 2) dan sejajar garis yang melalui (0, 3) dan (2, −1). Persamaan g adalah ....", ["y = −2x + 4", "y = −2x + 3", "y = ½x + 3/2", "y = 2x", "y = −2x"], 0,
     "m = −4 : 2 = −2; y − 2 = −2(x − 1).", "B: memakai konstanta garis yang lain. C: garis tegak lurus. D: gradien 2. E: memakai (x + 1)."),
    ("Tagihan air terdiri atas Rp25.000 per bulan ditambah Rp6.500 per m³. Tagihan bulan lalu Rp142.000. Pemakaian airnya adalah ....", ["18 m³", "≈ 21,85 m³", "≈ 25,69 m³", "19 m³", "5,42 m³"], 0,
     "(142.000 − 25.000) : 6.500 = 18.", "B: biaya tetap tidak dikurangkan. C: biaya tetap ditambahkan. D: model 25.000 + 6.500(x − 1). E: kedua tarif tertukar."),
    ("Jarak titik P(3, 4) ke garis y = −x + 1 adalah ....", ["3√2", "6", "2√5", "3", "18"], 0,
     "Garis tegak lurus melalui P: y = x + 1; titik temu (0, 1); √(3² + 3²) = 3√2.", "B: selisih koordinat dijumlahkan tanpa Pythagoras. C: jarak ke titik potong sumbu x (1, 0), bukan jarak terpendek. D: hanya selisih x. E: lupa menarik akar."),
]
UJI_URAIAN = [
    ("Fungsi linear f memenuhi f(−1) = 7 dan f(3) = −1. Tentukan rumus f, titik potong grafiknya dengan kedua sumbu, lalu sketsa grafiknya.", "f(x) = −2x + 5; (0, 5) dan (2½, 0)",
     "m = −8 : 4 = −2; −2 · (−1) + c = 7 → c = 5; −2x + 5 = 0 → x = 5/2."),
    ("Tentukan persamaan garis yang melalui A(4, −1) dan B(−2, 3) dalam bentuk ax + by + c = 0, lalu periksa apakah C(1, 1) terletak pada garis itu.", "2x + 3y − 5 = 0; C terletak pada garis",
     "m = 4 : (−6) = −⅔; y + 1 = −⅔(x − 4) → 3y + 3 = −2x + 8. C: 2 + 3 − 5 = 0."),
    ("Selesaikan sistem 5x + 2y = 4 dan 3x − 4y = 18 dengan eliminasi, lalu periksa jawabanmu.", "x = 2, y = −3",
     "Kalikan persamaan pertama dengan 2: 10x + 4y = 8; jumlahkan dengan 3x − 4y = 18: 13x = 26; 10 + 2y = 4 → y = −3. Cek: 6 + 12 = 18."),
    ("Diketahui garis g: 2x − 3y = 6 dan titik P(1, 3). Tentukan (a) persamaan garis melalui P yang sejajar g, (b) persamaan garis melalui P yang tegak lurus g, (c) titik temu garis (b) dengan g, (d) jarak P ke g.",
     "(a) 2x − 3y = −7; (b) 3x + 2y = 9; (c) (3, 0); (d) √13",
     "(a) 2 · 1 − 3 · 3 = −7. (b) 3 · 1 + 2 · 3 = 9. (c) Eliminasi: 4x − 6y = 12 dan 9x + 6y = 27 → 13x = 39 → x = 3, y = 0. (d) √(2² + 3²) = √13."),
    ("Les A memungut biaya pendaftaran Rp150.000 dan Rp60.000 per pertemuan. Les B tanpa pendaftaran, Rp80.000 per pertemuan. (a) Tulis model biaya keduanya untuk n pertemuan. (b) Mulai pertemuan ke berapa Les A lebih murah? (c) Raka ikut 12 pertemuan; mana yang lebih murah dan berapa selisihnya?",
     "(a) A = 150.000 + 60.000n, B = 80.000n; (b) mulai pertemuan ke-8; (c) Les A, lebih murah Rp90.000",
     "(b) 150.000 + 60.000n &lt; 80.000n → n &gt; 7,5 (kedua garis berpotongan di n = 7,5). (c) A = 870.000, B = 960.000."),
]

META = dict(
    title="Modul Fungsi Linear dan Persamaan Garis", kick="Modul belajar Matematika · Fase E · Kelas X", big="Fungsi Linear",
    subtitle="Gradien, persamaan garis lurus, titik temu dua garis, serta garis sejajar dan tegak lurus",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat menyatakan fungsi linear dalam rumus, tabel, dan grafik; menentukan gradien dan persamaan garis lurus; menyelesaikan sistem persamaan linear dua variabel sebagai titik temu dua garis; serta memakai syarat garis sejajar dan tegak lurus untuk memecahkan masalah, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Satu fungsi linear, tiga wujud</h2><table><tr><th>Rumus</th><th>Tabel</th><th>Grafik</th></tr><tr><td>f(x) = 2x + 1</td><td>x = 0, 1, 2 → f(x) = 1, 3, 5</td><td>garis melalui (0, 1), naik 2 per 1 ke kanan</td></tr></table>"
               "<p><b>c = 1</b> adalah nilai awal (potongan sumbu y) dan <b>m = 2</b> laju perubahan (gradien).</p>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit</b> tanpa kalkulator, dan uji setiap jawaban dengan memasukkannya ke persamaan.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Garis ditulis y = mx + c atau ax + by + c = 0; gradien m = Δy : Δx. Desimal ditulis dengan koma, ribuan dengan titik (Rp4.500).",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>gradien, persamaan garis, titik temu, atau sejajar/tegak lurus?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025 (specs/tka-templates/matematika.md).",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-MODEL, MAT-FUNGSI): mengenali, menghitung, bekerja mundur, memodelkan, atau menafsirkan fungsi. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Mengapa gradien dua garis tegak lurus hasil kalinya −1?", "Bagaimana kamu tahu sebuah sistem persamaan linear tidak mempunyai penyelesaian sebelum menghitungnya?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Fungsi linear</th><td>f(x) = mx + c; potong sumbu y (0, c); potong sumbu x (−c/m, 0)</td></tr>"
        "<tr><th>Gradien</th><td>m = (y₂ − y₁)/(x₂ − x₁); y = mx + c → m; ax + by + c = 0 → m = −a/b; y = k → m = 0; x = k → tidak terdefinisi</td></tr>"
        "<tr><th>Persamaan garis</th><td>y − y₁ = m(x − x₁); melalui dua titik: hitung m dulu; potong sumbu (a, 0), (0, b): bx + ay = ab</td></tr>"
        "<tr><th>Titik temu</th><td>selesaikan kedua persamaan bersama (substitusi atau eliminasi); uji pada kedua persamaan</td></tr>"
        "<tr><th>Sejajar</th><td>m₁ = m₂; melalui (x₁, y₁) sejajar ax + by + c = 0: ax + by = ax₁ + by₁</td></tr>"
        "<tr><th>Tegak lurus</th><td>m₁ · m₂ = −1; melalui (x₁, y₁) tegak lurus ax + by + c = 0: bx − ay = bx₁ − ay₁</td></tr>"
        "<tr><th>Jarak titik ke garis</th><td>cari kaki garis tegak lurus, lalu √((x₂ − x₁)² + (y₂ − y₁)²)</td></tr></table>"
        "<h2>Hubungan dua garis</h2><table><tr><th>Gradien</th><th>Kedudukan</th><th>Banyak titik temu</th></tr>"
        "<tr><td>m₁ ≠ m₂</td><td>berpotongan (tegak lurus bila m₁ · m₂ = −1)</td><td>tepat satu</td></tr>"
        "<tr><td>m₁ = m₂, c₁ ≠ c₂</td><td>sejajar</td><td>tidak ada</td></tr>"
        "<tr><td>m₁ = m₂, c₁ = c₂</td><td>berimpit</td><td>tak hingga</td></tr></table>"
        '<div class="fig">' + FIG_SEJ + "</div>"),
    jebakan5=["Gradien = Δy : Δx, dengan urutan titik yang sama di pembilang dan penyebut.", "Gradien ax + by + c = 0 adalah −a/b; jangan lupa tanda minus.",
              "Tanda pada y − y₁ = m(x − x₁): titik (−3, 2) memberi y − 2 = m(x + 3).", "Tegak lurus = negatif kebalikan: untuk m = 2, gradiennya −½.",
              "Uji titik temu pada kedua persamaan, bukan hanya pada satu persamaan."],
    guru=["Gradien, persamaan garis lurus, dan SPLDV umumnya diajarkan di SMP (Fase D) dan dipakai lagi di SMA Fase E sebagai dasar sistem persamaan linear dan fungsi. Modul ini cocok untuk pemantapan di kelas X; urutan bab dapat berbeda antarsekolah.",
          "Modul ini tidak memakai trigonometri. Kemiringan dinyatakan sebagai gradien, bukan sebagai tangen sudut.",
          "Rumus jarak titik ke garis |ax₁ + by₁ + c| / √(a² + b²) sengaja tidak diajarkan; siswa menghitungnya lewat kaki garis tegak lurus. Guru dapat menambahkannya sebagai pengayaan.",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


def check():
    def m(p, q):
        return F(q[1] - p[1], q[0] - p[0])

    def meet(a1, b1, c1, a2, b2, c2):
        """Intersection of a1x + b1y = c1 and a2x + b2y = c2."""
        d = a1 * b2 - a2 * b1
        return (F(c1 * b2 - c2 * b1, d), F(a1 * c2 - a2 * c1, d))

    def on(a, b, c, p):
        return a * p[0] + b * p[1] == c

    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    # prasyarat
    assert -3 - (-7) == 4 and (-2) * (-5) == 10 and F(5 - (-1), 2 - 4) == -3 and F(2, 3) * F(-9, 4) == F(-3, 2) and F(-2, 3) * F(-3, 2) == 1
    assert 3 * 5 - 5 == 10 and 2 * (-1) - 3 == -5 and all(F(-2, 3) * x + 2 == F(6 - 2 * x, 3) for x in range(-3, 4))
    # subbab 1
    assert 2 * 0 - 4 == -4 and 2 * 2 - 4 == 0 and 2 * 3 - 4 == 2
    assert 4500 * 12 + 7000 == 61000 and F(52000 - 7000, 4500) == 10
    assert F(11 - 5, 2) == 3 and 3 * (-3) + 5 == -4
    assert 3 * 4 - 2 == 10 and 3 * (-1) - 2 == -5 and -2 * 0 + 6 == 6 and F(-6, -2) == 3 and 3 * 2 + 1 == 7
    assert m((1, 4), (3, 10)) == 3 and 4 - 3 * 1 == 1
    assert on(3, 2, 12, (4, 0)) and on(3, 2, 12, (0, 6)) and F(24, F(3, 2)) == 16
    assert m((0, -1), (2, 3)) == 2
    assert F(150000, 4000 - 2500) == 100 and F(65 - 20, 9) == 5 and 5 * 4 + 20 == 40 and F(100 - 20, 5) == 16
    assert F(6, 2) == 3 and 3 * 5 - 1 == 14
    # subbab 2
    assert m((-1, 5), (3, -3)) == -2 and F(-4, -6) == F(2, 3)
    assert m((-1, 1), (1, 5)) == 2 and m((-1, 1), (2, 7)) == 2
    assert m((1, 2), (4, 11)) == 3 and m((-2, 3), (2, 1)) == F(-1, 2) and F(-3, 1) == -3 and F(-2, -5) == F(2, 5) and m((-3, -1), (3, 3)) == F(2, 3)
    assert m((4, 3), (2, -5)) == 4
    assert sorted([F(1, 2), F(3), F(5)]) == [F(1, 2), 3, 5]
    assert m((-1, -4), (1, 2)) == m((1, 2), (4, 11)) == 3
    assert F(12, 200) == F(6, 100)
    assert m((10, 85000), (25, 160000)) == 5000 and 85000 - 10 * 5000 == 35000
    # subbab 3
    assert 3 * 2 - 7 == -1
    assert m((-2, 5), (4, 2)) == F(-1, 2) and on(1, 2, 8, (-2, 5)) and on(1, 2, 8, (4, 2))
    assert on(-4, 6, -24, (6, 0)) and on(-4, 6, -24, (0, -4)) and F(4, 6) == F(2, 3)
    assert -1 * 4 + 5 == 1 and m((1, 1), (3, 7)) == 3 and 3 - 2 == 1 and on(2, 1, 6, (3, 0)) and on(2, 1, 6, (0, 6))
    assert all(on(2, 3, 12, (x, F(-2, 3) * x + 4)) for x in range(-3, 4))
    assert on(1, -2, -7, (-3, 2)) and F(1, 2) * 0 + F(7, 2) == F(7, 2) and m((-1, -2), (3, 6)) == 2 and 2 * (-1) == -2
    assert on(3, -2, -6, (-2, 0)) and on(3, -2, -6, (0, 3))
    assert F(-1 - 5, 2) == -3 and F(5, 3) * -3 + 5 == 0
    assert ((1 + 5) / 2, (3 + 5) / 2) == (3, 4)
    assert m((2, 35000), (5, 65000)) == 10000 and 35000 - 20000 == 15000 and 10000 * 8 + 15000 == 95000
    assert on(1, 1, 5, (2, 3))
    # subbab 4
    assert meet(1, -1, -1, -2, -1, -7) == (2, 3) or meet(-1, 1, 1, 2, 1, 7) == (2, 3)
    assert meet(2, 3, 12, 5, -2, 11) == (3, 2)
    assert meet(2, 3, 31000, 1, 2, 18000) == (8000, 5000)
    assert meet(-2, 1, 0, -1, 1, 3) == (3, 6) and meet(-3, 1, -1, 0, 1, 5) == (2, 5) and meet(1, 1, 10, 1, -1, 4) == (7, 3) and meet(2, 1, 7, -1, 1, 1) == (2, 3)
    assert meet(1, 1, 4, -1, 2, 2) == (2, 2)
    assert meet(3, 2, 16, 1, -4, -4) == (4, 2) and meet(4, -3, 1, 3, 2, 22) == (4, 5)
    assert 4 * 2 - (-1) * 2 * 2 == 4 * 2 + 4 and (4, -2, 6) == tuple(2 * v for v in (2, -1, 3)) and F(4, 2) == F(-2, -1) != F(1, 3)
    a, j = meet(3, 2, 96000, 1, 4, 72000)
    assert (a, j) == (24000, 12000) and 2 * a + j == 60000
    assert 3 * 2 - 5 == 1 and 2 * -1 + 2 * 5 == 8
    assert meet(-2500, 1, 5000, -2000, 1, 8000) == (6, 20000) and 5000 + 2500 * 10 == 30000 and 8000 + 2000 * 10 == 28000
    assert F(2, 6) == F(3, 9) and F(2, 6) != F(5, 4)
    # subbab 5
    assert F(-1, 4) * 4 == -1 and -1 / F(-2, 3) == F(3, 2) and F(6, 2) == 3 and F(1, 2) * -2 == -1
    assert 2 * 1 + 2 == 4 and on(1, 2, 9, (1, 4)) and F(-1, 2) * 2 == -1
    assert meet(-2, 1, -3, 1, 2, 9) == (3, 3) and on(1, 2, 9, (7, 1)) and on(1, 2, 9, (3, 3)) and close(dist((7, 1), (3, 3)), 2 * math.sqrt(5)) is None
    assert F(-3, 2) * F(2, 3) == -1 and F(-2, -3) == F(2, 3)
    assert on(1, 4, -2, (2, -1)) and F(-1, 4) * 4 == -1 and on(2, 5, 13, (-1, 3)) and F(6, 2) == 3
    assert F(2) * F(-1, 2) == -1 and F(-1, 2) == F(-1, 2) and F(-4, -2) == 2
    assert m((1, 2), (5, 6)) == 1 and on(1, 1, 7, (3, 4)) and dist((1, 2), (7, 0)) == dist((5, 6), (7, 0))
    assert m((-2, 1), (4, 3)) * m((4, 3), (2, 9)) == -1
    assert meet(-1, 1, -3, 1, 1, 9) == (6, 3) and close(dist((4, 5), (6, 3)), 2 * math.sqrt(2)) is None and close(abs(4 - 5 - 3) / math.sqrt(2), 2 * math.sqrt(2)) is None
    # campuran
    assert F(-5, 2) == F(-5, 2) and meet(1, 1, 4, -1, 1, -2) == (3, 1)
    assert m((-2, -3), (3, 7)) == 2
    assert meet(1, 1, 5, 2, -1, 1) == (2, 3) and on(1, 3, 11, (2, 3)) and F(-1, 3) * 3 == -1
    mf = m((2, 1), (-4, 10))
    assert mf == F(-3, 2) and 1 - mf * 2 == 4 and F(-4, mf) == F(8, 3)
    assert meet(-4000, 1, 20000, -2500, 1, 32000) == (8, 52000)
    assert F(8 * 6, 2) == 24
    assert meet(-2, 1, 1, 1, 1, 7) == (2, 5) and F(1, 2) * (7 - F(-1, 2)) * 5 == F(75, 4)
    assert meet(1, -1, 0, 1, 2, 6) == (2, 2) and m((6, 0), (2, 4)) * 1 == -1 and m((0, 0), (2, 4)) * F(-1, 2) == -1
    # TKA
    assert meet(-1, 1, 2, 1, 1, 1) == (F(-1, 2), F(3, 2)) and meet(-1, 1, -1, 1, 1, 1) == (1, 0) and -0 + 1 == 1
    assert on(2, 3, 0, (3, -2)) and F(3, 2) * F(-2, 3) == -1 and on(3, -2, 13, (3, -2)) and on(2, -3, 12, (3, -2)) and on(3, 2, 5, (3, -2)) and on(2, 3, 12, (3, 2))
    assert m((-1, 5), (3, -1)) == F(-3, 2) and F(-(7 - 1), 4) == F(-3, 2) and F(-(-5 - 1), 4) == F(3, 2) and F(-(F(-5, 3) - 1), 4) == F(2, 3) and F(-(F(11, 3) - 1), 4) == F(-2, 3)
    assert F(900, 90) == 10 and 1200 - 400 == 800 == 300 + 500 and 300 + 50 * 90 == 4800 and 300 + 400 == 700 and F(900, 50) == 18 and 1200 - 40 * 18 == 480 and F(900, 40) == F(45, 2) and 1200 - 900 == 300
    B = lambda k: 750 * k + 60000  # noqa: E731
    assert B(0) == 60000 and B(100) - B(0) == 75000 and B(400) != 2 * B(200) and B(320) == 300000 and B(321) > 300000
    yl = lambda x: F(-3, 2) * x + 4  # noqa: E731
    assert m((-2, 7), (4, -2)) == F(-3, 2) and yl(-2) == 7 and yl(0) == 4 and yl(2) == 1 and yl(6) == -5 and yl(1) == F(5, 2) and yl(-4) == 10
    assert meet(-2, 1, 3, 4, -1, 1) == (2, 7) and 2 * F(-1, 2) == -1
    cost = {"P": (1200000, 8000), "Q": (600000, 11000), "S": (0, 15000), "T": (1800000, 4000)}
    at = {k: {d: f + v * d for d in (120, 200, 240)} for k, (f, v) in cost.items()}
    assert [k for k in cost if at[k][240] <= 2800000] == ["T"] and at["T"][240] == 2760000 and min(cost, key=lambda k: at[k][120]) == "S" and at["P"][200] == 2800000
    assert meet(1, 1, 6, 2, -1, 3) == (3, 3) and F(8 - 3, 3) == F(5, 3) and F(8 + 3, 3) == F(11, 3)
    # uji
    assert m((2, -3), (5, 6)) == 3 and F(-6, -2) == 3 and on(4, -3, 12, (3, 0)) and on(4, -3, 12, (0, -4))
    assert -2 * 3 + 7 == 1 and -2 * (0 + 3) + 1 == -5 and -2 * (0 - 3) - 1 == 5 and 2 * 0 - 5 == -5
    assert m((-1, 4), (2, -2)) == -2 and on(2, 1, 2, (-1, 4)) and on(2, 1, 2, (2, -2)) and on(1, 2, 7, (-1, 4)) and on(2, -1, -6, (-1, 4)) and on(1, -2, -9, (-1, 4))
    assert F(-6, -2) == 3 and F(-1, 3) * 3 == -1 and F(-2, 5) * F(5, 2) == -1
    assert meet(-3, 1, -2, 1, 1, 6) == (2, 4) and meet(2, 1, 8, 1, -1, 1) == (3, 2) and F(8 - 1, 3) == F(7, 3) and 8 - 2 * F(7, 3) == F(10, 3)
    assert (3, -6, 9) == tuple(3 * v for v in (1, -2, 3))
    r, s = meet(2, 1, 19000, 1, 3, 22000)
    assert (r, s) == (7000, 5000) and r + s == 12000
    assert F(-3, 2) / -3 * 2 == 1 and F(-F(3, 2), 3) * 2 == -1 and F(6, 3) == 2
    assert m((0, 3), (2, -1)) == -2 and -2 * 1 + 4 == 2 and F(1, 2) * 1 + F(3, 2) == 2
    assert F(142000 - 25000, 6500) == 18 and close(142000 / 6500, 21.85, 0.005) is None and close(167000 / 6500, 25.69, 0.005) is None and F(142000 - 6500, 25000) == F(542, 100)
    assert 25000 + 6500 * (19 - 1) == 142000
    assert meet(1, 1, 1, -1, 1, 1) == (0, 1) and close(dist((3, 4), (0, 1)), 3 * math.sqrt(2)) is None and close(dist((3, 4), (1, 0)), 2 * math.sqrt(5)) is None
    assert m((-1, 7), (3, -1)) == -2 and -2 * -1 + 5 == 7
    assert m((4, -1), (-2, 3)) == F(-2, 3) and on(2, 3, 5, (4, -1)) and on(2, 3, 5, (-2, 3)) and on(2, 3, 5, (1, 1))
    assert meet(5, 2, 4, 3, -4, 18) == (2, -3)
    assert on(2, -3, -7, (1, 3)) and on(3, 2, 9, (1, 3)) and meet(2, -3, 6, 3, 2, 9) == (3, 0) and close(dist((1, 3), (3, 0)), math.sqrt(13)) is None
    A_, B_ = (lambda n: 150000 + 60000 * n), (lambda n: 80000 * n)
    assert F(150000, 20000) == F(15, 2) and A_(8) < B_(8) and A_(7) > B_(7) and A_(12) == 870000 and B_(12) == 960000
    return True
