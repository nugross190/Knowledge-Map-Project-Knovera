"""Content of the printable module "Eksponen dan Logaritma" (Matematika kelas X).

Logarithm notation follows Indonesian textbooks: ²log 8 = 3, and log x means base 10.
Every numeric answer is re-derived in check() with exact arithmetic where possible.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import plane  # noqa: E402
from kit import n, fr, Q, close  # noqa: E402

BLUE, RED, GREEN = "#1f3a68", "#c0502a", "#2e6b32"
L2, L3 = 0.301, 0.477          # log 2 and log 3 as given in the items


def lg(x, b=10):
    return math.log(x) / math.log(b)


PRASYARAT = [
    ("P1", "Hitung 2⁵ dan 3⁴.", "32 dan 81", "2 · 2 · 2 · 2 · 2 = 32; 3 · 3 · 3 · 3 = 81."),
    ("P2", "Hitung (−3)⁴ dan −3⁴.", "81 dan −81", "Pada −3⁴ yang dipangkatkan hanya 3."),
    ("P3", "Tuliskan 72 sebagai perkalian faktor prima.", "2³ · 3²", "72 = 8 · 9."),
    ("P4", "Sederhanakan √(16 · 9).", "12", "√144."),
    ("P5", "Hitung ⅔ · ¾ dan ⅔ : ¾.", "½ dan 8/9", "Membagi = mengalikan dengan kebalikan."),
    ("P6", "Naik 10% berarti dikali berapa? Turun 20%?", "1,1 dan 0,8", "1 + 0,1 dan 1 − 0,2."),
    ("P7", "Selesaikan 2x + 3 = 11.", "x = 4", "2x = 8."),
    ("P8", "Selesaikan x² − 5x + 6 = 0.", "x = 2 atau x = 3", "(x − 2)(x − 3) = 0."),
]

INGAT = [
    ("A", "Arti pangkat", "P1, P2", "Subbab 1–3", ["aⁿ = a · a · … · a (n faktor).", "Tanda kurung menentukan apa yang dipangkatkan: (−3)² = 9, −3² = −9."]),
    ("B", "Faktorisasi prima dan akar", "P3, P4", "Subbab 1–2", ["Tulis bilangan sebagai hasil kali bilangan prima berpangkat: 72 = 2³ · 3².", "√(ab) = √a · √b untuk a, b ≥ 0."]),
    ("C", "Pecahan dan persen", "P5, P6", "Subbab 1, 3, 5", ["Naik p% → dikali (1 + p/100); turun p% → dikali (1 − p/100)."]),
    ("D", "Persamaan linear dan kuadrat", "P7, P8", "Subbab 3, 5", ["Faktorkan persamaan kuadrat bila bisa; periksa setiap akar terhadap syarat soal."]),
]

SUB = []

# ================================================================== Subbab 1
SUB.append(dict(
    title="Sifat Bilangan Berpangkat",
    tujuan="Memakai sifat-sifat pangkat bulat positif, nol, dan negatif untuk menyederhanakan bentuk aljabar dan menulis notasi ilmiah.",
    konsep=[
        "aⁿ berarti a dikalikan dengan dirinya sendiri sebanyak n kali; a disebut <b>basis</b> dan n <b>pangkat</b> (eksponen).",
        "Sifat-sifat pangkat muncul dari menghitung banyaknya faktor. Misalnya 2³ · 2⁴ = (2·2·2)(2·2·2·2) = 2⁷: pangkatnya dijumlahkan.",
        "Supaya sifat a<sup>m</sup> : a<sup>n</sup> = a<sup>m−n</sup> tetap berlaku, didefinisikan <b>a⁰ = 1</b> dan <b>a⁻ⁿ = 1/aⁿ</b> (a ≠ 0). Pangkat negatif tidak membuat hasilnya negatif.",
        "<b>Notasi ilmiah</b> menulis bilangan sangat besar atau sangat kecil sebagai a × 10ⁿ dengan 1 ≤ a &lt; 10.",
    ],
    rumus=["a<sup>m</sup> · a<sup>n</sup> = a<sup>m+n</sup>; a<sup>m</sup> : a<sup>n</sup> = a<sup>m−n</sup>", "(a<sup>m</sup>)<sup>n</sup> = a<sup>mn</sup>; (ab)<sup>n</sup> = a<sup>n</sup>b<sup>n</sup>; (a/b)<sup>n</sup> = a<sup>n</sup>/b<sup>n</sup>",
           "a⁰ = 1 dan a⁻ⁿ = " + fr("1", "aⁿ") + " (a ≠ 0)", "Notasi ilmiah: a × 10ⁿ, 1 ≤ a &lt; 10"],
    contoh=[
        ("Menyederhanakan", "Sederhanakan " + fr("2³ · 2⁵", "2⁴") + " dan " + fr("(x²y³)²", "x³y") + ".", None,
         ["2³ · 2⁵ : 2⁴ = 2<sup>3+5−4</sup> = 2⁴ = 16.", "(x²y³)² = x⁴y⁶; dibagi x³y menjadi x<sup>4−3</sup>y<sup>6−1</sup> = xy⁵."], "16 dan xy⁵"),
        ("Notasi ilmiah", "Tulis 0,00045 dalam notasi ilmiah, lalu hitung (3 × 10⁸) · (2 × 10⁻³).", None,
         ["0,00045 = 4,5 × 10⁻⁴.", "(3 · 2) × 10<sup>8+(−3)</sup> = 6 × 10⁵."], "4,5 × 10⁻⁴; 6 × 10⁵"),
    ],
    bertahap=dict(
        soal="Sederhanakan (a³b⁻²)² · a⁻⁴b⁵ menjadi bentuk tanpa pangkat negatif.",
        langkah=["(a³b⁻²)² = a<sup>____</sup>b<sup>____</sup>.", "Dikali a⁻⁴b⁵: a<sup>6 + (−4)</sup> b<sup>−4 + 5</sup> = a<sup>____</sup>b<sup>____</sup>."],
        cek="Pada langkah pertama, pangkat di dalam kurung",
        opsi=["(a) dikalikan dengan 2", "(b) ditambah 2"],
        kunci="a⁶b⁻⁴; a²b. Alasan: (a).",
    ),
    jebakan=["(−3)² = 9 tetapi −3² = −9.", "a<sup>m</sup> + a<sup>n</sup> ≠ a<sup>m+n</sup>; sifat pangkat berlaku untuk perkalian, bukan penjumlahan.", "2⁻³ = 1/8, bukan −8."],
    latihan=[
        Q(1, "Hitung 2³ · 2⁴.", "128", "2⁷."), Q(1, "Hitung 5⁶ : 5⁴.", "25", "5²."), Q(1, "Hitung (3²)³.", "729", "3⁶."),
        Q(1, "Berapa 7⁰?", "1", "a⁰ = 1."), Q(1, "Tulis 2⁻³ sebagai pecahan.", "1/8", "1/2³."),
        Q(2, "Sederhanakan " + fr("(x³y²)³", "x⁴y⁵") + ".", "x⁵y", "x⁹y⁶ : x⁴y⁵."),
        Q(2, "Hitung " + fr("4³ · 8²", "2¹⁰") + ".", "4", "2⁶ · 2⁶ : 2¹⁰ = 2²."),
        Q(2, "Hitung (⅔)⁻².", "9/4", "(3/2)²."),
        Q(2, "Hitung (6 × 10⁴) · (5 × 10⁻⁷) dan tulis dalam notasi ilmiah.", "3 × 10⁻²", "30 × 10⁻³."),
        Q(3, "Sederhanakan " + fr("2<sup>n+2</sup> − 2<sup>n</sup>", "2<sup>n</sup>") + ".", "3", "2<sup>n</sup>(4 − 1) : 2<sup>n</sup>."),
        Q(3, "Mana yang lebih besar, 3²⁰ atau 2³⁰? Jelaskan tanpa kalkulator.", "3²⁰", "3²⁰ = 9¹⁰ dan 2³⁰ = 8¹⁰; 9 &gt; 8."),
        Q(3, "Cahaya merambat 3 × 10⁸ m/s. Satu tahun kira-kira 3,15 × 10⁷ s. Berapa meter jarak satu tahun cahaya?", "≈ 9,45 × 10¹⁵ m", "3 · 3,15 = 9,45; 10<sup>8+7</sup>."),
    ],
))

# ================================================================== Subbab 2
SUB.append(dict(
    title="Bentuk Akar dan Pangkat Pecahan",
    tujuan="Menghubungkan bentuk akar dengan pangkat pecahan, menyederhanakan dan menjumlahkan bentuk akar, serta merasionalkan penyebut.",
    konsep=[
        "Pangkat pecahan adalah bentuk akar: a<sup>1/n</sup> = ⁿ√a dan a<sup>m/n</sup> = ⁿ√(aᵐ). Semua sifat pangkat tetap berlaku.",
        "Bentuk akar disederhanakan dengan mengeluarkan faktor kuadrat sempurna: √72 = √(36 · 2) = 6√2. Hanya akar <b>sejenis</b> (bilangan di bawah akarnya sama) yang dapat dijumlahkan.",
        "<b>Merasionalkan penyebut</b> berarti menghilangkan akar dari penyebut dengan mengalikan pembilang dan penyebut dengan bentuk yang sama: √b, atau sekawannya (√b + √c dengan √b − √c).",
    ],
    rumus=["a<sup>1/n</sup> = ⁿ√a; a<sup>m/n</sup> = ⁿ√(aᵐ)", "√(ab) = √a · √b; p√a + q√a = (p + q)√a",
           fr("a", "√b") + " = " + fr("a√b", "b") + "; " + fr("a", "√b − √c") + " = " + fr("a(√b + √c)", "b − c")],
    contoh=[
        ("Akar sejenis", "Sederhanakan √50 + √18 − √8.", None, ["√50 = 5√2; √18 = 3√2; √8 = 2√2.", "(5 + 3 − 2)√2 = 6√2."], "6√2"),
        ("Merasionalkan", "Hitung 8<sup>2/3</sup>, lalu rasionalkan " + fr("6", "3 − √3") + ".", None,
         ["8<sup>2/3</sup> = (∛8)² = 2² = 4.", "Kalikan dengan " + fr("3 + √3", "3 + √3") + ": " + fr("6(3 + √3)", "9 − 3") + " = 3 + √3."], "4; 3 + √3"),
    ],
    bertahap=dict(
        soal="Rasionalkan penyebut " + fr("10", "√7 − √2") + ".",
        langkah=["Kalikan pembilang dan penyebut dengan ____.", "Penyebut: (√7 − √2)(√7 + √2) = 7 − ____ = ____.", "Hasil: " + fr("10(√7 + √2)", "____") + " = ____."],
        cek="Bentuk √7 + √2 dipilih karena",
        opsi=["(a) (a − b)(a + b) = a² − b² menghilangkan akar", "(b) √7 + √2 = √9 = 3"],
        kunci="√7 + √2; 7 − 2 = 5; 2(√7 + √2). Alasan: (a).",
    ),
    jebakan=["√(a + b) ≠ √a + √b; misalnya √(9 + 16) = 5, bukan 7.", "√2 + √3 tidak dapat digabung menjadi √5.", "√(x²) = |x|, bukan selalu x."],
    latihan=[
        Q(1, "Sederhanakan √48.", "4√3", "√(16 · 3)."), Q(1, "Hitung 27<sup>1/3</sup>.", "3", "∛27."), Q(1, "Hitung 16<sup>3/4</sup>.", "8", "(⁴√16)³ = 2³."),
        Q(1, "Hitung 3√2 · √8.", "12", "3√16."), Q(1, "Sederhanakan 2√3 + 5√3.", "7√3", "Akar sejenis."),
        Q(2, "Sederhanakan √75 − √27 + √12.", "4√3", "5√3 − 3√3 + 2√3."),
        Q(2, "Rasionalkan " + fr("4", "√2") + ".", "2√2", "4√2 : 2."),
        Q(2, "Rasionalkan " + fr("2", "√5 − 1") + ".", fr("√5 + 1", "2"), "2(√5 + 1) : (5 − 1)."),
        Q(2, "Jabarkan (√3 + 1)².", "4 + 2√3", "3 + 2√3 + 1."),
        Q(3, "Hitung (√5 + √3)(√5 − √3) dan jelaskan mengapa hasilnya bilangan bulat.", "2", "Bentuk (a + b)(a − b) = a² − b² = 5 − 3."),
        Q(3, "Luas sebuah persegi 50 cm². Tentukan panjang sisi dan panjang diagonalnya dalam bentuk akar paling sederhana.", "sisi 5√2 cm; diagonal 10 cm", "Sisi √50 = 5√2; diagonal = sisi · √2 = 5 · 2."),
        Q(3, "Tulis " + fr("√8 · ∛4", "2") + " sebagai satu bilangan berpangkat dengan basis 2.", "2<sup>7/6</sup>", "2<sup>3/2</sup> · 2<sup>2/3</sup> : 2¹ = 2<sup>3/2 + 2/3 − 1</sup> = 2<sup>7/6</sup>."),
    ],
))

# ================================================================== Subbab 3
EXP_FIG = plane((-3, 3, 1), (0, 8, 1), curves=[(lambda x: 2 ** x, -3, 3, BLUE, "y = 2ˣ"), (lambda x: 0.5 ** x, -3, 3, RED, "y = (½)ˣ")], points=[(0, 1, "(0, 1)")])
K_FIG = plane((-1, 4, 1), (0, 30, 5), curves=[(lambda x: 3 * 2 ** x, -1, 3.3, BLUE, "")], points=[(0, 3, "(0, 3)"), (2, 12, "(2, 12)")])
DECAY_FIG = plane((0, 5, 1), (0, 900, 100), curves=[(lambda t: 800 * 0.5 ** t, 0, 5, RED, "")], points=[(0, 800, "(0, 800)"), (1, 400, "(1, 400)")], xlabel="t (hari)", ylabel="m (mg)")
SUB.append(dict(
    title="Fungsi dan Persamaan Eksponen",
    tujuan="Menggambar dan menafsirkan fungsi eksponen, menyelesaikan persamaan eksponen sederhana, serta memodelkan pertumbuhan dan peluruhan.",
    konsep=[
        "<b>Fungsi eksponen</b> f(x) = aˣ dengan a &gt; 0 dan a ≠ 1. Grafiknya selalu melalui (0, 1), selalu di atas sumbu x, dan mendekati sumbu x tanpa menyentuhnya (asimtot y = 0).",
        "Bila a &gt; 1, grafik naik (pertumbuhan); bila 0 &lt; a &lt; 1, grafik turun (peluruhan). Grafik y = aˣ dan y = (1/a)ˣ simetris terhadap sumbu y.",
        "<b>Persamaan eksponen</b>: samakan basisnya, lalu samakan pangkatnya: a<sup>f(x)</sup> = a<sup>g(x)</sup> ⟹ f(x) = g(x).",
        "Pertumbuhan atau peluruhan dengan persentase tetap per periode adalah barisan geometri: N(t) = N₀(1 + r)ᵗ atau N(t) = N₀(1 − r)ᵗ. Peluruhan dengan waktu paruh T: N(t) = N₀(½)<sup>t/T</sup>.",
    ],
    rumus=["f(x) = aˣ, a &gt; 0, a ≠ 1; f(0) = 1", "a<sup>f(x)</sup> = a<sup>g(x)</sup> ⟹ f(x) = g(x)", "Pertumbuhan: N = N₀(1 + r)ᵗ; peluruhan: N = N₀(1 − r)ᵗ", "Waktu paruh T: N = N₀ · (½)<sup>t/T</sup>"],
    contoh=[
        ("Dua grafik eksponen", "Gambarkan y = 2ˣ dan y = (½)ˣ untuk −3 ≤ x ≤ 3, lalu bandingkan.", EXP_FIG,
         ["Keduanya melalui (0, 1) dan tidak pernah menyentuh sumbu x.", "y = 2ˣ naik; y = (½)ˣ turun; keduanya simetris terhadap sumbu y."], "lihat grafik"),
        ("Persamaan dan pertumbuhan", "Selesaikan 2<sup>x+1</sup> = 32 dan 9ˣ = 27. Lalu: 500 bakteri membelah menjadi dua setiap 20 menit; berapa banyaknya setelah 2 jam?", None,
         ["2<sup>x+1</sup> = 2⁵ → x = 4.", "3<sup>2x</sup> = 3³ → x = 3/2.", "2 jam = 6 kali pembelahan: 500 · 2⁶ = 32.000."], "x = 4; x = 3/2; 32.000 bakteri"),
    ],
    bertahap=dict(
        soal="Selesaikan 4<sup>x−1</sup> = 8<sup>x−2</sup>.",
        langkah=["Tulis dengan basis 2: 2<sup>____(x−1)</sup> = 2<sup>____(x−2)</sup>.", "2x − 2 = 3x − ____.", "x = ____."],
        cek="Persamaan ini diselesaikan dengan menyamakan basis karena",
        opsi=["(a) bila basisnya sama, pangkatnya harus sama", "(b) 4 dan 8 sama-sama genap"],
        kunci="2(x − 1) dan 3(x − 2); 2x − 2 = 3x − 6; x = 4. Alasan: (a).",
    ),
    jebakan=["Grafik y = aˣ tidak pernah menyentuh sumbu x: aˣ &gt; 0 untuk setiap x.", "Naik 10% per tahun berarti dikali 1,1 tiap tahun, bukan ditambah 10% dari nilai awal.", "2ˣ = 0 tidak mempunyai penyelesaian."],
    latihan=[
        Q(1, "Selesaikan 3ˣ = 81.", "x = 4", "3⁴."), Q(1, "Selesaikan 5<sup>x−2</sup> = 1.", "x = 2", "5⁰ = 1."), Q(1, "Jika f(x) = 2ˣ, berapa f(3) dan f(−1)?", "8 dan ½", "2³; 2⁻¹."),
        Q(1, "Titik mana yang pasti dilalui grafik y = 3ˣ?", "(0, 1)", "3⁰ = 1."), Q(1, "Apakah y = (0,5)ˣ naik atau turun?", "turun", "Basis antara 0 dan 1."),
        Q(2, "Selesaikan 2<sup>2x</sup> = 1/16.", "x = −2", "2<sup>2x</sup> = 2⁻⁴."),
        Q(2, "Selesaikan 25<sup>x+1</sup> = 125.", "x = ½", "5<sup>2x+2</sup> = 5³."),
        Q(2, "Penduduk sebuah desa 1.000 jiwa dan bertambah 10% per tahun. Berapa penduduknya setelah 2 tahun?", "1.210 jiwa", "1.000 · 1,1²."),
        Q(2, "Grafik y = k · 2ˣ melalui titik-titik yang ditandai di bawah. Tentukan k dan nilai y saat x = 3.", "k = 3; y = 24", "Saat x = 0, y = k = 3; cek 3 · 2² = 12; 3 · 2³ = 24.", fig=K_FIG),
        Q(3, "Selesaikan 2<sup>x² − 3x</sup> = ¼.", "x = 1 atau x = 2", "x² − 3x = −2 → (x − 1)(x − 2) = 0."),
        Q(3, "Zat radioaktif 80 g mempunyai waktu paruh 6 jam. Berapa sisanya setelah 1 hari?", "5 g", "24 : 6 = 4 kali paruh: 80 · (½)⁴."),
        Q(3, "Harga mobil Rp200.000.000 dan turun 20% per tahun dari harga tahun sebelumnya. Berapa harganya setelah 3 tahun?", "Rp102.400.000", "200 juta · 0,8³ = 200 · 0,512 juta."),
    ],
))

# ================================================================== Subbab 4
SUB.append(dict(
    title="Logaritma dan Sifat-sifatnya",
    tujuan="Mengubah bentuk pangkat ke bentuk logaritma dan sebaliknya, lalu memakai sifat-sifat logaritma untuk menghitung dan menyederhanakan.",
    konsep=[
        "Logaritma adalah kebalikan pangkat: <b>ᵃlog b = c ⟺ aᶜ = b</b>. Syaratnya: basis a &gt; 0, a ≠ 1, dan bilangan b (numerus) &gt; 0. Contoh: ²log 8 = 3 karena 2³ = 8.",
        "Logaritma basis 10 biasanya ditulis tanpa basis: log 1.000 = 3.",
        "Sifat-sifat logaritma berasal dari sifat pangkat: perkalian menjadi penjumlahan, pembagian menjadi pengurangan, dan pangkat menjadi pengali.",
    ],
    rumus=["ᵃlog b = c ⟺ aᶜ = b; ᵃlog a = 1; ᵃlog 1 = 0; a<sup>ᵃlog b</sup> = b", "ᵃlog(bc) = ᵃlog b + ᵃlog c; ᵃlog(b/c) = ᵃlog b − ᵃlog c; ᵃlog bⁿ = n · ᵃlog b",
           "Ganti basis: ᵃlog b = " + fr("log b", "log a") + "; ᵃlog b · ᵇlog c = ᵃlog c", "ᵃ<sup>ᵐ</sup>log bⁿ = " + fr("n", "m") + " · ᵃlog b"],
    contoh=[
        ("Nilai logaritma", "Hitung ²log 32, log 0,01, dan ⁹log 27.", None, ["2⁵ = 32 → 5.", "10⁻² = 0,01 → −2.", "⁹log 27 = ³²log 3³ = 3/2."], "5; −2; 3/2"),
        ("Memakai log 2 dan log 3", "Diketahui log 2 = 0,301 dan log 3 = 0,477. Hitung log 6, log 50, dan log 12.", None,
         ["log 6 = log 2 + log 3 = 0,778.", "log 50 = log 100 − log 2 = 2 − 0,301 = 1,699.", "log 12 = 2 log 2 + log 3 = 1,079."], "0,778; 1,699; 1,079"),
    ],
    bertahap=dict(
        soal="Hitung ²log 12 + ²log 6 − ²log 9.",
        langkah=["Gabungkan: ²log (12 · 6 : ____) = ²log ____.", "²log 8 = ____ karena 2<sup>____</sup> = 8."],
        cek="Penjumlahan logaritma digabung menjadi perkalian karena",
        opsi=["(a) ᵃlog b + ᵃlog c = ᵃlog(bc)", "(b) ᵃlog b + ᵃlog c = ᵃlog(b + c)"],
        kunci="12 · 6 : 9 = 8; ²log 8 = 3. Alasan: (a).",
    ),
    jebakan=["log(a + b) ≠ log a + log b.", "log b : log c ≠ log(b/c); yang benar log b : log c = ᶜlog b.", "Numerus harus positif: log(−2) tidak terdefinisi."],
    latihan=[
        Q(1, "Hitung ³log 81.", "4", "3⁴ = 81."), Q(1, "Hitung ⁵log 1.", "0", "5⁰ = 1."), Q(1, "Hitung log 1.000.", "3", "10³."),
        Q(1, "Hitung ²log ⅛.", "−3", "2⁻³."), Q(1, "Tulis 2⁵ = 32 dalam bentuk logaritma.", "²log 32 = 5", "Definisi."),
        Q(2, "Hitung ³log 18 − ³log 2.", "2", "³log 9."), Q(2, "Hitung ²log 3 · ³log 16.", "4", "²log 16."),
        Q(2, "Dengan log 2 = 0,301 dan log 3 = 0,477, hitung log 18.", "1,255", "log 2 + 2 log 3 = 0,301 + 0,954."),
        Q(2, "Hitung ⁴log 32.", "5/2", "²²log 2⁵ = 5/2."),
        Q(3, "Jika ²log 3 = p, nyatakan ²log 24 dalam p.", "3 + p", "²log(8 · 3) = 3 + p."),
        Q(3, "Hitung ²log 25 · ⁵log 8.", "6", "2 · ²log 5 · 3 · ⁵log 2 = 6 · ²log 5 · ⁵log 2 = 6."),
        Q(3, "Hitung 2<sup>²log 7</sup> + ³log ³√3.", "22/3", "2<sup>²log 7</sup> = 7; ³log 3<sup>1/3</sup> = 1/3; 7 + 1/3."),
    ],
))

# ================================================================== Subbab 5
SUB.append(dict(
    title="Persamaan Logaritma dan Penerapannya",
    tujuan="Menyelesaikan persamaan logaritma sederhana dengan memeriksa syarat numerus, serta memakai logaritma pada keasaman (pH), taraf intensitas bunyi, dan waktu pertumbuhan.",
    konsep=[
        "Persamaan ᵃlog f(x) = ᵃlog g(x) diselesaikan dengan f(x) = g(x), lalu <b>setiap akar diperiksa</b>: f(x) dan g(x) harus positif. Akar yang membuat numerus tidak positif dibuang.",
        "Logaritma dipakai untuk besaran yang rentangnya sangat lebar. Keasaman larutan: <b>pH = −log[H⁺]</b>. Taraf intensitas bunyi: <b>β = 10 log(I/I₀)</b> desibel, dengan I₀ = 10⁻¹² W/m².",
        "Logaritma juga menjawab pertanyaan 'berapa lama?' pada pertumbuhan: dari N = N₀(1 + r)ⁿ diperoleh n = log(N/N₀) : log(1 + r).",
    ],
    rumus=["ᵃlog f(x) = ᵃlog g(x) ⟹ f(x) = g(x), dengan f(x) &gt; 0 dan g(x) &gt; 0", "ᵃlog f(x) = c ⟹ f(x) = aᶜ",
           "pH = −log[H⁺]; β = 10 log(I/I₀)", "n = " + fr("log(N/N₀)", "log(1 + r)")],
    contoh=[
        ("Persamaan sederhana", "Selesaikan ²log(x + 3) = 4.", None, ["x + 3 = 2⁴ = 16 → x = 13.", "Cek numerus: 13 + 3 = 16 &gt; 0."], "x = 13"),
        ("pH larutan", "Tentukan pH larutan dengan [H⁺] = 10⁻³ M dan larutan dengan [H⁺] = 2 × 10⁻³ M (log 2 = 0,301).", None,
         ["pH = −log 10⁻³ = 3.", "pH = −(log 2 + log 10⁻³) = −(0,301 − 3) ≈ 2,7."], "3 dan ≈ 2,7"),
    ],
    bertahap=dict(
        soal="Selesaikan log(x + 1) + log(x − 2) = 1.",
        langkah=["log[(x + 1)(x − 2)] = log ____ → (x + 1)(x − 2) = ____.", "x² − x − ____ = 0 → (x − 4)(x + ____) = 0.", "Cek numerus: x = −3 membuat x − 2 = ____ (tidak boleh). Jadi x = ____."],
        cek="Akar x = −3 dibuang karena",
        opsi=["(a) numerus logaritma harus positif", "(b) penyelesaian tidak boleh negatif"],
        kunci="log 10, = 10; x² − x − 12 = 0, (x − 4)(x + 3); −5; x = 4. Alasan: (a).",
    ),
    jebakan=["Selalu periksa numerus setiap akar.", "pH turun 1 berarti [H⁺] naik 10 kali, bukan naik 1.", "Jawaban 'berapa tahun' biasanya dibulatkan ke atas bila targetnya harus tercapai."],
    latihan=[
        Q(1, "Selesaikan ³log x = 2.", "x = 9", "3²."), Q(1, "Selesaikan log x = −2.", "x = 0,01", "10⁻²."), Q(1, "Berapa pH larutan dengan [H⁺] = 10⁻⁵ M?", "5", "−log 10⁻⁵."),
        Q(1, "Berapa taraf intensitas bunyi dengan intensitas 10⁻⁶ W/m²?", "60 dB", "10 log(10⁻⁶/10⁻¹²) = 10 · 6."), Q(1, "Selesaikan ²log(2x) = 5.", "x = 16", "2x = 32."),
        Q(2, "Selesaikan ²log(x − 1) + ²log(x + 1) = 3.", "x = 3", "x² − 1 = 8 → x = ±3; x = −3 membuat numerus negatif."),
        Q(2, "Tabungan berbunga majemuk 10% per tahun. Setelah berapa tahun (bulat) tabungan menjadi paling sedikit dua kali lipat? (log 2 = 0,301; log 1,1 = 0,0414)", "8 tahun", "n ≥ 0,301 : 0,0414 ≈ 7,27, dibulatkan ke atas."),
        Q(2, "Dua pengeras suara yang sama dinyalakan bersamaan sehingga intensitasnya dua kali. Berapa kenaikan taraf intensitasnya? (log 2 = 0,301)", "≈ 3 dB", "10 log 2."),
        Q(2, "Larutan A ber-pH 4 dan larutan B ber-pH 6. Berapa kali [H⁺] larutan A dibanding B?", "100 kali", "10⁻⁴ : 10⁻⁶."),
        Q(3, "Selesaikan (²log x)² − 3 · ²log x + 2 = 0.", "x = 2 atau x = 4", "Misalkan p = ²log x: (p − 1)(p − 2) = 0."),
        Q(3, "Selesaikan log(x − 3) + log x = 1.", "x = 5", "x² − 3x − 10 = 0 → x = 5 atau −2; −2 dibuang."),
        Q(3, "Penduduk kota 1 juta jiwa bertambah 2% per tahun. Setelah berapa tahun (bulat) penduduknya paling sedikit 1,5 juta? (log 1,5 = 0,176; log 1,02 = 0,0086)", "21 tahun", "n ≥ 0,176 : 0,0086 ≈ 20,5."),
    ],
))

CAMPURAN = [
    Q(1, "Hitung 2⁻² + 4⁰.", "5/4", "¼ + 1."), Q(1, "Sederhanakan √32.", "4√2", "√(16 · 2)."), Q(1, "Hitung ²log 64.", "6", "2⁶."), Q(1, "Hitung 32<sup>2/5</sup>.", "4", "(⁵√32)² = 2²."),
    Q(2, "Selesaikan 3<sup>x+2</sup> = 9<sup>x</sup>.", "x = 2", "x + 2 = 2x."), Q(2, "Hitung ³log 54 − ³log 2.", "3", "³log 27."),
    Q(2, "Rasionalkan " + fr("3", "√3") + ".", "√3", "3√3 : 3."), Q(2, "Modal Rp5.000.000 berbunga majemuk 10% per tahun. Berapa nilainya setelah 3 tahun?", "Rp6.655.000", "5.000.000 · 1,331."),
    Q(2, "Jika log 2 = 0,301, hitung log 0,2.", "−0,699", "0,301 − 1."),
    Q(3, "Selesaikan ²log(x + 2) = 1 + ²log x.", "x = 2", "x + 2 = 2x."),
]

TKA = [
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Bentuk sederhana dari " + fr("2⁵ · 4³", "8³") + " adalah ....",
         opsi=["4", "8", "2", "16", "½"], kunci=0, bahas="2⁵ · 2⁶ : 2⁹ = 2².", salah="B: 2³ (lupa satu faktor). C, E: salah mengurangkan pangkat. D: 2⁴."),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pgk", soal="Bentuk yang nilainya sama dengan 2√3 adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["√12", fr("6", "√3"), "2 · 3<sup>1/2</sup>", "√6 + √6", "3√2"], kunci=[0, 1, 2], bahas="√12 = 2√3; 6/√3 = 2√3; 2 · 3<sup>1/2</sup> = 2√3.", salah="D: 2√6. E: √18."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="pg", soal="Banyak bakteri dalam sebuah sampel dimodelkan N(t) = 200 · 3<sup>t/2</sup>, dengan t dalam jam. Interpretasi yang tepat adalah ....",
         opsi=["Banyak bakteri menjadi tiga kali lipat setiap 2 jam, mulai dari 200.", "Banyak bakteri menjadi tiga kali lipat setiap jam.", "Banyak bakteri bertambah 3 setiap 2 jam.",
               "Banyak bakteri menjadi dua kali lipat setiap 3 jam.", "Banyak bakteri bertambah 200 setiap jam."], kunci=0,
         bahas="Setiap t bertambah 2, pangkat bertambah 1, jadi N dikali 3; N(0) = 200.", salah="B: membaca pangkat t/2 sebagai t. C, E: model linear. D: basis dan penyebut tertukar."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="pg", soal="Massa obat dalam darah seorang pasien menurun menurut grafik eksponen di bawah, dengan t dalam hari.", fig=DECAY_FIG,
         soal2="Massa obat tepat 50 mg pada hari ke ....", opsi=["2", "3", "4", "5", "8"], kunci=2,
         bahas="Dari grafik, massa menjadi setengah setiap hari: 800, 400, 200, 100, 50 mg. Jadi t = 4.", salah="A, B: saat 200 mg dan 100 mg. D: satu hari terlalu lama. E: model dianggap linear (turun 100 mg per hari)."),
    dict(tipe="MAT-MODEL", lv=2, fmt="pg", soal="Rina menabung Rp10.000.000 di bank dengan bunga majemuk 5% per tahun. Saldo tabungannya setelah 2 tahun (tanpa penarikan dan biaya) adalah ....",
         opsi=["Rp11.025.000", "Rp11.000.000", "Rp10.500.000", "Rp11.050.000", "Rp12.100.000"], kunci=0, bahas="10.000.000 · 1,05² = 11.025.000.", salah="B: bunga tunggal. C: hanya 1 tahun. D: 1,05 · 1,05 dihitung salah. E: memakai 10%."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Diketahui ²log a = 3 dan ²log b = 5. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["a = 8", "²log(ab) = 8", "b : a = 4", "²log(a + b) = 8"], kunci=[True, True, True, False],
         bahas="a = 8, b = 32; ab = 256 = 2⁸; b : a = 4; a + b = 40, bukan 2⁸.", salah=""),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg",
         soal="Dina punya modal Rp10.000.000 dan ingin uangnya mencapai paling sedikit Rp15.000.000 secepat mungkin (dalam tahun penuh). Pilihan investasinya: P bunga tunggal 9% per tahun; Q bunga majemuk 8%; R bunga majemuk 9%; S bunga majemuk 7%; T bunga tunggal 8%. (1,08⁵ = 1,469; 1,08⁶ = 1,587; 1,09⁴ = 1,412; 1,09⁵ = 1,539; 1,07⁵ = 1,403; 1,07⁶ = 1,501.) Pilihan terbaik adalah ....",
         opsi=["investasi R, tercapai dalam 5 tahun", "investasi P, tercapai dalam 5 tahun", "investasi Q, tercapai dalam 5 tahun", "investasi S, tercapai dalam 6 tahun", "investasi T, tercapai dalam 6 tahun"], kunci=0,
         bahas="P: 1 + 0,09n ≥ 1,5 → n ≥ 5,6 → 6 tahun. Q: 6 tahun. R: 5 tahun (1,539). S: 6 tahun. T: n ≥ 6,25 → 7 tahun. Hanya R yang 5 tahun.",
         salah="B: investasi P baru tercapai pada tahun ke-6. C: 1,08⁵ = 1,469 &lt; 1,5. D: 6 tahun lebih lama dari R. E: investasi T perlu 7 tahun."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Diketahui a &gt; 1, aˣ = 5, dan aʸ = 2. Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["a<sup>x+y</sup> = 10", "a<sup>x−y</sup> = 2,5", "a<sup>2x</sup> = 25", "a<sup>xy</sup> = 10", "x &gt; y"], kunci=[0, 1, 2, 4],
         bahas="a<sup>x+y</sup> = 5 · 2; a<sup>x−y</sup> = 5 : 2; a<sup>2x</sup> = 5². Karena a &gt; 1, fungsi aᵗ naik, sehingga 5 &gt; 2 berarti x &gt; y.", salah="D: a<sup>xy</sup> = (aˣ)ʸ = 5ʸ, bukan 10."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Larutan A ber-pH 3 dan larutan B ber-pH 5, dengan pH = −log[H⁺]. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["[H⁺] larutan A 100 kali [H⁺] larutan B.", "Larutan A lebih asam daripada larutan B.", "[H⁺] larutan A adalah 10⁻³ M.", "Bila [H⁺] dinaikkan 1 M, pH turun 1."],
         kunci=[True, True, True, False], bahas="10⁻³ : 10⁻⁵ = 100; pH lebih kecil berarti lebih asam. pH turun 1 bila [H⁺] dikali 10, bukan ditambah 1.", salah=""),
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Perhatikan grafik y = 2ˣ dan y = (½)ˣ berikut.", fig=EXP_FIG, soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["Kedua grafik melalui titik (0, 1).", "Kedua grafik simetris terhadap sumbu y.", "Kedua grafik naik.", "Kedua grafik tidak pernah menyentuh sumbu x.", "Kedua grafik berpotongan di (1, 2)."], kunci=[0, 1, 3],
         bahas="a⁰ = 1; (½)ˣ = 2⁻ˣ adalah cerminan 2ˣ terhadap sumbu y; aˣ &gt; 0.", salah="C: y = (½)ˣ turun. E: di x = 1 nilainya 2 dan ½."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Nilai 3⁻² adalah ....", ["1/9", "−9", "−6", "9", "1/6"], 0, "1/3².", "B, C: pangkat negatif dianggap tanda negatif. D: tanpa kebalikan. E: 1/(3 · 2)."),
    ("Bentuk sederhana " + fr("a⁵b²", "a²b⁻¹") + " adalah ....", ["a³b³", "a³b", "a⁷b", "a³b²", "a¹⁰b⁻²"], 0, "a<sup>5−2</sup>b<sup>2−(−1)</sup>.", "B: 2 − 1. C: pangkat a dijumlahkan. D, E: tidak sesuai."),
    ("Nilai 125<sup>2/3</sup> adalah ....", ["25", "5", "83,3", "625", "15"], 0, "(∛125)² = 5².", "B: hanya akar pangkat tiga. C: 125 · 2/3. D: 5⁴. E: tidak sesuai."),
    ("√45 + √20 = ....", ["5√5", "√65", "13√5", "6√5", "5√2"], 0, "3√5 + 2√5.", "B: akar dijumlahkan langsung. C, D, E: tidak sesuai."),
    ("Bentuk rasional dari " + fr("6", "√2") + " adalah ....", ["3√2", "6√2", "√3", "2√6", "12"], 0, "6√2 : 2.", "B: lupa dibagi 2. C, D, E: tidak sesuai."),
    ("Penyelesaian 2<sup>x−1</sup> = 16 adalah ....", ["5", "4", "8", "3", "17"], 0, "x − 1 = 4.", "B: lupa −1. C: 16 : 2. D: x − 1 = 2. E: x − 1 = 16."),
    ("Grafik y = aˣ dengan 0 &lt; a &lt; 1 ....", ["turun dan melalui (0, 1)", "naik dan melalui (0, 1)", "turun dan melalui (0, 0)", "naik dan melalui (1, 0)", "berupa garis lurus"], 0, "Basis kurang dari 1.", "B: untuk a &gt; 1. C, D: titik salah. E: bukan garis lurus."),
    ("Nilai ²log 16 + ³log 9 adalah ....", ["6", "8", "25", "5", "4"], 0, "4 + 2.", "B, C, D, E: salah menghitung salah satu suku."),
    ("Jika log 2 = 0,301 dan log 3 = 0,477, maka log 24 = ....", ["1,380", "0,778", "1,079", "1,431", "0,954"], 0, "3 log 2 + log 3 = 0,903 + 0,477.", "B: log 6. C: log 12. D: 3 log 3. E: 2 log 3."),
    ("Nilai ²log 5 · ⁵log 8 adalah ....", ["3", "8", "40", "1", "13"], 0, "²log 8.", "B: numerus. C: 5 · 8. D, E: tidak sesuai."),
    ("Penyelesaian ³log(2x − 1) = 2 adalah ....", ["5", "4", "4,5", "3,5", "9"], 0, "2x − 1 = 9.", "B: 2x = 8. C: 2x = 9. D: 2x − 1 = 6. E: numerus."),
    ("Penyelesaian log(x + 2) + log(x − 1) = 1 adalah ....", ["x = 3", "x = 3 atau x = −4", "x = −4", "x = 4", "x = 1"], 0, "x² + x − 12 = 0 → 3 atau −4; −4 dibuang.", "B: tidak memeriksa numerus. C: akar yang ditolak. D, E: tidak sesuai."),
    ("pH larutan dengan [H⁺] = 10⁻⁸ M adalah ....", ["8", "−8", "0,8", "10⁸", "−0,8"], 0, "−log 10⁻⁸.", "B: lupa tanda minus. C, D, E: tidak sesuai."),
    ("Zat 64 g mempunyai waktu paruh 2 hari. Sisa setelah 8 hari adalah ....", ["4 g", "8 g", "16 g", "0,25 g", "32 g"], 0, "4 kali paruh: 64 : 16.", "B: 3 kali paruh. C: 2 kali. D: 8 kali paruh. E: 1 kali."),
    ("Harga barang Rp1.000.000 naik 10% per tahun. Harganya setelah 2 tahun adalah ....", ["Rp1.210.000", "Rp1.200.000", "Rp1.100.000", "Rp1.020.000", "Rp1.221.000"], 0, "1.000.000 · 1,1².", "B: kenaikan tunggal. C: 1 tahun. D: 2% saja. E: tidak sesuai."),
]
UJI_URAIAN = [
    ("Sederhanakan " + fr("(2a²b⁻¹)³ · 4a⁻⁵", "8ab⁻²") + " dan tuliskan tanpa pangkat negatif.", "4/b", "(8a⁶b⁻³ · 4a⁻⁵) : (8ab⁻²) = 4a<sup>6−5−1</sup>b<sup>−3+2</sup> = 4b⁻¹."),
    ("Rasionalkan " + fr("12", "√6 + √2") + " dan sederhanakan.", "3(√6 − √2)", "12(√6 − √2) : (6 − 2)."),
    ("Selesaikan 27<sup>x−1</sup> = 9<sup>x+1</sup>, lalu jelaskan langkahmu.", "x = 5", "3<sup>3x−3</sup> = 3<sup>2x+2</sup> → 3x − 3 = 2x + 2."),
    ("Selesaikan ²log(x + 4) + ²log(x − 2) = 4 dan periksa syarat numerusnya.", "x = 4", "(x + 4)(x − 2) = 16 → x² + 2x − 24 = 0 → x = 4 atau −6; −6 dibuang."),
    ("Populasi ikan 2.000 ekor berkurang 20% per tahun. (a) Berapa populasinya setelah 3 tahun? (b) Setelah berapa tahun (bulat) populasinya pertama kali di bawah 1.000? (log 0,5 = −0,301; log 0,8 = −0,097)",
     "(a) 1.024 ekor; (b) 4 tahun", "(a) 2.000 · 0,8³ = 1.024. (b) n &gt; −0,301 : −0,097 ≈ 3,1, jadi tahun ke-4 (1.024 → 819)."),
]

META = dict(
    title="Modul Eksponen dan Logaritma", kick="Modul belajar Matematika · Fase E · Kelas X", big="Eksponen dan Logaritma",
    subtitle="Sifat pangkat, bentuk akar, fungsi dan persamaan eksponen, logaritma, serta penerapannya pada pertumbuhan, peluruhan, pH, dan desibel",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat menggeneralisasi sifat-sifat bilangan berpangkat (termasuk bilangan pangkat pecahan), menyelesaikan masalah yang berkaitan dengan fungsi eksponen dan logaritma, serta memodelkan pertumbuhan dan peluruhan, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Pangkat dan logaritma: dua arah dari satu hubungan</h2><table><tr><th>Diketahui</th><th>Dicari</th><th>Alat</th></tr><tr><td>basis dan pangkat</td><td>hasil</td><td>pangkat: 2⁵ = 32</td></tr><tr><td>basis dan hasil</td><td>pangkat</td><td>logaritma: ²log 32 = 5</td></tr><tr><td>pangkat dan hasil</td><td>basis</td><td>akar: ⁵√32 = 2</td></tr></table>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit</b> tanpa kalkulator, kecuali soal yang memberi nilai logaritma.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="ᵃlog b berarti logaritma b dengan basis a; log b tanpa basis berarti basis 10. Nilai logaritma yang diperlukan selalu diberikan di soal. Desimal ditulis dengan koma dan ribuan dengan titik (Rp1.210.000).",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>sifat pangkat, bentuk akar, persamaan eksponen, atau logaritma?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025 (specs/tka-templates/matematika.md).",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-MODEL, MAT-FUNGSI): mengenali, menghitung, bekerja mundur, memodelkan, atau menafsirkan fungsi. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Mengapa a⁰ = 1 dan a⁻ⁿ = 1/aⁿ?", "Kapan sebuah akar persamaan logaritma harus dibuang?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Pangkat</th><td>a<sup>m</sup>a<sup>n</sup> = a<sup>m+n</sup>; a<sup>m</sup>/a<sup>n</sup> = a<sup>m−n</sup>; (a<sup>m</sup>)<sup>n</sup> = a<sup>mn</sup>; a⁰ = 1; a⁻ⁿ = 1/aⁿ</td></tr>"
        "<tr><th>Akar</th><td>a<sup>m/n</sup> = ⁿ√(aᵐ); √(ab) = √a√b; a/√b = a√b/b; a/(√b − √c) = a(√b + √c)/(b − c)</td></tr>"
        "<tr><th>Fungsi eksponen</th><td>y = aˣ melalui (0, 1), selalu positif; naik bila a &gt; 1, turun bila 0 &lt; a &lt; 1</td></tr>"
        "<tr><th>Pertumbuhan/peluruhan</th><td>N = N₀(1 ± r)ᵗ; waktu paruh: N = N₀(½)<sup>t/T</sup></td></tr>"
        "<tr><th>Logaritma</th><td>ᵃlog b = c ⟺ aᶜ = b (a &gt; 0, a ≠ 1, b &gt; 0)</td></tr>"
        "<tr><th>Sifat logaritma</th><td>log(bc) = log b + log c; log(b/c) = log b − log c; log bⁿ = n log b; ᵃlog b = log b/log a</td></tr>"
        "<tr><th>Penerapan</th><td>pH = −log[H⁺]; β = 10 log(I/I₀); n = log(N/N₀)/log(1 + r)</td></tr></table>"
        '<div class="fig">' + EXP_FIG + "</div>"),
    jebakan5=["−3² = −9, sedangkan (−3)² = 9.", "a<sup>m</sup> + a<sup>n</sup> ≠ a<sup>m+n</sup> dan log(a + b) ≠ log a + log b.", "√(a + b) ≠ √a + √b.",
              "Pangkat negatif menghasilkan kebalikan, bukan bilangan negatif.", "Periksa numerus setiap akar persamaan logaritma."],
    guru=["Materi mengikuti Kurikulum Merdeka Matematika SMA Fase E (bab Eksponen dan Logaritma pada buku kelas X); urutan bab dapat berbeda antarsekolah.",
          "Notasi logaritma mengikuti kebiasaan buku Indonesia (²log 8). Nilai log yang dipakai (log 2 = 0,301; log 3 = 0,477, dan lainnya) selalu ditulis di soal.",
          "Penerapan pH dan desibel memakai definisi baku: pH = −log[H⁺] dan β = 10 log(I/I₀) dengan I₀ = 10⁻¹² W/m².",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


def check():
    c = close
    # subbab 1
    assert F(2 ** 3 * 2 ** 5, 2 ** 4) == 16 and 2 ** 7 == 128 and 5 ** 2 == 25 and 3 ** 6 == 729 and F(1, 2 ** 3) == F(1, 8)
    assert F(4 ** 3 * 8 ** 2, 2 ** 10) == 4 and F(3, 2) ** 2 == F(9, 4) and 6e4 * 5e-7 == 0.03 and 3 ** 20 > 2 ** 30
    c(3e8 * 3.15e7, 9.45e15, 1e10); c(2 ** 5 * 4 - 2 ** 5, 3 * 2 ** 5)
    # subbab 2
    c(math.sqrt(50) + math.sqrt(18) - math.sqrt(8), 6 * math.sqrt(2)); c(8 ** (2 / 3), 4); c(6 / (3 - math.sqrt(3)), 3 + math.sqrt(3))
    c(10 / (math.sqrt(7) - math.sqrt(2)), 2 * (math.sqrt(7) + math.sqrt(2))); c(16 ** 0.75, 8); c(3 * math.sqrt(2) * math.sqrt(8), 12)
    c(math.sqrt(75) - math.sqrt(27) + math.sqrt(12), 4 * math.sqrt(3)); c(2 / (math.sqrt(5) - 1), (math.sqrt(5) + 1) / 2); c((math.sqrt(3) + 1) ** 2, 4 + 2 * math.sqrt(3))
    c(math.sqrt(8) * 4 ** (1 / 3) / 2, 2 ** (7 / 6)); c(math.sqrt(50) * math.sqrt(2), 10)
    # subbab 3
    c(500 * 2 ** 6, 32000); c(1000 * 1.1 ** 2, 1210); c(80 * 0.5 ** 4, 5); c(200e6 * 0.8 ** 3, 102.4e6, 1); c(3 * 2 ** 3, 24)
    for x in (1, 2):
        assert x * x - 3 * x == -2
    # subbab 4
    c(lg(32, 2), 5); c(lg(27, 9), 1.5); c(L2 + L3, 0.778); c(2 - L2, 1.699); c(2 * L2 + L3, 1.079); c(lg(12 * 6 / 9, 2), 3)
    c(lg(16, 2), 4); c(L2 + 2 * L3, 1.255); c(lg(32, 4), 2.5); c(lg(25, 2) * lg(8, 5), 6); c(7 + 1 / 3, 22 / 3)
    # subbab 5
    c(3 - L2, 2.699); c(10 * 6, 60); c(math.ceil(0.301 / 0.0414), 8); c(10 * L2, 3.01); c(math.ceil(0.176 / 0.0086), 21); c(1.1 ** 7, 1.949, 0.001)
    assert 1.1 ** 8 > 2 > 1.1 ** 7 and 1.02 ** 21 > 1.5 > 1.02 ** 20
    for x in (4,):
        assert (x + 1) * (x - 2) == 10
    assert 5 * 5 - 3 * 5 - 10 == 0 and (-2) - 3 < 0
    # campuran, TKA, uji
    c(5e6 * 1.1 ** 3, 6.655e6, 1); c(1e7 * 1.05 ** 2, 1.1025e7, 1)
    plans = {"A": math.ceil((1.5 - 1) / 0.09), "B": next(k for k in range(1, 20) if 1.08 ** k >= 1.5), "C": next(k for k in range(1, 20) if 1.09 ** k >= 1.5),
             "D": next(k for k in range(1, 20) if 1.07 ** k >= 1.5), "E": math.ceil((1.5 - 1) / 0.08)}
    assert plans == {"A": 6, "B": 6, "C": 5, "D": 6, "E": 7}
    c(1.08 ** 5, 1.469, 0.001); c(1.09 ** 5, 1.539, 0.001); c(1.07 ** 6, 1.501, 0.001); c(1.09 ** 4, 1.412, 0.001); c(1.07 ** 5, 1.403, 0.001); c(1.08 ** 6, 1.587, 0.001)
    c(800 * 0.5 ** 4, 50); c(3 * L2 + L3, 1.380); c(64 / 16, 4); c(2000 * 0.8 ** 3, 1024); c(2000 * 0.8 ** 4, 819.2)
    c(12 / (math.sqrt(6) + math.sqrt(2)), 3 * (math.sqrt(6) - math.sqrt(2)))
    assert 4 * 4 + 2 * 4 - 24 == 0 and (4 + 4) * (4 - 2) == 16
    return True
