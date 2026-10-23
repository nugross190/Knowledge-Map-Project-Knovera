"""Content of the printable module "Trigonometri" (Matematika kelas X).

Ratios in a right triangle, special angles, heights and distances, angles in every quadrant,
the basic identities and the area formula ½ab sin C. Every numeric answer is re-derived in check().
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import plane  # noqa: E402
from kit import fr, Q, close  # noqa: E402

BLUE, RED, GREEN, INK = "#1f3a68", "#c0502a", "#2e6b32", "#1f2430"
th = "θ"


def sin(d):
    return math.sin(math.radians(d))


def cos(d):
    return math.cos(math.radians(d))


def tan(d):
    return math.tan(math.radians(d))


def poly(pts, names=(), sides=(), arcs=(), right=None, dashed=(), labels=(), w=230, h=150, pad=24):
    """A figure of a polygon in plane units.

    names: one label per vertex. sides: [(i, j, text, color)]. arcs: [(vertex, p1, p2, text)] with points in
    plane units. right: vertex index with a right-angle mark. dashed: [(x1, y1, x2, y2)]. labels: [(x, y, text)].
    """
    every = list(pts) + [p for d in dashed for p in (d[:2], d[2:4])] + [l[:2] for l in labels]
    x0, x1 = min(p[0] for p in every), max(p[0] for p in every)
    y0, y1 = min(p[1] for p in every), max(p[1] for p in every)
    s = min((w - 2 * pad) / max(x1 - x0, 1e-9), (h - 2 * pad) / max(y1 - y0, 1e-9))
    ox = (w - (x1 - x0) * s) / 2
    oy = (h - (y1 - y0) * s) / 2
    X = lambda x: ox + (x - x0) * s
    Y = lambda y: h - oy - (y - y0) * s
    cx = sum(X(p[0]) for p in pts) / len(pts)
    cy = sum(Y(p[1]) for p in pts) / len(pts)
    out = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,DejaVu Sans,sans-serif">']
    out.append('<polygon points="' + " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts) + f'" fill="#eef2f8" stroke="{BLUE}" stroke-width="1.6"/>')
    for x1_, y1_, x2_, y2_ in dashed:
        out.append(f'<line x1="{X(x1_):.1f}" y1="{Y(y1_):.1f}" x2="{X(x2_):.1f}" y2="{Y(y2_):.1f}" stroke="{INK}" stroke-width="1" stroke-dasharray="4 3"/>')
    if right is not None:
        v = pts[right]
        a, b = pts[right - 1], pts[(right + 1) % len(pts)]
        def unit(p):
            dx, dy = X(p[0]) - X(v[0]), Y(p[1]) - Y(v[1])
            r = math.hypot(dx, dy)
            return dx / r * 8, dy / r * 8
        (ax, ay), (bx, by) = unit(a), unit(b)
        vx, vy = X(v[0]), Y(v[1])
        out.append(f'<path d="M{vx+ax:.1f} {vy+ay:.1f} L{vx+ax+bx:.1f} {vy+ay+by:.1f} L{vx+bx:.1f} {vy+by:.1f}" fill="none" stroke="{INK}" stroke-width="0.9"/>')
    for v, p1, p2, text in arcs:
        vx, vy = X(v[0]), Y(v[1])
        u = []
        for p in (p1, p2):
            dx, dy = X(p[0]) - vx, Y(p[1]) - vy
            r = math.hypot(dx, dy)
            u.append((dx / r, dy / r))
        (u1x, u1y), (u2x, u2y) = u
        sweep = 1 if u1x * u2y - u1y * u2x > 0 else 0
        r = 16
        out.append(f'<path d="M{vx+r*u1x:.1f} {vy+r*u1y:.1f} A{r} {r} 0 0 {sweep} {vx+r*u2x:.1f} {vy+r*u2y:.1f}" fill="none" stroke="{RED}" stroke-width="1.1"/>')
        bx, by = u1x + u2x, u1y + u2y
        bl = math.hypot(bx, by) or 1
        out.append(f'<text x="{vx+27*bx/bl:.1f}" y="{vy+27*by/bl+3:.1f}" font-size="9" text-anchor="middle" fill="{RED}">{text}</text>')
    for k, name in enumerate(names):
        if not name:
            continue
        x, y = X(pts[k][0]), Y(pts[k][1])
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy) or 1
        out.append(f'<text x="{x+11*dx/r:.1f}" y="{y+11*dy/r+3:.1f}" font-size="9.5" font-weight="700" text-anchor="middle" fill="{INK}">{name}</text>')
    for i, j, text, color in sides:
        mx, my = (X(pts[i][0]) + X(pts[j][0])) / 2, (Y(pts[i][1]) + Y(pts[j][1])) / 2
        dx, dy = mx - cx, my - cy
        r = math.hypot(dx, dy) or 1
        out.append(f'<text x="{mx+11*dx/r:.1f}" y="{my+11*dy/r+3:.1f}" font-size="9" text-anchor="middle" fill="{color}">{text}</text>')
    for x, y, text in labels:
        out.append(f'<text x="{X(x):.1f}" y="{Y(y):.1f}" font-size="9" text-anchor="middle" fill="{INK}">{text}</text>')
    out.append("</svg>")
    return "".join(out)


def circle(r):
    return [(lambda x, r=r: math.sqrt(max(r * r - x * x, 0)), -r, r, "#9aa6b8", ""), (lambda x, r=r: -math.sqrt(max(r * r - x * x, 0)), -r, r, "#9aa6b8", "")]


PRASYARAT = [
    ("P1", "Sisi tegak segitiga siku-siku 5 dan 12. Hitung sisi miringnya.", "13", "√(25 + 144)."),
    ("P2", "Rasionalkan " + fr(6, "√3") + ".", "2√3", "6√3 : 3."),
    ("P3", "Sederhanakan √48.", "4√3", "√(16 · 3)."),
    ("P4", "Sisi tegak segitiga siku-siku sama kaki 4 cm. Hitung sisi miringnya.", "4√2 cm", "√(16 + 16)."),
    ("P5", "Dua sudut segitiga 90° dan 35°. Berapa sudut ketiga?", "55°", "180° − 125°."),
    ("P6", "Hitung (⅗)² + (⅘)².", "1", "9/25 + 16/25."),
    ("P7", "Selesaikan " + fr("x", 8) + " = " + fr(3, 4) + ".", "x = 6", "x = 8 · ¾."),
    ("P8", "Titik (−3, 4) berada di kuadran berapa, dan berapa jaraknya ke titik O(0, 0)?", "Kuadran II; 5", "x negatif, y positif; √(9 + 16)."),
]

INGAT = [
    ("A", "Pythagoras dan bentuk akar", "P1, P2, P3, P4", "Subbab 1–3", ["Sisi miring² = jumlah kuadrat sisi tegak. Tripel: 3-4-5, 5-12-13, 8-15-17, 7-24-25.", "√(a² · b) = a√b; " + fr("a", "√b") + " = " + fr("a√b", "b") + "."]),
    ("B", "Jumlah sudut segitiga", "P5", "Subbab 1, 3", ["Jumlah sudut segitiga 180°; pada segitiga siku-siku, dua sudut lancipnya berjumlah 90°."]),
    ("C", "Pecahan dan perbandingan", "P6, P7", "Subbab 1, 5", ["Kalikan silang untuk menyelesaikan perbandingan; kuadrat pecahan = kuadrat pembilang per kuadrat penyebut."]),
    ("D", "Kuadran bidang koordinat", "P8", "Subbab 4", ["Kuadran I (+, +), II (−, +), III (−, −), IV (+, −), berlawanan arah jarum jam mulai sumbu x positif."]),
]


def segi(a, b, names=("A", "B", "C"), sa=None, de=None, mi=None, angle=th, w=220, h=140):
    """Right triangle: A bottom-left (angle), B bottom-right (right angle), C top-right."""
    pts = [(0, 0), (a, 0), (a, b)]
    sides = [(i, j, t, c) for i, j, t, c in ((0, 1, sa, INK), (1, 2, de, INK), (0, 2, mi, INK)) if t]
    arcs = [((0, 0), (a, 0), (a, b), angle)] if angle else []
    return poly(pts, names, sides, arcs, right=1, w=w, h=h)


SUB = []

# ================================================================== Subbab 1
F11 = segi(8, 6, sa="8", de="6", mi="?", angle="A", names=("A", "B", "C"))
SUB.append(dict(
    title="Perbandingan Trigonometri pada Segitiga Siku-Siku",
    tujuan="Menentukan sinus, kosinus, tangen, dan kebalikannya dari panjang sisi segitiga siku-siku.",
    konsep=[
        "Pada segitiga siku-siku, dilihat dari sudut lancip " + th + ": sisi di hadapan " + th + " disebut <b>sisi depan</b> (de), sisi yang mengapit " + th + " selain sisi miring disebut <b>sisi samping</b> (sa), dan sisi di hadapan sudut siku-siku disebut <b>sisi miring</b> (mi).",
        "Segitiga siku-siku dengan sudut " + th + " yang sama sebangun, sehingga perbandingan sisinya tetap. Perbandingan itu diberi nama <b>sinus</b>, <b>kosinus</b>, dan <b>tangen</b>; nilainya hanya bergantung pada besar sudut, bukan pada ukuran segitiga.",
        "Kebalikannya: <b>kosekan</b> (csc), <b>sekan</b> (sec), dan <b>kotangen</b> (cot).",
    ],
    rumus=["sin " + th + " = " + fr("de", "mi") + "; cos " + th + " = " + fr("sa", "mi") + "; tan " + th + " = " + fr("de", "sa"),
           "csc " + th + " = " + fr(1, "sin " + th) + "; sec " + th + " = " + fr(1, "cos " + th) + "; cot " + th + " = " + fr(1, "tan " + th)],
    contoh=[
        ("Tiga perbandingan dari sisi", "Segitiga ABC siku-siku di B dengan AB = 8 dan BC = 6. Tentukan sin A, cos A, dan tan A.", F11,
         ["AC = √(64 + 36) = 10.", "Dari sudut A: de = BC = 6, sa = AB = 8, mi = AC = 10.", "sin A = 6/10 = ⅗; cos A = 8/10 = ⅘; tan A = 6/8 = ¾."], "sin A = ⅗; cos A = ⅘; tan A = ¾"),
        ("Dari satu perbandingan ke yang lain", "Diketahui sin " + th + " = " + fr(5, 13) + " dan " + th + " lancip. Tentukan cos " + th + " dan tan " + th + ".", None,
         ["Ambil de = 5, mi = 13.", "sa = √(169 − 25) = 12.", "cos " + th + " = 12/13; tan " + th + " = 5/12."], "cos " + th + " = " + fr(12, 13) + "; tan " + th + " = " + fr(5, 12)),
    ],
    bertahap=dict(
        soal="Segitiga PQR siku-siku di Q dengan PQ = 7 dan PR = 25. Tentukan QR, sin P, cos P, dan tan P.",
        langkah=["QR = √(25² − 7²) = √____ = ____.", "Dari sudut P: de = ____, sa = ____, mi = 25.", "sin P = ____; cos P = ____; tan P = ____."],
        cek="Untuk sudut P, sisi depannya QR karena",
        opsi=["(a) QR berhadapan dengan sudut P", "(b) QR adalah sisi terpanjang"],
        kunci="√576 = 24; de = QR = 24, sa = PQ = 7; sin P = 24/25, cos P = 7/25, tan P = 24/7. Alasan: (a).",
    ),
    jebakan=["Sisi depan dan sisi samping bergantung pada sudut yang ditinjau: sisi depan A adalah sisi samping C.", "Untuk sudut lancip, sin dan cos selalu di antara 0 dan 1 karena sisi miring paling panjang.", "sin " + th + " adalah satu lambang, bukan sin dikali " + th + "."],
    latihan=[
        Q(1, "Pada segitiga siku-siku, sisi depan " + th + " = 3, sisi samping = 4, sisi miring = 5. Tentukan sin " + th + ".", "⅗", "de/mi."),
        Q(1, "Dari soal 1.1, tentukan tan " + th + ".", "¾", "de/sa."),
        Q(1, "Jika cos " + th + " = 0,8, tentukan sec " + th + ".", "1,25", "1 : 0,8."),
        Q(1, "Segitiga ABC siku-siku di C dengan AC = 12 dan BC = 5. Hitung AB.", "13", "√(144 + 25)."),
        Q(1, "Segitiga ABC siku-siku di C dengan AC = 12, BC = 5, dan AB = 13. Tentukan sin A dan cos A.", fr(5, 13) + " dan " + fr(12, 13), "Sisi depan A adalah BC."),
        Q(2, "Diketahui tan " + th + " = " + fr(8, 15) + " dan " + th + " lancip. Tentukan sin " + th + " dan cos " + th + ".", fr(8, 17) + " dan " + fr(15, 17), "mi = √(64 + 225) = 17."),
        Q(2, "Segitiga ABC siku-siku di B dengan AB = 6 dan BC = 8. Tentukan sin C dan cos C.", "⅗ dan ⅘", "AC = 10; dari C: de = AB = 6, sa = BC = 8."),
        Q(2, "Jika sin " + th + " = 0,6 dan " + th + " lancip, hitung cos " + th + " dan tan " + th + ".", "0,8 dan 0,75", "Segitiga 3-4-5."),
        Q(2, "Sisi miring segitiga siku-siku 20 cm dan sin " + th + " = 0,6. Hitung sisi depan dan sisi samping " + th + ".", "12 cm dan 16 cm", "de = 20 · 0,6; sa = √(400 − 144)."),
        Q(3, "Pada segitiga ABC siku-siku di B, tunjukkan bahwa sin A = cos C.", "sin A = BC/AC = cos C", "Sisi depan A sama dengan sisi samping C; karena A + C = 90°, sin A = cos (90° − A)."),
        Q(3, "Segitiga ABC siku-siku di B dengan AB = 2√3 dan BC = 2. Hitung AC dan tan A.", "AC = 4; tan A = ⅓√3", "√(12 + 4) = 4; tan A = 2/(2√3). (Di Subbab 2 kamu akan tahu A = 30°.)"),
        Q(3, "Tangga 5 m bersandar pada dinding; kakinya 3 m dari dinding. Sudut antara tangga dan lantai " + th + ". Tentukan sin " + th + ", cos " + th + ", dan tan " + th + ".", "⅘; ⅗; " + fr(4, 3), "Tinggi ujung tangga √(25 − 9) = 4 m."),
    ],
))

# ================================================================== Subbab 2
F21a = poly([(0, 0), (1, 0), (1, 1)], ("", "", ""), [(0, 1, "1", INK), (1, 2, "1", INK), (0, 2, "√2", INK)], [((0, 0), (1, 0), (1, 1), "45°")], right=1, w=150, h=120)
F21b = poly([(0, 0), (math.sqrt(3), 0), (math.sqrt(3), 1)], ("", "", ""), [(0, 1, "√3", INK), (1, 2, "1", INK), (0, 2, "2", INK)],
            [((0, 0), (math.sqrt(3), 0), (math.sqrt(3), 1), "30°"), ((math.sqrt(3), 1), (0, 0), (math.sqrt(3), 0), "60°")], right=1, w=170, h=120)
F22 = segi(6 * math.sqrt(3), 6, sa="?", de="?", mi="12 cm", angle="30°", names=("", "", ""))
SUB.append(dict(
    title="Nilai Perbandingan Trigonometri Sudut Istimewa",
    tujuan="Menurunkan dan memakai nilai sin, cos, dan tan untuk 0°, 30°, 45°, 60°, dan 90°.",
    konsep=[
        "Segitiga siku-siku sama kaki dengan sisi tegak 1 mempunyai sisi miring √2 dan dua sudut 45°. Dari sini sin 45° = cos 45° = " + fr(1, "√2") + " = ½√2 dan tan 45° = 1.",
        "Segitiga sama sisi bersisi 2 dibelah dua oleh garis tingginya: diperoleh segitiga siku-siku dengan sisi 1, √3, dan 2 serta sudut 30° dan 60°.",
        "Untuk 0° dan 90° bayangkan sudut yang makin kecil atau makin mendekati siku-siku: sin 0° = 0, cos 0° = 1, sin 90° = 1, cos 90° = 0. tan 90° <b>tidak terdefinisi</b>.",
        '<div class="two"><div>' + F21a + "</div><div>" + F21b + "</div></div>",
    ],
    rumus=["sin 30° = ½; cos 30° = ½√3; tan 30° = ⅓√3", "sin 45° = cos 45° = ½√2; tan 45° = 1", "sin 60° = ½√3; cos 60° = ½; tan 60° = √3",
           "sin 0° = 0, cos 0° = 1, tan 0° = 0; sin 90° = 1, cos 90° = 0"],
    contoh=[
        ("Menghitung nilai bentuk", "Hitung sin 30° + cos 60° − tan 45°.", None, ["½ + ½ − 1."], "0"),
        ("Sisi dari sudut istimewa", "Sebuah segitiga siku-siku mempunyai sudut 30° dan sisi miring 12 cm. Tentukan sisi depan dan sisi samping sudut 30°.", F22,
         ["de = 12 · sin 30° = 12 · ½ = 6 cm.", "sa = 12 · cos 30° = 12 · ½√3 = 6√3 cm."], "6 cm dan 6√3 cm"),
    ],
    bertahap=dict(
        soal="Hitung 2 sin 45° · cos 45° + tan² 60°.",
        langkah=["2 · (½√2) · (½√2) = 2 · ____ = ____.", "tan² 60° = (√3)² = ____.", "Jumlahnya ____."],
        cek="tan² 60° berarti",
        opsi=["(a) (tan 60°)²", "(b) tan (60°²)"],
        kunci="2 · ½ = 1; 3; 4. Alasan: (a).",
    ),
    jebakan=["sin 30° + sin 30° ≠ sin 60°: perbandingan trigonometri tidak dapat dijumlahkan seperti sudutnya.", "tan 90° tidak terdefinisi (sisi samping 0), bukan 0 atau tak hingga.", "½√3 berarti setengah dikali √3, bukan √(3/2)."],
    latihan=[
        Q(1, "Tuliskan nilai sin 60°.", "½√3", "Dari segitiga 1-√3-2."),
        Q(1, "Hitung sin 45° · cos 45°.", "½", "(½√2)²."),
        Q(1, "Hitung tan 30° · tan 60°.", "1", "⅓√3 · √3."),
        Q(1, "Hitung cos 0° + sin 90°.", "2", "1 + 1."),
        Q(1, "Hitung 4 sin 30° − tan 45°.", "1", "2 − 1."),
        Q(2, "Hitung sin² 60° + cos² 60°.", "1", "¾ + ¼."),
        Q(2, "Tentukan " + th + " lancip yang memenuhi 2 cos " + th + " = √3.", "30°", "cos " + th + " = ½√3."),
        Q(2, "Segitiga siku-siku mempunyai sudut 60° dengan sisi samping sudut itu 5 cm. Hitung sisi miring dan sisi depannya.", "10 cm dan 5√3 cm", "mi = 5 : cos 60°; de = 5 · tan 60°."),
        Q(2, "Hitung (sin 30° + cos 30°)².", "1 + ½√3", "¼ + 2 · ½ · ½√3 + ¾."),
        Q(3, "Tentukan " + th + " (0° ≤ " + th + " ≤ 90°) yang memenuhi tan " + th + " = 3 tan 30°.", "60°", "3 · ⅓√3 = √3."),
        Q(3, "Pada persegi panjang ABCD, AB = 6√3 cm dan diagonal AC membentuk sudut 30° dengan AB. Hitung BC dan AC.", "BC = 6 cm; AC = 12 cm", "BC = AB tan 30°; AC = AB : cos 30°."),
        Q(3, "Tunjukkan bahwa sin 60° = 2 sin 30° cos 30°, tetapi sin 60° ≠ 2 sin 30°.", "½√3 = 2 · ½ · ½√3; 2 sin 30° = 1 ≠ ½√3", "Sinus sudut ganda bukan dua kali sinusnya."),
    ],
))

# ================================================================== Subbab 3
F31 = poly([(0, 0), (20, 0), (20, 20 * math.sqrt(3))], ("Pengamat", "", "Puncak"), [(0, 1, "20 m", INK), (1, 2, "h", RED)], [((0, 0), (20, 0), (20, 20 * math.sqrt(3)), "60°")], right=1, w=200, h=170)
F32 = poly([(0, 30), (0, 0), (30 * math.sqrt(3), 0)], ("Puncak", "", "Kapal"), [(0, 1, "30 m", INK), (1, 2, "d", RED)],
           [((0, 30), (30 * math.sqrt(3), 30), (30 * math.sqrt(3), 0), "30°")], right=1, dashed=[(0, 30, 30 * math.sqrt(3), 30)], w=240, h=130)
SUB.append(dict(
    title="Sudut Elevasi dan Depresi: Tinggi dan Jarak",
    tujuan="Memilih perbandingan trigonometri yang tepat untuk mencari sisi segitiga siku-siku, termasuk soal sudut elevasi dan depresi.",
    konsep=[
        "Untuk mencari sebuah sisi, pilih perbandingan yang memuat <b>sisi yang diketahui</b> dan <b>sisi yang dicari</b>, lalu selesaikan persamaannya.",
        "<b>Sudut elevasi</b> adalah sudut dari garis mendatar <b>ke atas</b> menuju benda. <b>Sudut depresi</b> adalah sudut dari garis mendatar <b>ke bawah</b> menuju benda.",
        "Sudut elevasi dari A ke B sama dengan sudut depresi dari B ke A, karena keduanya sudut dalam berseberangan dari dua garis mendatar yang sejajar. Jika tinggi mata pengamat diketahui, tambahkan pada hasilnya.",
    ],
    rumus=["de = mi · sin " + th + "; sa = mi · cos " + th + "; de = sa · tan " + th, "tinggi benda = jarak mendatar · tan (sudut elevasi) + tinggi mata"],
    contoh=[
        ("Sudut elevasi", "Dari titik yang berjarak 20 m dari kaki menara, sudut elevasi puncak menara 60°. Tentukan tinggi menara (tinggi pengamat diabaikan).", F31,
         ["tan 60° = h/20.", "h = 20 · √3 = 20√3 ≈ 34,6 m."], "20√3 m ≈ 34,6 m"),
        ("Sudut depresi", "Dari puncak mercusuar setinggi 30 m, sudut depresi ke sebuah kapal 30°. Berapa jarak kapal ke kaki mercusuar?", F32,
         ["Sudut depresi 30° = sudut elevasi dari kapal ke puncak.", "tan 30° = 30/d, jadi d = 30 : ⅓√3 = 30√3 ≈ 52 m."], "30√3 m ≈ 52 m"),
    ],
    bertahap=dict(
        soal="Panjang benang layang-layang 40 m dan benang membentuk sudut 37° dengan garis mendatar (sin 37° ≈ 0,6). Tangan Dina 1,5 m di atas tanah. Berapa tinggi layang-layang dari tanah? (Anggap benang lurus.)",
        langkah=["Tinggi di atas tangan = 40 · sin 37° = ____ m.", "Tinggi dari tanah = ____ + 1,5 = ____ m."],
        cek="Tinggi tangan ditambahkan karena",
        opsi=["(a) sudut diukur dari garis mendatar setinggi tangan", "(b) benang tidak lurus"],
        kunci="24; 25,5 m. Alasan: (a).",
    ),
    jebakan=["Sudut depresi diukur dari garis mendatar, bukan dari tiang tegak.", "Jangan lupa menambahkan tinggi mata pengamat bila diketahui.", "Gunakan sin bila sisi miring terlibat dengan sisi depan; tan bila hanya sisi depan dan samping."],
    latihan=[
        Q(1, "Sisi miring segitiga siku-siku 10 dan salah satu sudutnya 30°. Hitung sisi depan sudut itu.", "5", "10 · ½."),
        Q(1, "Sisi samping sudut 45° pada segitiga siku-siku adalah 7. Hitung sisi depannya.", "7", "7 · tan 45°."),
        Q(1, "Sisi miring 50 dan sudut 37° (cos 37° ≈ 0,8). Hitung sisi samping sudut itu.", "40", "50 · 0,8."),
        Q(1, "Pohon diamati dari jarak 12 m dengan sudut elevasi 45°. Berapa tinggi pohon (tinggi pengamat diabaikan)?", "12 m", "12 · tan 45°."),
        Q(1, "Jelaskan arti sudut depresi.", "sudut dari garis mendatar ke bawah menuju benda", "Diukur dari garis mendatar."),
        Q(2, "Tangga 6 m bersandar dan membentuk sudut 60° dengan lantai. Berapa tinggi ujung atas tangga?", "3√3 m ≈ 5,2 m", "6 · sin 60°."),
        Q(2, "Siswa dengan tinggi mata 1,5 m melihat puncak tiang bendera dengan sudut elevasi 37° dari jarak 16 m (tan 37° ≈ 0,75). Berapa tinggi tiang?", "13,5 m", "16 · 0,75 + 1,5."),
        Q(2, "Dari atap gedung setinggi 45 m, sudut depresi ke sebuah mobil 53° (tan 53° ≈ " + fr(4, 3) + "). Berapa jarak mobil ke gedung?", "33,75 m", "45 : " + fr(4, 3) + "."),
        Q(2, "Pesawat lepas landas dengan sudut 30° terhadap landasan dan terbang lurus sejauh 2 km. Berapa ketinggiannya?", "1 km", "2 · sin 30°."),
        Q(3, "Pengamat di A melihat puncak menara dengan sudut elevasi 30°. Setelah berjalan 20 m mendekati menara ke titik B, sudut elevasinya 60°. Hitung tinggi menara (tinggi pengamat diabaikan).", "10√3 m ≈ 17,3 m", "h/tan 30° − h/tan 60° = 20 → h√3 − h/√3 = 20."),
        Q(3, "Dari puncak menara setinggi 40 m, sudut depresi ke sebuah perahu berubah dari 30° menjadi 45° saat perahu mendekat. Berapa jarak yang ditempuh perahu?", "40(√3 − 1) m ≈ 29,3 m", "40√3 − 40."),
        Q(3, "Jalan menanjak dengan kemiringan 8%: naik 8 m untuk setiap 100 m mendatar. Tentukan tan sudut kemiringannya dan panjang jalan miring untuk 100 m mendatar (satu desimal).", "0,08; ≈ 100,3 m", "√(100² + 8²) = √10.064."),
    ],
))

# ================================================================== Subbab 4
F41 = plane((-6, 6, 1), (-6, 6, 1), curves=circle(5) + [(lambda x: math.sqrt(max(1.44 - x * x, 0)), -0.72, 1.2, RED, "")], arrows=[(0, 0, -3, 4, BLUE, "")], points=[(-3, 4, "P(−3, 4)")], segs=[(-3, 4, -3, 0, RED, True)],
            labels=[(-1.9, 2.5, "r = 5", BLUE), (1.2, 1.4, "θ", RED)], width=230, height=210, ticks_every=2)
F42 = plane((-4, 4, 1), (-4, 4, 1), curves=circle(3), labels=[(2, 2.2, "I: semua +", GREEN), (-2.2, 2.2, "II: sin +", GREEN), (-2.2, -2.4, "III: tan +", GREEN), (2.1, -2.4, "IV: cos +", GREEN)],
            width=230, height=210, ticks_every=4)
SUB.append(dict(
    title="Sudut di Semua Kuadran dan Sudut Berelasi",
    tujuan="Menentukan nilai perbandingan trigonometri sudut 0°–360° dari koordinat titik dan dari sudut berelasi.",
    konsep=[
        "Sudut " + th + " diukur dari sumbu x positif berlawanan arah jarum jam. Jika P(x, y) terletak pada kaki sudut dan r = √(x² + y²), maka sin " + th + " = y/r, cos " + th + " = x/r, dan tan " + th + " = y/x. Untuk sudut lancip, definisi ini sama dengan de/mi dan sa/mi.",
        "Karena r selalu positif, tanda sin mengikuti y dan tanda cos mengikuti x. Kuadran I: semua positif; II: hanya sin; III: hanya tan; IV: hanya cos.",
        "Nilai mutlaknya sama dengan nilai sudut lancip acuan. Contoh: 150° = 180° − 30°, jadi sin 150° = sin 30° = ½ (positif di kuadran II).",
    ],
    rumus=["sin " + th + " = y/r; cos " + th + " = x/r; tan " + th + " = y/x", "sin (180° − " + th + ") = sin " + th + "; cos (180° − " + th + ") = −cos " + th,
           "sin (180° + " + th + ") = −sin " + th + "; cos (180° + " + th + ") = −cos " + th, "sin (360° − " + th + ") = −sin " + th + "; cos (360° − " + th + ") = cos " + th,
           "sin (90° − " + th + ") = cos " + th],
    contoh=[
        ("Dari koordinat titik", "Titik P(−3, 4) terletak pada kaki sudut " + th + ". Tentukan sin " + th + ", cos " + th + ", dan tan " + th + ".", F41,
         ["r = √(9 + 16) = 5.", "sin " + th + " = 4/5; cos " + th + " = −3/5; tan " + th + " = 4/(−3)."], "⅘; −⅗; −" + fr(4, 3)),
        ("Sudut berelasi", "Hitung sin 150°, cos 240°, dan tan 315°.", F42,
         ["150° = 180° − 30° (kuadran II, sin +): sin 150° = ½.", "240° = 180° + 60° (kuadran III, cos −): cos 240° = −½.", "315° = 360° − 45° (kuadran IV, tan −): tan 315° = −1."], "½; −½; −1"),
    ],
    bertahap=dict(
        soal="Hitung cos 210° + sin 330°.",
        langkah=["210° = 180° + ____°, kuadran ____, jadi cos 210° = ____.", "330° = 360° − ____°, kuadran ____, jadi sin 330° = ____.", "Jumlahnya ____."],
        cek="cos 210° negatif karena",
        opsi=["(a) 210° di kuadran III, tempat x negatif", "(b) setiap sudut di atas 180° mempunyai cos negatif"],
        kunci="30°, III, −½√3; 30°, IV, −½; −½√3 − ½ = −½(√3 + 1). Alasan: (a) (300° di atas 180° tetapi cos 300° positif).",
    ),
    jebakan=["Tanda ditentukan kuadran; besar nilainya ditentukan sudut acuan.", "cos (180° − " + th + ") = −cos " + th + ", bukan cos " + th + ".", "tan 90° dan tan 270° tidak terdefinisi."],
    latihan=[
        Q(1, "Sudut 200° berada di kuadran berapa?", "III", "180° < 200° < 270°."),
        Q(1, "Apakah sin 120° positif atau negatif?", "positif", "Kuadran II."),
        Q(1, "Tentukan sin 180°.", "0", "Titik (−1, 0)."),
        Q(1, "Tentukan cos 300°.", "½", "cos (360° − 60°) = cos 60°."),
        Q(1, "Titik (5, 12) terletak pada kaki sudut " + th + ". Tentukan sin " + th + ".", fr(12, 13), "r = 13."),
        Q(2, "Hitung sin 135° + cos 135°.", "0", "½√2 + (−½√2)."),
        Q(2, "Titik P(−8, −6) terletak pada kaki sudut " + th + ". Tentukan sin " + th + ", cos " + th + ", dan tan " + th + ".", "−⅗; −⅘; ¾", "r = 10."),
        Q(2, "Hitung tan 120° · tan 240°.", "−3", "(−√3) · √3."),
        Q(2, "Diketahui sin " + th + " = ⅗ dan 90° &lt; " + th + " &lt; 180°. Tentukan cos " + th + " dan tan " + th + ".", "−⅘ dan −¾", "Kuadran II: x negatif."),
        Q(3, "Tentukan semua " + th + " (0° ≤ " + th + " ≤ 360°) yang memenuhi sin " + th + " = ½.", "30° dan 150°", "sin positif di kuadran I dan II."),
        Q(3, "Tentukan semua " + th + " (0° ≤ " + th + " ≤ 360°) yang memenuhi cos " + th + " = −½√2.", "135° dan 225°", "cos negatif di kuadran II dan III; sudut acuan 45°."),
        Q(3, "Sederhanakan sin (180° − " + th + ") + cos (90° − " + th + ") − 2 sin (360° − " + th + ").", "4 sin " + th, "sin " + th + " + sin " + th + " + 2 sin " + th + "."),
    ],
))

# ================================================================== Subbab 5
F52 = poly([(0, 0), (8, 0), (5 * cos(30), 5 * sin(30))], ("A", "B", "C"), [(0, 1, "8 cm", INK), (0, 2, "5 cm", INK)], [((0, 0), (8, 0), (5 * cos(30), 5 * sin(30)), "30°")],
           dashed=[(5 * cos(30), 5 * sin(30), 5 * cos(30), 0)], w=220, h=120)
SUB.append(dict(
    title="Identitas Dasar dan Luas Segitiga",
    tujuan="Memakai identitas sin² + cos² = 1 dan tan = sin/cos, serta menghitung luas segitiga dari dua sisi dan sudut apitnya.",
    konsep=[
        "Dari x² + y² = r², bagi kedua ruas dengan r²: (x/r)² + (y/r)² = 1, sehingga <b>sin² " + th + " + cos² " + th + " = 1</b> untuk setiap sudut. Dari y/x = (y/r) : (x/r) diperoleh <b>tan " + th + " = sin " + th + "/cos " + th + "</b>.",
        "Identitas dipakai untuk mencari nilai yang lain dari satu nilai yang diketahui (tanda dari kuadran) dan untuk menyederhanakan bentuk.",
        "Pada segitiga ABC dengan sisi b dan c yang mengapit sudut A, tinggi dari C ke AB adalah b sin A. Jadi <b>L = ½ bc sin A</b>.",
    ],
    rumus=["sin² " + th + " + cos² " + th + " = 1", "tan " + th + " = " + fr("sin " + th, "cos " + th), "1 + tan² " + th + " = sec² " + th, "L = ½ ab sin C (a dan b mengapit sudut C)"],
    contoh=[
        ("Menyederhanakan bentuk", "Sederhanakan (1 − sin² " + th + ") · tan " + th + ".", None,
         ["1 − sin² " + th + " = cos² " + th + ".", "cos² " + th + " · " + fr("sin " + th, "cos " + th) + " = sin " + th + " cos " + th + "."], "sin " + th + " cos " + th),
        ("Luas segitiga", "Segitiga ABC dengan AB = 8 cm, AC = 5 cm, dan sudut A = 30°. Hitung luasnya.", F52,
         ["Tinggi dari C = 5 sin 30° = 2,5 cm.", "L = ½ · 8 · 5 · sin 30° = 10 cm²."], "10 cm²"),
    ],
    bertahap=dict(
        soal="Dua sisi segitiga 6 cm dan 10 cm mengapit sudut 120°. Hitung luasnya.",
        langkah=["sin 120° = sin (180° − ____°) = ____.", "L = ½ · 6 · 10 · ____ = ____ cm²."],
        cek="sin 120° positif karena",
        opsi=["(a) 120° di kuadran II, tempat sin positif", "(b) luas tidak boleh negatif"],
        kunci="60°; ½√3; 15√3 cm². Alasan: (a).",
    ),
    jebakan=["sin² " + th + " berarti (sin " + th + ")², bukan sin (" + th + "²).", "Sudut pada rumus luas harus sudut yang diapit kedua sisi.", "sin " + th + " + cos " + th + " tidak selalu 1; yang selalu 1 adalah jumlah kuadratnya."],
    latihan=[
        Q(1, "Jika sin " + th + " = 0,6, berapa sin² " + th + " + cos² " + th + "?", "1", "Identitas."),
        Q(1, "Sederhanakan " + fr("sin " + th, "cos " + th) + ".", "tan " + th, "Identitas."),
        Q(1, "Sederhanakan 1 − cos² " + th + ".", "sin² " + th, "Identitas."),
        Q(1, "Hitung luas segitiga dengan dua sisi 4 cm dan 6 cm yang mengapit sudut 90°.", "12 cm²", "sin 90° = 1."),
        Q(1, "Hitung luas segitiga dengan dua sisi 10 cm dan 10 cm yang mengapit sudut 30°.", "25 cm²", "½ · 100 · ½."),
        Q(2, "Diketahui cos " + th + " = " + fr(5, 13) + " dan " + th + " di kuadran IV. Tentukan sin " + th + " dan tan " + th + ".", "−" + fr(12, 13) + " dan −" + fr(12, 5), "sin² " + th + " = 144/169; kuadran IV: sin negatif."),
        Q(2, "Sederhanakan cos " + th + " · tan " + th + ".", "sin " + th, "cos " + th + " · sin " + th + "/cos " + th + "."),
        Q(2, "Hitung luas segitiga dengan dua sisi 8 cm dan 12 cm yang mengapit sudut 45°.", "24√2 cm²", "½ · 96 · ½√2."),
        Q(2, "Buktikan (1 + tan² " + th + ") cos² " + th + " = 1.", "cos² " + th + " + sin² " + th + " = 1", "Kalikan masuk: cos² " + th + " + tan² " + th + " cos² " + th + "."),
        Q(3, "Luas segitiga 18 cm² dan dua sisinya 6 cm dan 12 cm. Tentukan sudut lancip yang diapit kedua sisi itu.", "30°", "½ · 72 · sin C = 18 → sin C = ½."),
        Q(3, "Jika sin " + th + " + cos " + th + " = 1,4, hitung sin " + th + " cos " + th + ".", "0,48", "Kuadratkan: 1 + 2 sin " + th + " cos " + th + " = 1,96."),
        Q(3, "Segi enam beraturan bersisi 4 cm tersusun dari enam segitiga sama sisi. Hitung luasnya.", "24√3 cm²", "6 · ½ · 4 · 4 · sin 60°."),
    ],
))

CAMPURAN = [
    Q(1, "Hitung cos 60° + sin 30°.", "1", "½ + ½."),
    Q(1, "Segitiga siku-siku bersisi 9, 12, dan 15. Tentukan sinus sudut yang berhadapan dengan sisi 9.", "⅗", "9/15."),
    Q(1, "Tentukan sin 240°.", "−½√3", "Kuadran III; sudut acuan 60°."),
    Q(1, "Sederhanakan sin² " + th + " + cos² " + th + " + tan " + th + " · cot " + th + ".", "2", "1 + 1."),
    Q(2, "Diketahui tan " + th + " = ¾ dan " + th + " di kuadran III. Tentukan sin " + th + " dan cos " + th + ".", "−⅗ dan −⅘", "x dan y negatif, r = 5."),
    Q(2, "Dari jarak 30 m, sudut elevasi puncak gedung 30°. Berapa tinggi gedung (tinggi pengamat diabaikan)?", "10√3 m ≈ 17,3 m", "30 · ⅓√3."),
    Q(2, "Hitung luas segitiga dengan dua sisi 7 cm dan 8 cm yang mengapit sudut 150°.", "14 cm²", "½ · 56 · ½."),
    Q(2, "Tentukan semua " + th + " (0° ≤ " + th + " ≤ 360°) yang memenuhi tan " + th + " = −1.", "135° dan 315°", "tan negatif di kuadran II dan IV."),
    Q(2, "Tangga 4 m membentuk sudut 60° dengan lantai. Berapa jarak kaki tangga ke dinding?", "2 m", "4 · cos 60°."),
    Q(3, "Buktikan (sin " + th + " + cos " + th + ")² + (sin " + th + " − cos " + th + ")² = 2.", "2(sin² " + th + " + cos² " + th + ") = 2", "Suku 2 sin " + th + " cos " + th + " saling menghapus."),
]

FK = poly([(0, 0), (4, 0), (4, 3)], ("A", "C", "B"), [(0, 1, "b", INK), (1, 2, "a", INK), (0, 2, "c", INK)], [((0, 0), (4, 0), (4, 3), "θ")], right=1, w=200, h=130)
TKA = [
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Nilai sin 150° + cos 300° − tan 225° adalah ....",
         opsi=["0", "2", "1", "−1", "½"], kunci=0, bahas="½ + ½ − 1 = 0 (tan 225° = tan 45° = 1, positif di kuadran III).",
         salah="B: tan 225° dianggap −1. C: tan 225° terlewat. D: cos 300° diberi tanda negatif. E: tidak sesuai."),
    dict(tipe="MAT-UKUR", lv=2, fmt="pg", soal="Seorang siswa dengan tinggi mata 1,6 m berdiri 24 m dari sebuah gedung. Sudut elevasi puncak gedung dari matanya 37° (sin 37° ≈ 0,6; tan 37° ≈ 0,75). Tinggi gedung adalah ....",
         opsi=["19,6 m", "18 m", "32 m", "16,4 m", "16 m"], kunci=0, bahas="24 · 0,75 + 1,6 = 19,6 m.",
         salah="B: tinggi mata tidak ditambahkan. C: jarak dibagi tan 37°. D: tinggi mata dikurangkan. E: memakai sin 37°."),
    dict(tipe="MAT-PARAM", lv=2, fmt="pg", soal="Diketahui cos " + th + " = k dengan " + th + " di kuadran II. Nilai tan " + th + " dinyatakan dalam k adalah ....",
         opsi=[fr("√(1 − k²)", "k"), "−" + fr("√(1 − k²)", "k"), fr("k", "√(1 − k²)"), fr("√(1 + k²)", "k"), fr("1 − k²", "k")], kunci=0,
         bahas="sin " + th + " = √(1 − k²) (positif di kuadran II); tan " + th + " = sin/cos. Karena k negatif, hasilnya otomatis negatif.",
         salah="B: tanda negatif ditambahkan padahal k sudah negatif. C: kebalikannya (cot). D: memakai 1 + k². E: lupa akar."),
    dict(tipe="MAT-KENAL", lv=1, fmt="pgk", soal="Perhatikan segitiga siku-siku ACB berikut (siku-siku di C).", fig=FK, soal2="Pernyataan yang tepat adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["sin " + th + " = " + fr("a", "c"), "cos " + th + " = " + fr("a", "c"), "tan " + th + " = " + fr("a", "b"), "sin B = " + fr("b", "c"), "a² + c² = b²"], kunci=[0, 2, 3],
         bahas="Dari " + th + ": de = a, sa = b, mi = c. Dari B: de = b.", salah="B: a sisi depan " + th + ", bukan sisi samping. E: sisi miringnya c, jadi a² + b² = c²."),
    dict(tipe="MAT-FUNGSI", lv=2, fmt="pg", soal="Tinggi sebuah kursi bianglala dari tanah dimodelkan oleh h(" + th + ") = 12 − 10 cos " + th + " (meter), dengan " + th + " besar sudut putaran roda sejak kursi berada di titik terendah. Tinggi kursi setelah roda berputar 120° adalah ....",
         opsi=["17 m", "7 m", "≈ 20,7 m", "2 m", "22 m"], kunci=0, bahas="cos 120° = −½, jadi h = 12 + 5 = 17 m.",
         salah="B: cos 120° diambil +½. C: memakai sin 120°. D: tinggi titik terendah (" + th + " = 0°). E: tinggi titik tertinggi (" + th + " = 180°)."),
    dict(tipe="MAT-PARAM", lv=2, fmt="bs", kolom=["Benar", "Salah"], soal="Segitiga ABC siku-siku di B dengan sin A = ⅗. Tentukan benar atau salah setiap pernyataan berikut.",
         opsi=["cos A = ⅘.", "tan C = " + fr(4, 3) + ".", "sin A = cos C.", "Jika AC = 15 cm, maka AB = 9 cm."], kunci=[True, True, True, False],
         bahas="Ambil BC = 3, AB = 4, AC = 5. tan C = AB/BC = 4/3. sin A = BC/AC = cos C. Jika AC = 15, AB = 12 dan BC = 9.", salah=""),
    dict(tipe="MAT-HITUNG", lv=2, fmt="pg", soal="Dua sisi sebuah segitiga 10 cm dan 12 cm mengapit sudut 135°. Luas segitiga itu adalah ....",
         opsi=["30√2 cm²", "60√2 cm²", "−30√2 cm²", "30 cm²", "30√3 cm²"], kunci=0, bahas="½ · 10 · 12 · sin 135° = 60 · ½√2.",
         salah="B: lupa ½. C: sin 135° diberi tanda negatif. D: sin 135° dianggap ½. E: memakai ½√3."),
    dict(tipe="MAT-KEPUTUSAN", lv=3, fmt="pg", soal="Sekolah akan membuat jalur landai (ramp) kursi roda menuju teras setinggi 0,6 m. Pengelola menetapkan sudut kemiringan ramp paling besar 6° (tan 6° ≈ 0,105). Tersedia lahan mendatar sepanjang 4 m, 5 m, 6 m, 7 m, atau 8 m. Lahan terpendek yang memenuhi syarat adalah ....",
         opsi=["6 m", "5 m", "4 m", "7 m", "8 m"], kunci=0, bahas="tan " + th + " = 0,6/panjang ≤ 0,105 → panjang ≥ 5,71 m. 5 m: 0,12 (terlalu curam); 6 m: 0,1.",
         salah="B, C: terlalu curam (tan 0,12 dan 0,15). D, E: memenuhi, tetapi bukan yang terpendek."),
    dict(tipe="MAT-NALAR", lv=3, fmt="pgk", soal="Diketahui " + th + " sudut tumpul (90° &lt; " + th + " &lt; 180°). Pernyataan yang pasti benar adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["sin " + th + " &gt; 0", "cos " + th + " &gt; 0", "tan " + th + " &lt; 0", "sin " + th + " + cos " + th + " &gt; 0", "sin (180° − " + th + ") = sin " + th], kunci=[0, 2, 4],
         bahas="Kuadran II: y positif, x negatif; sudut berelasi 180° − " + th + ".", salah="B: cos negatif di kuadran II. D: salah untuk " + th + " = 150°, karena ½ − ½√3 &lt; 0."),
    dict(tipe="MAT-UKUR", lv=2, fmt="pg", soal="Dari puncak bukit setinggi 60 m, sudut depresi ke dua rumah yang segaris dengan kaki bukit adalah 45° dan 30°. Jarak kedua rumah itu sekitar .... (√3 ≈ 1,73)",
         opsi=["44 m", "60 m", "104 m", "35 m", "25 m"], kunci=0, bahas="Jarak rumah dekat 60 m, rumah jauh 60√3 ≈ 104 m; selisihnya ≈ 44 m.",
         salah="B: jarak rumah yang dekat. C: jarak rumah yang jauh. D: memakai 60 tan 30°. E: 60 − 60 tan 30°."),
]
GRAPH_OPTS = {}

UJI_PG = [
    ("Nilai sin 30° adalah ....", ["½", "½√3", "½√2", "1", "√3"], 0, "Sudut istimewa.", "B: cos 30°. C: sin 45°. D: sin 90°. E: tan 60°."),
    ("Segitiga siku-siku bersisi 8, 15, dan 17. Kosinus sudut yang berhadapan dengan sisi 8 adalah ....", [fr(15, 17), fr(8, 17), fr(8, 15), fr(15, 8), fr(17, 15)], 0, "sa/mi.", "B: sinusnya. C: tangennya. D: kotangennya. E: sekannya."),
    ("Nilai tan 60° adalah ....", ["√3", "⅓√3", "1", "½√3", "½"], 0, "sin 60°/cos 60°.", "B: tan 30°. C: tan 45°. D: sin 60°. E: cos 60°."),
    ("Nilai 2 sin 45° cos 45° adalah ....", ["1", "½", "√2", "2", "½√2"], 0, "2 · ½.", "B: lupa dikali 2. C, D, E: tidak sesuai."),
    ("Diketahui sin " + th + " = " + fr(12, 13) + " dan " + th + " lancip. Nilai tan " + th + " adalah ....", [fr(12, 5), fr(5, 12), fr(5, 13), fr(13, 12), fr(12, 13)], 0, "sa = 5.", "B: cot. C: cos. D: csc. E: sin."),
    ("Tangga 8 m bersandar pada dinding dan membentuk sudut 60° dengan lantai. Tinggi ujung atas tangga adalah ....", ["4√3 m", "4 m", "8√3 m", "8 m", "16 m"], 0, "8 sin 60°.", "B: memakai cos 60°. C: memakai tan 60°. D, E: tidak sesuai."),
    ("Dari jarak 25 m, sudut elevasi puncak pohon 45°. Tinggi pohon (tinggi pengamat diabaikan) adalah ....", ["25 m", "12,5 m", "25√2 m", "50 m", "25√3 m"], 0, "25 tan 45°.", "B: memakai ½. C: sisi miring. D, E: tidak sesuai."),
    ("Nilai cos 120° adalah ....", ["−½", "½", "−½√3", "½√3", "−1"], 0, "−cos 60°.", "B: tanda kuadran II diabaikan. C: memakai sin 60°. D, E: tidak sesuai."),
    ("Sudut 250° terletak di kuadran ....", ["III", "II", "IV", "I", "tidak di kuadran mana pun"], 0, "180° < 250° < 270°.", "B, C, D, E: tidak sesuai."),
    ("Nilai tan 315° adalah ....", ["−1", "1", "−√3", "√3", "0"], 0, "Kuadran IV; −tan 45°.", "B: tanda diabaikan. C, D, E: tidak sesuai."),
    ("Titik P(−5, 12) terletak pada kaki sudut " + th + ". Nilai cos " + th + " adalah ....", ["−" + fr(5, 13), fr(5, 13), fr(12, 13), "−" + fr(12, 13), "−" + fr(5, 12)], 0, "x/r.", "B: tanda diabaikan. C: sin " + th + ". D: tidak sesuai. E: kebalikan tan " + th + "."),
    ("Nilai sin² 50° + cos² 50° adalah ....", ["1", "0", "2", "sin 100°", "cos 100°"], 0, "Identitas.", "B, C, D, E: tidak sesuai."),
    ("Luas segitiga dengan dua sisi 6 cm dan 8 cm yang mengapit sudut 30° adalah ....", ["12 cm²", "24 cm²", "48 cm²", "12√3 cm²", "6 cm²"], 0, "½ · 48 · ½.", "B: lupa ½ di depan. C: tanpa sin. D: memakai cos 30°. E: tidak sesuai."),
    ("Nilai " + th + " (0° ≤ " + th + " ≤ 360°) yang memenuhi cos " + th + " = ½ adalah ....", ["60° dan 300°", "60° dan 120°", "30° dan 330°", "60° dan 240°", "30° dan 150°"], 0, "cos positif di kuadran I dan IV.", "B: memakai pasangan sinus. C, E: memakai sin " + th + " = ½. D: kuadran III."),
    ("Bentuk sederhana sin " + th + " · cot " + th + " adalah ....", ["cos " + th, "sin " + th, "tan " + th, "1", fr("sin² " + th, "cos " + th)], 0, "sin · cos/sin.", "B, C, D: tidak sesuai. E: memakai tan, bukan cot."),
]
UJI_URAIAN = [
    ("Segitiga ABC siku-siku di B dengan AB = 15 dan AC = 17. Hitung BC, lalu tentukan keenam perbandingan trigonometri sudut A.", "BC = 8; sin A = 8/17, cos A = 15/17, tan A = 8/15, csc A = 17/8, sec A = 17/15, cot A = 15/8", "√(289 − 225) = 8."),
    ("Hitung sin 120° + cos 210° + tan 135°.", "−1", "½√3 − ½√3 − 1."),
    ("Dari jendela setinggi 12 m, sudut elevasi puncak gedung di seberang jalan 30° dan sudut depresi kaki gedung itu 45°. Hitung tinggi gedung.", "12 + 4√3 ≈ 18,9 m", "Jarak mendatar 12 m (depresi 45°); bagian atas 12 tan 30° = 4√3."),
    ("Diketahui cos " + th + " = −⅘ dan " + th + " di kuadran III. Tentukan sin " + th + ", tan " + th + ", dan sin² " + th + " + cos² " + th + ".", "−⅗; ¾; 1", "Kuadran III: sin negatif, tan positif."),
    ("Sebuah taman berbentuk segitiga dengan dua sisi 20 m dan 30 m yang mengapit sudut 150°. Hitung luas taman dan biaya menanam rumput bila biayanya Rp50.000 per m².", "150 m²; Rp7.500.000", "½ · 600 · ½; 150 · 50.000."),
]

META = dict(
    title="Modul Trigonometri", kick="Modul belajar Matematika · Fase E · Kelas X", big="Trigonometri",
    subtitle="Perbandingan trigonometri pada segitiga siku-siku, sudut istimewa, sudut elevasi dan depresi, sudut di semua kuadran, identitas dasar, serta luas segitiga",
    tka_mapel="TKA Matematika",
    kompetensi="Peserta didik dapat menentukan perbandingan trigonometri pada segitiga siku-siku dan pada sudut di semua kuadran, memakai nilai sudut istimewa dan identitas dasar, serta menyelesaikan masalah tinggi, jarak, dan luas, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Mengapa trigonometri?</h2><p>Tinggi gedung, lebar sungai, dan kemiringan ramp dapat dihitung tanpa diukur langsung: cukup satu jarak dan satu sudut. Trigonometri juga dipakai lagi di Fisika (komponen vektor dan gerak parabola).</p>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Gambarlah segitiganya</b> dan tandai sisi depan, samping, dan miring sebelum menghitung.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b>",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Sudut dalam derajat. de, sa, dan mi berarti sisi depan, samping, dan miring. ½√3 berarti setengah dikali √3. Bila soal memberi nilai pendekatan (misalnya sin 37° ≈ 0,6), pakai nilai itu. Desimal ditulis dengan koma.",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>segitiga siku-siku, sudut istimewa, kuadran, identitas, atau luas?</b>",
    tka_info=["Soal disusun meniru tipe soal Matematika pada Tes Kemampuan Akademik (TKA) SMA 2025, yang memakai perbandingan trigonometri untuk panjang dan sudut, serta fungsi trigonometri sebagai model.",
              "<b>Level 1–2</b> (MAT-KENAL, MAT-HITUNG, MAT-PARAM, MAT-FUNGSI, MAT-UKUR): mengenali, menghitung, bekerja dengan parameter, memakai fungsi, atau mengukur. <b>Level 3</b> (MAT-KEPUTUSAN, MAT-NALAR): memilih yang terbaik dengan batasan atau menalar apa yang pasti benar."],
    refleksi=["Bagaimana cara menentukan sisi depan dan sisi samping sebuah sudut?", "Mengapa cos 120° negatif tetapi sin 120° positif?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th>Segitiga siku-siku</th><td>sin = de/mi; cos = sa/mi; tan = de/sa; csc, sec, cot kebalikannya</td></tr>"
        "<tr><th>Sudut istimewa</th><td>30°: ½, ½√3, ⅓√3 · 45°: ½√2, ½√2, 1 · 60°: ½√3, ½, √3 (sin, cos, tan)</td></tr>"
        "<tr><th>Elevasi/depresi</th><td>diukur dari garis mendatar; tinggi = jarak · tan sudut + tinggi mata</td></tr>"
        "<tr><th>Semua kuadran</th><td>sin = y/r, cos = x/r, tan = y/x; tanda: I semua, II sin, III tan, IV cos</td></tr>"
        "<tr><th>Sudut berelasi</th><td>180° − " + th + ", 180° + " + th + ", 360° − " + th + ": nilai sudut acuan dengan tanda kuadran</td></tr>"
        "<tr><th>Identitas</th><td>sin² + cos² = 1; tan = sin/cos; 1 + tan² = sec²</td></tr>"
        "<tr><th>Luas segitiga</th><td>L = ½ ab sin C</td></tr></table>"
        '<div class="two"><div>' + segi(4, 3, sa="sa", de="de", mi="mi", names=("", "", "")) + "</div><div>" + F42 + "</div></div>"),
    jebakan5=["Sisi depan dan samping bergantung pada sudut yang ditinjau.", "sin 30° + sin 30° ≠ sin 60°.", "Sudut depresi diukur dari garis mendatar.",
              "Tanda dari kuadran, besar dari sudut acuan.", "Rumus luas memakai sudut yang diapit kedua sisi."],
    guru=["Materi mengikuti Kurikulum Merdeka Matematika SMA Fase E (bab Trigonometri pada buku kelas X): perbandingan trigonometri, sudut istimewa, dan penerapannya.",
          "Subbab 4 (sudut di semua kuadran) dan Subbab 5 (identitas dan luas ½ab sin C) dapat melampaui cakupan sebagian sekolah di kelas X; lewati bila belum diajarkan. Bagian lain tidak bergantung pada keduanya, kecuali beberapa soal campuran, TKA, dan uji yang memakai kuadran.",
          "Soal setara TKA meniru tipe soal TKA Matematika SMA 2025; soal ini buatan sendiri, bukan soal resmi. Batas 6° pada soal ramp adalah ketentuan dalam soal, bukan kutipan peraturan."],
)


def check():
    c = close
    r3, r2 = math.sqrt(3), math.sqrt(2)
    # prasyarat
    c(math.hypot(5, 12), 13); c(6 / r3, 2 * r3); c(math.sqrt(48), 4 * r3); c(math.hypot(4, 4), 4 * r2); c((3 / 5) ** 2 + (4 / 5) ** 2, 1); c(8 * 3 / 4, 6); c(math.hypot(-3, 4), 5)
    # subbab 1
    c(math.hypot(8, 6), 10); c(math.sqrt(169 - 25), 12); c(math.sqrt(625 - 49), 24); c(1 / 0.8, 1.25); c(math.hypot(12, 5), 13)
    c(math.hypot(8, 15), 17); c(math.hypot(6, 8), 10); c(20 * 0.6, 12); c(math.sqrt(400 - 144), 16); c(math.hypot(2 * r3, 2), 4); c(math.degrees(math.atan(2 / (2 * r3))), 30); c(math.sqrt(25 - 9), 4)
    # subbab 2
    c(sin(30) + cos(60) - tan(45), 0); c(12 * sin(30), 6); c(12 * cos(30), 6 * r3); c(2 * sin(45) * cos(45) + tan(60) ** 2, 4)
    c(sin(60), r3 / 2); c(sin(45) * cos(45), 0.5); c(tan(30) * tan(60), 1); c(cos(0) + sin(90), 2); c(4 * sin(30) - tan(45), 1); c(sin(60) ** 2 + cos(60) ** 2, 1)
    c(math.degrees(math.acos(r3 / 2)), 30); c(5 / cos(60), 10); c(5 * tan(60), 5 * r3); c((sin(30) + cos(30)) ** 2, 1 + r3 / 2); c(math.degrees(math.atan(3 * tan(30))), 60)
    c(6 * r3 * tan(30), 6); c(6 * r3 / cos(30), 12); c(sin(60), 2 * sin(30) * cos(30)); assert abs(sin(60) - 2 * sin(30)) > 0.1
    # subbab 3
    c(20 * tan(60), 20 * r3); c(30 / tan(30), 30 * r3); c(40 * 0.6 + 1.5, 25.5); c(10 * sin(30), 5); c(7 * tan(45), 7); c(50 * 0.8, 40); c(12 * tan(45), 12)
    c(6 * sin(60), 3 * r3); c(16 * 0.75 + 1.5, 13.5); c(45 / (4 / 3), 33.75); c(2 * sin(30), 1)
    h = 20 / (1 / tan(30) - 1 / tan(60)); c(h, 10 * r3); c(40 / tan(30) - 40 / tan(45), 40 * (r3 - 1)); c(math.hypot(100, 8), 100.3, 0.05)
    # subbab 4
    c(cos(210) + sin(330), -(r3 + 1) / 2); c(sin(150), 0.5); c(cos(240), -0.5); c(tan(315), -1)
    c(sin(180), 0); c(cos(300), 0.5); c(sin(135) + cos(135), 0); c(tan(120) * tan(240), -3); assert sin(120) > 0 and 180 < 200 < 270
    assert [d for d in range(361) if abs(sin(d) - 0.5) < 1e-9] == [30, 150]
    assert [d for d in range(361) if abs(cos(d) + r2 / 2) < 1e-9] == [135, 225]
    for t in (17, 40, 73):
        c(sin(180 - t) + cos(90 - t) - 2 * sin(360 - t), 4 * sin(t))
    # subbab 5
    c(0.5 * 8 * 5 * sin(30), 10); c(0.5 * 6 * 10 * sin(120), 15 * r3); c(0.5 * 4 * 6, 12); c(0.5 * 100 * sin(30), 25); c(0.5 * 8 * 12 * sin(45), 24 * r2)
    c(math.degrees(math.asin(18 / 36)), 30); c((1.4 ** 2 - 1) / 2, 0.48); c(6 * 0.5 * 16 * sin(60), 24 * r3)
    for t in (10, 100, 200, 300):
        c((1 - sin(t) ** 2) * tan(t), sin(t) * cos(t)); c((1 + tan(t) ** 2) * cos(t) ** 2, 1); c((sin(t) + cos(t)) ** 2 + (sin(t) - cos(t)) ** 2, 2)
    # campuran
    c(cos(60) + sin(30), 1); c(9 / 15, 0.6); c(sin(240), -r3 / 2); c(30 * tan(30), 10 * r3); c(0.5 * 56 * sin(150), 14); c(4 * cos(60), 2)
    assert [d for d in range(361) if d % 90 and abs(tan(d) + 1) < 1e-9] == [135, 315]
    t3 = 180 + math.degrees(math.atan(0.75)); c(sin(t3), -0.6); c(cos(t3), -0.8)
    # TKA
    c(sin(150) + cos(300) - tan(225), 0); c(24 * 0.75 + 1.6, 19.6)
    for k in (-0.3, -0.8):
        t = math.degrees(math.acos(k)); c(tan(t), math.sqrt(1 - k * k) / k)
    c(12 - 10 * cos(120), 17); c(0.5 * 120 * sin(135), 30 * r2)
    ok = [L for L in (4, 5, 6, 7, 8) if 0.6 / L <= 0.105]; assert min(ok) == 6
    assert 0.5 - r3 / 2 < 0; c(60 / tan(30) - 60 / tan(45), 43.9, 0.1); c(60 * tan(30), 34.6, 0.1); c(60 - 60 * tan(30), 25.4, 0.1)
    # uji
    c(math.sqrt(289 - 225), 8); c(sin(120) + cos(210) + tan(135), -1); c(12 + 12 * tan(30), 12 + 4 * r3); c(0.5 * 600 * sin(150), 150)
    c(8 * sin(60), 4 * r3); c(0.5 * 48 * sin(30), 12); c(tan(315), -1); c(cos(120), -0.5); c(2 * sin(45) * cos(45), 1)
    assert [d for d in range(361) if abs(cos(d) - 0.5) < 1e-9] == [60, 300]
    t4 = math.degrees(math.atan2(12, -5)); c(cos(t4), -5 / 13)
    return True
