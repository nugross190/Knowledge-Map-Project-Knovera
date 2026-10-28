"""Render content.py into modul.html; print/print.mjs turns it into print/jembatan-gerak-lurus.pdf.

The bridge sequence has its own layout (codification, translation drill, three support levels,
product before discussion), so it does not use modlib.build; it reuses modlib's CSS and boxes.

Usage (from the repository root):
    python print/jembatan-gerak-lurus/render.py
    NODE_PATH="$(npm root -g)" node print/print.mjs print/jembatan-gerak-lurus/modul.html print/jembatan-gerak-lurus.pdf "Jembatan ke Gerak Lurus · Fisika SMA Kelas X · Draf"
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import content as C  # noqa: E402
from modlib import CSS, box, ul, ol, fig  # noqa: E402

EXTRA = """
.kod{background:#fbf6ec;border:1.3px solid #c9a227;border-radius:6px;padding:10px 13px;margin:8px 0;break-inside:avoid}
.kod .lab{color:#8a6a00}.kod .q{font-family:Inter,sans-serif;font-weight:700;color:#8a6a00;margin-top:6px}
.lvl{break-after:avoid;display:block;width:max-content;font-family:Inter,sans-serif;font-size:7.5pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:9px;padding:2px 9px;margin:14px 0 4px}
.l-lihat{background:#e6ebf4;color:#1f3a68}.l-bersama{background:#fdf0cf;color:#8a5a00}.l-sendiri{background:#e3f1e1;color:#2e6b32}
.lvl small{font-weight:400;text-transform:none;letter-spacing:0}
.terj td:last-child{width:42%;color:#8a909b}
.produk{background:#ecf1fa;border-left:4px solid #1f3a68;border-radius:0 6px 6px 0}.produk .lab{color:#1f3a68}
.diskusi{background:#f3eefa;border-left:4px solid #6a4a9c;border-radius:0 6px 6px 0}.diskusi .lab{color:#5a3a8c}
.macet{background:#f4f5f8;border:1px dashed #9aa1ad}.macet .lab{color:#4b5260}.macet ol{margin:0;padding-left:1.3em}
.konkret{background:#eef6ec;border:1.3px solid #5a9a4f}.konkret .lab{color:#3d7a33}
.uji{border:1.6px solid #1f3a68;border-radius:6px;padding:9px 12px;margin:12px 0;break-inside:avoid}.uji .lab{color:#1f3a68;font-family:Inter,sans-serif;font-size:8pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
table.rasio{width:auto;min-width:60mm}table.rasio td{min-width:28mm}
.g4{display:grid;grid-template-columns:1fr 1fr;gap:4px 18px;max-width:150mm}.g4 svg{width:100%;height:auto}.g4 b{font-family:Inter,sans-serif;font-size:9pt}
.draft{font-family:Inter,sans-serif;font-size:8.5pt;color:#a3302a;border:1px solid #a3302a;border-radius:4px;padding:4px 8px;display:inline-block;margin-top:14px}
.kartu td:last-child{height:9mm;width:55%}
.cek td:nth-child(3){width:32%}
"""

LEVEL = {"lihat": ("Lihat", "guru mencontohkan · <i>ing ngarsa sung tuladha</i>"),
         "bersama": ("Bersama", "kerja kelompok · <i>ing madya mangun karsa</i>"),
         "sendiri": ("Sendiri", "guru hanya memeriksa · <i>tut wuri handayani</i>")}


def lvl(key):
    name, sub = LEVEL[key]
    return f'<div class="lvl l-{key}">{name} <small>· {sub}</small></div>'


def item(no, q, extra="", space=18):
    return f'<div class="item"><div class="no">{no}</div><div>{q}{extra}<div class="space" style="height:{space}mm"></div></div></div>'


def step(s):
    no = s["no"]
    h = [f'<section class="page"><div class="kick">Langkah {no}</div><h1 class="sec">{s["judul"]}</h1>',
         f'<p class="tujuan"><b>Tujuan:</b> {s["target"]}<br><b>Yang dipakai:</b> {s["beban"]}</p>']
    if s.get("ingat"):
        h.append(f'<p class="tujuan">Jika Cek Awal-mu menunjuk ke sini, baca dulu Kotak Ingat {", ".join(s["ingat"])}.</p>')
    h.append(f'<div class="kod"><div class="lab">Cerita</div><p>{s["kodifikasi"]}</p>{fig(s.get("kodifikasi_fig", ""))}'
             '<div class="q">Apa yang terjadi? Apa yang bisa kita ukur?</div><div class="space" style="height:14mm"></div></div>')
    h.append('<h2>Cerita → operasi</h2><p>Sebut operasinya saja. Jangan menghitung.</p><table class="terj"><tr><th>Pertanyaan</th><th>Operasi</th></tr>' +
             "".join(f"<tr><td>{q}</td><td></td></tr>" for q, _ in s["terjemah"]) + "</table>")

    L = s["lihat"]
    h.append(lvl("lihat"))
    h.append(box("contoh", "Contoh", f"<p><b>Soal.</b> {L['soal']}</p>{fig(L['fig'])}{ol(L['langkah'])}<div class='jawab'>Jawab: {L['jawab']}</div>"))

    B = s["bersama"]
    h.append(lvl("bersama"))
    bfig = ('<div class="g4">' + "".join(f"<div><b>{k}.</b>{C.FIG_COCOK[k]}</div>" for k in sorted(C.FIG_COCOK)) + "</div>") if B["fig"] == "COCOK" else fig(B["fig"])
    h.append(box("bertahap", "Lengkapi bagian yang kosong", f"<p><b>Soal.</b> {B['soal']}</p>{bfig}{ol(B['langkah'])}"))

    h.append(lvl("sendiri"))
    h.append(fig(s.get("sendiri_fig", "")))
    h.append("".join(item(f"{no}.{k}", q) for k, (q, _, _) in enumerate(s["sendiri"], start=1)))
    h.append(box("macet", "Kalau macet · ambil satu bantuan, coba lagi, baru ambil bantuan berikutnya", ol(s["macet"])))

    h.append(box("konkret", "Kegiatan", f"<p>{s['konkret']}</p>"))
    h.append(box("produk", "Hasil kerja · serahkan sebelum diskusi", f"<p>{s['produk']}</p>"))
    h.append(box("diskusi", "Diskusi · jawab dengan bukti dari hasil kerjamu", f"<p>{s['diskusi']}</p>"))

    u = [f'<div class="uji"><div class="lab">Uji keluar Langkah {no}</div>']
    for k, (q, _, _) in enumerate(s["uji"], start=1):
        extra = fig(s["uji_blank"]) if (k == 1 and s.get("uji_blank")) else ""
        u.append(item(f"U{no}.{k}", q, extra, 4 if extra else 14))
    u.append("</div>")
    h.append("".join(u) + "</section>")
    return "".join(h)


def main(out):
    M = C.META
    h = [f"<!doctype html><html lang='id'><head><meta charset='utf-8'><title>{M['title']}</title><style>{CSS}{EXTRA}</style></head><body>"]

    toc = ["Petunjuk", "Cek Awal dan Kotak Ingat"] + [f"Langkah {s['no']}. {s['judul']}" for s in C.LANGKAH] + [C.PRAKSIS["judul"], "Kunci jawaban", "Catatan untuk guru"]
    h.append(f"""<section class="cover"><div style="margin-top:40mm"><div class="kick">{M['kick']}</div>
<div class="big">{M['big']}</div><div class="sub">{M['subtitle']}</div>
<div class="draft">DRAF · belum diuji di kelas · angka dalam cerita adalah contoh</div></div>
<div class="stats"><div class="stat"><b>4</b><span>langkah, dari mudah ke grafik</span></div><div class="stat"><b>{len(C.CEK)}</b><span>soal cek awal</span></div>
<div class="stat"><b>{sum(len(s['sendiri']) + len(s['uji']) for s in C.LANGKAH)}</b><span>soal sendiri dan uji keluar</span></div></div>
<div class="fill"><span>Nama</span><i></i><span>Kelas</span><i></i><span>Kelompok</span><i></i></div>
<h2 style="margin-top:0">Isi</h2><ol class="toc">{''.join(f'<li>{x}</li>' for x in toc)}</ol></section>""")

    h.append('<section class="page"><h1 class="sec">Petunjuk</h1>')
    h.append(box("konsep", "Buklet ini untuk apa", "<p>Buklet ini adalah jembatan sebelum Modul Gerak Lurus. Isinya hanya hal-hal yang dibutuhkan untuk masuk ke sana: arti \"per\", posisi dan perpindahan, kelajuan rata-rata, dan membaca grafik posisi–waktu. Semua dimulai dari cerita yang dekat, bukan dari rumus.</p>"))
    h.append("<h2>Setelah buklet ini, kamu dapat:</h2>" + ol(M["tujuan"]))
    h.append("<h2>Cara memakai buklet ini</h2>" + ol(M["cara"]))
    h.append('<h2>Tiga tingkat bantuan di setiap langkah</h2><p>' + "".join(lvl(k).replace('class="lvl', 'style="display:inline-block;margin-right:6px" class="lvl') for k in LEVEL) + "</p><p style='margin-top:4px'>Bantuan berkurang dari Lihat ke Sendiri. Semua orang mengerjakan langkah yang sama; yang berbeda hanya seberapa dalam jawabanmu.</p>")
    h.append(f"<p><b>Konvensi.</b> {M['konvensi']} {M['catatan_angka']}</p></section>")

    h.append(f'<section class="page"><h1 class="sec">Cek Awal</h1><p>Kerjakan {len(C.CEK)} soal ini sendiri, tanpa kalkulator. Ini bukan ulangan: hasilnya menunjukkan bagian mana yang perlu kamu baca dulu.</p>')
    for code, _, q, _, _ in C.CEK:
        h.append(f'<div class="item"><div class="no">{code}</div><div>{q}<div class="line">Jawab:</div></div></div>')
    h.append('<h2>Setelah mencocokkan jawaban</h2><table class="cek"><tr><th>Keterampilan</th><th>Soal</th><th>Dipakai di</th><th>Jika salah satu soalnya salah</th></tr>' +
             "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in C.SKILL.values()) + "</table>")
    for k, t, items in C.INGAT:
        h.append(box("ingat", f"Kotak Ingat {k}: {t}", ul(items)))
    h.append("</section>")

    h += [step(s) for s in C.LANGKAH]

    P = C.PRAKSIS
    h.append(f'<section class="page"><div class="kick">Penutup</div><h1 class="sec">{P["judul"]}</h1><p>{P["intro"]}</p>')
    h.append(box("produk", "Untuk siapa", f"<p>{P['untuk']}</p>") + box("jebakan", "Aturan kartu", ul(P["aturan"])))
    h.append('<table class="kartu"><tr><th>Pertanyaan</th><th>Jawaban kelompok</th></tr>' + "".join(f"<tr><td>{r}</td><td></td></tr>" for r in P["baris"]) + "</table>")
    h.append("<p><b>Sketsa grafik x–t.</b> Pilih sendiri skala sumbunya.</p>" + f'<div class="fig" style="max-width:78mm">{C.blank_xt(t_max=6, x_max=12)}</div>')
    h.append("</section>")

    k = ['<section class="page"><h1 class="sec">Kunci Jawaban</h1><div class="kunci"><h4>Cek Awal</h4>']
    k += [f'<p><b>{c}</b> <span class="k">{a}</span>. {e}</p>' for c, _, q, a, e in C.CEK]
    for s in C.LANGKAH:
        no = s["no"]
        k.append(f"<h4>Langkah {no}. {s['judul']}</h4>")
        k.append("<p><b>Cerita → operasi</b> " + "; ".join(f'<span class="k">{a}</span>' for _, a in s["terjemah"]) + ".</p>")
        k.append(f"<p><b>Bersama</b> {s['bersama']['kunci']}</p>")
        k += [f'<p><b>{no}.{m}</b> <span class="k">{a}</span>. {e}</p>' for m, (_, a, e) in enumerate(s["sendiri"], start=1)]
        for m, (_, a, e) in enumerate(s["uji"], start=1):
            k.append(f'<p><b>U{no}.{m}</b> <span class="k">{a}</span>. {e}</p>')
            if m == 1 and s.get("uji_key"):
                k.append(f'<div class="kfig">{s["uji_key"]}</div>')
    k.append("</div></section>")
    h += k

    g = ['<section class="page"><h1 class="sec">Catatan untuk Guru</h1>', ul(C.GURU_UMUM)]
    for s in C.LANGKAH:
        G = s["guru"]
        g.append(f"<h2>Langkah {s['no']}. {s['judul']}</h2>")
        g.append(box("jebakan", "Kesalahan yang sering muncul", ul(G["salah"])))
        g.append(f"<p><b>Jika uji keluar gagal.</b> {G['gagal']}</p>")
        g.append("<table><tr><th>SOLO</th><th>Yang terlihat dari siswa</th></tr>" + "".join(
            f"<tr><td>{lab}</td><td>{G['solo'][key]}</td></tr>" for key, lab in [("uni", "Unistruktural"), ("multi", "Multistruktural"), ("rel", "Relasional"), ("ext", "Abstrak diperluas")]) + "</table>")
    g.append(box("guru", "Status draf", ul([
        "Belum diuji di kelas. Waktu, ambang 40% dan 75%, dan kriteria dua pertiga adalah perkiraan awal.",
        "Semua jawaban numerik diperiksa ulang dengan perhitungan komputer (content.check()).",
        "Angka harga, jarak, dan waktu adalah contoh bulat, bukan data lokal."])))
    g.append("</section>")
    h += g
    h.append("</body></html>")
    out.write_text("".join(h), encoding="utf-8")
    print("wrote", out)


assert C.check()
main(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "modul.html")
