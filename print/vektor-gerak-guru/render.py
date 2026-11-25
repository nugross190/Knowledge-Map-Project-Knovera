"""Render content.py into panduan.html (A4 print layout); print/print.mjs turns it into print/vektor-gerak-guru.pdf.

Usage (from the repository root):
    python print/vektor-gerak-guru/render.py
    NODE_PATH="$(npm root -g)" node print/print.mjs print/vektor-gerak-guru/panduan.html print/vektor-gerak-guru.pdf "Panduan Guru Vektor dan Gerak · Fisika SMA Kelas X–XI"
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))
import content as C  # noqa: E402
from modlib import CSS, L, box, ol, ul  # noqa: E402

assert C.check()
S = C.S
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "panduan.html"
PAGE_URL = "https://nugross190.github.io/Knowledge-Map-Project-Knovera/modul-vektor-gerak.html"  # build.PAGES_URL + page

EXTRA = """
table{break-inside:auto}tr{break-inside:avoid}th{break-after:avoid}
.alur td:first-child{width:48px;text-align:center;font-family:Inter,sans-serif;font-weight:600;color:#1f3a68}
.alur td:nth-child(2){width:58%}
.pemantik{background:#ecf1fa}.pemantik .lab{color:#1f3a68}
.pemantik p{margin:0 0 5px}.pemantik .exp{color:#4b5260;font-size:9.4pt}
.diff{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.diff .box{margin:0}
.bantu{background:#eef6ec;border-left:4px solid #5a9a4f;border-radius:0 6px 6px 0}.bantu .lab{color:#3d7a33}
.tantang{background:#f3eefa;border-left:4px solid #6a4a9c;border-radius:0 6px 6px 0}.tantang .lab{color:#5a3a8c}
.tiket{border:1.3px dashed #1f3a68}.tiket .lab{color:#1f3a68}
.tiket ol{margin:0;padding-left:1.3em}.tiket li{margin:3px 0}
.kj{color:#1f3a68;font-weight:700}
.meta{font-family:Inter,sans-serif;font-size:9pt;color:#4b5260;margin:2px 0 8px}
.rekap td,.rekap th{text-align:center;padding:4px 3px;height:7mm}
.rekap td:nth-child(2),.rekap th:nth-child(2){text-align:left;width:38%}
.rekap td:first-child{width:24px;font-size:8pt;color:#8a909b}
.tally{width:70px}
.small{font-size:9pt;color:#5b6270}
"""


def table(head, rows, cls=""):
    return (f'<table class="{cls}"><tr>' + "".join(f"<th>{c}</th>" for c in head) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</table>")


def latihan_text(p):
    return "; ".join(f"<b>{lab}:</b> {C.refs(rs)}" for lab, rs in p["latihan"])


def key_tka(t):
    if t["fmt"] == "pg":
        return L[t["kunci"]]
    if t["fmt"] == "pgk":
        return ", ".join(L[x] for x in t["kunci"])
    return "; ".join(f"{x + 1} {'Tepat' if v else 'Tidak Tepat'}" for x, v in enumerate(t["kunci"]))


def build():
    n_siswa = sum(len(s["latihan"]) for s in S.SUB) + len(S.CAMPURAN) + len(S.TKA) + len(S.UJI_PG) + len(S.UJI_URAIAN)
    P = C.PERTEMUAN
    h = [f"<!doctype html><html lang='id'><head><meta charset='utf-8'><title>Panduan Guru Vektor dan Gerak</title><style>{CSS}{EXTRA}</style></head><body>"]

    # ---------------------------------------------------------------- cover
    sections = ["Tentang panduan ini", "Gambaran bab dan alur pertemuan", "Persiapan alat dan bahan"] + [
        f"Pertemuan {k + 1}. {p['judul']}" for k, p in enumerate(P)] + [
        C.OPSIONAL["judul"], "Katalog miskonsepsi", "Asesmen: diagnostik, formatif, sumatif", "Kunci jawaban ringkas", "Catatan dan sumber"]
    h.append(f"""<section class="cover"><div style="margin-top:34mm"><div class="kick">Panduan guru · Fisika · Fase E–F · Kelas X–XI</div>
<div class="big">Vektor dan Gerak</div><div class="sub">Pendamping modul siswa: rencana per pertemuan, miskonsepsi, asesmen, dan kunci jawaban</div></div>
<div class="stats"><div class="stat"><b>{len(P)}</b><span>pertemuan × 2 JP (2 × 45 menit)</span></div>
<div class="stat"><b>{n_siswa}</b><span>soal di modul siswa, semuanya berkunci</span></div>
<div class="stat"><b>{len(C.MISKONSEPSI)}</b><span>miskonsepsi beserta cara menanganinya</span></div>
<div class="stat"><b>{sum(len(p["tiket"]) for p in P)}</b><span>soal tiket keluar</span></div></div>
<h2 style="margin-top:0">Isi panduan</h2><ol class="toc">{''.join(f'<li>{x}</li>' for x in sections)}</ol></section>""")

    # ---------------------------------------------------------------- about
    h.append('<section class="page"><h1 class="sec">Tentang Panduan Ini</h1>')
    h.append("<p>Panduan ini menemani <b>Modul Vektor dan Gerak</b> untuk siswa. Setiap pertemuan menunjuk bagian modul yang dipakai, sehingga guru tidak perlu menyusun soal sendiri. Semua nomor soal dalam panduan ini (misalnya Latihan 2.6 atau T.4) mengacu pada modul siswa versi cetak.</p>")
    h.append("<h2>Bahan yang dipakai</h2>" + table(["Bahan", "Untuk siapa", "Isi"], [
        ["Modul siswa (PDF cetak)", "Siswa", f"Cek prasyarat, 5 subbab (konsep, rumus, contoh, contoh bertahap, jebakan, latihan), latihan campuran, {len(S.TKA)} soal setara TKA, uji kompetensi, refleksi, kunci."],
        ["Halaman interaktif", "Siswa (ponsel atau laptop)", f"Materi ringkas dan latihan 5 tahap dengan pemeriksaan jawaban langsung: {PAGE_URL}"],
        ["Panduan guru (dokumen ini)", "Guru", "Rencana pertemuan, pertanyaan pemantik, miskonsepsi, diferensiasi, tiket keluar, kisi-kisi, rubrik, analisis pengecoh, kunci ringkas."]]))
    h.append("<h2>Cara memakai panduan</h2>" + ol([
        "Baca <b>Gambaran Bab</b> untuk melihat urutan delapan pertemuan, lalu sesuaikan dengan jumlah JP dan kalender sekolah.",
        "Sebelum tiap pertemuan, siapkan alat pada kotak <b>Persiapan</b> dan coba dulu demonstrasinya.",
        "Ikuti tabel <b>Alur kegiatan</b>. Menit yang tertulis adalah saran untuk 90 menit; bagian latihan mandiri paling mudah dipendekkan.",
        "Pakai <b>tiket keluar</b> di akhir pertemuan, lalu bahas jawabannya di awal pertemuan berikutnya.",
        "Setelah Uji Kompetensi, isi tabel <b>Analisis Pengecoh</b> untuk menentukan remedial berdasarkan jenis kesalahan, bukan hanya nilai.",
        "Format modul ajar atau RPP sekolah dapat berbeda. Bagian tujuan, alur, dan asesmen dapat disalin ke format sekolah."]))
    h.append("<h2>Prinsip mengajar bab ini</h2>" + ul([
        "<b>Sketsa dan arah positif dulu.</b> Hampir semua kesalahan vektor berasal dari tanda dan arah. Biasakan siswa menulis \"positif = …\" sebelum menghitung.",
        "<b>Komponen sebagai cara utama.</b> Rumus cosinus hanya untuk dua vektor; cara komponen bekerja untuk berapa pun vektor dan untuk semua soal gerak.",
        "<b>Contoh, lalu contoh bertahap, lalu latihan.</b> Contoh bertahap sengaja dikosongkan sebagian; jangan langsung membacakan kuncinya.",
        "<b>Prediksi sebelum demonstrasi.</b> Minta siswa menulis prediksinya. Miskonsepsi baru terlihat, dan baru bisa diperbaiki, bila prediksi itu ditulis.",
        "<b>Keyakinan bersama jawaban.</b> Jawaban salah yang ditandai \"Yakin\" adalah tanda miskonsepsi, bukan salah hitung; dahulukan itu dalam umpan balik."]))
    h.append("<h2>Konvensi modul</h2><p>Sumbu x positif = timur, sumbu y positif = utara. g = 10 m/s². sin 37° = cos 53° = 0,6 dan cos 37° = sin 53° = 0,8 adalah pembulatan (sudut sebenarnya 36,87° dan 53,13°); setiap soal menuliskan nilai yang dipakai. Desimal ditulis dengan koma.</p>")
    h.append("<h2>Kedudukan dalam kurikulum</h2><p>Vektor dan kinematika termasuk materi Fisika Fase E (kelas X) pada pemetaan CP 2025 yang dipakai repositori ini (Keputusan Kepala BSKAP No. 046/H/KR/2025). Letak gerak parabola dan kecepatan relatif berbeda antarbuku dan antarsekolah (kelas X atau XI). Cocokkan dengan ATP sekolah dan lewati pertemuan yang belum diajarkan.</p></section>")

    # ---------------------------------------------------------------- overview
    h.append('<section class="page"><h1 class="sec">Gambaran Bab dan Alur Pertemuan</h1>')
    h.append("<h2>Tujuan pembelajaran bab</h2><p>Setelah bab ini, peserta didik dapat:</p>" + ol(
        [s["tujuan"] for s in S.SUB] + ["Menjawab soal setara TKA (pilihan ganda, pilihan ganda kompleks, dan benar–salah) tentang vektor dan gerak."]))
    h.append("<h2>Alur delapan pertemuan</h2>" + table(["", "Fokus", "Bagian modul siswa", "Tugas rumah"],
             [[f"<b>{k + 1}</b>", p["judul"], p["bagian"], p["rumah"]] for k, p in enumerate(P)]
             + [["<b>+</b>", C.OPSIONAL["judul"] + " (opsional)", "Halaman interaktif, soal sulit, Soal Setara TKA", "Jadwal Mengulang"]]))
    h.append('<p class="small">Satu pertemuan = 2 JP × 45 menit. Bila sekolah memakai 3 JP per minggu, gabungkan Pertemuan 4 dan 5 menjadi satu pertemuan 3 JP, atau pakai sisa waktu untuk tiket keluar dan remedial.</p>')
    h.append("<h2>Bagaimana bagian modul siswa dipakai</h2>" + table(["Bagian modul siswa", "Dipakai di", "Catatan"], [
        ["Cek Prasyarat dan Kotak Ingat", "Pertemuan 1", "Diagnostik. Hasilnya dicatat di Lembar Rekap (bagian Asesmen)."],
        ["Konsep, Rumus, Contoh", "Penjelasan guru", "Contoh dikerjakan di papan bersama siswa."],
        ["Contoh Bertahap", "Latihan terbimbing, berpasangan", "Kuncinya ada di belakang modul; bahas Cek alasan secara lisan."],
        ["Jebakan", "Akhir penjelasan", "Hubungkan dengan pertanyaan pemantik."],
        ["Latihan (Mudah, Sedang, Sulit)", "Latihan mandiri dan tugas rumah", "Wajib, lanjutan, pengayaan ditunjuk tiap pertemuan."],
        ["Latihan Campuran dan Soal Setara TKA", "Pertemuan 7", "Memilih cara; memeriksa setiap pilihan."],
        ["Uji Kompetensi", "Pertemuan 8", "Sumatif. Kisi-kisi dan rubrik ada di panduan ini."],
        ["Refleksi dan Jadwal Mengulang", "Tugas rumah setelah Pertemuan 8", "Dasar pengelompokan remedial."]]) + "</section>")

    # ---------------------------------------------------------------- materials
    h.append('<section class="page"><h1 class="sec">Persiapan Alat dan Bahan</h1><p>Semua alat murah atau sudah ada di sekolah. Coba setiap demonstrasi sekali sebelum kelas.</p>')
    h.append(table(["Pertemuan", "Alat dan bahan"], [[f"{k + 1}. {p['judul']}", ul(p["persiapan"])] for k, p in enumerate(P)]))
    h.append(box("guru", "Bila waktu atau alat terbatas", ul([
        "Demonstrasi dapat diganti gambar di papan, tetapi tetap minta siswa menulis prediksi lebih dulu.",
        "Kegiatan di halaman (Pertemuan 3) dapat diganti rute di denah sekolah yang digambar di papan.",
        "Halaman interaktif dapat dibuka di ponsel; bila tidak ada koneksi, pakai butir latihan modul cetak yang setara."])))
    h.append("</section>")

    # ---------------------------------------------------------------- meetings
    for k, p in enumerate(P):
        no = k + 1
        h.append(f'<section class="page"><div class="kick">Pertemuan {no} · 2 × 45 menit</div><h1 class="sec">{p["judul"]}</h1>')
        h.append(f'<div class="meta"><b>Bagian modul siswa:</b> {p["bagian"]}</div>')
        h.append("<h2>Tujuan</h2>" + ol(p["tujuan"]))
        h.append(box("konsep", "Persiapan", ul(p["persiapan"])))
        if p["pemantik"]:
            h.append(box("pemantik", "Pertanyaan pemantik", "".join(
                f"<p><b>{q}</b><br><span class='exp'>Jawaban yang diharapkan: {a}</span></p>" for q, a in p["pemantik"])))
        h.append("<h2>Alur kegiatan</h2>" + table(["Menit", "Kegiatan guru", "Kegiatan siswa"],
                 [[m, g, s] for m, g, s in p["alur"]], "alur"))
        if p["latihan"]:
            h.append(f"<p><b>Butir latihan modul siswa.</b> {latihan_text(p)}.</p>")
        if p["miskonsepsi"]:
            h.append(box("jebakan", "Miskonsepsi yang perlu diwaspadai", ul(
                [f"<b>{m}</b> {r}" for m, r in p["miskonsepsi"]])))
        h.append('<div class="diff">' + box("bantu", "Siswa yang perlu bantuan", f"<p>{p['bantuan']}</p>")
                 + box("tantang", "Siswa yang sudah cepat", f"<p>{p['tantangan']}</p>") + "</div>")
        if p["tiket"]:
            h.append(box("tiket", "Tiket keluar (5 menit)", ol(
                [f"{q}<br><span class='kj'>Kunci: {a}</span>" for q, a in p["tiket"]])))
        h.append(f'<p class="meta" style="margin-top:8px"><b>Tugas rumah:</b> {p["rumah"]}</p></section>')

    # ---------------------------------------------------------------- follow-up
    h.append(f'<section class="page"><h1 class="sec">{C.OPSIONAL["judul"]}</h1>' + ul(C.OPSIONAL["isi"]))
    groups = {}
    for no, (sb, _) in C.KISI_PG.items():
        groups.setdefault(sb, []).append(f"PG {no}")
    for no, (sb, *_r) in C.KISI_URAIAN.items():
        groups.setdefault(sb, []).append(f"Uraian {no}")
    h.append("<h2>Dari soal yang salah ke bahan remedial</h2>" + table(
        ["Subbab", "Soal Uji Kompetensi", "Bahan remedial di modul siswa", "Soal ulang"],
        [[f"{sb}. {S.SUB[sb - 1]['title']}", ", ".join(groups[sb]), f"Contoh {sb}.1–{sb}.2, Contoh Bertahap {sb}, kotak Jebakan",
          f"Latihan {sb}.1–{sb}.9 yang belum dikerjakan"] for sb in sorted(groups)]))
    h.append(box("guru", "Catatan", ul([
        "Soal ulang sebaiknya bukan soal yang sama persis dengan Uji Kompetensi; pakai butir latihan yang belum dikerjakan atau halaman interaktif.",
        "Siswa yang salah karena hitungan (bukan konsep) cukup diberi umpan balik tertulis dan satu soal sejenis.",
        "Batas nilai (KKTP) mengikuti ketentuan sekolah."]) ) + "</section>")

    # ---------------------------------------------------------------- misconceptions
    h.append('<section class="page"><h1 class="sec">Katalog Miskonsepsi</h1><p>Miskonsepsi berikut paling sering muncul pada bab ini. Kolom ketiga menunjuk soal di modul siswa yang memunculkannya; pengecoh pada soal pilihan ganda disusun dari kesalahan-kesalahan ini.</p>')
    h.append(table(["Miskonsepsi", "Tampak sebagai", "Terlihat pada soal", "Tanggapan guru"], [list(r) for r in C.MISKONSEPSI]))
    h.append(box("jebakan", "Lima jebakan yang ditulis di Ringkasan Rumus modul siswa", ul([
        "Besar vektor tidak pernah negatif; tanda hanya ada pada komponen.", "3 + 4 = 5 hanya untuk vektor yang saling tegak lurus.",
        "Kelajuan rata-rata memakai jarak; kecepatan rata-rata memakai perpindahan.", "Di titik tertinggi parabola, kecepatan tidak nol (masih ada v<sub>x</sub>).",
        "Kecepatan relatif dihitung dengan mengurangkan vektor, bukan kelajuannya."])) + "</section>")

    # ---------------------------------------------------------------- assessment
    h.append('<section class="page"><h1 class="sec">Asesmen</h1>')
    h.append(table(["Jenis", "Alat", "Kapan", "Tindak lanjut"], [
        ["Diagnostik", "Cek Prasyarat P1–P8", "Awal Pertemuan 1", "Kotak Ingat; kelompok bantuan pada Pertemuan 1–2"],
        ["Formatif", "Tiket keluar, contoh bertahap, kotak keyakinan, kartu A–E", "Setiap pertemuan", "Bahas di awal pertemuan berikutnya"],
        ["Sumatif", f"Uji Kompetensi: {len(S.UJI_PG)} pilihan ganda dan {len(S.UJI_URAIAN)} uraian", "Pertemuan 8", "Analisis pengecoh, remedial, dan pengayaan"]]))
    h.append("<h2>Diagnostik: Lembar Rekap Cek Prasyarat</h2><p>Beri tanda ✗ pada soal yang salah. Kolom Kotak Ingat diisi huruf kotak yang perlu dibaca siswa (A: P1, P4; B: P2–P4; C: P5–P6; D: P7–P8).</p>")
    rows = [[str(r + 1), "", *[""] * 8, ""] for r in range(18)] + [["", "<b>Jumlah salah</b>", *[""] * 8, ""]]
    h.append(table(["", "Nama", *[c for c, *_ in S.PRASYARAT], "Kotak Ingat"], rows, "rekap"))
    h.append("</section>")

    h.append('<section class="page"><h2 style="margin-top:0">Formatif: membaca kotak keyakinan</h2>')
    h.append(table(["", "Benar", "Salah"], [
        ["<b>Yakin</b>", "Sudah kuat.", "<b>Prioritas.</b> Miskonsepsi: bahas di depan kelas dengan pertanyaan pemantik atau demonstrasi ulang."],
        ["<b>Ragu / Menebak</b>", "Belum kuat: beri satu soal sejenis.", "Belum paham: ulangi contoh bertahap bersama guru."]]))
    h.append("<h2>Sumatif: kisi-kisi Uji Kompetensi</h2>")
    h.append(table(["No", "Subbab", "Indikator", "Kunci"],
             [[f"PG {no}", sb, ind, f"{L[UJI[2]]} ({UJI[1][UJI[2]]})"] for (no, (sb, ind)), UJI in zip(sorted(C.KISI_PG.items()), C.UJI_PG)]
             + [[f"Uraian {no}", sb, ind, S.UJI_URAIAN[no - 1][1]] for no, (sb, ind, _) in sorted(C.KISI_URAIAN.items())]))
    h.append(f"<h2>Penskoran</h2><p>Pilihan ganda: {C.SKOR_PG} poin per soal ({len(S.UJI_PG) * C.SKOR_PG} poin). Uraian: {C.SKOR_URAIAN} poin per soal ({len(S.UJI_URAIAN) * C.SKOR_URAIAN} poin). Skor maksimum 50; <b>nilai = skor × 2</b>.</p></section>")

    h.append('<section class="page"><h2 style="margin-top:0">Rubrik uraian</h2>')
    h.append("<p>Pakai rincian poin per soal. Bila jawaban siswa memakai cara lain yang benar, pakai rubrik umum.</p>")
    for no, (sb, ind, parts) in sorted(C.KISI_URAIAN.items()):
        q, a, e = S.UJI_URAIAN[no - 1]
        h.append(f"<p style='margin-top:8px'><b>Uraian {no}.</b> {q}</p>" + table(["Poin", "Kriteria"], [[pt, c] for pt, c in parts]))
    h.append("<h2>Rubrik umum (0–4)</h2>" + table(["Skor", "Deskripsi"], [list(r) for r in C.RUBRIK_UMUM]) + "</section>")

    h.append('<section class="page"><h2 style="margin-top:0">Analisis pengecoh Uji Kompetensi</h2>')
    h.append("<p>Hitung berapa siswa memilih setiap pilihan. Pengecoh yang dipilih banyak siswa menunjukkan kesalahan yang perlu dibahas ulang di kelas. Huruf kunci sama dengan modul siswa versi cetak.</p>")
    h.append(table(["No", "Kunci", "Arti setiap pengecoh", "Jumlah siswa per pilihan (A / B / C / D / E)"],
             [[str(no), f"<b>{L[key]}</b>", sl, ""] for no, (q, opsi, key, e, sl) in enumerate(C.UJI_PG, start=1)]))
    h.append("<h2>Soal setara TKA</h2><p>Untuk pengecoh soal setara TKA (Pertemuan 7), pakai catatan \"Pilihan salah\" di kunci modul siswa.</p></section>")

    # ---------------------------------------------------------------- answer key
    k = ['<section class="page"><h1 class="sec">Kunci Jawaban Ringkas</h1><p>Jawaban akhir saja, untuk memeriksa dengan cepat. Pembahasan lengkap ada di bagian Kunci Jawaban modul siswa.</p><div class="kunci"><h4>Cek Prasyarat</h4>']
    k += [f'<p><b>{c}</b> <span class="k">{a}</span></p>' for c, q, a, e in S.PRASYARAT]
    for n, s in enumerate(S.SUB, start=1):
        k.append(f"<h4>Subbab {n}. {s['title']}</h4><p><b>Contoh Bertahap {n}</b> {s['bertahap']['kunci']}</p>")
        k += [f'<p><b>{n}.{m}</b> <span class="k">{a}</span></p>' for m, (lv, q, a, e) in enumerate(s["latihan"], start=1)]
    k.append("<h4>Latihan Campuran</h4>")
    k += [f'<p><b>C.{m}</b> <span class="k">{a}</span></p>' for m, (lv, q, a, e) in enumerate(S.CAMPURAN, start=1)]
    k.append("<h4>Soal Setara TKA</h4>")
    k += [f'<p><b>T.{m}</b> <span class="k">{key_tka(t)}</span></p>' for m, t in enumerate(C.TKA, start=1)]
    k.append("<h4>Uji Kompetensi: pilihan ganda</h4>")
    k += [f'<p><b>{m}</b> <span class="k">{L[key]}</span> ({opsi[key]})</p>' for m, (q, opsi, key, e, sl) in enumerate(C.UJI_PG, start=1)]
    k.append("<h4>Uji Kompetensi: uraian</h4>")
    k += [f'<p><b>{m}</b> <span class="k">{a}</span></p>' for m, (q, a, e) in enumerate(S.UJI_URAIAN, start=1)]
    k.append("<h4>Tiket keluar</h4>")
    for no, p in enumerate(P, start=1):
        k += [f'<p><b>P{no}.{m}</b> <span class="k">{a}</span></p>' for m, (q, a) in enumerate(p["tiket"], start=1)]
    k.append("</div></section>")
    h += k

    # ---------------------------------------------------------------- notes
    h.append('<section class="page"><h1 class="sec">Catatan dan Sumber</h1>' + box("guru", "Catatan untuk guru", ul([
        "Soal setara TKA di modul siswa meniru tipe soal TKA Fisika SMA 2025 (hitung, grafik/tabel, konsep, analisis, strategi). Soal itu buatan sendiri, bukan soal resmi; tingkat kesulitan sebenarnya dapat berbeda.",
        "Pembagian kelas mengikuti pemetaan CP 2025 di peta materi Fisika repositori ini. Rumusan CP dan ATP resmi tidak dikutip di sini; pakai dokumen sekolah sebagai acuan.",
        "Alokasi menit adalah saran, bukan ketentuan. Jumlah JP Fisika per minggu berbeda antarsekolah.",
        "Simulasi PhET bersifat opsional dan memerlukan internet. Semua kegiatan lain dapat dilakukan tanpa listrik.",
        "Huruf kunci pilihan ganda di panduan ini diambil dari rotasi yang sama dengan modul siswa versi cetak, sehingga keduanya selalu cocok.",
        "Semua jawaban numerik, termasuk tiket keluar dan angka pada pertanyaan pemantik, diperiksa ulang dengan perhitungan komputer."]))
        + "</section>")
    h.append("</body></html>")
    OUT.write_text("".join(h), encoding="utf-8")
    print("pertemuan:", len(P), "tiket:", sum(len(p["tiket"]) for p in P), "soal siswa:", n_siswa)


build()
