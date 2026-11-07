"""Content of the printable module "Program Linear" (Matematika kelas X).

Linear inequalities in two variables and their solution regions, systems of inequalities, writing a
linear-programming model from a story, the optimum by testing corner points, and the iso-value line
(garis selidik) with special cases (many optima, integer solutions, empty region).
check() recomputes every corner point from the constraints with exact fractions, every objective value,
and every integer optimum by enumeration.
"""
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import region_plane  # noqa: E402
from kit import fr, Q  # noqa: E402

BLUE, RED, GREEN, GREY = "#1f3a68", "#c0502a", "#2e6b32", "#7a8190"
POS = [(1, 0, ">=", 0), (0, 1, ">=", 0)]  # x ≥ 0, y ≥ 0

PRASYARAT = [
    ("P1", "Tentukan titik potong garis 2x + 3y = 12 dengan sumbu x dan sumbu y.", "(6, 0) dan (0, 4)", "y = 0 → x = 6; x = 0 → y = 4."),
    ("P2", "Apakah titik (2, 1) memenuhi 3x + 2y = 8?", "ya", "6 + 2 = 8."),
    ("P3", "Selesaikan x + y = 6 dan 2x + y = 8.", "x = 2, y = 4", "Kurangkan: x = 2."),
    ("P4", "Selesaikan 3x + 2y = 12 dan x + 2y = 8.", "x = 2, y = 3", "Kurangkan: 2x = 4."),
    ("P5", "Selesaikan 5 − 2x ≥ 1.", "x ≤ 2", "−2x ≥ −4; tanda dibalik."),
    ("P6", "Hitung f(x, y) = 3.000x + 2.500y untuk x = 10 dan y = 20.", "80.000", "30.000 + 50.000."),
    ("P7", "Tentukan persamaan garis yang melalui (4, 0) dan (0, 3).", "3x + 4y = 12", "Potong sumbu (a, 0) dan (0, b): bx + ay = ab."),
    ("P8", "Tulis dengan tanda pertidaksamaan: \"banyak peserta paling sedikit 30\" dan \"biaya tidak lebih dari Rp50.000\".", "x ≥ 30 dan B ≤ 50.000", "\"Paling sedikit\" ≥; \"tidak lebih dari\" ≤."),
]

INGAT = [
    ("A", "Garis lurus", "P1, P2, P7", "Subbab 1, 2", ["Garis ax + by = c memotong sumbu x di (c/a, 0) dan sumbu y di (0, c/b).",
                                                    "Garis melalui (a, 0) dan (0, b): bx + ay = ab."]),
    ("B", "Sistem persamaan linear", "P3, P4", "Subbab 2, 4", ["Eliminasi: samakan koefisien satu variabel, lalu kurangkan atau jumlahkan.", "Uji hasilnya pada kedua persamaan."]),
    ("C", "Pertidaksamaan linear", "P5", "Subbab 1", ["Mengalikan atau membagi dengan bilangan negatif membalik tanda."]),
    ("D", "Menerjemahkan kalimat", "P6, P8", "Subbab 3, 4", ["\"Paling sedikit\", \"minimal\": ≥. \"Paling banyak\", \"maksimal\", \"tersedia\", \"tidak lebih dari\": ≤.",
                                                           "Fungsi objektif f(x, y) = px + qy dihitung dengan mengganti x dan y."]),
]


def RP(xr, yr, cons, points=(), extra=(), labels=(), shade=True, ticks_every=1):
    return region_plane(xr, yr, cons, points=points, extra_segs=extra, labels=labels, shade=shade, ticks_every=ticks_every)


# Figures (the region is shaded; boundary lines solid for ≤/≥, dashed for </>).
FIG_S1A = RP((-1, 7, 1), (-1, 5, 1), [(2, 3, "<=", 12)], points=[(6, 0, "(6, 0)"), (0, 4, "(0, 4)"), (0, 0, "O")])
FIG_S1B = RP((-3, 5, 1), (-4, 4, 1), [(-1, 1, ">", -2)], points=[(2, 0, "(2, 0)"), (0, -2, "(0, −2)")], labels=[(3.1, 2.3, "y = x − 2", "#1f2430")])
BLANK_S1 = RP((-1, 5, 1), (-1, 4, 1), [], shade=False)
KEY_S1 = RP((-1, 5, 1), (-1, 4, 1), [(3, 4, "<=", 12)], points=[(4, 0, "(4, 0)"), (0, 3, "(0, 3)")])
FIG_S1C = RP((-1, 4, 1), (-1, 6, 1), [(5, 2, ">=", 10)], points=[(2, 0, "(2, 0)"), (0, 5, "(0, 5)")])
FIG_SYS = RP((-1, 7, 1), (-1, 7, 1), [(1, 1, "<=", 6), (2, 1, "<=", 8)] + POS, points=[(0, 0, "O"), (4, 0, "(4, 0)"), (2, 4, "(2, 4)"), (0, 6, "(0, 6)")])
FIG_FROMG = RP((-1, 9, 1), (-1, 5, 1), [(1, 2, "<=", 8), (1, 1, ">=", 3)] + POS, points=[(3, 0, "(3, 0)"), (8, 0, "(8, 0)"), (0, 4, "(0, 4)"), (0, 3, "(0, 3)")])
BLANK_S2 = RP((-1, 7, 1), (-1, 7, 1), [], shade=False)
KEY_S2 = RP((-1, 7, 1), (-1, 7, 1), [(2, 1, "<=", 6), (1, 2, "<=", 6)] + POS, points=[(3, 0, ""), (2, 2, "(2, 2)"), (0, 3, "")])
FIG_L23 = RP((-1, 6, 1), (-1, 6, 1), [(1, 1, "<=", 5), (1, 0, "<=", 3)] + POS, points=[(3, 2, "(3, 2)"), (0, 5, "(0, 5)"), (5, 0, "(5, 0)")])
FIG_L210 = RP((-1, 7, 1), (-1, 6, 1), [(1, 0, ">=", 1), (0, 1, ">=", 1), (3, 4, "<=", 19)], points=[(1, 1, "(1, 1)"), (5, 1, "(5, 1)"), (1, 4, "(1, 4)")])
FIG_ROTI = RP((0, 30, 5), (0, 45, 5), [(2, 1, "<=", 40), (1, 2, "<=", 50)] + POS, points=[(20, 0, "(20, 0)"), (10, 20, "(10, 20)"), (0, 25, "(0, 25)")])
FIG_DIET = RP((-1, 10, 1), (-1, 10, 1), [(3, 1, ">=", 9), (1, 2, ">=", 8)] + POS, points=[(0, 9, "(0, 9)"), (2, 3, "(2, 3)"), (8, 0, "(8, 0)")])
FIG_SEL = RP((-1, 7, 1), (-2, 8, 1), [(1, 1, "<=", 6), (2, 1, "<=", 8)] + POS, points=[(4, 0, "(4, 0)"), (2, 4, "(2, 4)"), (0, 6, "(0, 6)")],
             extra=[(-0.5, 3.75, 2.5, -0.75, RED, True), (0.0, 7.0, 4.67, 0.0, RED, True)],
             labels=[(0.2, -1.6, "3x + 2y = 6", RED), (4.2, 1.6, "3x + 2y = 14", RED)])
FIG_T1 = RP((-1, 6, 1), (-1, 5, 1), [(1, 1, "<=", 5), (1, 3, "<=", 9)] + POS, points=[(5, 0, "(5, 0)"), (3, 2, "(3, 2)"), (0, 3, "(0, 3)")])

SUB = []

# ================================================================== Subbab 1
SUB.append(dict(
    title="Pertidaksamaan Linear Dua Variabel",
    tujuan="Menggambar daerah penyelesaian pertidaksamaan linear dua variabel dengan garis batas dan uji titik, serta menentukan pertidaksamaan dari daerahnya.",
    konsep=[
        "Pertidaksamaan linear dua variabel berbentuk ax + by ≤ c (atau &lt;, ≥, &gt;). Penyelesaiannya adalah semua titik (x, y) yang memenuhi, yang membentuk <b>setengah bidang</b>, yaitu daerah di salah satu sisi garis ax + by = c.",
        "Langkah: (1) gambar <b>garis batas</b> ax + by = c dari dua titik potong sumbu; garis <b>penuh</b> untuk ≤ atau ≥, <b>putus-putus</b> untuk &lt; atau &gt;; (2) <b>uji satu titik</b> di luar garis, biasanya (0, 0); (3) jika benar, daerah penyelesaian adalah sisi yang memuat titik itu; jika salah, sisi seberangnya.",
        "Jika garis batas melalui (0, 0), pakai titik uji lain, misalnya (1, 0) atau (0, 1).",
        "<b>Konvensi modul ini:</b> daerah penyelesaian (DP) <b>diarsir</b>. Sebagian buku mengarsir daerah yang bukan penyelesaian, jadi bacalah keterangan gambar pada setiap soal.",
    ],
    rumus=["Garis batas ax + by = c melalui (" + fr("c", "a") + ", 0) dan (0, " + fr("c", "b") + ")", "≤, ≥: garis penuh; &lt;, &gt;: garis putus-putus",
           "Uji (0, 0): benar → DP memuat O; salah → DP di seberang O", "x ≥ k: kanan garis tegak x = k; y ≤ k: bawah garis mendatar y = k"],
    contoh=[
        ("Garis penuh", "Gambarkan daerah penyelesaian 2x + 3y ≤ 12.", FIG_S1A,
         ["Garis batas 2x + 3y = 12 melalui (6, 0) dan (0, 4); digambar penuh karena tanda ≤.", "Uji (0, 0): 0 ≤ 12 benar.", "DP adalah sisi garis yang memuat O (diarsir)."],
         "setengah bidang di bawah garis, memuat O"),
        ("Garis putus-putus", "Gambarkan daerah penyelesaian y &gt; x − 2.", FIG_S1B,
         ["Garis batas y = x − 2 melalui (2, 0) dan (0, −2); putus-putus karena tanda &gt;.", "Uji (0, 0): 0 &gt; −2 benar.", "DP adalah sisi yang memuat O, yaitu di atas garis; titik pada garis tidak termasuk."],
         "di atas garis y = x − 2, garis tidak termasuk"),
    ],
    bertahap=dict(
        soal="Tentukan daerah penyelesaian x − 2y ≥ −4.",
        langkah=["Titik potong garis x − 2y = −4: dengan sumbu x (____, 0), dengan sumbu y (0, ____).", "Garis digambar ____ karena tandanya ≥.", "Uji (0, 0): 0 ≥ −4 bernilai ____, jadi DP ____ titik O."],
        cek="Titik (0, 0) boleh dipakai sebagai titik uji karena",
        opsi=["(a) (0, 0) tidak terletak pada garis batas", "(b) (0, 0) selalu termasuk daerah penyelesaian"],
        kunci="(−4, 0) dan (0, 2); penuh; benar, memuat. Alasan: (a).",
    ),
    jebakan=["Garis untuk &lt; atau &gt; digambar putus-putus; titik pada garis itu tidak termasuk penyelesaian.",
             "Jangan menebak \"≤ berarti di bawah garis\": untuk −x + 2y ≤ 4 memang di bawah, tetapi untuk x − 2y ≤ 4 di atas. Selalu uji satu titik.",
             "Jika garis melalui O, titik (0, 0) tidak dapat dipakai sebagai titik uji.",
             "Perhatikan konvensi arsiran: DP yang diarsir atau DP yang bersih."],
    latihan=[
        Q(1, "Apakah titik (2, 1) memenuhi 3x + 2y ≤ 10?", "ya", "6 + 2 = 8 ≤ 10."),
        Q(1, "Tentukan titik potong garis batas 4x + 5y ≤ 20 dengan kedua sumbu.", "(5, 0) dan (0, 4)", "y = 0 → x = 5; x = 0 → y = 4."),
        Q(1, "Garis batas y &lt; 2x + 1 digambar penuh atau putus-putus?", "putus-putus", "Tanda &lt; tidak memuat garis."),
        Q(1, "Uji (0, 0) pada x + y ≥ 3. Apakah DP memuat O?", "tidak", "0 ≥ 3 salah."),
        Q(1, "Di sisi mana garis x = 2 letak daerah penyelesaian x ≥ 2?", "di kanan garis x = 2, garis termasuk", "x bernilai 2 atau lebih."),
        Q(2, "Gambarlah daerah penyelesaian 3x + 4y ≤ 12 pada bidang berikut.", "di bawah garis melalui (4, 0) dan (0, 3), memuat O", "Uji (0, 0): 0 ≤ 12 benar.", fig=BLANK_S1, kfig=KEY_S1),
        Q(2, "Daerah penyelesaian x − y &gt; 1 terletak di sisi mana garis x − y = 1, dan apakah garisnya termasuk?", "di sisi yang tidak memuat O (kanan bawah); garis tidak termasuk",
          "Garis melalui (1, 0) dan (0, −1); uji (0, 0): 0 &gt; 1 salah."),
        Q(2, "Mengapa titik (0, 0) tidak dapat dipakai untuk menguji 2x − 3y ≥ 0? Ujilah dengan titik lain.", "garis melalui O; uji (1, 0): 2 ≥ 0 benar, jadi DP memuat (1, 0)", "2 · 0 − 3 · 0 = 0 terletak tepat pada garis."),
        Q(2, "Tentukan nilai k agar titik (k, 2) memenuhi 2x + 5y ≤ 20.", "k ≤ 5", "2k + 10 ≤ 20."),
        Q(3, "Tentukan pertidaksamaan yang daerah penyelesaiannya diarsir pada gambar berikut.", "5x + 2y ≥ 10", "Garis melalui (2, 0) dan (0, 5): 5x + 2y = 10; DP tidak memuat O dan garisnya penuh.", fig=FIG_S1C),
        Q(3, "Uang Rp60.000 dipakai untuk membeli x buku seharga Rp12.000 dan y pulpen seharga Rp4.000. Tulis pertidaksamaannya dalam bentuk sederhana, lalu periksa apakah (3, 5) dan (4, 4) mungkin.", "3x + y ≤ 15; (3, 5) mungkin, (4, 4) tidak",
          "12.000x + 4.000y ≤ 60.000 dibagi 4.000; 9 + 5 = 14 ≤ 15; 12 + 4 = 16 &gt; 15."),
        Q(3, "Titik mana saja yang memenuhi y ≥ 2x: (1, 3), (2, 3), (−1, 0)?", "(1, 3) dan (−1, 0)", "3 ≥ 2 benar; 3 ≥ 4 salah; 0 ≥ −2 benar."),
    ],
))

# ================================================================== Subbab 2
SUB.append(dict(
    title="Sistem Pertidaksamaan Linear Dua Variabel",
    tujuan="Menentukan daerah penyelesaian dan titik pojok sistem pertidaksamaan linear dua variabel, serta menyusun sistem dari daerah yang diketahui.",
    konsep=[
        "Daerah penyelesaian <b>sistem</b> adalah irisan daerah penyelesaian setiap pertidaksamaannya. Kendala x ≥ 0 dan y ≥ 0 membatasi DP di kuadran I.",
        "<b>Titik pojok</b> adalah titik sudut DP. Titik pojok pada sumbu dibaca dari titik potong garis dengan sumbu; titik pojok di tengah dicari dengan menyelesaikan dua persamaan garis yang berpotongan di sana.",
        "Menyusun sistem dari gambar: (1) tentukan persamaan setiap garis batas dari dua titik yang dilaluinya; (2) tentukan tandanya dengan menguji satu titik di dalam DP; (3) tambahkan x ≥ 0, y ≥ 0 bila DP di kuadran I.",
        "DP dapat <b>tertutup</b> (terbatas, berbentuk poligon), <b>terbuka</b> (tak terbatas ke satu arah), atau <b>kosong</b> bila tidak ada titik yang memenuhi semua kendala.",
    ],
    rumus=["DP sistem = irisan DP semua pertidaksamaan", "Titik pojok tengah: selesaikan dua persamaan garis", "Garis melalui (a, 0) dan (0, b): bx + ay = ab",
           "Tanda: uji satu titik di dalam DP"],
    contoh=[
        ("Daerah dan titik pojok", "Gambarkan DP sistem x + y ≤ 6, 2x + y ≤ 8, x ≥ 0, y ≥ 0, lalu tentukan titik pojoknya.", FIG_SYS,
         ["Garis x + y = 6 melalui (6, 0) dan (0, 6); garis 2x + y = 8 melalui (4, 0) dan (0, 8). Uji (0, 0) benar untuk keduanya.",
          "Titik potong kedua garis: kurangkan, x = 2, lalu y = 4.", "Titik pojok: O(0, 0), (4, 0), (2, 4), dan (0, 6). Titik (6, 0) dan (0, 8) tidak termasuk karena melanggar salah satu kendala."],
         "(0, 0), (4, 0), (2, 4), (0, 6)"),
        ("Sistem dari gambar", "Tentukan sistem pertidaksamaan yang DP-nya diarsir pada gambar.", FIG_FROMG,
         ["Garis melalui (8, 0) dan (0, 4): 4x + 8y = 32, atau x + 2y = 8. Garis melalui (3, 0) dan (0, 3): x + y = 3.",
          "Uji titik (2, 2) di dalam DP: 2 + 4 = 6 ≤ 8 dan 2 + 2 = 4 ≥ 3.", "DP di kuadran I, jadi x ≥ 0 dan y ≥ 0."],
         "x + 2y ≤ 8, x + y ≥ 3, x ≥ 0, y ≥ 0"),
    ],
    bertahap=dict(
        soal="Tentukan titik pojok DP sistem x + 3y ≤ 9, 2x + y ≤ 8, x ≥ 0, y ≥ 0.",
        langkah=["Pada sumbu x: x + 3y = 9 memberi (9, 0), 2x + y = 8 memberi (____, 0); yang dipakai adalah yang lebih ____.", "Pada sumbu y: (0, 3) dan (0, 8); yang dipakai (0, ____).",
                 "Titik potong: x = 9 − 3y, jadi 2(9 − 3y) + y = 8 → y = ____, x = ____.", "Titik pojok: (0, 0), (4, 0), (____, ____), (0, 3)."],
        cek="Pada sumbu x dipilih titik yang lebih dekat ke O karena",
        opsi=["(a) titik yang lebih jauh melanggar kendala yang lain", "(b) titik pojok selalu bilangan kecil"],
        kunci="(4, 0), dekat; 3; y = 2, x = 3; (3, 2). Alasan: (a).",
    ),
    jebakan=["Titik potong garis dengan sumbu belum tentu titik pojok; periksa apakah titik itu memenuhi semua kendala.",
             "Tanda pertidaksamaan dari gambar ditentukan dengan menguji titik di <b>dalam</b> DP.",
             "Jangan lupa x ≥ 0 dan y ≥ 0 bila DP berada di kuadran I."],
    latihan=[
        Q(1, "Apakah titik (1, 2) termasuk DP sistem x + y ≤ 4, x − y ≤ 1, x ≥ 0, y ≥ 0?", "ya", "3 ≤ 4 dan −1 ≤ 1."),
        Q(1, "Tentukan titik pojok DP sistem x + y ≤ 5, x ≥ 0, y ≥ 0.", "(0, 0), (5, 0), (0, 5)", "Segitiga di kuadran I."),
        Q(1, "Daerah yang memenuhi x ≥ 0 dan y ≥ 0 disebut apa?", "kuadran I (beserta sumbunya)", "x dan y tidak negatif."),
        Q(1, "Tentukan titik potong garis x + y = 7 dan x − y = 1.", "(4, 3)", "Jumlahkan: 2x = 8."),
        Q(1, "Tentukan titik pojok DP sistem x ≤ 3, y ≤ 2, x ≥ 0, y ≥ 0.", "(0, 0), (3, 0), (3, 2), (0, 2)", "DP berbentuk persegi panjang."),
        Q(2, "Gambarlah DP sistem 2x + y ≤ 6, x + 2y ≤ 6, x ≥ 0, y ≥ 0 dan tentukan titik pojoknya.", "(0, 0), (3, 0), (2, 2), (0, 3)", "Titik potong: kurangkan 2 × persamaan kedua, 3y = 6.",
          fig=BLANK_S2, kfig=KEY_S2),
        Q(2, "Tentukan titik pojok DP sistem 3x + 2y ≤ 12, x + 2y ≤ 8, x ≥ 0, y ≥ 0.", "(0, 0), (4, 0), (2, 3), (0, 4)", "Kurangkan: 2x = 4 → x = 2, y = 3."),
        Q(2, "Tentukan sistem pertidaksamaan yang DP-nya diarsir pada gambar.", "x + y ≤ 5, x ≤ 3, x ≥ 0, y ≥ 0", "Garis melalui (5, 0) dan (0, 5), dan garis tegak x = 3; uji (1, 1).", fig=FIG_L23),
        Q(2, "Tunjukkan bahwa sistem x + y ≥ 4 dan x + y ≤ 2 tidak mempunyai penyelesaian.", "DP kosong", "Tidak ada bilangan x + y yang sekaligus ≥ 4 dan ≤ 2; kedua garis sejajar."),
        Q(3, "Tentukan sistem pertidaksamaan untuk DP segitiga pada gambar.", "x ≥ 1, y ≥ 1, 3x + 4y ≤ 19", "Garis miring melalui (5, 1) dan (1, 4): gradien −¾, 3x + 4y = 19; uji (2, 2): 14 ≤ 19.", fig=FIG_L210),
        Q(3, "Hitung luas DP sistem x + y ≤ 6, y ≤ 2x, y ≥ 0.", "12 satuan luas", "Titik pojok O, (6, 0), dan (2, 4); luas ½ · 6 · 4."),
        Q(3, "Berapa banyak titik (x, y) dengan x dan y bilangan bulat yang termasuk DP x + y ≤ 3, x ≥ 0, y ≥ 0?", "10", "Untuk x = 0, 1, 2, 3 ada 4, 3, 2, 1 nilai y."),
    ],
))

# ================================================================== Subbab 3
SUB.append(dict(
    title="Model Matematika",
    tujuan="Menerjemahkan masalah sehari-hari menjadi model program linear: variabel, kendala, dan fungsi objektif.",
    konsep=[
        "<b>Program linear</b> adalah cara menentukan nilai optimum (maksimum atau minimum) sebuah <b>fungsi objektif</b> f(x, y) = px + qy dengan syarat x dan y memenuhi sistem pertidaksamaan linear yang disebut <b>kendala</b>.",
        "Langkah: (1) tentukan arti x dan y beserta satuannya; (2) susun data dalam tabel (baris: jenis sumber daya, kolom: x, y, dan persediaan); (3) setiap baris menjadi satu kendala; (4) tambahkan x ≥ 0, y ≥ 0; (5) tulis fungsi objektif.",
        "Sumber daya yang \"tersedia\", \"paling banyak\", atau \"kapasitas\" memberi tanda ≤. Kebutuhan \"paling sedikit\" atau \"minimal\" memberi tanda ≥.",
        "Bila x dan y menyatakan banyak barang atau orang, keduanya juga harus bilangan bulat. Sederhanakan kendala dengan membagi kedua ruas dengan faktor persekutuan.",
    ],
    rumus=["Fungsi objektif: f(x, y) = px + qy (maksimumkan atau minimumkan)", "Kendala dari tabel: a₁x + b₁y ≤ c₁ (tersedia), a₂x + b₂y ≥ c₂ (kebutuhan)", "x ≥ 0, y ≥ 0 (dan bulat bila perlu)"],
    contoh=[
        ("Memaksimumkan untung", "Roti A memerlukan 200 g tepung dan 50 g mentega; roti B 100 g tepung dan 100 g mentega. Tersedia 4 kg tepung dan 2,5 kg mentega. Untung roti A Rp3.000 dan roti B Rp2.500. Susun modelnya.", None,
         ["Misalkan x banyak roti A dan y banyak roti B.", "Tepung: 200x + 100y ≤ 4.000 → 2x + y ≤ 40. Mentega: 50x + 100y ≤ 2.500 → x + 2y ≤ 50.", "x ≥ 0, y ≥ 0, bulat. Maksimumkan f(x, y) = 3.000x + 2.500y."],
         "2x + y ≤ 40, x + 2y ≤ 50, x, y ≥ 0; maks f = 3.000x + 2.500y"),
        ("Meminimumkan biaya", "Pakan P mengandung 3 unit vitamin A dan 1 unit vitamin B per kg, seharga Rp4.000 per kg. Pakan Q mengandung 1 unit vitamin A dan 2 unit vitamin B per kg, seharga Rp3.000 per kg. Ternak memerlukan paling sedikit 9 unit vitamin A dan 8 unit vitamin B. Susun modelnya.", None,
         ["Misalkan x kg pakan P dan y kg pakan Q.", "Vitamin A: 3x + y ≥ 9. Vitamin B: x + 2y ≥ 8. Tandanya ≥ karena kebutuhan minimal.", "x ≥ 0, y ≥ 0. Minimumkan f(x, y) = 4.000x + 3.000y."],
         "3x + y ≥ 9, x + 2y ≥ 8, x, y ≥ 0; min f = 4.000x + 3.000y"),
    ],
    bertahap=dict(
        soal="Lahan parkir seluas 480 m² dapat menampung paling banyak 50 kendaraan. Sebuah mobil memerlukan 6 m² dan sebuah bus 24 m². Tarif parkir mobil Rp5.000 dan bus Rp10.000. Susun model untuk memaksimumkan pendapatan.",
        langkah=["Misalkan x banyak mobil dan y banyak bus.", "Banyak kendaraan: x + y ____ 50.", "Luas: 6x + 24y ≤ ____, disederhanakan menjadi x + 4y ≤ ____.", "x ≥ 0, y ≥ 0; maksimumkan f(x, y) = ____."],
        cek="Tanda kendala luas adalah ≤ karena",
        opsi=["(a) luas yang terpakai tidak boleh melebihi luas lahan", "(b) bus lebih besar daripada mobil"],
        kunci="≤; 480; 80; 5.000x + 10.000y. Alasan: (a).",
    ),
    jebakan=["Jangan menukar baris dan kolom tabel: satu kendala memuat satu jenis sumber daya untuk kedua produk.",
             "Satuan harus sama: 4 kg tepung = 4.000 g bila kebutuhan per roti ditulis dalam gram.",
             "\"Tersedia\" berarti ≤, bukan ≥.",
             "Kendala x ≥ 0 dan y ≥ 0 jarang disebut dalam soal, tetapi tetap ditulis."],
    latihan=[
        Q(1, "Tulis dengan pertidaksamaan: \"banyak kursi x paling sedikit 20\".", "x ≥ 20", "\"Paling sedikit\" berarti ≥."),
        Q(1, "Harga pensil Rp2.000 dan buku Rp5.000. Tulis kendala untuk x pensil dan y buku jika uangnya paling banyak Rp40.000.", "2x + 5y ≤ 40", "2.000x + 5.000y ≤ 40.000, dibagi 1.000."),
        Q(1, "Sebuah kelas memuat paling banyak 36 siswa. Tulis kendala untuk x siswa laki-laki dan y siswa perempuan.", "x + y ≤ 36", "Jumlah siswa tidak melebihi kapasitas."),
        Q(1, "Untung produk A Rp4.000 per unit dan produk B Rp6.000 per unit. Tulis fungsi objektifnya.", "f(x, y) = 4.000x + 6.000y", "Untung per unit dikali banyaknya."),
        Q(1, "Mengapa model program linear memuat x ≥ 0 dan y ≥ 0?", "banyak barang tidak mungkin negatif", "x dan y menyatakan banyak barang."),
        Q(2, "Sebuah kemeja memerlukan 2 m kain katun dan 1 m kain sutra; sebuah gaun 1 m katun dan 2 m sutra. Tersedia 20 m katun dan 16 m sutra. Susun kendalanya.", "2x + y ≤ 20, x + 2y ≤ 16, x ≥ 0, y ≥ 0",
          "x kemeja, y gaun; satu baris per jenis kain."),
        Q(2, "Pedagang buah bermodal Rp1.200.000 membeli mangga Rp8.000 per kg dan jeruk Rp6.000 per kg. Gerobaknya memuat paling banyak 180 kg. Susun kendalanya.", "4x + 3y ≤ 600, x + y ≤ 180, x ≥ 0, y ≥ 0",
          "8.000x + 6.000y ≤ 1.200.000 dibagi 2.000."),
        Q(2, "Produk A memerlukan 2 jam di mesin I dan 1 jam di mesin II; produk B 1 jam di mesin I dan 3 jam di mesin II. Mesin I tersedia 12 jam dan mesin II 16 jam. Susun kendalanya.", "2x + y ≤ 12, x + 3y ≤ 16, x ≥ 0, y ≥ 0",
          "Satu kendala untuk setiap mesin."),
        Q(2, "Pakan jenis I mengandung 2 unit karbohidrat dan 1 unit protein per kg; jenis II 1 unit karbohidrat dan 2 unit protein. Kebutuhan paling sedikit 10 unit karbohidrat dan 8 unit protein. Susun kendalanya.", "2x + y ≥ 10, x + 2y ≥ 8, x ≥ 0, y ≥ 0",
          "Kebutuhan minimal memberi tanda ≥."),
        Q(3, "Sebanyak 360 peserta akan diangkut dengan bus A (40 kursi, sewa Rp2.000.000) dan bus B (30 kursi, sewa Rp1.200.000). Tersedia paling banyak 10 bus. Susun model untuk meminimumkan biaya, lalu periksa apakah 6 bus A dan 4 bus B memenuhi dan berapa biayanya.",
          "4x + 3y ≥ 36, x + y ≤ 10, x, y ≥ 0 bulat; min f = 2.000.000x + 1.200.000y; memenuhi, Rp16.800.000", "40x + 30y ≥ 360 dibagi 10; 24 + 12 = 36 dan 6 + 4 = 10."),
        Q(3, "Petani mempunyai lahan 10 ha untuk padi dan jagung. Modal per hektare: padi Rp4 juta, jagung Rp2 juta; modal tersedia Rp32 juta. Untung per hektare: padi Rp3 juta, jagung Rp2 juta. Susun modelnya.", "x + y ≤ 10, 2x + y ≤ 16, x, y ≥ 0; maks f = 3x + 2y (juta rupiah)",
          "Modal: 4x + 2y ≤ 32 dibagi 2."),
        Q(3, "Seorang siswa menulis kendala 2x + y ≥ 20 untuk \"kain katun yang tersedia 20 m\". Jelaskan kesalahannya.", "tandanya harus ≤", "Kain yang terpakai tidak boleh melebihi persediaan."),
    ],
))

# ================================================================== Subbab 4
SUB.append(dict(
    title="Nilai Optimum dengan Uji Titik Pojok",
    tujuan="Menentukan nilai maksimum dan minimum fungsi objektif dengan menguji titik pojok daerah penyelesaian, dan menafsirkan hasilnya dalam konteks.",
    konsep=[
        "Jika DP tertutup dan tidak kosong, nilai maksimum dan minimum f(x, y) = px + qy <b>selalu dicapai di titik pojok</b>. Jadi cukup menghitung f di setiap titik pojok, lalu memilih yang terbesar atau terkecil.",
        "Langkah: (1) susun model; (2) gambar DP; (3) tentukan semua titik pojok, termasuk titik potong dua garis; (4) hitung f di setiap titik pojok dalam tabel; (5) jawab pertanyaan dalam konteks soal.",
        "Pada DP terbuka (tak terbatas), nilai minimum dengan p, q &gt; 0 tetap dicapai di titik pojok, tetapi nilai maksimumnya tidak ada karena f dapat dibuat sebesar mungkin.",
        "Jawaban akhir menyebut banyak setiap barang <b>dan</b> nilai optimumnya, misalnya \"10 roti A dan 20 roti B dengan untung Rp80.000\".",
    ],
    rumus=["DP tertutup: nilai optimum di salah satu titik pojok", "Tabel uji: titik pojok | f(x, y)", "DP terbuka (p, q &gt; 0): minimum ada, maksimum tidak ada"],
    contoh=[
        ("Untung maksimum", "Lanjutkan model roti (2x + y ≤ 40, x + 2y ≤ 50, x, y ≥ 0, f = 3.000x + 2.500y). Tentukan untung maksimum.", FIG_ROTI,
         ["Titik potong 2x + y = 40 dan x + 2y = 50: kalikan persamaan pertama dengan 2 dan kurangkan, 3x = 30 → x = 10, y = 20.",
          "Titik pojok dan nilai f: (0, 0) → 0; (20, 0) → 60.000; (10, 20) → 80.000; (0, 25) → 62.500.", "Nilai terbesar di (10, 20)."],
         "10 roti A dan 20 roti B, untung Rp80.000"),
        ("Biaya minimum", "Lanjutkan model pakan (3x + y ≥ 9, x + 2y ≥ 8, x, y ≥ 0, f = 4.000x + 3.000y). Tentukan biaya minimum.", FIG_DIET,
         ["DP terbuka ke kanan atas. Titik potong: x = 8 − 2y, jadi 3(8 − 2y) + y = 9 → y = 3, x = 2.",
          "Titik pojok dan nilai f: (0, 9) → 27.000; (2, 3) → 17.000; (8, 0) → 32.000.", "Nilai terkecil di (2, 3)."],
         "2 kg pakan P dan 3 kg pakan Q, biaya Rp17.000"),
    ],
    bertahap=dict(
        soal="Tentukan nilai maksimum f(x, y) = 5x + 4y pada DP x + y ≤ 6, 2x + y ≤ 10, x ≥ 0, y ≥ 0.",
        langkah=["Titik pojok pada sumbu: (0, 0), (____, 0), (0, ____).", "Titik potong: kurangkan kedua persamaan, x = ____, y = ____.", "Nilai f: 0; 25; ____; 24. Nilai maksimum ____ di (____, ____)."],
        cek="Hanya titik pojok yang diuji karena",
        opsi=["(a) pada DP tertutup nilai optimum fungsi linear dicapai di titik pojok", "(b) titik di dalam DP tidak memenuhi kendala"],
        kunci="(5, 0), (0, 6); x = 4, y = 2; 28; maksimum 28 di (4, 2). Alasan: (a).",
    ),
    jebakan=["Titik potong dua garis harus dihitung, jangan ditaksir dari gambar.",
             "Jangan memasukkan titik potong garis dengan sumbu yang berada di luar DP, misalnya (0, 40) pada contoh roti.",
             "Pada DP terbuka, jangan menyimpulkan nilai maksimum dari titik pojok saja.",
             "Jawab dalam konteks: banyak barang dan nilai optimumnya."],
    latihan=[
        Q(1, "Titik pojok DP adalah (0, 0), (4, 0), (3, 2), dan (0, 4). Tentukan nilai maksimum f = 3x + 2y.", "13 di (3, 2)", "Nilai: 0, 12, 13, 8."),
        Q(1, "Titik pojok DP adalah (0, 3), (2, 1), dan (5, 0). Tentukan nilai minimum f = 2x + 5y.", "9 di (2, 1)", "Nilai: 15, 9, 10."),
        Q(1, "Tentukan nilai maksimum f = x + y pada DP x ≤ 4, y ≤ 3, x ≥ 0, y ≥ 0.", "7 di (4, 3)", "Titik pojok (0, 0), (4, 0), (4, 3), (0, 3)."),
        Q(1, "DP berbentuk segitiga dengan titik pojok (0, 0), (6, 0), dan (0, 8). Tentukan nilai maksimum f = 4x + y.", "24 di (6, 0)", "Nilai: 0, 24, 8."),
        Q(1, "Mengapa nilai optimum dicari di titik pojok, bukan di titik lain di dalam DP?", "pada DP tertutup, nilai optimum fungsi linear selalu dicapai di titik pojok", "Lihat Konsep."),
        Q(2, "Tentukan nilai maksimum f = 2x + 3y pada DP 3x + 2y ≤ 12, x + 2y ≤ 8, x ≥ 0, y ≥ 0.", "13 di (2, 3)", "Titik pojok (0, 0), (4, 0), (2, 3), (0, 4); nilai 0, 8, 13, 12."),
        Q(2, "Tentukan nilai minimum f = 3x + 2y pada DP x + y ≥ 4, x + 3y ≥ 6, x ≥ 0, y ≥ 0.", "8 di (0, 4)", "Titik pojok (0, 4), (3, 1), (6, 0); nilai 8, 11, 18."),
        Q(2, "Lanjutkan model petani (x + y ≤ 10, 2x + y ≤ 16, x, y ≥ 0, f = 3x + 2y juta rupiah). Tentukan luas padi dan jagung agar untung maksimum.", "6 ha padi dan 4 ha jagung, untung Rp26 juta",
          "Titik pojok (0, 0), (8, 0), (6, 4), (0, 10); nilai 0, 24, 26, 20."),
        Q(2, "Lanjutkan model kemeja dan gaun (2x + y ≤ 20, x + 2y ≤ 16, x, y ≥ 0). Untung kemeja Rp30.000 dan gaun Rp40.000. Tentukan untung maksimum.", "8 kemeja dan 4 gaun, Rp400.000",
          "Titik pojok (0, 0), (10, 0), (8, 4), (0, 8); nilai 0, 300.000, 400.000, 320.000."),
        Q(3, "Lanjutkan model mesin (2x + y ≤ 12, x + 3y ≤ 16, x, y ≥ 0). Untung produk A Rp40.000 dan produk B Rp30.000. Tentukan untung maksimum.", "4 produk A dan 4 produk B, Rp280.000",
          "Titik pojok (0, 0), (6, 0), (4, 4), (0, 16/3); nilai 0, 240.000, 280.000, 160.000."),
        Q(3, "Lanjutkan model bus (4x + 3y ≥ 36, x + y ≤ 10, x, y ≥ 0). Tentukan biaya sewa minimum.", "6 bus A dan 4 bus B, Rp16.800.000",
          "DP segitiga dengan titik pojok (9, 0), (10, 0), (6, 4); biaya 18, 20, dan 16,8 juta rupiah. Titik (0, 12) melanggar x + y ≤ 10."),
        Q(3, "Tunjukkan bahwa f = 4.000x + 3.000y tidak mempunyai nilai maksimum pada DP 3x + y ≥ 9, x + 2y ≥ 8, x ≥ 0, y ≥ 0.", "DP terbuka, f dapat dibuat sebesar mungkin",
          "Titik (n, n) dengan n ≥ 3 memenuhi semua kendala, dan f(n, n) = 7.000n makin besar bila n makin besar."),
    ],
))

# ================================================================== Subbab 5
SUB.append(dict(
    title="Garis Selidik dan Kasus Khusus",
    tujuan="Memakai garis selidik untuk menemukan titik optimum, serta menangani optimum di banyak titik, penyelesaian bilangan bulat, dan daerah penyelesaian kosong.",
    konsep=[
        "<b>Garis selidik</b> f(x, y) = px + qy = k menghubungkan semua titik yang nilai f-nya sama, k. Mengubah k menggeser garis itu secara sejajar (gradien −" + fr("p", "q") + ").",
        "Untuk p, q &gt; 0, menggeser garis selidik menjauhi O memperbesar k. Titik DP yang <b>terakhir</b> disentuh garis selidik adalah titik maksimum; titik yang <b>pertama</b> disentuh adalah titik minimum.",
        "Jika garis selidik sejajar salah satu sisi DP, nilai optimum dicapai di <b>semua titik pada sisi itu</b>, termasuk kedua titik pojok ujungnya.",
        "Bila x dan y harus bulat tetapi titik pojok optimum tidak bulat, periksa titik-titik bulat di dalam DP di dekatnya; membulatkan begitu saja dapat menghasilkan titik di luar DP. DP kosong berarti masalahnya tidak mempunyai penyelesaian.",
    ],
    rumus=["Garis selidik: px + qy = k, gradien −" + fr("p", "q"), "p, q &gt; 0: titik terakhir yang disentuh saat menjauhi O → maksimum", "Garis selidik sejajar sisi DP: optimum di sepanjang sisi itu",
           "Penyelesaian bulat: periksa titik bulat di DP dekat titik pojok optimum"],
    contoh=[
        ("Garis selidik", "Pakai garis selidik untuk menentukan nilai maksimum f = 3x + 2y pada DP x + y ≤ 6, 2x + y ≤ 8, x ≥ 0, y ≥ 0.", FIG_SEL,
         ["Gambar garis selidik awal 3x + 2y = 6 (melalui (2, 0) dan (0, 3)).", "Geser sejajar menjauhi O. Titik DP terakhir yang disentuh adalah (2, 4).",
          "f(2, 4) = 6 + 8 = 14. Cek: f(4, 0) = 12 dan f(0, 6) = 12, keduanya lebih kecil."], "maksimum 14 di (2, 4)"),
        ("Optimum di banyak titik", "Tentukan nilai maksimum f = 2x + 2y pada DP yang sama.", None,
         ["Nilai di titik pojok: (0, 0) → 0; (4, 0) → 8; (2, 4) → 12; (0, 6) → 12.", "Garis selidik 2x + 2y = k sejajar sisi x + y = 6, yang menghubungkan (2, 4) dan (0, 6).",
          "Maksimum 12 dicapai di setiap titik pada sisi itu, misalnya (1, 5)."], "maksimum 12 di sepanjang ruas dari (2, 4) ke (0, 6)"),
    ],
    bertahap=dict(
        soal="Tentukan nilai maksimum f = 5x + 4y pada DP x + y ≤ 5, 3x + y ≤ 10, x ≥ 0, y ≥ 0, dengan x dan y bilangan bulat.",
        langkah=["Titik potong kedua garis: 2x = 5 → x = ____, y = ____; nilai f di sana 22,5.", "Titik pojok lain: (" + fr("10", "3") + ", 0) → f ≈ 16,7 dan (0, 5) → f = ____.",
                 "Periksa titik bulat di dekat (2½, 2½): (2, 3) → f = ____ dan memenuhi kendala; (3, 2) → 3 · 3 + 2 = ____ &gt; 10, melanggar.", "Nilai maksimum bulat ____ di (____, ____)."],
        cek="Titik (3, 2) tidak boleh dipakai karena",
        opsi=["(a) titik itu berada di luar DP", "(b) nilai f di titik itu terlalu kecil"],
        kunci="x = 2½, y = 2½; 20; 22; 11; maksimum 22 di (2, 3). Alasan: (a).",
    ),
    jebakan=["Garis selidik harus sejajar fungsi objektif px + qy = k, bukan sejajar salah satu kendala.",
             "Membulatkan titik pojok tidak bulat dapat menghasilkan titik di luar DP; periksa setiap kendala.",
             "Jika dua titik pojok bernilai sama dan optimum, semua titik pada ruas di antaranya juga optimum.",
             "Untuk minimum, cari titik yang pertama disentuh, bukan yang terakhir."],
    latihan=[
        Q(1, "Tentukan persamaan garis selidik f = 2x + 5y yang melalui (1, 2).", "2x + 5y = 12", "k = f(1, 2) = 12."),
        Q(1, "Tentukan gradien garis selidik f = 3x + 4y.", "−¾", "3x + 4y = k → y = −¾x + k/4."),
        Q(1, "Titik (1, 5) dan (4, 2) terletak pada satu garis selidik f = x + y. Apa artinya?", "nilai f di kedua titik sama, yaitu 6", "1 + 5 = 4 + 2."),
        Q(1, "Apakah sistem x + y ≤ 2, x + y ≥ 5 mempunyai nilai optimum?", "tidak, DP kosong", "Tidak ada titik yang memenuhi keduanya."),
        Q(1, "Titik pojok optimum (2½, 1½), tetapi x dan y menyatakan banyak barang. Apa yang harus dilakukan?", "periksa titik bulat di DP di sekitarnya", "Barang tidak dapat dibagi."),
        Q(2, "DP mempunyai titik pojok (0, 0), (5, 0), (3, 4), dan (0, 6). Tentukan nilai maksimum f = 4x + 3y.", "24 di (3, 4)", "Nilai: 0, 20, 24, 18; garis selidik terakhir menyentuh (3, 4)."),
        Q(2, "Pada DP 2x + y ≤ 10, 2x + 3y ≤ 18, x ≥ 0, y ≥ 0, tentukan nilai maksimum f = 4x + 2y dan banyak titik bulat yang mencapainya.", "20; 3 titik: (5, 0), (4, 2), (3, 4)",
          "Titik pojok (0, 0), (5, 0), (3, 4), (0, 6); f(5, 0) = f(3, 4) = 20. Garis selidik sejajar 2x + y = 10."),
        Q(2, "Tentukan nilai maksimum f = 3x + 2y pada DP 2x + 2y ≤ 9, x ≤ 3, x ≥ 0, y ≥ 0 dengan x dan y bulat.", "11 di (3, 1)", "Titik pojok optimum (3, 1½) dengan f = 12 tidak bulat; (3, 1) memberi 11 dan memenuhi; (2, 2) memberi 10."),
        Q(2, "DP mempunyai titik pojok (1, 1), (4, 1), dan (1, 5). Tentukan nilai minimum f = 3x + y.", "4 di (1, 1)", "Nilai: 4, 13, 8."),
        Q(3, "DP mempunyai titik pojok (0, 0), (4, 0), (2, 4), dan (0, 6). Tentukan nilai k agar f = kx + y mencapai maksimum hanya di (2, 4).", "1 &lt; k &lt; 2",
          "f(4, 0) = 4k, f(2, 4) = 2k + 4, f(0, 6) = 6. Syarat 2k + 4 &gt; 4k dan 2k + 4 &gt; 6."),
        Q(3, "Tentukan nilai minimum f = x + 2y pada DP x + y ≥ 4, x ≤ 6, y ≤ 5, x ≥ 0, y ≥ 0.", "4 di (4, 0)", "Titik pojok (4, 0), (6, 0), (6, 5), (0, 5), (0, 4); nilai 4, 6, 16, 10, 8."),
        Q(3, "Tunjukkan bahwa f = 2x + 4y mencapai maksimum di banyak titik pada DP x + 2y ≤ 8, 3x + 2y ≤ 12, x ≥ 0, y ≥ 0, lalu tentukan titik bulat yang mencapainya.", "maksimum 16 di sepanjang ruas (2, 3)–(0, 4); titik bulat (0, 4) dan (2, 3)",
          "Titik pojok (0, 0), (4, 0), (2, 3), (0, 4); f = 0, 8, 16, 16. Garis selidik sejajar x + 2y = 8; pada ruas itu x = 8 − 2y bulat hanya untuk y = 3 dan y = 4."),
    ],
))

CAMPURAN = [
    Q(1, "Apakah titik (3, 1) memenuhi 2x − y ≥ 4?", "ya", "6 − 1 = 5 ≥ 4."),
    Q(1, "Tentukan titik pojok DP x + 2y ≤ 10, x ≥ 0, y ≥ 0.", "(0, 0), (10, 0), (0, 5)", "Titik potong dengan sumbu."),
    Q(1, "Titik pojok DP adalah (0, 0), (3, 0), (2, 3), dan (0, 4). Tentukan nilai maksimum f = 5x + 2y.", "16 di (2, 3)", "Nilai: 0, 15, 16, 8."),
    Q(2, "Tentukan titik potong garis 3x + y = 9 dan x + 2y = 8.", "(2, 3)", "y = 9 − 3x; x + 18 − 6x = 8 → x = 2."),
    Q(2, "Sebuah garis melalui (4, 0) dan (0, 6). DP-nya memuat O dan garisnya digambar penuh. Tulis pertidaksamaannya.", "3x + 2y ≤ 12", "6x + 4y = 24 dibagi 2; uji (0, 0)."),
    Q(2, "Tentukan nilai minimum f = 10x + 20y pada DP x + y ≥ 5, x + 3y ≥ 9, x ≥ 0, y ≥ 0.", "70 di (3, 2)", "Titik pojok (0, 5), (3, 2), (9, 0); nilai 100, 70, 90."),
    Q(2, "Toko kue memuat paling banyak 60 kue. Modal kue A Rp5.000 dan kue B Rp3.000, modal tersedia Rp240.000. Untung kue A Rp2.500 dan kue B Rp2.000. Tentukan untung maksimum.", "30 kue A dan 30 kue B, Rp135.000",
      "x + y ≤ 60, 5x + 3y ≤ 240; titik pojok (0, 0), (48, 0), (30, 30), (0, 60); nilai 0, 120.000, 135.000, 120.000."),
    Q(2, "Hitung luas DP x + 2y ≤ 8, 3x + 2y ≤ 12, x ≥ 0, y ≥ 0.", "10 satuan luas", "Titik pojok (0, 0), (4, 0), (2, 3), (0, 4); bagi menjadi dua segitiga: ½ · 4 · 3 + ½ · 4 · 2."),
    Q(3, "DP mempunyai titik pojok (0, 0), (4, 0), (3, 2), dan (0, 3). Tentukan nilai k agar f = 2x + ky mencapai maksimum hanya di (3, 2).", "1 &lt; k &lt; 6", "f(4, 0) = 8, f(3, 2) = 6 + 2k, f(0, 3) = 3k; syarat 6 + 2k &gt; 8 dan 6 + 2k &gt; 3k."),
    Q(3, "Produk A memerlukan 3 jam perakitan dan 3 jam pengecatan; produk B 4 jam perakitan dan 1 jam pengecatan. Tersedia 24 jam perakitan dan 12 jam pengecatan. Untung A Rp50.000 dan B Rp30.000. Tentukan untung maksimum bila banyak produk harus bulat.",
      "3 produk A dan 3 produk B, Rp240.000", "3x + 4y ≤ 24, 3x + y ≤ 12; titik pojok optimum (8/3, 4) tidak bulat (f ≈ 253.333). Titik bulat terbaik di DP: (3, 3) dengan f = 240.000; (2, 4) memberi 220.000."),
]

TKA = [
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Daerah yang diarsir pada gambar berikut adalah daerah penyelesaian sebuah sistem pertidaksamaan linear dengan x ≥ 0 dan y ≥ 0.", fig=FIG_T1,
         soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["titik (2, 2) termasuk daerah penyelesaian", "titik pojoknya (0, 0), (5, 0), (3, 2), dan (0, 3)", "daerah penyelesaian memenuhi x + 3y ≥ 9", "titik (4, 1) termasuk daerah penyelesaian", "titik (1, 3) termasuk daerah penyelesaian"], kunci=[0, 1, 3],
         bahas="Garis batasnya x + y = 5 dan x + 3y = 9, dan DP memuat O, jadi x + y ≤ 5 dan x + 3y ≤ 9. (2, 2): 4 ≤ 5 dan 8 ≤ 9. (4, 1): 5 ≤ 5 dan 7 ≤ 9 (pada garis penuh).",
         salah="C: DP memuat O, jadi tandanya ≤. E: 1 + 9 = 10 &gt; 9."),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Nilai maksimum f(x, y) = 3x + 4y pada daerah x + y ≤ 6, x + 2y ≤ 8, x ≥ 0, y ≥ 0 adalah ....",
         opsi=["20", "18", "16", "24", "32"], kunci=0,
         bahas="Titik pojok (0, 0), (6, 0), (4, 2), (0, 4); nilai f: 0, 18, 20, 16. Maksimum 20 di (4, 2).",
         salah="B: hanya titik pada sumbu x. C: hanya titik pada sumbu y. D: memakai (0, 6), yang melanggar x + 2y ≤ 8. E: memakai (0, 8), yang melanggar kedua kendala."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Daerah penyelesaian mempunyai titik pojok (0, 0), (4, 0), (2, 3), dan (0, 4). Nilai maksimum f(x, y) = ax + 2y dicapai di (2, 3) dan di (4, 0) sekaligus. Nilai a adalah ....",
         opsi=["3", fr("3", "2"), "1", "2", "4"], kunci=0,
         bahas="f(4, 0) = f(2, 3): 4a = 2a + 6 → a = 3. Cek: f = 12 di kedua titik, dan f(0, 4) = 8 lebih kecil.",
         salah="B: suku 2a terlupa (4a = 6). C: memakai pasangan (2, 3) dan (0, 4). D: a disamakan dengan koefisien y. E: a disamakan dengan absis titik (4, 0)."),
    dict(tipe="MAT-MODEL", lv=2, fmt="pg", soal="Sebuah konveksi membuat x kaos dan y jaket. Sebuah kaos memerlukan 1 m kain dan 2 jam kerja; sebuah jaket 2 m kain dan 3 jam kerja. Tersedia 40 m kain dan 70 jam kerja. Model kendala yang tepat adalah ....",
         opsi=["x + 2y ≤ 40; 2x + 3y ≤ 70; x ≥ 0; y ≥ 0", "x + 2y ≥ 40; 2x + 3y ≥ 70; x ≥ 0; y ≥ 0", "x + 2y ≤ 70; 2x + 3y ≤ 40; x ≥ 0; y ≥ 0", "x + 2y ≤ 40; 3x + 2y ≤ 70; x ≥ 0; y ≥ 0", "2x + y ≤ 40; 3x + 2y ≤ 70; x ≥ 0; y ≥ 0"], kunci=0,
         bahas="Kain: 1 · x + 2 · y ≤ 40. Jam kerja: 2 · x + 3 · y ≤ 70.",
         salah="B: \"tersedia\" diterjemahkan ≥. C: ruas kanan tertukar. D: koefisien jam kerja tertukar. E: koefisien kaos dan jaket tertukar pada kedua kendala."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Sebuah usaha memproduksi x unit barang P dan y unit barang Q dengan kendala x + 2y ≤ 40, 3x + 2y ≤ 60, x ≥ 0, y ≥ 0, dan keuntungan f(x, y) = 30.000x + 50.000y. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["Keuntungan maksimum Rp1.050.000.", "Keuntungan maksimum dicapai dengan memproduksi 10 unit P dan 15 unit Q.", "Memproduksi 20 unit P dan 10 unit Q masih memenuhi semua kendala.", "Jika keuntungan Q turun menjadi Rp30.000 per unit, titik optimum pindah ke (20, 0)."], kunci=[True, True, False, False],
         bahas="Titik pojok (0, 0), (20, 0), (10, 15), (0, 20); f = 0; 600.000; 1.050.000; 1.000.000. (20, 10): 3 · 20 + 2 · 10 = 80 &gt; 60. Dengan f = 30.000x + 30.000y: 600.000, 750.000, 600.000, jadi optimum tetap di (10, 15).", salah=""),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pgk", soal="Titik yang termasuk daerah penyelesaian sistem 2x + y ≤ 8, x + y ≥ 3, x ≥ 0, y ≥ 0 adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["(1, 2)", "(0, 0)", "(2, 4)", "(4, 1)", "(3, 0)"], kunci=[0, 2, 4],
         bahas="(1, 2): 4 ≤ 8 dan 3 ≥ 3. (2, 4): 8 ≤ 8 dan 6 ≥ 3. (3, 0): 6 ≤ 8 dan 3 ≥ 3.",
         salah="B: 0 ≥ 3 salah. D: 2 · 4 + 1 = 9 &gt; 8."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Daerah penyelesaian sistem x + y ≤ 8, x ≤ 5, x ≥ 0, y ≥ 0 akan dipakai untuk memaksimumkan f(x, y) = px + y dengan p &gt; 0. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["Jika p = 2, nilai maksimumnya 13 di (5, 3).", "Jika p = 1, nilai maksimum dicapai di banyak titik.", "Jika p = 0,5, nilai maksimum dicapai di (5, 3).", "Untuk setiap p &gt; 0, nilai f di (5, 3) lebih besar daripada di (5, 0)."], kunci=[True, True, False, True],
         bahas="Titik pojok (0, 0), (5, 0), (5, 3), (0, 8); f = 0, 5p, 5p + 3, 8. p = 2: 13 &gt; 8. p = 1: f(5, 3) = f(0, 8) = 8. p = 0,5: 5,5 &lt; 8, jadi maksimum di (0, 8). 5p + 3 &gt; 5p.", salah=""),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg",
         soal="Sebuah perusahaan harus mengangkut paling sedikit 30 ton barang. Truk kecil memuat 3 ton dengan sewa Rp400.000, truk besar memuat 5 ton dengan sewa Rp600.000. Hanya ada sopir untuk paling banyak 8 truk. Pilihan dengan biaya paling murah adalah ....",
         opsi=["6 truk besar saja (Rp3.600.000)", "5 truk kecil dan 3 truk besar (Rp3.800.000)", "10 truk kecil (Rp4.000.000)", "8 truk besar (Rp4.800.000)", "4 truk kecil dan 4 truk besar (Rp4.000.000)"], kunci=0,
         bahas="Kendala 3x + 5y ≥ 30, x + y ≤ 8, x, y ≥ 0. Titik pojok (0, 6), (0, 8), (5, 3); biaya 3,6 juta, 4,8 juta, dan 3,8 juta rupiah. Minimum di (0, 6).",
         salah="B: titik potong kedua garis dianggap pasti optimum. C: melanggar batas 8 truk. D: titik pojok dengan biaya terbesar. E: memenuhi kendala, tetapi bukan titik pojok dan lebih mahal."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Fungsi objektif f(x, y) = px + qy dengan p &gt; 0 dan q &gt; 0 dioptimumkan pada sebuah daerah penyelesaian di kuadran I. Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["jika (0, 0) termasuk daerah penyelesaian, nilai minimum f adalah 0", "jika daerahnya tertutup, nilai maksimum f dicapai di sebuah titik pojok", "nilai maksimum f selalu dicapai di tepat satu titik", "jika daerahnya tak terbatas ke arah x dan y membesar, f tidak mempunyai nilai maksimum", "titik optimum selalu mempunyai koordinat bilangan bulat"], kunci=[0, 1, 3],
         bahas="Di kuadran I, f ≥ 0 dan f(0, 0) = 0. Pada daerah tertutup, optimum fungsi linear dicapai di titik pojok. Jika x dan y dapat dibuat sebesar mungkin, f juga.",
         salah="C: bila garis selidik sejajar sebuah sisi, maksimum dicapai di banyak titik. E: titik pojok dapat berupa pecahan, misalnya (8/3, 4)."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Nilai maksimum f(x, y) = 2x + 3y pada daerah x + y ≤ k, x ≥ 0, y ≥ 0 adalah 24. Nilai k adalah ....",
         opsi=["8", "12", fr("24", "5"), "72", "3"], kunci=0,
         bahas="Titik pojok (0, 0), (k, 0), (0, k); nilai 0, 2k, 3k. Maksimum 3k = 24, jadi k = 8.",
         salah="B: memakai titik (k, 0). C: kedua koefisien dijumlahkan (5k = 24). D: 24 dikali 3, bukan dibagi. E: koefisien y, bukan k."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Garis batas 3x + 5y ≤ 15 memotong sumbu x dan sumbu y di titik ....", ["(5, 0) dan (0, 3)", "(3, 0) dan (0, 5)", "(15, 0) dan (0, 15)", "(5, 0) dan (0, −3)", "(−5, 0) dan (0, 3)"], 0, "y = 0 → x = 5; x = 0 → y = 3.",
     "B: koefisien tertukar. C: memakai ruas kanan saja. D, E: tanda salah."),
    ("Titik yang memenuhi 2x + 3y ≤ 12 adalah ....", ["(3, 2)", "(4, 2)", "(2, 3)", "(6, 1)", "(0, 5)"], 0, "6 + 6 = 12 ≤ 12.",
     "B: 14 &gt; 12. C: 13 &gt; 12. D: 15 &gt; 12. E: 15 &gt; 12."),
    ("Garis batas digambar putus-putus bila tanda pertidaksamaannya ....", ["&lt; atau &gt;", "≤ atau ≥", "≤ saja", "≥ saja", "= "], 0, "Titik pada garis tidak termasuk.",
     "B, C, D: titik pada garis termasuk, jadi garisnya penuh. E: itu persamaan, bukan pertidaksamaan."),
    ("Banyak titik (x, y) dengan x dan y bilangan bulat pada daerah x + y ≤ 4, x ≥ 0, y ≥ 0 adalah ....", ["15", "10", "6", "25", "20"], 0, "5 + 4 + 3 + 2 + 1.",
     "B: memakai x + y ≤ 3. C: titik pada sumbu tidak dihitung. D: dihitung seperti persegi 5 × 5. E: 4 × 5."),
    ("Titik potong garis 2x + y = 8 dan x + y = 5 adalah ....", ["(3, 2)", "(2, 3)", "(4, 1)", "(3, −2)", "(0, 5)"], 0, "Kurangkan: x = 3, y = 2.",
     "B: koordinat tertukar. C: hanya x + y = 5 yang dipenuhi. D: tanda salah. E: titik potong salah satu garis dengan sumbu y."),
    ("Daerah penyelesaian berbentuk segitiga dengan titik pojok (0, 0), (6, 0), dan (0, 4). Sistemnya adalah ....",
     ["2x + 3y ≤ 12, x ≥ 0, y ≥ 0", "3x + 2y ≤ 12, x ≥ 0, y ≥ 0", "2x + 3y ≥ 12, x ≥ 0, y ≥ 0", "x + y ≤ 10, x ≥ 0, y ≥ 0", "2x + 3y ≤ 10, x ≥ 0, y ≥ 0"], 0, "Garis melalui (6, 0) dan (0, 4): 4x + 6y = 24.",
     "B: koefisien tidak ditukar. C: tanda salah, DP memuat O. D: absis dan ordinat dijumlahkan. E: ruas kanan dijumlahkan."),
    ("Nilai maksimum f = 2x + 3y pada daerah x + y ≤ 5, x + 2y ≤ 8, x ≥ 0, y ≥ 0 adalah ....", ["13", "12", "10", "15", "16"], 0, "Titik pojok (0, 0), (5, 0), (2, 3), (0, 4); nilai 0, 10, 13, 12.",
     "B: titik (0, 4). C: titik (5, 0). D: titik (0, 5) melanggar kendala kedua. E: titik (8, 0) melanggar kendala pertama."),
    ("Nilai minimum f = 4x + 3y pada daerah 2x + y ≥ 8, x + 2y ≥ 10, x ≥ 0, y ≥ 0 adalah ....", ["20", "24", "40", "0", "22"], 0, "Titik pojok (0, 8), (2, 4), (10, 0); nilai 24, 20, 40.",
     "B: titik (0, 8). C: titik (10, 0). D: (0, 0) tidak termasuk DP. E: koordinat titik potong tertukar."),
    ("Lahan parkir 360 m² memuat paling banyak 30 kendaraan; mobil memerlukan 6 m² dan bus 24 m². Model untuk x mobil dan y bus adalah ....",
     ["6x + 24y ≤ 360; x + y ≤ 30; x ≥ 0; y ≥ 0", "x + 4y ≥ 60; x + y ≤ 30; x ≥ 0; y ≥ 0", "24x + 6y ≤ 360; x + y ≤ 30; x ≥ 0; y ≥ 0", "6x + 24y ≤ 30; x + y ≤ 360; x ≥ 0; y ≥ 0", "x + 4y ≤ 60; x + y ≥ 30; x ≥ 0; y ≥ 0"], 0,
     "Luas dan banyak kendaraan sama-sama dibatasi dari atas.", "B: tanda kendala luas salah. C: luas mobil dan bus tertukar. D: ruas kanan tertukar. E: tanda kendala banyak kendaraan salah."),
    ("Gradien garis selidik f = 5x + 2y adalah ....", ["−" + fr("5", "2"), "−" + fr("2", "5"), fr("5", "2"), fr("2", "5"), "5"], 0, "y = −5/2 x + k/2.",
     "B: dibalik. C: tanda salah. D: dibalik dan tanda salah. E: koefisien x saja."),
    ("Daerah penyelesaian mempunyai titik pojok (0, 0), (4, 0), (3, 2), dan (0, 5). Nilai maksimum f = 3x + 3y dan letaknya adalah ....",
     ["15, di sepanjang ruas dari (3, 2) ke (0, 5)", "15, hanya di (3, 2)", "15, hanya di (0, 5)", "12, di (4, 0)", "24, di (3, 5)"], 0, "f = 0, 12, 15, 15; garis selidik sejajar sisi x + y = 5.",
     "B, C: kedua titik pojok bernilai sama, jadi seluruh ruasnya optimum. D: nilai terkecil yang tidak nol. E: (3, 5) tidak termasuk DP."),
    ("Nilai maksimum f = 2x + y pada daerah 2x + 2y ≤ 7, x ≤ 3, x ≥ 0, y ≥ 0 dengan x dan y bulat adalah ....", ["6", "6,5", "7", "5", "8"], 0,
     "Titik pojok optimum (3, ½) tidak bulat; titik bulat (3, 0) memberi 6 dan (2, 1) memberi 5.", "B: nilai di titik pojok yang tidak bulat. C: titik (3, 1) melanggar 2x + 2y ≤ 7. D: titik (2, 1). E: titik (3, 2) di luar DP."),
    ("Toko sepatu memuat paling banyak 40 pasang. Modal sepatu A Rp100.000 dan B Rp150.000 per pasang, modal tersedia Rp5.000.000. Untung A Rp30.000 dan B Rp40.000. Untung maksimumnya adalah ....",
     ["Rp1.400.000", "Rp1.200.000", "≈ Rp1.333.333", "Rp1.600.000", "Rp2.800.000"], 0, "x + y ≤ 40, 2x + 3y ≤ 100; titik pojok (0, 0), (40, 0), (20, 20), (0, 33⅓); maksimum di (20, 20).",
     "B: titik (40, 0). C: titik (0, 33⅓), yang juga bukan bilangan bulat. D: (0, 40) memerlukan modal Rp6.000.000. E: x dan y keduanya 40."),
    ("Sistem yang tidak mempunyai penyelesaian adalah ....", ["x + y ≤ 2; x + y ≥ 4", "x + y ≤ 4; x + y ≥ 2", "x ≤ 3; y ≤ 3", "x + y ≤ 2; x ≥ 0", "2x + y ≥ 4; x ≥ 0"], 0, "x + y tidak dapat sekaligus ≤ 2 dan ≥ 4.",
     "B: (1, 2) memenuhi. C: (0, 0) memenuhi. D: (0, 0) memenuhi. E: (2, 0) memenuhi."),
    ("Nilai minimum f = x + y pada daerah x + 2y ≥ 6, 2x + y ≥ 6, x ≥ 0, y ≥ 0 adalah ....", ["4", "6", "2", "0", "12"], 0, "Titik pojok (0, 6), (2, 2), (6, 0); nilai 6, 4, 6.",
     "B: titik pada sumbu. C: hanya nilai x di titik potong. D: (0, 0) tidak termasuk DP. E: kedua titik sumbu dijumlahkan."),
]
UJI_URAIAN = [
    ("Gambarkan daerah penyelesaian sistem 3x + 2y ≤ 12, x + 2y ≤ 8, x ≥ 0, y ≥ 0, lalu tentukan semua titik pojoknya.", "(0, 0), (4, 0), (2, 3), (0, 4)",
     "Garis melalui (4, 0), (0, 6) dan (8, 0), (0, 4); kurangkan: 2x = 4 → (2, 3); uji (0, 0) benar untuk keduanya."),
    ("Daerah penyelesaian sebuah sistem di kuadran I mempunyai titik pojok (0, 0), (5, 0), (3, 4), dan (0, 6). Tentukan sistem pertidaksamaannya.", "2x + y ≤ 10, 2x + 3y ≤ 18, x ≥ 0, y ≥ 0",
     "Garis melalui (5, 0) dan (3, 4): gradien −2, y = −2x + 10. Garis melalui (3, 4) dan (0, 6): gradien −⅔, 2x + 3y = 18. Uji (0, 0)."),
    ("Tentukan nilai minimum f = 5x + 4y pada daerah x + y ≥ 6, 2x + y ≥ 8, x ≥ 0, y ≥ 0, dan jelaskan mengapa nilai maksimumnya tidak ada.", "26 di (2, 4); DP terbuka",
     "Titik pojok (0, 8), (2, 4), (6, 0); nilai 32, 26, 30. DP tak terbatas ke kanan atas, jadi f dapat dibuat sebesar mungkin."),
    ("Kue A memerlukan 2 butir telur dan 100 g gula; kue B 1 butir telur dan 150 g gula. Tersedia 30 butir telur dan 2,1 kg gula. Untung kue A Rp4.000 dan kue B Rp5.000. (a) Susun modelnya. (b) Tentukan titik pojok DP. (c) Tentukan untung maksimum.",
     "(a) 2x + y ≤ 30, 2x + 3y ≤ 42, x, y ≥ 0; maks 4.000x + 5.000y; (b) (0, 0), (15, 0), (12, 6), (0, 14); (c) 12 kue A dan 6 kue B, Rp78.000",
     "Gula: 100x + 150y ≤ 2.100 dibagi 50. Titik potong: kurangkan, 2y = 12. Nilai f: 0, 60.000, 78.000, 70.000."),
    ("Produk A memerlukan 3 jam perakitan dan 3 jam pengecatan; produk B 4 jam perakitan dan 1 jam pengecatan. Tersedia 24 jam perakitan dan 12 jam pengecatan. Untung A Rp50.000 dan B Rp30.000. (a) Susun modelnya. (b) Tentukan titik pojok DP. (c) Tentukan titik optimum tanpa syarat bulat. (d) Tentukan untung maksimum bila banyak produk harus bulat.",
     "(a) 3x + 4y ≤ 24, 3x + y ≤ 12, x, y ≥ 0; (b) (0, 0), (4, 0), (8/3, 4), (0, 6); (c) (8/3, 4), f ≈ Rp253.333; (d) 3 A dan 3 B, Rp240.000",
     "(b) Kurangkan: 3y = 12 → y = 4, x = 8/3. (d) Titik bulat di DP dekat (8/3, 4): (2, 4) → 220.000; (3, 3) → 240.000 (9 + 12 = 21 ≤ 24, 9 + 3 = 12 ≤ 12); (4, 0) → 200.000."),
]

META = dict(
    title="Modul Program Linear", kick="Modul belajar Matematika · Fase E · Kelas X", big="Program Linear",
    subtitle="Sistem pertidaksamaan linear dua variabel, model matematika, titik pojok, dan garis selidik",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat menggambar daerah penyelesaian sistem pertidaksamaan linear dua variabel, menyusun model matematika dari masalah sehari-hari, serta menentukan nilai optimum fungsi objektif dengan uji titik pojok dan garis selidik, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Alur program linear</h2><table><tr><th>Langkah</th><th>Hasil</th></tr>"
               "<tr><td>1. Baca soal, tentukan x dan y</td><td>arti dan satuan variabel</td></tr><tr><td>2. Susun tabel</td><td>kendala dan fungsi objektif</td></tr>"
               "<tr><td>3. Gambar daerah penyelesaian</td><td>garis batas, uji titik, arsiran</td></tr><tr><td>4. Tentukan titik pojok</td><td>titik potong garis</td></tr>"
               "<tr><td>5. Uji titik pojok atau garis selidik</td><td>nilai optimum dan jawabannya dalam konteks</td></tr></table>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b> Gambar daerah penyelesaian dengan penggaris, dan uji setiap titik pojok pada semua kendala.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Daerah penyelesaian (DP) diarsir. Garis batas penuh untuk ≤ dan ≥, putus-putus untuk &lt; dan &gt;. Fungsi objektif ditulis f(x, y) = px + qy. Desimal ditulis dengan koma, ribuan dengan titik.",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>daerah penyelesaian, titik pojok, model, atau nilai optimum?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025 (specs/tka-templates/matematika.md).",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-MODEL, MAT-FUNGSI): mengenali, menghitung, bekerja mundur, memodelkan, atau menafsirkan fungsi. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Mengapa nilai optimum pada daerah tertutup selalu dicapai di titik pojok?", "Bagaimana kamu menentukan tanda kendala dari kalimat soal?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Daerah penyelesaian</th><td>garis batas dari titik potong sumbu; penuh (≤, ≥) atau putus-putus (&lt;, &gt;); uji (0, 0)</td></tr>"
        "<tr><th>Sistem</th><td>DP = irisan; titik pojok dari titik potong dua garis; x ≥ 0, y ≥ 0 untuk kuadran I</td></tr>"
        "<tr><th>Garis dari gambar</th><td>melalui (a, 0) dan (0, b): bx + ay = ab; tanda dari titik uji di dalam DP</td></tr>"
        "<tr><th>Model</th><td>variabel, tabel, kendala (tersedia ≤, kebutuhan ≥), x, y ≥ 0, fungsi objektif px + qy</td></tr>"
        "<tr><th>Uji titik pojok</th><td>hitung f di setiap titik pojok; pilih terbesar atau terkecil</td></tr>"
        "<tr><th>Garis selidik</th><td>px + qy = k; geser menjauhi O: titik terakhir maksimum, titik pertama minimum</td></tr>"
        "<tr><th>Kasus khusus</th><td>sejajar sisi: optimum di sepanjang sisi; bulat: periksa titik bulat di DP; DP kosong: tidak ada penyelesaian; DP terbuka: maksimum mungkin tidak ada</td></tr></table>"
        '<div class="fig">' + FIG_SEL + "</div>"),
    jebakan5=["Uji satu titik untuk menentukan sisi daerah penyelesaian; jangan menebak dari tanda.", "\"Tersedia\" dan \"paling banyak\" berarti ≤; \"paling sedikit\" berarti ≥.",
              "Titik potong garis dengan sumbu belum tentu titik pojok; periksa semua kendala.", "Titik potong dua garis dihitung, bukan ditaksir dari gambar.",
              "Membulatkan titik pojok yang tidak bulat dapat menghasilkan titik di luar daerah penyelesaian."],
    guru=["Modul ini mengikuti capaian Fase E \"menyelesaikan masalah yang berkaitan dengan sistem pertidaksamaan linear dua variabel\" dan simpul ALJ-04 pada peta Matematika (kelas X). Urutan bab dapat berbeda antarsekolah.",
          "Modul ini mengarsir daerah penyelesaian. Sebagian buku dan soal mengarsir daerah yang bukan penyelesaian; ingatkan siswa untuk selalu membaca keterangan gambar.",
          "Pertidaksamaan satu variabel (linear, kuadrat, pecahan, nilai mutlak, akar) dibahas di modul Pertidaksamaan.",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


# ------------------------------------------------------------------ check
def _ok(cons, p):
    """p satisfies every constraint (a, b, op, c)."""
    x, y = p
    for a, b, op, c in cons:
        v = a * x + b * y
        if not {"<=": v <= c, "<": v < c, ">=": v >= c, ">": v > c}[op]:
            return False
    return True


def corners(cons):
    """All corner points of the region, as a sorted list of exact points."""
    pts = set()
    for (a1, b1, _, c1), (a2, b2, _, c2) in combinations(cons, 2):
        d = a1 * b2 - a2 * b1
        if d:
            p = (F(c1 * b2 - c2 * b1, d), F(a1 * c2 - a2 * c1, d))
            if _ok(cons, p):
                pts.add(p)
    return sorted(pts)


def P(*pts):
    return sorted((F(x), F(y)) for x, y in pts)


def best(f, pts, mode=max):
    v = mode(f(*p) for p in pts)
    return v, sorted(p for p in pts if f(*p) == v)


def int_best(f, cons, rng=60, mode=max):
    pts = [(x, y) for x in range(-rng, rng + 1) for y in range(-rng, rng + 1) if _ok(cons, (x, y))]
    return best(f, pts, mode)


def check():
    le = lambda a, b, c: (a, b, "<=", c)  # noqa: E731
    ge = lambda a, b, c: (a, b, ">=", c)  # noqa: E731
    # prasyarat
    assert (F(12, 2), F(12, 3)) == (6, 4) and 3 * 2 + 2 * 1 == 8 and corners([le(1, 1, 6), le(2, 1, 8), ge(1, 1, 6), ge(2, 1, 8)]) == P((2, 4))
    assert corners([le(3, 2, 12), le(1, 2, 8), ge(3, 2, 12), ge(1, 2, 8)]) == P((2, 3)) and 3000 * 10 + 2500 * 20 == 80000 and 3 * 4 + 4 * 0 == 12 == 3 * 0 + 4 * 3
    # subbab 1
    assert _ok([le(2, 3, 12)], (0, 0)) and _ok([(-1, 1, ">", -2)], (0, 0)) and not _ok([(-1, 1, ">", -2)], (2, 0))
    assert 1 * -4 - 2 * 0 == -4 and 0 - 2 * 2 == -4 and _ok([ge(1, -2, -4)], (0, 0))
    assert _ok([le(3, 2, 10)], (2, 1)) and (F(20, 4), F(20, 5)) == (5, 4) and not _ok([ge(1, 1, 3)], (0, 0)) and _ok([le(3, 4, 12)], (0, 0))
    assert not _ok([(1, -1, ">", 1)], (0, 0)) and _ok([(1, -1, ">", 1)], (2, 0)) and _ok([ge(2, -3, 0)], (1, 0))
    assert max(k for k in range(-20, 20) if _ok([le(2, 5, 20)], (k, 2))) == 5
    assert 5 * 2 + 2 * 0 == 10 == 5 * 0 + 2 * 5 and not _ok([ge(5, 2, 10)], (0, 0))
    assert _ok([le(3, 1, 15)], (3, 5)) and not _ok([le(3, 1, 15)], (4, 4)) and [_ok([ge(-2, 1, 0)], p) for p in [(1, 3), (2, 3), (-1, 0)]] == [True, False, True]
    # subbab 2
    assert corners([le(1, 1, 6), le(2, 1, 8)] + POS) == P((0, 0), (4, 0), (2, 4), (0, 6))
    assert corners([le(1, 2, 8), ge(1, 1, 3)] + POS) == P((3, 0), (8, 0), (0, 4), (0, 3)) and _ok([le(1, 2, 8), ge(1, 1, 3)], (2, 2))
    assert corners([le(1, 3, 9), le(2, 1, 8)] + POS) == P((0, 0), (4, 0), (3, 2), (0, 3))
    assert _ok([le(1, 1, 4), le(1, -1, 1)] + POS, (1, 2)) and corners([le(1, 1, 5)] + POS) == P((0, 0), (5, 0), (0, 5)) and corners([le(1, 1, 7), le(1, -1, 1), ge(1, 1, 7), ge(1, -1, 1)]) == P((4, 3))
    assert corners([le(1, 0, 3), le(0, 1, 2)] + POS) == P((0, 0), (3, 0), (3, 2), (0, 2))
    assert corners([le(2, 1, 6), le(1, 2, 6)] + POS) == P((0, 0), (3, 0), (2, 2), (0, 3)) and corners([le(3, 2, 12), le(1, 2, 8)] + POS) == P((0, 0), (4, 0), (2, 3), (0, 4))
    assert corners([le(1, 1, 5), le(1, 0, 3)] + POS) == P((0, 0), (3, 0), (3, 2), (0, 5)) and _ok([le(1, 1, 5), le(1, 0, 3)], (1, 1))
    assert corners([ge(1, 1, 4), le(1, 1, 2)]) == [] and not any(_ok([ge(1, 1, 4), le(1, 1, 2)], (x, y)) for x in range(-9, 10) for y in range(-9, 10))
    assert corners([ge(1, 0, 1), ge(0, 1, 1), le(3, 4, 19)]) == P((1, 1), (5, 1), (1, 4)) and _ok([le(3, 4, 19)], (2, 2))
    tri = corners([le(1, 1, 6), le(-2, 1, 0), ge(0, 1, 0)])
    assert tri == P((0, 0), (6, 0), (2, 4)) and F(1, 2) * 6 * 4 == 12
    assert len([(x, y) for x in range(0, 5) for y in range(0, 5) if x + y <= 3]) == 10
    # subbab 3
    assert (200 * 2 // 100, 4000 // 100) == (4, 40) and F(50 * 2, 50) == 2 and corners([le(2, 1, 40), le(1, 2, 50)] + POS) == P((0, 0), (20, 0), (10, 20), (0, 25))
    assert corners([ge(3, 1, 9), ge(1, 2, 8)] + POS) == P((0, 9), (2, 3), (8, 0))
    assert corners([le(1, 1, 50), le(1, 4, 80)] + POS) == P((0, 0), (50, 0), (40, 10), (0, 20)) and F(480, 6) == 80
    assert F(40000, 1000) == 40 and F(1200000, 2000) == 600 and F(360, 10) == 36
    assert _ok([ge(4, 3, 36), le(1, 1, 10)] + POS, (6, 4)) and 2000000 * 6 + 1200000 * 4 == 16800000 and F(32, 2) == 16
    # subbab 4
    roti = lambda x, y: 3000 * x + 2500 * y  # noqa: E731
    assert best(roti, corners([le(2, 1, 40), le(1, 2, 50)] + POS)) == (80000, P((10, 20))) and roti(20, 0) == 60000 and roti(0, 25) == 62500
    diet = lambda x, y: 4000 * x + 3000 * y  # noqa: E731
    assert best(diet, corners([ge(3, 1, 9), ge(1, 2, 8)] + POS), min) == (17000, P((2, 3))) and [diet(0, 9), diet(8, 0)] == [27000, 32000]
    assert corners([le(1, 1, 6), le(2, 1, 10)] + POS) == P((0, 0), (5, 0), (4, 2), (0, 6)) and best(lambda x, y: 5 * x + 4 * y, P((0, 0), (5, 0), (4, 2), (0, 6))) == (28, P((4, 2)))
    assert best(lambda x, y: 3 * x + 2 * y, P((0, 0), (4, 0), (3, 2), (0, 4))) == (13, P((3, 2))) and best(lambda x, y: 2 * x + 5 * y, P((0, 3), (2, 1), (5, 0)), min) == (9, P((2, 1)))
    assert best(lambda x, y: x + y, corners([le(1, 0, 4), le(0, 1, 3)] + POS)) == (7, P((4, 3))) and best(lambda x, y: 4 * x + y, P((0, 0), (6, 0), (0, 8))) == (24, P((6, 0)))
    assert best(lambda x, y: 2 * x + 3 * y, corners([le(3, 2, 12), le(1, 2, 8)] + POS)) == (13, P((2, 3)))
    assert corners([ge(1, 1, 4), ge(1, 3, 6)] + POS) == P((0, 4), (3, 1), (6, 0)) and best(lambda x, y: 3 * x + 2 * y, P((0, 4), (3, 1), (6, 0)), min) == (8, P((0, 4)))
    assert corners([le(1, 1, 10), le(2, 1, 16)] + POS) == P((0, 0), (8, 0), (6, 4), (0, 10)) and best(lambda x, y: 3 * x + 2 * y, P((0, 0), (8, 0), (6, 4), (0, 10))) == (26, P((6, 4)))
    assert corners([le(2, 1, 20), le(1, 2, 16)] + POS) == P((0, 0), (10, 0), (8, 4), (0, 8)) and best(lambda x, y: 30000 * x + 40000 * y, P((0, 0), (10, 0), (8, 4), (0, 8))) == (400000, P((8, 4)))
    mes = corners([le(2, 1, 12), le(1, 3, 16)] + POS)
    assert mes == P((0, 0), (6, 0), (4, 4), (0, F(16, 3))) and best(lambda x, y: 40000 * x + 30000 * y, mes) == (280000, P((4, 4))) and 30000 * F(16, 3) == 160000
    bus = corners([ge(4, 3, 36), le(1, 1, 10)] + POS)
    assert bus == P((9, 0), (10, 0), (6, 4)) and best(lambda x, y: F(2) * x + F(6, 5) * y, bus, min) == (F(84, 5), P((6, 4))) and not _ok([le(1, 1, 10)], (0, 12))
    assert all(_ok([ge(3, 1, 9), ge(1, 2, 8)] + POS, (n, n)) for n in range(3, 50)) and diet(10, 10) == 70000
    # subbab 5
    assert best(lambda x, y: 3 * x + 2 * y, corners([le(1, 1, 6), le(2, 1, 8)] + POS)) == (14, P((2, 4))) and 3 * 2 == 6 == 2 * 3
    assert best(lambda x, y: 2 * x + 2 * y, corners([le(1, 1, 6), le(2, 1, 8)] + POS)) == (12, P((0, 6), (2, 4))) and _ok([le(1, 1, 6), le(2, 1, 8)], (1, 5))
    bc = [le(1, 1, 5), le(3, 1, 10)] + POS
    assert corners(bc) == P((0, 0), (F(10, 3), 0), (F(5, 2), F(5, 2)), (0, 5)) and 5 * F(5, 2) + 4 * F(5, 2) == F(45, 2)
    assert int_best(lambda x, y: 5 * x + 4 * y, bc) == (22, [(2, 3)]) and not _ok(bc, (3, 2)) and 3 * 3 + 2 == 11
    assert 2 * 1 + 5 * 2 == 12 and F(-3, 4) == F(-3, 4) and 1 + 5 == 4 + 2 and corners([le(1, 1, 2), ge(1, 1, 5)]) == []
    g5 = [le(2, 1, 10), le(2, 3, 18)] + POS
    assert corners(g5) == P((0, 0), (5, 0), (3, 4), (0, 6)) and best(lambda x, y: 4 * x + 3 * y, corners(g5)) == (24, P((3, 4)))
    assert int_best(lambda x, y: 4 * x + 2 * y, g5) == (20, [(3, 4), (4, 2), (5, 0)])
    ib = [le(2, 2, 9), le(1, 0, 3)] + POS
    assert corners(ib) == P((0, 0), (3, 0), (3, F(3, 2)), (0, F(9, 2))) and best(lambda x, y: 3 * x + 2 * y, corners(ib)) == (12, P((3, F(3, 2)))) and int_best(lambda x, y: 3 * x + 2 * y, ib) == (11, [(3, 1)])
    assert best(lambda x, y: 3 * x + y, P((1, 1), (4, 1), (1, 5)), min) == (4, P((1, 1)))
    assert corners([le(2, 1, 8), le(1, 1, 6)] + POS) == P((0, 0), (4, 0), (2, 4), (0, 6))
    for k in [F(j, 8) for j in range(-16, 40)]:
        assert (best(lambda x, y: k * x + y, P((0, 0), (4, 0), (2, 4), (0, 6)))[1] == P((2, 4))) == (1 < k < 2)
    m5 = [ge(1, 1, 4), le(1, 0, 6), le(0, 1, 5)] + POS
    assert corners(m5) == P((4, 0), (6, 0), (6, 5), (0, 5), (0, 4)) and best(lambda x, y: x + 2 * y, corners(m5), min) == (4, P((4, 0)))
    e5 = [le(1, 2, 8), le(3, 2, 12)] + POS
    assert corners(e5) == P((0, 0), (4, 0), (2, 3), (0, 4)) and best(lambda x, y: 2 * x + 4 * y, corners(e5)) == (16, P((0, 4), (2, 3)))
    assert int_best(lambda x, y: 2 * x + 4 * y, e5) == (16, [(0, 4), (2, 3)])
    # campuran
    assert _ok([ge(2, -1, 4)], (3, 1)) and corners([le(1, 2, 10)] + POS) == P((0, 0), (10, 0), (0, 5)) and best(lambda x, y: 5 * x + 2 * y, P((0, 0), (3, 0), (2, 3), (0, 4))) == (16, P((2, 3)))
    assert corners([le(3, 1, 9), ge(3, 1, 9), le(1, 2, 8), ge(1, 2, 8)]) == P((2, 3)) and _ok([le(3, 2, 12)], (0, 0)) and 3 * 4 == 12 == 2 * 6
    c6 = corners([ge(1, 1, 5), ge(1, 3, 9)] + POS)
    assert c6 == P((0, 5), (3, 2), (9, 0)) and best(lambda x, y: 10 * x + 20 * y, c6, min) == (70, P((3, 2)))
    kue = corners([le(1, 1, 60), le(5, 3, 240)] + POS)
    assert kue == P((0, 0), (48, 0), (30, 30), (0, 60)) and best(lambda x, y: 2500 * x + 2000 * y, kue) == (135000, P((30, 30)))
    assert F(1, 2) * 4 * 3 + F(1, 2) * 4 * 2 == 10
    for k in [F(j, 4) for j in range(-8, 40)]:
        assert (best(lambda x, y: 2 * x + k * y, P((0, 0), (4, 0), (3, 2), (0, 3)))[1] == P((3, 2))) == (1 < k < 6)
    assert corners([le(2, 1, 8), le(1, 3, 9)] + POS) == P((0, 0), (4, 0), (3, 2), (0, 3))
    pk = [le(3, 4, 24), le(3, 1, 12)] + POS
    assert corners(pk) == P((0, 0), (4, 0), (F(8, 3), 4), (0, 6)) and int_best(lambda x, y: 50000 * x + 30000 * y, pk) == (240000, [(3, 3)]) and 50000 * 2 + 30000 * 4 == 220000
    # TKA
    t1 = [le(1, 1, 5), le(1, 3, 9)] + POS
    assert corners(t1) == P((0, 0), (5, 0), (3, 2), (0, 3)) and [_ok(t1, p) for p in [(2, 2), (4, 1), (1, 3)]] == [True, True, False] and not _ok([ge(1, 3, 9)], (0, 0))
    t2 = corners([le(1, 1, 6), le(1, 2, 8)] + POS)
    assert t2 == P((0, 0), (6, 0), (4, 2), (0, 4)) and best(lambda x, y: 3 * x + 4 * y, t2) == (20, P((4, 2))) and 3 * 0 + 4 * 6 == 24 and 4 * 8 == 32
    assert best(lambda x, y: 3 * x + 2 * y, P((0, 0), (4, 0), (2, 3), (0, 4))) == (12, P((2, 3), (4, 0))) and F(6, 4) == F(3, 2) and 2 * 1 + 6 == 8 == 2 * 4
    t5 = corners([le(1, 2, 40), le(3, 2, 60)] + POS)
    assert t5 == P((0, 0), (20, 0), (10, 15), (0, 20)) and best(lambda x, y: 30000 * x + 50000 * y, t5) == (1050000, P((10, 15)))
    assert not _ok([le(3, 2, 60)], (20, 10)) and best(lambda x, y: 30000 * x + 30000 * y, t5) == (750000, P((10, 15)))
    t6 = [le(2, 1, 8), ge(1, 1, 3)] + POS
    assert [_ok(t6, p) for p in [(1, 2), (0, 0), (2, 4), (4, 1), (3, 0)]] == [True, False, True, False, True]
    t7 = corners([le(1, 1, 8), le(1, 0, 5)] + POS)
    assert t7 == P((0, 0), (5, 0), (5, 3), (0, 8))
    assert best(lambda x, y: 2 * x + y, t7) == (13, P((5, 3))) and best(lambda x, y: x + y, t7) == (8, P((0, 8), (5, 3))) and best(lambda x, y: F(1, 2) * x + y, t7) == (8, P((0, 8)))
    t8 = [ge(3, 5, 30), le(1, 1, 8)] + POS
    assert corners(t8) == P((0, 6), (0, 8), (5, 3)) and int_best(lambda x, y: 400000 * x + 600000 * y, t8, mode=min) == (3600000, [(0, 6)])
    assert _ok(t8, (4, 4)) and 400000 * 4 + 600000 * 4 == 4000000 and not _ok(t8, (10, 0)) and 400000 * 5 + 600000 * 3 == 3800000
    assert F(24, 3) == 8 and F(24, 2) == 12 and F(24, 5) == F(24, 5)
    # uji
    assert (F(15, 3), F(15, 5)) == (5, 3) and [2 * x + 3 * y for x, y in [(3, 2), (4, 2), (2, 3), (6, 1), (0, 5)]] == [12, 14, 13, 15, 15]
    assert len([(x, y) for x in range(0, 6) for y in range(0, 6) if x + y <= 4]) == 15 and len([(x, y) for x in range(1, 6) for y in range(1, 6) if x + y <= 4]) == 6
    assert corners([le(2, 1, 8), ge(2, 1, 8), le(1, 1, 5), ge(1, 1, 5)]) == P((3, 2))
    assert corners([le(2, 3, 12)] + POS) == P((0, 0), (6, 0), (0, 4)) and corners([le(3, 2, 12)] + POS) != P((0, 0), (6, 0), (0, 4))
    u7 = corners([le(1, 1, 5), le(1, 2, 8)] + POS)
    assert u7 == P((0, 0), (5, 0), (2, 3), (0, 4)) and best(lambda x, y: 2 * x + 3 * y, u7) == (13, P((2, 3)))
    u8 = corners([ge(2, 1, 8), ge(1, 2, 10)] + POS)
    assert u8 == P((0, 8), (2, 4), (10, 0)) and best(lambda x, y: 4 * x + 3 * y, u8, min) == (20, P((2, 4))) and 4 * 4 + 3 * 2 == 22
    assert F(360, 6) == 60 and F(-5, 2) == F(-5, 2)
    assert corners([le(2, 1, 8), le(1, 1, 5)] + POS) == P((0, 0), (4, 0), (3, 2), (0, 5)) and best(lambda x, y: 3 * x + 3 * y, P((0, 0), (4, 0), (3, 2), (0, 5))) == (15, P((0, 5), (3, 2)))
    u12 = [le(2, 2, 7), le(1, 0, 3)] + POS
    assert best(lambda x, y: 2 * x + y, corners(u12)) == (F(13, 2), P((3, F(1, 2)))) and int_best(lambda x, y: 2 * x + y, u12) == (6, [(3, 0)]) and not _ok(u12, (3, 1))
    u13 = corners([le(1, 1, 40), le(2, 3, 100)] + POS)
    assert u13 == P((0, 0), (40, 0), (20, 20), (0, F(100, 3))) and best(lambda x, y: 30000 * x + 40000 * y, u13) == (1400000, P((20, 20))) and 150000 * 40 == 6000000
    assert not any(_ok([le(1, 1, 2), ge(1, 1, 4)], (x, y)) for x in range(-9, 10) for y in range(-9, 10))
    assert _ok([le(1, 1, 4), ge(1, 1, 2)], (1, 2)) and _ok([le(1, 0, 3), le(0, 1, 3)], (0, 0)) and _ok([ge(2, 1, 4), ge(1, 0, 0)], (2, 0))
    u15 = corners([ge(1, 2, 6), ge(2, 1, 6)] + POS)
    assert u15 == P((0, 6), (2, 2), (6, 0)) and best(lambda x, y: x + y, u15, min) == (4, P((2, 2)))
    # uraian
    u2 = corners([le(2, 1, 10), le(2, 3, 18)] + POS)
    assert u2 == P((0, 0), (5, 0), (3, 4), (0, 6))
    u3 = corners([ge(1, 1, 6), ge(2, 1, 8)] + POS)
    assert u3 == P((0, 8), (2, 4), (6, 0)) and best(lambda x, y: 5 * x + 4 * y, u3, min) == (26, P((2, 4)))
    u4 = corners([le(2, 1, 30), le(2, 3, 42)] + POS)
    assert F(2100, 50) == 42 and u4 == P((0, 0), (15, 0), (12, 6), (0, 14)) and best(lambda x, y: 4000 * x + 5000 * y, u4) == (78000, P((12, 6)))
    assert best(lambda x, y: 50000 * x + 30000 * y, corners(pk)) == (F(760000, 3), P((F(8, 3), 4)))
    return True
