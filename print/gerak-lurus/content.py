"""Content of the printable module "Gerak Lurus" (Fisika kelas X).

Graphs come from print/graphs.py: each item picks a fixed template and adds a Motion,
data points or straight lines. Numeric answers are computed from the same models and
re-derived in check().
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import Motion, TEMPLATES as TP, render  # noqa: E402


def n(x, d=2):
    """Indonesian number format: 1.087,5 and −3."""
    x = round(x + 0.0, d)
    if abs(x - round(x)) < 1e-9:
        s = f"{int(round(x)):,}".replace(",", ".")
    else:
        s = f"{x:,.{d}f}".rstrip("0").rstrip(".")
        s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return s.replace("-", "−")


def fr(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'


def G(name, *motions, w=300, h=190, **kw):
    return render(TP[name], motions, width=w, height=h, **kw)


def Q(lv, q, a, e, fig=None, opts=None, kfig=None):
    """A practice item. fig: graph in the stem; opts: list of graph options (A–D); kfig: graph in the key."""
    return dict(lv=lv, q=q, a=a, e=e, fig=fig, opts=opts, kfig=kfig)


BLUE, RED = "#1f3a68", "#c0502a"

# ------------------------------------------------------------------ noisy tracking data (deterministic)
def noisy(f, ts, amp, seed):
    r = random.Random(seed)
    return [(t, round(f(t) + r.uniform(-amp, amp), 2)) for t in ts]


def lsq_slope(pts):
    k = len(pts)
    mt = sum(t for t, _ in pts) / k
    my = sum(y for _, y in pts) / k
    return sum((t - mt) * (y - my) for t, y in pts) / sum((t - mt) ** 2 for t, _ in pts)


TS = [k * 0.25 for k in range(17)]                                # 0 … 4 s every 0,25 s
DATA_GLB = noisy(lambda t: 0.5 * t, TS, 0.06, 11)                   # troli GLB 0,5 m/s
DATA_GLB_ITEM = noisy(lambda t: 0.25 + 0.375 * t, TS, 0.07, 23)     # latihan 5.5
DATA_V_BERTAHAP = noisy(lambda t: 0.4 + 0.3 * t, TS, 0.07, 5)       # contoh bertahap 5
DATA_V_ITEM = noisy(lambda t: 1.2 - 0.3 * t, TS, 0.07, 41)          # latihan 5.7
TS2 = [k * 0.5 for k in range(9)]
DATA_TABLE_NOISY = noisy(lambda t: 0.8 * t, TS2, 0.05, 7)           # latihan 5.10

PRASYARAT = [
    ("P1", "Tentukan kemiringan (gradien) garis yang melalui titik (2, 4) dan (6, 12).", "2", "(12 − 4) : (6 − 2) = 8 : 4 = 2."),
    ("P2", "Hitung luas trapesium dengan sisi sejajar 4 dan 10 serta tinggi 6.", "42", "½ · (4 + 10) · 6 = 42."),
    ("P3", "Hitung luas segitiga dengan alas 8 dan tinggi 5.", "20", "½ · 8 · 5 = 20."),
    ("P4", "Ubah 72 km/jam ke m/s dan 15 m/s ke km/jam.", "20 m/s dan 54 km/jam", "km/jam : 3,6 = m/s; m/s × 3,6 = km/jam."),
    ("P5", "Selesaikan 3t + 6 = 2t + 10.", "t = 4", "3t − 2t = 10 − 6."),
    ("P6", "Selesaikan 5t² = 80 untuk t positif.", "t = 4", "t² = 16, jadi t = 4."),
    ("P7", "Hitung 12 − (−3) dan (−5) − 4.", "15 dan −9", "Mengurangkan bilangan negatif sama dengan menambah."),
    ("P8", "Jika y = 2 + 3t, berapa y saat t = 4?", "14", "2 + 3 · 4 = 14."),
]

INGAT = [
    ("A", "Gradien dan luas bangun datar", "P1–P3", "Semua subbab",
     ["Gradien garis = Δy : Δx, yaitu perubahan tegak dibagi perubahan mendatar. Garis naik bergradien positif, garis turun negatif, garis mendatar nol.",
      "Luas segitiga = ½ · alas · tinggi. Luas persegi panjang = panjang · lebar. Luas trapesium = ½ · (jumlah sisi sejajar) · tinggi."]),
    ("B", "Konversi satuan", "P4", "Subbab 2–4",
     ["1 km/jam = 1.000 m : 3.600 s. Jadi km/jam : 3,6 = m/s dan m/s × 3,6 = km/jam.", "1 menit = 60 s; 1 cm = 0,01 m."]),
    ("C", "Persamaan linear dan kuadrat sederhana", "P5–P6, P8", "Subbab 2–4",
     ["Kumpulkan suku yang memuat t di satu ruas, lalu bagi dengan koefisiennya.", "at² = c → t = √(c/a). Untuk waktu, ambil akar yang positif."]),
    ("D", "Bilangan bertanda", "P7", "Subbab 1–3",
     ["Pada gerak lurus, tanda + dan − menyatakan arah. Selisih selalu dihitung akhir − awal."]),
]

SUB = []

# ================================================================== Subbab 1
M1 = Motion(0, 0, [(2, 5), (2, 0), (2, -5), (4, 0)])
P1 = Motion(0, 0, [(10, 1)])
TAN1 = (2, 0, 7, 20, True)                         # tangent to s = ½t² at t = 4: s = 4t − 8
RUN_S = [(0, 0), (5, 30), (7, 30), (10, 15)]       # piecewise-linear s–t (GLB segments)
P2 = Motion(0, 0, [(7, 2)])                         # s = t², used with tangent at t = 4
TAN2 = (2, 0, 6, 32, True)                          # s = 8t − 16


def piecewise_st(pts, name, w=300, h=190, color=BLUE):
    """s–t graph made of straight GLB pieces through the given corner points."""
    tp = TP[name]
    lines = [(t1, s1, t2, s2, False) for (t1, s1), (t2, s2) in zip(pts, pts[1:])]
    svg = render(tp, (), lines=lines, width=w, height=h)
    return svg.replace('stroke="#c0502a" stroke-width="1.6"', f'stroke="{color}" stroke-width="2.2"')


SUB.append(dict(
    title="Posisi, Perpindahan, dan Kecepatan",
    tujuan="Menyatakan posisi dengan koordinat s, lalu menentukan perpindahan, kecepatan rata-rata, kecepatan sesaat, dan percepatan dari data dan grafik.",
    konsep=[
        "Gerak lurus terjadi di sepanjang satu garis. Posisi benda dinyatakan dengan satu koordinat, <b>s</b>, yaitu jarak bertanda dari titik acuan. Pilih dulu titik acuan (s = 0) dan arah positif.",
        "Huruf s dipakai untuk koordinat umum. Dalam soal tertentu koordinat ini diberi nama sesuai arahnya: <b>x</b> untuk gerak mendatar dan <b>y</b> untuk gerak tegak (dibahas di modul berikutnya). Rumusnya sama; hanya namanya yang berganti.",
        "<b>Kecepatan rata-rata</b> adalah perpindahan dibagi selang waktu. <b>Kecepatan sesaat</b> adalah kecepatan pada satu saat tertentu. Pada grafik s–t, kecepatan sesaat sama dengan <b>kemiringan garis singgung</b> di titik itu; spidometer kendaraan menunjukkan besarnya.",
    ],
    rumus=[
        "Perpindahan: Δs = s<sub>akhir</sub> − s<sub>awal</sub> (tanda menyatakan arah)",
        "Kecepatan rata-rata: v̄ = " + fr("Δs", "Δt") + "; kelajuan rata-rata = " + fr("jarak", "Δt"),
        "Kecepatan sesaat = kemiringan garis singgung grafik s–t pada saat itu",
        "Percepatan rata-rata: ā = " + fr("Δv", "Δt"),
    ],
    contoh=[
        ("Membaca grafik s–t", "Grafik s–t sebuah sepeda ditunjukkan di bawah. Tentukan posisi pada t = 2 s, 4 s, dan 6 s, serta kecepatan rata-rata pada selang 0–6 s.",
         G("glb-st", M1, marks=[(2, M1.s(2), "P"), (4, M1.s(4), "Q"), (6, M1.s(6), "R")]),
         [f"Dari grafik: s(2) = {n(M1.s(2))} m, s(4) = {n(M1.s(4))} m, s(6) = {n(M1.s(6))} m.",
          f"v̄ = (s(6) − s(0)) : 6 = {n(M1.s(6))} : 6 ≈ {n(M1.s(6) / 6)} m/s."],
         f"{n(M1.s(2))} m, {n(M1.s(4))} m, {n(M1.s(6))} m; v̄ ≈ {n(M1.s(6) / 6)} m/s"),
        ("Kecepatan sesaat dari garis singgung", "Grafik s–t sebuah troli melengkung seperti di bawah. Garis putus-putus adalah garis singgung di t = 4 s. Tentukan kecepatan sesaat pada t = 4 s dan bandingkan dengan kecepatan rata-rata pada 0–4 s.",
         G("glb-st", P1, lines=[TAN1], marks=[(4, P1.s(4), "")]),
         ["Garis singgung melalui (2, 0) dan (7, 20).", f"Kecepatan sesaat = (20 − 0) : (7 − 2) = {n(20 / 5)} m/s.",
          f"Kecepatan rata-rata 0–4 s = s(4) : 4 = {n(P1.s(4))} : 4 = {n(P1.s(4) / 4)} m/s. Keduanya berbeda karena kecepatannya berubah."],
         f"{n(P1.v(4))} m/s (sesaat); {n(P1.s(4) / 4)} m/s (rata-rata)"),
    ],
    bertahap=dict(
        soal="Grafik s–t seorang pelari ditunjukkan di bawah. Tentukan perpindahan, jarak, kecepatan rata-rata, dan kelajuan rata-ratanya pada selang 0–10 s.",
        fig=piecewise_st(RUN_S, "glb-st"),
        langkah=["Perpindahan = s(10) − s(0) = ____ − 0 = ____ m.", "Jarak = 30 + 0 + ____ = ____ m.",
                 "Kecepatan rata-rata = ____ : 10 = ____ m/s.", "Kelajuan rata-rata = ____ : 10 = ____ m/s."],
        cek="Pada selang 7–10 s, pelari bergerak ke arah",
        opsi=["(a) negatif, karena grafik s–t menurun", "(b) positif, karena nilai s masih positif"],
        kunci="15; 15 m. 15; 45 m. 15 : 10 = 1,5 m/s. 45 : 10 = 4,5 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Nilai s yang positif tidak berarti benda bergerak ke arah positif. Arah gerak dilihat dari <b>perubahan</b> s, yaitu kemiringan grafik s–t.",
        "Kecepatan sesaat sama dengan kecepatan rata-rata hanya bila kecepatannya tetap (grafik s–t lurus).",
        "Kecepatan negatif berarti bergerak ke arah negatif, bukan sedang melambat.",
    ],
    latihan=[
        Q(1, "Posisi awal sebuah semut s = −3 m dan posisi akhirnya s = 5 m. Berapa perpindahannya?", "8 m ke arah positif", "Δs = 5 − (−3) = 8 m."),
        Q(1, "Sebuah mobil berpindah dari s = 20 m ke s = −10 m dalam 6 s. Berapa kecepatan rata-ratanya?", "−5 m/s (5 m/s ke arah negatif)", "v̄ = (−10 − 20) : 6 = −5 m/s."),
        Q(1, "Grafik s–t sebuah troli ditunjukkan di bawah. Berapa posisi troli pada t = 5 s?", f"{n(10 + 2 * 5)} m",
          "Baca grafik: pada t = 5 s, s = 20 m.", fig=G("glb-st", Motion(10, 2, [(10, 0)]))),
        Q(1, "Sebuah sepeda motor bergerak dari diam dan kecepatannya menjadi 12 m/s dalam 4 s. Berapa percepatan rata-ratanya?", "3 m/s²", "ā = (12 − 0) : 4 = 3 m/s²."),
        Q(1, "Spidometer mobil menunjukkan angka 60 km/jam. Apakah angka itu kelajuan sesaat atau kelajuan rata-rata?", "kelajuan sesaat", "Spidometer menunjukkan kelajuan pada saat itu."),
        Q(2, "Grafik s–t pada Contoh Bertahap 1 menunjukkan seorang pelari. Pada selang waktu mana pelari bergerak ke arah negatif, dan berapa kecepatannya?", "7–10 s; −5 m/s",
          "Grafik menurun dari (7, 30) ke (10, 15): (15 − 30) : 3 = −5 m/s."),
        Q(2, "Grafik s–t sebuah troli melengkung seperti di bawah. Garis putus-putus adalah garis singgung di t = 4 s. Berapa kecepatan sesaat troli pada t = 4 s?", f"{n(P2.v(4))} m/s",
          "Garis singgung melalui (2, 0) dan (6, 32): (32 − 0) : (6 − 2) = 8 m/s.", fig=G("glb-st", P2, lines=[TAN2], marks=[(4, P2.s(4), "")])),
        Q(2, "Untuk troli pada soal sebelumnya, hitung kecepatan rata-rata pada selang 2–6 s. Bandingkan dengan kecepatan sesaat pada t = 4 s.", f"{n((P2.s(6) - P2.s(2)) / 4)} m/s; sama",
          f"s(2) = {n(P2.s(2))} m dan s(6) = {n(P2.s(6))} m; ({n(P2.s(6))} − {n(P2.s(2))}) : 4 = {n((P2.s(6) - P2.s(2)) / 4)} m/s. Pada percepatan tetap, kecepatan rata-rata sama dengan kecepatan sesaat di tengah selang."),
        Q(2, "Kecepatan sebuah mobil berubah dari 20 m/s menjadi 5 m/s dalam 5 s, arahnya tetap. Berapa percepatan rata-ratanya?", "−3 m/s² (diperlambat)", "ā = (5 − 20) : 5 = −3 m/s²."),
        Q(2, "Dengan memakai grafik pada Contoh Bertahap 1, tentukan kecepatan pelari pada t = 2 s dan pada t = 6 s.", "6 m/s dan 0", "0–5 s: (30 − 0) : 5 = 6 m/s. 5–7 s: grafik mendatar, v = 0."),
        Q(3, "Seseorang berjalan 40 m ke arah positif dalam 20 s, lalu 40 m ke arah negatif dalam 30 s. Hitung kelajuan rata-rata dan kecepatan rata-ratanya.", "1,6 m/s; 0",
          "Jarak 80 m dalam 50 s → 1,6 m/s. Kembali ke titik awal → perpindahan 0, kecepatan rata-rata 0."),
        Q(3, "Sebuah sepeda menempuh 6 km dengan kelajuan 12 km/jam, lalu kembali 6 km dengan kelajuan 6 km/jam. Berapa kelajuan rata-ratanya? Apakah sama dengan (12 + 6) : 2?", "8 km/jam; tidak sama dengan 9 km/jam",
          "Waktu pergi 0,5 jam dan pulang 1 jam. 12 km : 1,5 jam = 8 km/jam."),
        Q(3, "Mengapa pada grafik s–t yang berupa garis lurus, kecepatan sesaat di setiap titik sama dengan kecepatan rata-rata pada selang mana pun?", "Garis lurus mempunyai kemiringan yang sama di semua titik",
          "Garis singgung pada garis lurus adalah garis itu sendiri, jadi kemiringannya sama dengan kemiringan antara dua titik mana pun."),
        Q(3, "Sebuah benda bergerak dengan kecepatan −4 m/s dan percepatan −2 m/s². Apakah benda itu sedang dipercepat atau diperlambat? Jelaskan.", "dipercepat (ke arah negatif)",
          "v dan a searah (keduanya negatif), jadi kelajuannya bertambah."),
    ],
))

# ================================================================== Subbab 2: GLB
C21 = Motion(-10, 4, [(8, 0)])
A6, B6 = Motion(0, 4, [(10, 0)], "A", BLUE), Motion(30, 1, [(10, 0)], "B", RED)
assert A6.s(10) == B6.s(10) == 40
SK8 = Motion(10, -5, [(6, 0)])
STEP13 = Motion(0, 4, [(3, 0)])
SUB.append(dict(
    title="Gerak Lurus Beraturan (GLB)",
    tujuan="Mengenali GLB dari grafik, cerita, dan persamaan, lalu menentukan posisi serta saat dan tempat dua benda bertemu.",
    konsep=[
        "<b>GLB</b> adalah gerak lurus dengan <b>kecepatan tetap</b>: besar dan arahnya tidak berubah, sehingga percepatannya nol. Dalam selang waktu yang sama, benda menempuh perpindahan yang sama.",
        "<b>Grafik.</b> Grafik s–t berupa garis lurus miring; kemiringannya adalah kecepatan. Grafik v–t berupa garis mendatar; luas di bawahnya adalah perpindahan. Grafik a–t berimpit dengan sumbu t.",
        "<b>Dua benda.</b> Dua benda bertemu ketika posisinya sama: s<sub>A</sub> = s<sub>B</sub>. Pada grafik s–t, titik potong kedua garis adalah tempat dan saat bertemu.",
    ],
    rumus=["s = s₀ + v·t", "v = " + fr("Δs", "Δt") + " (kemiringan grafik s–t)", "Δs = v·t (luas di bawah grafik v–t)", "Bertemu: s<sub>A</sub>(t) = s<sub>B</sub>(t)"],
    contoh=[
        ("Dua grafik untuk satu gerak", "Sebuah robot mulai di s = −10 m dan bergerak 4 m/s ke arah positif selama 8 s. Gambarkan grafik v–t dan s–t-nya, lalu tentukan posisinya pada t = 8 s.",
         '<div class="two">' + G("glb-vt", C21, w=260, h=170, shade=(0, 0, 8)) + G("glb-st2", C21, w=260, h=170) + "</div>",
         ["Grafik v–t: garis mendatar pada v = 4 m/s. Luas = 4 × 8 = 32 m = perpindahan.", f"s(8) = −10 + 4 · 8 = {n(C21.s(8))} m. Grafik s–t: garis lurus dari (0, −10) ke (8, 22)."],
         f"s(8) = {n(C21.s(8))} m"),
        ("Berpapasan", "Mobil A berada di s = 0 dan melaju 15 m/s ke arah positif. Pada saat yang sama, mobil B berada di s = 300 m dan melaju 10 m/s ke arah negatif. Kapan dan di mana keduanya berpapasan?",
         None, ["s<sub>A</sub> = 15t; s<sub>B</sub> = 300 − 10t.", "15t = 300 − 10t → 25t = 300 → t = 12 s.", "s = 15 · 12 = 180 m."], "t = 12 s, di s = 180 m"),
    ],
    bertahap=dict(
        soal="Motor A di s = 0 melaju 20 m/s. Motor B berada 100 m di depannya dan melaju 10 m/s searah. Kapan dan di mana A menyusul B?",
        fig=None,
        langkah=["s<sub>A</sub> = 20t dan s<sub>B</sub> = ____ + 10t.", "20t = ____ + 10t → t = ____ s.", "s = 20 · ____ = ____ m."],
        cek="A menyusul B ketika",
        opsi=["(a) posisi keduanya sama", "(b) kecepatan keduanya sama"],
        kunci="100; t = 10 s; s = 200 m. Alasan: (a).",
    ),
    jebakan=[
        "Grafik s–t yang miring belum tentu GLBB. Bila garisnya lurus, kecepatannya tetap (GLB).",
        "Titik potong dua garis pada grafik <b>s–t</b> berarti bertemu. Titik potong pada grafik <b>v–t</b> hanya berarti kecepatannya sama.",
        "Luas di bawah sumbu t pada grafik v–t bernilai negatif: perpindahannya ke arah negatif.",
    ],
    latihan=[
        Q(1, "Mobil melaju tetap 20 m/s selama 15 s. Berapa perpindahannya?", "300 m", "Δs = 20 · 15 = 300 m."),
        Q(1, "Bus melaju tetap 72 km/jam selama 5 menit. Berapa jarak yang ditempuhnya?", "6 km", "72 km/jam = 20 m/s; 5 menit = 300 s; 20 · 300 = 6.000 m."),
        Q(1, "Grafik s–t sebuah troli ditunjukkan di bawah. Berapa kecepatannya?", "3 m/s", "Melalui (0, 5) dan (10, 35): 30 : 10 = 3 m/s.", fig=G("glb-st", Motion(5, 3, [(10, 0)]))),
        Q(1, "Grafik v–t sebuah benda ditunjukkan di bawah. Berapa perpindahannya selama 8 s?", "−32 m", "Luas = (−4) · 8 = −32 m, ke arah negatif.", fig=G("glb-vt", Motion(0, -4, [(8, 0)]))),
        Q(1, "Posisi sebuah benda dinyatakan s = 12 − 3t (s dalam meter, t dalam sekon). Tentukan posisi awal, kecepatan, dan posisinya pada t = 6 s.", "12 m; −3 m/s; −6 m", "Bentuk s = s₀ + vt: s₀ = 12, v = −3; s(6) = 12 − 18 = −6 m."),
        Q(2, "Grafik s–t benda A dan B ditunjukkan di bawah. Kapan dan di mana keduanya bertemu?", "t = 10 s, di s = 40 m",
          "s<sub>A</sub> = 4t, s<sub>B</sub> = 30 + t. 4t = 30 + t → t = 10 s; s = 40 m (titik potong).", fig=G("glb-st", A6, B6)),
        Q(2, "Kereta sepanjang 150 m melaju tetap 54 km/jam melintasi jembatan sepanjang 300 m. Berapa lama sejak lokomotif masuk jembatan sampai gerbong terakhir keluar?", "30 s",
          "54 km/jam = 15 m/s. Jarak yang ditempuh = 300 + 150 = 450 m; 450 : 15 = 30 s."),
        Q(2, "Pada bingkai di bawah, gambarlah grafik s–t benda yang mula-mula di s = 10 m dan bergerak 5 m/s ke arah negatif selama 6 s.", "garis lurus dari (0, 10) ke (6, −20)",
          "s(6) = 10 − 5 · 6 = −20 m.", fig=G("glb-st2"), kfig=G("glb-st2", SK8, w=240, h=150)),
        Q(2, "Seorang anak berjalan 2,5 m/s ke arah positif selama 4 s, berhenti 2 s, lalu berjalan 5 m/s ke arah negatif selama 3 s. Gambarlah grafik s–t-nya pada bingkai di bawah.", "titik sudut (0, 0), (4, 10), (6, 10), (9, −5)",
          "s(4) = 10 m; tetap sampai t = 6 s; s(9) = 10 − 15 = −5 m.", fig=G("glb-st2"), kfig=piecewise_st([(0, 0), (4, 10), (6, 10), (9, -5)], "glb-st2", 240, 150)),
        Q(2, "Mobil A melaju 25 m/s dan berada 50 m di belakang mobil B yang melaju 15 m/s searah. Berapa lama A menyusul B dan berapa jauh A bergerak sampai saat itu?", "5 s; 125 m",
          "25t = 50 + 15t → t = 5 s; 25 · 5 = 125 m."),
        Q(3, "Dua pesepeda terpisah 3 km dan saling mendekat dengan kelajuan 18 km/jam dan 12 km/jam. Setelah berapa menit mereka bertemu, dan berapa jauh dari posisi awal pesepeda pertama?", "6 menit; 1,8 km",
          "Mereka saling mendekat 30 km/jam: 3 km : 30 km/jam = 0,1 jam = 6 menit; 18 · 0,1 = 1,8 km."),
        Q(3, "Bus A berangkat dari kota P pukul 07.00 dengan 60 km/jam. Bus B berangkat dari P pukul 07.30 searah dengan 80 km/jam. Pukul berapa dan berapa jauh dari P bus B menyusul bus A?", "pukul 09.00; 120 km",
          "Dengan t sejak 07.00: 60t = 80(t − 0,5) → t = 2 jam; 60 · 2 = 120 km."),
        Q(3, "Grafik v–t sebuah benda ditunjukkan di bawah. Hitung perpindahan dan jaraknya selama 9 s.", "perpindahan 0; jarak 24 m",
          "0–3 s: 4 · 3 = 12 m. 3–5 s: diam. 5–9 s: (−3) · 4 = −12 m. Perpindahan 0; jarak 12 + 12 = 24 m.",
          fig=render(TP["glb-vt"], (), lines=[(0, 4, 3, 4, False), (3, 0, 5, 0, False), (5, -3, 9, -3, False)]).replace('stroke="#c0502a" stroke-width="1.6"', f'stroke="{BLUE}" stroke-width="2.2"')),
        Q(3, "Kilat terlihat dan gunturnya terdengar 6 s kemudian. Jika bunyi merambat tetap 340 m/s dan cahaya dianggap tiba seketika, berapa jauh sambaran petir itu?", "2.040 m", "Bunyi ber-GLB: 340 · 6 = 2.040 m."),
    ],
))

# ================================================================== Subbab 3: GLBB
C31 = Motion(0, 4, [(6, 2)])
V3 = Motion(0, 2, [(6, 2)])
S3 = Motion(0, 10, [(5, -2), (2, 0)])
REV = Motion(0, 6, [(6, -2), (2, 0)])
D13 = Motion(0, -4, [(6, 2)])
CAR, BIKE = Motion(0, 0, [(10, 2)], "A", BLUE), Motion(0, 10, [(10, 0)], "B", RED)
assert CAR.s(10) == BIKE.s(10) == 100
SUB.append(dict(
    title="Gerak Lurus Berubah Beraturan (GLBB)",
    tujuan="Mengenali GLBB dari grafik, cerita, dan persamaan; menentukan kecepatan sesaat dengan v(t) dan garis singgung; memakai v² = v₀² + 2as.",
    konsep=[
        "<b>GLBB</b> adalah gerak lurus dengan <b>percepatan tetap</b>. Kecepatannya bertambah atau berkurang dengan jumlah yang sama setiap sekon.",
        "<b>Grafik.</b> Grafik v–t berupa garis lurus miring: kemiringannya percepatan, luas di bawahnya perpindahan. Grafik s–t berupa parabola. Grafik a–t berupa garis mendatar.",
        "<b>Dipercepat atau diperlambat?</b> Bila v dan a searah (tandanya sama), kelajuan bertambah. Bila berlawanan, kelajuan berkurang. Bila garis v–t memotong sumbu t, benda berhenti sesaat lalu berbalik arah.",
        "<b>Kecepatan sesaat</b> pada GLBB dihitung dengan v(t) = v₀ + at, atau dibaca sebagai kemiringan garis singgung grafik s–t.",
    ],
    rumus=["v = v₀ + a·t", "s = s₀ + v₀·t + ½·a·t²", "v² = v₀² + 2a·(s − s₀), dipakai bila waktu tidak diketahui", "Δs = ½·(v₀ + v)·t (luas trapesium di bawah grafik v–t)"],
    contoh=[
        ("Kemiringan dan luas grafik v–t", "Grafik v–t sebuah mobil ditunjukkan di bawah. Tentukan percepatan dan perpindahannya selama 6 s.",
         G("glbb-vt", C31, shade=(0, 0, 6)),
         ["a = (16 − 4) : 6 = 2 m/s².", f"Δs = luas trapesium = ½ · (4 + 16) · 6 = {n(C31.s(6))} m."], f"a = 2 m/s²; Δs = {n(C31.s(6))} m"),
        ("Pengereman", "Mobil melaju 20 m/s lalu direm dengan percepatan −4 m/s² sampai berhenti. Tentukan waktu dan jarak pengeremannya.",
         None, ["0 = 20 + (−4)t → t = 5 s.", "0² = 20² + 2(−4)Δs → Δs = 400 : 8 = 50 m."], "5 s; 50 m"),
    ],
    bertahap=dict(
        soal="Sepeda motor bergerak dari diam dengan percepatan tetap 3 m/s². Tentukan kecepatan dan posisinya pada t = 4 s, lalu kecepatannya saat sudah menempuh 54 m.",
        fig=None,
        langkah=["v(4) = 0 + 3 · 4 = ____ m/s.", "s(4) = ½ · 3 · 4² = ____ m.", "v² = 0 + 2 · 3 · 54 = ____, jadi v = ____ m/s."],
        cek="Pada langkah ketiga dipakai v² = v₀² + 2as karena",
        opsi=["(a) waktunya tidak diketahui", "(b) percepatannya tidak diketahui"],
        kunci="12 m/s; 24 m; 324, v = 18 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Percepatan negatif tidak selalu berarti melambat. Benda melambat bila v dan a berlawanan tanda.",
        "Grafik s–t pada GLBB melengkung (parabola). Jangan menghitung kecepatan GLBB dengan s : t; itu kecepatan rata-rata.",
        "v² = v₀² + 2as hanya memberi besar kecepatan. Tanda (arah) ditentukan dari situasinya.",
    ],
    latihan=[
        Q(1, "Benda bergerak dari diam dengan percepatan 2 m/s². Berapa kecepatannya setelah 5 s?", "10 m/s", "v = 0 + 2 · 5."),
        Q(1, "Grafik v–t sebuah troli ditunjukkan di bawah. Berapa percepatannya?", "2 m/s²", "(14 − 2) : 6 = 2 m/s².", fig=G("glbb-vt", V3)),
        Q(1, "Untuk troli pada soal sebelumnya, berapa perpindahannya selama 6 s?", f"{n(V3.s(6))} m", "Luas trapesium ½ · (2 + 14) · 6 = 48 m."),
        Q(1, "Kecepatan sebuah benda dinyatakan v = 10 + 3t (SI). Tentukan v₀, a, dan v pada t = 4 s.", "10 m/s; 3 m/s²; 22 m/s", "Bentuk v = v₀ + at."),
        Q(1, "Mobil yang melaju 15 m/s direm sampai berhenti dalam 3 s. Berapa percepatannya?", "−5 m/s²", "(0 − 15) : 3."),
        Q(2, "Posisi benda dinyatakan s = 2 + 4t + t² (SI). Tentukan kecepatan sesaatnya pada t = 3 s.", "10 m/s",
          "Bandingkan dengan s = s₀ + v₀t + ½at²: v₀ = 4 m/s dan ½a = 1, jadi a = 2 m/s². v(3) = 4 + 2 · 3 = 10 m/s."),
        Q(2, "Pesawat bergerak dari diam dan harus mencapai 60 m/s untuk lepas landas. Jika percepatannya 3 m/s², berapa panjang landasan minimal?", "600 m", "60² = 0 + 2 · 3 · Δs → Δs = 3.600 : 6 = 600 m."),
        Q(2, "Grafik s–t sebuah troli yang didorong lalu dilepas ditunjukkan di bawah. Garis putus-putus adalah garis singgung di t = 2 s. Tentukan kecepatan sesaat pada t = 2 s dan pada t = 5 s.", "6 m/s dan 0",
          "Garis singgung melalui (0, 4) dan (6, 40): 36 : 6 = 6 m/s. Pada t = 5 s grafik mencapai puncak (garis singgung mendatar), v = 0.",
          fig=G("glb-st", S3, lines=[(0, 4, 6, 40, True)], marks=[(2, S3.s(2), ""), (5, S3.s(5), "puncak")])),
        Q(2, "Keping hoki meluncur 10 m/s di lantai es dan mengalami percepatan −2 m/s². Berapa jarak yang ditempuhnya sampai kecepatannya 6 m/s?", "16 m", "6² = 10² + 2(−2)Δs → Δs = 64 : 4 = 16 m."),
        Q(2, "Grafik v–t sebuah troli ditunjukkan di bawah. Kapan troli berbalik arah? Gambarlah grafik a–t-nya pada bingkai kanan.", "t = 3 s; a = −2 m/s² pada 0–6 s, 0 pada 6–8 s",
          "v = 0 pada t = 3 s. Kemiringan 0–6 s: (−6 − 6) : 6 = −2 m/s²; 6–8 s mendatar.",
          fig='<div class="two">' + G("glbb-vt2", REV, w=260, h=170) + G("glbb-at", w=260, h=170) + "</div>", kfig=G("glbb-at", REV, w=240, h=150)),
        Q(3, "Grafik v–t mobil A (dari diam) dan motor B ditunjukkan di bawah; keduanya mulai dari tempat yang sama pada t = 0. Kapan A menyusul B, dan apa arti titik potong kedua garis?", f"t = 10 s, setelah menempuh {n(CAR.s(10))} m; titik potong (t = 5 s) berarti kecepatan sama",
          "Luas di bawah garis A sama dengan luas di bawah garis B saat ½ · 2 · t² = 10t → t = 10 s; s = 100 m. Pada t = 5 s, B masih di depan (50 m lawan 25 m).",
          fig=render(TP["glbb-vt"], (CAR, BIKE))),
        Q(3, "Kereta melambat dari 30 m/s menjadi 10 m/s dalam jarak 400 m. Tentukan percepatan dan waktu pengeremannya.", "−1 m/s²; 20 s", "10² = 30² + 2a · 400 → a = −800 : 800 = −1 m/s². t = (10 − 30) : (−1) = 20 s."),
        Q(3, "Grafik v–t sebuah benda ditunjukkan di bawah. Hitung perpindahan dan jaraknya selama 6 s.", f"perpindahan {n(D13.s(6))} m; jarak {n(D13.distance(0, 6))} m",
          "0–2 s: luas segitiga di bawah sumbu = −4 m. 2–6 s: luas di atas sumbu = ½ · 4 · 8 = 16 m. Perpindahan 12 m; jarak 4 + 16 = 20 m.", fig=G("glbb-vt2", D13)),
        Q(3, "Benda bergerak dari diam dengan percepatan 4 m/s². Berapa jarak yang ditempuhnya pada detik ke-3 saja (antara t = 2 s dan t = 3 s)?", "10 m", "s(3) − s(2) = ½ · 4 · (9 − 4) = 10 m."),
    ],
))

# ================================================================== Subbab 4: gabungan dan kasus nyata
ANGKOT = Motion(0, 10, [(4, 0), (4, -2.5), (4, 0), (4, 2.5), (4, 0)])
TRAP = Motion(0, 0, [(2, 5), (4, 0), (2, -5)])
BUS = Motion(0, 0, [(6, 2.5), (8, 0), (6, -2.5)])
TROLI = Motion(0, 0, [(3, 2), (2, 0), (5, -2)])
SUB.append(dict(
    title="Gerak Gabungan dan Kasus Nyata",
    tujuan="Memecah gerak nyata menjadi bagian GLB dan GLBB, lalu menyelesaikan kasus jarak henti, lampu lalu lintas, dan kejar-mengejar.",
    konsep=[
        "Gerak kendaraan sehari-hari jarang hanya GLB atau hanya GLBB. Biasanya gerak itu tersusun dari beberapa bagian: dipercepat, melaju tetap, lalu diperlambat. Setiap bagian dikerjakan dengan rumus GLB atau GLBB.",
        "<b>Kecepatan dan posisi akhir</b> suatu bagian menjadi kecepatan dan posisi <b>awal</b> bagian berikutnya.",
        "<b>Jarak henti</b> kendaraan = jarak reaksi (selama pengemudi bereaksi, kendaraan masih GLB) + jarak pengereman (GLBB).",
    ],
    rumus=["Jarak reaksi = v · t<sub>reaksi</sub>", "Jarak pengereman = " + fr("v²", "2|a|"), "Jarak henti = v · t<sub>reaksi</sub> + " + fr("v²", "2|a|"),
           "Perpindahan total = jumlah luas di bawah grafik v–t setiap bagian"],
    contoh=[
        ("Angkot", "Sebuah angkot melaju tetap 10 m/s selama 4 s, mengerem rata sampai berhenti dalam 4 s, menunggu penumpang 4 s, lalu melaju lagi dan mencapai 10 m/s dalam 4 s, kemudian melaju tetap 4 s. Gambarkan grafik v–t dan hitung perpindahannya selama 20 s.",
         G("gab-vt", ANGKOT, shade=(0, 0, 20)),
         ["Bagian 1 (GLB): 10 · 4 = 40 m. Bagian 2 (GLBB): ½ · 10 · 4 = 20 m. Bagian 3: diam.",
          "Bagian 4 (GLBB): ½ · 10 · 4 = 20 m. Bagian 5 (GLB): 10 · 4 = 40 m.", f"Total = {n(ANGKOT.s(20))} m."], f"{n(ANGKOT.s(20))} m"),
        ("Jarak henti", "Mobil melaju 20 m/s. Waktu reaksi pengemudi 0,8 s dan rem memberi percepatan −5 m/s². Berapa jarak hentinya?",
         None, ["Jarak reaksi = 20 · 0,8 = 16 m.", "Jarak pengereman = 20² : (2 · 5) = 40 m.", "Jarak henti = 16 + 40 = 56 m."], "56 m"),
    ],
    bertahap=dict(
        soal="KRL berangkat dari stasiun dengan percepatan 1 m/s² selama 20 s, lalu melaju tetap selama 120 s, kemudian direm dengan percepatan −2 m/s² sampai berhenti di stasiun berikutnya. Berapa jarak antarstasiun?",
        fig=None,
        langkah=["Kecepatan setelah 20 s: v = 1 · 20 = ____ m/s.", "Bagian 1: ½ · 1 · 20² = ____ m.", "Bagian 2: ____ · 120 = ____ m.", "Bagian 3: ____² : (2 · 2) = ____ m. Total = ____ m."],
        cek="Kecepatan awal bagian 2 adalah",
        opsi=["(a) kecepatan akhir bagian 1", "(b) nol, karena setiap bagian dimulai dari diam"],
        kunci="20 m/s; 200 m; 20 · 120 = 2.400 m; 20² : 4 = 100 m; total 2.700 m. Alasan: (a).",
    ),
    jebakan=[
        "Jangan lupa jarak reaksi. Selama pengemudi bereaksi, kendaraan belum mulai mengerem.",
        "Setiap bagian gerak memakai v₀ dari akhir bagian sebelumnya, bukan nol.",
        "Saat kejar-mengejar, samakan posisi (s<sub>A</sub> = s<sub>B</sub>), bukan kecepatan.",
    ],
    latihan=[
        Q(1, "Mobil melaju 20 m/s dan waktu reaksi pengemudinya 0,5 s. Berapa jarak reaksinya?", "10 m", "20 · 0,5 = 10 m."),
        Q(1, "Grafik v–t sebuah sepeda motor ditunjukkan di bawah. Sebutkan jenis gerak pada setiap bagian.", "0–2 s GLBB dipercepat; 2–6 s GLB; 6–8 s GLBB diperlambat",
          "Garis naik, mendatar, lalu turun.", fig=G("glbb-vt", Motion(0, 0, [(2, 5), (4, 0), (2, -5)]))),
        Q(1, "Untuk sepeda motor pada soal sebelumnya, berapa perpindahannya selama 8 s?", f"{n(TRAP.s(8))} m", "Luas trapesium: 10 + 40 + 10 = 60 m."),
        Q(1, "Motor melaju 10 m/s lalu dipercepat 2 m/s² selama 3 s. Berapa kecepatannya sekarang?", "16 m/s", "10 + 2 · 3 = 16 m/s."),
        Q(1, "Mobil yang melaju 10 m/s direm dengan percepatan −2 m/s² sampai berhenti. Berapa jarak pengeremannya?", "25 m", "10² : (2 · 2) = 25 m."),
        Q(2, "Mobil melaju 25 m/s, waktu reaksi pengemudi 1 s, dan perlambatan rem 5 m/s². Berapa jarak hentinya?", "87,5 m", "25 · 1 + 25² : 10 = 25 + 62,5 = 87,5 m."),
        Q(2, "Pengemudi pada soal sebelumnya mengantuk sehingga waktu reaksinya menjadi 2 s. Berapa bertambahnya jarak henti?", "25 m (menjadi 112,5 m)", "Hanya jarak reaksi yang berubah: 25 · 2 = 50 m."),
        Q(2, "Mobil melaju 15 m/s ketika lampu menjadi kuning, 30 m sebelum garis berhenti. Waktu reaksi 0,6 s dan perlambatan rem 5 m/s². Dapatkah mobil berhenti sebelum garis?", "tidak; jarak hentinya 31,5 m, melewati garis 1,5 m",
          "Jarak reaksi 9 m; jarak pengereman 225 : 10 = 22,5 m; total 31,5 m > 30 m."),
        Q(2, "Bus dipercepat dari diam sampai 15 m/s dalam 6 s, melaju tetap 8 s, lalu direm sampai berhenti dalam 6 s. Gambarlah grafik v–t-nya pada bingkai di bawah dan hitung jarak antarhalte.", f"{n(BUS.s(20))} m",
          "Luas: ½ · 15 · 6 + 15 · 8 + ½ · 15 · 6 = 45 + 120 + 45 = 210 m.", fig=G("gab-vt"), kfig=G("gab-vt", BUS, w=240, h=150)),
        Q(2, "Grafik v–t sebuah troli ditunjukkan di bawah. Ceritakan geraknya dan tentukan kapan troli berbalik arah.", "dipercepat 3 s, melaju tetap 2 s, lalu diperlambat dan berbalik pada t = 8 s",
          "0–3 s: a = 2 m/s² sampai 6 m/s. 3–5 s: GLB 6 m/s. 5–10 s: a = −2 m/s²; v = 0 saat 6 − 2(t − 5) = 0 → t = 8 s, lalu bergerak ke arah negatif.",
          fig=G("glbb-vt2", TROLI)),
        Q(3, "Pengendara yang ngebut melaju tetap 20 m/s melewati polisi yang sedang diam. Saat itu juga polisi mengejar dengan percepatan 2,5 m/s². Kapan dan di mana polisi menyusul, dan berapa kecepatan polisi saat itu?", "16 s; 320 m; 40 m/s",
          "½ · 2,5 · t² = 20t → t = 16 s; s = 20 · 16 = 320 m; v = 2,5 · 16 = 40 m/s."),
        Q(3, "KRL dipercepat 0,8 m/s² sampai 16 m/s, melaju tetap 100 s, lalu direm 1,6 m/s² sampai berhenti. Hitung jarak dan waktu total, serta kelajuan rata-ratanya.", "1.840 m; 130 s; ≈ 14,15 m/s",
          "Bagian 1: 20 s, 160 m. Bagian 2: 1.600 m. Bagian 3: 10 s, 80 m. 1.840 : 130 ≈ 14,15 m/s."),
        Q(3, "Grafik v–t sebuah sepeda motor ditunjukkan di sebelah kiri. Grafik s–t yang sesuai adalah ....", "B",
          "Bagian GLBB dipercepat melengkung ke atas, bagian GLB lurus, bagian diperlambat melengkung mendatar; posisi tidak pernah turun karena v ≥ 0. A: menyalin bentuk v–t. C: posisi turun di akhir. D: semua bagian lurus.",
          fig=G("glbb-vt", TRAP, w=260, h=170), opts="TRAP"),
        Q(3, "Mobil A dan B berjarak 200 m dan saling mendekat. A melaju tetap 10 m/s; B mulai dari diam dengan percepatan 2 m/s². Kapan keduanya berpapasan, dan berapa jauh A sudah bergerak?", "10 s; 100 m",
          "10t + ½ · 2 · t² = 200 → t² + 10t − 200 = 0 → (t + 20)(t − 10) = 0 → t = 10 s; A menempuh 100 m."),
    ],
))

# ================================================================== Subbab 5: data pelacakan gerak
SUB.append(dict(
    title="Data Pelacakan Gerak dengan Ponsel",
    tujuan="Membaca data pelacakan gerak yang mengandung derau, menarik garis terbaik, lalu menentukan jenis gerak, kecepatan, dan percepatannya.",
    konsep=[
        "Aplikasi pelacak gerak di ponsel merekam posisi, kecepatan, atau percepatan berkali-kali setiap sekon. Data itu tidak pernah benar-benar mulus: selalu ada <b>derau</b> (noise) dari sensor, getaran tangan, dan ketidaktelitian pengukuran.",
        "Karena itu, <b>jangan menghitung kecepatan dari dua titik data yang berdekatan</b>: deraunya ikut terbagi dengan selang waktu yang kecil sehingga hasilnya melonjak. Tarik <b>garis terbaik</b>, yaitu satu garis yang paling dekat dengan semua titik, lalu hitung kemiringannya dari dua titik yang berjauhan <b>pada garis itu</b>.",
        "<b>Mengenali jenis gerak dari data.</b> GLB: titik s–t membentuk garis lurus, dan perpindahan pada selang waktu yang sama selalu sama. GLBB: titik v–t membentuk garis lurus, titik s–t membentuk parabola, dan perpindahan pada selang waktu yang sama bertambah dengan jumlah tetap.",
    ],
    rumus=["v ≈ kemiringan garis terbaik grafik s–t", "a ≈ kemiringan garis terbaik grafik v–t",
           "GLBB dengan selang waktu sama Δt: selisih dua perpindahan berurutan = a·(Δt)²"],
    contoh=[
        ("Troli GLB", "Ponsel merekam posisi troli setiap 0,25 s (titik). Garis merah adalah garis terbaik. Tentukan kecepatan troli.",
         render(TP["data-st"], points=DATA_GLB, lines=[(0, 0, 4, 2, False)]),
         ["Garis terbaik melalui (0, 0) dan (4, 2).", "v = (2 − 0) : (4 − 0) = 0,5 m/s.",
          f"Pembanding: dua titik berdekatan t = 1,00 dan 1,25 s memberi ({n(DATA_GLB[5][1])} − {n(DATA_GLB[4][1])}) : 0,25 = {n((DATA_GLB[5][1] - DATA_GLB[4][1]) / 0.25)} m/s, jauh meleset."],
         "0,5 m/s"),
        ("Selisih perpindahan GLBB", "Posisi troli yang dilepas di bidang miring direkam setiap 0,5 s: s = 0; 0,10; 0,40; 0,90; 1,60; 2,50 m. Apakah geraknya GLBB, dan berapa percepatannya?",
         None, ["Perpindahan tiap 0,5 s: 0,10; 0,30; 0,50; 0,70; 0,90 m.", "Selisih berurutan selalu 0,20 m, jadi GLBB.", "a = 0,20 : (0,5)² = 0,8 m/s²."], "GLBB, a = 0,8 m/s²"),
    ],
    bertahap=dict(
        soal="Ponsel merekam kecepatan sebuah troli setiap 0,25 s (titik). Garis merah adalah garis terbaik. Tentukan kecepatan awal dan percepatan troli.",
        fig=render(TP["data-vt"], points=DATA_V_BERTAHAP, lines=[(0, 0.4, 4, 1.6, False)]),
        langkah=["Garis terbaik memotong sumbu v di v₀ = ____ m/s.", "Garis melalui (4 ; ____).", "a = (____ − ____) : 4 = ____ m/s²."],
        cek="Kemiringan dihitung dari dua titik pada garis terbaik yang berjauhan karena",
        opsi=["(a) derau data terbagi dengan selang waktu yang besar sehingga pengaruhnya kecil", "(b) titik data yang berjauhan selalu bebas derau"],
        kunci="0,4 m/s; 1,6 m/s; (1,6 − 0,4) : 4 = 0,3 m/s². Alasan: (a).",
    ),
    jebakan=[
        "Garis terbaik tidak harus melalui titik data pertama atau titik mana pun.",
        "Perhatikan satuan pada aplikasi: data sering tertulis dalam cm atau ms.",
        "Pada sebagian aplikasi, sumbu tegak akselerometer menunjukkan sekitar 9,8 m/s² walau ponsel diam, karena sensor ikut merasakan gravitasi. Pilih data percepatan linear bila tersedia.",
    ],
    latihan=[
        Q(1, "Posisi sebuah troli tercatat setiap 1 s: s = 0; 1,1; 1,9; 3,0; 4,0 m. Jenis gerak apa yang paling sesuai, dan berapa kira-kira kecepatannya?", "GLB, sekitar 1 m/s", "Perpindahan tiap sekon hampir sama (≈ 1 m); dari titik pertama dan terakhir: 4,0 : 4 = 1 m/s."),
        Q(1, "Mengapa kecepatan tidak boleh dihitung dari dua titik data yang berdekatan?", "deraunya menjadi sangat berpengaruh", "Kesalahan kecil pada s dibagi selang waktu yang kecil menghasilkan kesalahan besar pada v."),
        Q(1, "Perpindahan troli tercatat 0,5 m setiap 0,5 s secara tetap. Berapa kecepatannya?", "1 m/s", "0,5 : 0,5 = 1 m/s."),
        Q(1, "Aplikasi mencatat troli berpindah 25 cm setiap 0,5 s. Berapa kecepatannya dalam m/s?", "0,5 m/s", "25 cm = 0,25 m; 0,25 : 0,5 = 0,5 m/s."),
        Q(2, "Ponsel merekam posisi sebuah troli (titik). Garis merah adalah garis terbaik. Berapa kecepatan troli?", "0,375 m/s (≈ 0,38 m/s)",
          "Garis melalui (0 ; 0,25) dan (4 ; 1,75): 1,5 : 4 = 0,375 m/s.", fig=render(TP["data-st"], points=DATA_GLB_ITEM, lines=[(0, 0.25, 4, 1.75, False)])),
        Q(2, "Posisi sebuah benda tercatat setiap 1 s: s = 0; 1; 4; 9; 16; 25 m. Tentukan jenis gerak dan percepatannya.", "GLBB, a = 2 m/s²", "Perpindahan tiap sekon: 1; 3; 5; 7; 9. Selisihnya tetap 2 m, jadi a = 2 : 1² = 2 m/s²."),
        Q(2, "Ponsel merekam kecepatan troli yang didorong lalu dilepas (titik). Garis merah adalah garis terbaik. Berapa percepatannya?", "−0,3 m/s²",
          "Garis melalui (0 ; 1,2) dan (4 ; 0): (0 − 1,2) : 4 = −0,3 m/s².", fig=render(TP["data-vt"], points=DATA_V_ITEM, lines=[(0, 1.2, 4, 0, False)])),
        Q(2, "Untuk troli pada soal sebelumnya, berapa jarak yang ditempuhnya selama 4 s?", "2,4 m", "Luas segitiga di bawah garis terbaik: ½ · 1,2 · 4 = 2,4 m."),
        Q(2, "Posisi troli ber-GLB tercatat setiap 0,5 s: s = 0; 0,5; 1,0; 2,3; 2,0; 2,5 m. Data mana yang kemungkinan salah ukur, dan berapa kecepatan troli?", "data ke-4 (t = 1,5 s, s = 2,3 m); 1 m/s",
          "Pola yang lain naik 0,5 m tiap 0,5 s, jadi pada t = 1,5 s seharusnya 1,5 m. v = 0,5 : 0,5 = 1 m/s."),
        Q(3, "Data posisi sebuah troli (setiap 0,5 s): s = " + "; ".join(n(y) for _, y in DATA_TABLE_NOISY) + " m. Hitung kecepatannya dengan dua cara: (a) dari t = 1,0 s dan t = 1,5 s; (b) dari t = 0 dan t = 4,0 s. Cara mana yang lebih dapat dipercaya?",
          f"(a) {n((DATA_TABLE_NOISY[3][1] - DATA_TABLE_NOISY[2][1]) / 0.5)} m/s; (b) {n((DATA_TABLE_NOISY[8][1] - DATA_TABLE_NOISY[0][1]) / 4)} m/s; cara (b)",
          "Cara (b) memakai selang 4 s sehingga derau beberapa sentimeter hanya sedikit memengaruhi hasil."),
        Q(3, "Posisi sebuah troli dicatat setiap 0,2 s: s = 0; 0,02; 0,08; 0,18; 0,32; 0,50 m. Tentukan jenis gerak, percepatan, dan kecepatan troli pada t = 1,0 s.", "GLBB; a = 1 m/s²; v = 1 m/s",
          "Perpindahan: 0,02; 0,06; 0,10; 0,14; 0,18 m; selisih tetap 0,04 m. a = 0,04 : 0,2² = 1 m/s². Dari diam: v(1,0) = 1 · 1,0 = 1 m/s."),
        Q(3, "Sebutkan tiga cara membuat data pelacakan gerak dengan ponsel lebih bersih.", "contoh: pasang ponsel kokoh, ulangi beberapa kali lalu dirata-rata, pakai selang waktu dan jarak yang panjang",
          "Cara lain: kurangi getaran, rekam dengan laju pencuplikan yang lebih tinggi, ratakan beberapa titik berurutan (rata-rata bergerak), pastikan objek tetap terlihat jelas oleh kamera."),
    ],
))

CAMPURAN = [
    Q(1, "Posisi benda s = 5 + 2t (SI). Jenis geraknya dan kecepatannya?", "GLB, 2 m/s", "s linear terhadap t."),
    Q(1, "Kecepatan benda v = 4 − 2t (SI). Kapan benda berhenti sesaat?", "t = 2 s", "4 − 2t = 0."),
    Q(1, "Grafik v–t sebuah benda berupa garis mendatar pada v = −3 m/s. Jenis gerak dan arahnya?", "GLB ke arah negatif", "v tetap dan negatif."),
    Q(1, "Mobil melaju tetap 36 km/jam selama 1 menit. Berapa jarak tempuhnya?", "600 m", "36 km/jam = 10 m/s; 10 · 60 = 600 m."),
    Q(2, "Posisi benda s = 3t² − 12t (SI). Kapan benda berbalik arah dan di mana posisinya saat itu?", "t = 2 s; s = −12 m", "v₀ = −12 m/s, a = 6 m/s². v = −12 + 6t = 0 → t = 2 s; s = 12 − 24 = −12 m."),
    Q(2, "Mobil yang melaju 10 m/s dipercepat 2 m/s² dan menempuh 75 m. Berapa kecepatan akhir dan waktunya?", "20 m/s; 5 s", "v² = 100 + 300 = 400 → v = 20 m/s; t = (20 − 10) : 2 = 5 s."),
    Q(2, "Pada grafik s–t, garis benda A dan B berpotongan di t = 6 s, s = 24 m. Apa arti titik itu?", "A dan B bertemu di s = 24 m pada t = 6 s", "Titik potong pada grafik s–t berarti posisinya sama."),
    Q(2, "Ponsel mencatat perpindahan sebuah troli setiap 0,2 s: 0,12; 0,20; 0,28; 0,36 m. Tentukan jenis gerak dan percepatannya.", "GLBB; a = 2 m/s²", "Selisih berurutan tetap 0,08 m; a = 0,08 : 0,04 = 2 m/s²."),
    Q(2, "Kereta melaju 20 m/s lalu melambat 0,5 m/s² sampai berhenti. Berapa jarak dan waktu pengeremannya?", "400 m; 40 s", "20² : (2 · 0,5) = 400 m; 20 : 0,5 = 40 s."),
    Q(3, "Kereta B melaju 30 m/s dan berada 100 m di belakang kereta A yang melaju 20 m/s searah pada rel yang sama. Masinis B mengerem saat itu juga. Berapa perlambatan minimal B agar tidak menabrak A?", "0,5 m/s²",
      "Relatif terhadap A, B mendekat 10 m/s dan harus berhenti relatif dalam 100 m: 10² = 2 · a · 100 → a = 0,5 m/s²."),
]

# ------------------------------------------------------------------ TKA-level items
TKA_A, TKA_B = Motion(0, 0, [(5, 4), (5, 0)], "A", BLUE), Motion(0, 12, [(10, 0)], "B", RED)
TKA_ST = [(0, 0), (4, 20), (6, 20), (10, 0)]
TKA_VT = Motion(0, 8, [(4, -2), (4, 0)])
TKA = [
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Mobil A (dari diam) dan motor B mulai bergerak dari garis start yang sama pada saat yang sama. Grafik v–t keduanya ditunjukkan di bawah.",
         fig=render(TP["glbb-vt"], (TKA_A, TKA_B)), soal2="Mobil A menyusul motor B setelah menempuh jarak ....",
         opsi=["18 m", "36 m", "60 m", "75 m", "100 m"], kunci=3,
         bahas="A: s = 2t² sampai t = 5 s (50 m, v = 20 m/s), lalu GLB. B: s = 12t, pada t = 5 s di 60 m, masih di depan. Setelah itu 50 + 20(t − 5) = 12t → t = 6,25 s; s = 12 · 6,25 = 75 m.",
         salah="A: posisi A pada titik potong grafik (t = 3 s). B: posisi B pada titik potong (titik potong dianggap saat menyusul). C: posisi B pada t = 5 s. E: tidak sesuai luas grafik."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Grafik s–t seorang pelari pada lintasan lurus ditunjukkan di bawah.", fig=piecewise_st(TKA_ST, "glb-st"),
         soal2="Pernyataan yang tepat tentang gerak pelari adalah ....",
         opsi=["Pelari diam pada selang 4–6 s dan kembali ke titik awal pada t = 10 s.", "Pelari bergerak dengan kecepatan tetap 5 m/s selama 10 s.",
               "Pelari dipercepat pada 0–4 s dan diperlambat pada 6–10 s.", "Jarak yang ditempuh pelari selama 10 s adalah 0.", "Kecepatan pelari pada selang 6–10 s adalah 5 m/s."], kunci=0,
         bahas="Grafik mendatar 4–6 s (diam); s(10) = 0 (kembali). 0–4 s: v = 5 m/s; 6–10 s: v = −5 m/s.",
         salah="B: arah berubah dan ada saat diam. C: garis lurus berarti GLB, bukan dipercepat. D: jarak 40 m; yang nol adalah perpindahan. E: kecepatannya −5 m/s."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Grafik v–t sebuah troli ditunjukkan di bawah.", fig=G("glbb-vt2", TKA_VT, w=280, h=170),
         soal2="Grafik a–t yang sesuai adalah ....", opsi="TKA_AT", kunci=1,
         bahas="0–4 s: a = (0 − 8) : 4 = −2 m/s². 4–8 s: v tetap 0, a = 0.",
         salah="A: tanda percepatan terbalik. C: menyalin bentuk v–t. D: percepatan dianggap berlaku 8 s."),
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Sebuah mobil melaju 72 km/jam di jalan lurus. Pengemudi melihat kucing di depan dan menginjak rem setelah waktu reaksi 0,5 s. Rem memberi perlambatan tetap 5 m/s². Jarak henti mobil sejak pengemudi melihat kucing adalah ....",
         opsi=["10 m", "36 m", "40 m", "50 m", "90 m"], kunci=3,
         bahas="72 km/jam = 20 m/s. Jarak reaksi 20 · 0,5 = 10 m; jarak pengereman 20² : 10 = 40 m; total 50 m.",
         salah="A: hanya jarak reaksi. B: memakai 72 · 0,5 tanpa konversi satuan. C: lupa jarak reaksi. E: lupa faktor 2 pada v²/2a (10 + 80)."),
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Pesawat latih bergerak dari diam di landasan lurus dan harus mencapai 80 m/s untuk lepas landas. Panjang landasan yang tersedia 1.600 m. Percepatan tetap minimal yang diperlukan adalah ....",
         opsi=["0,05 m/s²", "1 m/s²", "2 m/s²", "4 m/s²", "20 m/s²"], kunci=2,
         bahas="80² = 2 · a · 1.600 → a = 6.400 : 3.200 = 2 m/s².", salah="B: membagi 1.600 dengan 1.600. D: lupa faktor 2. A, E: rasio terbalik atau tanpa kuadrat."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Sebuah mobil melaju 20 m/s ketika lampu lalu lintas berubah kuning, 45 m sebelum garis berhenti. Lampu kuning menyala 3 s sebelum merah. Waktu reaksi pengemudi 0,5 s dan perlambatan rem maksimum 5 m/s². Keputusan dan akibat yang paling tepat adalah ....",
         opsi=["Mobil tidak dapat berhenti sebelum garis; bila terus melaju tetap, mobil melewati garis sebelum lampu merah.",
               "Mobil dapat berhenti tepat 5 m sebelum garis bila pengemudi segera mengerem.",
               "Mobil harus mengerem karena bila terus melaju akan melewati garis setelah lampu merah.",
               "Mobil tidak dapat berhenti sebelum garis dan bila terus melaju juga akan melanggar lampu merah.",
               "Mobil dapat berhenti sebelum garis asal perlambatannya 4 m/s²."], kunci=0,
         bahas="Jarak henti = 20 · 0,5 + 20² : 10 = 50 m > 45 m, jadi tidak dapat berhenti sebelum garis. Bila melaju tetap, mobil mencapai garis setelah 45 : 20 = 2,25 s < 3 s, sebelum merah.",
         salah="B: lupa jarak reaksi (40 m). C, D: waktu melaju 2,25 s masih sebelum merah. E: perlambatan lebih kecil justru memperpanjang jarak henti."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Pengendara melaju tetap 20 m/s melewati polisi yang diam. Saat itu juga polisi mengejar dengan percepatan tetap. Dengan percepatan 2,5 m/s², polisi menyusul setelah 16 s. Jika polisi hanya mampu berakselerasi setengahnya, yaitu 1,25 m/s², maka ....",
         opsi=["polisi menyusul setelah 32 s, di titik 640 m dari tempat semula", "polisi menyusul setelah 16 s juga karena pengendara bergerak tetap",
               "polisi menyusul setelah 32 s, di titik 320 m dari tempat semula", "polisi menyusul setelah 22,6 s, di titik 452 m dari tempat semula",
               "polisi tidak pernah dapat menyusul pengendara"], kunci=0,
         bahas="½ · 1,25 · t² = 20t → t = 32 s; s = 20 · 32 = 640 m. Waktu menyusul berbanding terbalik dengan percepatan.",
         salah="B: waktu bergantung pada percepatan. C: jarak tidak ikut berubah. D: memakai √2. E: pada GLBB kecepatan polisi terus bertambah, jadi selalu dapat menyusul."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="pg",
         soal="Pengemudi melaju 20 m/s dan melihat penghalang 40 m di depan. Waktu reaksinya 0,4 s. Ia ingin berhenti tepat sebelum penghalang dengan pengereman tetap. Strategi pengereman yang memenuhi tujuan dengan perlambatan sekecil mungkin adalah ....",
         opsi=["mengerem dengan perlambatan 6,25 m/s²", "mengerem dengan perlambatan 5 m/s²", "mengerem dengan perlambatan 4 m/s²",
               "mengerem dengan perlambatan 10 m/s²", "tidak perlu mengerem karena jarak 40 m sudah cukup"], kunci=0,
         bahas="Jarak tersedia untuk mengerem = 40 − 20 · 0,4 = 32 m. a = 20² : (2 · 32) = 6,25 m/s². Perlambatan 10 m/s² juga berhenti, tetapi bukan yang terkecil.",
         salah="B: lupa jarak reaksi (40 m dipakai seluruhnya). C: perlambatan terlalu kecil (berhenti setelah 58 m). D: berhenti, tetapi bukan perlambatan terkecil. E: menabrak."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="bs",
         soal="Bus harus menempuh 1,8 km di jalan lurus antara dua halte dalam waktu <b>tidak lebih dari 2 menit</b>, dimulai dan diakhiri dalam keadaan diam. Kecepatan bus dibatasi <b>20 m/s</b>, dan percepatan maupun perlambatannya 1 m/s². Tentukan apakah setiap strategi berikut tepat.",
         opsi=["Dipercepat sampai 20 m/s, melaju tetap, lalu direm sampai berhenti tepat di halte.",
               "Dipercepat sampai 15 m/s, melaju tetap, lalu direm sampai berhenti tepat di halte.",
               "Dipercepat terus sampai pertengahan jalan, lalu direm sampai berhenti di halte.",
               "Dipercepat sampai 20 m/s, melaju tetap, lalu mulai mengerem 100 m sebelum halte."],
         kunci=[True, False, False, False],
         bahas="1: 20 s + 70 s + 20 s = 110 s ≤ 120 s (Tepat). 2: 15 s + 105 s + 15 s = 135 s (Tidak Tepat). 3: kecepatan di tengah √1.800 ≈ 42 m/s melanggar batas (Tidak Tepat). 4: pengereman dari 20 m/s butuh 200 m, bus melewati halte (Tidak Tepat).",
         salah=""),
    dict(tipe="FIS-EKSP", lv=3, fmt="pg",
         soal="Siswa menyelidiki pengaruh kemiringan lintasan terhadap percepatan troli. Troli yang sama dilepas dari keadaan diam pada lintasan dengan sudut 5°, 10°, dan 15°. Ponsel yang dipasang di troli merekam kecepatan setiap 0,05 s, lalu percepatan dihitung dari kemiringan garis terbaik grafik v–t.",
         soal2="Variabel bebas, variabel terikat, dan variabel kontrol pada percobaan ini berturut-turut adalah ....",
         opsi=["sudut lintasan; percepatan troli; massa troli dan posisi lepas", "percepatan troli; sudut lintasan; massa troli",
               "massa troli; percepatan troli; sudut lintasan", "sudut lintasan; massa troli; percepatan troli", "waktu rekam; kecepatan troli; sudut lintasan"], kunci=0,
         bahas="Yang sengaja diubah adalah sudut; yang diukur adalah percepatan; yang dijaga tetap antara lain troli (massanya) dan titik lepas.",
         salah="B: bebas dan terikat tertukar. C, D: massa dijaga tetap, bukan diubah atau diukur. E: waktu rekam bukan yang diselidiki."),
    dict(tipe="FIS-KONSEP", lv=2, fmt="pgk",
         soal="Pernyataan yang benar tentang grafik gerak lurus adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["Titik potong dua garis pada grafik v–t menunjukkan saat kecepatan kedua benda sama.", "Luas di bawah grafik v–t menyatakan perpindahan.",
               "Grafik s–t yang mendatar menunjukkan benda bergerak dengan kecepatan tetap yang tidak nol.", "Kemiringan garis singgung grafik s–t menyatakan kecepatan sesaat.",
               "Percepatan negatif selalu berarti benda sedang diperlambat."], kunci=[0, 1, 3],
         bahas="A, B, dan D sesuai definisi.", salah="C: s–t mendatar berarti diam. E: bila v juga negatif, benda dipercepat ke arah negatif."),
]

# graph options (A–D) for the two graph-choice items
def at_option(segs, color=BLUE):
    return Motion(0, 0, segs, color=color)


GRAPH_OPTS = {
    # Latihan 4.13: s–t options for the trapezoid v–t (TRAP). Key B.
    "TRAP": [render(TP["glbb-vt"], (Motion(0, 0, [(2, 5), (4, 0), (2, -5)]),), width=210, height=135).replace("v (m/s)", "s (m)"),   # A: v–t shape copied
             render(TP["glbb-st"], (TRAP,), width=210, height=135),                                                                        # B: key
             render(TP["glbb-st"], (Motion(0, 0, [(2, 5), (4, 0), (2, -5)]),), lines=[(8, 60, 10, 40, False)], width=210, height=135)
             .replace('stroke="#c0502a" stroke-width="1.6"', f'stroke="{BLUE}" stroke-width="2.2"'),                                     # C: position falls at the end
             render(TP["glbb-st"], (), lines=[(0, 0, 2, 10, False), (2, 10, 6, 50, False), (6, 50, 8, 60, False)], width=210, height=135)
             .replace('stroke="#c0502a" stroke-width="1.6"', f'stroke="{BLUE}" stroke-width="2.2"')],                                    # D: all straight
    # TKA a–t options for TKA_VT. Key B.
    "TKA_AT": [render(TP["glbb-at"], (at_option([(4, 2), (4, 0)]),), width=210, height=135),
               render(TP["glbb-at"], (at_option([(4, -2), (4, 0)]),), width=210, height=135),
               render(TP["glbb-at"], (), lines=[(0, 4, 4, 0, False), (4, 0, 8, 0, False)], width=210, height=135)
               .replace('stroke="#c0502a" stroke-width="1.6"', f'stroke="{BLUE}" stroke-width="2.2"'),
               render(TP["glbb-at"], (at_option([(8, -2)]),), width=210, height=135)],
}
GRAPH_OPT_KEYS = {"TRAP": 1, "TKA_AT": 1}

# ------------------------------------------------------------------ Uji kompetensi
UJI_PG = [
    ("Posisi benda s = 4 + 3t (SI). Kecepatannya adalah ....", ["4 m/s", "3 m/s", "7 m/s", "12 m/s", "1 m/s"], 1, "Bentuk s = s₀ + vt.", "A: posisi awal. C: 4 + 3. D: 4 · 3. E: 4 − 3."),
    ("Grafik s–t sebuah benda berupa garis mendatar. Benda itu ....", ["diam", "bergerak lurus beraturan", "dipercepat beraturan", "diperlambat beraturan", "berbalik arah"], 0,
     "Posisinya tidak berubah.", "B: GLB berupa garis miring. C, D: GLBB berupa parabola. E: tidak ada perubahan arah."),
    ("Grafik v–t sebuah benda berupa garis lurus naik dari titik asal. Gerak benda adalah ....", ["GLB", "GLBB dipercepat", "GLBB diperlambat", "diam", "berbalik arah"], 1,
     "v bertambah tetap.", "A: GLB berupa garis mendatar. C: garis turun. D, E: tidak sesuai."),
    ("Kecepatan benda naik beraturan dari 0 menjadi 12 m/s dalam 4 s. Perpindahannya selama 4 s adalah ....", ["48 m", "24 m", "12 m", "3 m", "36 m"], 1,
     "Luas segitiga ½ · 12 · 4 = 24 m.", "A: lupa ½. C: kecepatan akhir. D: percepatan. E: tidak ada dasar."),
    ("Untuk benda pada soal 4, percepatannya adalah ....", ["48 m/s²", "12 m/s²", "3 m/s²", "4 m/s²", "0,33 m/s²"], 2, "12 : 4 = 3 m/s².", "A, B: bukan kemiringan. D: waktu. E: kebalikannya."),
    ("Mobil melaju tetap 90 km/jam selama 20 s. Jarak tempuhnya adalah ....", ["1.800 m", "500 m", "4,5 m", "250 m", "180 m"], 1, "90 km/jam = 25 m/s; 25 · 20 = 500 m.", "A: lupa konversi. C: 90 : 20. D, E: konversi salah."),
    ("Benda bergerak dari diam dengan percepatan 4 m/s². Perpindahannya setelah 5 s adalah ....", ["20 m", "100 m", "50 m", "10 m", "25 m"], 2, "½ · 4 · 25 = 50 m.", "A: v · t tanpa ½ dan tanpa kuadrat. B: lupa ½. D, E: tidak ada dasar."),
    ("Benda bergerak dari diam dengan percepatan 2 m/s² dan menempuh 25 m. Kecepatannya saat itu adalah ....", ["50 m/s", "10 m/s", "100 m/s", "5 m/s", "7,1 m/s"], 1, "v² = 2 · 2 · 25 = 100.", "A: 2 · 25. C: lupa diakar. D: tanpa faktor 2. E: √50."),
    ("Mobil yang melaju 30 m/s direm dengan perlambatan 6 m/s². Waktu sampai berhenti adalah ....", ["5 s", "180 s", "0,2 s", "24 s", "36 s"], 0, "30 : 6 = 5 s.", "B: dikalikan. C: kebalikannya. D: 30 − 6. E: 30 + 6."),
    ("Mobil melaju 15 m/s. Waktu reaksi pengemudi 1 s dan perlambatan rem 5 m/s². Jarak hentinya adalah ....", ["22,5 m", "15 m", "37,5 m", "30 m", "45 m"], 2,
     "15 · 1 + 15² : 10 = 37,5 m.", "A: lupa jarak reaksi. B: hanya jarak reaksi. D: memakai v · t untuk pengereman. E: lupa faktor 2."),
    ("Benda A di s = 0 bergerak 5 m/s; benda B di s = 60 m bergerak −7 m/s. Keduanya bertemu pada ....", ["t = 5 s, s = 25 m", "t = 12 s, s = 60 m", "t = 30 s, s = 150 m", "t = 5 s, s = 35 m", "t = 8,6 s, s = 43 m"], 0,
     "5t = 60 − 7t → t = 5 s; s = 25 m.", "B: 60 : 5. C: 60 : (7 − 5). D: posisi dari B salah tanda. E: tidak ada dasar."),
    ("Posisi benda s = t² + 2t (SI). Kecepatan sesaat pada t = 3 s adalah ....", ["5 m/s", "8 m/s", "15 m/s", "6 m/s", "3 m/s"], 1,
     "v₀ = 2, a = 2: v(3) = 2 + 2 · 3 = 8 m/s.", "A: kecepatan rata-rata s(3) : 3. C: posisinya. D: 2 · 3 saja. E: waktunya."),
    ("Ponsel mencatat perpindahan troli setiap 0,5 s: 0,1; 0,3; 0,5; 0,7 m. Percepatan troli adalah ....", ["0,2 m/s²", "0,4 m/s²", "0,8 m/s²", "1,6 m/s²", "0,1 m/s²"], 2,
     "Selisih 0,2 m; a = 0,2 : 0,25 = 0,8 m/s².", "A: selisihnya saja. B: dibagi 0,5. D: dikali 2 lagi. E: tidak ada dasar."),
    ("Benda bergerak dengan v = −6 m/s dan a = −2 m/s². Pernyataan yang tepat adalah ....", ["benda diperlambat", "benda dipercepat ke arah negatif", "benda diam", "benda segera berbalik arah", "benda ber-GLB"], 1,
     "v dan a searah, kelajuan bertambah.", "A: tanda negatif tidak berarti melambat. C, E: ada kecepatan dan percepatan. D: berbalik bila v dan a berlawanan."),
    ("Dua mobil mulai dari tempat yang sama. Garis v–t keduanya berpotongan pada t = 4 s. Artinya, pada t = 4 s ....", ["kecepatan kedua mobil sama", "kedua mobil bertemu", "kedua mobil berhenti", "percepatan kedua mobil sama", "perpindahan kedua mobil sama"], 0,
     "Titik potong grafik v–t berarti v sama.", "B, E: bertemu bila luas di bawah grafik sama. C: v belum tentu nol. D: kemiringan berbeda."),
]
UJI_URAIAN = [
    ("KRL dipercepat 1 m/s² dari diam sampai 15 m/s, melaju tetap 60 s, lalu direm 1,5 m/s² sampai berhenti. (a) Gambarlah grafik v–t-nya. (b) Hitung jarak antarstasiun dan waktu tempuhnya.",
     "(b) 1.087,5 m; 85 s", "Bagian 1: 15 s, 112,5 m. Bagian 2: 900 m. Bagian 3: 10 s, 75 m. Total 1.087,5 m dalam 85 s."),
    ("Posisi benda s = 20 + 8t − t² (SI). (a) Kapan benda berbalik arah dan di mana? (b) Tentukan perpindahan dan jaraknya selama 0–10 s.",
     "(a) t = 4 s, s = 36 m; (b) perpindahan −20 m, jarak 52 m", "v₀ = 8, a = −2: v = 0 pada t = 4 s; s(4) = 36 m. s(10) = 0. Perpindahan 0 − 20 = −20 m; jarak 16 + 36 = 52 m."),
    ("Pengendara melaju tetap 25 m/s melewati polisi yang diam. Saat itu juga polisi mengejar dengan percepatan 2 m/s². Kapan dan di mana polisi menyusul, dan berapa kecepatan polisi saat itu?",
     "25 s; 625 m; 50 m/s", "t² = 25t → t = 25 s; s = 625 m; v = 2 · 25 = 50 m/s."),
    ("Ponsel merekam posisi troli setiap 0,5 s: s = 0; 0,15; 0,60; 1,35; 2,40; 3,75 m. (a) Tunjukkan bahwa geraknya GLBB. (b) Tentukan percepatan dan kecepatannya pada t = 2,5 s.",
     "(b) a = 1,2 m/s²; v = 3 m/s", "Perpindahan: 0,15; 0,45; 0,75; 1,05; 1,35, selisih tetap 0,30 m. a = 0,30 : 0,25 = 1,2 m/s². Dari diam: v(2,5) = 1,2 · 2,5 = 3 m/s."),
    ("Mobil melaju 15 m/s, 25 m sebelum garis berhenti, ketika lampu berubah kuning. Waktu reaksi 0,5 s dan perlambatan rem 6 m/s². (a) Dapatkah mobil berhenti sebelum garis? (b) Berapa perlambatan minimal agar dapat berhenti tepat di garis?",
     "(a) tidak, jarak henti 26,25 m; (b) ≈ 6,43 m/s²", "(a) 7,5 + 225 : 12 = 26,25 m > 25 m. (b) Jarak untuk mengerem 25 − 7,5 = 17,5 m; a = 225 : 35 ≈ 6,43 m/s²."),
]


def check():
    c = lambda a, b, t=1e-6: abs(a - b) <= t or (_ for _ in ()).throw(AssertionError((a, b)))
    # subbab 1
    c(M1.s(2), 10); c(M1.s(4), 30); c(M1.s(6), 40)
    c(P1.s(4), 8); c(P1.v(4), 4); c(20 / 5, 4)                        # tangent of s = ½t² at t = 4: s = 4t − 8
    c(4 * 2 - 8, 0); c(4 * 7 - 8, 20)
    c(P2.v(4), 8); c(8 * 2 - 16, 0); c(8 * 6 - 16, 32); c((P2.s(6) - P2.s(2)) / 4, 8)
    c(10 + 2 * 5, 20)
    # subbab 2
    c(C21.s(8), 22); c(SK8.s(6), -20); c(-4 * 8, -32); c(450 / 15, 30); c(50 / (25 - 15), 5); c(3 / 30 * 18, 1.8); c(60 * 2, 80 * 1.5); c(12 - 12, 0)
    # subbab 3
    c(C31.a(1), 2); c(C31.s(6), 60); c(V3.s(6), 48); c(S3.v(2), 6); c(6 * 0 + 4, 4); c(6 * 6 + 4, 40); c(S3.s(2), 16); c(S3.v(5), 0)
    c(REV.v(3), 0); c(D13.s(6), 12); c(D13.distance(0, 6), 20, 1e-3); c(CAR.s(10), BIKE.s(10)); c(CAR.s(5), 25); c(BIKE.s(5), 50)
    c((10 ** 2 - 30 ** 2) / (2 * 400), -1); c(0.5 * 4 * 9 - 0.5 * 4 * 4, 10); c((36 - 100) / -4, 16)
    # subbab 4
    c(ANGKOT.s(20), 120); c(TRAP.s(8), 60); c(BUS.s(20), 210); c(TROLI.v(8), 0)
    c(25 + 25 ** 2 / 10, 87.5); c(9 + 225 / 10, 31.5); c(160 + 1600 + 80, 1840); c(1840 / 130, 14.15, 0.01)
    c(10 * 10 + 10 ** 2, 200); c(0.5 * 2.5 * 16 ** 2, 20 * 16)
    # subbab 5: the drawn best-fit lines are close to the least-squares fit of the data
    c(lsq_slope(DATA_GLB), 0.5, 0.03); c(lsq_slope(DATA_GLB_ITEM), 0.375, 0.03)
    c(lsq_slope(DATA_V_BERTAHAP), 0.3, 0.03); c(lsq_slope(DATA_V_ITEM), -0.3, 0.03)
    c(lsq_slope(DATA_TABLE_NOISY), 0.8, 0.03)
    s = [0, 0.02, 0.08, 0.18, 0.32, 0.50]
    d = [round(b - a, 4) for a, b in zip(s, s[1:])]
    c(d[1] - d[0], 0.04); c(0.04 / 0.04, 1)
    # TKA
    c(TKA_A.s(5), 50); c(TKA_A.v(3), TKA_B.v(3)); c(TKA_A.s(6.25), TKA_B.s(6.25)); c(TKA_B.s(6.25), 75); c(TKA_A.s(3), 18); c(TKA_B.s(3), 36); c(10 + 400 / 10, 50); c(6400 / 3200, 2); c(10 + 40, 50); c(45 / 20, 2.25)
    c(20 * 32, 640); c(400 / 64, 6.25); c(20 + 70 + 20, 110); c(15 + 1575 / 15 + 15, 135); c(math.sqrt(1800), 42.43, 0.01)
    # uji
    c(112.5 + 900 + 75, 1087.5); c(20 + 8 * 10 - 100, 0); c(16 + 36, 52); c(7.5 + 225 / 12, 26.25); c(225 / 35, 6.43, 0.01)
    c(0.30 / 0.25, 1.2)
    return True
