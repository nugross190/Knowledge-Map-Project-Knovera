"""Render content.py into modul.html (A4 print layout); print/print.mjs turns it into print/vektor-gerak.pdf.

Usage (from the repository root):
    python print/vektor-gerak/render.py
    NODE_PATH="$(npm root -g)" node print/print.mjs print/vektor-gerak/modul.html print/vektor-gerak.pdf "Modul Vektor dan Gerak · Fisika SMA Kelas X–XI"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content as C  # noqa: E402

assert C.check()
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "modul.html"
LV = {1: ("mudah", "●○○ Mudah"), 2: ("sedang", "●●○ Sedang"), 3: ("sulit", "●●● Sulit")}
LVNAME = {1: "Tingkat mudah", 2: "Tingkat sedang", 3: "Tingkat sulit"}
L = "ABCDE"

CSS = """
@page{size:A4;margin:16mm 15mm 18mm 15mm}
*{box-sizing:border-box}
body{margin:0;font-family:"DejaVu Serif",Georgia,serif;font-size:10.4pt;line-height:1.5;color:#1f2430}
h1,h2,h3,h4,.lab,.badge,.no,th,.kick{font-family:Inter,"DejaVu Sans",sans-serif}
.navy{color:#1f3a68}
h1.sec{font-size:20pt;color:#1f3a68;margin:0 0 10px;padding-bottom:6px;border-bottom:2px solid #1f3a68;font-weight:700}
.page{break-before:page}
.kick{font-size:8.5pt;letter-spacing:.12em;text-transform:uppercase;color:#2e5597;font-weight:600}
h2{font-size:13pt;color:#1f3a68;margin:16px 0 6px;break-after:avoid}
h3{break-after:avoid}
h3.tier{font-size:8.5pt;letter-spacing:.1em;text-transform:uppercase;margin:14px 0 6px;padding-bottom:3px;border-bottom:1px solid #d5d9e2}
.t1{color:#2e6b32}.t2{color:#8a5a00}.t3{color:#a3302a}
p{margin:0 0 6px}
.tujuan{color:#5b6270;margin:4px 0 10px}
.box{border-radius:6px;padding:9px 12px;margin:8px 0;break-inside:avoid}
.box .lab{font-size:8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px}
.konsep{background:#ecf1fa}.konsep .lab{color:#1f3a68}
.rumus{border:1.3px solid #1f3a68}.rumus .lab{color:#1f3a68}
.rumus ul{margin:0;padding-left:1.2em}.rumus li{margin:3px 0}
.contoh{background:#f4f5f8;border-left:4px solid #2e5597;border-radius:0 6px 6px 0}.contoh .lab{color:#1f3a68}
.contoh ol{margin:2px 0 4px;padding-left:1.3em}.jawab{color:#1f3a68;font-weight:700}
.bertahap{background:#fffbea;border:1.3px dashed #c9a227}.bertahap .lab{color:#8a6a00}
.bertahap ol{margin:2px 0 4px;padding-left:1.3em}.bertahap li{margin:3px 0}
.jebakan{background:#fdeeec;border-left:4px solid #d4643c;border-radius:0 6px 6px 0}.jebakan .lab{color:#b4452a}
.jebakan ul,.ingat ul,.guru ul{margin:0;padding-left:1.2em}
.ingat{background:#eef6ec;border-left:4px solid #5a9a4f;border-radius:0 6px 6px 0}.ingat .lab{color:#3d7a33}
.tka-info{background:#f3eefa;border-left:4px solid #6a4a9c;border-radius:0 6px 6px 0}.tka-info .lab{color:#5a3a8c}
.guru{background:#f4f5f8}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;line-height:1.15;margin:0 2px}
.fr span:last-child{border-top:1px solid currentColor}
table{border-collapse:collapse;width:100%;font-size:9.4pt;margin:6px 0;break-inside:avoid}
th{background:#e6ebf4;color:#1f3a68;text-align:left;font-size:8.3pt;padding:5px 7px;border:1px solid #cdd4e0}
td{padding:5px 7px;border:1px solid #d5d9e2;vertical-align:top}
.item{display:grid;grid-template-columns:34px 1fr;gap:0 6px;margin:7px 0;break-inside:avoid}
.no{font-weight:700;font-size:9pt;color:#1f3a68;padding-top:2px}
.badge{display:inline-block;font-size:7pt;font-weight:600;border-radius:9px;padding:1px 7px;margin-right:6px;vertical-align:1px;white-space:nowrap}
.b-mudah{background:#e3f1e1;color:#2e6b32}.b-sedang{background:#fdf0cf;color:#8a5a00}.b-sulit{background:#fbe0dc;color:#a3302a}
.b-tka{background:#ece4f7;color:#5a3a8c}
.line{border-bottom:1px dotted #9aa1ad;height:18px;color:#8a909b;font-size:8pt;padding-top:2px}
.space{border:1px dashed #c4c9d2;border-radius:5px;margin-top:5px}
.opts{display:grid;grid-template-columns:repeat(5,1fr);gap:2px 10px;margin-top:3px}
.opts.long{grid-template-columns:1fr}
.opts.mid{grid-template-columns:repeat(3,1fr)}
.yakin{font-family:Inter,sans-serif;font-size:7.5pt;color:#5b6270;margin-top:3px}
.chk{display:inline-block;width:9px;height:9px;border:1px solid #6b7280;border-radius:2px;margin:0 3px 0 8px;vertical-align:-1px}
.bs td:not(:first-child),.bs th:not(:first-child){width:68px;text-align:center}
.cover{height:250mm;display:flex;flex-direction:column}
.cover .big{font-family:Inter,sans-serif;font-size:40pt;font-weight:800;color:#1f3a68;line-height:1.05;margin:6px 0 4px}
.cover .sub{font-size:13pt;color:#5b6270}
.stats{display:flex;gap:36px;margin:44px 0 40px}
.stat{border-left:3px solid #1f3a68;padding-left:8px}
.stat b{display:block;font-family:Inter,sans-serif;font-size:22pt;color:#1f3a68}
.stat span{font-size:9pt;color:#5b6270}
.fill{display:grid;grid-template-columns:90px 280px;gap:14px 10px;font-family:Inter,sans-serif;font-size:9.5pt;color:#4b5260;margin-bottom:40px}
.fill i{border-bottom:1px solid #8a909b}
.toc{columns:1;padding-left:2.2em}.toc li{margin:4px 0}
.kunci{columns:2;column-gap:22px;font-size:8.6pt;line-height:1.42}
.kunci h4{font-size:9.5pt;color:#1f3a68;margin:8px 0 3px;break-after:avoid}
.kunci p{margin:0 0 4px;break-inside:avoid}
.kunci .k{color:#1f3a68;font-weight:700}
.kunci .s{color:#9a4a22}
figure{margin:6px 0;text-align:center;break-inside:avoid}
figure svg{width:62mm;height:auto}
figcaption{font-size:8.5pt;color:#5b6270}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
"""

SVG_ADD = ('<svg viewBox="0 0 260 200"><defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1f2430"/></marker>'
           '<marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2e5597"/></marker></defs>'
           '<g fill="none" stroke-width="3"><line x1="30" y1="175" x2="150" y2="175" stroke="#1f2430" marker-end="url(#ah)"/>'
           '<line x1="150" y1="175" x2="150" y2="22" stroke="#1f2430" marker-end="url(#ah)"/>'
           '<line x1="30" y1="175" x2="146" y2="27" stroke="#2e5597" stroke-dasharray="7 4" marker-end="url(#ah2)"/></g>'
           '<g font-size="14" font-family="DejaVu Sans" fill="#1f2430"><text x="62" y="195">A = 6 (timur)</text><text x="158" y="105">B = 8 (utara)</text>'
           '<text x="40" y="90" fill="#2e5597">R = 10</text><text x="62" y="166">θ</text></g></svg>')
SVG_RIVER = ('<svg viewBox="0 0 300 210"><defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#1f2430"/></marker>'
             '<marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="#2e5597"/></marker></defs>'
             '<rect x="0" y="40" width="300" height="130" fill="#dde7f6"/>'
             '<line x1="0" y1="40" x2="300" y2="40" stroke="#1f2430"/><line x1="0" y1="170" x2="300" y2="170" stroke="#1f2430"/>'
             '<g fill="none" stroke-width="3"><line x1="150" y1="165" x2="96" y2="68" stroke="#1f2430" marker-end="url(#ar)"/>'
             '<line x1="96" y1="68" x2="146" y2="68" stroke="#1f2430" stroke-dasharray="5 4" marker-end="url(#ar)"/>'
             '<line x1="150" y1="165" x2="150" y2="72" stroke="#2e5597" marker-end="url(#ar2)"/>'
             '<line x1="215" y1="120" x2="275" y2="120" stroke="#1f2430" marker-end="url(#ar)"/></g>'
             '<g font-size="13" font-family="DejaVu Sans" fill="#1f2430"><text x="34" y="120">v perahu</text><text x="92" y="60">v arus</text>'
             '<text x="156" y="120" fill="#2e5597">v hasil</text><text x="215" y="112">arus</text><text x="133" y="150">θ</text>'
             '<text x="8" y="30">tepi seberang</text><text x="8" y="196">tepi berangkat (hulu di kiri)</text></g></svg>')
FIGS = {1: (SVG_ADD, "Cara ujung–pangkal: pangkal B diletakkan di ujung A; resultan R ditarik dari pangkal A ke ujung B."),
        4: (SVG_RIVER, "Perahu diarahkan ke hulu dengan sudut θ; komponen ke hulu meniadakan arus sehingga lintasannya lurus menyeberang.")}


def box(cls, lab, body):
    return f'<div class="box {cls}"><div class="lab">{lab}</div>{body}</div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ol(items):
    return "<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


def answer_area(level):
    if level == 1:
        return '<div class="line">Jawab:</div>'
    return f'<div class="space" style="height:{22 if level == 2 else 30}mm"></div>'


def latihan_items(prefix, items):
    out, cur = [], None
    for n, (lv, q, *_ ) in enumerate(items, start=1):
        if lv != cur:
            cur = lv
            out.append(f'<h3 class="tier t{lv}">{LVNAME[lv]}</h3>')
        cls, lab = LV[lv]
        out.append(f'<div class="item"><div class="no">{prefix}{n}</div><div><span class="badge b-{cls}">{lab}</span>{q}{answer_area(lv)}</div></div>')
    return "".join(out)


def yakin():
    return '<div class="yakin">Keyakinan:<span class="chk"></span>Yakin<span class="chk"></span>Ragu<span class="chk"></span>Menebak</div>'


def opts_html(opsi, kind=None):
    longest = max(len(o) for o in opsi)
    cls = "long" if longest > 34 else ("mid" if longest > 14 else "")
    return f'<div class="opts {cls}">' + "".join(f"<div><b>{L[k]}.</b> {o}</div>" for k, o in enumerate(opsi)) + "</div>"


def tka_item(n, t):
    fmt_name = {"pg": "Pilihan ganda", "pgk": "Pilihan ganda kompleks", "bs": "Benar–salah (Tepat/Tidak Tepat)"}[t["fmt"]]
    head = f'<span class="badge b-tka">TKA · {t["tipe"]} · level {t["lv"]}</span><span class="badge b-{"sedang" if t["lv"] == 2 else "sulit"}">{fmt_name}</span>'
    body = f"<p>{t['soal']}</p>"
    if t.get("tabel"):
        rows = t["tabel"]
        body += "<table><tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows[1:]) + "</table>"
    if t.get("soal2"):
        body += f"<p>{t['soal2']}</p>"
    if t["fmt"] == "bs":
        body += '<table class="bs"><tr><th>Strategi</th><th>Tepat</th><th>Tidak Tepat</th></tr>' + "".join(
            f'<tr><td>{k + 1}. {o}</td><td><span class="chk"></span></td><td><span class="chk"></span></td></tr>' for k, o in enumerate(t["opsi"])) + "</table>"
    else:
        body += opts_html(t["opsi"])
    return f'<div class="item"><div class="no">T.{n}</div><div>{head}{body}{yakin()}</div></div>'


def build():
    n_lat = sum(len(s["latihan"]) for s in C.SUB)
    n_total = n_lat + len(C.CAMPURAN) + len(C.TKA) + len(C.UJI_PG) + len(C.UJI_URAIAN)
    h = [f"<!doctype html><html lang='id'><head><meta charset='utf-8'><title>Modul Vektor dan Gerak</title><style>{CSS}</style></head><body>"]

    # cover
    sections = ["Petunjuk belajar dan tujuan", "Cek prasyarat dan Kotak Ingat"] + [f"Subbab {k + 1}. {s['title']}" for k, s in enumerate(C.SUB)] + [
        "Latihan campuran", "Soal setara TKA", "Uji kompetensi", "Refleksi dan jadwal mengulang", "Ringkasan rumus", "Kunci jawaban dan pembahasan"]
    h.append(f"""<section class="cover"><div style="margin-top:40mm"><div class="kick">Modul belajar Fisika · Fase E–F · Kelas X–XI</div>
<div class="big">Vektor dan Gerak</div><div class="sub">Skalar dan vektor, resultan, perpindahan, kecepatan, gerak dua dimensi, dan kecepatan relatif</div></div>
<div class="stats"><div class="stat"><b>{2 * len(C.SUB)}</b><span>contoh soal lengkap</span></div><div class="stat"><b>{len(C.SUB)}</b><span>contoh bertahap</span></div>
<div class="stat"><b>{n_total}</b><span>soal latihan, mudah sampai setara TKA</span></div><div class="stat"><b>{len(C.TKA)}</b><span>soal setara TKA</span></div></div>
<div class="fill"><span>Nama</span><i></i><span>Kelas</span><i></i><span>Sekolah</span><i></i></div>
<h2 style="margin-top:0">Isi modul</h2><ol class="toc">{''.join(f'<li>{x}</li>' for x in sections)}</ol></section>""")

    # petunjuk
    h.append('<section class="page"><h1 class="sec">Petunjuk Belajar</h1>')
    h.append(box("konsep", "Kompetensi yang dilatih", "<p>Peserta didik dapat menganalisis besaran vektor dan menerapkannya pada gerak: perpindahan, kecepatan, percepatan, gerak dua dimensi, dan gerak relatif, termasuk menyelesaikan soal analisis dan strategi berformat Tes Kemampuan Akademik (TKA).</p>"))
    h.append("<h2>Tujuan pembelajaran</h2><p>Setelah mempelajari modul ini, kamu dapat:</p>" + ol([s["tujuan"] for s in C.SUB] + ["Menjawab soal setara TKA (pilihan ganda, pilihan ganda kompleks, dan benar–salah) tentang vektor dan gerak."]))
    h.append("<h2>Cara belajar dengan modul ini</h2>" + ol([
        "<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
        "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Pada contoh bertahap, sebagian langkah sengaja dikosongkan. Isi titik-titiknya sebelum melihat kunci.",
        "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b> Tulis jawabanmu dulu, baru cocokkan dengan kunci.",
        "<b>Gambar sketsa dan tetapkan arah positif</b> sebelum menghitung. Hampir semua kesalahan vektor berasal dari tanda dan arah.",
        "<b>Kerjakan Soal Setara TKA setelah Latihan Campuran.</b> Soal ini meniru tipe soal TKA Fisika 2025: memprediksi keadaan gerak dan memilih strategi.",
        "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."]))
    h.append('<h2>Tanda tingkat soal</h2><p><span class="badge b-mudah">●○○ Mudah</span>langsung memakai satu rumus. <span class="badge b-sedang">●●○ Sedang</span>perlu dua langkah atau lebih. <span class="badge b-sulit">●●● Sulit</span>memerlukan pemodelan atau penalaran. <span class="badge b-tka">TKA · tipe · level</span>soal yang meniru tipe soal TKA Fisika.</p>')
    h.append('<h2>Peta konsep</h2><table><tr><th></th><th>Satu dimensi (garis lurus)</th><th>Dua dimensi (bidang)</th></tr>'
             '<tr><th>Menyatakan vektor</th><td>tanda + dan − sebagai arah</td><td>Subbab 1: komponen, besar, arah</td></tr>'
             '<tr><th>Menggabungkan</th><td>dijumlahkan dengan tanda</td><td>Subbab 2: rumus cosinus dan cara komponen</td></tr>'
             '<tr><th>Gerak</th><td>Subbab 3–4: GLB dan GLBB</td><td>Subbab 3–4: kecepatan rata-rata 2D, gerak parabola</td></tr>'
             '<tr><th>Kerangka acuan</th><td>Subbab 5: kereta, mobil berpapasan</td><td>Subbab 5: perahu, pesawat, hujan</td></tr></table>')
    h.append("<p><b>Konvensi modul.</b> Sumbu x positif = timur, sumbu y positif = utara. g = 10 m/s². sin 37° = cos 53° = 0,6 dan cos 37° = sin 53° = 0,8 (pembulatan; nilai yang dipakai selalu ditulis di soal). Desimal ditulis dengan koma.</p></section>")

    # prasyarat
    h.append('<section class="page"><h1 class="sec">Cek Prasyarat</h1><p>Kerjakan delapan soal berikut tanpa kalkulator. Soal ini memeriksa bekal yang dipakai di seluruh bab.</p>')
    for code, q, *_ in C.PRASYARAT:
        h.append(f'<div class="item"><div class="no">{code}</div><div>{q}<div class="line">Jawab:</div></div></div>')
    h.append("<h2>Setelah mencocokkan jawaban</h2><table><tr><th>Jika salah pada soal</th><th>Baca dulu</th><th>Dipakai di</th></tr>" +
             "".join(f"<tr><td>{w}</td><td>Kotak Ingat {k}: {t}</td><td>{d}</td></tr>" for k, t, w, d, _ in C.INGAT) + "</table>")
    h.append('<p style="color:#5b6270;font-size:9pt">Semua benar? Langsung ke Subbab 1. Kunci Cek Prasyarat ada di bagian Kunci Jawaban.</p>')
    for k, t, w, d, items in C.INGAT:
        h.append(box("ingat", f"Kotak Ingat {k}: {t}", ul(items)))
    h.append("</section>")

    # subbab
    for k, s in enumerate(C.SUB):
        no = k + 1
        h.append(f'<section class="page"><div class="kick">Subbab {no}</div><h1 class="sec">{s["title"]}</h1><p class="tujuan"><b>Tujuan:</b> {s["tujuan"]}</p>')
        h.append(box("konsep", "Konsep", "".join(f"<p>{p}</p>" for p in s["konsep"])))
        h.append(box("rumus", "Rumus", ul(s["rumus"])))
        if k in FIGS:
            h.append(f"<figure>{FIGS[k][0]}<figcaption>{FIGS[k][1]}</figcaption></figure>")
        for m, (judul, soal, langkah, jawab) in enumerate(s["contoh"], start=1):
            h.append(box("contoh", f"Contoh {no}.{m} · {judul}", f"<p><b>Soal.</b> {soal}</p><p><b>Penyelesaian.</b></p>{ol(langkah)}<div class='jawab'>Jawab: {jawab}</div>"))
        b = s["bertahap"]
        h.append(box("bertahap", f"Contoh bertahap {no} · Lengkapi bagian yang kosong",
                     f"<p><b>Soal.</b> {b['soal']}</p>{ol(b['langkah'])}<p><b>Cek alasan.</b> {b['cek']}</p><p>" + " &nbsp; ".join(f'<span class="chk" style="margin-left:0"></span> {o}' for o in b["opsi"]) + "</p>"))
        h.append(box("jebakan", "Jebakan", ul(s["jebakan"])))
        h.append(f'<h2 style="border-top:1px solid #d5d9e2;padding-top:10px">Latihan {no}</h2>')
        h.append(latihan_items(f"{no}.", s["latihan"]))
        h.append("</section>")

    # campuran
    h.append('<section class="page"><h1 class="sec">Latihan Campuran</h1><p>Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>skalar atau vektor? jarak atau perpindahan? perlu diuraikan per komponen?</b> Memilih cara yang tepat adalah bagian dari latihannya.</p>')
    h.append(latihan_items("C.", C.CAMPURAN) + "</section>")

    # TKA
    h.append('<section class="page"><h1 class="sec">Soal Setara TKA</h1>')
    h.append(box("tka-info", "Tentang bagian ini", ul([
        "Soal disusun meniru tipe soal Fisika pada Tes Kemampuan Akademik (TKA) SMA 2025: stimulus situasi sehari-hari, lalu pertanyaan yang meminta hitungan, analisis, atau evaluasi strategi.",
        "<b>Level 2</b> (FIS-HITUNG, FIS-GRAF, FIS-KONSEP): menerapkan satu konsep atau membaca data. <b>Level 3</b> (FIS-ANALISIS, FIS-STRATEGI): memprediksi keadaan gerak atau memilih strategi yang memenuhi tujuan dan batasan.",
        "Format: pilihan ganda (satu jawaban), pilihan ganda kompleks (lebih dari satu jawaban), dan benar–salah (Tepat/Tidak Tepat per pernyataan).",
        "Strategi: tetapkan arah positif, uraikan per komponen, lalu hitung hasil <b>setiap</b> pilihan. Pilihan pengecoh sering benar besarnya tetapi salah arah atau sudutnya.",
        "Ini soal latihan buatan, bukan soal TKA resmi."])))
    h.append("".join(tka_item(n, t) for n, t in enumerate(C.TKA, start=1)) + "</section>")

    # uji kompetensi
    h.append('<section class="page"><h1 class="sec">Uji Kompetensi</h1><p>Kerjakan tanpa melihat bagian lain modul ini. Setelah menjawab setiap soal, centang seberapa yakin kamu. Waktu yang disarankan: 90 menit.</p><h2>A. Pilihan ganda</h2>')
    for n, (q, opsi, *_ ) in enumerate(C.UJI_PG, start=1):
        h.append(f'<div class="item"><div class="no">{n}</div><div>{q}{opts_html(opsi)}{yakin()}</div></div>')
    h.append("<h2>B. Uraian</h2>")
    for n, (q, *_ ) in enumerate(C.UJI_URAIAN, start=1):
        h.append(f'<div class="item"><div class="no">{n}</div><div>{q}<div class="space" style="height:38mm"></div>{yakin()}</div></div>')
    h.append("</section>")

    # refleksi
    rows = [(f"Latihan {k + 1}: {s['title']}", len(s["latihan"])) for k, s in enumerate(C.SUB)] + [("Latihan campuran", len(C.CAMPURAN)), ("Soal setara TKA", len(C.TKA)), ("Uji kompetensi", len(C.UJI_PG) + len(C.UJI_URAIAN))]
    h.append('<section class="page"><h1 class="sec">Refleksi dan Jadwal Mengulang</h1><h2>Skor latihan</h2><table><tr><th>Bagian</th><th style="width:60px">Benar</th><th>Soal yang salah (tulis nomornya)</th></tr>' +
             "".join(f"<tr><td>{a}</td><td>&nbsp;&nbsp;&nbsp;/ {b}</td><td></td></tr>" for a, b in rows) + "</table>")
    h.append('<h2>Cocokkan keyakinan dan hasil</h2><table><tr><th></th><th>Benar</th><th>Salah</th></tr><tr><th>Yakin</th><td>Sudah kuat. Cukup diulang sekali di jadwal ke-3.</td><td><b>Paling penting.</b> Ada konsep yang keliru. Baca lagi kotak Jebakan dan contoh di subbab terkait.</td></tr><tr><th>Ragu / Menebak</th><td>Belum kuat. Ulangi di semua jadwal.</td><td>Pelajari ulang contoh dan contoh bertahap, lalu kerjakan soal sejenis.</td></tr></table>')
    h.append('<h2 style="margin-top:10px">Jadwal mengulang</h2><p>Kerjakan ulang soal yang salah atau yang kamu tandai Ragu/Menebak, <b>tanpa melihat jawaban sebelumnya</b>.</p><table><tr><th>Ulangan</th><th>Kapan</th><th>Tanggal</th><th>Nomor soal</th><th>Selesai</th></tr>'
             '<tr><td>1</td><td>Besok</td><td></td><td></td><td><span class="chk"></span></td></tr><tr><td>2</td><td>Sekitar satu minggu kemudian</td><td></td><td></td><td><span class="chk"></span></td></tr><tr><td>3</td><td>Sekitar tiga minggu kemudian, atau beberapa hari sebelum ulangan/TKA</td><td></td><td></td><td><span class="chk"></span></td></tr></table>')
    h.append('<h2>Pertanyaan refleksi</h2>' + ol([f'{q}<div class="space" style="height:12mm"></div>' for q in [
        "Bagaimana cara cepat membedakan kelajuan rata-rata dan kecepatan rata-rata?", "Kapan kamu memakai rumus cosinus, dan kapan cara komponen?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"]]) + "</section>")

    # ringkasan
    h.append('<section class="page"><h1 class="sec">Ringkasan Rumus</h1><table>' + "".join(f"<tr><th style='width:34%'>{a}</th><td>{b}</td></tr>" for a, b in [
        ("Besar dan arah vektor", "|A| = √(A<sub>x</sub>² + A<sub>y</sub>²); tan θ = A<sub>y</sub>/A<sub>x</sub>"),
        ("Komponen", "A<sub>x</sub> = A cos θ; A<sub>y</sub> = A sin θ"),
        ("Resultan dua vektor", "R = √(A² + B² + 2AB cos θ); selisih √(A² + B² − 2AB cos θ)"),
        ("Batas resultan", "|A − B| ≤ R ≤ A + B"),
        ("Perpindahan", "Δr = r<sub>akhir</sub> − r<sub>awal</sub>"),
        ("Kecepatan dan kelajuan rata-rata", "v = Δr/Δt; kelajuan rata-rata = jarak/Δt"),
        ("Percepatan rata-rata", "a = Δv/Δt (Δv dihitung sebagai vektor)"),
        ("GLBB per sumbu", "v = v₀ + at; s = v₀t + ½at²; v² = v₀² + 2as"),
        ("Gerak parabola", "v<sub>x</sub> = v₀ cos α; v<sub>y</sub> = v₀ sin α − gt; t<sub>puncak</sub> = v₀ sin α/g; h<sub>maks</sub> = (v₀ sin α)²/2g; R = v₀² sin 2α/g"),
        ("Lemparan mendatar", "t = √(2h/g); x = v₀t"),
        ("Kecepatan relatif", "v<sub>AB</sub> = v<sub>A</sub> − v<sub>B</sub>; v<sub>tanah</sub> = v<sub>relatif</sub> + v<sub>arus/angin</sub>"),
        ("Menyeberang sungai", "tegak lurus: t = d/v<sub>p</sub>, x = v<sub>a</sub>t; tepat di seberang: sin θ = v<sub>a</sub>/v<sub>p</sub>, t = d/√(v<sub>p</sub>² − v<sub>a</sub>²)")]) + "</table>")
    h.append('<p style="color:#5b6270;font-size:9pt">A, B = besar vektor; θ = sudut; v₀ = kecepatan awal; α = sudut elevasi; g = 10 m/s²; v<sub>p</sub> = kecepatan perahu terhadap air; v<sub>a</sub> = kecepatan arus.</p>')
    h.append(box("jebakan", "Lima jebakan yang paling sering", ul([
        "Besar vektor tidak pernah negatif; tanda hanya ada pada komponen.", "3 + 4 = 5 hanya untuk vektor yang saling tegak lurus.",
        "Kelajuan rata-rata memakai jarak; kecepatan rata-rata memakai perpindahan.", "Di titik tertinggi parabola, kecepatan tidak nol (masih ada v<sub>x</sub>).",
        "Kecepatan relatif dihitung dengan mengurangkan vektor, bukan kelajuannya."])) + "</section>")

    # kunci
    k = ['<section class="page"><h1 class="sec">Kunci Jawaban dan Pembahasan</h1><div class="kunci"><h4>Cek Prasyarat</h4>']
    k += [f'<p><b>{c}</b> <span class="k">{a}</span>. {e}</p>' for c, q, a, e in C.PRASYARAT]
    for n, s in enumerate(C.SUB, start=1):
        k.append(f"<h4>Subbab {n}. {s['title']}</h4><p><b>Contoh Bertahap {n}</b> {s['bertahap']['kunci']}</p>")
        k += [f'<p><b>{n}.{m}</b> <span class="k">{a}</span>. {e}</p>' for m, (lv, q, a, e) in enumerate(s["latihan"], start=1)]
    k.append("<h4>Latihan Campuran</h4>")
    k += [f'<p><b>C.{m}</b> <span class="k">{a}</span>. {e}</p>' for m, (lv, q, a, e) in enumerate(C.CAMPURAN, start=1)]
    k.append("<h4>Soal Setara TKA</h4>")
    for m, t in enumerate(C.TKA, start=1):
        if t["fmt"] == "pg":
            key = f"{L[t['kunci']]}"
        elif t["fmt"] == "pgk":
            key = ", ".join(L[x] for x in t["kunci"])
        else:
            key = "; ".join(f"{x + 1} {'Tepat' if v else 'Tidak Tepat'}" for x, v in enumerate(t["kunci"]))
        k.append(f'<p><b>T.{m}</b> <span class="k">{key}</span>. {t["bahas"]}' + (f' <span class="s">Pilihan salah: {t["salah"]}</span>' if t["salah"] else "") + "</p>")
    k.append("<h4>Uji Kompetensi: pilihan ganda</h4>")
    k += [f'<p><b>{m}</b> <span class="k">{L[key]} ({opsi[key]})</span>. {e} <span class="s">Pilihan salah: {sl}</span></p>' for m, (q, opsi, key, e, sl) in enumerate(C.UJI_PG, start=1)]
    k.append("<h4>Uji Kompetensi: uraian</h4>")
    k += [f'<p><b>{m}</b> <span class="k">{a}</span>. {e}</p>' for m, (q, a, e) in enumerate(C.UJI_URAIAN, start=1)]
    k.append("</div>")
    k.append(box("guru", "Catatan untuk guru", ul([
        "Materi mengikuti Kurikulum Merdeka Fisika SMA. Letak vektor dan kinematika dua dimensi berbeda antarbuku (kelas X atau XI); lewati bagian yang belum diajarkan.",
        "Soal setara TKA meniru tipe soal TKA Fisika SMA 2025 (hitung, grafik/tabel, konsep, analisis, strategi). Soal ini buatan sendiri, bukan soal resmi; tingkat kesulitan sebenarnya dapat berbeda.",
        "Nilai sin 37° = 0,6 dan cos 37° = 0,8 adalah pembulatan (sudut sebenarnya 36,87°); setiap soal menuliskan nilai yang dipakai.",
        "Pilihan salah pada soal pilihan ganda disusun dari kesalahan yang umum, sehingga jawaban yang dipilih siswa menunjukkan letak salah konsepnya.",
        "Semua jawaban numerik sudah diperiksa ulang dengan perhitungan komputer."])))
    k.append("</section>")
    h += k
    h.append("</body></html>")
    OUT.write_text("".join(h), encoding="utf-8")
    print("items:", n_total, "latihan", n_lat, "campuran", len(C.CAMPURAN), "tka", len(C.TKA), "uji", len(C.UJI_PG) + len(C.UJI_URAIAN))


build()
