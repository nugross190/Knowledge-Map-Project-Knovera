"""Content of the printable module "Fungsi Invers" (Matematika kelas XI).

One-to-one functions and the condition for an inverse, the inverse of linear, rational, quadratic
(restricted domain), root and exponential functions, the graph of f⁻¹ as the mirror image in y = x,
and inverses of composite functions. Every numeric answer is re-derived in check() with exact fractions.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import plane  # noqa: E402
from kit import fr, Q, close  # noqa: E402

BLUE, RED, GREEN, GREY = "#1f3a68", "#c0502a", "#2e6b32", "#7a8190"
INV = "f⁻¹"

PRASYARAT = [
    ("P1", "Diketahui f(x) = 3x − 5. Hitung f(4) dan f(−1).", "7 dan −8", "12 − 5; −3 − 5."),
    ("P2", "Selesaikan 2x + 7 = 1.", "x = −3", "2x = −6."),
    ("P3", "Nyatakan x dalam y jika y = " + fr("x − 2", "5") + ".", "x = 5y + 2", "Kalikan 5: 5y = x − 2."),
    ("P4", "Nyatakan x dalam y jika y = " + fr("x + 1", "x − 2") + ".", "x = " + fr("2y + 1", "y − 1"), "xy − 2y = x + 1 → xy − x = 2y + 1 → x(y − 1) = 2y + 1."),
    ("P5", "Tulis x² − 6x + 11 dalam bentuk (x − p)² + q.", "(x − 3)² + 2", "(x − 3)² = x² − 6x + 9; 11 − 9 = 2."),
    ("P6", "Diketahui f(x) = 2x + 1 dan g(x) = x². Hitung (f ∘ g)(2).", "9", "g(2) = 4 dulu, lalu f(4) = 9."),
    ("P7", "Diketahui f(x) = x + 3 dan g(x) = 2x. Tentukan (g ∘ f)(x).", "2x + 6", "g(f(x)) = 2(x + 3)."),
    ("P8", "Hitung ²log 32, lalu tentukan x jika 3ˣ = " + fr("1", "9") + ".", "5 dan x = −2", "2⁵ = 32; 3⁻² = 1/9."),
]

INGAT = [
    ("A", "Fungsi dan substitusi", "P1, P2", "Subbab 1, 2", ["f(a) adalah nilai fungsi saat x diganti a; pakai tanda kurung untuk bilangan negatif.",
                                                            "Persamaan linear diselesaikan dengan memindahkan suku (tandanya berganti), lalu membagi dengan koefisien x."]),
    ("B", "Mengubah subjek rumus", "P3, P4", "Subbab 2, 3", ["Lepaskan penyebut dengan mengalikan kedua ruas.",
                                                             "Kumpulkan semua suku yang memuat x di satu ruas, keluarkan x sebagai faktor, lalu bagi."]),
    ("C", "Melengkapkan kuadrat", "P5", "Subbab 3", ["x² + bx + c = (x + ½b)² + c − (½b)².", "Puncak grafik y = (x − p)² + q ada di (p, q)."]),
    ("D", "Komposisi fungsi", "P6, P7", "Subbab 5", ["(f ∘ g)(x) = f(g(x)): g dikerjakan dulu, hasilnya dimasukkan ke f.", "Pada umumnya f ∘ g ≠ g ∘ f."]),
    ("E", "Eksponen dan logaritma", "P8", "Subbab 4, 5", ["ᵃlog b = c artinya aᶜ = b (a &gt; 0, a ≠ 1, b &gt; 0).", "a⁻ⁿ = 1/aⁿ dan a⁰ = 1."]),
]


def yx(lo, hi):
    """Dashed mirror line y = x from lo to hi."""
    return (lo, lo, hi, hi, GREY, True)


# Figures. Every marked point lies on grid points.
FIG_TIDAK = plane((-1, 5, 1), (-5, 5, 1), curves=[(lambda x: x * x - 4 * x, -0.8, 4.8, BLUE, "g(x) = x² − 4x")],
                  segs=[(-1, -3, 5, -3, RED, True)], points=[(1, -3, "(1, −3)"), (3, -3, "(3, −3)"), (2, -4, "(2, −4)")],
                  labels=[(3.6, -3.6, "y = −3", RED)])
FIG_REF = plane((-3, 5, 1), (-3, 5, 1), curves=[(lambda x: 2 * x - 2, -0.5, 3.5, BLUE, "f"), (lambda x: x / 2 + 1, -3, 5, RED, INV)],
                segs=[yx(-3, 5)], points=[(0, -2, "(0, −2)"), (-2, 0, "(−2, 0)"), (3, 4, "(3, 4)"), (4, 3, ""), (2, 2, "")],
                labels=[(-2.8, -2.4, "y = x", GREY)])
FIG_EXP = plane((-3, 5, 1), (-3, 5, 1), curves=[(lambda x: 2 ** x, -3, 2.3, BLUE, "y = 2ˣ"), (lambda x: math.log2(x), 0.13, 5, RED, "y = ²log x")],
                segs=[yx(-3, 5)], points=[(0, 1, ""), (1, 2, ""), (2, 4, "(2, 4)"), (1, 0, ""), (2, 1, ""), (4, 2, "")])
FIG_L4 = plane((-2, 4, 1), (-2, 6, 1), curves=[(lambda x: 2 * x + 1, -1.5, 2.5, BLUE, "f")], points=[(0, 1, "(0, 1)"), (1, 3, "(1, 3)"), (2, 5, "(2, 5)")])
FIG_SK = plane((-3, 5, 1), (-3, 5, 1), curves=[(lambda x: x / 2 + 1, -3, 5, BLUE, "f")], segs=[yx(-3, 5)], points=[(-2, 0, "(−2, 0)"), (0, 1, "(0, 1)"), (2, 2, "(2, 2)"), (4, 3, "")])
KEY_SK = plane((-3, 5, 1), (-3, 5, 1), curves=[(lambda x: x / 2 + 1, -3, 5, BLUE, "f"), (lambda x: 2 * x - 2, -0.5, 3.5, RED, INV)], segs=[yx(-3, 5)],
               points=[(0, -2, ""), (1, 0, ""), (2, 2, ""), (3, 4, "")])
FIG_T1 = plane((-4, 5, 1), (-4, 5, 1), curves=[(lambda x: 3 * x - 3, -1 / 3, 8 / 3, BLUE, "f")], segs=[yx(-4, 5)],
               points=[(0, -3, ""), (1, 0, ""), (2, 3, "")], labels=[(-3.8, -3.4, "y = x", GREY)])

SUB = []

# ================================================================== Subbab 1
SUB.append(dict(
    title="Fungsi Satu-satu dan Syarat Invers",
    tujuan="Menjelaskan arti invers sebuah fungsi, memeriksa apakah fungsi mempunyai invers, dan membatasi domain agar inversnya ada.",
    konsep=[
        "Fungsi f dari A ke B memasangkan setiap x di A dengan tepat satu f(x) di B. <b>Invers</b> f membalik setiap pasangan: jika f(a) = b, maka " + INV + "(b) = a. Invers adalah proses kebalikan, yaitu dari hasil kembali ke asal.",
        "Pembalikan itu menghasilkan fungsi hanya bila f <b>bijektif</b>: <b>injektif</b> (satu-satu, setiap dua x yang berbeda menghasilkan nilai yang berbeda) dan <b>surjektif</b> (setiap anggota B terpakai, jadi range = kodomain). Fungsi yang mempunyai fungsi invers disebut fungsi yang <b>invertibel</b>.",
        "<b>Uji garis mendatar:</b> fungsi real injektif bila setiap garis mendatar memotong grafiknya paling banyak di satu titik. Fungsi yang selalu naik atau selalu turun pasti injektif.",
        "Fungsi yang tidak injektif dapat dibuat injektif dengan <b>membatasi domainnya</b>, misalnya g(x) = x² untuk x ≥ 0 saja. Domain " + INV + " adalah range f, dan range " + INV + " adalah domain f.",
    ],
    rumus=["f(a) = b ⇔ " + INV + "(b) = a", "Injektif: f(x₁) = f(x₂) ⇒ x₁ = x₂", "Domain " + INV + " = range f; range " + INV + " = domain f",
           INV + "(x) adalah fungsi invers, bukan " + fr("1", "f(x)")],
    contoh=[
        ("Fungsi pada himpunan", "Fungsi f dari A = {1, 2, 3, 4} ke B = {4, 6, 8, 10} adalah f = {(1, 4), (2, 6), (3, 8), (4, 10)}. Apakah f mempunyai invers? Jika ya, tuliskan " + INV + " dan hitung " + INV + "(8).", None,
         ["Setiap anggota B dipasangkan dengan tepat satu anggota A (4, 6, 8, 10 masing-masing muncul sekali), jadi f bijektif.",
          "Balik setiap pasangan: " + INV + " = {(4, 1), (6, 2), (8, 3), (10, 4)}.", INV + "(8) = 3 karena f(3) = 8."],
         INV + " = {(4, 1), (6, 2), (8, 3), (10, 4)}; " + INV + "(8) = 3"),
        ("Membatasi domain", "Tunjukkan bahwa g(x) = x² − 4x dengan domain semua bilangan real tidak mempunyai invers, lalu tentukan domain x ≥ k terbesar agar inversnya ada.", FIG_TIDAK,
         ["g(1) = 1 − 4 = −3 dan g(3) = 9 − 12 = −3: dua x berbeda memberi nilai sama, jadi g tidak injektif. Pada grafik, garis y = −3 memotong dua kali.",
          "g(x) = (x − 2)² − 4, jadi puncaknya (2, −4). Di kanan puncak grafik selalu naik.", "Domain x ≥ 2 membuat g injektif; range-nya y ≥ −4."],
         "tidak injektif; domain x ≥ 2"),
    ],
    bertahap=dict(
        soal="Fungsi f(x) = 2x + 1 didefinisikan pada domain {0, 1, 2, 3}. Tentukan domain dan range " + INV + ".",
        langkah=["Range f: f(0) = ____, f(1) = ____, f(2) = ____, f(3) = ____.", "Domain " + INV + " = range f = {____}.", "Range " + INV + " = domain f = {____}."],
        cek="Domain dan range bertukar karena",
        opsi=["(a) invers membalik setiap pasangan (x, y) menjadi (y, x)", "(b) fungsi linear selalu mempunyai domain sama dengan range"],
        kunci="1, 3, 5, 7; domain " + INV + " = {1, 3, 5, 7}; range " + INV + " = {0, 1, 2, 3}. Alasan: (a).",
    ),
    jebakan=[INV + "(x) bukan " + fr("1", "f(x)") + ". Untuk f(x) = 2x: " + INV + "(8) = 4, sedangkan " + fr("1", "f(8)") + " = " + fr("1", "16") + ".",
             "Uji garis <b>mendatar</b> menentukan injektif; uji garis <b>tegak</b> hanya menentukan apakah grafik itu fungsi.",
             "Saat membatasi domain fungsi kuadrat, batasnya adalah absis puncak, bukan titik potong sumbu x."],
    latihan=[
        Q(1, "Diketahui f = {(1, 3), (2, 5), (3, 7)}. Tuliskan " + INV + ".", "{(3, 1), (5, 2), (7, 3)}", "Balik setiap pasangan."),
        Q(1, "Diketahui g = {(−1, 1), (0, 0), (1, 1)}. Apakah pembalikan g merupakan fungsi?", "tidak", "Pembalikannya memuat (1, −1) dan (1, 1): nilai 1 dipasangkan dengan dua nilai."),
        Q(1, "Fungsi f invertibel dan f(4) = 9. Tentukan " + INV + "(9).", "4", "f(4) = 9 ⇔ " + INV + "(9) = 4."),
        Q(1, "Untuk f(x) = 2x, hitung " + INV + "(8) dan " + fr("1", "f(8)") + ".", "4 dan " + fr("1", "16"), INV + "(8): bilangan yang dikali 2 menjadi 8; f(8) = 16."),
        Q(1, "Manakah yang injektif pada semua bilangan real: f(x) = 3x − 1, g(x) = x², h(x) = 5?", "f saja", "g(−1) = g(1); h bernilai 5 untuk setiap x; f selalu naik."),
        Q(2, "Fungsi f(x) = x² didefinisikan pada {−2, −1, 0, 1, 2}. Tentukan range-nya dan periksa apakah f injektif.", "{0, 1, 4}; tidak injektif", "f(−2) = f(2) = 4 dan f(−1) = f(1) = 1."),
        Q(2, "Nilai f(x) untuk x = 1, 2, 3, 4, 5 berturut-turut 2, 5, 10, 17, 26. Hitung " + INV + "(17) + " + INV + "(5).", "6", INV + "(17) = 4 dan " + INV + "(5) = 2."),
        Q(2, "Fungsi f(x) = (x − 3)² + 1 dibatasi pada x ≥ k. Tentukan k terkecil agar f invertibel, lalu tentukan domain " + INV + ".", "k = 3; x ≥ 1", "Puncak (3, 1); untuk x ≥ 3 grafik naik dan nilainya mulai dari 1."),
        Q(2, "Fungsi f memasangkan A = {a, b, c} ke B = {1, 2, 3, 4}. Mungkinkah f mempunyai fungsi invers dari B ke A? Jelaskan.", "tidak mungkin",
          "Paling banyak 3 anggota B terpakai, jadi ada anggota B yang tidak mempunyai pasangan: f tidak surjektif."),
        Q(3, "Buktikan bahwa f(x) = 5 − 2x injektif.", "terbukti", "f(a) = f(b) → 5 − 2a = 5 − 2b → a = b."),
        Q(3, "Fungsi f(x) = x² + 6x + 5 dibatasi pada x ≤ k. Tentukan k terbesar agar f invertibel, lalu tentukan domain " + INV + ".", "k = −3; x ≥ −4",
          "f(x) = (x + 3)² − 4; di kiri puncak (−3, −4) grafik selalu turun, dan nilainya paling kecil −4."),
        Q(3, "Untuk fungsi real f(x) = x³ − x, periksa apakah f injektif dengan menghitung f(−1), f(0), dan f(1).", "tidak injektif", "f(−1) = f(0) = f(1) = 0: garis y = 0 memotong grafik di tiga titik."),
    ],
))

# ================================================================== Subbab 2
SUB.append(dict(
    title="Rumus Invers Fungsi Linear",
    tujuan="Menentukan rumus invers fungsi linear dengan langkah tukar-selesaikan, memeriksanya, dan menafsirkannya dalam konteks.",
    konsep=[
        "Langkah menentukan " + INV + "(x): (1) tulis y = f(x); (2) nyatakan x dalam y; (3) ganti nama variabel, x menjadi " + INV + "(y) lalu tulis dengan x. Hasilnya <b>selalu diuji</b>: f(" + INV + "(x)) harus sama dengan x.",
        "Invers membalik <b>urutan dan jenis</b> operasi. f(x) = 2x − 5 berarti \"kalikan 2, lalu kurangi 5\"; inversnya \"tambah 5, lalu bagi 2\": " + INV + "(x) = " + fr("x + 5", "2") + ".",
        "Fungsi linear f(x) = ax + b dengan a ≠ 0 selalu invertibel, dan inversnya juga linear dengan gradien " + fr("1", "a") + ".",
        "Dalam soal cerita, f mengubah masukan menjadi hasil (misalnya modal menjadi harga jual), sedangkan " + INV + " menghitung masukan dari hasil yang diketahui.",
    ],
    rumus=["f(x) = ax + b, a ≠ 0 → " + INV + "(x) = " + fr("x − b", "a"), "Uji: f(" + INV + "(x)) = x dan " + INV + "(f(x)) = x",
           "f(x) = " + fr("ax + b", "c") + " → " + INV + "(x) = " + fr("cx − b", "a")],
    contoh=[
        ("Langkah tukar-selesaikan", "Tentukan " + INV + "(x) untuk f(x) = 3x − 6, lalu uji dengan x = 4.", None,
         ["y = 3x − 6 → 3x = y + 6 → x = " + fr("y + 6", "3") + ".", INV + "(x) = " + fr("x + 6", "3") + ", atau " + fr("x", "3") + " + 2.",
          "Uji: f(4) = 6 dan " + INV + "(6) = 12 : 3 = 4. Kembali ke asal."], INV + "(x) = " + fr("x + 6", "3")),
        ("Harga jual dan modal", "Seorang pedagang menetapkan harga jual h(x) = 1,25x + 2.000 rupiah untuk barang bermodal x rupiah. Tentukan rumus h⁻¹ dan modal barang yang dijual Rp27.000.", None,
         ["y = 1,25x + 2.000 → x = " + fr("y − 2.000", "1,25") + ".", "h⁻¹(x) = " + fr("x − 2.000", "1,25") + " = 0,8(x − 2.000): dari harga jual ke modal.",
          "h⁻¹(27.000) = 0,8 · 25.000 = 20.000. Uji: 1,25 · 20.000 + 2.000 = 27.000."], "modal Rp20.000"),
    ],
    bertahap=dict(
        soal="Tentukan " + INV + "(x) untuk f(x) = " + fr("2x − 5", "3") + ", lalu hitung " + INV + "(1).",
        langkah=["y = " + fr("2x − 5", "3") + " → 3y = ____.", "2x = 3y + ____ → x = ____.", INV + "(x) = ____, sehingga " + INV + "(1) = ____."],
        cek="Hasil " + INV + "(1) dapat diuji dengan",
        opsi=["(a) menghitung f(" + INV + "(1)) yang harus bernilai 1", "(b) menghitung f(1) yang harus sama dengan " + INV + "(1)"],
        kunci="3y = 2x − 5; x = " + fr("3y + 5", "2") + "; " + INV + "(x) = " + fr("3x + 5", "2") + ", " + INV + "(1) = 4 (cek f(4) = 1). Alasan: (a).",
    ),
    jebakan=["Invers f(x) = 4x + 8 adalah " + fr("x − 8", "4") + ", bukan " + fr("x", "4") + " − 8: operasi terakhir pada f dibalik paling dulu.",
             "Jangan hanya membalik tanda: invers 2x − 5 bukan −2x + 5.",
             "Setelah x dinyatakan dalam y, jangan lupa menulis hasilnya sebagai fungsi x."],
    latihan=[
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = x + 7.", "x − 7", "Kebalikan menambah 7 adalah mengurangi 7."),
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = 4x.", fr("x", "4"), "Kebalikan mengali 4 adalah membagi 4."),
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = 2x − 8.", fr("x + 8", "2"), "y + 8 = 2x."),
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = 5 − x.", "5 − x (sama dengan f)", "y = 5 − x → x = 5 − y."),
        Q(1, "Untuk f(x) = 3x + 1, tentukan " + INV + "(10) tanpa mencari rumus inversnya.", "3", "3x + 1 = 10 → x = 3."),
        Q(2, "Tentukan " + INV + "(x) untuk f(x) = " + fr("3x + 4", "5") + ".", fr("5x − 4", "3"), "5y = 3x + 4 → x = (5y − 4) : 3."),
        Q(2, "Tentukan " + INV + "(x) untuk f(x) = −½x + 3.", "6 − 2x", "½x = 3 − y → x = 6 − 2y. Uji: −½(6 − 2x) + 3 = x."),
        Q(2, "Diketahui f(x) = ax + 2 dan " + INV + "(8) = 3. Tentukan a.", "a = 2", "f(3) = 8 → 3a + 2 = 8."),
        Q(2, "Suhu dalam Fahrenheit dihitung dari Celsius dengan F(C) = 1,8C + 32. Tentukan F⁻¹ dan suhu Celsius untuk 104 °F.", "F⁻¹(x) = " + fr("x − 32", "1,8") + "; 40 °C", "(104 − 32) : 1,8 = 72 : 1,8 = 40."),
        Q(3, "Diketahui f(x) = ax + b dan " + INV + "(x) = 2x − 6. Tentukan a dan b.", "a = ½, b = 3", "f adalah invers dari " + INV + ": y = 2x − 6 → x = ½y + 3, jadi f(x) = ½x + 3."),
        Q(3, "Fungsi linear f memenuhi f(1) = 5 dan f(3) = 11. Tentukan " + INV + "(20).", "6", "m = 6 : 2 = 3; f(x) = 3x + 2; 3x + 2 = 20 → x = 6."),
        Q(3, "Tarif taksi B(x) = 4.000x + 6.000 rupiah untuk x km. Tentukan B⁻¹, jelaskan artinya, lalu hitung jarak jika penumpang membayar Rp50.000.", "B⁻¹(x) = " + fr("x − 6.000", "4.000") + "; jarak dari tarif; 11 km",
          "B⁻¹ mengubah besar tarif (rupiah) menjadi jarak (km); (50.000 − 6.000) : 4.000 = 11."),
    ],
))

# ================================================================== Subbab 3
SUB.append(dict(
    title="Invers Fungsi Rasional, Kuadrat, dan Akar",
    tujuan="Menentukan invers fungsi rasional linear, fungsi kuadrat dengan domain terbatas, fungsi akar, dan fungsi pangkat tiga, beserta domainnya.",
    konsep=[
        "Untuk f(x) = " + fr("ax + b", "cx + d") + " dengan x ≠ −" + fr("d", "c") + ": y(cx + d) = ax + b → cxy − ax = b − dy → x = " + fr("−dy + b", "cy − a") + ". Jadi " + INV + "(x) = " + fr("−dx + b", "cx − a") + " dengan x ≠ " + fr("a", "c") + ".",
        "Cara cepat: <b>tukar letak a dan d, lalu ganti tanda keduanya</b>; b dan c tetap. Syaratnya ad − bc ≠ 0 (jika ad − bc = 0, f bernilai konstan).",
        "Fungsi kuadrat hanya invertibel pada domain terbatas. Tulis dulu f(x) = (x − p)² + q. Untuk x ≥ p, " + INV + "(x) = p + √(x − q); untuk x ≤ p, " + INV + "(x) = p − √(x − q). Domain " + INV + ": x ≥ q.",
        "Fungsi pangkat tiga x³ selalu naik, jadi invertibel pada semua bilangan real: inversnya ∛x. Invers √x (x ≥ 0) adalah x² dengan x ≥ 0.",
    ],
    rumus=["f(x) = " + fr("ax + b", "cx + d") + ", x ≠ −" + fr("d", "c") + " → " + INV + "(x) = " + fr("−dx + b", "cx − a") + ", x ≠ " + fr("a", "c"),
           "f(x) = (x − p)² + q, x ≥ p → " + INV + "(x) = p + √(x − q), x ≥ q", "f(x) = x³ + k → " + INV + "(x) = ∛(x − k)",
           "f(x) = √(x − p), x ≥ p → " + INV + "(x) = x² + p, x ≥ 0"],
    contoh=[
        ("Fungsi rasional", "Tentukan " + INV + "(x) untuk f(x) = " + fr("2x + 1", "x − 3") + ", x ≠ 3, lalu uji dengan x = 4.", None,
         ["a = 2, b = 1, c = 1, d = −3. Tukar a dan d lalu ganti tandanya: pembilang 3x + 1, penyebut x − 2.",
          INV + "(x) = " + fr("3x + 1", "x − 2") + " dengan x ≠ 2.", "Uji: f(4) = 9 : 1 = 9 dan " + INV + "(9) = 28 : 7 = 4."], INV + "(x) = " + fr("3x + 1", "x − 2") + ", x ≠ 2"),
        ("Fungsi kuadrat", "Tentukan " + INV + "(x) untuk f(x) = x² − 4x + 7 dengan x ≥ 2.", None,
         ["f(x) = (x − 2)² + 3. Tulis y = (x − 2)² + 3 → (x − 2)² = y − 3.", "Karena x ≥ 2, x − 2 = +√(y − 3), jadi x = 2 + √(y − 3).",
          INV + "(x) = 2 + √(x − 3), x ≥ 3. Uji: f(5) = 12 dan " + INV + "(12) = 2 + 3 = 5."], INV + "(x) = 2 + √(x − 3), x ≥ 3"),
    ],
    bertahap=dict(
        soal="Tentukan " + INV + "(x) untuk f(x) = " + fr("x + 5", "2x − 1") + ", x ≠ ½.",
        langkah=["y(2x − 1) = x + 5 → 2xy − y = ____.", "2xy − x = y + 5 → x(____) = y + 5.", "x = ____, jadi " + INV + "(x) = ____, x ≠ ____."],
        cek="Hasilnya sama dengan f karena",
        opsi=["(a) a = 1 dan d = −1, sehingga menukar dan mengganti tanda keduanya tidak mengubah apa pun", "(b) setiap fungsi rasional sama dengan inversnya"],
        kunci="2xy − y = x + 5; x(2y − 1) = y + 5; x = " + fr("y + 5", "2y − 1") + ", " + INV + "(x) = " + fr("x + 5", "2x − 1") + ", x ≠ ½. Alasan: (a).",
    ),
    jebakan=["Pada " + fr("−dx + b", "cx − a") + ", yang tandanya diganti adalah a dan d; b dan c tetap.",
             "Domain " + INV + " untuk fungsi rasional adalah x ≠ " + fr("a", "c") + ", bukan x ≠ −" + fr("d", "c") + " (itu domain f).",
             "Pada fungsi kuadrat, tanda di depan akar ditentukan oleh domain: x ≥ p memakai +√, x ≤ p memakai −√. Jangan menulis ±.",
             "Lengkapkan kuadrat dulu; menarik akar langsung dari x² − 4x + 7 tidak mungkin."],
    latihan=[
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = x³.", "∛x", "y = x³ → x = ∛y."),
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = √x, x ≥ 0.", "x², x ≥ 0", "y = √x → x = y²; nilai √x tidak pernah negatif."),
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = " + fr("x + 2", "x − 4") + ", x ≠ 4.", fr("4x + 2", "x − 1") + ", x ≠ 1", "a = 1, d = −4: tukar dan ganti tanda."),
        Q(1, "Tentukan " + INV + "(x) untuk f(x) = " + fr("3", "x") + ", x ≠ 0.", fr("3", "x") + " (sama dengan f)", "xy = 3 → x = 3/y."),
        Q(1, "Untuk f(x) = " + fr("2x", "x + 3") + ", tentukan " + INV + "(1).", "3", "2x = x + 3 → x = 3."),
        Q(2, "Tentukan " + INV + "(x) untuk f(x) = " + fr("3x − 2", "2x + 1") + ", x ≠ −½.", fr("x + 2", "3 − 2x") + ", x ≠ " + fr("3", "2"),
          "a = 3, b = −2, c = 2, d = 1: (−x − 2) : (2x − 3), lalu pembilang dan penyebut dikali −1."),
        Q(2, "Tentukan " + INV + "(x) untuk f(x) = x² + 2, x ≥ 0.", "√(x − 2), x ≥ 2", "x² = y − 2 dan x ≥ 0."),
        Q(2, "Tentukan " + INV + "(x) untuk f(x) = (x + 1)², x ≤ −1.", "−1 − √x, x ≥ 0", "x + 1 ≤ 0, jadi x + 1 = −√y."),
        Q(2, "Tentukan " + INV + "(x) untuk f(x) = √(2x − 4), x ≥ 2.", fr("x² + 4", "2") + ", x ≥ 0", "y² = 2x − 4 → x = (y² + 4) : 2."),
        Q(3, "Diketahui f(x) = " + fr("ax + 1", "x − 2") + " dan " + INV + "(3) = 4. Tentukan a.", "a = " + fr("5", "4"), "f(4) = 3 → (4a + 1) : 2 = 3 → 4a = 5."),
        Q(3, "Tentukan k agar f(x) = " + fr("kx + 3", "x − 2") + " sama dengan inversnya.", "k = 2", INV + "(x) = (2x + 3) : (x − k); sama dengan f bila k = 2 (a = −d). Cek ad − bc = −4 − 3 ≠ 0."),
        Q(3, "Diketahui f(x) = x² − 6x + 5 dengan x ≥ 3. Tentukan " + INV + "(x) beserta domainnya, lalu hitung " + INV + "(12).", "3 + √(x + 4), x ≥ −4; 7",
          "f(x) = (x − 3)² − 4; " + INV + "(12) = 3 + √16 = 7. Cek f(7) = 49 − 42 + 5 = 12."),
    ],
))

# ================================================================== Subbab 4
SUB.append(dict(
    title="Grafik Fungsi Invers",
    tujuan="Menggambar grafik " + INV + " sebagai pencerminan grafik f terhadap garis y = x dan memakai sifat itu untuk titik, asimtot, dan titik potong.",
    konsep=[
        "Titik (a, b) terletak pada grafik f jika dan hanya jika (b, a) terletak pada grafik " + INV + ". Menukar koordinat sama dengan <b>mencerminkan terhadap garis y = x</b>, jadi grafik " + INV + " adalah bayangan cermin grafik f terhadap y = x.",
        "Cara menggambar: ambil beberapa titik pada f, tukar koordinatnya, lalu hubungkan. Titik pada garis y = x tidak berpindah.",
        "Fungsi eksponen y = aˣ dan logaritma y = ᵃlog x saling invers: grafik y = 2ˣ melalui (0, 1), (1, 2), (2, 4), sedangkan y = ²log x melalui (1, 0), (2, 1), (4, 2). Asimtot y = 0 pada 2ˣ menjadi asimtot x = 0 pada ²log x.",
        "Untuk fungsi rasional " + fr("ax + b", "cx + d") + ", asimtot tegak x = −" + fr("d", "c") + " dan asimtot datar y = " + fr("a", "c") + " bertukar peran pada inversnya. Jika f selalu naik, titik potong grafik f dan " + INV + " terletak pada garis y = x, jadi dicari dari f(x) = x.",
    ],
    rumus=["(a, b) pada f ⇔ (b, a) pada " + INV, "Grafik " + INV + " = cermin grafik f terhadap y = x",
           "Asimtot f: x = −" + fr("d", "c") + ", y = " + fr("a", "c") + " → asimtot " + INV + ": x = " + fr("a", "c") + ", y = −" + fr("d", "c"),
           "f naik: titik potong f dan " + INV + " dari f(x) = x"],
    contoh=[
        ("Garis dan bayangannya", "Gambarkan grafik f(x) = 2x − 2 dan " + INV + " pada satu bidang, lalu tentukan titik potong keduanya.", FIG_REF,
         ["Titik pada f: (0, −2), (1, 0), (3, 4). Tukar koordinatnya: (−2, 0), (0, 1), (4, 3) terletak pada " + INV + ".",
          INV + "(x) = " + fr("x + 2", "2") + " = ½x + 1; grafiknya melalui ketiga titik itu.", "f naik, jadi titik potongnya pada y = x: 2x − 2 = x → x = 2. Titik potongnya (2, 2)."],
         INV + "(x) = ½x + 1; titik potong (2, 2)"),
        ("Eksponen dan logaritma", "Gambarkan y = 2ˣ dan inversnya, lalu tentukan " + INV + "(8) dan " + INV + "(½) untuk f(x) = 2ˣ.", FIG_EXP,
         ["y = 2ˣ ⇔ x = ²log y, jadi " + INV + "(x) = ²log x dengan x &gt; 0.", "Titik (0, 1), (1, 2), (2, 4) pada 2ˣ menjadi (1, 0), (2, 1), (4, 2) pada ²log x.",
          INV + "(8) = ²log 8 = 3 dan " + INV + "(½) = ²log ½ = −1."], INV + "(x) = ²log x; 3 dan −1"),
    ],
    bertahap=dict(
        soal="Tentukan titik potong grafik f(x) = 3x − 4 dengan grafik inversnya.",
        langkah=["f naik (gradien 3 &gt; 0), jadi titik potongnya terletak pada garis y = ____.", "Selesaikan f(x) = x: 3x − 4 = x → x = ____.", "Titik potongnya (____, ____). Cek: " + INV + "(x) = ____ juga melalui titik itu."],
        cek="Titik potong dicari dari f(x) = x karena",
        opsi=["(a) grafik f dan " + INV + " saling cermin terhadap y = x, dan untuk f naik keduanya bertemu pada garis itu", "(b) setiap fungsi memotong garis y = x"],
        kunci="y = x; x = 2; (2, 2); " + INV + "(x) = " + fr("x + 4", "3") + ", dan (2 + 4) : 3 = 2. Alasan: (a).",
    ),
    jebakan=["Cermin terhadap y = x menukar koordinat: (3, −5) menjadi (−5, 3), bukan (3, 5) atau (−3, 5).",
             "Grafik " + INV + " bukan grafik " + fr("1", "f(x)") + " dan bukan cermin terhadap sumbu y.",
             "Rumus f(x) = x untuk titik potong hanya dijamin berlaku bila f naik. Untuk f(x) = −x + 3, f dan " + INV + " berimpit."],
    latihan=[
        Q(1, "Titik (2, 5) terletak pada grafik f. Titik mana yang pasti terletak pada grafik " + INV + "?", "(5, 2)", "Tukar koordinat."),
        Q(1, "Grafik f melalui (−1, 3). Tentukan " + INV + "(3).", "−1", "f(−1) = 3."),
        Q(1, "Grafik fungsi linear f ditunjukkan di bawah. Baca " + INV + "(5) dan " + INV + "(1).", "2 dan 0", "f(2) = 5 dan f(0) = 1.", fig=FIG_L4),
        Q(1, "Domain f adalah 0 ≤ x ≤ 4 dan range-nya 1 ≤ y ≤ 9. Tentukan domain dan range " + INV + ".", "domain 1 ≤ x ≤ 9; range 0 ≤ y ≤ 4", "Domain dan range bertukar."),
        Q(1, "Tentukan bayangan titik (−3, 1) oleh pencerminan terhadap garis y = x.", "(1, −3)", "Tukar koordinat."),
        Q(2, "Grafik f di bawah melalui titik-titik yang ditandai. Gambarlah grafik " + INV + " pada bidang yang sama, lalu tuliskan rumusnya.", INV + "(x) = 2x − 2",
          "Tukar koordinat: (0, −2), (1, 0), (2, 2), (3, 4). Gradien 2, potong sumbu y di −2.", fig=FIG_SK, kfig=KEY_SK),
        Q(2, "Tentukan titik potong grafik f(x) = 4x − 9 dengan grafik inversnya.", "(3, 3)", "f naik; 4x − 9 = x → x = 3."),
        Q(2, "Tentukan asimtot grafik f(x) = " + fr("2x + 1", "x − 3") + " dan asimtot grafik inversnya.", "f: x = 3, y = 2; " + INV + ": x = 2, y = 3", "Asimtot bertukar; cek " + INV + "(x) = (3x + 1) : (x − 2)."),
        Q(2, "Untuk f(x) = 2ˣ, hitung " + INV + "(16) dan " + INV + "(" + fr("1", "4") + ").", "4 dan −2", "²log 16 = 4; ²log ¼ = −2."),
        Q(3, "Tentukan titik potong grafik f(x) = x² − 2 (x ≥ 0) dengan grafik inversnya.", "(2, 2)", "f naik pada x ≥ 0; x² − 2 = x → (x − 2)(x + 1) = 0; x = −1 tidak memenuhi x ≥ 0."),
        Q(3, "Tunjukkan bahwa grafik f(x) = −x + 3 sama dengan grafik inversnya, dan jelaskan secara geometris.", INV + "(x) = −x + 3 = f(x)",
          "y = −x + 3 → x = 3 − y. Garis itu tegak lurus y = x (gradien −1), jadi bayangan cerminnya adalah garis itu sendiri."),
        Q(3, "Grafik fungsi linear f melalui (1, 4), dan grafik " + INV + " melalui (2, 0). Tentukan f(x) dan " + INV + "(10).", "f(x) = 2x + 2; " + INV + "(10) = 4",
          "(2, 0) pada " + INV + " berarti f(0) = 2, jadi b = 2; a + 2 = 4 → a = 2; 2x + 2 = 10 → x = 4."),
    ],
))

# ================================================================== Subbab 5
SUB.append(dict(
    title="Invers dan Komposisi Fungsi",
    tujuan="Memakai sifat f ∘ " + INV + " = I dan (f ∘ g)⁻¹ = g⁻¹ ∘ " + INV + " untuk menentukan invers fungsi komposisi dan fungsi yang belum diketahui.",
    konsep=[
        "Fungsi dan inversnya saling meniadakan: (f ∘ " + INV + ")(x) = x dan (" + INV + " ∘ f)(x) = x. Fungsi I(x) = x disebut <b>fungsi identitas</b>.",
        "Invers komposisi dibalik urutannya: (f ∘ g)⁻¹ = g⁻¹ ∘ " + INV + ". Seperti memakai kaus kaki lalu sepatu: membukanya dimulai dari sepatu. Pada f ∘ g, g dikerjakan dulu, jadi " + INV + " dikerjakan dulu saat membalik.",
        "Jika f dan h = f ∘ g diketahui, g dicari dengan g = " + INV + " ∘ h. Jika g dan h = f ∘ g diketahui, f dicari dengan f = h ∘ g⁻¹, yaitu f(x) = h(g⁻¹(x)).",
        "Logaritma dan eksponen berbasis sama saling invers: a<sup>ᵃlog x</sup> = x untuk x &gt; 0 dan ᵃlog aˣ = x.",
    ],
    rumus=["(f ∘ " + INV + ")(x) = (" + INV + " ∘ f)(x) = x", "(f ∘ g)⁻¹(x) = (g⁻¹ ∘ " + INV + ")(x)", "f ∘ g = h → g = " + INV + " ∘ h dan f = h ∘ g⁻¹",
           "f(x) = aˣ ⇔ " + INV + "(x) = ᵃlog x"],
    contoh=[
        ("Invers komposisi", "Diketahui f(x) = 2x + 1 dan g(x) = x − 3. Tentukan (f ∘ g)⁻¹(x) dengan dua cara.", None,
         ["Cara 1: (f ∘ g)(x) = 2(x − 3) + 1 = 2x − 5, jadi (f ∘ g)⁻¹(x) = " + fr("x + 5", "2") + ".",
          "Cara 2: " + INV + "(x) = " + fr("x − 1", "2") + " dan g⁻¹(x) = x + 3. (g⁻¹ ∘ " + INV + ")(x) = " + fr("x − 1", "2") + " + 3 = " + fr("x + 5", "2") + ".",
          "Kedua cara memberi hasil yang sama."], "(f ∘ g)⁻¹(x) = " + fr("x + 5", "2")),
        ("Mencari fungsi dalam", "Diketahui f(x) = 3x − 1 dan (f ∘ g)(x) = 6x + 5. Tentukan g(x).", None,
         ["f(g(x)) = 3g(x) − 1 = 6x + 5.", "3g(x) = 6x + 6 → g(x) = 2x + 2.", "Cara invers: " + INV + "(x) = " + fr("x + 1", "3") + ", jadi g(x) = " + INV + "(6x + 5) = " + fr("6x + 6", "3") + " = 2x + 2."],
         "g(x) = 2x + 2"),
    ],
    bertahap=dict(
        soal="Diketahui g(x) = x + 2 dan (f ∘ g)(x) = 3x + 4. Tentukan f(x).",
        langkah=["g⁻¹(x) = ____.", "f(x) = (f ∘ g)(g⁻¹(x)) = 3(____) + 4.", "f(x) = ____. Cek: f(g(x)) = 3(x + 2) − 2 = ____."],
        cek="Yang dimasukkan ke (f ∘ g) adalah g⁻¹(x) karena",
        opsi=["(a) f(g(g⁻¹(x))) = f(x)", "(b) g⁻¹(x) selalu sama dengan −g(x)"],
        kunci="g⁻¹(x) = x − 2; 3(x − 2) + 4; f(x) = 3x − 2; cek 3x + 4. Alasan: (a).",
    ),
    jebakan=["(f ∘ g)⁻¹ = g⁻¹ ∘ " + INV + ", bukan " + INV + " ∘ g⁻¹: urutannya dibalik.",
             "Untuk mencari f dari f ∘ g, masukkan g⁻¹(x), bukan g(x), ke dalam f ∘ g.",
             "(" + INV + ")⁻¹ = f: invers dari invers adalah fungsi semula."],
    latihan=[
        Q(1, "Untuk f(x) = 5x − 2, hitung f(" + INV + "(7)).", "7", "f ∘ " + INV + " adalah identitas."),
        Q(1, "Diketahui f(x) = x + 4 dan g(x) = 2x. Tentukan (f ∘ g)(x) dan (f ∘ g)⁻¹(x).", "2x + 4 dan " + fr("x − 4", "2"), "f(g(x)) = 2x + 4."),
        Q(1, "Diketahui " + INV + "(x) = 3x + 2. Tentukan f(x).", fr("x − 2", "3"), "f adalah invers dari " + INV + "."),
        Q(1, "Diketahui f(x) = ³log x. Tentukan " + INV + "(x) dan " + INV + "(2).", "3ˣ dan 9", "y = ³log x ⇔ x = 3ʸ."),
        Q(1, "Untuk f(x) = 2ˣ, sederhanakan f(²log 5).", "5", "2<sup>²log 5</sup> = 5."),
        Q(2, "Diketahui f(x) = 2x − 3 dan (f ∘ g)(x) = 4x + 5. Tentukan g(x).", "2x + 4", "2g(x) − 3 = 4x + 5 → g(x) = 2x + 4."),
        Q(2, "Diketahui g(x) = 2x − 1 dan (f ∘ g)(x) = 6x + 1. Tentukan f(x).", "3x + 4", "g⁻¹(x) = (x + 1) : 2; f(x) = 6 · (x + 1)/2 + 1 = 3x + 4."),
        Q(2, "Diketahui f(x) = x − 1 dan g(x) = " + fr("x + 2", "x − 3") + ". Tentukan (g ∘ f)⁻¹(x).", fr("4x + 1", "x − 1") + ", x ≠ 1",
          "(g ∘ f)(x) = (x + 1) : (x − 4); a = 1, d = −4. Cek: g⁻¹(x) = (3x + 2) : (x − 1) dan f⁻¹(t) = t + 1."),
        Q(2, "Diketahui f(x) = 3x + 2 dan g(x) = " + fr("x − 1", "2") + ". Hitung (f ∘ g)⁻¹(8).", "5", INV + "(8) = 2, lalu g⁻¹(2) = 2 · 2 + 1 = 5. Cek: (f ∘ g)(5) = f(2) = 8."),
        Q(3, "Diketahui f(x) = 2x + 1 dan g(x) = x − 3. Tentukan x jika (" + INV + " ∘ g⁻¹)(x) = 4.", "x = 6", INV + " ∘ g⁻¹ = (g ∘ f)⁻¹, jadi x = (g ∘ f)(4) = f(4) − 3 = 6."),
        Q(3, "Toko memberi diskon 20%, lalu menambahkan pajak 10% dari harga setelah diskon. Pembeli membayar Rp132.000. Tentukan harga awal barang dengan memakai invers fungsi komposisi.", "Rp150.000",
          "d(x) = 0,8x, p(x) = 1,1x; (p ∘ d)(x) = 0,88x; (p ∘ d)⁻¹(132.000) = 132.000 : 0,88 = 150.000."),
        Q(3, "Diketahui f(x) = " + fr("x + 1", "x − 2") + " dan g(x) = 2x − 1. Tentukan (f ∘ g)⁻¹(x).", fr("3x", "2x − 2") + ", x ≠ 1",
          "(f ∘ g)(x) = 2x : (2x − 3); a = 2, b = 0, c = 2, d = −3 → 3x : (2x − 2)."),
    ],
))

CAMPURAN = [
    Q(1, "Tentukan " + INV + "(x) untuk f(x) = 7 − 3x.", fr("7 − x", "3"), "3x = 7 − y."),
    Q(1, "Titik (4, −1) terletak pada grafik f. Tentukan " + INV + "(−1).", "4", "f(4) = −1."),
    Q(1, "Tentukan " + INV + "(x) untuk f(x) = " + fr("x − 5", "x + 2") + ", x ≠ −2.", fr("2x + 5", "1 − x") + ", x ≠ 1", "a = 1, d = 2: (−2x − 5) : (x − 1)."),
    Q(2, "Tentukan " + INV + "(x) untuk f(x) = x² + 4x, x ≥ −2.", "−2 + √(x + 4), x ≥ −4", "f(x) = (x + 2)² − 4."),
    Q(2, "Diketahui f(x) = 2x − 5 dan g(x) = x + 3. Tentukan (f ∘ g)⁻¹(x).", fr("x − 1", "2"), "(f ∘ g)(x) = 2x + 1."),
    Q(2, "Diketahui " + INV + "(x) = " + fr("x + 1", "x − 3") + ", x ≠ 3. Tentukan f(x).", fr("3x + 1", "x − 1") + ", x ≠ 1", "f adalah invers dari " + INV + ": a = 1, d = −3."),
    Q(2, "Diketahui f(x) = 4ˣ. Hitung " + INV + "(32).", fr("5", "2"), "4ᵗ = 32 → 2²ᵗ = 2⁵ → t = 5/2."),
    Q(2, "Diketahui f(x) = " + fr("ax + b", "x + 1") + ", " + INV + "(1) = 2, dan " + INV + "(5) = 0. Tentukan a dan b.", "a = −1, b = 5", "f(0) = b = 5; f(2) = (2a + 5) : 3 = 1 → a = −1."),
    Q(3, "Fungsi linear f memenuhi f(0) = 4, dan grafik f memotong grafik " + INV + " di (1, 1). Tentukan f(x) dan " + INV + "(10).", "f(x) = −3x + 4; " + INV + "(10) = −2",
      "(1, 1) pada f: a + 4 = 1 → a = −3; −3x + 4 = 10 → x = −2."),
    Q(3, "Biaya laundry B(m) = 8.000m + 5.000 rupiah untuk m kg cucian. Tentukan B⁻¹, berat cucian bila tagihannya Rp61.000, dan berat terbesar (dalam kg bulat) yang dapat dicuci dengan Rp50.000.", "B⁻¹(x) = " + fr("x − 5.000", "8.000") + "; 7 kg; 5 kg",
      "(61.000 − 5.000) : 8.000 = 7; (50.000 − 5.000) : 8.000 = 5,625, jadi paling banyak 5 kg."),
]

TKA = [
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Grafik fungsi linear f dan garis y = x ditunjukkan berikut. Grafik f melalui titik-titik kisi yang ditandai.", fig=FIG_T1,
         soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=[INV + "(3) = 2", INV + "(0) = −3", "grafik " + INV + " melalui (−3, 0)", INV + "(−3) = 0", "grafik " + INV + " lebih curam daripada grafik f"], kunci=[0, 2, 3],
         bahas="Dari grafik: f(2) = 3, f(1) = 0, f(0) = −3. Jadi " + INV + "(3) = 2, " + INV + "(0) = 1, dan " + INV + "(−3) = 0, sehingga (−3, 0) pada " + INV + ".",
         salah="B: −3 adalah f(0); " + INV + "(0) = 1. E: f(x) = 3x − 3, jadi gradien " + INV + " adalah ⅓, lebih landai."),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Diketahui f(x) = " + fr("3x + 2", "x − 4") + ", x ≠ 4. Rumus " + INV + "(x) adalah ....",
         opsi=[fr("4x + 2", "x − 3"), fr("−4x + 2", "x − 3"), fr("4x + 2", "x + 3"), fr("x − 4", "3x + 2"), fr("4x − 2", "x − 3")], kunci=0,
         bahas="a = 3, b = 2, c = 1, d = −4. " + INV + "(x) = (−dx + b) : (cx − a) = (4x + 2) : (x − 3), x ≠ 3.",
         salah="B: tanda d tidak diganti. C: penyebut ditulis cx + a. D: memakai " + fr("1", "f(x)") + ". E: tanda b ikut diganti."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Diketahui f(x) = " + fr("ax − 1", "2x + 3") + " dan " + INV + "(1) = 2. Nilai a adalah ....",
         opsi=["4", "11", "3", "8", fr("7", "2")], kunci=0,
         bahas=INV + "(1) = 2 berarti f(2) = 1: (2a − 1) : 7 = 1 → 2a = 8 → a = 4.",
         salah="B: memakai f(1) = 2. C: tanda −1 tidak diganti saat pindah ruas (2a = 6). D: lupa membagi 2. E: suku −1 diabaikan."),
    dict(tipe="MAT-MODEL", lv=2, fmt="pg", soal="Sebuah toko menetapkan harga jual setiap barang sebesar 125% dari modalnya ditambah Rp4.000 untuk ongkos kemasan. Sebuah barang dijual Rp54.000. Modal barang itu adalah ....",
         opsi=["Rp40.000", "Rp39.200", "Rp71.500", "Rp46.400", "Rp50.000"], kunci=0,
         bahas="h(x) = 1,25x + 4.000, jadi h⁻¹(x) = (x − 4.000) : 1,25. h⁻¹(54.000) = 50.000 : 1,25 = 40.000.",
         salah="B: urutan operasi tidak dibalik (54.000 : 1,25 − 4.000). C: memakai h, bukan h⁻¹. D: ongkos kemasan ditambahkan. E: lupa membagi 1,25."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Suhu dalam °F dihitung dari suhu dalam °C dengan F(C) = 1,8C + 32. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["F⁻¹(212) = 100.", "F⁻¹(x) = " + fr("x − 32", "1,8") + " mengubah suhu °F menjadi °C.", "F⁻¹(50) = 18.", "Ada suhu yang angkanya sama dalam °C dan °F, yaitu −40."], kunci=[True, True, False, True],
         bahas="(212 − 32) : 1,8 = 100; (50 − 32) : 1,8 = 10, bukan 18; 1,8C + 32 = C → 0,8C = −32 → C = −40.", salah=""),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pgk", soal="Diketahui f(x) = x² − 2x + 3 dengan x ≥ 1. Pernyataan yang benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=[INV + "(x) = 1 + √(x − 2)", "domain " + INV + " adalah x ≥ 2", INV + "(11) = 4", INV + "(3) = 0", INV + "(x) = 1 − √(x − 2)"], kunci=[0, 1, 2],
         bahas="f(x) = (x − 1)² + 2; untuk x ≥ 1, " + INV + "(x) = 1 + √(x − 2) dengan x ≥ 2. f(4) = 11, jadi " + INV + "(11) = 4.",
         salah="D: f(0) = 3, tetapi 0 tidak termasuk domain; " + INV + "(3) = 2. E: tanda minus untuk domain x ≤ 1."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Diketahui f(x) = 2x + k dan " + INV + "(7) = 3. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["k = 1.", INV + "(x) = " + fr("x − 1", "2") + ".", INV + "(f(5)) = 11.", "(f ∘ " + INV + ")(x) = x untuk setiap x real."], kunci=[True, True, False, True],
         bahas="f(3) = 7 → 6 + k = 7 → k = 1. " + INV + "(f(5)) = 5, bukan f(5) = 11. f ∘ " + INV + " adalah identitas.", salah=""),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg",
         soal="Biaya mencetak n buku tahunan adalah B(n) = 12.000n + 300.000 rupiah. Panitia mempunyai anggaran Rp1.450.000 dan ingin mencetak sebanyak mungkin tanpa melebihi anggaran. Banyak buku yang dapat dicetak adalah ....",
         opsi=["95", "96", "120", "121", "145"], kunci=0,
         bahas="B⁻¹(1.450.000) = (1.450.000 − 300.000) : 12.000 = 95,8…. Buku harus bulat dan biaya tidak boleh melebihi anggaran, jadi 95 (B(95) = 1.440.000; B(96) = 1.452.000).",
         salah="B: dibulatkan ke atas, padahal B(96) melebihi anggaran. C, D: biaya tetap diabaikan. E: biaya tetap ditambahkan."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Diketahui f(x) = ax + b dengan a ≠ 0. Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=[INV + " juga fungsi linear", "jika a &gt; 0, " + INV + " juga naik", "grafik f dan " + INV + " selalu berpotongan", INV + "(b) = 0", INV + "(x) = " + fr("1", "ax + b")], kunci=[0, 1, 3],
         bahas=INV + "(x) = (x − b) : a, linear dengan gradien 1/a, yang bertanda sama dengan a. f(0) = b, jadi " + INV + "(b) = 0.",
         salah="C: untuk a = 1 dan b ≠ 0, f(x) = x + b dan " + INV + "(x) = x − b sejajar dan tidak berpotongan. E: itu " + fr("1", "f(x)") + "."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Diketahui f(x) = 3x − 2 dan (g ∘ f)(x) = 6x + 1. Nilai g⁻¹(9) adalah ....",
         opsi=["2", fr("4", "3"), "23", "7", fr("1", "23")], kunci=0,
         bahas="g(3x − 2) = 6x + 1 = 2(3x − 2) + 5, jadi g(t) = 2t + 5 dan g⁻¹(9) = (9 − 5) : 2 = 2. Cek: 6x + 1 = 9 → x = 4/3 dan f(4/3) = 2.",
         salah="B: nilai x, bukan f(x). C: menghitung g(9). D: tanda 5 tidak diganti ((9 + 5) : 2). E: memakai 1 : g(9)."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Invers f(x) = 4x + 8 adalah ....", [fr("x − 8", "4"), fr("x + 8", "4"), fr("x", "4") + " − 8", "4x − 8", fr("1", "4x + 8")], 0, "y − 8 = 4x.",
     "B: tanda 8 tidak diganti. C: urutan operasi tidak dibalik. D: hanya tanda yang dibalik. E: memakai 1/f(x)."),
    ("Diketahui f(x) = 6 − 2x. Nilai " + INV + "(10) adalah ....", ["−2", "2", "−14", "8", "−" + fr("1", "14")], 0, "6 − 2x = 10 → x = −2.",
     "B: tanda salah. C: menghitung f(10). D: (10 + 6) : 2. E: memakai 1/f(10)."),
    ("Fungsi dari {1, 2, 3} ke {a, b, c} yang mempunyai fungsi invers adalah ....",
     ["{(1, a), (2, b), (3, c)}", "{(1, a), (2, a), (3, b)}", "{(1, a), (1, b), (2, c)}", "{(1, b), (2, b), (3, b)}", "{(1, a), (2, c), (3, a)}"], 0,
     "Setiap anggota kodomain dipakai tepat sekali.", "B, E: dua anggota domain dipetakan ke nilai yang sama. C: bukan fungsi (1 mempunyai dua pasangan). D: fungsi konstan."),
    ("Invers f(x) = " + fr("2x − 1", "x + 3") + ", x ≠ −3, adalah ....", [fr("−3x − 1", "x − 2"), fr("3x − 1", "x − 2"), fr("−3x + 1", "x − 2"), fr("−3x − 1", "x + 2"), fr("x + 3", "2x − 1")], 0,
     "a = 2, b = −1, c = 1, d = 3: (−3x − 1) : (x − 2).", "B: tanda d tidak diganti. C: tanda b ikut diganti. D: penyebut cx + a. E: memakai 1/f(x)."),
    ("Domain invers f(x) = " + fr("4x + 1", "2x − 6") + " adalah ....", ["x ≠ 2", "x ≠ 3", "x ≠ −¼", "x ≠ −2", "x ≠ ½"], 0, INV + "(x) = (6x + 1) : (2x − 4); x ≠ a/c = 2.",
     "B: domain f. C: pembuat nol pembilang f. D: tanda salah. E: memakai c/a."),
    ("Titik (3, −5) terletak pada grafik f. Titik yang terletak pada grafik " + INV + " adalah ....", ["(−5, 3)", "(3, 5)", "(−3, 5)", "(5, −3)", "(−3, −5)"], 0, "Tukar koordinat.",
     "B: cermin terhadap sumbu x. C: cermin terhadap titik asal. D: cermin terhadap y = −x. E: cermin terhadap sumbu y."),
    ("Invers f(x) = x² − 8x + 10 dengan x ≥ 4 adalah ....", ["4 + √(x + 6)", "4 − √(x + 6)", "4 + √(x − 6)", "−4 + √(x + 6)", "4 + √(x − 10)"], 0,
     "f(x) = (x − 4)² − 6, jadi " + INV + "(x) = 4 + √(x + 6), x ≥ −6.", "B: tanda akar untuk x ≤ 4. C: tanda q salah. D: tanda p salah. E: konstanta tidak dilengkapkan kuadratnya."),
    ("Invers f(x) = ³log(x − 1), x &gt; 1, adalah ....", ["3ˣ + 1", "3ˣ − 1", "3<sup>x−1</sup>", "x³ + 1", "³log(x + 1)"], 0, "y = ³log(x − 1) ⇔ x − 1 = 3ʸ.",
     "B: tanda 1 salah. C: 1 dikurangkan di eksponen. D: pangkat dan basis tertukar. E: hanya tanda yang diganti."),
    ("Grafik f(x) = 5x − 8 dan grafik inversnya berpotongan di titik ....", ["(2, 2)", "(" + fr("8", "5") + ", 0)", "(0, −8)", "(8, 8)", "(−2, −2)"], 0, "f naik; 5x − 8 = x → x = 2.",
     "B: titik potong f dengan sumbu x. C: titik potong f dengan sumbu y. D: hanya konstanta yang dipakai. E: tanda −8 tidak diganti saat pindah ruas."),
    ("Diketahui f(x) = 2x + 1 dan g(x) = 3x. (f ∘ g)⁻¹(x) adalah ....", [fr("x − 1", "6"), fr("x − 3", "6"), "6x + 1", fr("x + 1", "6"), fr("1", "6x + 1")], 0, "(f ∘ g)(x) = 6x + 1.",
     "B: urutan tidak dibalik (" + INV + " ∘ g⁻¹ = (g ∘ f)⁻¹). C: (f ∘ g) sendiri. D: tanda salah. E: memakai 1/(f ∘ g)."),
    ("Diketahui f(x) = x + 5 dan (f ∘ g)(x) = 3x − 2. Fungsi g(x) adalah ....", ["3x − 7", "3x + 3", "3x − 2", "3x − 17", fr("3x − 2", "x + 5")], 0, "g(x) + 5 = 3x − 2.",
     "B: 5 ditambahkan, bukan dikurangkan. C: (f ∘ g) sendiri. D: menghitung (f ∘ g)(" + INV + "(x)). E: dibagi f."),
    ("Diketahui g(x) = x − 4 dan (f ∘ g)(x) = 2x + 3. Fungsi f(x) adalah ....", ["2x + 11", "2x − 5", "2x + 7", "2x + 3", fr("x + 5", "2")], 0, "g⁻¹(x) = x + 4; f(x) = 2(x + 4) + 3.",
     "B: memasukkan g, bukan g⁻¹. C: 4 ditambahkan di luar. D: (f ∘ g) sendiri. E: invers (f ∘ g) ditambah 4."),
    ("Diketahui " + INV + "(x) = " + fr("x + 3", "2") + ". Nilai f(4) adalah ....", ["5", fr("7", "2"), "11", fr("1", "2"), fr("2", "7")], 0, "f(x) = 2x − 3.",
     "B: menghitung " + INV + "(4). C: tanda salah (2x + 3). D: (4 − 3) : 2. E: memakai 1/" + INV + "(4)."),
    ("Tarif taksi B(x) = 3.500x + 8.000 rupiah untuk x km. Seorang penumpang membayar Rp57.000. Jarak yang ditempuh adalah ....", ["14 km", "≈ 16,29 km", "≈ 18,57 km", "15 km", "≈ 6,13 km"], 0,
     "(57.000 − 8.000) : 3.500 = 14.", "B: biaya tetap tidak dikurangkan. C: biaya tetap ditambahkan. D: model 8.000 + 3.500(x − 1). E: kedua tarif tertukar."),
    ("Fungsi f(x) = " + fr("ax + 5", "x − 1") + " sama dengan inversnya bila a = ....", ["1", "−1", "5", "−5", "0"], 0, INV + "(x) = (x + 5) : (x − a); sama dengan f bila a = 1. Cek ad − bc = −1 − 5 ≠ 0.",
     "B: a disamakan dengan d. C: a disamakan dengan b. D: a = −b. E: a = 0 memberi " + INV + "(x) = (x + 5) : x."),
]
UJI_URAIAN = [
    ("Diketahui f(x) = " + fr("3x − 4", "2") + ". Tentukan " + INV + "(x), tunjukkan bahwa f(" + INV + "(x)) = x, lalu hitung " + INV + "(10).", INV + "(x) = " + fr("2x + 4", "3") + "; " + INV + "(10) = 8",
     "2y = 3x − 4 → x = (2y + 4) : 3. f((2x + 4)/3) = (2x + 4 − 4) : 2 = x. (20 + 4) : 3 = 8."),
    ("Diketahui f(x) = " + fr("x + 4", "2x − 3") + ", x ≠ " + fr("3", "2") + ". Tentukan " + INV + "(x) beserta domainnya, lalu hitung " + INV + "(2) dan periksa jawabanmu.", INV + "(x) = " + fr("3x + 4", "2x − 1") + ", x ≠ ½; " + INV + "(2) = " + fr("10", "3"),
     "a = 1, d = −3. Cek: f(10/3) = (22/3) : (11/3) = 2."),
    ("Diketahui f(x) = x² + 2x − 3 dengan x ≥ −1. (a) Tulis f dalam bentuk (x − p)² + q. (b) Tentukan " + INV + "(x) dan domainnya. (c) Hitung " + INV + "(5). (d) Sketsa grafik f dan " + INV + " beserta garis y = x.",
     "(a) (x + 1)² − 4; (b) " + INV + "(x) = −1 + √(x + 4), x ≥ −4; (c) 2", "(c) −1 + √9 = 2; cek f(2) = 4 + 4 − 3 = 5. (d) Grafik " + INV + " adalah cermin grafik f terhadap y = x."),
    ("Diketahui f(x) = 2x − 1 dan g(x) = " + fr("x + 3", "x − 2") + ". (a) Tentukan (g ∘ f)(x). (b) Tentukan (g ∘ f)⁻¹(x) langsung dan dengan " + INV + " ∘ g⁻¹, lalu bandingkan. (c) Hitung (g ∘ f)⁻¹(4).",
     "(a) " + fr("2x + 2", "2x − 3") + "; (b) " + fr("3x + 2", "2x − 2") + ", x ≠ 1; (c) " + fr("7", "3"),
     "(b) g⁻¹(x) = (2x + 3) : (x − 1), " + INV + "(t) = (t + 1) : 2, dan ((2x + 3)/(x − 1) + 1) : 2 = (3x + 2) : (2x − 2). (c) 14 : 6; cek (g ∘ f)(7/3) = (20/3) : (5/3) = 4."),
    ("Pedagang menetapkan harga jual J(x) = 1,3x + 2.000 rupiah untuk barang bermodal x rupiah. Saat promo, harga jual dipotong 10%: P(y) = 0,9y. (a) Tentukan harga promo (P ∘ J)(x). (b) Tentukan (P ∘ J)⁻¹(x). (c) Pembeli membayar Rp118.800 saat promo; berapa modal barang itu? (d) Apakah pedagang masih untung?",
     "(a) 1,17x + 1.800; (b) " + fr("x − 1.800", "1,17") + "; (c) Rp100.000; (d) ya, untung Rp18.800",
     "(a) 0,9(1,3x + 2.000). (c) (118.800 − 1.800) : 1,17 = 117.000 : 1,17 = 100.000. (d) 118.800 − 100.000."),
]

META = dict(
    title="Modul Fungsi Invers", kick="Modul belajar Matematika · Fase F · Kelas XI", big="Fungsi Invers",
    subtitle="Syarat invers, rumus invers, grafik cermin terhadap y = x, dan invers fungsi komposisi",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat menjelaskan syarat sebuah fungsi mempunyai invers, menentukan rumus invers fungsi linear, rasional, kuadrat dengan domain terbatas, akar, dan eksponen; menggambar grafik fungsi invers sebagai pencerminan terhadap garis y = x; serta memakai invers fungsi komposisi untuk memecahkan masalah, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Fungsi dan inversnya: maju dan mundur</h2><table><tr><th></th><th>Fungsi f</th><th>Invers " + INV + "</th></tr>"
               "<tr><td>Rumus</td><td>f(x) = 2x + 1</td><td>" + INV + "(x) = (x − 1) : 2</td></tr>"
               "<tr><td>Langkah</td><td>kalikan 2, lalu tambah 1</td><td>kurangi 1, lalu bagi 2</td></tr>"
               "<tr><td>Contoh</td><td>3 → 7</td><td>7 → 3</td></tr></table>"
               "<p>Invers membalik <b>urutan dan jenis</b> operasi, sehingga hasil f kembali ke asalnya.</p>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit</b> tanpa kalkulator, dan uji setiap invers dengan memasukkan satu bilangan: f(" + INV + "(x)) harus kembali ke x.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Invers f ditulis " + INV + "; (f ∘ g)(x) = f(g(x)). Domain ditulis sebagai syarat, misalnya x ≠ 3 atau x ≥ 2. Desimal ditulis dengan koma, ribuan dengan titik (Rp4.000).",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>syarat invers, rumus invers, grafik, atau komposisi?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025 (specs/tka-templates/matematika.md). TKA Matematika 2025 memuat soal nilai invers fungsi dalam konteks.",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-MODEL, MAT-FUNGSI): mengenali, menghitung, bekerja mundur, memodelkan, atau menafsirkan fungsi. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Mengapa fungsi kuadrat perlu dibatasi domainnya sebelum dicari inversnya?", "Mengapa (f ∘ g)⁻¹ sama dengan g⁻¹ ∘ " + INV + " dan bukan " + INV + " ∘ g⁻¹?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Syarat invers</th><td>f bijektif (injektif dan surjektif); uji garis mendatar; batasi domain bila perlu</td></tr>"
        "<tr><th>Arti</th><td>f(a) = b ⇔ " + INV + "(b) = a; domain " + INV + " = range f</td></tr>"
        "<tr><th>Langkah</th><td>y = f(x) → nyatakan x dalam y → tulis " + INV + "(x); uji f(" + INV + "(x)) = x</td></tr>"
        "<tr><th>Linear</th><td>f(x) = ax + b → " + INV + "(x) = (x − b)/a</td></tr>"
        "<tr><th>Rasional</th><td>f(x) = (ax + b)/(cx + d) → " + INV + "(x) = (−dx + b)/(cx − a), x ≠ a/c</td></tr>"
        "<tr><th>Kuadrat</th><td>f(x) = (x − p)² + q, x ≥ p → " + INV + "(x) = p + √(x − q), x ≥ q</td></tr>"
        "<tr><th>Eksponen</th><td>f(x) = aˣ → " + INV + "(x) = ᵃlog x, x &gt; 0</td></tr>"
        "<tr><th>Grafik</th><td>cermin terhadap y = x; (a, b) ↔ (b, a); asimtot bertukar</td></tr>"
        "<tr><th>Komposisi</th><td>f ∘ " + INV + " = I; (f ∘ g)⁻¹ = g⁻¹ ∘ " + INV + "; f ∘ g = h → g = " + INV + " ∘ h, f = h ∘ g⁻¹</td></tr></table>"
        '<div class="fig">' + FIG_REF + "</div>"),
    jebakan5=[INV + "(x) adalah fungsi invers, bukan 1/f(x).", "Invers membalik urutan operasi: invers 4x + 8 adalah (x − 8)/4, bukan x/4 − 8.",
              "Pada invers fungsi rasional, a dan d ditukar dan diganti tandanya; b dan c tetap.", "Fungsi kuadrat perlu domain terbatas, dan tanda akar mengikuti domain itu.",
              "(f ∘ g)⁻¹ = g⁻¹ ∘ " + INV + ": urutannya dibalik."],
    guru=["Modul ini mengikuti simpul FUN-02 (Komposisi dan invers fungsi) pada peta Matematika, yang ditempatkan di kelas XI. Urutan bab dapat berbeda antarsekolah.",
          "Komposisi fungsi hanya diulang sebagai prasyarat (Kotak Ingat D) dan dipakai di Subbab 5; modul ini tidak mengajarkan komposisi dari awal.",
          "Rumus cepat invers fungsi rasional dan fungsi kuadrat sengaja diturunkan dari langkah tukar-selesaikan; siswa sebaiknya tetap bisa menurunkannya sendiri.",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


def check():
    def lin(a, b):
        return lambda x: a * x + b

    def rat(a, b, c, d):
        return lambda x: F(a * x + b, 1) / (c * x + d)

    def rat_inv(a, b, c, d):
        assert a * d - b * c != 0
        return (-d, b, c, -a)

    def inverse_ok(f, g, xs):
        """g is the inverse of f on the sample xs: g(f(x)) = x."""
        return all(g(f(F(x))) == x for x in xs)

    def inv_close(f, g, xs):
        for x in xs:
            close(g(f(x)), x)
        return True

    xs = [-3, -1, 0, 2, 5, 7]
    # prasyarat
    assert 3 * 4 - 5 == 7 and 3 * -1 - 5 == -8 and F(1 - 7, 2) == -3
    assert all(5 * F(x - 2, 5) + 2 == x for x in xs)
    assert all(F(2 * F(x + 1, x - 2) + 1) / (F(x + 1, x - 2) - 1) == x for x in xs if x != 2)
    assert all(x * x - 6 * x + 11 == (x - 3) ** 2 + 2 for x in xs)
    assert 2 * 2 ** 2 + 1 == 9 and all(2 * (x + 3) == 2 * x + 6 for x in xs) and 2 ** 5 == 32 and F(3) ** -2 == F(1, 9)
    # subbab 1
    f = {1: 4, 2: 6, 3: 8, 4: 10}
    assert sorted(f.values()) == [4, 6, 8, 10] and {v: k for k, v in f.items()}[8] == 3
    g = lambda x: x * x - 4 * x  # noqa: E731
    assert g(1) == g(3) == -3 and g(2) == -4 and all(g(x + 1) > g(x) for x in range(2, 8))
    assert [2 * x + 1 for x in range(4)] == [1, 3, 5, 7]
    assert {v: k for k, v in {1: 3, 2: 5, 3: 7}.items()} == {3: 1, 5: 2, 7: 3}
    assert F(8, 2) == 4 and F(1, 2 * 8) == F(1, 16)
    assert sorted({x * x for x in range(-2, 3)}) == [0, 1, 4]
    tab = {x: x * x + 1 for x in range(1, 6)}
    assert list(tab.values()) == [2, 5, 10, 17, 26] and {v: k for k, v in tab.items()}[17] + {v: k for k, v in tab.items()}[5] == 6
    assert all((x - 3) ** 2 + 1 >= 1 for x in range(3, 9)) and (3 - 3) ** 2 + 1 == 1
    assert all(x * x + 6 * x + 5 == (x + 3) ** 2 - 4 for x in xs) and (-3 + 3) ** 2 - 4 == -4
    assert [x ** 3 - x for x in (-1, 0, 1)] == [0, 0, 0]
    # subbab 2
    assert inverse_ok(lin(3, -6), lambda x: (x + 6) / 3, xs) and 3 * 4 - 6 == 6 and F(6 + 6, 3) == 4
    h = lambda x: F(5, 4) * x + 2000  # noqa: E731
    assert inverse_ok(h, lambda x: F(4, 5) * (x - 2000), xs) and F(4, 5) * (27000 - 2000) == 20000 and h(20000) == 27000
    fb = lambda x: F(2 * x - 5, 3)  # noqa: E731
    assert inverse_ok(fb, lambda x: (3 * x + 5) / 2, xs) and fb(4) == 1
    assert inverse_ok(lin(1, 7), lambda x: x - 7, xs) and inverse_ok(lin(4, 0), lambda x: x / 4, xs) and inverse_ok(lin(2, -8), lambda x: (x + 8) / 2, xs)
    assert inverse_ok(lin(-1, 5), lin(-1, 5), xs) and F(10 - 1, 3) == 3
    assert inverse_ok(lambda x: (3 * x + 4) / 5, lambda x: (5 * x - 4) / 3, xs) and inverse_ok(lin(F(-1, 2), 3), lin(-2, 6), xs)
    assert F(8 - 2, 3) == 2
    fc = lambda c: F(9, 5) * c + 32  # noqa: E731
    assert inverse_ok(fc, lambda x: (x - 32) / F(9, 5), xs) and (104 - 32) / F(9, 5) == 40
    assert inverse_ok(lin(F(1, 2), 3), lin(2, -6), xs)
    assert F(11 - 5, 3 - 1) == 3 and 5 - 3 == 2 and F(20 - 2, 3) == 6
    assert inverse_ok(lin(4000, 6000), lambda x: (x - 6000) / 4000, xs) and F(50000 - 6000, 4000) == 11
    # subbab 3
    assert rat_inv(2, 1, 1, -3) == (3, 1, 1, -2) and rat(2, 1, 1, -3)(4) == 9 and rat(3, 1, 1, -2)(9) == 4
    assert inverse_ok(rat(2, 1, 1, -3), rat(3, 1, 1, -2), [0, 1, 5, 7])
    q = lambda x: x * x - 4 * x + 7  # noqa: E731
    assert all(q(x) == (x - 2) ** 2 + 3 for x in xs) and q(5) == 12 and 2 + math.isqrt(12 - 3) == 5
    assert inv_close(q, lambda x: 2 + math.sqrt(x - 3), [2, 2.5, 4, 9.3])
    assert rat_inv(1, 5, 2, -1) == (1, 5, 2, -1) and inverse_ok(rat(1, 5, 2, -1), rat(1, 5, 2, -1), [0, 2, 3, -4])
    assert inv_close(lambda x: x ** 3, lambda x: math.copysign(abs(x) ** (1 / 3), x), [-8, -1, 0, 2, 27])
    assert inv_close(math.sqrt, lambda x: x * x, [0, 1, 4, 7])
    assert rat_inv(1, 2, 1, -4) == (4, 2, 1, -1) and inverse_ok(rat(1, 2, 1, -4), rat(4, 2, 1, -1), [0, 2, 5, 7])
    assert inverse_ok(rat(0, 3, 1, 0), rat(0, 3, 1, 0), [1, 2, -3]) and rat(2, 0, 1, 3)(3) == 1
    assert rat_inv(3, -2, 2, 1) == (-1, -2, 2, -3) and inverse_ok(rat(3, -2, 2, 1), rat(1, 2, -2, 3), [0, 1, 2, 5])
    assert inv_close(lambda x: x * x + 2, lambda x: math.sqrt(x - 2), [0, 1, 3.5])
    assert inv_close(lambda x: (x + 1) ** 2, lambda x: -1 - math.sqrt(x), [-1, -2, -4.5])
    assert inv_close(lambda x: math.sqrt(2 * x - 4), lambda x: (x * x + 4) / 2, [2, 3, 10])
    a = F(5, 4)
    assert (4 * a + 1) / (4 - 2) == 3
    assert rat_inv(2, 3, 1, -2) == (2, 3, 1, -2) and 2 * -2 - 3 * 1 == -7
    assert all(x * x - 6 * x + 5 == (x - 3) ** 2 - 4 for x in xs) and 3 + math.isqrt(12 + 4) == 7 and 49 - 42 + 5 == 12
    assert inv_close(lambda x: x * x - 6 * x + 5, lambda x: 3 + math.sqrt(x + 4), [3, 4, 8])
    # subbab 4
    assert inverse_ok(lin(2, -2), lambda x: (x + 2) / 2, xs) and [2 * x - 2 for x in (0, 1, 3)] == [-2, 0, 4] and F(-2 + 2, 2) == 0 and F(4 + 2, 2) == 3 and 2 * 2 - 2 == 2
    assert [2 ** x for x in (0, 1, 2)] == [1, 2, 4] and [math.log2(x) for x in (1, 2, 4, 8)] == [0, 1, 2, 3] and math.log2(0.5) == -1
    assert 3 * 2 - 4 == 2 and F(2 + 4, 3) == 2 and inverse_ok(lin(3, -4), lambda x: (x + 4) / 3, xs)
    assert [2 * x + 1 for x in (0, 1, 2)] == [1, 3, 5]
    assert inverse_ok(lin(F(1, 2), 1), lin(2, -2), xs) and [2 * x - 2 for x in (0, 1, 2, 3)] == [-2, 0, 2, 4] and [F(x, 2) + 1 for x in (-2, 0, 2, 4)] == [0, 1, 2, 3]
    assert 4 * 3 - 9 == 3 and rat_inv(2, 1, 1, -3) == (3, 1, 1, -2)
    assert math.log2(16) == 4 and math.log2(0.25) == -2
    assert 2 * 2 - 2 == 2 and (-1) ** 2 - 2 == -1 and all((x - 2) * (x + 1) == x * x - 2 - x for x in xs)
    assert inverse_ok(lin(-1, 3), lin(-1, 3), xs)
    fl = lin(2, 2)
    assert fl(1) == 4 and fl(0) == 2 and F(10 - 2, 2) == 4
    # subbab 5
    assert inverse_ok(lin(5, -2), lambda x: (x + 2) / 5, xs)
    assert inverse_ok(lin(2, 4), lambda x: (x - 4) / 2, xs) and inverse_ok(lin(3, 2), lambda x: (x - 2) / 3, xs)
    assert 3 ** 2 == 9 and close(2 ** math.log2(5), 5) is None
    assert all(2 * (x - 3) + 1 == 2 * x - 5 for x in xs) and all(F(x - 1, 2) + 3 == F(x + 5, 2) for x in xs)
    assert all(3 * (2 * x + 2) - 1 == 6 * x + 5 for x in xs) and all(F(6 * x + 5 + 1, 3) == 2 * x + 2 for x in xs)
    assert all(3 * (x + 2) - 2 == 3 * x + 4 for x in xs)
    assert all(2 * (2 * x + 4) - 3 == 4 * x + 5 for x in xs) and all(3 * (2 * x - 1) + 4 == 6 * x + 1 for x in xs)
    gf = lambda x: rat(1, 2, 1, -3)(x - 1)  # noqa: E731
    assert all(gf(x) == rat(1, 1, 1, -4)(x) for x in [0, 2, 6]) and rat_inv(1, 1, 1, -4) == (4, 1, 1, -1)
    assert all(rat(3, 2, 1, -1)(x) + 1 == rat(4, 1, 1, -1)(x) for x in [0, 2, 3]) and rat_inv(1, 2, 1, -3) == (3, 2, 1, -1)
    fog = lambda x: 3 * F(x - 1, 2) + 2  # noqa: E731
    assert fog(5) == 8 and F(8 - 2, 3) == 2 and 2 * 2 + 1 == 5
    assert (2 * 4 + 1) - 3 == 6 and F(6 + 3 - 1, 2) == 4
    assert F(88, 100) * 150000 == 132000 and F(8, 10) * F(11, 10) == F(88, 100)
    fg = lambda x: rat(1, 1, 1, -2)(2 * x - 1)  # noqa: E731
    assert all(fg(x) == rat(2, 0, 2, -3)(x) for x in [0, 1, 3]) and rat_inv(2, 0, 2, -3) == (3, 0, 2, -2)
    assert all((rat(2, 1, 1, -1)(x) + 1) / 2 == rat(3, 0, 2, -2)(x) for x in [0, 2, 3])
    # campuran
    assert inverse_ok(lin(-3, 7), lambda x: (7 - x) / 3, xs)
    assert rat_inv(1, -5, 1, 2) == (-2, -5, 1, -1) and inverse_ok(rat(1, -5, 1, 2), rat(2, 5, -1, 1), [0, 2, 3, 5])
    assert inv_close(lambda x: x * x + 4 * x, lambda x: -2 + math.sqrt(x + 4), [-2, 0, 1.5])
    assert all(2 * (x + 3) - 5 == 2 * x + 1 for x in xs) and inverse_ok(lin(2, 1), lambda x: (x - 1) / 2, xs)
    assert rat_inv(1, 1, 1, -3) == (3, 1, 1, -1) and inverse_ok(rat(1, 1, 1, -3), rat(3, 1, 1, -1), [0, 2, 5])
    assert close(4 ** 2.5, 32) is None and 2 * F(5, 2) == 5
    fab = rat(-1, 5, 1, 1)
    assert fab(0) == 5 and fab(2) == 1 and -1 * 1 - 5 * 1 != 0
    assert lin(-3, 4)(1) == 1 and lin(-3, 4)(-2) == 10
    assert F(61000 - 5000, 8000) == 7 and F(50000 - 5000, 8000) == F(45, 8) and 8000 * 5 + 5000 <= 50000 < 8000 * 6 + 5000
    # TKA
    assert [3 * x - 3 for x in (0, 1, 2)] == [-3, 0, 3]
    assert rat_inv(3, 2, 1, -4) == (4, 2, 1, -3) and inverse_ok(rat(3, 2, 1, -4), rat(4, 2, 1, -3), [0, 1, 5, 6])
    assert not inverse_ok(rat(3, 2, 1, -4), rat(-4, 2, 1, -3), [0, 1, 5]) and not inverse_ok(rat(3, 2, 1, -4), rat(4, -2, 1, -3), [0, 1, 5])
    a = F(8, 2)
    assert (2 * a - 1) / 7 == 1 and (11 - 1) / F(5) == 2 and F(6, 2) == 3 and F(7, 2) * 2 / 7 == 1
    hj = lambda x: F(5, 4) * x + 4000  # noqa: E731
    assert hj(40000) == 54000 and 54000 / F(5, 4) - 4000 == 39200 and hj(54000) == 71500 and (54000 + 4000) / F(5, 4) == 46400
    assert (212 - 32) / F(9, 5) == 100 and (50 - 32) / F(9, 5) == 10 and F(-32, F(4, 5)) == -40 and fc(-40) == -40
    p = lambda x: x * x - 2 * x + 3  # noqa: E731
    assert all(p(x) == (x - 1) ** 2 + 2 for x in xs) and p(4) == 11 and p(0) == 3 and 1 + math.isqrt(3 - 2) == 2
    assert 2 * 3 + 1 == 7 and lin(2, 1)(5) == 11
    Bk = lambda n: 12000 * n + 300000  # noqa: E731
    assert Bk(95) == 1440000 <= 1450000 < Bk(96) == 1452000 and 1450000 // 12000 == 120 and math.ceil(1450000 / 12000) == 121 and (1450000 + 300000) // 12000 == 145
    assert all(2 * (3 * x - 2) + 5 == 6 * x + 1 for x in xs) and F(9 - 5, 2) == 2 and F(9 - 1, 6) == F(4, 3) and 3 * F(4, 3) - 2 == 2 and 2 * 9 + 5 == 23 and F(9 + 5, 2) == 7
    # uji
    assert inverse_ok(lin(4, 8), lambda x: (x - 8) / 4, xs) and F(6 - 10, 2) == -2 and 6 - 2 * 10 == -14 and F(10 + 6, 2) == 8
    assert rat_inv(2, -1, 1, 3) == (-3, -1, 1, -2) and inverse_ok(rat(2, -1, 1, 3), rat(-3, -1, 1, -2), [0, 1, 4])
    assert rat_inv(4, 1, 2, -6) == (6, 1, 2, -4) and F(4, 2) == 2
    pp = lambda x: x * x - 8 * x + 10  # noqa: E731
    assert all(pp(x) == (x - 4) ** 2 - 6 for x in xs) and inv_close(pp, lambda x: 4 + math.sqrt(x + 6), [4, 5, 9])
    assert inv_close(lambda x: math.log(x - 1, 3), lambda x: 3 ** x + 1, [2, 4, 10])
    assert 5 * 2 - 8 == 2 and F(8, 5) * 5 - 8 == 0 and F(-8, 4) == -2
    assert all(2 * 3 * x + 1 == 6 * x + 1 for x in xs) and inverse_ok(lin(6, 1), lambda x: (x - 1) / 6, xs) and inverse_ok(lin(6, 3), lambda x: (x - 3) / 6, xs)
    assert all((3 * x - 7) + 5 == 3 * x - 2 for x in xs) and all(3 * (x - 5) - 2 == 3 * x - 17 for x in xs)
    assert all(2 * ((x - 4) + 4) + 3 == 2 * (x - 4) + 11 for x in xs) and all(2 * (x - 4) + 3 == 2 * x - 5 for x in xs) and all(F(x - 3, 2) + 4 == F(x + 5, 2) for x in xs)
    assert inverse_ok(lin(2, -3), lambda x: (x + 3) / 2, xs) and lin(2, -3)(4) == 5 and F(4 + 3, 2) == F(7, 2) and F(4 - 3, 2) == F(1, 2)
    assert F(57000 - 8000, 3500) == 14 and close(57000 / 3500, 16.29, 0.005) is None and close(65000 / 3500, 18.57, 0.005) is None and F(49000, 3500) + 1 == 15 and close(49000 / 8000, 6.13, 0.005) is None
    assert rat_inv(1, 5, 1, -1) == (1, 5, 1, -1) and 1 * -1 - 5 * 1 == -6
    # uraian
    assert inverse_ok(lambda x: F(3 * x - 4, 2), lambda x: F(2 * x + 4, 3), xs) and F(24, 3) == 8
    assert rat_inv(1, 4, 2, -3) == (3, 4, 2, -1) and rat(3, 4, 2, -1)(2) == F(10, 3) and rat(1, 4, 2, -3)(F(10, 3)) == 2
    assert all(x * x + 2 * x - 3 == (x + 1) ** 2 - 4 for x in xs) and -1 + math.isqrt(5 + 4) == 2 and 4 + 4 - 3 == 5
    gof = lambda x: rat(1, 3, 1, -2)(2 * x - 1)  # noqa: E731
    assert all(gof(x) == rat(2, 2, 2, -3)(x) for x in [0, 1, 3]) and rat_inv(2, 2, 2, -3) == (3, 2, 2, -2)
    assert all((rat(2, 3, 1, -1)(x) + 1) / 2 == rat(3, 2, 2, -2)(x) for x in [0, 2, 3]) and rat(3, 2, 2, -2)(4) == F(7, 3) and gof(F(7, 3)) == 4
    PJ = lambda x: F(9, 10) * (F(13, 10) * x + 2000)  # noqa: E731
    assert all(PJ(x) == F(117, 100) * x + 1800 for x in xs) and PJ(100000) == 118800 and (118800 - 1800) / F(117, 100) == 100000
    return True
