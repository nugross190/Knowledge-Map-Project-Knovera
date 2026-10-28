"""Content of the printable bridge sequence "Jembatan ke Gerak Lurus" (Fisika kelas X).

DRAFT of an among sequence (mode `masuk`): four steps (0–3) that bring a class with weak
prerequisites to the point where the Gerak Lurus module becomes usable, plus a praxis card
that collects the students' own motion cases for the follow-on case-analysis sequence.

Theme: a fishing trip from the beach (the reference class's theme). Prices, distances and
times are illustrative round numbers, not local data; the teacher replaces them with the
students' own reports. Every numeric answer is derived by the helpers below and re-checked
in check().
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import plane  # noqa: E402
from kit import n, fr  # noqa: E402

BLUE, RED, GREEN = "#1f3a68", "#c0502a", "#2e6b32"


# ------------------------------------------------------------------ physics helpers
def rate(amount, per):
    """'amount per one unit of per' as an exact fraction."""
    return F(amount, per)


def jarak(path):
    """Distance along a path of positions on a line: the sum of the lengths of every leg."""
    return sum(abs(b - a) for a, b in zip(path, path[1:]))


def perpindahan(path):
    """Displacement: final position minus initial position."""
    return path[-1] - path[0]


def slopes(pts):
    """Velocity of each straight piece of an x–t graph given its corner points."""
    return [F(x2 - x1, t2 - t1) for (t1, x1), (t2, x2) in zip(pts, pts[1:])]


def xt(pts, t_max=6, x_max=14, x_step=2, color=BLUE, w=300, h=190, labels=()):
    """An x–t graph (t in jam, x in km) made of straight pieces through grid points."""
    segs = [(t1, x1, t2, x2, color, False) for (t1, x1), (t2, x2) in zip(pts, pts[1:])]
    marks = [(t, x, "") for t, x in pts]
    return plane((0, t_max, 1), (0, x_max, x_step), segs=segs, points=marks, labels=labels,
                 width=w, height=h, xlabel="t (jam)", ylabel="x (km)")


def numberline(lo, hi, path=(), w=330):
    """Beach (0) to sea (+) number line in km; path is drawn as arrows above the line."""
    L, R = 22, 22
    W = w - L - R
    X = lambda x: L + W * (x - lo) / (hi - lo)
    rows = max(1, len(path) - 1)
    h = 46 + 14 * rows
    base = h - 22
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,DejaVu Sans,sans-serif">',
         '<defs><marker id="nl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>',
         f'<line x1="{L-8}" y1="{base}" x2="{L+W+10}" y2="{base}" stroke="#1f2430" stroke-width="1.3" marker-end="url(#nl)"/>']
    for k in range(lo, hi + 1):
        s.append(f'<line x1="{X(k):.1f}" y1="{base-3}" x2="{X(k):.1f}" y2="{base+3}" stroke="#1f2430"/>')
        s.append(f'<text x="{X(k):.1f}" y="{base+13}" font-size="8" text-anchor="middle" fill="#4b5260">{n(k)}</text>')
    s.append(f'<text x="{X(0):.1f}" y="{base-6}" font-size="7.5" text-anchor="middle" fill="{GREEN}" font-weight="700">pantai</text>')
    s.append(f'<text x="{L+W+8}" y="{base-6}" font-size="7.5" text-anchor="end" fill="{BLUE}" font-weight="700">ke laut (+)</text>')
    for k, (a, b) in enumerate(zip(path, path[1:])):
        y = 12 + 14 * k
        s.append(f'<line x1="{X(a):.1f}" y1="{y}" x2="{X(b):.1f}" y2="{y}" stroke="{RED}" stroke-width="2" marker-end="url(#nl)"/>')
        s.append(f'<circle cx="{X(a):.1f}" cy="{y}" r="2.2" fill="{RED}"/>')
    s.append("</svg>")
    return "".join(s)


def blank_xt(t_max=6, x_max=14, x_step=2):
    return plane((0, t_max, 1), (0, x_max, x_step), width=300, height=190, xlabel="t (jam)", ylabel="x (km)")


# ------------------------------------------------------------------ numbers used in the booklet
# Step 0: price per kg and km per jam
HARGA_A = (60000, 3)          # rupiah, kg
HARGA_B = (90000, 5)
BERSAMA0 = (24, 3)            # km, jam
SENDIRI0 = [(20, 4), (600, 5)]
PERAHU_A, PERAHU_B = (15, 3), (16, 4)
UJI0 = (18, 3)

# Step 1: paths on the beach–sea line (km, or m for the tape walk)
LIHAT1 = [0, 6, 2]
BERSAMA1 = [2, 8, 5]
SENDIRI1 = [[0, 6, 0], [4, 1], [0, 4, -2]]
UJI1 = [0, 5, 3]

# Step 2: (path, time in jam)
LIHAT2 = ([0, 12, 12, 0], 2 + 2 + 2)
BERSAMA2 = ([0, 10], 2)
SENDIRI2 = [([0, 3], 1), ([0, 9, 6], 2 + 1), ([0, 8], 2)]
SENDIRI2_B = ([0, 8], 4)
UJI2 = ([0, 10, 0], 2 + 2)

# Step 3: x–t corner points (t in jam, x in km)
TRIP = [(0, 0), (2, 12), (4, 12), (6, 0)]
SENDIRI3 = [(0, 0), (2, 8), (3, 8), (4, 0)]
UJI3 = [(0, 0), (1, 6), (3, 6), (4, 0)]
COCOK = {   # graph letter -> (corner points, story number)
    "A": ([(0, 0), (2, 8), (4, 8)], 3),
    "B": ([(0, 4), (4, 4)], 1),
    "C": ([(0, 0), (4, 8)], 4),
    "D": ([(0, 8), (4, 0)], 2),
}
CERITA = [
    "Perahu berlabuh di rumpon, 4 km dari pantai, dan tidak bergerak.",
    "Perahu pulang ke pantai dengan laju tetap.",
    "Perahu berangkat ke laut, lalu berhenti untuk memancing.",
    "Perahu berangkat ke laut dengan laju tetap dan terus berlayar.",
]


def rp(x):
    return "Rp" + n(x)


# ------------------------------------------------------------------ figures
FIG_NL_LIHAT = numberline(-1, 8, LIHAT1)
FIG_NL_BERSAMA = numberline(-1, 9, BERSAMA1)
FIG_NL_KOSONG = numberline(-3, 8)
FIG_TRIP = xt(TRIP)
FIG_SENDIRI3 = xt(SENDIRI3, t_max=5, x_max=10)
FIG_COCOK = {k: xt(p, t_max=4, x_max=10, w=200, h=140) for k, (p, _) in COCOK.items()}
FIG_BLANK = blank_xt(t_max=5, x_max=8)
FIG_UJI3 = xt(UJI3, t_max=5, x_max=8)


def ratio_table(rows, head=("Banyaknya", "Jumlah")):
    """A two-column ratio table; rows are (left, right) strings."""
    return ("<table class='rasio'><tr><th>" + head[0] + "</th><th>" + head[1] + "</th></tr>" +
            "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table>")


# ------------------------------------------------------------------ cek awal (diagnostic)
# (code, skill id, question, answer, note)
CEK = [
    ("P1", "tambah-kurang", "Hitung 7 + 5 dan 12 − 4.", "12 dan 8", ""),
    ("P2", "tambah-kurang", "Hitung 25 + 18 dan 40 − 13.", "43 dan 27", ""),
    ("P3", "cerita", "Perahu membawa 15 liter bensin. Selama perjalanan terpakai 6 liter. Berapa liter sisanya?", "9 liter", "Sisa: 15 − 6."),
    ("P4", "cerita", "Dimas berjalan 3 km, lalu 2 km lagi ke arah yang sama. Berapa km seluruhnya?", "5 km", "Searah: 3 + 2."),
    ("P5", "kali", "Hitung 4 × 6 dan 3 × 15.", "24 dan 45", ""),
    ("P6", "kali", "Satu keranjang berisi 8 kg ikan. Berapa kg isi 5 keranjang?", "40 kg", "8 × 5."),
    ("P7", "bagi", "Hitung 24 : 4 dan 90 : 5.", "6 dan 18", ""),
    ("P8", "bagi", "Tali 12 m dipotong menjadi 3 bagian sama panjang. Berapa panjang tiap bagian?", "4 m", "12 : 3."),
    ("P9", "per", "Harga ikan Rp20.000 per kg. Apa artinya? (a) 20.000 kg ikan berharga Rp1; (b) setiap 1 kg ikan berharga Rp20.000; (c) semua ikan berharga Rp20.000.", "(b)", "\"Per kg\" berarti untuk setiap 1 kg."),
    ("P10", "per", "Sebuah sepeda menempuh 10 km dalam 2 jam dengan laju tetap. Berapa km yang ditempuh dalam 1 jam?", "5 km", "10 : 2: \"tiap 1 jam\" berarti dibagi."),
    ("P11", "negatif", "Pada garis bilangan, mulai dari 5 lalu mundur 7 langkah. Di bilangan berapa kamu berhenti?", "−2", "5 − 7 = −2."),
    ("P12", "negatif", "Hitung 3 − 5 dan 2 − 8.", "−2 dan −6", ""),
]

SKILL = {   # skill id -> (name, items, where it is used, Kotak Ingat or step that bridges it)
    "tambah-kurang": ("Menjumlah dan mengurang", "P1, P2", "Langkah 1–3", "Langkah 1 memakainya langsung"),
    "cerita": ("Menjumlah dan mengurang dalam cerita", "P3, P4", "Langkah 1, 2", "Kotak Ingat A"),
    "kali": ("Perkalian", "P5, P6", "Langkah 0, 3", "Kalkulator boleh"),
    "bagi": ("Pembagian", "P7, P8", "Langkah 0, 2, 3", "Langkah 0, kalkulator boleh"),
    "per": ("Arti kata \"per\"", "P9, P10", "Langkah 0, 2, 3", "Langkah 0"),
    "negatif": ("Bilangan negatif", "P11, P12", "Langkah 1, 3", "Kotak Ingat B"),
}

INGAT = [
    ("A", "Dari cerita ke operasi", [
        "Baca ceritanya dulu, jangan langsung mencari angka.",
        "Tanyakan: apakah dua bagian <b>digabung</b> (jumlah), <b>diambil</b> (kurang), <b>diulang</b> beberapa kali (kali), atau <b>dibagi rata</b> (bagi)?",
        "Kata kunci bisa menipu. \"Sisa\" biasanya berarti kurang, tetapi bacalah situasinya, bukan katanya saja.",
    ]),
    ("B", "Bilangan negatif pada garis bilangan", [
        "Ke kanan berarti bertambah, ke kiri berarti berkurang. Melewati 0 ke kiri, bilangannya menjadi negatif.",
        "3 − 5: mulai di 3, mundur 5 langkah, berhenti di −2.",
        "Di fisika, tanda − pada posisi atau perpindahan berarti <b>arah</b>, bukan \"kurang dari nol\" dalam arti sedikit.",
    ]),
    ("C", "Satuan waktu", [
        "1 jam = 60 menit; 30 menit = ½ jam; 15 menit = ¼ jam.",
        "Sebelum membagi jarak dengan waktu, pastikan satuan waktunya sama dengan yang diminta (per jam atau per menit).",
    ]),
]


# ------------------------------------------------------------------ the four steps
def _r(pair):
    return rate(*pair)


LANGKAH = [
    dict(
        no=0, judul="\"Per\" artinya dibagi",
        target="Memahami bahwa \"per\" berarti \"untuk setiap satu\", dan menemukannya dengan membagi.",
        beban="Pembagian (dijembatani dengan tabel rasio). Kalkulator boleh.",
        kodifikasi=("Pagi hari di tempat pelelangan ikan. Perahu baru merapat. Seorang pembeli membeli 3 kg ikan dan membayar "
                    f"{rp(HARGA_A[0])}. Pembeli lain membeli 5 kg ikan yang sama dan membayar {rp(HARGA_B[0])}."),
        terjemah=[
            (f"Berapa harga 1 kg jika 3 kg harganya {rp(HARGA_A[0])}?", "bagi"),
            ("Berapa harga 4 kg jika 1 kg harganya Rp20.000?", "kali"),
            ("Perahu sudah menempuh 7 km dari 12 km. Berapa km lagi?", "kurang"),
            ("Perahu menempuh 18 km dalam 3 jam. Berapa km tiap jam?", "bagi"),
        ],
        lihat=dict(
            soal="Siapa yang membayar lebih murah untuk setiap 1 kg ikan?",
            fig=ratio_table([("3 kg", rp(HARGA_A[0])), ("1 kg", "? (bagi kedua kolom dengan 3)")], ("Pembeli 1: berat", "harga")),
            langkah=[
                f"Pembeli 1: {rp(HARGA_A[0])} untuk 3 kg. Bagi kedua kolom dengan 3: 1 kg → {rp(_r(HARGA_A))}.",
                f"Pembeli 2: {rp(HARGA_B[0])} untuk 5 kg. Bagi kedua kolom dengan 5: 1 kg → {rp(_r(HARGA_B))}.",
                f"Bandingkan harga <b>per kg</b>, bukan harga totalnya: {rp(_r(HARGA_B))} &lt; {rp(_r(HARGA_A))}.",
            ],
            jawab=f"Pembeli 2 membayar lebih murah per kg ({rp(_r(HARGA_B))} per kg), walaupun total bayarnya lebih besar.",
        ),
        bersama=dict(
            soal=f"Sebuah perahu menempuh {BERSAMA0[0]} km dalam {BERSAMA0[1]} jam dengan laju tetap. Berapa km per jam?",
            fig=ratio_table([(f"{BERSAMA0[1]} jam", f"{BERSAMA0[0]} km"), ("1 jam", "____ km")], ("Waktu", "Jarak")),
            langkah=[
                "Kita mencari jarak untuk <b>1</b> jam. Dari 3 jam ke 1 jam, waktunya dibagi ____.",
                "Kolom jarak juga dibagi dengan bilangan yang sama: 24 : ____ = ____ km.",
                "Jadi laju perahu ____ km per jam, ditulis ____ km/jam.",
            ],
            kunci=f"Dibagi 3; 24 : 3 = {n(_r(BERSAMA0))} km; laju {n(_r(BERSAMA0))} km/jam.",
        ),
        sendiri=[
            (f"Sebuah perahu menempuh {SENDIRI0[0][0]} km dalam {SENDIRI0[0][1]} jam. Berapa km per jam?",
             f"{n(_r(SENDIRI0[0]))} km/jam", "Tabel rasio: 4 jam → 20 km, bagi dengan 4: 1 jam → 5 km."),
            (f"Kamu berjalan {SENDIRI0[1][0]} m dalam {SENDIRI0[1][1]} menit. Berapa meter per menit?",
             f"{n(_r(SENDIRI0[1]))} m/menit", "600 : 5."),
            (f"Perahu A menempuh {PERAHU_A[0]} km dalam {PERAHU_A[1]} jam. Perahu B menempuh {PERAHU_B[0]} km dalam {PERAHU_B[1]} jam. "
             "Perahu B menempuh jarak lebih jauh. Apakah B lebih cepat? Jelaskan dengan km per jam.",
             f"Tidak. A: {n(_r(PERAHU_A))} km/jam, B: {n(_r(PERAHU_B))} km/jam; A lebih cepat",
             "Yang dibandingkan adalah jarak <b>per jam</b>, bukan jarak totalnya."),
        ],
        konkret=("<b>Ukur sendiri.</b> Tandai 10 m di halaman. Satu orang berjalan biasa, satu orang mengukur waktunya dengan stopwatch ponsel, "
                 "satu orang mencatat. Ulangi tiga kali dengan orang berbeda. Hitung meter per detik dengan kalkulator dan bulatkan ke satu angka "
                 "di belakang koma. Hasilnya tidak harus bulat: ini data nyata."),
        produk="Tabel rasio yang sudah terisi untuk soal Bersama dan Sendiri, ditambah tabel hasil pengukuran kelompok.",
        diskusi=("Di tempat pelelangan, harga per kg tidak selalu sama untuk setiap pembeli atau setiap hari. "
                 "<b>Siapa yang menentukan harga per kg, bagaimana caranya, dan data apa yang bisa kalian kumpulkan untuk mengetahuinya?</b>"),
        macet=["Apa yang ditanyakan: jumlah total, atau jumlah untuk <b>satu</b>?",
               "Buat tabel rasio dua kolom. Tulis baris yang diketahui, lalu baris \"1 ...\".",
               "Bagi kedua kolom dengan bilangan yang sama sampai kolom kiri menjadi 1."],
        uji=[
            (f"Sebuah perahu menempuh {UJI0[0]} km dalam {UJI0[1]} jam dengan laju tetap. Berapa km per jam?",
             f"{n(_r(UJI0))} km/jam", "18 : 3."),
            ("Laju sebuah perahu 6 km/jam. Pilih arti yang tepat: (a) perahu menempuh 6 km dalam 6 jam; "
             "(b) setiap 1 jam perahu menempuh 6 km; (c) perahu berhenti setelah 6 km.",
             "(b)", "\"Per jam\" berarti untuk setiap 1 jam."),
        ],
        ingat=["A", "C"],
        guru=dict(
            salah=["Membagi terbalik (3 : 18) karena \"bilangan besar dibagi bilangan kecil\" tidak dipikirkan. Tanyakan: \"km per jam: km-nya di atas atau di bawah?\"",
                   "Membandingkan total, bukan per satuan (soal Perahu A dan B, dan contoh Lihat).",
                   "Takut memakai kalkulator. Tegaskan bahwa di sini yang dinilai adalah memilih operasi."],
            gagal="Jika kurang dari dua pertiga kelompok benar pada uji keluar, ulangi Bersama dengan konteks yang lebih dekat (uang jajan per hari, halaman per menit) sebelum masuk Langkah 1.",
            solo=dict(uni="Menghitung harga 1 kg dari satu pasangan data.",
                      multi="Menghitung harga per kg untuk dua pembeli secara terpisah.",
                      rel="Membandingkan dua pembeli dengan harga per kg dan menjelaskan mengapa total bayar bukan ukuran yang tepat.",
                      ext="Memakai ide \"per\" pada kasus lain yang dipilih sendiri (liter per km, halaman per hari)."),
        ),
    ),
    dict(
        no=1, judul="Posisi, jarak, dan perpindahan",
        target="Membedakan jarak (panjang seluruh lintasan) dan perpindahan (posisi akhir dikurangi posisi awal, punya arah).",
        beban="Menjumlah dan mengurang, termasuk bilangan negatif.",
        kodifikasi=("Sebuah perahu berangkat dari pantai dan berlayar 6 km lurus ke laut. "
                    "Lalu perahu itu kembali 4 km ke arah pantai untuk menjemput teman di perahu lain."),
        terjemah=[
            ("Berapa km seluruhnya yang dilalui perahu?", "jumlah (panjang setiap bagian dijumlahkan)"),
            ("Di mana perahu sekarang, dibandingkan tempat berangkatnya?", "kurang (posisi akhir − posisi awal)"),
            ("Perahu ada di 8 km, lalu kembali 3 km. Di mana posisinya?", "kurang"),
        ],
        lihat=dict(
            soal=f"Perahu berangkat dari pantai (x = {LIHAT1[0]}), berlayar ke x = {LIHAT1[1]} km, lalu kembali ke x = {LIHAT1[2]} km. Tentukan jarak dan perpindahannya.",
            fig=FIG_NL_LIHAT,
            langkah=[
                "Pilih titik nol dan arah positif: pantai = 0, ke laut = positif.",
                f"Jarak: jumlahkan panjang setiap bagian lintasan: {LIHAT1[1] - LIHAT1[0]} km + {abs(LIHAT1[2] - LIHAT1[1])} km = {n(jarak(LIHAT1))} km.",
                f"Perpindahan: posisi akhir − posisi awal = {LIHAT1[2]} − {LIHAT1[0]} = +{n(perpindahan(LIHAT1))} km (ke arah laut).",
            ],
            jawab=f"Jarak {n(jarak(LIHAT1))} km; perpindahan +{n(perpindahan(LIHAT1))} km.",
        ),
        bersama=dict(
            soal=f"Perahu mulai di rumpon x = {BERSAMA1[0]} km, berlayar ke x = {BERSAMA1[1]} km, lalu kembali ke x = {BERSAMA1[2]} km.",
            fig=FIG_NL_BERSAMA,
            langkah=[
                "Panjang bagian pertama: 8 − 2 = ____ km. Panjang bagian kedua: 8 − 5 = ____ km.",
                "Jarak = ____ km + ____ km = ____ km.",
                "Perpindahan = posisi akhir − posisi awal = ____ − ____ = ____ km.",
            ],
            kunci=f"6 dan 3; jarak {n(jarak(BERSAMA1))} km; perpindahan 5 − 2 = +{n(perpindahan(BERSAMA1))} km.",
        ),
        sendiri=[
            (f"Perahu berangkat dari pantai ke x = {SENDIRI1[0][1]} km, lalu pulang ke pantai. Tentukan jarak dan perpindahannya.",
             f"jarak {n(jarak(SENDIRI1[0]))} km; perpindahan {n(perpindahan(SENDIRI1[0]))}",
             "6 + 6 = 12; posisi akhir sama dengan posisi awal, jadi perpindahan 0."),
            (f"Perahu bergerak dari x = {SENDIRI1[1][0]} km ke x = {SENDIRI1[1][1]} km. Tentukan jarak dan perpindahannya. Apa arti tandanya?",
             f"jarak {n(jarak(SENDIRI1[1]))} km; perpindahan {n(perpindahan(SENDIRI1[1]))} km",
             "1 − 4 = −3: tanda negatif berarti perahu berpindah ke arah pantai. Jarak selalu positif."),
            (f"Di lantai kelas ada pita meteran: 0 = \"pantai\", ke depan = positif. Seorang siswa berjalan dari 0 ke +{SENDIRI1[2][1]} m, "
             f"lalu berbalik dan berhenti di {n(SENDIRI1[2][2])} m. Tentukan jarak dan perpindahannya.",
             f"jarak {n(jarak(SENDIRI1[2]))} m; perpindahan {n(perpindahan(SENDIRI1[2]))} m",
             "4 + 6 = 10 (dari 4 ke −2 panjangnya 6); −2 − 0 = −2."),
        ],
        konkret=("<b>Jalan di garis.</b> Tempel pita meteran 10 m di lantai. Tandai 0 sebagai \"pantai\" dan arah ke depan sebagai \"laut\" (+). "
                 "Bergiliran, satu orang berjalan sesuai kartu perintah (\"maju 4 m, mundur 6 m\"), yang lain mencatat posisi setiap berhenti "
                 "di tabel, lalu menghitung jarak dan perpindahan. Tukar kartu antarkelompok."),
        produk="Tabel posisi dari kegiatan jalan di garis (posisi awal, setiap posisi berhenti, posisi akhir), dengan jarak dan perpindahannya.",
        diskusi=("Seberapa jauh perahu berlayar tidak hanya ditentukan oleh nelayannya. "
                 "<b>Apa saja yang menentukan seberapa jauh sebuah perahu bisa pergi (misalnya bahan bakar, cuaca, ukuran perahu, aturan), "
                 "siapa yang memutuskannya, dan data apa yang bisa membuktikannya?</b>"),
        macet=["Gambar garis bilangan dulu: di mana 0, ke mana arah positif?",
               "Untuk jarak: gambar panah untuk setiap bagian perjalanan, lalu ukur panjang setiap panah.",
               "Untuk perpindahan: lihat hanya titik awal dan titik akhir, abaikan jalan di tengahnya."],
        uji=[
            ("Perahu berlayar 5 km dari pantai ke laut, lalu kembali 2 km ke arah pantai. Tentukan jarak dan perpindahannya.",
             f"jarak {n(jarak(UJI1))} km; perpindahan +{n(perpindahan(UJI1))} km", "5 + 2 = 7; posisi akhir 3 km, jadi 3 − 0 = +3."),
            ("Perpindahan sebuah perahu −3 km (pantai = 0, ke laut = positif). Apa artinya?",
             "Posisi akhir perahu 3 km lebih dekat ke pantai daripada posisi awalnya",
             "Tanda − menunjukkan arah perpindahan (ke arah pantai), bukan jarak yang negatif."),
        ],
        ingat=["A", "B"],
        guru=dict(
            salah=["Menganggap jarak dan perpindahan selalu sama. Contoh Sendiri 1 (pulang-pergi) membongkar ini.",
                   "Menulis jarak negatif. Jarak tidak punya arah.",
                   "Menghitung perpindahan dengan menjumlahkan semua bagian bertanda, lalu salah tanda. Arahkan ke \"akhir − awal\"."],
            gagal="Jika uji keluar gagal, ulangi kegiatan jalan di garis dengan kartu yang hanya punya dua gerakan, dan minta siswa menyebut posisi dengan suara keras setiap berhenti.",
            solo=dict(uni="Menentukan posisi akhir dari satu gerakan.",
                      multi="Menghitung jarak dan perpindahan, tetapi tidak bisa menjelaskan mengapa berbeda.",
                      rel="Menjelaskan kapan jarak sama dengan perpindahan (gerak searah tanpa berbalik) dan kapan tidak.",
                      ext="Merancang kartu perintah sendiri dengan perpindahan 0 tetapi jarak sejauh mungkin di pita 10 m."),
        ),
    ),
    dict(
        no=2, judul="Kelajuan rata-rata dan kecepatan rata-rata",
        target="Menghitung kelajuan rata-rata (jarak : waktu) dan kecepatan rata-rata (perpindahan : waktu), dan menjelaskan perbedaannya.",
        beban="Pembagian. Kalkulator boleh: yang dilatih adalah memilih jarak atau perpindahan.",
        kodifikasi=("Perahu berangkat pukul 04.00, berlayar 12 km ke laut selama 2 jam, memancing di tempat selama 2 jam, "
                    "lalu pulang 12 km ke pantai selama 2 jam."),
        terjemah=[
            ("Berapa km seluruhnya yang dilalui perahu?", "jumlah"),
            ("Berapa lama seluruh perjalanan, termasuk saat memancing?", "jumlah"),
            ("Berapa km rata-rata yang dilalui tiap jam?", "bagi (jarak : waktu)"),
        ],
        lihat=dict(
            soal="Tentukan kelajuan rata-rata dan kecepatan rata-rata perahu untuk seluruh perjalanan pada cerita di atas.",
            fig="",
            langkah=[
                f"Jarak = 12 + 0 + 12 = {n(jarak(LIHAT2[0]))} km. Waktu = 2 + 2 + 2 = {LIHAT2[1]} jam (waktu memancing ikut dihitung).",
                f"Kelajuan rata-rata = jarak : waktu = {n(jarak(LIHAT2[0]))} : {LIHAT2[1]} = {n(rate(jarak(LIHAT2[0]), LIHAT2[1]))} km/jam.",
                f"Perpindahan = 0 − 0 = {n(perpindahan(LIHAT2[0]))} km (perahu kembali ke pantai).",
                f"Kecepatan rata-rata = perpindahan : waktu = 0 : {LIHAT2[1]} = {n(rate(perpindahan(LIHAT2[0]), LIHAT2[1]))} km/jam.",
            ],
            jawab=f"Kelajuan rata-rata {n(rate(jarak(LIHAT2[0]), LIHAT2[1]))} km/jam; kecepatan rata-rata {n(rate(perpindahan(LIHAT2[0]), LIHAT2[1]))} km/jam.",
        ),
        bersama=dict(
            soal=f"Perahu hanya berangkat: dari pantai menempuh {BERSAMA2[0][1]} km ke laut dalam {BERSAMA2[1]} jam, tanpa berbalik.",
            fig="",
            langkah=[
                "Jarak = ____ km. Perpindahan = ____ − 0 = ____ km.",
                "Kelajuan rata-rata = ____ : ____ = ____ km/jam.",
                "Kecepatan rata-rata = ____ : ____ = ____ km/jam, arahnya ke ______.",
                "Mengapa di soal ini kelajuan rata-rata sama dengan besar kecepatan rata-rata? ____________",
            ],
            kunci=(f"Jarak 10 km, perpindahan +10 km; kelajuan {n(rate(jarak(BERSAMA2[0]), BERSAMA2[1]))} km/jam; "
                   f"kecepatan +{n(rate(perpindahan(BERSAMA2[0]), BERSAMA2[1]))} km/jam ke arah laut; sama karena perahu bergerak searah tanpa berbalik."),
        ),
        sendiri=[
            (f"Seorang siswa berjalan lurus {SENDIRI2[0][0][1]} km dalam {SENDIRI2[0][1]} jam. Berapa kelajuan rata-ratanya?",
             f"{n(rate(jarak(SENDIRI2[0][0]), SENDIRI2[0][1]))} km/jam", "3 : 1."),
            ("Perahu berlayar 9 km ke laut dalam 2 jam, lalu kembali 3 km ke arah pantai dalam 1 jam. "
             "Tentukan kelajuan rata-rata dan kecepatan rata-ratanya.",
             f"kelajuan {n(rate(jarak(SENDIRI2[1][0]), SENDIRI2[1][1]))} km/jam; kecepatan +{n(rate(perpindahan(SENDIRI2[1][0]), SENDIRI2[1][1]))} km/jam",
             "Jarak 9 + 3 = 12 km, perpindahan 6 − 0 = +6 km, waktu 3 jam; 12 : 3 = 4 dan 6 : 3 = 2."),
            (f"Perahu A menempuh {SENDIRI2[2][0][1]} km dalam {SENDIRI2[2][1]} jam. Perahu B menempuh {SENDIRI2_B[0][1]} km yang sama dalam {SENDIRI2_B[1]} jam. "
             "Mana yang kelajuan rata-ratanya lebih besar, dan berapa kali lipat?",
             f"A, {n(rate(jarak(SENDIRI2[2][0]), SENDIRI2[2][1]) / rate(jarak(SENDIRI2_B[0]), SENDIRI2_B[1]))} kali lipat",
             f"A: 8 : 2 = {n(rate(8, 2))} km/jam; B: 8 : 4 = {n(rate(8, 4))} km/jam; 4 : 2 = 2."),
        ],
        konkret=("<b>Bolak-balik di halaman.</b> Pakai jalur 10 m dari Langkah 0. Satu orang berjalan dari 0 ke 10 m lalu kembali ke 0; "
                 "ukur waktunya. Hitung kelajuan rata-rata dan kecepatan rata-rata dengan kalkulator, bulatkan ke satu angka di belakang koma. "
                 "Lalu ulangi, tetapi berhenti di 10 m (tanpa kembali). Bandingkan kedua hasilnya."),
        produk="Perhitungan kelajuan dan kecepatan rata-rata untuk soal Sendiri dan untuk dua percobaan kelompok, masing-masing dengan satuan.",
        diskusi=("Perahu tidak selalu bisa memilih kapan berangkat dan kapan pulang. "
                 "<b>Apa atau siapa yang menentukan jam berangkat dan jam pulang perahu, dan bagaimana kalian bisa memeriksanya, "
                 "misalnya dengan mencatat jam berangkat dan pulang selama seminggu?</b>"),
        macet=["Tulis tiga angka dulu: jarak, perpindahan, dan waktu total.",
               "Kelajuan memakai <b>jarak</b>; kecepatan memakai <b>perpindahan</b>. Mana yang diminta?",
               "Ingat: waktu berhenti tetap dihitung dalam waktu total."],
        uji=[
            ("Perahu berlayar 10 km ke laut dalam 2 jam, lalu pulang 10 km ke pantai dalam 2 jam. Tentukan kelajuan rata-rata dan kecepatan rata-ratanya.",
             f"kelajuan {n(rate(jarak(UJI2[0]), UJI2[1]))} km/jam; kecepatan {n(rate(perpindahan(UJI2[0]), UJI2[1]))} km/jam",
             "Jarak 20 km, waktu 4 jam; perpindahan 0."),
            ("Perahu itu bergerak selama 4 jam, tetapi kecepatan rata-ratanya 0. Jelaskan mengapa ini tidak salah.",
             "Karena posisi akhir sama dengan posisi awal, perpindahannya 0",
             "Kecepatan rata-rata hanya melihat perpindahan (dari mana ke mana), bukan seberapa banyak perahu bergerak."),
        ],
        ingat=["C"],
        guru=dict(
            salah=["Tidak memasukkan waktu berhenti ke waktu total (pada contoh Lihat: 24 : 4 = 6, bukan 24 : 6 = 4).",
                   "Merata-ratakan dua kelajuan, bukan membagi jarak total dengan waktu total.",
                   "Menulis kecepatan tanpa arah atau tanda."],
            gagal="Jika uji keluar gagal, kembali ke tabel tiga kolom (jarak, perpindahan, waktu) dan kerjakan contoh Lihat sekali lagi bersama, kali ini dengan waktu memancing 0, lalu 2 jam, supaya terlihat pengaruh waktu berhenti.",
            solo=dict(uni="Menghitung kelajuan rata-rata dari jarak dan waktu yang diberikan.",
                      multi="Menghitung kelajuan dan kecepatan rata-rata secara terpisah tanpa mengaitkannya.",
                      rel="Menjelaskan mengapa keduanya sama pada gerak searah dan berbeda pada gerak bolak-balik.",
                      ext="Mengusulkan cara mengukur kelajuan rata-rata perjalanan sungguhan (ke sekolah, ke pasar) dan menyebut sumber ketidakpastiannya."),
        ),
    ),
    dict(
        no=3, judul="Membaca grafik posisi–waktu",
        target="Membaca grafik x–t sebagai cerita sebelum menghitung, lalu menghitung kecepatan dari kemiringan dengan menghitung kotak.",
        beban="Membilang kotak, lalu pembagian.",
        kodifikasi="Grafik di bawah adalah perjalanan perahu dari Langkah 2: berangkat, memancing, lalu pulang. Coba ceritakan gerak perahu hanya dari bentuk grafiknya.",
        kodifikasi_fig=FIG_TRIP,
        terjemah=[
            ("Garis naik: perahu ...", "menjauh dari pantai"),
            ("Garis mendatar: perahu ...", "diam (posisinya tetap)"),
            ("Garis turun: perahu ...", "mendekat ke pantai"),
            ("Kecepatan dari grafik", "bagi (perubahan posisi : waktu)"),
        ],
        lihat=dict(
            soal="Pada grafik di atas, tentukan kecepatan perahu saat berangkat.",
            fig="",
            langkah=[
                "Ceritakan dulu: dari t = 0 sampai t = 2 jam garisnya naik, jadi perahu menjauh dari pantai.",
                f"Hitung kotak: posisi naik dari 0 ke {TRIP[1][1]} km, waktu bertambah dari 0 ke {TRIP[1][0]} jam.",
                f"Kecepatan = perubahan posisi : waktu = {TRIP[1][1]} : {TRIP[1][0]} = {n(slopes(TRIP)[0])} km/jam.",
                "Semakin curam garisnya, semakin cepat geraknya.",
            ],
            jawab=f"{n(slopes(TRIP)[0])} km/jam ke arah laut.",
        ),
        bersama=dict(
            soal="Pasangkan setiap cerita (1–4) dengan grafiknya (A–D).",
            fig="COCOK",
            langkah=[f"Cerita {k + 1}: {c} → grafik ____" for k, c in enumerate(CERITA)],
            kunci="; ".join(f"cerita {s} → {g}" for g, (_, s) in sorted(COCOK.items(), key=lambda kv: kv[1][1])),
        ),
        sendiri=[
            ("Grafik di atas menunjukkan perjalanan perahu lain. Ceritakan geraknya dalam tiga kalimat (satu kalimat untuk setiap bagian grafik).",
             "Berangkat menjauh dari pantai 8 km dalam 2 jam; diam 1 jam di 8 km; pulang ke pantai dalam 1 jam",
             "Naik, mendatar, turun."),
            ("Berapa kecepatan perahu pada setiap bagian?",
             f"{n(slopes(SENDIRI3)[0])} km/jam; {n(slopes(SENDIRI3)[1])}; {n(slopes(SENDIRI3)[2])} km/jam (ke arah pantai)",
             "8 : 2 = 4; mendatar berarti 0; turun 8 km dalam 1 jam, tanda − menunjukkan arah ke pantai."),
            ("Pada bagian mana perahu paling cepat? Jelaskan hanya dengan melihat bentuk grafik.",
             "Saat pulang", "Garisnya paling curam."),
            ("Tentukan kelajuan rata-rata perahu untuk seluruh perjalanan.",
             f"{n(rate(jarak([x for _, x in SENDIRI3]), SENDIRI3[-1][0]))} km/jam",
             "Jarak 8 + 0 + 8 = 16 km, waktu 4 jam; 16 : 4 = 4."),
        ],
        sendiri_fig=FIG_SENDIRI3,
        konkret=("<b>Berjalan mengikuti grafik.</b> Guru menunjukkan sebuah kartu grafik x–t (dalam meter dan detik). Satu siswa berjalan di pita meteran "
                 "sehingga geraknya sesuai grafik; siswa lain menghitung detik dengan suara keras. Kelas menilai: apakah geraknya cocok? "
                 "Jika ada aplikasi pelacak gerak gratis di ponsel, rekam gerakannya dan bandingkan grafiknya."),
        produk="Pasangan cerita–grafik, cerita tertulis untuk grafik Sendiri, dan kecepatan setiap bagian dengan tandanya.",
        diskusi=("Grafik seperti ini bisa dibuat dari catatan jam dan posisi. "
                 "<b>Jika kalian ingin tahu apakah perahu pulang pada jam yang aman, data apa yang perlu dicatat, siapa yang sebaiknya memutuskan jam pulang, "
                 "dan bagaimana grafik bisa membantu keputusan itu?</b>"),
        macet=["Baca sumbunya dulu: sumbu mendatar waktu (jam), sumbu tegak posisi (km).",
               "Ceritakan setiap bagian garis: naik, mendatar, atau turun?",
               "Untuk kecepatan: hitung berapa kotak posisi berubah dan berapa kotak waktu berlalu, lalu bagi."],
        uji=[
            ("Gambar grafik x–t untuk cerita ini: perahu berlayar 6 km ke laut selama 1 jam, menunggu 2 jam, lalu pulang ke pantai selama 1 jam.",
             "Lihat grafik kunci", "Titik sudut (0, 0), (1, 6), (3, 6), (4, 0)."),
            ("Dari grafikmu, berapa kecepatan perahu saat berangkat dan saat pulang?",
             f"{n(slopes(UJI3)[0])} km/jam dan {n(slopes(UJI3)[2])} km/jam",
             "6 : 1 = 6 menjauh; turun 6 km dalam 1 jam, tanda − berarti ke arah pantai."),
        ],
        uji_blank=FIG_BLANK,
        uji_key=FIG_UJI3,
        ingat=["B"],
        guru=dict(
            salah=["Membaca grafik x–t sebagai gambar jalan atau bukit (\"perahu mendaki\"). Selalu minta cerita dulu, baru angka.",
                   "Mengira garis mendatar berarti perahu bergerak dengan kecepatan tetap. Garis mendatar pada grafik x–t berarti diam.",
                   "Menghitung kemiringan dengan membagi posisi akhir dengan waktu akhir, bukan perubahan dengan perubahan."],
            gagal="Jika uji keluar gagal, ulangi kegiatan berjalan mengikuti grafik dengan grafik yang hanya punya dua bagian, sebelum masuk Modul Gerak Lurus.",
            solo=dict(uni="Menyebut apakah perahu bergerak atau diam pada satu bagian grafik.",
                      multi="Menceritakan setiap bagian grafik secara terpisah.",
                      rel="Menghubungkan kecuraman garis dengan kecepatan dan membandingkan bagian-bagian grafik.",
                      ext="Menggambar grafik untuk perjalanan sungguhan dari lingkungannya sendiri, lengkap dengan skala yang dipilih sendiri."),
        ),
    ),
]


PRAKSIS = dict(
    judul="Kartu Gerak Kita",
    intro=("Sekarang giliran kalian membawa cerita. Pilih satu gerak lurus yang benar-benar terjadi di sekitar kalian: perjalanan ke sekolah, "
           "angkot ke pasar, perahu, sepeda, kereta, atau gerak lain yang kalian kenal. Kartu ini akan dipakai di pertemuan berikutnya, "
           "ketika kelas menganalisis kasus-kasus dari kartu kalian."),
    baris=["Apa yang bergerak?", "Dari mana ke mana? (sebut tempat umum, misalnya \"pertigaan\" atau \"pasar\", bukan alamat rumah)",
           "Perkiraan jarak (dan bagaimana kalian memperkirakannya)", "Perkiraan waktu (dan bagaimana kalian mengukurnya)",
           "Kelajuan rata-rata (dengan satuan)", "Apakah ada bagian ketika benda itu berhenti? Berapa lama?",
           "Satu hal yang membuat kalian penasaran tentang gerak ini"],
    aturan=["Jangan menulis nama orang, alamat rumah, atau biaya yang dikeluarkan keluarga.",
            "Angka boleh perkiraan, tetapi tulis bagaimana kalian memperkirakannya.",
            "Sertakan sketsa grafik x–t di kotak yang tersedia."],
    untuk="Hasilnya ditempel di papan kelas sebagai \"peta gerak\" lingkungan sekolah, dan dipakai sebagai kasus di pertemuan berikutnya.",
)


META = dict(
    title="Jembatan ke Gerak Lurus",
    kick="Fisika SMA Kelas X · Rangkaian among · Draf",
    big="Jembatan ke<br>Gerak Lurus",
    subtitle="Empat langkah dari \"per\" sampai grafik posisi–waktu, untuk kelas yang ingin masuk ke Gerak Lurus dari cerita di sekitarnya",
    tujuan=[f"Langkah {s['no']}. {s['target']}" for s in LANGKAH],
    cara=[
        "Kerjakan Cek Awal sendiri dulu. Hasilnya bukan nilai; hasilnya memberi tahu kotak mana yang perlu kamu baca.",
        "Setiap langkah dimulai dengan sebuah <b>cerita</b>. Sebelum menghitung apa pun, jawab: <i>Apa yang terjadi? Apa yang bisa kita ukur?</i>",
        "Lalu <b>Cerita → operasi</b>: sebut operasinya saja (jumlah, kurang, kali, bagi). Jangan menghitung dulu.",
        "Bagian <b>Lihat</b> dikerjakan guru di depan kelas. Bagian <b>Bersama</b> dikerjakan dalam kelompok campuran. Bagian <b>Sendiri</b> dikerjakan sendiri; guru hanya memeriksa.",
        "Kalau macet, pakai kotak <b>Kalau macet</b> dari atas ke bawah. Ambil satu bantuan, coba lagi, baru ambil bantuan berikutnya.",
        "Serahkan <b>hasil kerja</b> dulu, baru diskusi. Dalam diskusi, pakai angka dari hasil kerjamu sendiri sebagai bukti.",
        "Kalkulator boleh dipakai di semua langkah. Yang dilatih adalah memilih operasi dan memahami artinya, bukan berhitung cepat.",
    ],
    konvensi="Posisi diukur dari pantai (x = 0); arah ke laut positif. Jarak dalam km atau m, waktu dalam jam, menit, atau detik. Desimal ditulis dengan koma.",
    catatan_angka="Harga, jarak, dan waktu dalam cerita adalah angka contoh yang dibuat bulat, bukan data sungguhan.",
)

GURU_UMUM = [
    "<b>Untuk siapa.</b> Kelas yang hasil cek prasyaratnya lemah pada pembagian, arti \"per\", atau soal cerita. Semua siswa mengerjakan langkah yang sama dalam kelompok campuran; perbedaan ada pada kedalaman jawaban (target SOLO di bawah), bukan pada jalur terpisah.",
    "<b>Tema.</b> Perjalanan perahu nelayan adalah tema kelas acuan, hasil dialog dengan siswanya. Untuk kelas lain, temukan tema lewat dialog lebih dulu. Tema alternatif dengan fisika yang sama: jalan kaki atau bersepeda ke sekolah (titik nol = rumah atau gerbang), angkot dari terminal ke pasar.",
    "<b>Membaca Cek Awal per kelas.</b> Hitung persentase siswa yang benar pada <b>kedua</b> soal sebuah keterampilan. Di bawah 40%: kerjakan jembatannya bersama seluruh kelas sebelum langkah yang memakainya. 40–75%: cukup Kotak Ingat di awal langkah itu. Di atas 75%: lewati. Dengan sekitar 30 siswa, selisih beberapa persen tidak berarti; jangan membuat keputusan dari selisih kecil di sekitar batas.",
    "<b>Waktu.</b> Rencana awal: satu pertemuan (2 × 45 menit) untuk setiap langkah, ditambah setengah pertemuan untuk Kartu Gerak Kita. Ini perkiraan, belum diuji di kelas.",
    "<b>Pindah dari Bersama ke Sendiri</b> jika sedikitnya dua pertiga kelompok menyelesaikan Bersama tanpa memakai bantuan ketiga di kotak Kalau macet.",
    "<b>Diskusi.</b> Pertanyaan diskusi tidak punya jawaban sosial yang \"benar\". Nilai penggunaan bukti dari hasil kerja siswa, bukan kesimpulannya. Jangan menanyakan penghasilan, utang, atau kesulitan keluarga siswa.",
    "<b>Setelah Langkah 3.</b> Siswa yang lulus uji keluar Langkah 3 siap untuk Modul Gerak Lurus. Kartu Gerak Kita dikumpulkan sebagai bahan kasus untuk rangkaian analisis kasus berikutnya.",
]


# ------------------------------------------------------------------ checks
def check():
    # cek awal
    assert 7 + 5 == 12 and 12 - 4 == 8 and 25 + 18 == 43 and 40 - 13 == 27
    assert 15 - 6 == 9 and 3 + 2 == 5 and 4 * 6 == 24 and 3 * 15 == 45 and 8 * 5 == 40
    assert 24 / 4 == 6 and 90 / 5 == 18 and 12 / 3 == 4 and 10 / 2 == 5
    assert 5 - 7 == -2 and 3 - 5 == -2 and 2 - 8 == -6

    # Langkah 0: every rate divides evenly (spec §5)
    for pair in [HARGA_A, HARGA_B, BERSAMA0, *SENDIRI0, PERAHU_A, PERAHU_B, UJI0]:
        assert pair[0] % pair[1] == 0, pair
    assert _r(HARGA_A) == 20000 and _r(HARGA_B) == 18000 and _r(HARGA_B) < _r(HARGA_A)
    assert _r(BERSAMA0) == 8 and _r(SENDIRI0[0]) == 5 and _r(SENDIRI0[1]) == 120
    assert _r(PERAHU_A) == 5 and _r(PERAHU_B) == 4 and PERAHU_B[0] > PERAHU_A[0]
    assert _r(UJI0) == 6

    # Langkah 1
    assert (jarak(LIHAT1), perpindahan(LIHAT1)) == (10, 2)
    assert (jarak(BERSAMA1), perpindahan(BERSAMA1)) == (9, 3)
    assert (jarak(SENDIRI1[0]), perpindahan(SENDIRI1[0])) == (12, 0)
    assert (jarak(SENDIRI1[1]), perpindahan(SENDIRI1[1])) == (3, -3)
    assert (jarak(SENDIRI1[2]), perpindahan(SENDIRI1[2])) == (10, -2)
    assert (jarak(UJI1), perpindahan(UJI1)) == (7, 3)
    assert UJI1[1] - UJI1[0] == 5 and UJI1[1] - UJI1[2] == 2

    # Langkah 2
    assert jarak(LIHAT2[0]) == 24 and LIHAT2[1] == 6 and rate(24, 6) == 4 and perpindahan(LIHAT2[0]) == 0
    assert rate(jarak(BERSAMA2[0]), BERSAMA2[1]) == 5 == rate(perpindahan(BERSAMA2[0]), BERSAMA2[1])
    assert rate(jarak(SENDIRI2[0][0]), SENDIRI2[0][1]) == 3
    assert jarak(SENDIRI2[1][0]) == 12 and perpindahan(SENDIRI2[1][0]) == 6 and SENDIRI2[1][1] == 3
    assert rate(12, 3) == 4 and rate(6, 3) == 2
    assert rate(8, 2) / rate(8, 4) == 2
    assert jarak(UJI2[0]) == 20 and rate(20, UJI2[1]) == 5 and perpindahan(UJI2[0]) == 0
    for path, t in [LIHAT2, BERSAMA2, *SENDIRI2, SENDIRI2_B, UJI2]:
        assert jarak(path) % t == 0 and perpindahan(path) % t == 0, (path, t)

    # Langkah 3: the trip graph matches Langkah 2's story; corners on gridlines
    assert [x for _, x in TRIP] == LIHAT2[0] and TRIP[-1][0] == LIHAT2[1]
    assert slopes(TRIP) == [6, 0, -6]
    assert slopes(SENDIRI3) == [4, 0, -8] and jarak([x for _, x in SENDIRI3]) == 16 and rate(16, SENDIRI3[-1][0]) == 4
    assert slopes(UJI3) == [6, 0, -6] and UJI3[1] == (1, 6) and UJI3[2][0] - UJI3[1][0] == 2 and UJI3[3][0] - UJI3[2][0] == 1
    for pts, x_step in [(TRIP, 2), (SENDIRI3, 2), (UJI3, 2)] + [(p, 2) for p, _ in COCOK.values()]:
        assert all(float(t).is_integer() and x % x_step == 0 for t, x in pts), pts
    # matching: each story used once; shapes agree with the stories
    assert sorted(s for _, s in COCOK.values()) == [1, 2, 3, 4]
    shape = {g: slopes(p) for g, (p, _) in COCOK.items()}
    story = {s: g for g, (_, s) in COCOK.items()}
    assert shape[story[1]] == [0] and COCOK[story[1]][0][0][1] == 4
    assert len(shape[story[2]]) == 1 and shape[story[2]][0] < 0 and COCOK[story[2]][0][-1][1] == 0
    assert len(shape[story[3]]) == 2 and shape[story[3]][0] > 0 and shape[story[3]][1] == 0
    assert len(shape[story[4]]) == 1 and shape[story[4]][0] > 0
    # the matching key is not in story order
    assert [story[k] for k in (1, 2, 3, 4)] != ["A", "B", "C", "D"]

    # every step has all parts the among spec requires
    for s in LANGKAH:
        for key in ("target", "beban", "kodifikasi", "terjemah", "lihat", "bersama", "sendiri", "konkret", "produk", "diskusi", "macet", "uji", "guru"):
            assert s.get(key), (s["no"], key)
        assert 2 <= len(s["terjemah"]) <= 4 and len(s["macet"]) == 3 and len(s["uji"]) == 2
        assert set(s["guru"]["solo"]) == {"uni", "multi", "rel", "ext"}
        assert "=" not in s["kodifikasi"], s["no"]   # no formula in the codification
    assert [s["no"] for s in LANGKAH] == [0, 1, 2, 3]
    return True
