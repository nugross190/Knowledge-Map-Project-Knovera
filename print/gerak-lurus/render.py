"""Render content.py into modul.html (A4 print layout); print/print.mjs turns it into print/gerak-lurus.pdf.

Usage (from the repository root):
    python print/gerak-lurus/render.py
    NODE_PATH="$(npm root -g)" node print/print.mjs print/gerak-lurus/modul.html print/gerak-lurus.pdf "Modul Gerak Lurus · Fisika SMA Kelas X"
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
.fig{margin:6px 0 4px;max-width:96mm;break-inside:avoid}.fig svg,.two svg,.gopts svg,.kfig svg{width:100%;height:auto}
.gopts{display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;max-width:150mm;margin-top:4px}.gopts b{font-family:Inter,sans-serif;font-size:9pt}
.kfig{width:52mm;margin:2px 0 4px}
.sketch{font-family:Inter,sans-serif;font-size:7.5pt;color:#5b6270}
"""


def box(cls, lab, body):
    return f'<div class="box {cls}"><div class="lab">{lab}</div>{body}</div>'


def ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ol(items):
    return "<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


def fig(svg):
    if not svg:
        return ""
    return svg if svg.startswith('<div class="two">') else f'<div class="fig">{svg}</div>'


def gopts(key):
    return '<div class="gopts">' + "".join(f"<div><b>{L[k]}.</b>{svg}</div>" for k, svg in enumerate(C.GRAPH_OPTS[key])) + "</div>"


def answer_area(it):
    if it["kfig"]:
        return '<div class="sketch">Gambar pada bingkai di atas.</div>'
    if it["opts"]:
        return '<div class="line">Jawab:</div>'
    if it["lv"] == 1:
        return '<div class="line">Jawab:</div>'
    return f'<div class="space" style="height:{22 if it["lv"] == 2 else 30}mm"></div>'


def latihan_items(prefix, items):
    out, cur = [], None
    for k, it in enumerate(items, start=1):
        if it["lv"] != cur:
            cur = it["lv"]
            out.append(f'<h3 class="tier t{cur}">{LVNAME[cur]}</h3>')
        cls, lab = LV[it["lv"]]
        extra = fig(it["fig"]) + (gopts(it["opts"]) if it["opts"] else "")
        out.append(f'<div class="item"><div class="no">{prefix}{k}</div><div><span class="badge b-{cls}">{lab}</span>{it["q"]}{extra}{answer_area(it)}</div></div>')
    return "".join(out)


def yakin():
    return '<div class="yakin">Keyakinan:<span class="chk"></span>Yakin<span class="chk"></span>Ragu<span class="chk"></span>Menebak</div>'


def opts_html(opsi):
    longest = max(len(o) for o in opsi)
    cls = "long" if longest > 34 else ("mid" if longest > 14 else "")
    return f'<div class="opts {cls}">' + "".join(f"<div><b>{L[k]}.</b> {o}</div>" for k, o in enumerate(opsi)) + "</div>"


def tka_item(n, t):
    fmt_name = {"pg": "Pilihan ganda", "pgk": "Pilihan ganda kompleks", "bs": "Benar–salah (Tepat/Tidak Tepat)"}[t["fmt"]]
    head = f'<span class="badge b-tka">TKA · {t["tipe"]} · level {t["lv"]}</span><span class="badge b-{"sedang" if t["lv"] == 2 else "sulit"}">{fmt_name}</span>'
    body = f"<p>{t['soal']}</p>" + fig(t.get("fig"))
    if t.get("soal2"):
        body += f"<p>{t['soal2']}</p>"
    if t["fmt"] == "bs":
        body += '<table class="bs"><tr><th>Strategi</th><th>Tepat</th><th>Tidak Tepat</th></tr>' + "".join(
            f'<tr><td>{k + 1}. {o}</td><td><span class="chk"></span></td><td><span class="chk"></span></td></tr>' for k, o in enumerate(t["opsi"])) + "</table>"
    elif isinstance(t["opsi"], str):
        body += gopts(t["opsi"])
    else:
        body += opts_html(t["opsi"])
    return f'<div class="item"><div class="no">T.{n}</div><div>{head}{body}{yakin()}</div></div>'


def build():
    n_lat = sum(len(s["latihan"]) for s in C.SUB)
    n_total = n_lat + len(C.CAMPURAN) + len(C.TKA) + len(C.UJI_PG) + len(C.UJI_URAIAN)
    h = [f"<!doctype html><html lang='id'><head><meta charset='utf-8'><title>Modul Gerak Lurus</title><style>{CSS}</style></head><body>"]
    sections = ["Petunjuk belajar dan tujuan", "Cek prasyarat dan Kotak Ingat"] + [f"Subbab {k + 1}. {s['title']}" for k, s in enumerate(C.SUB)] + [
        "Latihan campuran", "Soal setara TKA", "Uji kompetensi", "Refleksi dan jadwal mengulang", "Ringkasan rumus dan grafik", "Kunci jawaban dan pembahasan"]
    h.append(f"""<section class="cover"><div style="margin-top:40mm"><div class="kick">Modul belajar Fisika · Fase E · Kelas X</div>
<div class="big">Gerak Lurus</div><div class="sub">GLB dan GLBB dalam tiga cara: grafik, cerita, dan persamaan, ditambah membaca data pelacakan gerak dari ponsel</div></div>
<div class="stats"><div class="stat"><b>{2 * len(C.SUB)}</b><span>contoh soal lengkap</span></div><div class="stat"><b>{len(C.SUB)}</b><span>contoh bertahap</span></div>
<div class="stat"><b>{n_total}</b><span>soal latihan, mudah sampai setara TKA</span></div><div class="stat"><b>{len(C.TKA)}</b><span>soal setara TKA</span></div></div>
<div class="fill"><span>Nama</span><i></i><span>Kelas</span><i></i><span>Sekolah</span><i></i></div>
<h2 style="margin-top:0">Isi modul</h2><ol class="toc">{''.join(f'<li>{x}</li>' for x in sections)}</ol></section>""")

    h.append('<section class="page"><h1 class="sec">Petunjuk Belajar</h1>')
    h.append(box("konsep", "Kompetensi yang dilatih", "<p>Peserta didik dapat mendeskripsikan gerak lurus beraturan dan gerak lurus berubah beraturan melalui grafik, cerita, persamaan, dan data pengukuran, serta menyelesaikan masalah gerak dalam kehidupan sehari-hari, termasuk soal berformat Tes Kemampuan Akademik (TKA).</p>"))
    h.append("<h2>Tujuan pembelajaran</h2><p>Setelah mempelajari modul ini, kamu dapat:</p>" + ol([s["tujuan"] for s in C.SUB]))
    h.append("<h2>Satu gerak, tiga cara melihatnya</h2><p>Setiap gerak di modul ini bisa dilihat dengan tiga cara yang saling menerjemahkan. Bila kamu bisa berpindah di antara ketiganya, kamu benar-benar memahami geraknya.</p>"
             '<table><tr><th>Grafik</th><th>Cerita</th><th>Persamaan</th></tr><tr><td>Garis s–t lurus miring; garis v–t mendatar</td><td>"Angkot melaju tetap 10 m/s"</td><td>s = s₀ + vt</td></tr>'
             '<tr><td>Garis v–t lurus miring; s–t melengkung</td><td>"Motor dipercepat dari diam"</td><td>v = v₀ + at; s = s₀ + v₀t + ½at²</td></tr></table>')
    h.append("<h2>Cara belajar dengan modul ini</h2>" + ol([
        "<b>Mulai dari Cek Prasyarat.</b> Jika ada soal yang salah, baca Kotak Ingat yang ditunjuk, lalu lanjutkan.",
        "<b>Pelajari contoh, lalu kerjakan Contoh Bertahap sendiri.</b> Isi titik-titiknya sebelum melihat kunci.",
        "<b>Kerjakan latihan dari tingkat Mudah ke Sulit.</b> Untuk soal menggambar, pakai bingkai grafik yang tersedia; kuncinya berupa grafik.",
        "<b>Selalu tetapkan titik acuan dan arah positif</b> sebelum menghitung.",
        "<b>Lakukan percobaan pelacakan gerak</b> dengan ponsel bila tersedia, lalu kerjakan Subbab 5 dengan datamu sendiri.",
        "<b>Centang keyakinanmu</b> (Yakin, Ragu, Menebak) sebelum melihat kunci, lalu ulangi soal yang salah mengikuti Jadwal Mengulang."]))
    h.append('<h2>Tanda tingkat soal</h2><p><span class="badge b-mudah">●○○ Mudah</span>langsung memakai satu rumus atau satu bacaan grafik. <span class="badge b-sedang">●●○ Sedang</span>perlu dua langkah atau lebih. <span class="badge b-sulit">●●● Sulit</span>memerlukan pemodelan atau penalaran. <span class="badge b-tka">TKA · tipe · level</span>soal yang meniru tipe soal TKA Fisika.</p>')
    h.append("<p><b>Konvensi modul.</b> Koordinat posisi ditulis <b>s</b>. Pada soal tertentu koordinat ini boleh diganti <b>x</b> (gerak mendatar) atau <b>y</b> (gerak tegak); rumusnya tetap sama. Arah positif selalu ditetapkan di soal atau di gambar. Desimal ditulis dengan koma.</p></section>")

    h.append('<section class="page"><h1 class="sec">Cek Prasyarat</h1><p>Kerjakan delapan soal berikut tanpa kalkulator.</p>')
    for code, q, *_ in C.PRASYARAT:
        h.append(f'<div class="item"><div class="no">{code}</div><div>{q}<div class="line">Jawab:</div></div></div>')
    h.append("<h2>Setelah mencocokkan jawaban</h2><table><tr><th>Jika salah pada soal</th><th>Baca dulu</th><th>Dipakai di</th></tr>" +
             "".join(f"<tr><td>{w}</td><td>Kotak Ingat {k}: {t}</td><td>{d}</td></tr>" for k, t, w, d, _ in C.INGAT) + "</table>")
    for k, t, w, d, items in C.INGAT:
        h.append(box("ingat", f"Kotak Ingat {k}: {t}", ul(items)))
    h.append("</section>")

    for k, s in enumerate(C.SUB):
        no = k + 1
        h.append(f'<section class="page"><div class="kick">Subbab {no}</div><h1 class="sec">{s["title"]}</h1><p class="tujuan"><b>Tujuan:</b> {s["tujuan"]}</p>')
        h.append(box("konsep", "Konsep", "".join(f"<p>{p}</p>" for p in s["konsep"])))
        h.append(box("rumus", "Rumus", ul(s["rumus"])))
        for m, (judul, soal, svg, langkah, jawab) in enumerate(s["contoh"], start=1):
            h.append(box("contoh", f"Contoh {no}.{m} · {judul}", f"<p><b>Soal.</b> {soal}</p>{fig(svg)}<p><b>Penyelesaian.</b></p>{ol(langkah)}<div class='jawab'>Jawab: {jawab}</div>"))
        b = s["bertahap"]
        h.append(box("bertahap", f"Contoh bertahap {no} · Lengkapi bagian yang kosong",
                     f"<p><b>Soal.</b> {b['soal']}</p>{fig(b['fig'])}{ol(b['langkah'])}<p><b>Cek alasan.</b> {b['cek']}</p><p>" + " &nbsp; ".join(f'<span class="chk" style="margin-left:0"></span> {o}' for o in b["opsi"]) + "</p>"))
        h.append(box("jebakan", "Jebakan", ul(s["jebakan"])))
        h.append(f'<h2 style="border-top:1px solid #d5d9e2;padding-top:10px">Latihan {no}</h2>')
        h.append(latihan_items(f"{no}.", s["latihan"]))
        h.append("</section>")

    h.append('<section class="page"><h1 class="sec">Latihan Campuran</h1><p>Soal di bagian ini sengaja dicampur. Untuk setiap soal, tentukan dulu: <b>GLB atau GLBB? satu bagian atau beberapa bagian gerak? lebih mudah dengan grafik atau persamaan?</b></p>')
    h.append(latihan_items("C.", C.CAMPURAN) + "</section>")

    h.append('<section class="page"><h1 class="sec">Soal Setara TKA</h1>')
    h.append(box("tka-info", "Tentang bagian ini", ul([
        "Soal disusun meniru tipe soal Fisika pada Tes Kemampuan Akademik (TKA) SMA 2025: stimulus situasi sehari-hari, sering dengan grafik, lalu pertanyaan yang meminta hitungan, analisis, evaluasi strategi, atau rancangan percobaan.",
        "<b>Level 2</b> (FIS-GRAF, FIS-HITUNG, FIS-KONSEP): membaca grafik atau menerapkan satu konsep. <b>Level 3</b> (FIS-ANALISIS, FIS-STRATEGI, FIS-EKSP): memprediksi keadaan gerak, memilih strategi yang memenuhi tujuan dan batasan, atau menelaah percobaan.",
        "Ini soal latihan buatan, bukan soal TKA resmi."])))
    h.append("".join(tka_item(n, t) for n, t in enumerate(C.TKA, start=1)) + "</section>")

    h.append('<section class="page"><h1 class="sec">Uji Kompetensi</h1><p>Kerjakan tanpa melihat bagian lain modul ini. Setelah menjawab setiap soal, centang seberapa yakin kamu. Waktu yang disarankan: 90 menit.</p><h2>A. Pilihan ganda</h2>')
    for k, (q, opsi, *_ ) in enumerate(C.UJI_PG, start=1):
        h.append(f'<div class="item"><div class="no">{k}</div><div>{q}{opts_html(opsi)}{yakin()}</div></div>')
    h.append("<h2>B. Uraian</h2>")
    for k, (q, *_ ) in enumerate(C.UJI_URAIAN, start=1):
        h.append(f'<div class="item"><div class="no">{k}</div><div>{q}<div class="space" style="height:38mm"></div>{yakin()}</div></div>')
    h.append("</section>")

    rows = [(f"Latihan {k + 1}: {s['title']}", len(s["latihan"])) for k, s in enumerate(C.SUB)] + [("Latihan campuran", len(C.CAMPURAN)), ("Soal setara TKA", len(C.TKA)), ("Uji kompetensi", len(C.UJI_PG) + len(C.UJI_URAIAN))]
    h.append('<section class="page"><h1 class="sec">Refleksi dan Jadwal Mengulang</h1><h2>Skor latihan</h2><table><tr><th>Bagian</th><th style="width:60px">Benar</th><th>Soal yang salah (tulis nomornya)</th></tr>' +
             "".join(f"<tr><td>{a}</td><td>&nbsp;&nbsp;&nbsp;/ {b}</td><td></td></tr>" for a, b in rows) + "</table>")
    h.append('<h2>Cocokkan keyakinan dan hasil</h2><table><tr><th></th><th>Benar</th><th>Salah</th></tr><tr><th>Yakin</th><td>Sudah kuat. Cukup diulang sekali di jadwal ke-3.</td><td><b>Paling penting.</b> Ada konsep yang keliru. Baca lagi kotak Jebakan dan contoh di subbab terkait.</td></tr><tr><th>Ragu / Menebak</th><td>Belum kuat. Ulangi di semua jadwal.</td><td>Pelajari ulang contoh dan contoh bertahap, lalu kerjakan soal sejenis.</td></tr></table>')
    h.append('<h2 style="margin-top:10px">Jadwal mengulang</h2><table><tr><th>Ulangan</th><th>Kapan</th><th>Tanggal</th><th>Nomor soal</th><th>Selesai</th></tr>'
             '<tr><td>1</td><td>Besok</td><td></td><td></td><td><span class="chk"></span></td></tr><tr><td>2</td><td>Sekitar satu minggu kemudian</td><td></td><td></td><td><span class="chk"></span></td></tr><tr><td>3</td><td>Sekitar tiga minggu kemudian, atau beberapa hari sebelum ulangan/TKA</td><td></td><td></td><td><span class="chk"></span></td></tr></table>')
    h.append('<h2>Pertanyaan refleksi</h2>' + ol([f'{q}<div class="space" style="height:12mm"></div>' for q in [
        "Bagaimana cara cepat membedakan GLB dan GLBB dari grafik s–t dan v–t?", "Kapan kamu memakai v² = v₀² + 2as?", "Kesalahan apa yang paling sering kamu lakukan di modul ini?"]]) + "</section>")

    h.append('<section class="page"><h1 class="sec">Ringkasan Rumus dan Grafik</h1><table><tr><th></th><th>GLB</th><th>GLBB</th></tr>'
             "<tr><th>Ciri</th><td>kecepatan tetap, a = 0</td><td>percepatan tetap</td></tr>"
             "<tr><th>Grafik s–t</th><td>garis lurus; kemiringan = v</td><td>parabola; kemiringan garis singgung = v sesaat</td></tr>"
             "<tr><th>Grafik v–t</th><td>garis mendatar; luas = Δs</td><td>garis miring; kemiringan = a; luas = Δs</td></tr>"
             "<tr><th>Grafik a–t</th><td>berimpit sumbu t</td><td>garis mendatar; luas = Δv</td></tr>"
             "<tr><th>Persamaan</th><td>s = s₀ + vt</td><td>v = v₀ + at; s = s₀ + v₀t + ½at²; v² = v₀² + 2a(s − s₀)</td></tr>"
             "<tr><th>Data ponsel</th><td>Δs tiap selang sama tetap</td><td>selisih Δs berurutan tetap = a(Δt)²</td></tr></table>")
    tp = C.TP
    h.append('<div class="two">' + C.render(tp["glb-st"], (C.Motion(5, 3, [(10, 0)]),), width=260, height=160, note="GLB: s–t") + C.render(tp["glbb-st"], (C.Motion(0, 0, [(10, 1.6)]),), width=260, height=160, note="GLBB: s–t") + "</div>")
    h.append('<div class="two">' + C.render(tp["glb-vt"], (C.Motion(0, 4, [(10, 0)]),), width=260, height=160, note="GLB: v–t") + C.render(tp["glbb-vt"], (C.Motion(0, 2, [(8, 2)]),), width=260, height=160, note="GLBB: v–t") + "</div>")
    h.append(box("jebakan", "Lima jebakan yang paling sering", ul([
        "Titik potong grafik v–t berarti kecepatan sama, bukan bertemu.", "Grafik s–t lurus berarti GLB, bukan GLBB.",
        "Percepatan negatif belum tentu melambat; lihat tanda v juga.", "Jarak henti = jarak reaksi + jarak pengereman.",
        "Jangan menghitung kecepatan dari dua titik data ponsel yang berdekatan."])) + "</section>")

    k = ['<section class="page"><h1 class="sec">Kunci Jawaban dan Pembahasan</h1><div class="kunci"><h4>Cek Prasyarat</h4>']
    k += [f'<p><b>{c}</b> <span class="k">{a}</span>. {e}</p>' for c, q, a, e in C.PRASYARAT]
    for no, s in enumerate(C.SUB, start=1):
        k.append(f"<h4>Subbab {no}. {s['title']}</h4><p><b>Contoh Bertahap {no}</b> {s['bertahap']['kunci']}</p>")
        for m, it in enumerate(s["latihan"], start=1):
            k.append(f'<p><b>{no}.{m}</b> <span class="k">{it["a"]}</span>. {it["e"]}</p>' + (f'<div class="kfig">{it["kfig"]}</div>' if it["kfig"] else ""))
    k.append("<h4>Latihan Campuran</h4>")
    k += [f'<p><b>C.{m}</b> <span class="k">{it["a"]}</span>. {it["e"]}</p>' for m, it in enumerate(C.CAMPURAN, start=1)]
    k.append("<h4>Soal Setara TKA</h4>")
    for m, t in enumerate(C.TKA, start=1):
        if t["fmt"] == "pg":
            key = L[t["kunci"]]
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
        "Materi mengikuti Kurikulum Merdeka Fisika SMA Fase E. Gerak vertikal dan gerak dua dimensi dibahas di modul lain.",
        "Semua grafik dibuat dari satu model gerak per soal dan memakai bingkai tetap, sehingga grafik dan kunci tidak mungkin bertentangan; bingkai kosong yang sama dipakai siswa untuk menggambar.",
        "Data pelacakan gerak di Subbab 5 adalah data simulasi dengan derau buatan. Garis terbaik yang digambar sudah dicek terhadap regresi kuadrat terkecil datanya. Untuk praktik, ganti dengan data rekaman kelas sendiri.",
        "Soal setara TKA meniru tipe soal TKA Fisika SMA 2025; soal ini buatan sendiri, bukan soal resmi.",
        "Semua jawaban numerik sudah diperiksa ulang dengan perhitungan komputer."])))
    k.append("</section>")
    h += k
    h.append("</body></html>")
    OUT.write_text("".join(h), encoding="utf-8")
    print("items:", n_total, "latihan", n_lat, "campuran", len(C.CAMPURAN), "tka", len(C.TKA), "uji", len(C.UJI_PG) + len(C.UJI_URAIAN))


build()
