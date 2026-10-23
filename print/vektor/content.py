"""Content of the printable module "Vektor dan Operasinya" (Matematika kelas X).

Two-dimensional vectors written as columns (x; y). Every numeric answer is re-derived in check()
with exact arithmetic where possible.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import plane  # noqa: E402
from kit import n, fr, Q, close  # noqa: E402

BLUE, RED, GREEN = "#1f3a68", "#c0502a", "#2e6b32"


def col(a, b):
    """A column vector (a; b) drawn with round brackets."""
    a, b = (n(v) if isinstance(v, (int, float)) else str(v).replace("-", "−") for v in (a, b))
    return (f'<span style="display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.1;font-size:.9em;'
            f'border-left:1.2px solid;border-right:1.2px solid;border-radius:6px;padding:0 4px;margin:0 2px">'
            f"<span>{a}</span><span>{b}</span></span>")


def vec(name):
    return f"<b>{name}</b>"


def c2(v):
    return col(n(v[0]), n(v[1]))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(k, a):
    return (k * a[0], k * a[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def norm(a):
    return math.hypot(*a)


def angle(a, b):
    return math.degrees(math.acos(dot(a, b) / (norm(a) * norm(b))))


a_, b_ = vec("a"), vec("b")

PRASYARAT = [
    ("P1", "Hitung √(3² + 4²) dan √(6² + 8²).", "5 dan 10", "Tripel Pythagoras."),
    ("P2", "Tentukan jarak titik (1, 2) dan (4, 6).", "5", "√(3² + 4²)."),
    ("P3", "Tentukan titik tengah ruas garis (2, 4) dan (8, 10).", "(5, 7)", "Rata-rata koordinat."),
    ("P4", "Selesaikan sistem x + 3y = 7 dan 2x + y = 4.", "x = 1, y = 2", "Eliminasi."),
    ("P5", "Tuliskan nilai cos 0°, cos 60°, cos 90°, dan cos 120°.", "1; ½; 0; −½", "Sudut istimewa."),
    ("P6", "Tentukan kemiringan garis melalui (0, 1) dan (2, 5).", "2", "(5 − 1) : 2."),
    ("P7", "Sederhanakan √50.", "5√2", "√(25 · 2)."),
    ("P8", "Hitung 3 · (−2) + 4 · 5.", "14", "−6 + 20."),
]

INGAT = [
    ("A", "Pythagoras dan jarak dua titik", "P1, P2, P7", "Subbab 1–2", ["Jarak (x₁, y₁) ke (x₂, y₂) = √((x₂ − x₁)² + (y₂ − y₁)²).", "Tripel: 3-4-5, 5-12-13, 6-8-10, 8-15-17."]),
    ("B", "Titik tengah dan kemiringan", "P3, P6", "Subbab 3", ["Titik tengah = rata-rata koordinat. Tiga titik segaris bila kemiringan antarpasangannya sama."]),
    ("C", "Sistem persamaan linear", "P4", "Subbab 2", ["Eliminasi atau substitusi satu variabel."]),
    ("D", "Nilai kosinus", "P5, P8", "Subbab 4–5", ["cos 0° = 1; cos 30° = ½√3; cos 45° = ½√2; cos 60° = ½; cos 90° = 0; cos 120° = −½; cos 180° = −1."]),
]

SUB = []

# ================================================================== Subbab 1
F11 = plane((0, 6, 1), (0, 7, 1), arrows=[(1, 2, 4, 6, BLUE, "AB")], points=[(1, 2, "A(1, 2)"), (4, 6, "B(4, 6)")],
            segs=[(1, 2, 4, 2, RED, True), (4, 2, 4, 6, RED, True)], labels=[(2.2, 1.6, "3", RED), (4.15, 4, "4", RED)])
F15 = plane((0, 5, 1), (0, 4, 1), arrows=[(1, 1, 4, 3, BLUE, "v")])
SUB.append(dict(
    title="Konsep Vektor, Notasi, dan Besarnya",
    tujuan="Menyatakan vektor dengan ruas garis berarah, vektor kolom, dan vektor satuan, lalu menghitung besar (panjang) vektor.",
    konsep=[
        "<b>Vektor</b> adalah besaran yang mempunyai besar dan arah. Secara geometris vektor digambar sebagai ruas garis berarah; vektor dari titik A ke titik B ditulis " + vec("AB") + ".",
        "Pada bidang koordinat, vektor ditulis sebagai <b>vektor kolom</b> " + col("x", "y") + ", yaitu perpindahan x satuan ke kanan dan y satuan ke atas. Bentuk lain: x" + vec("i") + " + y" + vec("j") + ", dengan " + vec("i") + " dan " + vec("j") + " vektor satuan searah sumbu x dan y.",
        "Dua vektor <b>sama</b> bila besar dan arahnya sama, di mana pun letaknya. Vektor −" + a_ + " sama besar dengan " + a_ + " tetapi berlawanan arah. <b>Vektor satuan</b> adalah vektor yang panjangnya 1.",
    ],
    rumus=[vec("AB") + " = " + col("x<sub>B</sub> − x<sub>A</sub>", "y<sub>B</sub> − y<sub>A</sub>"), "|" + a_ + "| = √(x² + y²) untuk " + a_ + " = " + col("x", "y"),
           "Vektor satuan searah " + a_ + ": " + fr(a_, "|" + a_ + "|")],
    contoh=[
        ("Vektor dari dua titik", "Diketahui A(1, 2) dan B(4, 6). Tentukan " + vec("AB") + " dan |" + vec("AB") + "|.", F11,
         [vec("AB") + " = " + col("4 − 1", "6 − 2") + " = " + col(3, 4) + ".", "|" + vec("AB") + "| = √(9 + 16) = 5."], vec("AB") + " = " + col(3, 4) + "; panjang 5"),
        ("Vektor satuan", "Tentukan vektor satuan searah " + vec("v") + " = " + col(6, -8) + ".", None,
         ["|" + vec("v") + "| = √(36 + 64) = 10.", "Vektor satuan = " + col("6/10", "−8/10") + " = " + col("0,6", "−0,8") + "."], col("0,6", "−0,8")),
    ],
    bertahap=dict(
        soal="Tentukan besar dan vektor satuan searah " + vec("w") + " = " + col(-5, 12) + ".",
        langkah=["|" + vec("w") + "| = √((−5)² + 12²) = √____ = ____.", "Vektor satuan = " + col("−5/____", "12/____") + "."],
        cek="Besar vektor tetap positif walaupun komponennya negatif karena",
        opsi=["(a) setiap komponen dikuadratkan", "(b) tanda negatif boleh diabaikan"],
        kunci="√169 = 13; " + col("−5/13", "12/13") + ". Alasan: (a).",
    ),
    jebakan=[vec("AB") + " = titik akhir − titik awal, bukan sebaliknya; " + vec("BA") + " = −" + vec("AB") + ".", "Panjang vektor tidak pernah negatif.", "Dua vektor dengan komponen sama adalah vektor yang sama walaupun pangkalnya berbeda."],
    latihan=[
        Q(1, "Hitung panjang vektor " + col(3, 4) + ".", "5", "√25."),
        Q(1, "Diketahui A(2, 1) dan B(5, 5). Tentukan " + vec("AB") + ".", col(3, 4), "(5 − 2, 5 − 1)."),
        Q(1, "Jika " + a_ + " = " + col(2, -7) + ", tentukan −" + a_ + ".", col(-2, 7), "Semua komponen berganti tanda."),
        Q(1, "Tulis " + vec("v") + " = 3" + vec("i") + " − 2" + vec("j") + " sebagai vektor kolom.", col(3, -2), "Komponen x dan y."),
        Q(1, "Tentukan vektor " + vec("v") + " pada gambar di bawah sebagai vektor kolom.", col(3, 2), "Dari (1, 1) ke (4, 3).", fig=F15),
        Q(2, "Hitung panjang " + col(2, -1) + ".", "√5", "√(4 + 1)."),
        Q(2, "Tentukan vektor satuan searah " + col(4, 3) + ".", col("4/5", "3/5"), "Dibagi panjangnya, 5."),
        Q(2, "Panjang vektor " + col("p", 4) + " adalah 5. Tentukan p.", "p = 3 atau p = −3", "p² + 16 = 25."),
        Q(2, "Diketahui " + col("2a", 3) + " = " + col(6, "b + 1") + ". Tentukan a dan b.", "a = 3; b = 2", "Komponen yang bersesuaian sama."),
        Q(3, "Diketahui A(−2, 3) dan B(4, −5). Hitung |" + vec("AB") + "|.", "10", vec("AB") + " = " + col(6, -8) + "."),
        Q(3, "Titik A(0, 0), B(3, 4), dan C(3, 0) membentuk segitiga. Hitung kelilingnya dengan panjang vektor-vektor sisinya.", "12", "|AB| = 5, |BC| = 4, |AC| = 3."),
        Q(3, "Tentukan semua vektor yang panjangnya 26 dan sejajar " + col(5, 12) + ".", col(10, 24) + " atau " + col(-10, -24), "Panjang " + col(5, 12) + " adalah 13; kalikan ±2."),
    ],
))

# ================================================================== Subbab 2
F21 = plane((0, 7, 1), (0, 5, 1), arrows=[(0, 0, 4, 1, BLUE, "a"), (4, 1, 6, 4, RED, "b"), (0, 0, 6, 4, GREEN, "a + b")])
SUB.append(dict(
    title="Penjumlahan, Pengurangan, dan Perkalian Skalar",
    tujuan="Menjumlahkan dan mengurangkan vektor secara geometris dan dengan komponen, mengalikan vektor dengan skalar, serta mengenali vektor yang sejajar.",
    konsep=[
        "<b>Aturan segitiga:</b> letakkan pangkal " + b_ + " di ujung " + a_ + "; " + a_ + " + " + b_ + " ditarik dari pangkal " + a_ + " ke ujung " + b_ + ". <b>Aturan jajargenjang</b> memberi hasil yang sama. Dengan komponen, jumlahkan komponen yang bersesuaian.",
        a_ + " − " + b_ + " = " + a_ + " + (−" + b_ + "). Untuk titik-titik: " + vec("AB") + " + " + vec("BC") + " = " + vec("AC") + ".",
        "<b>Perkalian skalar</b> k" + a_ + " mengalikan setiap komponen dengan k: panjangnya menjadi |k| kali, arahnya tetap bila k &gt; 0 dan berbalik bila k &lt; 0. Dua vektor <b>sejajar</b> bila yang satu kelipatan skalar yang lain.",
    ],
    rumus=[col("a₁", "a₂") + " ± " + col("b₁", "b₂") + " = " + col("a₁ ± b₁", "a₂ ± b₂"), "k" + col("a₁", "a₂") + " = " + col("ka₁", "ka₂"), a_ + " ∥ " + b_ + " ⟺ " + a_ + " = k" + b_ + " untuk suatu k"],
    contoh=[
        ("Operasi dengan komponen", "Diketahui " + a_ + " = " + col(4, 1) + " dan " + b_ + " = " + col(2, 3) + ". Gambarkan " + a_ + " + " + b_ + " dan hitung " + a_ + " + " + b_ + ", " + a_ + " − " + b_ + ", dan 3" + a_ + " − 2" + b_ + ".", F21,
         [a_ + " + " + b_ + " = " + col(6, 4) + ".", a_ + " − " + b_ + " = " + col(2, -2) + ".", "3" + a_ + " − 2" + b_ + " = " + col("12 − 4", "3 − 6") + " = " + col(8, -3) + "."], col(6, 4) + "; " + col(2, -2) + "; " + col(8, -3)),
        ("Sejajar", "Apakah " + col(2, -3) + " dan " + col(-6, 9) + " sejajar?", None, [col(-6, 9) + " = −3 · " + col(2, -3) + ".", "Sejajar, tetapi berlawanan arah."], "sejajar, berlawanan arah"),
    ],
    bertahap=dict(
        soal="Tentukan x dan y jika 2" + col("x", 1) + " + " + col(3, "y") + " = " + col(7, 5) + ".",
        langkah=["Komponen pertama: 2x + 3 = ____ → x = ____.", "Komponen kedua: 2 + y = ____ → y = ____."],
        cek="Persamaan vektor dipecah menjadi dua persamaan karena",
        opsi=["(a) dua vektor sama bila setiap komponennya sama", "(b) panjang kedua ruas harus sama"],
        kunci="7, x = 2; 5, y = 3. Alasan: (a).",
    ),
    jebakan=["|" + a_ + " + " + b_ + "| ≠ |" + a_ + "| + |" + b_ + "| kecuali keduanya searah.", vec("AB") + " = " + vec("b") + " − " + vec("a") + " (posisi B dikurangi posisi A).", "Mengalikan dengan skalar negatif membalik arah vektor."],
    latihan=[
        Q(1, "Hitung " + col(1, 4) + " + " + col(3, -2) + ".", col(4, 2), "Komponen dijumlah."), Q(1, "Hitung " + col(5, 3) + " − " + col(2, 7) + ".", col(3, -4), "Komponen dikurangkan."),
        Q(1, "Hitung 4" + col(-1, 2) + ".", col(-4, 8), "Setiap komponen dikali 4."), Q(1, "Sederhanakan " + vec("AB") + " + " + vec("BC") + " + " + vec("CD") + ".", vec("AD"), "Aturan segitiga berulang."),
        Q(1, "Jika |" + a_ + "| = 3, berapa |−2" + a_ + "|?", "6", "|k| · |" + a_ + "|."),
        Q(2, "Diketahui " + a_ + " = " + col(3, 1) + " dan " + b_ + " = " + col(1, -2) + ". Hitung 2" + a_ + " − 3" + b_ + ".", col(3, 8), "(6 − 3, 2 + 6)."),
        Q(2, "Tentukan k agar " + col(2, "k") + " sejajar dengan " + col(6, 9) + ".", "k = 3", col(6, 9) + " = 3 · " + col(2, 3) + "."),
        Q(2, "Diketahui " + a_ + " = " + col(1, 2) + " dan " + b_ + " = " + col(2, 2) + ". Bandingkan |" + a_ + " + " + b_ + "| dengan |" + a_ + "| + |" + b_ + "|.", "5 dan ≈ 5,06; tidak sama",
          "|" + col(3, 4) + "| = 5; √5 + √8 ≈ 5,06."),
        Q(2, "Tentukan x dan y agar x" + col(1, 2) + " + y" + col(3, 1) + " = " + col(7, 4) + ".", "x = 1; y = 2", "x + 3y = 7 dan 2x + y = 4."),
        Q(3, "Sebuah kapal bergerak 3 km ke timur, 4 km ke utara, lalu 2 km ke barat. Nyatakan perpindahannya sebagai vektor kolom dan hitung jaraknya dari titik awal.", col(1, 4) + "; √17 ≈ 4,12 km", "(3 − 2, 4)."),
        Q(3, "Tiga gaya bekerja pada satu titik: " + col(4, 1) + " N, " + col(-1, 3) + " N, dan " + vec("F") + ". Tentukan " + vec("F") + " agar titik itu setimbang, dan besarnya.", col(-3, -4) + " N; 5 N", "Jumlah ketiga gaya harus " + col(0, 0) + "."),
        Q(3, "ABCD jajargenjang dengan A(1, 1), B(5, 2), dan D(2, 4). Tentukan koordinat C.", "C(6, 5)", vec("AC") + " = " + vec("AB") + " + " + vec("AD") + " = " + col(4, 1) + " + " + col(1, 3) + "."),
    ],
))

# ================================================================== Subbab 3
SUB.append(dict(
    title="Vektor Posisi dan Pembagian Ruas Garis",
    tujuan="Memakai vektor posisi untuk menentukan titik yang membagi ruas garis, titik berat segitiga, dan memeriksa kesegarisan tiga titik.",
    konsep=[
        "<b>Vektor posisi</b> titik A adalah vektor dari titik asal O ke A, ditulis " + a_ + " = " + vec("OA") + ". Untuk A(x, y), " + a_ + " = " + col("x", "y") + ". Maka " + vec("AB") + " = " + b_ + " − " + a_ + ".",
        "Titik P pada ruas AB dengan <b>AP : PB = m : n</b> mempunyai vektor posisi " + vec("p") + " = (n" + a_ + " + m" + b_ + ") : (m + n). Perhatikan: m dipasangkan dengan " + b_ + ", bukan dengan " + a_ + ".",
        "Tiga titik A, B, C <b>segaris</b> (kolinear) bila " + vec("AB") + " = k" + vec("AC") + " untuk suatu k.",
    ],
    rumus=[vec("AB") + " = " + b_ + " − " + a_, "AP : PB = m : n ⟹ " + vec("p") + " = " + fr("n" + a_ + " + m" + b_, "m + n"), "Titik tengah: " + fr(a_ + " + " + b_, "2") + "; titik berat segitiga: " + fr(a_ + " + " + b_ + " + " + vec("c"), "3"),
           "A, B, C segaris ⟺ " + vec("AB") + " = k" + vec("AC")],
    contoh=[
        ("Membagi ruas garis", "Diketahui A(2, 1) dan B(8, 10). Tentukan P pada AB dengan AP : PB = 1 : 2.", None,
         [vec("p") + " = (2" + a_ + " + 1" + b_ + ") : 3.", "= " + col("(4 + 8) : 3", "(2 + 10) : 3") + " = " + col(4, 4) + "."], "P(4, 4)"),
        ("Segaris", "Apakah A(1, 2), B(3, 6), dan C(4, 8) segaris?", None, [vec("AB") + " = " + col(2, 4) + "; " + vec("AC") + " = " + col(3, 6) + ".", vec("AC") + " = 1,5 · " + vec("AB") + ", jadi segaris."], "segaris"),
    ],
    bertahap=dict(
        soal="Tentukan titik berat segitiga dengan titik sudut A(1, 1), B(7, 3), dan C(4, 8).",
        langkah=[a_ + " + " + b_ + " + " + vec("c") + " = " + col("____", "____") + ".", "Dibagi 3: " + col("____", "____") + "."],
        cek="Titik berat dihitung dengan rata-rata ketiga vektor posisi karena",
        opsi=["(a) titik berat membagi setiap garis berat dengan perbandingan 2 : 1", "(b) titik berat selalu di tengah sisi terpanjang"],
        kunci=col(12, 12) + "; " + col(4, 4) + ", jadi titik berat (4, 4). Alasan: (a).",
    ),
    jebakan=["Pada rumus pembagian, m (bagian dekat A) dipasangkan dengan " + b_ + ".", "AP : PB = 1 : 2 berarti P lebih dekat ke A.", "Segaris berarti satu vektor kelipatan yang lain, bukan sekadar panjangnya sama."],
    latihan=[
        Q(1, "Tentukan titik tengah ruas garis (2, 6) dan (8, 2).", "(5, 4)", "Rata-rata."), Q(1, "Tuliskan vektor posisi titik P(3, −2).", col(3, -2), "Koordinatnya."),
        Q(1, "Jika " + a_ + " = " + col(1, 5) + " dan " + b_ + " = " + col(4, 1) + ", tentukan " + vec("AB") + ".", col(3, -4), b_ + " − " + a_ + "."),
        Q(1, "Tentukan titik berat segitiga (0, 0), (6, 0), dan (0, 9).", "(2, 3)", "(6 : 3, 9 : 3)."),
        Q(1, "P titik tengah AB dengan A(−2, 4) dan P(1, 1). Tentukan B.", "B(4, −2)", vec("b") + " = 2" + vec("p") + " − " + a_ + "."),
        Q(2, "P pada AB dengan AP : PB = 2 : 1, A(1, 1), B(7, 4). Tentukan P.", "P(5, 3)", "(1 · " + a_ + " + 2 · " + b_ + ") : 3."),
        Q(2, "Periksa apakah (1, 1), (3, 5), dan (4, 7) segaris.", "segaris", col(3, 6) + " = 1,5 · " + col(2, 4) + "."),
        Q(2, "Tentukan k agar (0, 1), (2, 5), dan (4, k) segaris.", "k = 9", "Komponen kedua harus 2 kali: " + col(4, "k − 1") + " = 2 · " + col(2, 4) + "."),
        Q(2, "P pada AB dengan AP : PB = 3 : 1, A(2, −1), B(6, 7). Tentukan P.", "P(5, 5)", "(1 · " + a_ + " + 3 · " + b_ + ") : 4."),
        Q(3, "Titik P(4, 3) terletak pada ruas A(1, 0)B(9, 8). Tentukan AP : PB.", "3 : 5", vec("AP") + " = " + col(3, 3) + ", " + vec("PB") + " = " + col(5, 5) + "."),
        Q(3, "ABCD jajargenjang dengan A(1, 2), B(5, 3), dan C(7, 7). Tentukan D dengan sifat bahwa diagonal-diagonalnya saling membagi dua.", "D(3, 6)", "Titik tengah AC = titik tengah BD: " + vec("d") + " = " + a_ + " + " + vec("c") + " − " + b_ + "."),
        Q(3, "Titik berat segitiga ABC adalah G(3, 3), dengan A(0, 0) dan B(6, 2). Tentukan C.", "C(3, 7)", vec("c") + " = 3" + vec("g") + " − " + a_ + " − " + b_ + "."),
    ],
))

# ================================================================== Subbab 4
F41 = plane((-1, 5, 1), (-4, 5, 1), arrows=[(0, 0, 3, 4, BLUE, "a"), (0, 0, 4, -3, RED, "b")])
SUB.append(dict(
    title="Hasil Kali Titik dan Sudut Antarvektor",
    tujuan="Menghitung hasil kali titik (skalar) dua vektor, menentukan sudut antara dua vektor, dan memeriksa ketegaklurusan.",
    konsep=[
        "<b>Hasil kali titik</b> " + a_ + " · " + b_ + " menghasilkan sebuah bilangan (skalar), bukan vektor. Dengan komponen: a₁b₁ + a₂b₂. Secara geometris: |" + a_ + "||" + b_ + "| cos θ, dengan θ sudut antara kedua vektor (0° ≤ θ ≤ 180°).",
        "Menyamakan kedua bentuk memberi cara menghitung sudut: cos θ = " + a_ + " · " + b_ + " : (|" + a_ + "||" + b_ + "|).",
        "Tanda hasil kali titik menunjukkan jenis sudut: positif (lancip), nol (<b>tegak lurus</b>), negatif (tumpul). Juga " + a_ + " · " + a_ + " = |" + a_ + "|².",
    ],
    rumus=[a_ + " · " + b_ + " = a₁b₁ + a₂b₂ = |" + a_ + "||" + b_ + "| cos θ", "cos θ = " + fr(a_ + " · " + b_, "|" + a_ + "| |" + b_ + "|"), a_ + " ⊥ " + b_ + " ⟺ " + a_ + " · " + b_ + " = 0",
           "|" + a_ + " + " + b_ + "|² = |" + a_ + "|² + |" + b_ + "|² + 2" + a_ + " · " + b_],
    contoh=[
        ("Tegak lurus", "Tunjukkan bahwa " + a_ + " = " + col(3, 4) + " dan " + b_ + " = " + col(4, -3) + " saling tegak lurus.", F41, [a_ + " · " + b_ + " = 3 · 4 + 4 · (−3) = 0.", "Hasil kali titik nol, jadi tegak lurus."], "tegak lurus"),
        ("Sudut", "Tentukan sudut antara " + col(1, 0) + " dan " + col(1, 1) + ".", None, ["Hasil kali titik = 1; panjangnya 1 dan √2.", "cos θ = 1/√2 → θ = 45°."], "45°"),
    ],
    bertahap=dict(
        soal="Tentukan sudut antara " + a_ + " = " + col(2, 1) + " dan " + b_ + " = " + col(1, 3) + ".",
        langkah=[a_ + " · " + b_ + " = 2 · 1 + 1 · 3 = ____.", "|" + a_ + "| = √____; |" + b_ + "| = √____.", "cos θ = ____ : √50 = ____ → θ = ____°."],
        cek="Sudut ini lancip karena",
        opsi=["(a) hasil kali titiknya positif", "(b) kedua vektor berada di kuadran I"],
        kunci="5; √5 dan √10; cos θ = 5 : √50 = 1/√2, θ = 45°. Alasan: (a).",
    ),
    jebakan=["Hasil kali titik adalah bilangan, bukan vektor.", "Sudut antarvektor diukur dengan pangkal kedua vektor disatukan.", "Hasil kali titik nol tidak berarti salah satu vektor nol; bisa jadi keduanya tegak lurus."],
    latihan=[
        Q(1, "Hitung " + col(2, 3) + " · " + col(4, 1) + ".", "11", "8 + 3."), Q(1, "Apakah " + col(1, -2) + " dan " + col(2, 1) + " tegak lurus?", "ya", "2 − 2 = 0."),
        Q(1, "Hitung " + a_ + " · " + a_ + " untuk " + a_ + " = " + col(3, 4) + ".", "25", "|" + a_ + "|²."), Q(1, "|" + a_ + "| = 4, |" + b_ + "| = 5, sudut antaranya 60°. Hitung " + a_ + " · " + b_ + ".", "10", "4 · 5 · ½."),
        Q(1, "Bila sudut antara dua vektor tumpul, apa tanda hasil kali titiknya?", "negatif", "cos θ &lt; 0."),
        Q(2, "Tentukan sudut antara " + col(1, 1) + " dan " + col(-1, 1) + ".", "90°", "Hasil kali titik 0."),
        Q(2, "Tentukan p agar " + col("p", 2) + " tegak lurus " + col(3, -6) + ".", "p = 4", "3p − 12 = 0."),
        Q(2, "Tentukan sudut antara " + col(3, 0) + " dan " + col(1, "√3") + ".", "60°", "cos θ = 3 : (3 · 2) = ½."),
        Q(2, "|" + a_ + "| = 3, |" + b_ + "| = 4, dan |" + a_ + " + " + b_ + "| = 5. Tentukan sudut antara " + a_ + " dan " + b_ + ".", "90°", "25 = 9 + 16 + 2" + a_ + " · " + b_ + " → " + a_ + " · " + b_ + " = 0."),
        Q(3, "|" + a_ + "| = 2, |" + b_ + "| = 3, dan sudut antaranya 60°. Hitung |" + a_ + " + " + b_ + "|.", "√19", "4 + 9 + 2 · 3 = 19."),
        Q(3, "Pada segitiga A(0, 0), B(4, 0), C(2, 2), tentukan besar sudut BAC dengan hasil kali titik.", "45°", vec("AB") + " · " + vec("AC") + " = 8; 8 : (4 · 2√2) = 1/√2."),
        Q(3, "Buktikan bahwa diagonal-diagonal belah ketupat saling tegak lurus. (Petunjuk: sisi-sisinya " + a_ + " dan " + b_ + " dengan |" + a_ + "| = |" + b_ + "|.)", "(" + a_ + " + " + b_ + ") · (" + a_ + " − " + b_ + ") = 0",
          "(" + a_ + " + " + b_ + ") · (" + a_ + " − " + b_ + ") = |" + a_ + "|² − |" + b_ + "|² = 0."),
    ],
))

# ================================================================== Subbab 5
F51 = plane((0, 5, 1), (0, 4, 1), arrows=[(0, 0, 4, 3, BLUE, "a"), (0, 0, 4, 0, GREEN, "")], segs=[(4, 3, 4, 0, RED, True)], labels=[(1.6, -0.35, "proyeksi", GREEN)])
SUB.append(dict(
    title="Proyeksi Vektor dan Penerapannya",
    tujuan="Menghitung panjang proyeksi dan vektor proyeksi, lalu memakainya pada usaha, komponen gaya atau kecepatan, dan jarak.",
    konsep=[
        "<b>Proyeksi</b> " + a_ + " pada " + b_ + " adalah 'bayangan' " + a_ + " pada garis yang searah " + b_ + ", seperti bayangan tongkat ketika cahaya datang tegak lurus pada " + b_ + ".",
        "Panjang proyeksi (proyeksi skalar) adalah |" + a_ + "| cos θ = " + a_ + " · " + b_ + " : |" + b_ + "|; bisa negatif bila sudutnya tumpul. Vektor proyeksinya adalah panjang itu dikali vektor satuan searah " + b_ + ".",
        "Dalam fisika, <b>usaha</b> W = " + vec("F") + " · " + vec("s") + ": hanya komponen gaya yang searah perpindahan yang melakukan usaha.",
    ],
    rumus=["Panjang proyeksi " + a_ + " pada " + b_ + ": " + fr(a_ + " · " + b_, "|" + b_ + "|"), "Vektor proyeksi: " + fr(a_ + " · " + b_, "|" + b_ + "|²") + " " + b_, "Usaha: W = " + vec("F") + " · " + vec("s") + " = |F||s| cos θ"],
    contoh=[
        ("Proyeksi pada sumbu x", "Tentukan proyeksi " + a_ + " = " + col(4, 3) + " pada " + b_ + " = " + col(1, 0) + ".", F51,
         [a_ + " · " + b_ + " = 4; |" + b_ + "| = 1.", "Panjang proyeksi 4; vektor proyeksi " + col(4, 0) + "."], "4; " + col(4, 0)),
        ("Usaha", "Gaya " + vec("F") + " = " + col(10, 5) + " N memindahkan kotak sejauh " + vec("s") + " = " + col(6, 0) + " m. Berapa usahanya?", None, ["W = 10 · 6 + 5 · 0 = 60 J.", "Komponen tegak gaya tidak melakukan usaha."], "60 J"),
    ],
    bertahap=dict(
        soal="Tentukan panjang proyeksi dan vektor proyeksi " + a_ + " = " + col(5, 1) + " pada " + b_ + " = " + col(3, 4) + ".",
        langkah=[a_ + " · " + b_ + " = ____; |" + b_ + "| = ____.", "Panjang proyeksi = ____ : 5 = ____.", "Vektor proyeksi = (19 : 25) · " + col(3, 4) + " = " + col("____", "____") + "."],
        cek="Pada vektor proyeksi, pembaginya |" + b_ + "|² karena",
        opsi=["(a) panjang proyeksi dikali vektor satuan " + b_ + "/|" + b_ + "|", "(b) proyeksi selalu lebih pendek"],
        kunci="19; 5; 3,8; " + col("2,28", "3,04") + ". Alasan: (a).",
    ),
    jebakan=["Proyeksi " + a_ + " pada " + b_ + " berbeda dengan proyeksi " + b_ + " pada " + a_ + ".", "Panjang proyeksi bisa negatif (arah berlawanan dengan " + b_ + ").", "Usaha memakai komponen gaya yang searah perpindahan."],
    latihan=[
        Q(1, "Tentukan panjang proyeksi " + col(3, 4) + " pada " + col(1, 0) + ".", "3", "Komponen x."), Q(1, "Tentukan panjang proyeksi " + col(2, 5) + " pada " + col(0, 1) + ".", "5", "Komponen y."),
        Q(1, "Gaya " + col(3, 4) + " N memindahkan benda sejauh " + col(2, 0) + " m. Hitung usahanya.", "6 J", "3 · 2."),
        Q(1, "Berapa panjang proyeksi " + a_ + " pada " + b_ + " bila keduanya tegak lurus?", "0", a_ + " · " + b_ + " = 0."),
        Q(1, "Berapa panjang proyeksi " + a_ + " pada dirinya sendiri?", "|" + a_ + "|", "|" + a_ + "|² : |" + a_ + "|."),
        Q(2, "Tentukan panjang proyeksi " + col(2, 3) + " pada " + col(3, 4) + ".", "3,6", "18 : 5."),
        Q(2, "Tentukan vektor proyeksi " + col(2, 3) + " pada " + col(3, 4) + ".", col("2,16", "2,88"), "(18 : 25) · " + col(3, 4) + "."),
        Q(2, "Tali menarik peti dengan gaya 50 N yang membentuk sudut 37° terhadap lantai (sin 37° = 0,6; cos 37° = 0,8). Peti berpindah 10 m mendatar. Hitung usahanya.", "400 J", vec("F") + " = " + col(40, 30) + "; " + vec("s") + " = " + col(10, 0) + "."),
        Q(2, "Tentukan panjang proyeksi " + col(6, 2) + " pada " + col(1, -1) + ".", "2√2", "(6 − 2) : √2."),
        Q(3, "Tentukan jarak titik P(3, 4) ke garis yang melalui O(0, 0) dengan arah " + col(1, 1) + ".", "√2/2", "Proyeksi " + vec("OP") + " pada arah garis: 7/√2. Jarak = √(25 − 49/2) = √½."),
        Q(3, "Rute kapal searah " + col(4, 3) + ". Angin bertiup dengan kecepatan " + col(10, 0) + " km/jam. Berapa komponen kecepatan angin yang searah rute?", "8 km/jam", "40 : 5."),
        Q(3, "Gaya " + col(-2, 3) + " N bekerja pada benda yang berpindah " + col(4, 1) + " m. Hitung usahanya dan jelaskan artinya.", "−5 J; gaya itu menghambat gerak", "−8 + 3 = −5; sudutnya tumpul."),
    ],
))

CAMPURAN = [
    Q(1, "Hitung |" + col(-6, 8) + "|.", "10", "√100."), Q(1, "Hitung " + col(2, -1) + " + 3" + col(1, 2) + ".", col(5, 5), "(2 + 3, −1 + 6)."),
    Q(1, "Hitung " + col(1, 2) + " · " + col(4, -1) + ".", "2", "4 − 2."), Q(1, "Titik tengah (−3, 5) dan (5, 1)?", "(1, 3)", "Rata-rata."),
    Q(2, "Tentukan sudut antara " + col(2, 0) + " dan " + col(-1, 1) + ".", "135°", "cos θ = −2 : (2√2) = −½√2."), Q(2, "Tentukan k agar " + col("k", 4) + " ∥ " + col(3, 6) + ".", "k = 2", col(2, 4) + " = ⅔ · " + col(3, 6) + "."),
    Q(2, "Tentukan k agar " + col("k", 4) + " ⊥ " + col(3, 6) + ".", "k = −8", "3k + 24 = 0."), Q(2, "P pada AB, AP : PB = 1 : 3, A(0, 0), B(8, 4). Tentukan P.", "P(2, 1)", "(3 · " + a_ + " + 1 · " + b_ + ") : 4."),
    Q(2, "Panjang proyeksi " + col(4, 2) + " pada " + col(3, 4) + "?", "4", "20 : 5."),
    Q(3, "Diketahui |" + a_ + "| = |" + b_ + "| = 5 dan |" + a_ + " − " + b_ + "| = 5. Tentukan sudut antara " + a_ + " dan " + b_ + ".", "60°", "25 = 25 + 25 − 2" + a_ + " · " + b_ + " → " + a_ + " · " + b_ + " = 12,5; cos θ = ½."),
]

FK = plane((-1, 8, 1), (-4, 5, 1), arrows=[(0, 0, 3, 4, BLUE, "a"), (3, 4, 7, 1, RED, "b"), (0, 0, 7, 1, GREEN, "c")])
TKA = [
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Diketahui " + a_ + " = " + col(2, -1) + " dan " + b_ + " = " + col(1, 3) + ". Vektor 2" + a_ + " + " + b_ + " adalah ....",
         opsi=[col(5, 1), col(3, 2), col(5, 5), col(4, 1), col(5, -5)], kunci=0, bahas="(4 + 1, −2 + 3).", salah="B: " + a_ + " + " + b_ + ". C: tanda −2 menjadi +2. D: 2 · 2 tanpa + 1. E: 2 · (−1) − 3."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Diketahui A(1, 2) dan B(m, 10). Jika panjang vektor " + vec("AB") + " adalah 10 satuan, nilai m yang memenuhi adalah ....",
         opsi=["7 atau −5", "−7 atau 5", "7 atau 5", "6 atau −6", "9 atau −7"], kunci=0, bahas="(m − 1)² + 8² = 100 → m − 1 = ±6.", salah="B: tanda kedua akar terbalik. C: akar −6 diberi tanda +. D: lupa −1. E: memakai (m − 1)² = 64."),
    dict(tipe="MAT-UKUR", lv=2, fmt="pg", soal="Sebuah drone terbang 6 km ke timur lalu 8 km ke utara. Jarak drone dari titik awal dan arahnya dari titik awal adalah .... (tan 53° ≈ 4/3)",
         opsi=["10 km, 53° dari arah timur ke utara", "14 km, 53° dari arah timur ke utara", "10 km, 37° dari arah timur ke utara", "10 km, 53° dari arah utara ke timur", "2 km, ke arah utara"], kunci=0,
         bahas="|" + col(6, 8) + "| = 10; tan θ = 8/6 → θ ≈ 53° dari timur.", salah="B: komponen dijumlahkan. C: sudut tertukar. D: sudut diukur dari utara. E: 8 − 6."),
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Perhatikan vektor " + a_ + ", " + b_ + ", dan " + vec("c") + " pada grid berikut.", fig=FK, soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=[vec("c") + " = " + a_ + " + " + b_, "|" + a_ + "| = 5", a_ + " tegak lurus " + b_, b_ + " = −" + a_, "|" + vec("c") + "| = 7"], kunci=[0, 1, 2],
         bahas=a_ + " = " + col(3, 4) + ", " + b_ + " = " + col(4, -3) + ", " + vec("c") + " = " + col(7, 1) + ". " + a_ + " · " + b_ + " = 0.", salah="D: " + b_ + " tidak berlawanan arah dengan " + a_ + ". E: |" + vec("c") + "| = √50."),
    dict(tipe="MAT-MODEL", lv=2, fmt="pg", soal="Robot di gudang menerima perintah berurutan: " + col(3, 2) + ", " + col(-1, 4) + ", lalu 2 · " + col(1, -1) + " (satuan meter). Robot mula-mula di (0, 0). Posisi akhirnya adalah ....",
         opsi=["(4, 4)", "(3, 5)", "(4, 6)", "(2, 8)", "(5, 4)"], kunci=0, bahas="(3 − 1 + 2, 2 + 4 − 2).", salah="B: perintah ketiga tidak dikali 2. C: perintah ketiga diabaikan. D, E: salah menjumlah."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Diketahui " + a_ + " = " + col("p", 2) + " dan " + b_ + " = " + col(3, -6) + ". Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=[a_ + " ⊥ " + b_ + " bila p = 4.", a_ + " ∥ " + b_ + " bila p = −1.", "|" + b_ + "| = 3√5.", a_ + " · " + b_ + " = 3p + 12."], kunci=[True, True, True, False],
         bahas="3p − 12 = 0 → p = 4; " + col(-1, 2) + " = −⅓" + b_ + "; √45 = 3√5; " + a_ + " · " + b_ + " = 3p − 12.", salah=""),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Besar sudut antara vektor " + col(1, "√3") + " dan " + col("√3", 1) + " adalah ....",
         opsi=["30°", "60°", "45°", "90°", "0°"], kunci=0, bahas="Hasil kali titik 2√3; panjang keduanya 2; cos θ = √3/2.", salah="B: cos θ dibaca ½. C, D, E: tidak sesuai."),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg", soal="Rafi menarik koper sejauh 8 m di lantai datar dengan gaya 50 N. Ia ingin usahanya paling sedikit 300 J, tetapi tali yang lebih tegak terasa lebih nyaman. Sudut tali terhadap lantai yang paling besar namun masih memenuhi syarat adalah .... (cos 30° ≈ 0,87; cos 37° = 0,8; cos 45° ≈ 0,71; cos 53° = 0,6; cos 60° = 0,5)",
         opsi=["37°", "30°", "45°", "53°", "60°"], kunci=0, bahas="W = 400 cos θ ≥ 300 → cos θ ≥ 0,75. 30°: 348 J; 37°: 320 J; 45°: 283 J. Sudut terbesar yang memenuhi: 37°.",
         salah="B: memenuhi, tetapi bukan sudut terbesar. C: 283 J &lt; 300 J. D: 240 J. E: 200 J."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Diketahui |" + a_ + "| = |" + b_ + "| = 1 dan " + a_ + " · " + b_ + " = 0. Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["|" + a_ + " + " + b_ + "| = √2", "(" + a_ + " + " + b_ + ") · (" + a_ + " − " + b_ + ") = 0", a_ + " = " + b_, "|" + a_ + " − " + b_ + "| = 0", a_ + " + " + b_ + " membentuk sudut 45° dengan " + a_],
         kunci=[0, 1, 4], bahas="|" + a_ + " + " + b_ + "|² = 1 + 1 + 0; (" + a_ + " + " + b_ + ") · (" + a_ + " − " + b_ + ") = 1 − 1; cos θ = (" + a_ + " + " + b_ + ") · " + a_ + " : √2 = 1/√2.",
         salah="C, D: dua vektor tegak lurus tidak mungkin sama; |" + a_ + " − " + b_ + "| = √2."),
    dict(tipe="MAT-UKUR", lv=2, fmt="pg", soal="Panjang proyeksi vektor " + col(4, 2) + " pada vektor " + col(3, 4) + " adalah ....",
         opsi=["4", "20", "2√5", "0,8", "16/5"], kunci=0, bahas="(12 + 8) : 5.", salah="B: tanpa dibagi panjang. C: panjang " + col(4, 2) + ". D: dibagi 25. E: tidak sesuai."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Panjang vektor " + col(-6, 8) + " adalah ....", ["10", "2", "14", "100", "√28"], 0, "√100.", "B: −6 + 8. C: 6 + 8. D: lupa akar. E: tidak sesuai."),
    ("Diketahui A(2, 3) dan B(5, −1). Vektor " + vec("AB") + " adalah ....", [col(3, -4), col(-3, 4), col(7, 2), col(3, 4), col(10, -3)], 0, "(5 − 2, −1 − 3).", "B: " + vec("BA") + ". C: dijumlahkan. D: tanda salah. E: dikalikan."),
    (col(2, 1) + " + " + col(-4, 3) + " = ....", [col(-2, 4), col(6, 4), col(-2, 2), col(2, -4), col(-8, 3)], 0, "Komponen dijumlah.", "B, C, D, E: salah tanda atau operasi."),
    ("3" + col(2, -1) + " − " + col(1, 4) + " = ....", [col(5, -7), col(7, -7), col(5, 1), col(5, -1), col(6, -7)], 0, "(6 − 1, −3 − 4).", "B, C, D, E: salah tanda atau lupa dikali 3."),
    ("Vektor satuan searah " + col(0, -5) + " adalah ....", [col(0, -1), col(0, 1), col(0, -5), col(-1, 0), col(1, -1)], 0, "Dibagi 5.", "B: arah terbalik. C: belum dibagi. D, E: tidak sesuai."),
    ("Titik tengah ruas garis (−2, 6) dan (4, 0) adalah ....", ["(1, 3)", "(3, 3)", "(2, 6)", "(1, 6)", "(−3, 3)"], 0, "Rata-rata.", "B: selisih dibagi 2. C, D, E: tidak sesuai."),
    (col(3, -2) + " · " + col(4, 5) + " = ....", ["2", "22", "−2", col(12, -10), "12"], 0, "12 − 10.", "B: tanda diabaikan. C: tanda salah. D: hasil kali titik ditulis sebagai vektor. E: satu suku saja."),
    ("Nilai p agar " + col(2, "p") + " tegak lurus " + col(3, 6) + " adalah ....", ["−1", "1", "4", "−4", "9"], 0, "6 + 6p = 0.", "B: tanda salah. C, D, E: tidak sesuai."),
    ("Sudut antara " + col(1, 0) + " dan " + col(0, -3) + " adalah ....", ["90°", "0°", "180°", "45°", "270°"], 0, "Hasil kali titik 0.", "B, C, D, E: tidak sesuai."),
    ("|" + a_ + "| = 2, |" + b_ + "| = 6, sudut antaranya 60°. Nilai " + a_ + " · " + b_ + " adalah ....", ["6", "12", "6√3", "3", "8"], 0, "2 · 6 · ½.", "B: tanpa cos. C: memakai sin. D, E: tidak sesuai."),
    ("Panjang proyeksi " + col(6, 8) + " pada " + col(0, 1) + " adalah ....", ["8", "6", "10", "48", "14"], 0, "Komponen y.", "B: komponen x. C: panjang vektor. D, E: tidak sesuai."),
    ("Nilai k agar " + col("k", 6) + " sejajar " + col(2, 3) + " adalah ....", ["4", "9", "−4", "3", "12"], 0, col(4, 6) + " = 2 · " + col(2, 3) + ".", "B: syarat tegak lurus tidak dipakai di sini; 9 tidak sesuai. C: tanda salah. D, E: tidak sesuai."),
    ("Titik berat segitiga (0, 0), (3, 6), dan (6, 3) adalah ....", ["(3, 3)", "(9, 9)", "(4,5; 4,5)", "(2, 2)", "(1, 1)"], 0, "(9 : 3, 9 : 3).", "B: belum dibagi 3. C: dibagi 2. D, E: tidak sesuai."),
    ("Gaya " + col(5, 2) + " N memindahkan benda sejauh " + col(3, 1) + " m. Usahanya adalah ....", ["17 J", "15 J", "13 J", "21 J", "√29 J"], 0, "15 + 2.", "B: komponen x saja. C, D, E: tidak sesuai."),
    ("P pada AB dengan AP : PB = 1 : 3, A(0, 0), B(8, 4). Koordinat P adalah ....", ["(2, 1)", "(6, 3)", "(4, 2)", "(8/3, 4/3)", "(3, 1)"], 0, "(3" + a_ + " + " + b_ + ") : 4.", "B: m dan n tertukar. C: titik tengah. D: dibagi 3. E: tidak sesuai."),
]
UJI_URAIAN = [
    ("Diketahui A(1, 2), B(4, 6), dan C(7, 2). Hitung panjang ketiga sisi segitiga ABC dengan vektor, lalu tentukan jenis segitiganya dan kelilingnya.", "5, 5, 6; segitiga sama kaki; keliling 16", "|AB| = |BC| = 5, |AC| = 6."),
    ("Diketahui " + a_ + " = " + col(1, 2) + " dan " + b_ + " = " + col(3, -1) + ". Hitung " + a_ + " + " + b_ + ", 2" + a_ + " − " + b_ + ", |" + a_ + " + " + b_ + "|, dan " + a_ + " · " + b_ + ".", col(4, 1) + "; " + col(-1, 5) + "; √17; 1", "Operasi per komponen."),
    ("Tunjukkan bahwa A(1, 1), B(3, 4), dan C(7, 10) segaris, lalu tentukan AB : BC.", "segaris; 1 : 2", vec("AB") + " = " + col(2, 3) + ", " + vec("BC") + " = " + col(4, 6) + " = 2" + vec("AB") + "."),
    ("Tentukan sudut antara " + col(2, 1) + " dan " + col(1, 3) + ", lengkap dengan langkahnya.", "45°", "5 : (√5 · √10) = 1/√2."),
    ("Gaya 100 N membentuk sudut 60° terhadap arah perpindahan sejauh 20 m. Hitung usahanya, lalu jelaskan hubungannya dengan proyeksi vektor.", "1.000 J", "W = 100 · 20 · ½; hanya proyeksi gaya pada arah perpindahan (50 N) yang melakukan usaha."),
]

META = dict(
    title="Modul Vektor dan Operasinya", kick="Modul belajar Matematika · Fase E · Kelas X", big="Vektor dan Operasinya",
    subtitle="Notasi dan besar vektor, operasi vektor, vektor posisi dan pembagian ruas garis, hasil kali titik, sudut, serta proyeksi dan penerapannya",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat menyatakan vektor dalam berbagai bentuk, melakukan operasi vektor, menentukan hasil kali titik, sudut, dan proyeksi, serta memakai vektor untuk menyelesaikan masalah geometri dan kehidupan sehari-hari, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Hubungan dengan modul Fisika</h2><p>Modul Fisika <i>Vektor dan Gerak</i> memakai vektor untuk perpindahan dan kecepatan; modul ini membahasnya sebagai objek matematika.</p>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Gambarlah vektornya di kertas berpetak</b> bila ragu: hampir semua soal dapat dicek dengan gambar.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b>",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Vektor ditulis tebal (" + a_ + ") atau dengan dua huruf titik (" + vec("AB") + "). Vektor pada bidang ditulis sebagai vektor kolom " + col("x", "y") + "; " + vec("i") + " = " + col(1, 0) + " dan " + vec("j") + " = " + col(0, 1) + ". Sudut antarvektor 0° sampai 180°. Desimal ditulis dengan koma.",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>yang dicari vektor, panjang, titik, sudut, atau proyeksi?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025, yang memuat vektor (misalnya menentukan parameter dari panjang vektor).",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-MODEL, MAT-UKUR): mengenali, menghitung, bekerja mundur, memodelkan, atau mengukur. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Apa beda " + vec("AB") + " dan " + vec("BA") + "?", "Bagaimana hasil kali titik memberi tahu apakah dua vektor tegak lurus?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Vektor dua titik</th><td>" + vec("AB") + " = " + b_ + " − " + a_ + "</td></tr>"
        "<tr><th>Panjang</th><td>|" + col("x", "y") + "| = √(x² + y²); vektor satuan " + a_ + "/|" + a_ + "|</td></tr>"
        "<tr><th>Operasi</th><td>dijumlah/dikurangi per komponen; k" + a_ + " mengalikan setiap komponen</td></tr>"
        "<tr><th>Sejajar</th><td>" + a_ + " = k" + b_ + "</td></tr>"
        "<tr><th>Pembagian ruas</th><td>AP : PB = m : n ⟹ " + vec("p") + " = (n" + a_ + " + m" + b_ + ")/(m + n); titik berat (" + a_ + " + " + b_ + " + " + vec("c") + ")/3</td></tr>"
        "<tr><th>Hasil kali titik</th><td>" + a_ + " · " + b_ + " = a₁b₁ + a₂b₂ = |" + a_ + "||" + b_ + "| cos θ; tegak lurus ⟺ " + a_ + " · " + b_ + " = 0</td></tr>"
        "<tr><th>Proyeksi " + a_ + " pada " + b_ + "</th><td>panjang " + a_ + " · " + b_ + "/|" + b_ + "|; vektor (" + a_ + " · " + b_ + "/|" + b_ + "|²)" + b_ + "</td></tr>"
        "<tr><th>Usaha</th><td>W = " + vec("F") + " · " + vec("s") + "</td></tr></table>"
        '<div class="two"><div>' + F21 + "</div><div>" + F51 + "</div></div>"),
    jebakan5=[vec("AB") + " = posisi B − posisi A.", "|" + a_ + " + " + b_ + "| ≠ |" + a_ + "| + |" + b_ + "|.", "Hasil kali titik adalah bilangan, bukan vektor.",
              "Pada pembagian ruas AP : PB = m : n, m dipasangkan dengan " + b_ + ".", "Proyeksi " + a_ + " pada " + b_ + " ≠ proyeksi " + b_ + " pada " + a_ + "."],
    guru=["Materi mengikuti Kurikulum Merdeka Matematika SMA Fase E (bab Vektor dan Operasinya pada buku kelas X); modul ini membatasi diri pada vektor di bidang (dua dimensi).",
          "Proyeksi dan usaha dipakai sebagai penerapan; untuk kelas yang belum membahas proyeksi, Subbab 5 dapat dilewati.",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


def check():
    c = close
    # subbab 1
    assert sub((4, 6), (1, 2)) == (3, 4); c(norm((3, 4)), 5); c(norm((6, -8)), 10); c(norm((-5, 12)), 13); c(norm((2, -1)), math.sqrt(5))
    assert sub((5, 5), (2, 1)) == (3, 4) and sub((4, 3), (1, 1)) == (3, 2); c(norm(sub((4, -5), (-2, 3))), 10); c(norm((3, 4)) + 4 + 3, 12)
    assert 3 ** 2 + 16 == 25 and norm((10, 24)) == 26
    # subbab 2
    a, b = (4, 1), (2, 3)
    assert add(a, b) == (6, 4) and sub(a, b) == (2, -2) and sub(mul(3, a), mul(2, b)) == (8, -3)
    assert add((1, 4), (3, -2)) == (4, 2) and sub((5, 3), (2, 7)) == (3, -4) and mul(4, (-1, 2)) == (-4, 8)
    assert sub(mul(2, (3, 1)), mul(3, (1, -2))) == (3, 8); c(norm(add((1, 2), (2, 2))), 5); c(norm((1, 2)) + norm((2, 2)), 5.06, 0.01)
    assert (1 + 3 * 2, 2 * 1 + 2) == (7, 4); c(norm((1, 4)), 4.12, 0.01); assert add(add((4, 1), (-1, 3)), (-3, -4)) == (0, 0)
    assert add((5, 2), (2, 4)) == (7, 6) and add((1, 1), add(sub((5, 2), (1, 1)), sub((2, 4), (1, 1)))) == (6, 5)
    # subbab 3
    assert ((2 * 2 + 8) / 3, (2 * 1 + 10) / 3) == (4, 4) and ((1 + 7 + 4) / 3, (1 + 3 + 8) / 3) == (4, 4)
    assert ((1 + 14) / 3, (1 + 8) / 3) == (5, 3) and ((2 + 18) / 4, (-1 + 21) / 4) == (5, 5) and (2 * 1 - (-2), 2 * 1 - 4) == (4, -2)
    assert (3, 6) == mul(1.5, (2, 4)) and 1 + 2 * 4 == 9 and add((1, 2), sub((7, 7), (5, 3))) == (3, 6) and sub(sub(mul(3, (3, 3)), (0, 0)), (6, 2)) == (3, 7)
    # subbab 4
    assert dot((3, 4), (4, -3)) == 0 and dot((2, 3), (4, 1)) == 11 and dot((1, -2), (2, 1)) == 0
    c(angle((1, 0), (1, 1)), 45); c(angle((2, 1), (1, 3)), 45); c(angle((1, 1), (-1, 1)), 90); c(angle((3, 0), (1, math.sqrt(3))), 60)
    c(math.sqrt(4 + 9 + 2 * 3), math.sqrt(19)); c(angle((4, 0), (2, 2)), 45); c(angle((2, 0), (-1, 1)), 135)
    # subbab 5
    c(dot((5, 1), (3, 4)) / 5, 3.8); c(19 / 25 * 3, 2.28); c(19 / 25 * 4, 3.04); c(dot((2, 3), (3, 4)) / 5, 3.6); c(18 / 25 * 3, 2.16); c(18 / 25 * 4, 2.88)
    c(dot((40, 30), (10, 0)), 400); c(dot((6, 2), (1, -1)) / math.sqrt(2), 2 * math.sqrt(2)); c(math.sqrt(25 - 49 / 2), math.sqrt(0.5)); c(dot((10, 0), (4, 3)) / 5, 8); c(dot((-2, 3), (4, 1)), -5)
    # campuran, TKA, uji
    assert add(mul(2, (2, -1)), (1, 3)) == (5, 1) and add(add((3, 2), (-1, 4)), mul(2, (1, -1))) == (4, 4) and dot((3, 4), (4, -3)) == 0
    assert all((m - 1) ** 2 + 64 == 100 for m in (7, -5)); c(angle((1, math.sqrt(3)), (math.sqrt(3), 1)), 30)
    W = {d: 400 * math.cos(math.radians(d)) for d in (30, 37, 45, 53, 60)}
    assert W[37] >= 300 > W[45] and W[30] >= 300; c(dot((4, 2), (3, 4)) / 5, 4)
    c(angle(add((1, 0), (0, 1)), (1, 0)), 45); assert dot((5, 2), (3, 1)) == 17 and ((3 * 0 + 8) / 4, (3 * 0 + 4) / 4) == (2, 1)
    assert dot((3, -2), (4, 5)) == 2 and 6 + 6 * -1 == 0; c(angle((1, 0), (0, -3)), 90)
    c(norm(sub((4, 6), (1, 2))), 5); c(norm(sub((7, 2), (4, 6))), 5); c(norm(sub((7, 2), (1, 2))), 6); c(100 * 20 * 0.5, 1000)
    return True
