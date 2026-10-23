"""Content of the printable module "Gerak Vertikal" (Fisika kelas X).

Convention: y up, g = 10 m/s², a = −g, no air resistance unless stated. Every graph comes from a
Motion on a fixed template (print/graphs.py) and every numeric answer is re-derived in check().
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import Motion, TEMPLATES as TP, render  # noqa: E402
from kit import n, fr, Q, noisy, lsq_slope, close  # noqa: E402

g = 10
BLUE, RED = "#1f3a68", "#c0502a"


def fall(y0, v0, t_end, label="", color=BLUE):
    """Vertical motion with a = −g from height y0 with velocity v0 (up positive) for t_end seconds."""
    return Motion(y0, v0, [(t_end, -g)], label, color)


def G(name, *motions, w=300, h=190, **kw):
    return render(TP[name], motions, width=w, height=h, **kw)


def t_hit(y0, v0, y=0.0):
    """Later root of y0 + v0 t − ½ g t² = y."""
    a, b, c = -g / 2, v0, y0 - y
    return (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)


PRASYARAT = [
    ("P1", "Pada GLBB dengan v₀ = 20 m/s dan a = −10 m/s², berapa v pada t = 3 s?", "−10 m/s", "v = 20 + (−10)(3) = −10 m/s."),
    ("P2", "Hitung √(2 · 45 : 10).", "3", "√9 = 3."),
    ("P3", "Selesaikan 5t² − 20t = 0 untuk t &gt; 0.", "t = 4", "5t(t − 4) = 0."),
    ("P4", "Selesaikan t² − 4t + 3 = 0.", "t = 1 atau t = 3", "(t − 1)(t − 3) = 0."),
    ("P5", "Benda GLBB dari diam dengan a = 2 m/s². Berapa perpindahannya setelah 3 s?", "9 m", "½ · 2 · 3² = 9 m."),
    ("P6", "Selesaikan 0 = 20² + 2(−10)s.", "s = 20", "400 = 20s."),
    ("P7", "Hitung (−15) − (+15).", "−30", "Selisih akhir − awal."),
    ("P8", "Ubah 108 km/jam ke m/s.", "30 m/s", "108 : 3,6 = 30."),
]

INGAT = [
    ("A", "Rumus GLBB", "P1, P5, P6", "Semua subbab",
     ["v = v₀ + at; s = s₀ + v₀t + ½at²; v² = v₀² + 2a(s − s₀).", "Pada gerak vertikal, s diganti y dan a = −g bila arah ke atas positif."]),
    ("B", "Persamaan kuadrat", "P3, P4", "Subbab 2–4",
     ["Faktorkan bila bisa: t² − 4t + 3 = (t − 1)(t − 3).", "Rumus abc: t = (−b ± √(b² − 4ac)) : 2a. Pada soal waktu, buang akar negatif; dua akar positif berarti benda melewati titik itu dua kali."]),
    ("C", "Akar kuadrat", "P2", "Subbab 1",
     ["√(2h/g) dan √(2gh) sering muncul. Kuadrat sempurna yang berguna: 4, 9, 16, 25, 36, 49, 64, 100, 400, 900."]),
    ("D", "Bilangan bertanda dan satuan", "P7, P8", "Semua subbab",
     ["Arah ke atas positif, ke bawah negatif. Selisih = akhir − awal.", "km/jam : 3,6 = m/s."]),
]

SUB = []

# ================================================================== Subbab 1: jatuh bebas
D45 = fall(45, 0, 3)
D80 = fall(80, 0, 4)
SUB.append(dict(
    title="Percepatan Gravitasi dan Jatuh Bebas",
    tujuan="Menjelaskan percepatan gravitasi dan menganalisis gerak jatuh bebas dengan grafik, cerita, dan persamaan.",
    konsep=[
        "Di dekat permukaan Bumi, semua benda yang hanya dipengaruhi gravitasi mendapat percepatan yang sama, <b>g ≈ 9,8 m/s²</b> ke bawah. Modul ini memakai g = 10 m/s². Tanpa hambatan udara, benda berat dan ringan jatuh bersamaan.",
        "Gerak vertikal adalah GLBB pada garis tegak. Koordinatnya ditulis <b>y</b> (pengganti s), dengan <b>arah ke atas positif</b>. Karena percepatan gravitasi mengarah ke bawah, a = −g.",
        "<b>Jatuh bebas</b> adalah gerak dari keadaan diam (v₀ = 0) yang hanya dipengaruhi gravitasi. Kecepatannya bertambah 10 m/s setiap sekon ke arah bawah.",
    ],
    rumus=["v = −g·t (tanda negatif: ke bawah)", "y = y₀ − ½·g·t²", "Waktu jatuh dari ketinggian h: t = √(2h/g)", "Kelajuan saat menyentuh tanah: |v| = √(2gh)"],
    contoh=[
        ("Batu dari tebing", "Batu dijatuhkan dari tebing setinggi 45 m. Tentukan waktu jatuh dan kecepatannya saat menyentuh tanah. Gambarkan grafik y–t-nya.",
         G("vert-yt", D45, marks=[(3, 0, "tanah")]),
         ["Saat menyentuh tanah y = 0: 0 = 45 − 5t² → t = 3 s.", "v = −10 · 3 = −30 m/s, yaitu 30 m/s ke bawah. Cek: √(2 · 10 · 45) = 30 m/s."], "3 s; 30 m/s ke bawah"),
        ("Berat dan ringan", "Bola besi 2 kg dan bola plastik 0,2 kg dijatuhkan bersamaan dari ketinggian 20 m. Hambatan udara diabaikan. Mana yang tiba lebih dulu?",
         None, ["Percepatan keduanya sama, g, tidak bergantung pada massa.", "Keduanya tiba setelah √(2 · 20 : 10) = 2 s."], "bersamaan, setelah 2 s"),
    ],
    bertahap=dict(
        soal="Sebutir kelapa jatuh dari pohon setinggi 20 m. Tentukan waktu jatuh, kecepatan saat menyentuh tanah, dan jarak yang ditempuh pada sekon terakhir.",
        langkah=["t = √(2 · 20 : 10) = ____ s.", "|v| = 10 · ____ = ____ m/s.", "Posisi pada t = 1 s: y = 20 − 5 · 1² = ____ m. Jarak pada sekon terakhir = ____ − 0 = ____ m."],
        cek="Jarak pada sekon kedua lebih besar daripada pada sekon pertama karena",
        opsi=["(a) kecepatannya terus bertambah", "(b) percepatannya terus bertambah"],
        kunci="2 s; 20 m/s; 15 m, jarak 15 m. Alasan: (a).",
    ),
    jebakan=[
        "Tanpa hambatan udara, massa tidak memengaruhi gerak jatuh.",
        "Yang bertambah tetap setiap sekon adalah <b>kecepatan</b> (10 m/s), bukan jarak.",
        "Kecepatan negatif berarti ke bawah, bukan melambat.",
    ],
    latihan=[
        Q(1, "Batu dijatuhkan dari keadaan diam. Berapa kecepatannya setelah 2 s?", "20 m/s ke bawah", "v = −10 · 2 = −20 m/s."),
        Q(1, "Berapa jarak yang ditempuh benda jatuh bebas selama 3 s?", "45 m", "½ · 10 · 9 = 45 m."),
        Q(1, "Berapa lama benda jatuh bebas dari ketinggian 80 m sampai ke tanah?", "4 s", "√(160 : 10) = 4 s."),
        Q(1, "Berapa kelajuan benda yang jatuh bebas dari ketinggian 5 m saat menyentuh tanah?", "10 m/s", "√(2 · 10 · 5) = 10 m/s."),
        Q(1, "Pada misi Apollo 15 (1971), astronaut menjatuhkan palu dan bulu bersamaan di permukaan Bulan. Apa yang terjadi, dan mengapa?", "keduanya tiba bersamaan, karena di Bulan tidak ada udara",
          "Tanpa hambatan udara, semua benda mendapat percepatan gravitasi yang sama."),
        Q(2, "Grafik v–t sebuah bola yang dijatuhkan ditunjukkan di bawah. Berapa kecepatannya pada t = 2,5 s, dan berapa kemiringan grafiknya?", "−25 m/s; −10 m/s²",
          "Baca grafik pada t = 2,5 s. Kemiringan = (−40 − 0) : 4 = −10 m/s² = −g.", fig=G("vert-vt", D80)),
        Q(2, "Berapa jarak yang ditempuh benda jatuh bebas pada sekon ketiga saja (antara t = 2 s dan t = 3 s)?", "25 m", "45 − 20 = 25 m."),
        Q(2, "Sebuah batu dijatuhkan ke dalam sumur kering dan menyentuh dasar setelah 2 s. Berapa kedalaman sumur? (Abaikan waktu rambat bunyi.)", "20 m", "½ · 10 · 2² = 20 m."),
        Q(2, "Bola dijatuhkan dari ketinggian 45 m. Pada ketinggian berapa bola berada setelah 2 s?", "25 m", "y = 45 − 5 · 4 = 25 m."),
        Q(3, "Batu A dijatuhkan dari ketinggian h dan batu B dari ketinggian 4h. Bandingkan waktu jatuh dan kelajuan akhir keduanya.", "waktu dan kelajuan B dua kali A", "t ∝ √h dan v ∝ √h; √4 = 2."),
        Q(3, "Batu dijatuhkan dari atap gedung. Pada sekon terakhir sebelum menyentuh tanah, batu menempuh 25 m. Berapa tinggi gedung?", "45 m",
          "Jarak pada sekon terakhir = 5t² − 5(t − 1)² = 10t − 5 = 25 → t = 3 s; h = 5 · 9 = 45 m."),
        Q(3, "Dua bola dijatuhkan dari ketinggian 80 m dengan selang 1 s. Berapa jarak antara keduanya saat bola pertama menyentuh tanah?", "35 m",
          "Bola pertama tiba pada t = 4 s. Bola kedua baru jatuh 3 s: 45 m, jadi masih di ketinggian 35 m. Jaraknya 35 m."),
    ],
))

# ================================================================== Subbab 2: vertikal ke bawah
DN30 = fall(30, -5, 2)
DN40 = fall(40, -10, 2)
DN75 = fall(75, -10, 3)
SUB.append(dict(
    title="Gerak Vertikal ke Bawah",
    tujuan="Menganalisis benda yang dilempar ke bawah sebagai GLBB dengan kecepatan awal ke bawah dan percepatan g.",
    konsep=[
        "Benda yang <b>dilempar ke bawah</b> sudah mempunyai kecepatan awal ke bawah. Dengan arah ke atas positif, kecepatan awalnya ditulis negatif, misalnya v₀ = −5 m/s.",
        "Percepatannya tetap −g, sama seperti jatuh bebas. Benda yang dilempar ke bawah dan benda yang dijatuhkan dari tempat yang sama mempunyai kecepatan yang berselisih tetap sebesar kecepatan awal tadi.",
        "Waktu tiba di tanah dicari dari y = 0, yang biasanya menghasilkan persamaan kuadrat. Ambil akar yang positif.",
    ],
    rumus=["v = v₀ − g·t (v₀ negatif untuk lemparan ke bawah)", "y = y₀ + v₀·t − ½·g·t²", "v² = v₀² − 2g·(y − y₀)",
           "Dalam besaran saja (arah ke bawah): |v| = |v₀| + g·t dan h = |v₀|·t + ½·g·t²"],
    contoh=[
        ("Waktu tiba", "Bola dilempar ke bawah 5 m/s dari ketinggian 30 m. Tentukan waktu tiba dan kecepatannya di tanah.",
         G("vert-yt", DN30, marks=[(2, 0, "tanah")]),
         ["0 = 30 − 5t − 5t² → t² + t − 6 = 0 → (t + 3)(t − 2) = 0 → t = 2 s.", "v = −5 − 10 · 2 = −25 m/s."], "2 s; 25 m/s ke bawah"),
        ("Tanpa waktu", "Batu dilempar ke bawah 10 m/s dari ketinggian 40 m. Berapa kelajuannya di tanah?",
         None, ["v² = (−10)² − 2 · 10 · (0 − 40) = 100 + 800 = 900.", "|v| = 30 m/s."], "30 m/s"),
    ],
    bertahap=dict(
        soal="Kunci dilempar ke bawah 10 m/s dari jendela setinggi 75 m. Kapan dan dengan kecepatan berapa kunci menyentuh tanah?",
        langkah=["0 = 75 − 10t − 5t² → t² + 2t − ____ = 0.", "(t + ____)(t − ____) = 0 → t = ____ s.", "v = −10 − 10 · ____ = ____ m/s."],
        cek="Kecepatan awal ditulis −10 m/s karena",
        opsi=["(a) arahnya ke bawah, sedangkan arah positif ke atas", "(b) kunci melambat"],
        kunci="15; (t + 5)(t − 3), t = 3 s; v = −40 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Jangan memakai rumus jatuh bebas (v₀ = 0) untuk benda yang dilempar.",
        "Persamaan kuadrat waktu menghasilkan dua akar; akar negatif tidak bermakna di sini.",
        "Tanda v₀ dan g harus konsisten dengan arah positif yang dipilih.",
    ],
    latihan=[
        Q(1, "Bola dilempar ke bawah 5 m/s. Berapa kecepatannya setelah 2 s?", "25 m/s ke bawah", "v = −5 − 20 = −25 m/s."),
        Q(1, "Berapa jarak yang ditempuh bola itu selama 2 s?", "30 m", "5 · 2 + 5 · 4 = 30 m."),
        Q(1, "Batu dilempar ke bawah 10 m/s dan jatuh sejauh 15 m. Berapa kelajuannya sekarang?", "20 m/s", "v² = 100 + 2 · 10 · 15 = 400."),
        Q(1, "Grafik v–t sebuah bola ditunjukkan di bawah. Tentukan kecepatan awal dan percepatannya.", "−5 m/s; −10 m/s²", "Garis mulai di −5 m/s dan turun 10 m/s setiap sekon.",
          fig=G("vert-vt", fall(35, -5, 3))),
        Q(1, "Dari ketinggian yang sama, bola A dijatuhkan dan bola B dilempar ke bawah. Mana yang tiba lebih dulu?", "bola B", "B sudah punya kecepatan awal ke bawah, percepatannya sama."),
        Q(2, "Bola dilempar ke bawah 10 m/s dari ketinggian 40 m. Kapan bola menyentuh tanah dan berapa kecepatannya?", "2 s; 30 m/s ke bawah",
          "t² + 2t − 8 = 0 → (t + 4)(t − 2) = 0 → t = 2 s; v = −10 − 20 = −30 m/s."),
        Q(2, "Batu dilempar ke bawah 10 m/s dari ketinggian 45 m. Berapa kelajuannya saat berada 25 m di atas tanah?", f"√500 ≈ {n(math.sqrt(500))} m/s",
          "Batu sudah turun 20 m: v² = 100 + 2 · 10 · 20 = 500."),
        Q(2, "Grafik y–t sebuah bola yang dilempar ke bawah ditunjukkan di bawah. Kapan bola menyentuh tanah, dan di mana posisinya pada t = 1 s?", "2 s; 25 m",
          "Grafik memotong y = 0 pada t = 2 s; y(1) = 40 − 10 − 5 = 25 m.", fig=G("vert-yt", DN40)),
        Q(2, "Pada bingkai di bawah, gambarlah grafik v–t bola yang dilempar ke bawah 10 m/s dari menara tinggi selama 3 s.", "garis lurus dari (0, −10) ke (3, −40)",
          "v = −10 − 10t.", fig=G("vert-vt"), kfig=G("vert-vt", fall(100, -10, 3), w=240, h=150)),
        Q(3, "Bola A dijatuhkan dari puncak menara. Tepat 1 s kemudian, bola B dilempar ke bawah 10 m/s dari tempat yang sama. Apakah B dapat menyusul A sebelum keduanya menyentuh tanah?", "tidak; jaraknya tetap 5 m",
          "Saat B dilempar, A sudah turun 5 m dan bergerak 10 m/s, sama dengan kecepatan awal B. Percepatan keduanya sama, jadi selisih kecepatan nol dan jaraknya tetap 5 m."),
        Q(3, "Bola dilempar ke bawah dari ketinggian 60 m dan tiba di tanah 2 s kemudian. Berapa kecepatan lemparnya?", "20 m/s ke bawah", "60 = 2v₀ + 5 · 4 → v₀ = 20 m/s."),
        Q(3, "Dari jembatan setinggi 45 m, batu A dijatuhkan dan batu B dilempar ke bawah bersamaan. B tiba 1 s lebih awal. Berapa kecepatan lempar B?", "12,5 m/s",
          "A tiba setelah 3 s, jadi B setelah 2 s: 45 = 2v₀ + 20 → v₀ = 12,5 m/s."),
    ],
))

# ================================================================== Subbab 3: vertikal ke atas
UP20 = fall(0, 20, 4)
UP25 = fall(0, 25, 5)
SUB.append(dict(
    title="Gerak Vertikal ke Atas",
    tujuan="Menganalisis benda yang dilempar ke atas: titik tertinggi, waktu naik dan turun, serta kecepatan pada setiap ketinggian.",
    konsep=[
        "Benda yang dilempar ke atas diperlambat oleh gravitasi sampai berhenti sesaat di <b>titik tertinggi</b>, lalu jatuh kembali. Seluruh gerak itu cukup dihitung dengan <b>satu</b> persamaan GLBB dengan a = −g; tidak perlu dipecah menjadi gerak naik dan turun.",
        "Di titik tertinggi <b>v = 0 tetapi a = −g</b>, bukan nol: kecepatannya sedang berubah dari positif ke negatif.",
        "Gerak ini <b>simetris</b>: waktu naik sama dengan waktu turun ke ketinggian awal, dan pada setiap ketinggian kelajuan naik sama dengan kelajuan turun.",
    ],
    rumus=["v = v₀ − g·t; y = y₀ + v₀·t − ½·g·t²", "Titik tertinggi: t<sub>puncak</sub> = " + fr("v₀", "g") + "; h<sub>maks</sub> = " + fr("v₀²", "2g"),
           "Kembali ke ketinggian awal: t = " + fr("2v₀", "g") + ", dengan kelajuan v₀", "v² = v₀² − 2g·(y − y₀)"],
    contoh=[
        ("Satu lemparan, dua grafik", "Bola dilempar ke atas 20 m/s dari tanah. Tentukan waktu ke puncak, tinggi maksimum, dan kapan bola kembali. Gambarkan grafik y–t dan v–t-nya.",
         '<div class="two">' + G("vert-yt", UP20, w=260, h=170, marks=[(2, 20, "puncak")]) + G("vert-vt", UP20, w=260, h=170) + "</div>",
         ["t<sub>puncak</sub> = 20 : 10 = 2 s; h<sub>maks</sub> = 400 : 20 = 20 m.", "Kembali pada t = 4 s dengan v = −20 m/s.",
          "Grafik v–t memotong sumbu t pada puncak (t = 2 s); luas segitiga di atas sumbu = 20 m = tinggi maksimum."], "2 s; 20 m; kembali pada t = 4 s"),
        ("Dua kali di ketinggian yang sama", "Untuk bola yang sama, kapan bola berada 15 m di atas tanah, dan berapa kecepatannya saat itu?",
         None, ["15 = 20t − 5t² → t² − 4t + 3 = 0 → t = 1 s atau t = 3 s.", "v(1) = 10 m/s (naik); v(3) = −10 m/s (turun)."], "t = 1 s (naik 10 m/s) dan t = 3 s (turun 10 m/s)"),
    ],
    bertahap=dict(
        soal="Bola dilempar ke atas 30 m/s dari tanah. Tentukan t<sub>puncak</sub>, h<sub>maks</sub>, dan kapan bola berada 25 m di atas tanah.",
        langkah=["t<sub>puncak</sub> = 30 : 10 = ____ s.", "h<sub>maks</sub> = 30² : 20 = ____ m.", "25 = 30t − 5t² → t² − 6t + 5 = 0 → t = ____ s atau t = ____ s."],
        cek="Ada dua jawaban waktu karena",
        opsi=["(a) bola melewati ketinggian itu saat naik dan saat turun", "(b) salah satu akarnya harus dibuang"],
        kunci="3 s; 45 m; t = 1 s atau t = 5 s. Alasan: (a).",
    ),
    jebakan=[
        "Di titik tertinggi kecepatan nol, tetapi percepatan tetap g ke bawah.",
        "Persamaan posisi bisa memberi dua akar positif: saat naik dan saat turun. Keduanya bermakna.",
        "Waktu naik sama dengan waktu turun hanya bila benda kembali ke ketinggian awalnya.",
    ],
    latihan=[
        Q(1, "Bola dilempar ke atas 15 m/s. Kapan bola mencapai titik tertinggi?", "1,5 s", "15 : 10."),
        Q(1, "Bola dilempar ke atas 10 m/s. Berapa tinggi maksimumnya?", "5 m", "100 : 20."),
        Q(1, "Bola dilempar ke atas 25 m/s dan ditangkap kembali pada ketinggian lempar. Berapa lama bola di udara?", "5 s", "2 · 25 : 10."),
        Q(1, "Berapa percepatan bola tepat di titik tertingginya?", "10 m/s² ke bawah", "Gravitasi tetap bekerja; hanya kecepatannya yang nol."),
        Q(1, "Bola dilempar ke atas 20 m/s. Berapa kecepatannya setelah 3 s?", "10 m/s ke bawah", "v = 20 − 30 = −10 m/s."),
        Q(2, "Grafik y–t sebuah bola yang dilempar ke atas dari tanah ditunjukkan di bawah. Kapan bola di puncak dan berapa lama bola di udara?", "2,5 s; 5 s",
          "Puncak grafik pada t = 2,5 s; kembali ke y = 0 pada t = 5 s.", fig=G("vert-yt", UP25)),
        Q(2, "Bola dilempar ke atas 25 m/s. Kapan bola berada 20 m di atas titik lempar, dan berapa kecepatannya saat itu?", "t = 1 s (15 m/s naik) dan t = 4 s (15 m/s turun)",
          "20 = 25t − 5t² → t² − 5t + 4 = 0 → t = 1 atau 4; v = 25 − 10t."),
        Q(2, "Grafik v–t sebuah bola ditunjukkan di bawah. Kapan bola di puncak, dan berapa tinggi maksimumnya di atas titik lempar?", "2 s; 20 m",
          "v = 0 pada t = 2 s; luas segitiga ½ · 2 · 20 = 20 m.", fig=G("vert-vt", UP20)),
        Q(2, "Bola ditangkap kembali 4 s setelah dilempar ke atas. Berapa kecepatan lempar dan tinggi maksimumnya?", "20 m/s; 20 m", "Naik 2 s → v₀ = 20 m/s; h = 400 : 20."),
        Q(3, "Roket air A dan B diluncurkan tegak bersamaan dengan kecepatan awal 20 m/s dan 35 m/s. Berapa selisih ketinggian keduanya setelah 1,5 s?", "22,5 m",
          "h<sub>A</sub> = 30 − 11,25 = 18,75 m; h<sub>B</sub> = 52,5 − 11,25 = 41,25 m. Selisihnya = (35 − 20) · 1,5 = 22,5 m."),
        Q(3, "Dari atap setinggi 25 m, bola dilempar ke atas 20 m/s. Kapan bola menyentuh tanah dan berapa kecepatannya?", "5 s; 30 m/s ke bawah",
          "0 = 25 + 20t − 5t² → t² − 4t − 5 = 0 → t = 5 s; v = 20 − 50 = −30 m/s."),
        Q(3, "Bola A dilempar ke atas 20 m/s dari tanah. Pada saat yang sama, bola B dijatuhkan dari ketinggian 40 m tepat di atasnya. Kapan dan di mana keduanya bertemu?", "t = 2 s, pada ketinggian 20 m",
          "20t − 5t² = 40 − 5t² → t = 2 s; y = 20 m. Saat itu A tepat di puncak (v = 0)."),
    ],
))

# ================================================================== Subbab 4: kasus nyata dan dua benda
TOWER = fall(40, 10, 4)
A9, B9 = fall(0, 15, 2, "A", BLUE), fall(30, 0, 2, "B", RED)
SUB.append(dict(
    title="Kasus Nyata dan Dua Benda",
    tujuan="Menyelesaikan gerak vertikal dari ketinggian tertentu, dua benda yang bergerak bersamaan, dan menjelaskan pengaruh hambatan udara.",
    konsep=[
        "Benda yang dilempar ke atas dari ketinggian y₀ tetap memakai y = y₀ + v₀t − ½gt². Benda menyentuh tanah saat y = 0.",
        "Untuk <b>dua benda</b>, tulis persamaan posisi masing-masing dengan jam yang sama dan titik acuan yang sama, lalu samakan: y<sub>A</sub>(t) = y<sub>B</sub>(t).",
        "<b>Hambatan udara</b> bertambah besar bila benda bergerak lebih cepat. Pada penerjun payung, hambatan udara akhirnya sama besar dengan berat, sehingga percepatannya nol dan ia jatuh dengan <b>kecepatan terminal</b> yang tetap.",
    ],
    rumus=["y = y₀ + v₀·t − ½·g·t²; menyentuh tanah saat y = 0", "Bertemu: y<sub>A</sub>(t) = y<sub>B</sub>(t)", "Benda di tempat yang sama yang dilempar ke atas dan ke bawah dengan kelajuan sama tiba dengan kelajuan sama; selisih waktunya 2v₀/g"],
    contoh=[
        ("Dilempar ke atas dari menara", "Batu dilempar ke atas 10 m/s dari menara setinggi 40 m. Kapan batu menyentuh tanah dan berapa kecepatannya?",
         G("vert-yt", TOWER, marks=[(1, 45, "puncak")]),
         ["0 = 40 + 10t − 5t² → t² − 2t − 8 = 0 → (t − 4)(t + 2) = 0 → t = 4 s.", "v = 10 − 40 = −30 m/s."], "4 s; 30 m/s ke bawah"),
        ("Air mancur", "Air keluar tegak ke atas dari air mancur dengan kecepatan 15 m/s. Seberapa tinggi semburannya, dan berapa lama setetes air berada di udara?",
         None, ["h = 15² : 20 = 11,25 m.", "Waktu di udara = 2 · 15 : 10 = 3 s."], "11,25 m; 3 s"),
    ],
    bertahap=dict(
        soal="Bola A dilempar ke atas 25 m/s dari tanah. Pada saat yang sama, bola B dijatuhkan dari ketinggian 50 m tepat di atasnya. Kapan dan di mana keduanya bertemu?",
        langkah=["y<sub>A</sub> = 25t − 5t² dan y<sub>B</sub> = 50 − 5t².", "25t − 5t² = 50 − 5t² → t = ____ s.", "y = 50 − 5 · ____ = ____ m.", "v<sub>A</sub> = 25 − 10 · 2 = ____ m/s; v<sub>B</sub> = ____ m/s."],
        cek="Suku −5t² hilang dari kedua ruas karena",
        opsi=["(a) kedua bola mendapat percepatan yang sama", "(b) kedua bola bergerak searah"],
        kunci="t = 2 s; y = 30 m; v<sub>A</sub> = 5 m/s (masih naik), v<sub>B</sub> = −20 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Untuk dua benda, gunakan satu jam dan satu titik acuan. Jangan mengukur posisi B dari tempat B dilepas.",
        "Kelajuan saat menyentuh tanah tidak bergantung pada arah lemparan (atas atau bawah) bila kelajuan awal dan ketinggiannya sama.",
        "Dengan hambatan udara, benda ringan yang lebar (kertas, bulu) jatuh lebih lambat; tanpa udara, semua benda jatuh bersamaan.",
    ],
    latihan=[
        Q(1, "Air mancur menyemburkan air tegak ke atas dengan kecepatan 10 m/s. Seberapa tinggi semburannya?", "5 m", "100 : 20."),
        Q(1, "Pemain voli melompat tegak dengan kecepatan awal 4 m/s. Seberapa tinggi lompatannya dan berapa lama ia di udara?", "0,8 m; 0,8 s", "16 : 20 = 0,8 m; 2 · 4 : 10 = 0,8 s."),
        Q(1, "Bola dilempar ke atas 10 m/s dari balkon setinggi 15 m. Berapa tinggi maksimumnya dari tanah?", "20 m", "15 + 100 : 20 = 20 m."),
        Q(1, "Mengapa penerjun payung akhirnya jatuh dengan kecepatan tetap?", "hambatan udara menjadi sama besar dengan beratnya",
          "Hambatan udara bertambah seiring kecepatan; saat sama dengan berat, gaya total nol sehingga percepatan nol."),
        Q(1, "Bola dilempar ke atas 12 m/s. Di mana bola setelah 2 s, dan sedang naik atau turun?", "4 m di atas titik lempar, sedang turun", "y = 24 − 20 = 4 m; v = 12 − 20 = −8 m/s."),
        Q(2, "Bola dilempar ke atas 10 m/s dari atap setinggi 15 m. Kapan bola menyentuh tanah dan berapa kecepatannya?", "3 s; 20 m/s ke bawah",
          "0 = 15 + 10t − 5t² → t² − 2t − 3 = 0 → t = 3 s; v = 10 − 30 = −20 m/s."),
        Q(2, "Seekor kanguru melompat setinggi 1,8 m. Berapa kecepatan tegak awalnya dan berapa lama ia di udara?", "6 m/s; 1,2 s", "v₀ = √(2 · 10 · 1,8) = 6 m/s; t = 2 · 6 : 10 = 1,2 s."),
        Q(2, "Dua bola dilempar ke atas 20 m/s dari tanah dengan selang 1 s. Kapan dan pada ketinggian berapa keduanya bertemu?", "t = 2,5 s (sejak bola pertama), 18,75 m",
          "20t − 5t² = 20(t − 1) − 5(t − 1)² → 0 = 10t − 25 → t = 2,5 s; y = 50 − 31,25 = 18,75 m."),
        Q(2, "Grafik y–t bola A (dilempar ke atas dari tanah) dan bola B (dijatuhkan) ditunjukkan di bawah. Kapan dan di mana keduanya bertemu?", "t = 2 s, pada ketinggian 10 m",
          "Titik potong grafik: 15t − 5t² = 30 − 5t² → t = 2 s; y = 10 m.", fig=G("vert-yt", A9, B9)),
        Q(3, "Dari atap setinggi 20 m, bola P dilempar ke atas 10 m/s dan bola Q dilempar ke bawah 10 m/s. Bandingkan kelajuan dan waktu tiba keduanya di tanah.", "kelajuan sama (≈ 22,4 m/s); P tiba 2 s lebih lambat",
          f"Keduanya: v² = 100 + 400 = 500. Q: t² + 2t − 4 = 0 → t ≈ {n(t_hit(20, -10))} s. P: t² − 2t − 4 = 0 → t ≈ {n(t_hit(20, 10))} s. Selisih = 2 · 10 : 10 = 2 s (waktu naik dan turun kembali ke atap)."),
        Q(3, "Bola dilempar ke atas dari jendela setinggi 20 m dan menyentuh tanah 4 s kemudian. Berapa kecepatan lemparnya?", "15 m/s", "0 = 20 + 4v₀ − 80 → v₀ = 15 m/s."),
        Q(3, "Penumpang lift yang naik dengan kecepatan tetap 2 m/s menjatuhkan koin dari ketinggian 1,8 m di atas lantai lift. Berapa lama koin sampai di lantai lift?", "0,6 s",
          "Lift bergerak tetap, jadi menurut penumpang koin jatuh bebas seperti di lantai diam: t = √(2 · 1,8 : 10) = 0,6 s."),
    ],
))

# ================================================================== Subbab 5: data pelacakan gerak vertikal
TS = [k * 0.05 for k in range(13)]                         # 0 … 0,6 s
DROP_V = noisy(lambda t: -10 * t, TS, 0.25, 3)             # contoh 5.1
UP_V = noisy(lambda t: 3 - 10 * t, TS, 0.25, 17)           # bertahap
DROP_V2 = noisy(lambda t: -10 * t, TS, 0.3, 29)            # latihan 5.6
PAPER_V = noisy(lambda t: -6 * t, TS, 0.25, 31)            # latihan 5.7 (kertas, hambatan udara)
SUB.append(dict(
    title="Mengukur g dengan Video dan Ponsel",
    tujuan="Menentukan percepatan gravitasi dari data pelacakan gerak dan menjelaskan derau serta pengaruh hambatan udara pada data.",
    konsep=[
        "Rekaman video sebuah bola yang jatuh dapat dianalisis dengan aplikasi pelacak gerak: setiap bingkai video memberi satu posisi y. Dari data itu diperoleh grafik y–t (parabola) dan v–t (garis lurus). <b>Kemiringan garis terbaik v–t adalah −g.</b>",
        "Cara tanpa grafik: pada selang waktu yang sama Δt, selisih dua perpindahan berurutan tetap, yaitu g·(Δt)².",
        "Akselerometer ponsel tidak mengukur gravitasi secara langsung. Ponsel yang diam di meja menunjukkan sekitar 9,8 m/s², sedangkan ponsel yang jatuh bebas menunjukkan sekitar 0. Jadi untuk mengukur g, analisis video lebih mudah ditafsirkan.",
    ],
    rumus=["g ≈ −(kemiringan garis terbaik grafik v–t)", "Selisih perpindahan berurutan = g·(Δt)²", "Video 30 bingkai per sekon: Δt = 1/30 s antara dua bingkai"],
    contoh=[
        ("Garis terbaik v–t", "Kecepatan bola yang dijatuhkan diperoleh dari video setiap 0,05 s (titik). Garis merah adalah garis terbaik. Tentukan g.",
         render(TP["data-vyt"], points=DROP_V, lines=[(0, 0, 0.6, -6, False)]),
         ["Garis melalui (0, 0) dan (0,6 ; −6).", "Kemiringan = −6 : 0,6 = −10 m/s², jadi g ≈ 10 m/s². (Nilai baku g di Bumi ≈ 9,8 m/s².)"], "g ≈ 10 m/s²"),
        ("Selisih perpindahan", "Posisi bola yang dijatuhkan, diukur setiap 0,1 s: y = 2,00; 1,95; 1,80; 1,55; 1,20 m. Tentukan g.",
         None, ["Perpindahan tiap 0,1 s: −0,05; −0,15; −0,25; −0,35 m.", "Selisih berurutan tetap −0,10 m.", "g = 0,10 : (0,1)² = 10 m/s²."], "g = 10 m/s²"),
    ],
    bertahap=dict(
        soal="Kecepatan bola yang dilempar ke atas diperoleh dari video (titik). Garis merah adalah garis terbaik. Tentukan kecepatan awal, g, dan kapan bola di puncak.",
        fig=render(TP["data-vyt"], points=UP_V, lines=[(0, 3, 0.6, -3, False)]),
        langkah=["Garis memotong sumbu v di v₀ = ____ m/s.", "Kemiringan = (−3 − 3) : 0,6 = ____ m/s², jadi g ≈ ____ m/s².", "Puncak saat v = 0, yaitu t = ____ s."],
        cek="Titik data tidak tepat berada di garis karena",
        opsi=["(a) ada derau dari pengukuran video", "(b) percepatannya berubah-ubah"],
        kunci="3 m/s; −10, g ≈ 10 m/s²; t = 0,3 s. Alasan: (a).",
    ),
    jebakan=[
        "Jangan menghitung g dari dua titik data yang berdekatan; deraunya terlalu berpengaruh.",
        "Pakai skala di bidang jatuh bola (misalnya penggaris 1 m di belakang bola) agar ukuran piksel dapat diubah ke meter dengan benar.",
        "Benda ringan yang lebar mendapat hambatan udara besar, sehingga datanya memberi nilai lebih kecil dari g.",
    ],
    latihan=[
        Q(1, "Mengapa akselerometer ponsel yang sedang jatuh bebas menunjukkan sekitar 0?", "sensor hanya merasakan gaya selain gravitasi; saat jatuh bebas tidak ada",
          "Di meja, meja menahan ponsel sehingga sensor menunjukkan ≈ 9,8 m/s²."),
        Q(1, "Perpindahan bola tiap 0,1 s tercatat 0,05; 0,15; 0,25; 0,35 m. Gerak apa ini?", "GLBB", "Selisih berurutan tetap (0,10 m)."),
        Q(1, "Sebuah video direkam 30 bingkai per sekon. Berapa selang waktu antara dua bingkai berurutan?", "1/30 s ≈ 0,033 s", "1 : 30."),
        Q(1, "Garis terbaik grafik v–t bola jatuh melalui (0, 0) dan (0,5 ; −5). Berapa g?", "10 m/s²", "−5 : 0,5 = −10 m/s²."),
        Q(2, "Posisi bola yang dijatuhkan, setiap 0,1 s: y = 2,00; 1,95; 1,80; 1,55; 1,20; 0,75 m. Tentukan g dengan selisih perpindahan.", "10 m/s²",
          "Perpindahan: 0,05; 0,15; 0,25; 0,35; 0,45 m (ke bawah); selisih 0,10 m; g = 0,10 : 0,01."),
        Q(2, "Data kecepatan bola jatuh dari video ditunjukkan di bawah, dengan garis terbaiknya. Tentukan g.", "10 m/s²",
          "Garis melalui (0, 0) dan (0,6 ; −6): kemiringan −10 m/s².", fig=render(TP["data-vyt"], points=DROP_V2, lines=[(0, 0, 0.6, -6, False)])),
        Q(2, "Data kecepatan selembar kertas lipat yang dijatuhkan ditunjukkan di bawah. Berapa percepatannya, dan mengapa lebih kecil dari g?", "sekitar 6 m/s²; hambatan udara",
          "Garis melalui (0, 0) dan (0,5 ; −3): −3 : 0,5 = −6 m/s². Hambatan udara melawan gerak kertas.",
          fig=render(TP["data-vyt"], points=PAPER_V, lines=[(0, 0, 0.5, -3, False)])),
        Q(2, "Posisi bola yang dilempar ke atas tercatat setiap 0,1 s: y = 0; 0,25; 0,40; 0,45; 0,40; 0,25 m. Kapan bola di puncak, dan berapa kecepatan awalnya?", "0,3 s; 3 m/s",
          "Data simetris terhadap t = 0,3 s (y = 0,45 m). v₀ = g · t<sub>puncak</sub> = 10 · 0,3 = 3 m/s."),
        Q(3, f"Data kecepatan bola jatuh (setiap 0,05 s): v = {'; '.join(n(v) for _, v in DROP_V2[:6])} m/s. Hitung g dari (a) dua titik pertama, (b) titik pertama dan keenam. Mana yang lebih dapat dipercaya?",
          f"(a) {n(-(DROP_V2[1][1] - DROP_V2[0][1]) / 0.05)} m/s²; (b) {n(-(DROP_V2[5][1] - DROP_V2[0][1]) / 0.25)} m/s²; cara (b)",
          "Cara (b) memakai selang lebih panjang, jadi derau 0,1–0,3 m/s hanya sedikit memengaruhi hasil."),
        Q(3, "Bola dijatuhkan dari keadaan diam dan video menunjukkan bola turun 1,25 m dalam 0,5 s. Berapa g menurut data ini?", "10 m/s²", "1,25 = ½ · g · 0,25 → g = 10 m/s²."),
        Q(3, "Susun langkah percobaan mengukur g dengan video ponsel.", "contoh: pasang penggaris di bidang jatuh, ponsel di tripod tegak lurus, rekam, lacak, buat grafik v–t, ambil kemiringan",
          "Ulangi beberapa kali dan rata-ratakan; pakai bola kecil yang berat agar hambatan udara kecil; kamera cukup jauh agar perspektif tidak membelokkan skala."),
    ],
))

CAMPURAN = [
    Q(1, "Bola dijatuhkan dari ketinggian 20 m. Berapa lama sampai ke tanah?", "2 s", "√4."),
    Q(1, "Bola dilempar ke atas 30 m/s. Berapa tinggi maksimumnya?", "45 m", "900 : 20."),
    Q(1, "Grafik v–t gerak vertikal berupa garis lurus dengan kemiringan −10 m/s². Apa arti kemiringan itu?", "percepatan gravitasi ke bawah", "a = −g."),
    Q(1, "Bola dilempar ke bawah 15 m/s. Berapa kecepatannya setelah 1 s?", "25 m/s ke bawah", "−15 − 10."),
    Q(2, "Bola dilempar ke atas 20 m/s dari tanah. Di mana bola dan bagaimana kecepatannya pada t = 3 s?", "15 m di atas tanah, 10 m/s ke bawah", "y = 60 − 45; v = 20 − 30."),
    Q(2, "Bola dilempar ke atas dari tanah dan kembali ke tangan setelah 6 s. Berapa tinggi maksimumnya?", "45 m", "Naik 3 s → v₀ = 30 m/s; 900 : 20."),
    Q(2, "Benda dilempar ke bawah 5 m/s dari ketinggian 10 m. Berapa kelajuannya di tanah?", "15 m/s", "v² = 25 + 200 = 225."),
    Q(2, "Posisi bola tiap 0,2 s (jatuh dari diam): turun 0,2; 0,6; 1,0; 1,4 m dalam selang berurutan. Tentukan g.", "10 m/s²", "Selisih 0,4 m; 0,4 : 0,04."),
    Q(2, "Bola A dilempar ke atas 30 m/s dari tanah; bola B dijatuhkan dari 60 m tepat di atasnya pada saat yang sama. Kapan keduanya bertemu?", "2 s", "30t = 60."),
    Q(3, "Dari atap setinggi 35 m, bola dilempar ke atas 30 m/s. Kapan bola menyentuh tanah?", "7 s", "0 = 35 + 30t − 5t² → t² − 6t − 7 = 0 → t = 7 s."),
]

# ------------------------------------------------------------------ TKA-level items
UP25B = fall(0, 25, 5)
TKA = [
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Dari puncak gedung setinggi 35 m, sebuah bola dilempar tegak ke atas dengan kecepatan 30 m/s (g = 10 m/s²). Bola kemudian jatuh melewati tepi gedung sampai ke tanah. Waktu yang diperlukan bola dari dilempar sampai menyentuh tanah adalah ....",
         opsi=["3 s", "6 s", "7 s", "8 s", "9 s"], kunci=2,
         bahas="0 = 35 + 30t − 5t² → t² − 6t − 7 = 0 → (t − 7)(t + 1) = 0 → t = 7 s.",
         salah="A: waktu ke puncak saja. B: waktu kembali ke ketinggian gedung (2v₀/g). D, E: tidak sesuai persamaan."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Grafik v–t sebuah bola yang dilempar tegak ke atas dari tanah ditunjukkan di bawah.", fig=G("vert-vt", UP25B, w=280, h=170),
         soal2="Pernyataan yang tepat tentang gerak bola adalah ....",
         opsi=["Bola mencapai puncak pada t = 2,5 s, setinggi 31,25 m, dan kembali ke tanah pada t = 5 s.", "Bola berhenti selama 2,5 s di puncak.",
               "Percepatan bola nol pada t = 2,5 s.", "Bola mencapai puncak pada t = 5 s.", "Tinggi maksimum bola 62,5 m."], kunci=0,
         bahas="v = 0 pada t = 2,5 s; luas segitiga ½ · 2,5 · 25 = 31,25 m; luas total di atas dan di bawah sumbu sama, jadi kembali pada t = 5 s.",
         salah="B: v = 0 hanya sesaat. C: kemiringan tetap −10 m/s². D: itu saat kembali. E: lupa ½ pada luas segitiga."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Grafik y–t sebuah bola yang dilempar tegak ke atas dari tanah ditunjukkan di bawah.", fig=G("vert-yt", UP20, w=280, h=170),
         soal2="Grafik v–t yang sesuai adalah ....", opsi="VT", kunci=2,
         bahas="v₀ = 20 m/s (puncak pada t = 2 s, tinggi 20 m), lalu turun lurus dengan kemiringan −10 m/s² sampai −20 m/s pada t = 4 s.",
         salah="A: tanda terbalik. B: kecepatan dianggap nol setelah puncak. D: menyalin bentuk grafik y–t."),
    dict(tipe="FIS-KONSEP", lv=2, fmt="pgk",
         soal="Sebuah bola dilempar tegak ke atas dan ditangkap kembali pada ketinggian yang sama. Hambatan udara diabaikan. Pernyataan yang benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["Di titik tertinggi kecepatan bola nol, tetapi percepatannya 10 m/s² ke bawah.", "Bola yang lebih berat naik lebih rendah meskipun kecepatan awalnya sama.",
               "Waktu naik sama dengan waktu turun.", "Arah percepatan berubah menjadi ke atas saat bola turun.", "Kelajuan bola saat ditangkap sama dengan kelajuan lemparnya."], kunci=[0, 2, 4],
         bahas="A, C, E sesuai sifat gerak vertikal tanpa hambatan udara.", salah="B: tinggi tidak bergantung pada massa. D: percepatan selalu ke bawah."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Dari atap gedung setinggi 40 m, bola P dilempar tegak ke atas dan bola Q dilempar tegak ke bawah, keduanya dengan kelajuan 15 m/s pada saat yang sama (g = 10 m/s²). Kondisi yang akan terjadi adalah ....",
         opsi=["Keduanya menyentuh tanah dengan kelajuan sama, tetapi P tiba 3 s lebih lambat.", "Q menyentuh tanah dengan kelajuan lebih besar karena dilempar ke bawah.",
               "Keduanya tiba bersamaan karena kelajuan awalnya sama.", "P menyentuh tanah dengan kelajuan lebih besar karena jatuh dari tempat lebih tinggi.",
               "Keduanya menyentuh tanah dengan kelajuan sama, dan P tiba 1,5 s lebih lambat."], kunci=0,
         bahas=f"Keduanya: v² = 15² + 2 · 10 · 40 = 1.025, v ≈ {n(math.sqrt(1025))} m/s. P naik lalu kembali ke atap setelah 2 · 15 : 10 = 3 s dengan kecepatan 15 m/s ke bawah, sama seperti Q saat dilempar; jadi P tiba 3 s lebih lambat.",
         salah="B, D: kelajuan akhir hanya bergantung pada kelajuan awal dan tinggi jatuh. C: P perlu waktu naik-turun. E: memakai waktu naik saja."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Percepatan gravitasi di permukaan Bulan sekitar 1,6 m/s². Seorang astronaut melempar bola tegak ke atas dengan kecepatan 8 m/s di Bulan, lalu melakukan lemparan yang sama di Bumi (g = 10 m/s²). Hambatan udara diabaikan. Perbandingan yang tepat adalah ....",
         opsi=["Di Bulan bola naik 20 m dan berada di udara 10 s, sekitar 6,25 kali tinggi dan lama di Bumi.", "Di Bulan bola naik 20 m, tetapi lama di udaranya sama dengan di Bumi.",
               "Di Bulan bola naik 3,2 m, sama dengan di Bumi, karena kecepatan awalnya sama.", "Di Bulan bola naik 40 m dan berada di udara 5 s.", "Di Bulan bola tidak kembali karena gravitasinya terlalu kecil."], kunci=0,
         bahas="Bulan: h = 64 : 3,2 = 20 m; t = 2 · 8 : 1,6 = 10 s. Bumi: h = 64 : 20 = 3,2 m; t = 1,6 s. Perbandingan 10 : 1,6 = 6,25.",
         salah="B: waktu juga berbanding terbalik dengan g. C: tinggi bergantung pada g. D: lupa faktor 2 pada 2g dan pada waktu. E: gravitasi tetap menarik bola kembali."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="pg",
         soal="Rina melempar kunci tegak ke atas kepada temannya di balkon yang berada 5 m di atas tangan Rina. Agar mudah ditangkap, kunci harus sampai di ketinggian balkon dengan kelajuan tidak lebih dari 5 m/s (g = 10 m/s²). Kecepatan lempar yang memenuhi syarat adalah ....",
         opsi=["8 m/s", "10,5 m/s", "12 m/s", "15 m/s", "20 m/s"], kunci=1,
         bahas="Di balkon: v² = v₀² − 100. Syarat: v₀ ≥ 10 m/s (sampai) dan v₀² − 100 ≤ 25, yaitu v₀ ≤ √125 ≈ 11,2 m/s. Hanya 10,5 m/s: kelajuannya di balkon √(110,25 − 100) ≈ 3,2 m/s.",
         salah="A: kunci tidak sampai (tinggi maksimum 3,2 m). C: tiba dengan √44 ≈ 6,6 m/s. D: ≈ 11,2 m/s. E: ≈ 17,3 m/s."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="bs",
         soal="Tim relawan akan menjatuhkan paket obat dari helikopter yang melayang diam di ketinggian 80 m. Paket rusak bila menyentuh tanah dengan kelajuan <b>lebih dari 20 m/s</b> (g = 10 m/s²). Tentukan apakah setiap strategi berikut tepat.",
         opsi=["Menjatuhkan paket langsung dari ketinggian 80 m.", "Menurunkan helikopter ke ketinggian 20 m, lalu menjatuhkan paket.",
               "Memasang parasut kecil yang membuat paket turun dengan kecepatan tetap 5 m/s.", "Menurunkan helikopter ke 20 m, lalu melempar paket ke bawah 10 m/s agar cepat sampai."],
         kunci=[False, True, True, False],
         bahas="1: √(2 · 10 · 80) = 40 m/s (Tidak Tepat). 2: √400 = 20 m/s, tidak lebih dari 20 (Tepat). 3: 5 m/s (Tepat). 4: √(100 + 400) ≈ 22,4 m/s (Tidak Tepat).", salah=""),
    dict(tipe="FIS-EKSP", lv=3, fmt="pg",
         soal="Siswa mengukur g dengan merekam bola yang dijatuhkan memakai kamera ponsel, lalu melacak posisinya dengan aplikasi. Hasilnya g = 13 m/s², jauh dari nilai baku 9,8 m/s². Penyebab yang paling mungkin adalah ....",
         opsi=["penggaris acuan diletakkan jauh di belakang bola (lebih jauh dari kamera) sehingga skala piksel ke meter salah", "bola yang dipakai terlalu berat",
               "rekaman dimulai sedikit setelah bola dilepas", "bola dijatuhkan dari ketinggian 1,5 m, bukan 2 m", "data diambil setiap 1/30 s"], kunci=0,
         bahas="Penggaris yang lebih jauh dari kamera tampak lebih kecil, sehingga satu meter dianggap berisi lebih sedikit piksel. Akibatnya jarak tempuh bola terbaca lebih besar dengan faktor tetap, dan g yang dihitung terlalu besar.",
         salah="B: bola berat justru mengurangi pengaruh hambatan udara. C: kemiringan grafik v–t tidak bergantung pada saat mulai merekam. D: ketinggian tidak memengaruhi g. E: selang waktu itu wajar."),
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Sebuah batu dijatuhkan ke dalam sumur. Bunyi batu mengenai dasar sumur terdengar 2,06 s setelah batu dilepas. Kelajuan bunyi di udara 340 m/s dan g = 10 m/s². Kedalaman sumur sekitar ....",
         opsi=["20 m", "21,2 m", "700 m", "10,3 m", "41,2 m"], kunci=0,
         bahas="Coba h = 20 m: waktu jatuh √(40 : 10) = 2 s dan waktu rambat bunyi 20 : 340 ≈ 0,06 s; jumlahnya 2,06 s.",
         salah="B: mengabaikan waktu bunyi (5 · 2,06²). C: membagi seluruh waktu dengan kelajuan bunyi. D, E: lupa ½ atau salah memakai faktor 2."),
]

GRAPH_OPTS = {
    "VT": [render(TP["vert-vt"], (Motion(0, -20, [(4, 10)]),), width=210, height=135),
           render(TP["vert-vt"], (Motion(0, 20, [(2, -10), (2, 0)]),), width=210, height=135),
           render(TP["vert-vt"], (UP20,), width=210, height=135),
           render(TP["vert-vt"], (), lines=[(0, 0, 2, 20, False), (2, 20, 4, 0, False)], width=210, height=135)
           .replace('stroke="#c0502a" stroke-width="1.6"', f'stroke="{BLUE}" stroke-width="2.2"')],
}

UJI_PG = [
    ("Benda jatuh bebas. Kecepatannya setelah 2 s adalah ....", ["10 m/s", "20 m/s", "5 m/s", "40 m/s", "2 m/s"], 1, "g · t = 20 m/s.", "A: g saja. C: g/2. D: dikali 2 lagi. E: waktunya."),
    ("Jarak yang ditempuh benda jatuh bebas selama 3 s adalah ....", ["30 m", "90 m", "45 m", "15 m", "60 m"], 2, "½ · 10 · 9.", "A: v · t tanpa kuadrat. B: lupa ½. D: ½ · 10 · 3. E: tidak ada dasar."),
    ("Waktu jatuh bebas dari ketinggian 125 m adalah ....", ["5 s", "12,5 s", "25 s", "√12,5 s", "10 s"], 0, "√(250 : 10) = 5 s.", "B: h/g. C: 2h/g tanpa akar. D: lupa faktor 2. E: tidak ada dasar."),
    ("Bola dilempar ke atas 30 m/s. Waktu mencapai puncak adalah ....", ["3 s", "6 s", "300 s", "0,33 s", "30 s"], 0, "30 : 10.", "B: waktu kembali. C: dikali. D: kebalikannya. E: v₀."),
    ("Tinggi maksimum bola pada soal 4 adalah ....", ["90 m", "45 m", "30 m", "15 m", "4,5 m"], 1, "900 : 20.", "A: lupa ½. C: v₀. D, E: tidak ada dasar."),
    ("Percepatan bola tepat di titik tertinggi lintasannya adalah ....", ["nol", "10 m/s² ke atas", "10 m/s² ke bawah", "5 m/s² ke bawah", "berubah-ubah"], 2, "Gravitasi tetap bekerja.", "A: miskonsepsi. B: arah salah. D, E: tidak sesuai."),
    ("Bola besi dan bola kertas yang dibentuk sama ukurannya dijatuhkan bersamaan di ruang hampa. Yang terjadi adalah ....", ["bola besi tiba lebih dulu", "bola kertas tiba lebih dulu", "keduanya tiba bersamaan", "bola kertas melayang", "bergantung pada ketinggian"], 2,
     "Tanpa udara, percepatannya sama.", "A, B, D: pengaruh udara atau massa yang keliru. E: tetap bersamaan dari ketinggian berapa pun."),
    ("Bola dilempar ke atas 20 m/s dari tanah. Posisinya setelah 3 s adalah ....", ["15 m di atas tanah", "60 m di atas tanah", "45 m di atas tanah", "5 m di atas tanah", "di tanah"], 0, "60 − 45 = 15 m.", "B: lupa gravitasi. C: hanya ½gt². D: tidak ada dasar. E: bola baru kembali pada t = 4 s."),
    ("Kecepatan bola pada soal 8 saat itu adalah ....", ["10 m/s ke atas", "10 m/s ke bawah", "30 m/s ke bawah", "50 m/s ke atas", "nol"], 1, "20 − 30 = −10 m/s.", "A: tanda salah. C: hanya gt. D: dijumlahkan. E: itu pada t = 2 s."),
    ("Batu dilempar ke bawah 10 m/s dari ketinggian 20 m. Kelajuannya saat menyentuh tanah adalah ....", ["20 m/s", "30 m/s", "≈ 22,4 m/s", "10 m/s", "500 m/s"], 2, "v² = 100 + 400 = 500.", "A: jatuh bebas. B: dijumlahkan 10 + 20. D: v₀. E: lupa diakar."),
    ("Bola dilempar ke atas 15 m/s dari atap setinggi 20 m. Waktu sampai menyentuh tanah adalah ....", ["3 s", "4 s", "1,5 s", "2 s", "5 s"], 1, "0 = 20 + 15t − 5t² → t² − 3t − 4 = 0 → t = 4 s.", "A: kembali ke atap. C: ke puncak. D: jatuh bebas dari 20 m. E: tidak sesuai."),
    ("Pada grafik v–t gerak vertikal (arah atas positif), kemiringan garisnya menyatakan ....", ["−g", "tinggi maksimum", "kecepatan awal", "waktu di udara", "nol"], 0, "Kemiringan v–t = percepatan = −g.", "B: luas, bukan kemiringan. C: titik potong sumbu v. D, E: tidak sesuai."),
    ("Data video bola jatuh: perpindahan tiap 0,1 s bertambah tetap 0,1 m. Nilai g menurut data adalah ....", ["1 m/s²", "10 m/s²", "0,1 m/s²", "100 m/s²", "9,8 m/s²"], 1, "0,1 : 0,01.", "A: dibagi 0,1. C: selisihnya saja. D: dibagi 0,001. E: nilai baku, bukan hasil data."),
    ("Akselerometer ponsel yang jatuh bebas menunjukkan sekitar ....", ["0", "9,8 m/s²", "19,6 m/s²", "−9,8 m/s²", "nilai yang terus bertambah"], 0, "Saat jatuh bebas tidak ada gaya selain gravitasi yang dirasakan sensor.", "B: itu saat diam di meja. C, D, E: tidak sesuai."),
    ("Bola dilempar ke atas dan kembali ke tangan setelah 6 s. Kecepatan lemparnya adalah ....", ["30 m/s", "60 m/s", "15 m/s", "10 m/s", "6 m/s"], 0, "Naik 3 s: 10 · 3.", "B: memakai 6 s. C: dibagi 2 lagi. D, E: tidak sesuai."),
]
UJI_URAIAN = [
    ("Dari menara setinggi 60 m, batu dilempar ke atas 20 m/s. (a) Berapa tinggi maksimumnya dari tanah? (b) Kapan dan dengan kecepatan berapa batu menyentuh tanah? (c) Gambarlah grafik v–t-nya.",
     "(a) 80 m; (b) 6 s, 40 m/s ke bawah", "(a) 60 + 400 : 20. (b) 0 = 60 + 20t − 5t² → t² − 4t − 12 = 0 → t = 6 s; v = 20 − 60 = −40 m/s. (c) Garis lurus dari (0, 20) ke (6, −40)."),
    ("Bola A dilempar ke atas 30 m/s dari tanah. Pada saat yang sama, bola B dijatuhkan dari ketinggian 60 m tepat di atasnya. Kapan dan di mana keduanya bertemu, dan berapa kecepatan masing-masing saat itu?",
     "t = 2 s; 40 m; v<sub>A</sub> = 10 m/s ke atas, v<sub>B</sub> = 20 m/s ke bawah", "30t = 60 → t = 2 s; y = 60 − 20 = 40 m."),
    ("Posisi bola yang dijatuhkan dari diam, diukur dari video setiap 0,1 s: y = 1,80; 1,75; 1,60; 1,35; 1,00; 0,55 m. (a) Tunjukkan bahwa geraknya GLBB. (b) Tentukan g. (c) Berapa kecepatannya pada t = 0,5 s?",
     "(b) 10 m/s²; (c) 5 m/s ke bawah", "Perpindahan: 0,05; 0,15; 0,25; 0,35; 0,45 m; selisih tetap 0,10 m. g = 0,10 : 0,01. v = 10 · 0,5."),
    ("Di Bulan (g = 1,6 m/s²), astronaut melempar bola tegak ke atas 8 m/s. (a) Kapan bola di puncak, dan berapa tingginya? (b) Bandingkan dengan lemparan yang sama di Bumi.",
     "(a) 5 s; 20 m; (b) di Bumi 0,8 s dan 3,2 m", "t = 8 : 1,6; h = 64 : 3,2. Di Bumi t = 0,8 s, h = 3,2 m: 6,25 kali lebih kecil."),
    ("Batu dijatuhkan dari atap gedung. Pada sekon terakhir sebelum menyentuh tanah, batu menempuh 35 m. Berapa tinggi gedung dan berapa lama batu jatuh?",
     "80 m; 4 s", "5t² − 5(t − 1)² = 10t − 5 = 35 → t = 4 s; h = 5 · 16 = 80 m."),
]


META = dict(
    title="Modul Gerak Vertikal", kick="Modul belajar Fisika · Fase E · Kelas X", big="Gerak Vertikal",
    subtitle="Jatuh bebas, gerak vertikal ke bawah dan ke atas sebagai GLBB dengan percepatan g: grafik, cerita, persamaan, dan pengukuran g dengan video",
    kompetensi="Peserta didik dapat menganalisis gerak vertikal (jatuh bebas, dilempar ke bawah, dan dilempar ke atas) sebagai gerak lurus berubah beraturan dengan percepatan gravitasi melalui grafik, persamaan, dan data pengukuran, serta menyelesaikan masalah sehari-hari, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Lanjutan dari modul Gerak Lurus</h2><p>Gerak vertikal adalah GLBB pada garis tegak. Semua rumus GLBB tetap berlaku; yang berubah hanya dua hal:</p><table><tr><th>Gerak Lurus</th><th>Gerak Vertikal</th></tr><tr><td>koordinat s</td><td>koordinat y, arah ke atas positif</td></tr><tr><td>percepatan a</td><td>a = −g = −10 m/s²</td></tr><tr><td>v = v₀ + at; s = s₀ + v₀t + ½at²</td><td>v = v₀ − gt; y = y₀ + v₀t − ½gt²</td></tr></table>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Selalu tulis arah positif</b> (ke atas) dan tanda setiap besaran sebelum menghitung.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b> Untuk soal menggambar, pakai bingkai grafik yang tersedia; kuncinya berupa grafik.",
          "<b>Lakukan percobaan video</b> bila memungkinkan, lalu kerjakan Subbab 5 dengan datamu sendiri.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Koordinat tegak ditulis <b>y</b> dengan arah ke atas positif; titik acuan (y = 0) adalah tanah kecuali disebut lain. g = 10 m/s² (nilai baku ≈ 9,8 m/s²), sehingga a = −10 m/s². Hambatan udara diabaikan kecuali disebutkan. Desimal ditulis dengan koma.",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>jatuh bebas, dilempar ke bawah, atau dilempar ke atas? dari tanah atau dari ketinggian? satu benda atau dua?</b>",
    tka_info=["Soal disusun meniru tipe soal Fisika pada Tes Kemampuan Akademik (TKA) SMA 2025, yang memuat gerak vertikal (misalnya roket air).",
              "<b>Level 2</b> (FIS-HITUNG, FIS-GRAF, FIS-KONSEP): menerapkan satu konsep atau membaca grafik. <b>Level 3</b> (FIS-ANALISIS, FIS-STRATEGI, FIS-EKSP): memprediksi keadaan gerak, memilih strategi, atau menelaah percobaan."],
    refleksi=["Mengapa percepatan di titik tertinggi tidak nol?", "Kapan persamaan posisi memberi dua jawaban waktu, dan apa artinya?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th></th><th>Jatuh bebas</th><th>Dilempar ke bawah</th><th>Dilempar ke atas</th></tr>"
        "<tr><th>v₀</th><td>0</td><td>negatif</td><td>positif</td></tr>"
        "<tr><th>Kecepatan</th><td colspan='3'>v = v₀ − gt</td></tr>"
        "<tr><th>Posisi</th><td colspan='3'>y = y₀ + v₀t − ½gt²</td></tr>"
        "<tr><th>Tanpa waktu</th><td colspan='3'>v² = v₀² − 2g(y − y₀)</td></tr>"
        "<tr><th>Rumus khusus</th><td>t = √(2h/g); |v| = √(2gh)</td><td>pakai persamaan umum</td><td>t<sub>puncak</sub> = v₀/g; h<sub>maks</sub> = v₀²/2g; kembali setelah 2v₀/g</td></tr>"
        "<tr><th>Grafik v–t</th><td colspan='3'>garis lurus dengan kemiringan −g; luas = perpindahan</td></tr></table>"
        '<div class="two">' + G("vert-yt", UP20, w=260, h=160, note="dilempar ke atas: y–t") + G("vert-vt", UP20, w=260, h=160, note="dilempar ke atas: v–t") + "</div>"),
    jebakan5=["Di titik tertinggi v = 0 tetapi a = −g.", "Tanpa hambatan udara, massa tidak memengaruhi gerak jatuh.",
              "Kecepatan ke bawah bertanda negatif; jangan mencampur tanda.", "Dua akar positif berarti melewati ketinggian itu saat naik dan saat turun.",
              "Untuk dua benda, pakai satu jam dan satu titik acuan."],
    guru=["Materi mengikuti Kurikulum Merdeka Fisika SMA Fase E, sebagai lanjutan modul Gerak Lurus. Gerak dua dimensi (parabola) dibahas di modul berikutnya.",
          "Modul memakai g = 10 m/s² agar hitungan bersih; nilai baku sekitar 9,8 m/s² disebut di Subbab 1 dan 5.",
          "Data video di Subbab 5 adalah data simulasi dengan derau buatan; garis terbaik yang digambar sudah dicek terhadap regresi kuadrat terkecil. Ganti dengan data rekaman kelas bila tersedia.",
          "Soal setara TKA meniru tipe soal TKA Fisika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


def check():
    c = close
    c(t_hit(45, 0), 3); c(D45.v(3), -30); c(math.sqrt(2 * g * 45), 30)
    c(t_hit(20, 0), 2); c(20 - 5, 15); c(t_hit(80, 0), 4); c(math.sqrt(2 * g * 5), 10); c(D80.v(2.5), -25)
    c(45 - 20, 25); c(45 - 5 * 4, 25); c(5 * 9, 45)
    c(t_hit(80, 0) - 1, 3); c(80 - 5 * 9, 35)
    # subbab 2
    c(t_hit(30, -5), 2); c(DN30.v(2), -25); c(math.sqrt(100 + 800), 30); c(t_hit(75, -10), 3); c(DN75.v(3), -40)
    c(5 * 2 + 5 * 4, 30); c(math.sqrt(100 + 300), 20); c(t_hit(40, -10), 2); c(DN40.s(1), 25); c(math.sqrt(500), 22.36, 0.01)
    c((60 - 20) / 2, 20); c((45 - 20) / 2, 12.5)
    # subbab 3
    c(UP20.s(2), 20); c(UP20.v(4), -20); c(UP20.s(1), 15); c(UP20.s(3), 15); c(UP25.s(2.5), 31.25); c(UP25.s(5), 0)
    c(25 * 1 - 5, 20); c(25 * 4 - 80, 20); c(30 * 1.5 - 5 * 2.25, 33.75); c(20 * 1.5 - 11.25, 18.75); c(35 * 1.5 - 11.25, 41.25)
    c(t_hit(25, 20), 5); c(20 - 50, -30)
    # subbab 4
    c(t_hit(40, 10), 4); c(TOWER.v(4), -30); c(15 ** 2 / 20, 11.25); c(16 / 20, 0.8); c(t_hit(15, 10), 3); c(math.sqrt(36), 6)
    c(20 * 2.5 - 5 * 6.25, 18.75); c(A9.s(2), B9.s(2)); c(A9.s(2), 10)
    c(t_hit(20, 10) - t_hit(20, -10), 2); c(t_hit(20, 15), 4); c(math.sqrt(2 * 1.8 / 10), 0.6)
    # subbab 5
    for data, slope in ((DROP_V, -10), (UP_V, -10), (DROP_V2, -10), (PAPER_V, -6)):
        c(lsq_slope(data), slope, 0.6)
    c(0.10 / 0.01, 10); c(2 * 1.25 / 0.25, 10)
    # campuran, TKA, uji
    c(t_hit(35, 30), 7); c(math.sqrt(25 + 200), 15); c(60 - 45, 15)
    c(math.sqrt(1025), 32.02, 0.01); c(t_hit(40, 15) - t_hit(40, -15), 3); c(64 / 3.2, 20); c(2 * 8 / 1.6, 10)
    c(math.sqrt(10.5 ** 2 - 100), 3.2, 0.01); c(math.sqrt(144 - 100), 6.63, 0.01); c(math.sqrt(1600), 40); c(math.sqrt(2 * 10 * 20), 20); c(math.sqrt(500), 22.36, 0.01)
    c(math.sqrt(40 / 10) + 20 / 340, 2.06, 0.005); c(5 * 2.06 ** 2, 21.2, 0.05)
    c(t_hit(20, 15), 4); c(t_hit(60, 20), 6); c(60 + 20, 80); c(80 - 5 * 9, 35)
    return True
