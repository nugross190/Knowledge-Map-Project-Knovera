"""Content of the printable module "Gerak Parabola" (Fisika kelas X–XI).

Convention: x horizontal (forward positive), y up, g = 10 m/s², no air resistance unless stated.
Trajectories come from graphs.Shot, component graphs from graphs.Motion; every numeric answer is
re-derived in check().
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from graphs import Motion, Shot, TEMPLATES as TP, render  # noqa: E402
from kit import n, fr, Q, noisy, close  # noqa: E402

g = 10
BLUE, RED = "#1f3a68", "#c0502a"
S37, C37 = 0.6, 0.8
S53, C53 = 0.8, 0.6
R3 = math.sqrt(3)


def T(name, *shots, w=300, h=190, **kw):
    return render(TP[name], shots=shots, width=w, height=h, **kw)


def G(name, *motions, w=300, h=190, **kw):
    return render(TP[name], motions, width=w, height=h, **kw)


def comp_vt(vx, vy, t_end, **kw):
    """vx–t (red, constant) and vy–t (blue, slope −g) on one frame."""
    return render(TP["par-vt"], (Motion(0, vx, [(t_end, 0)], "vₓ", RED), Motion(0, vy, [(t_end, -g)], "v<tspan font-size='6' dy='2'>y</tspan>", BLUE)), width=kw.get("w", 300), height=kw.get("h", 190))


def t_land(y0, vy, y=0.0):
    a, b, c = -g / 2, vy, y0 - y
    return (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)


PRASYARAT = [
    ("P1", "Uraikan kecepatan 20 m/s yang membentuk sudut 37° terhadap horizontal (sin 37° = 0,6; cos 37° = 0,8).", "16 m/s mendatar; 12 m/s tegak", "20 · 0,8 dan 20 · 0,6."),
    ("P2", "Hitung 2 · sin 37° · cos 37°.", "0,96", "2 · 0,6 · 0,8."),
    ("P3", "Hitung √(12² + 5²).", "13", "√169."),
    ("P4", "Selesaikan 4t − 5t² = 0.", "t = 0 atau t = 0,8", "t(4 − 5t) = 0."),
    ("P5", "Jika tan θ = 3/4, berapa θ?", "θ ≈ 37°", "Segitiga 3-4-5."),
    ("P6", "Benda jatuh bebas dari 20 m (g = 10 m/s²). Berapa waktu jatuhnya?", "2 s", "√(40 : 10)."),
    ("P7", "Benda ber-GLB 15 m/s selama 2 s. Berapa jaraknya?", "30 m", "15 · 2."),
    ("P8", "Tuliskan nilai sin 30°, cos 30°, dan sin 60°.", "½; ½√3; ½√3", "√3 ≈ 1,73."),
]

INGAT = [
    ("A", "Komponen vektor", "P1, P3, P5", "Subbab 1–4",
     ["v<sub>x</sub> = v cos α, v<sub>y</sub> = v sin α (α dari horizontal).", "Besar dari komponen: v = √(v<sub>x</sub>² + v<sub>y</sub>²); arah tan θ = v<sub>y</sub>/v<sub>x</sub>. Lihat juga modul Vektor dan Gerak."]),
    ("B", "Trigonometri sudut istimewa", "P2, P8", "Subbab 3–4",
     ["37°/53°: sin 37° = cos 53° ≈ 0,6; cos 37° = sin 53° ≈ 0,8.", "30°/60°: sin 30° = cos 60° = ½; cos 30° = sin 60° = ½√3. 45°: sin = cos = ½√2.", "sin 2α = 2 sin α cos α."]),
    ("C", "GLB dan gerak vertikal", "P6, P7", "Semua subbab",
     ["GLB: x = v·t.", "Gerak vertikal: v = v₀ − gt; y = y₀ + v₀t − ½gt² (modul Gerak Vertikal)."]),
    ("D", "Persamaan kuadrat", "P4", "Subbab 3–5",
     ["Faktorkan atau pakai rumus abc. Untuk waktu mendarat, ambil akar positif yang lebih besar."]),
]

SUB = []

# ================================================================== Subbab 1: gabungan GLB dan GLBB
A_drop, B_throw = Shot(0, 0, y0=20, label="A", color=RED), Shot(10, 0, y0=20, label="B", color=BLUE)
SUB.append(dict(
    title="Gerak Dua Dimensi: Gabungan GLB dan GLBB",
    tujuan="Menjelaskan gerak parabola sebagai gabungan GLB mendatar dan gerak vertikal yang saling bebas, lalu menentukan posisi dan kecepatan dari komponennya.",
    konsep=[
        "Benda yang dilempar lalu hanya dipengaruhi gravitasi bergerak di bidang x–y. Geraknya dapat dipisah menjadi dua gerak yang <b>saling bebas</b>: arah mendatar (x) dan arah tegak (y).",
        "Arah <b>mendatar</b>: tidak ada percepatan, jadi GLB dengan v<sub>x</sub> tetap. Arah <b>tegak</b>: percepatan −g, jadi sama dengan gerak vertikal pada modul sebelumnya.",
        "Kedua gerak berbagi <b>waktu</b> yang sama. Posisi benda pada saat t adalah (x, y), dan kecepatannya adalah vektor (v<sub>x</sub>, v<sub>y</sub>) yang menyinggung lintasan.",
    ],
    rumus=["Mendatar (GLB): x = x₀ + v<sub>x</sub>·t; v<sub>x</sub> tetap", "Tegak: y = y₀ + v<sub>0y</sub>·t − ½·g·t²; v<sub>y</sub> = v<sub>0y</sub> − g·t",
           "Kelajuan: v = √(v<sub>x</sub>² + v<sub>y</sub>²); arah: tan θ = " + fr("v<sub>y</sub>", "v<sub>x</sub>")],
    contoh=[
        ("Dijatuhkan dan dilempar mendatar", "Dari ketinggian 20 m, bola A dijatuhkan dan bola B dilempar mendatar 10 m/s pada saat yang sama. Kapan dan di mana masing-masing mendarat?",
         T("traj-a", A_drop, B_throw, marks=[(20, 0, "")]),
         ["Gerak tegak keduanya sama: 20 = 5t² → t = 2 s untuk keduanya.", "A mendarat tepat di bawah titik lepas; B mendarat di x = 10 · 2 = 20 m."], "keduanya 2 s; A di x = 0, B di x = 20 m"),
        ("Kecepatan dari komponen", "Bola dilempar mendatar 15 m/s dari tempat tinggi. Tentukan kelajuan dan arah kecepatannya pada t = 2 s.",
         None, ["v<sub>x</sub> = 15 m/s (tetap); v<sub>y</sub> = −10 · 2 = −20 m/s.", "v = √(225 + 400) = 25 m/s; tan θ = 20/15 → θ ≈ 53° di bawah horizontal."], "25 m/s, 53° di bawah horizontal"),
    ],
    bertahap=dict(
        soal="Bola menggelinding keluar dari tepi meja setinggi 1,25 m dengan kecepatan mendatar 3 m/s. Tentukan waktu jatuh, jarak mendarat dari kaki meja, dan kelajuan saat menyentuh lantai.",
        langkah=["Tegak: 1,25 = 5t² → t = ____ s.", "Mendatar: x = 3 · ____ = ____ m.", "v<sub>y</sub> = 10 · ____ = ____ m/s; v = √(3² + ____²) = ____ m/s."],
        cek="Waktu jatuh dihitung hanya dari gerak tegak karena",
        opsi=["(a) gerak mendatar tidak memengaruhi gerak tegak", "(b) kecepatan mendatarnya kecil"],
        kunci="0,5 s; 1,5 m; v<sub>y</sub> = 5 m/s, v = √34 ≈ 5,83 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Kecepatan mendatar tidak memengaruhi waktu jatuh.",
        "Kecepatan mendatar tetap selama melayang (tanpa hambatan udara); hanya v<sub>y</sub> yang berubah.",
        "Kelajuan bukan v<sub>x</sub> + v<sub>y</sub>; gabungkan dengan Pythagoras.",
    ],
    latihan=[
        Q(1, "Dari ketinggian yang sama, bola P dijatuhkan dan bola Q dilempar mendatar bersamaan. Mana yang menyentuh tanah lebih dulu?", "bersamaan", "Gerak tegak keduanya sama."),
        Q(1, "Bola dilempar mendatar 12 m/s. Berapa v<sub>x</sub>-nya setelah 3 s?", "12 m/s", "v<sub>x</sub> tetap."),
        Q(1, "Untuk bola yang sama, berapa v<sub>y</sub>-nya setelah 3 s?", "30 m/s ke bawah", "−10 · 3."),
        Q(1, "Bola dilempar mendatar 8 m/s. Berapa kelajuannya pada t = 0,6 s?", "10 m/s", "v<sub>y</sub> = 6 m/s; √(64 + 36)."),
        Q(1, "Bola dilempar mendatar 10 m/s dari titik asal. Tentukan posisinya pada t = 1 s.", "(10 m, −5 m)", "x = 10; y = −5."),
        Q(2, "Pesawat terbang mendatar 50 m/s pada ketinggian 180 m dan menjatuhkan paket. Hambatan udara diabaikan. Kapan paket menyentuh tanah, berapa jauh secara mendatar, dan di mana posisi pesawat saat itu?", "6 s; 300 m; tepat di atas paket",
          "180 = 5t² → t = 6 s; x = 300 m. Paket dan pesawat mempunyai v<sub>x</sub> yang sama."),
        Q(2, "Bola dilempar mendatar 20 m/s. Ke mana arah kecepatannya pada t = 1,5 s?", "37° di bawah horizontal", "v<sub>y</sub> = −15; tan θ = 15/20."),
        Q(2, "Bola dilempar mendatar 10 m/s dari titik asal. Berapa jaraknya dari titik asal pada t = 2 s?", f"√800 ≈ {n(math.sqrt(800))} m", "x = 20 m, y = −20 m."),
        Q(2, "Grafik v<sub>x</sub>–t dan v<sub>y</sub>–t sebuah bola ditunjukkan di bawah. Berapa kelajuan bola pada t = 2 s?", "25 m/s", "v<sub>x</sub> = 15, v<sub>y</sub> = −20; √625.",
          fig=comp_vt(15, 0, 2.5)),
        Q(3, "Bola menggelinding 2 m/s keluar dari anak tangga teratas. Setiap anak tangga tingginya 20 cm dan lebarnya 20 cm. Anak tangga ke berapa yang pertama kali dikenai bola?", "anak tangga ke-4",
          "Bola mengenai garis ujung tangga saat turun = maju: 5t² = 2t → t = 0,4 s; x = 0,8 m = 4 lebar anak tangga."),
        Q(3, "Dua bola dilempar mendatar dari ketinggian 20 m dengan kecepatan 10 m/s dan 15 m/s. Bandingkan waktu jatuh dan jarak mendaratnya.", "waktu sama 2 s; berjarak 10 m (20 m dan 30 m)", "Waktu ditentukan tinggi saja."),
        Q(3, "Penumpang kereta yang melaju tetap 20 m/s menjatuhkan bola dari ketinggian 1,25 m di atas lantai kereta. Di mana bola jatuh menurut penumpang, dan berapa jauh bola bergerak menurut orang di peron?", "tepat di bawah titik lepas; 10 m",
          "Bola dan kereta mempunyai v<sub>x</sub> sama. t = 0,5 s; menurut peron x = 20 · 0,5 = 10 m (lintasan parabola)."),
    ],
))

# ================================================================== Subbab 2: lemparan mendatar
H45 = Shot(40, 0, y0=45)
H20 = Shot(15, 0, y0=20)
SUB.append(dict(
    title="Gerak Horizontal (Lemparan Mendatar)",
    tujuan="Menentukan waktu, jarak mendarat, serta kelajuan dan arah akhir benda yang dilempar mendatar dari ketinggian tertentu.",
    konsep=[
        "Pada <b>lemparan mendatar</b>, kecepatan awal hanya punya komponen x: v<sub>0x</sub> = v₀ dan v<sub>0y</sub> = 0. Gerak tegaknya sama dengan jatuh bebas.",
        "Waktu di udara ditentukan <b>hanya oleh ketinggian</b>. Jarak mendarat sebanding dengan kecepatan lempar.",
        "Saat mendarat, kecepatan mempunyai dua komponen: v₀ mendatar dan g·t ke bawah. Makin lama jatuh, makin curam arahnya.",
    ],
    rumus=["Waktu jatuh: t = √(2h/g)", "Jarak mendarat: x = v₀·t = v₀·√(2h/g)", "Saat mendarat: v<sub>y</sub> = −g·t; v = √(v₀² + (gt)²); tan θ = " + fr("g·t", "v₀")],
    contoh=[
        ("Dari tebing", "Bola dilempar mendatar 40 m/s dari tebing setinggi 45 m. Tentukan waktu, jarak mendarat, serta kelajuan dan arah saat menyentuh tanah.",
         T("traj-b", H45),
         ["t = √(90 : 10) = 3 s; x = 40 · 3 = 120 m.", "v<sub>y</sub> = −30 m/s; v = √(1.600 + 900) = 50 m/s; tan θ = 30/40 → θ ≈ 37° di bawah horizontal."], "3 s; 120 m; 50 m/s, 37° di bawah horizontal"),
        ("Mengenai sasaran", "Dari menara setinggi 20 m, bola harus mengenai sasaran di tanah yang berjarak mendatar 30 m. Berapa kecepatan lempar mendatarnya?",
         None, ["t = √(40 : 10) = 2 s.", "v₀ = 30 : 2 = 15 m/s."], "15 m/s"),
    ],
    bertahap=dict(
        soal="Kelereng menggelinding keluar dari meja setinggi 0,8 m dan mendarat 1,2 m dari kaki meja. Tentukan kecepatan kelereng saat meninggalkan meja dan kelajuannya saat menyentuh lantai.",
        langkah=["t = √(2 · 0,8 : 10) = ____ s.", "v₀ = 1,2 : ____ = ____ m/s.", "v<sub>y</sub> = 10 · ____ = ____ m/s; v = √(____² + ____²) = ____ m/s."],
        cek="Bila meja lebih tinggi tetapi v₀ sama, jarak mendarat",
        opsi=["(a) bertambah, karena waktu jatuh lebih lama", "(b) tetap, karena v₀ sama"],
        kunci="0,4 s; 3 m/s; v<sub>y</sub> = 4 m/s, v = 5 m/s. Alasan: (a).",
    ),
    jebakan=[
        "Waktu jatuh tidak dipengaruhi v₀.",
        "Sudut saat mendarat dihitung dari tan θ = v<sub>y</sub>/v<sub>x</sub>, bukan dari tinggi dibagi jarak.",
        "Tinggi 4 kali lipat membuat waktu dan jarak mendarat hanya 2 kali lipat.",
    ],
    latihan=[
        Q(1, "Bola dilempar mendatar 6 m/s dari ketinggian 5 m. Berapa waktu dan jarak mendaratnya?", "1 s; 6 m", "t = 1 s; x = 6 m."),
        Q(1, "Bola dilempar mendatar 10 m/s dari ketinggian 80 m. Berapa jarak mendaratnya?", "40 m", "t = 4 s."),
        Q(1, "Untuk bola dari ketinggian 5 m dengan v₀ = 6 m/s, berapa kelajuannya saat menyentuh tanah?", f"√136 ≈ {n(math.sqrt(136))} m/s", "v<sub>y</sub> = 10 m/s."),
        Q(1, "Apakah melempar lebih cepat membuat bola lebih lama di udara pada lemparan mendatar?", "tidak", "Waktu hanya bergantung pada tinggi."),
        Q(1, "Dari ketinggian 20 m, bola mendarat 30 m dari kaki menara. Berapa kecepatan lempar mendatarnya?", "15 m/s", "t = 2 s."),
        Q(2, "Bola menggelinding dari meja setinggi 1,25 m dan mendarat 2 m dari kaki meja. Berapa kecepatannya saat meninggalkan meja?", "4 m/s", "t = 0,5 s."),
        Q(2, "Bola dilempar mendatar 20 m/s dari ketinggian 20 m. Ke mana arah kecepatannya saat menyentuh tanah?", "45° di bawah horizontal", "v<sub>y</sub> = 20 = v<sub>x</sub>."),
        Q(2, "Lintasan sebuah bola yang dilempar mendatar ditunjukkan di bawah. Dari grafik, tentukan tinggi lempar, jarak mendarat, dan kecepatan lemparnya.", "20 m; 30 m; 15 m/s",
          "Dari grafik: y₀ = 20 m dan mendarat di x = 30 m. t = 2 s, jadi v₀ = 15 m/s.", fig=T("traj-a", H20)),
        Q(2, "Dari tebing setinggi 45 m, batu harus melewati sungai selebar 15 m di kaki tebing. Berapa kecepatan lempar mendatar minimalnya?", "5 m/s", "t = 3 s; 15 : 3."),
        Q(3, "Pesawat bantuan terbang mendatar 60 m/s pada ketinggian 180 m. Berapa jarak mendatar sebelum sasaran paket harus dilepas?", "360 m", "t = 6 s; 60 · 6."),
        Q(3, "Dari jendela setinggi 20 m, bola dilempar mendatar dan harus mengenai jendela gedung lain yang berjarak 30 m dan setinggi 15 m. Berapa kecepatan lemparnya?", "30 m/s", "Turun 5 m → t = 1 s; 30 : 1."),
        Q(3, "Bola dilempar mendatar dengan kecepatan sama dari ketinggian h dan 4h. Bandingkan waktu jatuh dan jarak mendaratnya.", "keduanya 2 kali lipat", "t ∝ √h."),
    ],
))

# ================================================================== Subbab 3: parabola dari tanah
P53 = Shot(12, 16)                      # 20 m/s, 53°
P45 = Shot(20, 20)                      # 20√2 m/s, 45°
SUB.append(dict(
    title="Gerak Parabola dari Tanah",
    tujuan="Menguraikan kecepatan awal miring, lalu menentukan waktu ke puncak, tinggi maksimum, waktu di udara, dan jarak mendatar.",
    konsep=[
        "Benda yang ditendang atau dilempar miring dengan kecepatan v₀ dan sudut elevasi α mempunyai kecepatan awal mendatar v<sub>0x</sub> = v₀ cos α dan tegak v<sub>0y</sub> = v₀ sin α.",
        "Komponen tegak berperilaku seperti lemparan vertikal ke atas: naik, berhenti sesaat (v<sub>y</sub> = 0) di puncak, lalu turun. Komponen mendatar tetap. Karena itu, <b>di puncak kelajuan benda sama dengan v<sub>0x</sub>, bukan nol</b>.",
        "Bila benda mendarat di ketinggian yang sama dengan titik lempar, lintasannya simetris: waktu naik sama dengan waktu turun.",
    ],
    rumus=["v<sub>0x</sub> = v₀ cos α; v<sub>0y</sub> = v₀ sin α", "t<sub>puncak</sub> = " + fr("v<sub>0y</sub>", "g") + "; h<sub>maks</sub> = " + fr("v<sub>0y</sub>²", "2g"),
           "Waktu di udara T = 2·t<sub>puncak</sub>; jarak mendatar R = v<sub>0x</sub>·T = " + fr("v₀² sin 2α", "g"), "Posisi: x = v<sub>0x</sub>·t; y = v<sub>0y</sub>·t − ½·g·t²"],
    contoh=[
        ("Tendangan bola", "Bola ditendang 20 m/s dengan sudut 53° (sin 53° = 0,8; cos 53° = 0,6). Tentukan t<sub>puncak</sub>, h<sub>maks</sub>, T, dan R.",
         T("traj-a", P53, marks=[(P53.x(1.6), P53.h_max, "puncak")]),
         ["v<sub>0x</sub> = 12 m/s; v<sub>0y</sub> = 16 m/s.", "t<sub>puncak</sub> = 1,6 s; h<sub>maks</sub> = 256 : 20 = 12,8 m.", "T = 3,2 s; R = 12 · 3,2 = 38,4 m."], "1,6 s; 12,8 m; 3,2 s; 38,4 m"),
        ("Posisi dan kecepatan pada satu saat", "Bola dilempar 25 m/s dengan sudut 37°. Tentukan posisi dan kelajuannya pada t = 1 s.",
         None, ["v<sub>0x</sub> = 20 m/s; v<sub>0y</sub> = 15 m/s.", "x = 20 m; y = 15 − 5 = 10 m.", "v<sub>y</sub> = 15 − 10 = 5 m/s; v = √(400 + 25) ≈ 20,6 m/s."], "(20 m, 10 m); ≈ 20,6 m/s"),
    ],
    bertahap=dict(
        soal="Peluru ditembakkan 50 m/s dengan sudut 37° (sin 37° = 0,6; cos 37° = 0,8). Tentukan t<sub>puncak</sub>, h<sub>maks</sub>, T, dan R.",
        langkah=["v<sub>0x</sub> = 50 · 0,8 = ____ m/s; v<sub>0y</sub> = 50 · 0,6 = ____ m/s.", "t<sub>puncak</sub> = ____ : 10 = ____ s; h<sub>maks</sub> = ____² : 20 = ____ m.", "T = ____ s; R = ____ · ____ = ____ m."],
        cek="Kelajuan peluru di titik tertinggi adalah",
        opsi=["(a) v<sub>0x</sub>, karena hanya v<sub>y</sub> yang nol", "(b) nol, karena peluru berhenti sesaat"],
        kunci="40 m/s dan 30 m/s; 3 s; 45 m; T = 6 s; R = 40 · 6 = 240 m. Alasan: (a).",
    ),
    jebakan=[
        "Di puncak, v<sub>y</sub> = 0 tetapi kelajuan sama dengan v<sub>0x</sub>.",
        "R = v₀² sin 2α / g hanya berlaku bila titik lempar dan titik mendarat sama tinggi.",
        "Jangan tertukar: komponen tegak memakai sin α, komponen mendatar memakai cos α (α dari horizontal).",
    ],
    latihan=[
        Q(1, "Uraikan kecepatan 30 m/s dengan sudut 53° (sin 53° = 0,8).", "v<sub>0x</sub> = 18 m/s; v<sub>0y</sub> = 24 m/s", "30 · 0,6 dan 30 · 0,8."),
        Q(1, "Untuk bola itu, kapan mencapai puncak?", "2,4 s", "24 : 10."),
        Q(1, "Berapa tinggi maksimumnya?", "28,8 m", "576 : 20."),
        Q(1, "Berapa jarak mendatarnya bila mendarat setinggi titik tendang?", "86,4 m", "18 · 4,8, atau 900 · 0,96 : 10."),
        Q(1, "Berapa kelajuannya di titik tertinggi?", "18 m/s", "Hanya v<sub>0x</sub>."),
        Q(2, "Lintasan sebuah bola ditunjukkan di bawah: tinggi maksimum 20 m dan jarak mendatar 80 m. Tentukan waktu di udara, v<sub>0x</sub>, v<sub>0y</sub>, dan sudut elevasinya.", "4 s; 20 m/s; 20 m/s; 45°",
          "h = 20 m → v<sub>0y</sub> = 20 m/s, t<sub>puncak</sub> = 2 s, T = 4 s; v<sub>0x</sub> = 80 : 4 = 20 m/s; tan α = 1.", fig=T("traj-b", P45)),
        Q(2, "Bola ditendang 25 m/s dengan sudut 53°. Tentukan posisinya pada t = 1 s.", "(15 m, 15 m)", "v<sub>0x</sub> = 15, v<sub>0y</sub> = 20; y = 20 − 5."),
        Q(2, "Untuk bola itu, kapan bola berada 15 m di atas tanah, dan berapa x saat itu?", "t = 1 s (x = 15 m) dan t = 3 s (x = 45 m)", "15 = 20t − 5t² → t² − 4t + 3 = 0."),
        Q(2, "Grafik v<sub>x</sub>–t dan v<sub>y</sub>–t sebuah bola ditunjukkan di bawah. Tentukan tinggi maksimum dan jarak mendatarnya.", "20 m; 60 m",
          "Luas segitiga di bawah v<sub>y</sub> sampai t = 2 s: ½ · 2 · 20 = 20 m. R = 15 · 4 = 60 m.", fig=comp_vt(15, 20, 4)),
        Q(3, "Bola ditendang 20 m/s dengan sudut 30° (√3 ≈ 1,73). Tentukan waktu di udara, tinggi maksimum, dan jarak mendatarnya.", f"2 s; 5 m; ≈ {n(20 * R3 / 2 * 2, 1)} m",
          "v<sub>0x</sub> = 10√3, v<sub>0y</sub> = 10; T = 2 s; h = 5 m; R = 20√3."),
        Q(3, "Dengan kecepatan 20 m/s, berapa jarak mendatar terjauh yang bisa dicapai? Dengan sudut berapa jarak mendatarnya 20 m?", "40 m pada 45°; 15° atau 75°", "R<sub>maks</sub> = v₀²/g. 400 sin 2α : 10 = 20 → sin 2α = 0,5."),
        Q(3, "Berapa kecepatan minimal agar bola mencapai jarak mendatar 90 m?", "30 m/s (dengan sudut 45°)", "R terbesar pada 45°: v₀² : 10 = 90."),
    ],
))

# ================================================================== Subbab 4: analisis lanjutan
B_IN = Shot(8, 6, y0=2)                 # 10 m/s at 37° from 2 m: enters a 3 m ring at x = 8 m
CLIFF = Shot(20, 15, y0=20)             # 25 m/s at 37° from a 20 m cliff
C30, C60 = Shot(15 * R3, 15, label="30°", color=RED), Shot(15, 15 * R3, label="60°", color=BLUE)
SUB.append(dict(
    title="Analisis Lintasan dan Sasaran",
    tujuan="Menganalisis lintasan dengan ketinggian awal dan akhir yang berbeda, membandingkan sudut elevasi, dan memeriksa apakah benda mengenai sasaran.",
    konsep=[
        "Bila titik lempar dan titik mendarat <b>tidak sama tinggi</b>, rumus R = v₀² sin 2α/g tidak berlaku. Kembali ke dua persamaan dasar: x = v<sub>0x</sub>·t dan y = y₀ + v<sub>0y</sub>·t − ½gt². Cari t dari syarat tegak, lalu masukkan ke persamaan mendatar.",
        "Pada ketinggian yang sama, <b>dua sudut yang jumlahnya 90°</b> (misalnya 30° dan 60°) memberi jarak mendatar sama; sudut yang lebih besar memberi lintasan lebih tinggi dan lebih lama. Jarak terjauh dicapai pada 45°.",
        "Untuk memeriksa sasaran (ring basket, dinding, jendela), hitung waktu saat x sama dengan jarak sasaran, lalu bandingkan y pada saat itu dengan tinggi sasaran.",
    ],
    rumus=["Mendarat di ketinggian lain: selesaikan y₀ + v<sub>0y</sub>·t − ½gt² = y<sub>akhir</sub>, ambil akar positif yang lebih besar", "Memeriksa sasaran: t = x<sub>sasaran</sub> : v<sub>0x</sub>, lalu hitung y(t)",
           "Sudut komplementer: R(α) = R(90° − α); R terbesar pada α = 45°"],
    contoh=[
        ("Tembakan basket", "Pemain melepas bola dari ketinggian 2 m dengan kecepatan 10 m/s pada sudut 37°. Ring setinggi 3 m berada 8 m darinya (mendatar). Apakah bola masuk?",
         T("traj-a", B_IN, marks=[(8, 3, "ring")]),
         ["v<sub>0x</sub> = 8 m/s; v<sub>0y</sub> = 6 m/s.", "Saat x = 8 m: t = 1 s; y = 2 + 6 − 5 = 3 m.", "v<sub>y</sub> = 6 − 10 = −4 m/s: bola sedang turun saat tiba di ring, jadi masuk dari atas."], "masuk"),
        ("Sudut komplementer", "Dua bola ditendang 30 m/s dengan sudut 30° dan 60° (√3 ≈ 1,73). Bandingkan jarak, tinggi, dan waktunya.",
         T("traj-b", C30, C60),
         ["R = 900 · sin 60° : 10 = 45√3 ≈ 77,9 m untuk keduanya.", "30°: h = 15² : 20 = 11,25 m, T = 3 s. 60°: h = (15√3)² : 20 = 33,75 m, T = 3√3 ≈ 5,2 s."], "jarak sama; sudut 60° lebih tinggi dan lebih lama"),
    ],
    bertahap=dict(
        soal="Dari tebing setinggi 20 m, bola ditendang 25 m/s dengan sudut 37° ke atas. Kapan dan di mana bola mendarat di dasar tebing?",
        fig=T("traj-b", CLIFF),
        langkah=["v<sub>0x</sub> = ____ m/s; v<sub>0y</sub> = ____ m/s.", "0 = 20 + 15t − 5t² → t² − 3t − ____ = 0 → t = ____ s.", "x = ____ · ____ = ____ m."],
        cek="Rumus R = v₀² sin 2α/g tidak dipakai karena",
        opsi=["(a) titik tendang lebih tinggi daripada titik mendarat", "(b) sudutnya bukan 45°"],
        kunci="20 dan 15 m/s; t² − 3t − 4 = 0, t = 4 s; x = 20 · 4 = 80 m. Alasan: (a).",
    ),
    jebakan=[
        "Untuk ketinggian berbeda, R = v₀² sin 2α/g memberi jawaban salah.",
        "Saat memeriksa sasaran, cek juga apakah benda sedang naik atau turun.",
        "45° memberi jarak terjauh hanya bila titik lempar dan mendarat sama tinggi.",
    ],
    latihan=[
        Q(1, "Sudut elevasi berapa yang memberi jarak mendatar sama dengan sudut 20° (kecepatan sama, tanah datar)?", "70°", "20° + 70° = 90°."),
        Q(1, "Pada tanah datar, sudut elevasi berapa yang memberi jarak mendatar terjauh?", "45°", "sin 2α terbesar = 1."),
        Q(1, "Berapa jarak mendatar bola yang ditendang 20 m/s pada 45° di tanah datar?", "40 m", "400 : 10."),
        Q(1, "Dengan kecepatan sama, bola mana yang lebih tinggi: ditendang pada 30° atau 60°?", "60°", "v<sub>0y</sub> lebih besar."),
        Q(1, "Bola mana yang lebih lama di udara?", "60°", "T sebanding dengan v<sub>0y</sub>."),
        Q(2, "Dari tebing setinggi 15 m, bola ditendang 20 m/s dengan sudut 30°. Kapan dan sejauh mana (mendatar) bola mendarat? (√3 ≈ 1,73)", f"3 s; ≈ {n(10 * R3 * 3, 1)} m",
          "v<sub>0x</sub> = 10√3, v<sub>0y</sub> = 10. 0 = 15 + 10t − 5t² → t² − 2t − 3 = 0 → t = 3 s; x = 30√3."),
        Q(2, "Bola ditendang 20 m/s pada 37° dari tanah. Apakah bola melewati dinding setinggi 3 m yang berjarak 12 m?", "ya, bola berada sekitar 6,2 m di atas tanah", "t = 12 : 16 = 0,75 s; y = 9 − 2,81 ≈ 6,2 m."),
        Q(2, "Pemain melepas bola dari ketinggian 2 m dengan 10 m/s pada 53°. Ring setinggi 3 m berjarak 6 m. Apakah bola masuk?", "tidak; bola lewat 2 m di atas ring",
          "v<sub>0x</sub> = 6 m/s, v<sub>0y</sub> = 8 m/s. Saat x = 6 m: t = 1 s; y = 2 + 8 − 5 = 5 m."),
        Q(2, "Air dari selang menyembur 10 m/s pada 53° dari permukaan tanah. Pada ketinggian berapa air mengenai dinding yang berjarak 3 m?", "2,75 m", "t = 3 : 6 = 0,5 s; y = 4 − 1,25."),
        Q(3, "Dengan kecepatan 20 m/s di tanah datar, pada sudut berapa bola harus ditendang agar jatuh 38,4 m jauhnya?", "37° atau 53°", "sin 2α = 384 : 400 = 0,96 = 2 · 0,6 · 0,8."),
        Q(3, "Atlet lompat jauh melompat dengan kecepatan 9 m/s pada sudut 37°. Berapa jarak lompatannya bila titik lepas dan titik mendarat dianggap sama tinggi?", f"≈ {n(81 * 0.96 / 10)} m", "R = 81 · 0,96 : 10."),
        Q(3, "Dari tebing setinggi 20 m, bola P dilempar mendatar 25 m/s dan bola Q ditendang 25 m/s pada 37° ke atas. Mana yang mendarat lebih jauh, dan berapa selisihnya?", "Q, lebih jauh 30 m",
          "P: t = 2 s, x = 50 m. Q: t = 4 s (lihat Contoh Bertahap 4), x = 80 m."),
    ],
))

# ================================================================== Subbab 5: data video
TS = [k * 0.05 for k in range(17)]                      # 0 … 0,8 s
X_DATA = noisy(lambda t: 3 * t, TS, 0.04, 8)
VY_DATA = noisy(lambda t: 4 - 10 * t, TS, 0.25, 12)
X_DATA2 = noisy(lambda t: 2.5 * t, TS, 0.04, 19)
VY_DATA2 = noisy(lambda t: 3 - 10 * t, TS, 0.25, 21)
SUB.append(dict(
    title="Data Video Lintasan Parabola",
    tujuan="Membaca data pelacakan video gerak parabola: menentukan v<sub>x</sub> dari grafik x–t, g dari grafik v<sub>y</sub>–t, dan kecepatan awalnya.",
    konsep=[
        "Aplikasi pelacak video memberi posisi (x, y) bola pada setiap bingkai. Data x–t membentuk <b>garis lurus</b> (v<sub>x</sub> tetap), data y–t membentuk <b>parabola</b>, dan data v<sub>y</sub>–t membentuk <b>garis lurus</b> dengan kemiringan −g.",
        "Dari data itu: v<sub>x</sub> = kemiringan garis terbaik x–t; v<sub>0y</sub> = titik potong garis terbaik v<sub>y</sub>–t dengan sumbu v; g = −kemiringan garis terbaik v<sub>y</sub>–t.",
        "Bila v<sub>x</sub> pada data sedikit berkurang dari waktu ke waktu, berarti ada hambatan udara yang cukup berarti.",
    ],
    rumus=["v<sub>x</sub> ≈ kemiringan garis terbaik x–t", "g ≈ −(kemiringan garis terbaik v<sub>y</sub>–t)", "v₀ = √(v<sub>x</sub>² + v<sub>0y</sub>²); tan α = v<sub>0y</sub>/v<sub>x</sub>"],
    contoh=[
        ("Komponen mendatar", "Posisi mendatar bola yang dilempar diperoleh dari video setiap 0,05 s (titik); garis merah adalah garis terbaik. Tentukan v<sub>x</sub>.",
         render(TP["data-xt"], points=X_DATA, lines=[(0, 0, 0.8, 2.4, False)]),
         ["Garis melalui (0, 0) dan (0,8 ; 2,4).", "v<sub>x</sub> = 2,4 : 0,8 = 3 m/s."], "3 m/s"),
        ("Tabel posisi", "Data video setiap 0,1 s: x = 0; 0,3; 0,6; 0,9; 1,2 m dan y = 0; 0,35; 0,60; 0,75; 0,80 m. Tentukan v<sub>x</sub>, g, dan v<sub>0y</sub>.",
         None, ["x bertambah 0,3 m tiap 0,1 s: v<sub>x</sub> = 3 m/s.", "Perpindahan tegak: 0,35; 0,25; 0,15; 0,05 m; selisih −0,10 m, jadi g = 0,10 : 0,01 = 10 m/s².",
                "y(0,1) = 0,1·v<sub>0y</sub> − 0,05 = 0,35 → v<sub>0y</sub> = 4 m/s."], "v<sub>x</sub> = 3 m/s; g = 10 m/s²; v<sub>0y</sub> = 4 m/s"),
    ],
    bertahap=dict(
        soal="Data v<sub>y</sub>–t bola yang sama diperoleh dari video (titik); garis merah adalah garis terbaik. Tentukan v<sub>0y</sub>, g, saat bola di puncak, lalu v₀ dan sudut lemparnya (v<sub>x</sub> = 3 m/s).",
        fig=render(TP["data-vy"], points=VY_DATA, lines=[(0, 4, 0.8, -4, False)]),
        langkah=["Garis memotong sumbu v di v<sub>0y</sub> = ____ m/s.", "Kemiringan = (−4 − 4) : 0,8 = ____ m/s², jadi g ≈ ____ m/s².", "Puncak saat v<sub>y</sub> = 0: t = ____ s.", "v₀ = √(3² + ____²) = ____ m/s; tan α = ____ : 3 → α ≈ ____°."],
        cek="Garis terbaik dipakai, bukan dua titik data berdekatan, karena",
        opsi=["(a) derau pengukuran berkurang pengaruhnya bila selangnya panjang", "(b) titik data berdekatan selalu salah"],
        kunci="4 m/s; −10, g ≈ 10 m/s²; t = 0,4 s; v₀ = 5 m/s, tan α = 4/3, α ≈ 53°. Alasan: (a).",
    ),
    jebakan=[
        "Pastikan kamera tegak lurus bidang gerak dan ada penggaris acuan di bidang yang sama.",
        "Selang antarbingkai = 1 : (bingkai per sekon).",
        "Titik potong garis v<sub>y</sub>–t dengan sumbu v adalah v<sub>0y</sub>, bukan v₀.",
    ],
    latihan=[
        Q(1, "Data x bola tiap 0,1 s: 0; 0,25; 0,50; 0,75 m. Berapa v<sub>x</sub>?", "2,5 m/s", "0,25 : 0,1."),
        Q(1, "Data perpindahan tegak tiap 0,1 s: 0,35; 0,25; 0,15; 0,05 m. Berapa g?", "10 m/s²", "Selisih 0,10; 0,10 : 0,01."),
        Q(1, "Video direkam 60 bingkai per sekon dan bola bergerak mendatar 5 cm setiap bingkai. Berapa v<sub>x</sub>?", "3 m/s", "0,05 m : (1/60) s."),
        Q(1, "Mengapa perlu penggaris acuan di bidang gerak bola saat merekam?", "untuk mengubah piksel menjadi meter dengan skala yang benar", "Benda di luar bidang itu tampak berbeda ukuran."),
        Q(2, "Data x–t sebuah bola dari video ditunjukkan di bawah dengan garis terbaiknya. Berapa v<sub>x</sub>?", "2,5 m/s", "Garis melalui (0, 0) dan (0,8 ; 2): 2 : 0,8.",
          fig=render(TP["data-xt"], points=X_DATA2, lines=[(0, 0, 0.8, 2, False)])),
        Q(2, "Data v<sub>y</sub>–t bola yang sama ditunjukkan di bawah. Tentukan v<sub>0y</sub> dan g.", "3 m/s; 10 m/s²", "Garis melalui (0, 3) dan (0,6 ; −3): −6 : 0,6.",
          fig=render(TP["data-vy"], points=VY_DATA2, lines=[(0, 3, 0.6, -3, False)])),
        Q(2, "Dari dua soal sebelumnya, berapa kecepatan awal dan sudut lempar bola?", "≈ 3,9 m/s; ≈ 50°", f"√(2,5² + 3²) ≈ {n(math.hypot(2.5, 3))} m/s; tan α = 3 : 2,5 = 1,2 → α ≈ {n(math.degrees(math.atan2(3, 2.5)), 0)}°."),
        Q(2, "Pada data sebuah bola plastik ringan, jarak mendatar tiap 0,1 s berturut-turut 0,30; 0,28; 0,26; 0,24 m. Apa artinya?", "v<sub>x</sub> berkurang karena hambatan udara", "Tanpa hambatan udara, v<sub>x</sub> tetap."),
        Q(3, "Bola dilepas dari ketinggian 1 m dengan v<sub>x</sub> = 3 m/s dan v<sub>0y</sub> = 4 m/s. Di mana bola menyentuh lantai?", "x = 3 m (setelah 1 s)", "0 = 1 + 4t − 5t² → (5t + 1)(t − 1) = 0 → t = 1 s."),
        Q(3, "Susun langkah percobaan untuk menentukan v₀ dan sudut lempar bola dengan video ponsel.", "contoh: tripod, penggaris di bidang gerak, rekam, lacak, grafik x–t dan v<sub>y</sub>–t, ambil kemiringan dan titik potong",
          "v<sub>x</sub> dari kemiringan x–t, v<sub>0y</sub> dari titik potong v<sub>y</sub>–t; ulangi beberapa kali dan rata-ratakan."),
        Q(3, "Data menunjukkan v<sub>x</sub> = 4 m/s dan bola mencapai puncak setelah 0,3 s. Berapa v₀ dan sudut lemparnya?", "5 m/s; ≈ 37°", "v<sub>0y</sub> = 10 · 0,3 = 3 m/s; √(16 + 9) = 5; tan α = 3/4."),
    ],
))

CAMPURAN = [
    Q(1, "Pada gerak parabola tanpa hambatan udara, komponen kecepatan mana yang tetap?", "komponen mendatar", "Tidak ada gaya mendatar."),
    Q(1, "Bola dilempar mendatar dari ketinggian 45 m. Berapa lama bola di udara?", "3 s", "√9."),
    Q(1, "Bola ditendang dengan v<sub>0y</sub> = 15 m/s. Berapa tinggi maksimumnya?", "11,25 m", "225 : 20."),
    Q(1, "Sudut elevasi 25° memberi jarak sama dengan sudut berapa?", "65°", "Jumlahnya 90°."),
    Q(2, "Bola dilempar mendatar 15 m/s dari ketinggian 20 m. Berapa kelajuan dan arahnya saat menyentuh tanah?", "25 m/s; 53° di bawah horizontal", "v<sub>y</sub> = 20; √625; tan θ = 20/15."),
    Q(2, "Bola ditendang 40 m/s pada 53°. Berapa jarak mendatarnya di tanah datar?", "153,6 m", "v<sub>0x</sub> = 24, T = 6,4 s."),
    Q(2, "Bola dilempar mendatar dan mendarat 12 m dari kaki menara setelah 2 s. Berapa tinggi menara dan kecepatan lemparnya?", "20 m; 6 m/s", "h = 5 · 4; 12 : 2."),
    Q(2, "Pada lintasan parabola, di titik mana kelajuan paling kecil?", "di titik tertinggi", "Hanya tersisa v<sub>0x</sub>."),
    Q(2, "Data video: x bertambah 0,2 m tiap 0,05 s. Berapa v<sub>x</sub>?", "4 m/s", "0,2 : 0,05."),
    Q(3, "Dari tebing setinggi 50 m, bola ditendang 25 m/s pada 37° ke atas. Kapan dan sejauh mana (mendatar) bola mendarat?", "5 s; 100 m", "0 = 50 + 15t − 5t² → t² − 3t − 10 = 0 → t = 5 s; x = 20 · 5."),
]

# ------------------------------------------------------------------ TKA-level items
TK_A, TK_B = Shot(16, 12, label="P", color=RED), Shot(12, 16, label="Q", color=BLUE)
TKA = [
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Pesawat bantuan terbang mendatar 50 m/s pada ketinggian 125 m dan akan menjatuhkan paket ke titik sasaran di tanah (g = 10 m/s²; hambatan udara diabaikan). Paket harus dilepas ketika pesawat masih berjarak mendatar ... dari sasaran.",
         opsi=["50 m", "125 m", "250 m", "625 m", "1.250 m"], kunci=2,
         bahas="125 = 5t² → t = 5 s; x = 50 · 5 = 250 m.", salah="A: kecepatan dikali 1 s. B: tinggi pesawat. D: 125 · 5. E: 50 · 25 (memakai t²)."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Lintasan dua bola P dan Q yang ditendang dari tanah dengan kelajuan awal sama (20 m/s) ditunjukkan di bawah.", fig=T("traj-a", TK_A, TK_B),
         soal2="Pernyataan yang tepat tentang kedua bola adalah ....",
         opsi=["Jarak mendatar keduanya sama, tetapi Q lebih tinggi dan lebih lama di udara.", "P lebih jauh karena lintasannya lebih rendah.", "Keduanya sama lama di udara karena kelajuan awalnya sama.",
               "Kelajuan kedua bola di titik tertinggi sama.", "Q ditendang dengan sudut lebih kecil daripada P."], kunci=0,
         bahas="Keduanya mendarat di x = 38,4 m. Q: h = 12,8 m, T = 3,2 s; P: h = 7,2 m, T = 2,4 s.", salah="B: jaraknya sama. C: T bergantung pada v<sub>0y</sub>. D: kelajuan di puncak = v<sub>0x</sub> (P 16 m/s, Q 12 m/s). E: Q lebih tinggi karena sudutnya lebih besar."),
    dict(tipe="FIS-GRAF", lv=2, fmt="pg",
         soal="Grafik v<sub>x</sub>–t dan v<sub>y</sub>–t sebuah bola yang ditendang dari tanah datar ditunjukkan di bawah.", fig=comp_vt(15, 20, 4, w=280, h=170),
         soal2="Tinggi maksimum dan jarak mendatar bola berturut-turut adalah ....",
         opsi=["20 m dan 60 m", "40 m dan 60 m", "20 m dan 30 m", "20 m dan 80 m", "10 m dan 60 m"], kunci=0,
         bahas="Luas di bawah v<sub>y</sub> sampai puncak (t = 2 s): ½ · 2 · 20 = 20 m. R = 15 · 4 = 60 m.",
         salah="B: lupa ½. C: memakai waktu puncak untuk jarak. D: memakai v<sub>0y</sub> untuk jarak. E: tidak ada dasar."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Pemain basket melepas bola dari ketinggian 2 m dengan kecepatan 10 m/s pada sudut 37° (sin 37° = 0,6; cos 37° = 0,8), dan bola masuk ke ring setinggi 3 m yang berjarak mendatar 8 m. Pada lemparan berikutnya ia memakai sudut dan titik lepas yang sama, tetapi kecepatan 11 m/s. Yang akan terjadi adalah ....",
         opsi=["Bola melewati atas ring sekitar 0,9 m.", "Bola tetap masuk karena sudutnya sama.", "Bola jatuh sebelum ring karena lintasannya lebih rendah.", "Bola mengenai ring tepat di bibirnya.", "Bola melewati atas ring sekitar 2 m."], kunci=0,
         bahas=f"v<sub>0x</sub> = 8,8 m/s; v<sub>0y</sub> = 6,6 m/s. Saat x = 8 m: t = 8 : 8,8 ≈ 0,91 s; y = 2 + 6,6 · 0,91 − 5 · 0,91² ≈ {n(2 + 6.6 * (8 / 8.8) - 5 * (8 / 8.8) ** 2)} m, sekitar 0,9 m di atas ring.",
         salah="B: titik di x = 8 m berubah bila kecepatan berubah. C: kecepatan lebih besar membuat lintasan lebih tinggi pada jarak itu. D, E: tidak sesuai hitungan."),
    dict(tipe="FIS-ANALISIS", lv=3, fmt="pg",
         soal="Sebuah bola ditendang dari tanah datar dengan sudut tertentu dan mencapai jarak mendatar 20 m. Jika tendangan diulang dengan sudut sama tetapi kelajuan awal dua kali lipat (hambatan udara diabaikan), maka ....",
         opsi=["jarak mendatar menjadi 80 m, tinggi maksimum 4 kali, dan waktu di udara 2 kali", "jarak mendatar menjadi 40 m, dan tinggi maksimum 2 kali", "jarak mendatar menjadi 80 m, tetapi waktu di udara tetap",
               "jarak mendatar menjadi 40 m, dan waktu di udara 4 kali", "jarak mendatar tetap 20 m karena sudutnya sama"], kunci=0,
         bahas="R ∝ v₀², h ∝ v₀², T ∝ v₀. Dua kali v₀: R dan h empat kali, T dua kali.", salah="B, D: lupa kuadrat. C: T sebanding v₀. E: R bergantung pada v₀."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="pg",
         soal="Petugas pemadam mengarahkan air dari selang di permukaan tanah dengan kelajuan 20 m/s ke jendela yang terbuka pada ketinggian <b>12 m sampai 14 m</b>, yang berjarak mendatar 20 m (g = 10 m/s²; hambatan udara diabaikan). Sudut elevasi selang yang membuat air masuk ke jendela adalah .... (sin 37° = 0,6; sin 53° = 0,8; √3 ≈ 1,73; √2 ≈ 1,41)",
         opsi=["30°", "37°", "45°", "53°", "60°"], kunci=3,
         bahas="Pada x = 20 m, tinggi air: 30° → 4,9 m; 37° → 7,2 m; 45° → 10 m; 53° → ≈ 12,8 m (masuk); 60° → ≈ 14,6 m (di atas jendela).",
         salah="A, B, C: air mengenai dinding di bawah jendela. E: air lewat di atas jendela."),
    dict(tipe="FIS-STRATEGI", lv=3, fmt="bs",
         soal="Pesawat terbang mendatar 40 m/s pada ketinggian 80 m dan harus menjatuhkan paket tepat di titik sasaran (g = 10 m/s²; hambatan udara diabaikan). Tentukan apakah setiap strategi pelepasan berikut tepat.",
         opsi=["Melepas paket tepat ketika pesawat berada di atas sasaran.", "Melepas paket ketika sasaran masih 160 m di depan (jarak mendatar).",
               "Melepas paket ketika sasaran masih 80 m di depan, karena tinggi pesawat 80 m.", "Turun ke ketinggian 20 m dengan kelajuan sama, lalu melepas paket ketika sasaran 80 m di depan."],
         kunci=[False, True, False, True],
         bahas="Dari 80 m: t = 4 s, paket bergerak maju 160 m (1 Tidak Tepat, 2 Tepat, 3 Tidak Tepat). Dari 20 m: t = 2 s, maju 80 m (4 Tepat).", salah=""),
    dict(tipe="FIS-EKSP", lv=3, fmt="pg",
         soal="Siswa merekam lemparan bola dengan kamera ponsel untuk menentukan v<sub>x</sub>. Kamera diletakkan agak serong (tidak tegak lurus bidang gerak bola), sedangkan penggaris acuan diletakkan di bidang gerak bola.",
         soal2="Akibat yang paling mungkin pada hasil pengukuran adalah ....",
         opsi=["jarak mendatar tampak lebih pendek dari sebenarnya, sehingga v<sub>x</sub> terukur lebih kecil", "nilai g terukur lebih besar dari 10 m/s²",
               "jumlah bingkai per sekon berkurang", "lintasan berubah menjadi garis lurus", "v<sub>x</sub> terukur lebih besar karena bola tampak lebih dekat"], kunci=0,
         bahas="Bila kamera serong, gerak mendatar terlihat dari samping-miring sehingga panjangnya tampak memendek (seperti melihat penggaris dari sudut). Jarak mendatar terbaca lebih kecil, begitu juga v<sub>x</sub>.",
         salah="B: kesalahan sudut kamera terutama memendekkan arah mendatar. C: laju rekam tidak bergantung pada sudut. D: lintasan tetap melengkung. E: tidak sesuai."),
    dict(tipe="FIS-KONSEP", lv=2, fmt="pgk",
         soal="Pernyataan yang benar tentang gerak parabola tanpa hambatan udara adalah .... (Jawaban benar lebih dari satu.)",
         opsi=["Di titik tertinggi, kelajuan benda sama dengan komponen mendatar kecepatan awalnya.", "Percepatan benda selalu g ke bawah di sepanjang lintasan.",
               "Komponen mendatar kecepatannya tetap.", "Di titik tertinggi percepatannya nol.", "Benda yang lebih berat mendarat lebih jauh bila ditendang dengan kecepatan dan sudut sama."], kunci=[0, 1, 2],
         bahas="A, B, C sesuai.", salah="D: percepatan tetap g. E: massa tidak memengaruhi lintasan."),
    dict(tipe="FIS-HITUNG", lv=2, fmt="pg",
         soal="Dari puncak tebing setinggi 20 m, batu dilempar mendatar 15 m/s (g = 10 m/s²). Kecepatan batu tepat sebelum menyentuh tanah adalah ....",
         opsi=["25 m/s, arah 53° di bawah horizontal", "25 m/s, arah 37° di bawah horizontal", "35 m/s, arah 53° di bawah horizontal", "20 m/s, arah tegak ke bawah", "15 m/s, arah mendatar"], kunci=0,
         bahas="t = 2 s; v<sub>y</sub> = 20 m/s; v = 25 m/s; tan θ = 20/15 → 53°.", salah="B: sudut tertukar. C: komponen dijumlahkan. D, E: satu komponen saja."),
]

GRAPH_OPTS = {}

UJI_PG = [
    ("Pada gerak parabola tanpa hambatan udara, komponen kecepatan yang tetap adalah ....", ["mendatar", "tegak", "keduanya", "tidak ada", "bergantung pada sudut"], 0, "Tidak ada percepatan mendatar.", "B: berubah karena g. C, D, E: tidak sesuai."),
    ("Kecepatan 50 m/s dengan sudut 37° mempunyai komponen mendatar dan tegak ....", ["40 dan 30 m/s", "30 dan 40 m/s", "25 dan 25 m/s", "50 dan 0 m/s", "35 dan 15 m/s"], 0, "50 · 0,8 dan 50 · 0,6.", "B: sin dan cos tertukar. C, D, E: tidak sesuai."),
    ("Untuk soal 2, waktu mencapai puncak adalah ....", ["3 s", "4 s", "6 s", "5 s", "1,5 s"], 0, "30 : 10.", "B: memakai v<sub>0x</sub>. C: waktu di udara. D: 50 : 10. E: dibagi 2 lagi."),
    ("Untuk soal 2, tinggi maksimumnya adalah ....", ["45 m", "90 m", "80 m", "30 m", "125 m"], 0, "900 : 20.", "B: lupa ½. C: memakai v<sub>0x</sub>. D: v<sub>0y</sub>. E: memakai v₀."),
    ("Untuk soal 2, jarak mendatar di tanah datar adalah ....", ["240 m", "120 m", "250 m", "180 m", "300 m"], 0, "40 · 6.", "B: memakai t<sub>puncak</sub>. C: v₀ · 5. D: 30 · 6. E: 50 · 6."),
    ("Untuk soal 2, kelajuan di titik tertinggi adalah ....", ["40 m/s", "0", "30 m/s", "50 m/s", "10 m/s"], 0, "Hanya v<sub>0x</sub>.", "B: miskonsepsi. C: v<sub>0y</sub>. D: v₀. E: tidak ada dasar."),
    ("Bola dilempar mendatar 10 m/s dari ketinggian 45 m. Jarak mendaratnya adalah ....", ["30 m", "45 m", "90 m", "15 m", "4,5 m"], 0, "t = 3 s.", "B: tinggi. C: memakai t² = 9. D: t = 1,5 s. E: 45 : 10."),
    ("Bila kecepatan lempar mendatar diperbesar, waktu jatuhnya ....", ["tetap", "lebih lama", "lebih singkat", "dua kali", "nol"], 0, "Bergantung pada tinggi saja.", "B, C, D: miskonsepsi. E: tidak sesuai."),
    ("Sudut yang memberi jarak mendatar sama dengan 30° (kecepatan sama, tanah datar) adalah ....", ["60°", "45°", "15°", "90°", "120°"], 0, "Jumlahnya 90°.", "B: sudut jarak terjauh. C, D, E: tidak sesuai."),
    ("Jarak mendatar terjauh di tanah datar dicapai pada sudut ....", ["45°", "30°", "60°", "90°", "37°"], 0, "sin 90° = 1.", "B, C, E: jaraknya lebih pendek daripada pada 45°. D: lurus ke atas, jarak nol."),
    ("Percepatan benda di titik tertinggi lintasan parabola adalah ....", ["g ke bawah", "nol", "g ke atas", "g mendatar", "bergantung pada sudut"], 0, "Selalu g ke bawah.", "B: miskonsepsi. C, D, E: tidak sesuai."),
    ("Bola dilempar mendatar 20 m/s dari ketinggian 20 m. Arah kecepatannya saat menyentuh tanah adalah ....", ["45° di bawah horizontal", "37° di bawah horizontal", "53° di bawah horizontal", "tegak ke bawah", "mendatar"], 0, "v<sub>y</sub> = v<sub>x</sub> = 20 m/s.", "B, C: komponen tidak sama. D, E: satu komponen saja."),
    ("Data video: x bola bertambah 0,15 m tiap 0,05 s. Kecepatan mendatarnya adalah ....", ["3 m/s", "0,15 m/s", "7,5 m/s", "0,3 m/s", "30 m/s"], 0, "0,15 : 0,05.", "B: selisihnya saja. C: dibagi 0,02. D: dikali 2. E: tidak sesuai."),
    ("Bola ditendang dengan sudut sama tetapi kelajuan dua kali lipat. Jarak mendatarnya menjadi ....", ["4 kali", "2 kali", "tetap", "½ kali", "√2 kali"], 0, "R ∝ v₀².", "B: lupa kuadrat. C, D, E: tidak sesuai."),
    ("Pesawat yang terbang mendatar dengan kecepatan tetap menjatuhkan paket. Tanpa hambatan udara, saat paket menyentuh tanah pesawat berada ....", ["tepat di atas paket", "di belakang paket", "jauh di depan paket", "tepat di atas titik pelepasan", "bergantung pada ketinggian"], 0,
     "v<sub>x</sub> paket sama dengan kecepatan pesawat.", "B, C: v<sub>x</sub> keduanya sama. D: paket ikut bergerak maju. E: berlaku untuk ketinggian berapa pun."),
]
UJI_URAIAN = [
    ("Bola ditendang 40 m/s pada sudut 53° (sin 53° = 0,8). Tentukan t<sub>puncak</sub>, h<sub>maks</sub>, waktu di udara, jarak mendatar, dan kelajuan di titik tertinggi. Sketsakan lintasannya.",
     "3,2 s; 51,2 m; 6,4 s; 153,6 m; 24 m/s", "v<sub>0x</sub> = 24, v<sub>0y</sub> = 32 m/s."),
    ("Dari tebing setinggi 50 m, bola ditendang 25 m/s pada 37° ke atas. Kapan dan sejauh mana bola mendarat? Berapa kelajuannya saat itu?",
     f"5 s; 100 m; √1.625 ≈ {n(math.sqrt(1625))} m/s", "0 = 50 + 15t − 5t² → t = 5 s; v<sub>y</sub> = 15 − 50 = −35 m/s; v = √(400 + 1.225)."),
    ("Pesawat terbang mendatar 40 m/s pada ketinggian 80 m. (a) Berapa jarak mendatar sebelum sasaran paket harus dilepas? (b) Berapa kelajuan dan arah paket saat menyentuh tanah?",
     f"(a) 160 m; (b) ≈ {n(math.sqrt(3200))} m/s, 45° di bawah horizontal", "t = 4 s; v<sub>y</sub> = 40 m/s = v<sub>x</sub>."),
    ("Data video setiap 0,1 s: x = 0; 0,4; 0,8; 1,2; 1,6 m dan y = 0; 0,25; 0,40; 0,45; 0,40 m. Tentukan v<sub>x</sub>, g, v<sub>0y</sub>, v₀, dan sudut lemparnya.",
     "v<sub>x</sub> = 4 m/s; g = 10 m/s²; v<sub>0y</sub> = 3 m/s; v₀ = 5 m/s; 37°", "Perpindahan tegak 0,25; 0,15; 0,05; −0,05: selisih −0,10. y(0,1) = 0,1 v<sub>0y</sub> − 0,05 = 0,25."),
    ("Pemain melepas bola basket dari ketinggian 2 m dengan 10 m/s pada 37°. Ring setinggi 3 m berjarak 8 m. Buktikan bahwa bola masuk dan tentukan apakah bola sedang naik atau turun saat tiba di ring.",
     "masuk; sedang turun (v<sub>y</sub> = −4 m/s)", "t = 1 s; y = 2 + 6 − 5 = 3 m."),
]

META = dict(
    title="Modul Gerak Parabola", kick="Modul belajar Fisika · Fase E–F · Kelas X–XI", big="Gerak Parabola",
    subtitle="Gabungan GLB mendatar dan gerak vertikal: lemparan mendatar, lemparan miring, analisis sasaran, dan data video lintasan",
    kompetensi="Peserta didik dapat menganalisis gerak parabola sebagai gabungan gerak lurus beraturan mendatar dan gerak vertikal, menentukan besaran-besaran geraknya dari persamaan, grafik, dan data video, serta menyelesaikan masalah sehari-hari, termasuk soal berformat Tes Kemampuan Akademik (TKA).",
    intro_html="<h2>Lanjutan dari modul sebelumnya</h2><p>Modul ini menggabungkan tiga modul sebelumnya:</p><table><tr><th>Dari modul</th><th>Dipakai untuk</th></tr><tr><td>Vektor dan Gerak</td><td>menguraikan kecepatan awal menjadi komponen</td></tr><tr><td>Gerak Lurus (GLB)</td><td>arah mendatar: x = v<sub>x</sub>·t</td></tr><tr><td>Gerak Vertikal</td><td>arah tegak: y = y₀ + v<sub>0y</sub>·t − ½gt²</td></tr></table>",
    cara=["<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
          "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
          "<b>Selalu uraikan dulu</b> kecepatan awal menjadi v<sub>0x</sub> dan v<sub>0y</sub>, lalu kerjakan arah mendatar dan tegak terpisah.",
          "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b>",
          "<b>Rekam lemparan bola dengan ponsel</b> bila memungkinkan, lalu kerjakan Subbab 5 dengan datamu sendiri.",
          "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."],
    konvensi="Sumbu <b>x</b> mendatar (arah gerak positif) dan sumbu <b>y</b> tegak (ke atas positif); titik lempar di x = 0. g = 10 m/s². sin 37° = cos 53° ≈ 0,6; cos 37° = sin 53° ≈ 0,8; √3 ≈ 1,73. Hambatan udara diabaikan kecuali disebutkan. Desimal ditulis dengan koma.",
    campuran_intro="Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>lemparan mendatar atau miring? mendarat setinggi titik lempar atau tidak? yang ditanya komponen mendatar, tegak, atau gabungannya?</b>",
    tka_info=["Soal disusun meniru tipe soal Fisika pada Tes Kemampuan Akademik (TKA) SMA 2025, yang memuat gerak parabola (misalnya tembakan basket).",
              "<b>Level 2</b> (FIS-HITUNG, FIS-GRAF, FIS-KONSEP): menerapkan satu konsep atau membaca grafik. <b>Level 3</b> (FIS-ANALISIS, FIS-STRATEGI, FIS-EKSP): memprediksi lintasan, memilih strategi, atau menelaah percobaan."],
    refleksi=["Mengapa waktu jatuh lemparan mendatar tidak bergantung pada kecepatan lempar?", "Kapan rumus R = v₀² sin 2α/g tidak boleh dipakai?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"],
    ringkasan_html=(
        "<table><tr><th></th><th>Mendatar (x)</th><th>Tegak (y)</th></tr>"
        "<tr><th>Jenis gerak</th><td>GLB</td><td>gerak vertikal, a = −g</td></tr>"
        "<tr><th>Kecepatan</th><td>v<sub>x</sub> = v₀ cos α (tetap)</td><td>v<sub>y</sub> = v₀ sin α − gt</td></tr>"
        "<tr><th>Posisi</th><td>x = v<sub>x</sub>·t</td><td>y = y₀ + v₀ sin α · t − ½gt²</td></tr></table>"
        "<table><tr><th>Lemparan mendatar</th><td>t = √(2h/g); x = v₀t; v = √(v₀² + (gt)²)</td></tr>"
        "<tr><th>Dari tanah, mendarat setinggi titik lempar</th><td>t<sub>puncak</sub> = v₀ sin α/g; h<sub>maks</sub> = (v₀ sin α)²/2g; T = 2t<sub>puncak</sub>; R = v₀² sin 2α/g</td></tr>"
        "<tr><th>Ketinggian berbeda</th><td>cari t dari persamaan y, lalu x = v<sub>x</sub>·t</td></tr></table>"
        '<div class="two">' + T("traj-a", TK_A, TK_B, w=260, h=160, note="lintasan, sudut 37° dan 53°") + comp_vt(15, 20, 4, w=260, h=160) + "</div>"),
    jebakan5=["Di titik tertinggi kelajuan = v<sub>0x</sub>, bukan nol.", "Percepatan selalu g ke bawah, juga di puncak.", "Waktu lemparan mendatar hanya bergantung pada tinggi.",
              "R = v₀² sin 2α/g hanya untuk ketinggian awal dan akhir yang sama.", "sin untuk komponen tegak, cos untuk komponen mendatar (α dari horizontal)."],
    guru=["Materi mengikuti Kurikulum Merdeka Fisika SMA; letak gerak parabola dapat berbeda antarbuku (kelas X atau XI). Modul ini menyambung modul Vektor dan Gerak, Gerak Lurus, dan Gerak Vertikal.",
          "Lintasan dan grafik komponen dibuat dari satu model per soal, sehingga grafik dan kunci tidak mungkin bertentangan.",
          "Data video di Subbab 5 adalah data simulasi dengan derau buatan; ganti dengan rekaman kelas bila tersedia.",
          "Soal setara TKA meniru tipe soal TKA Fisika SMA 2025; soal ini buatan sendiri, bukan soal resmi."],
)


def check():
    c = close
    # subbab 1
    c(A_drop.t_land, 2); c(B_throw.x_land, 20); c(math.hypot(15, 20), 25); c(t_land(1.25, 0), 0.5); c(math.sqrt(9 + 25), 5.83, 0.01)
    c(math.hypot(8, 6), 10); c(t_land(180, 0), 6); c(50 * 6, 300); c(math.degrees(math.atan2(15, 20)), 36.87, 0.01); c(math.hypot(20, 20), math.sqrt(800))
    c(5 * 0.4 ** 2, 2 * 0.4); c(t_land(1.25, 0) * 20, 10)
    # subbab 2
    c(H45.t_land, 3); c(H45.x_land, 120); c(math.hypot(40, 30), 50); c(H20.x_land, 30); c(t_land(0.8, 0), 0.4); c(1.2 / 0.4, 3); c(math.hypot(3, 4), 5)
    c(t_land(5, 0) * 6, 6); c(t_land(80, 0) * 10, 40); c(math.sqrt(36 + 100), 11.66, 0.01); c(2 / t_land(1.25, 0), 4); c(15 / t_land(45, 0), 5); c(60 * t_land(180, 0), 360); c(30 / t_land(5, 0), 30)
    # subbab 3
    c(P53.t_top, 1.6); c(P53.h_max, 12.8); c(P53.t_land, 3.2); c(P53.x_land, 38.4); c(math.hypot(20, 5), 20.62, 0.01)
    c(Shot(40, 30).h_max, 45); c(Shot(40, 30).x_land, 240); c(Shot(18, 24).t_top, 2.4); c(Shot(18, 24).h_max, 28.8); c(Shot(18, 24).x_land, 86.4)
    c(P45.h_max, 20); c(P45.x_land, 80); c(Shot(15, 20).y(1), 15); c(Shot(15, 20).y(3), 15); c(Shot(15, 20).x_land, 60)
    c(Shot(10 * R3, 10).x_land, 20 * R3); c(Shot(10 * R3, 10).h_max, 5); c(400 * 0.5 / 10, 20); c(math.sqrt(900), 30)
    # subbab 4
    c(B_IN.y(1), 3); c(B_IN.vy_at(1), -4); c(C30.x_land, C60.x_land); c(C30.x_land, 45 * R3); c(C30.h_max, 11.25); c(C60.h_max, 33.75)
    c(CLIFF.t_land, 4); c(CLIFF.x_land, 80); c(Shot(10 * R3, 10, y0=15).t_land, 3); c(Shot(16, 12).y(0.75), 6.1875); c(Shot(6, 8, y0=2).y(1), 5); c(Shot(6, 8).y(0.5), 2.75)
    c(400 * 0.96 / 10, 38.4); c(81 * 0.96 / 10, 7.776); c(Shot(25, 0, y0=20).x_land, 50)
    # subbab 5
    from kit import lsq_slope
    c(lsq_slope(X_DATA), 3, 0.1); c(lsq_slope(VY_DATA), -10, 0.6); c(lsq_slope(X_DATA2), 2.5, 0.1); c(lsq_slope(VY_DATA2), -10, 0.6)
    c(t_land(1, 4), 1); c(0.05 * 60, 3); c(math.hypot(4, 3), 5)
    # campuran, TKA, uji
    c(Shot(24, 32).x_land, 153.6); c(Shot(20, 15, y0=50).t_land, 5); c(Shot(20, 15, y0=50).x_land, 100)
    c(t_land(125, 0) * 50, 250); c(TK_A.x_land, TK_B.x_land)
    heights = {a: Shot(20 * math.cos(math.radians(a)), 20 * math.sin(math.radians(a))) for a in (30, 45, 60)}
    for a, h in ((30, 4.88), (45, 10), (60, 14.64)):
        sh = heights[a]
        c(sh.y(20 / sh.vx), h, 0.01)
    c(Shot(16, 12).y(20 / 16), 7.19, 0.01); c(Shot(12, 16).y(20 / 12), 12.78, 0.01)
    c(2 + 6.6 * (8 / 8.8) - 5 * (8 / 8.8) ** 2, 3.87, 0.01); c(t_land(80, 0) * 40, 160); c(t_land(20, 0) * 40, 80)
    c(Shot(15, 0, y0=20).t_land, 2); c(math.sqrt(1625), 40.31, 0.01); c(math.sqrt(3200), 56.57, 0.01)
    return True
