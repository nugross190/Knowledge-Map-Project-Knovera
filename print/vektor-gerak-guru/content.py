"""Content of the teacher's guide (Panduan Guru) for the printable module "Vektor dan Gerak".

The guide follows the student module print/vektor-gerak/content.py: lesson plans per meeting, misconceptions,
assessment (blueprint, rubric, distractor analysis) and a compact answer key. Every item it refers to is
looked up in the student content, and check() re-derives every new number (exit tickets, prompts).
"""
import importlib.util
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from kit import balance_keys  # noqa: E402

_spec = importlib.util.spec_from_file_location("print_vektor_gerak_siswa", HERE.parent / "vektor-gerak" / "content.py")
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

# The same rotation as print/vektor-gerak/render.py, so letters here match the student PDF.
TKA, UJI_PG = balance_keys(S.TKA, S.UJI_PG, "Modul Vektor dan Gerak")

V = lambda s: f"<b>{s}</b>"  # noqa: E731
i, j = V("i"), V("j")

MENIT = 90  # one meeting = 2 × 45 minutes

# ------------------------------------------------------------------ references into the student module
# ("L", sub, first, last) = Latihan sub.first–sub.last; ("C", first, last) = Latihan Campuran; ("T", first, last) = Soal setara TKA


def ref(r):
    kind = r[0]
    if kind == "L":
        _, sb, a, b = r
        return f"{sb}.{a}" if a == b else f"{sb}.{a}–{sb}.{b}"
    a, b = r[1], r[2]
    return f"{kind}.{a}" if a == b else f"{kind}.{a}–{kind}.{b}"


def refs(rs):
    return ", ".join(ref(r) for r in rs)


# ------------------------------------------------------------------ meetings
# Each meeting: alur rows are (minutes, teacher, students). Minutes must add up to MENIT.
PERTEMUAN = []

PERTEMUAN.append(dict(
    judul="Cek Prasyarat dan Besaran Vektor",
    bagian="Cek Prasyarat, Kotak Ingat, Subbab 1",
    tujuan=[S.SUB[0]["tujuan"], "Mengenali bekal prasyarat yang belum kuat dan memakai Kotak Ingat yang sesuai."],
    persiapan=["Selotip kertas dan meteran (atau ubin lantai kelas sebagai satuan).",
               "Tanda arah di dinding: TIMUR, UTARA, BARAT, SELATAN (boleh arah kelas, bukan arah kompas sebenarnya).",
               "Lembar Rekap Cek Prasyarat (bagian Asesmen) untuk mencatat hasil kelas."],
    pemantik=[("Saya berjalan 5 langkah dari pintu. Di mana saya sekarang?",
               "Tidak bisa ditentukan tanpa arah. Ini pintu masuk ke perbedaan skalar dan vektor."),
              ("Mana yang lebih jauh dari pintu: berjalan 3 ubin ke timur lalu 4 ubin ke utara, atau 5 ubin lurus?",
               "Sama: posisi akhirnya 5 ubin dari pintu (segitiga 3-4-5). Panjang lintasannya berbeda: 7 ubin dan 5 ubin.")],
    alur=[(15, "Bagikan Cek Prasyarat P1–P8. Siswa mengerjakan sendiri tanpa kalkulator, lalu menukar lembar dan mencocokkan dengan kunci yang dibacakan.",
           "Mengerjakan, mencocokkan, dan menandai nomor yang salah."),
          (5, "Minta siswa mengangkat tangan per nomor yang salah; catat di Lembar Rekap. Arahkan ke Kotak Ingat yang ditunjuk tabel di modul.",
           "Membaca Kotak Ingat yang sesuai dengan nomor yang salah."),
          (15, "Kegiatan lantai: pasang sumbu dengan selotip. Seorang siswa berjalan 3 ubin ke timur lalu 4 ubin ke utara. Tanyakan pemantik kedua, lalu ukur garis lurus dari awal ke akhir.",
           "Memprediksi dulu, lalu mengukur. Menuliskan perpindahan sebagai 3" + i + " + 4" + j + "."),
          (20, "Jelaskan Konsep dan Rumus Subbab 1 dengan Contoh 1.1 dan 1.2. Tekankan: komponen yang bersebelahan dengan sudut memakai cos.",
           "Mencatat dan menjawab pertanyaan singkat guru selama contoh."),
          (10, "Siswa berpasangan mengerjakan Contoh Bertahap 1. Keliling dan dengarkan alasan pada bagian Cek alasan.",
           "Mengisi titik-titik dan memilih alasan (a) atau (b)."),
          (20, "Latihan mandiri. Semua siswa mengerjakan tingkat mudah; yang selesai lanjut ke tingkat sedang.",
           "Mengerjakan Latihan 1, lalu mencocokkan dengan kunci."),
          (5, "Tiket keluar (dua soal di bawah).", "Menjawab di potongan kertas.")],
    latihan=[("Wajib", [("L", 1, 1, 5)]), ("Lanjutan", [("L", 1, 6, 9)]), ("Pengayaan", [("L", 1, 10, 12)])],
    miskonsepsi=[("Besar vektor ditulis negatif, misalnya |−8" + i + " + 6" + j + "| = −10.",
                  "Minta siswa mengukur panjang panah di lantai: panjang tidak pernah negatif. Tanda hanya ada pada komponen."),
                 ("sin dan cos tertukar saat menguraikan.",
                  "Minta siswa menebalkan sisi yang <b>menempel</b> pada sudut; sisi itu selalu memakai cos. Jika sudut diukur dari sumbu y, perannya bertukar."),
                 ("Kelajuan dianggap vektor karena ada kata \"cepat\".",
                  "Kelajuan adalah besar kecepatan. Spidometer menunjukkan kelajuan; ia tidak tahu motor menghadap ke mana.")],
    bantuan="Siswa yang salah pada P1–P4 mengerjakan Kotak Ingat A dan B dulu, lalu hanya Latihan 1.1–1.5. Pakai kertas berpetak untuk menggambar komponen.",
    tantangan="Latihan 1.10–1.12; minta juga siswa menyatakan arah 1.12 dengan arah mata angin dan sudut dari utara.",
    tiket=[(f"Tentukan besar vektor {V('A')} = (−6{i} + 8{j}) m dan kuadran arahnya.", "10 m; kuadran II"),
           ("Kecepatan 30 m/s berarah 37° di atas horizontal (cos 37° = 0,8). Berapa komponen mendatarnya?", "24 m/s")],
    rumah="Halaman interaktif Tahap 1 (Mengenal). Soal yang belum selesai di Latihan 1.",
))

PERTEMUAN.append(dict(
    judul="Penjumlahan dan Selisih Vektor",
    bagian="Subbab 2",
    tujuan=[S.SUB[1]["tujuan"]],
    persiapan=["Dua utas tali sepanjang 30 cm dan 40 cm (atau dua sedotan) untuk menunjukkan batas resultan.",
               "Busur derajat dan penggaris untuk metode grafis.",
               "Kertas berpetak secukupnya."],
    pemantik=[("Vektor 3 satuan dan 4 satuan dijumlahkan. Berapa hasilnya?",
               "Jawaban umum: 5 atau 7. Keduanya benar hanya untuk satu keadaan; resultannya bisa berapa saja dari 1 sampai 7, tergantung sudut apitnya."),
              ("Kapan resultan dua vektor paling besar, dan kapan paling kecil?",
               "Paling besar bila searah (A + B), paling kecil bila berlawanan (|A − B|).")],
    alur=[(10, "Ulas tiket keluar Pertemuan 1. Bahas satu jawaban salah yang paling sering (tanpa menyebut nama).",
           "Memperbaiki jawaban sendiri."),
          (15, "Demonstrasi tali 3 dan 4: sambungkan ujung–pangkal dan ubah sudutnya; minta siswa memperkirakan resultan pada sudut 0°, 90°, dan 180°.",
           "Memprediksi, lalu mengukur resultan dengan penggaris (1, 5, dan 7 satuan)."),
          (20, "Jelaskan cara ujung–pangkal, rumus cosinus (Contoh 2.1), dan cara komponen (Contoh 2.2). Tunjukkan bahwa sudut pada rumus cosinus adalah sudut apit.",
           "Mencatat; membandingkan hasil rumus dengan gambar berskala."),
          (10, "Contoh Bertahap 2 berpasangan. Tanyakan mengapa pilihan (b) menghasilkan 20 km, bukan 10 km.",
           "Mengisi langkah dan memilih alasan."),
          (30, "Latihan mandiri.", "Mengerjakan Latihan 2."),
          (5, "Tiket keluar.", "Menjawab.")],
    latihan=[("Wajib", [("L", 2, 1, 5)]), ("Lanjutan", [("L", 2, 6, 9)]), ("Pengayaan", [("L", 2, 10, 12)])],
    miskonsepsi=[("Besar vektor dijumlahkan langsung: 3 + 4 = 7 untuk sudut berapa pun.",
                  "Kembali ke demonstrasi tali. Minta siswa memeriksa jawabannya dengan batas |A − B| ≤ R ≤ A + B."),
                 ("Sudut pada rumus cosinus diambil dari sumbu x masing-masing vektor.",
                  "Minta siswa menyatukan pangkal kedua vektor dan menandai sudut di antaranya dengan busur sebelum memakai rumus."),
                 ("Selisih vektor dihitung dengan rumus resultan.",
                  "Tulis A − B = A + (−B): balik arah B, lalu jumlahkan. Sudut apit A dan −B adalah 180° − θ, sehingga tandanya berubah menjadi minus.")],
    bantuan="Pakai cara komponen saja (tanpa rumus cosinus) untuk Latihan 2.1–2.5 dan 2.9; gambarkan setiap ruas di kertas berpetak.",
    tantangan="Latihan 2.10–2.12. Tanyakan juga: berapa sudut apit agar resultan dua vektor sama besar F sama dengan F√2?",
    tiket=[("Dua vektor 7 satuan dan 8 satuan membentuk sudut apit 60°. Tentukan besar resultannya.", "13 satuan"),
           ("Mungkinkah resultan vektor 6 satuan dan 9 satuan bernilai 2 satuan? Bernilai 16 satuan? Jelaskan.",
            "Tidak keduanya: resultan hanya mungkin dari 3 sampai 15 satuan.")],
    rumah="Halaman interaktif Tahap 2 (Satu langkah).",
))

PERTEMUAN.append(dict(
    judul="Jarak, Perpindahan, Kelajuan, dan Kecepatan",
    bagian="Subbab 3",
    tujuan=[S.SUB[2]["tujuan"]],
    persiapan=["Stopwatch (ponsel) dan meteran.",
               "Denah sekolah sederhana atau peta digital di proyektor untuk contoh rute."],
    pemantik=[("Pelari mengelilingi lapangan satu putaran penuh. Berapa kecepatan rata-ratanya?",
               "Nol, karena perpindahannya nol. Kelajuan rata-ratanya tidak nol. Biarkan siswa berdebat dulu."),
              ("Aplikasi ojek menulis \"jarak 7 km\". Itu jarak atau perpindahan?",
               "Jarak: panjang rute yang ditempuh, bukan garis lurus dari titik jemput ke tujuan.")],
    alur=[(10, "Ulas tiket keluar Pertemuan 2. Ajukan pemantik pertama dan kumpulkan jawaban tanpa membahasnya.",
           "Menulis jawaban pemantik di buku."),
          (15, "Kegiatan halaman: dua siswa berjalan dari titik A ke titik B, satu lurus dan satu lewat sudut lapangan. Catat waktu dan ukur panjang rute.",
           "Menghitung kelajuan rata-rata dan kecepatan rata-rata kedua siswa, lalu membandingkannya."),
          (20, "Jelaskan posisi, perpindahan, dan dua jenis rata-rata dengan Contoh 3.1 dan 3.2. Kembali ke pemantik pertama.",
           "Merevisi jawaban pemantik."),
          (10, "Contoh Bertahap 3 berpasangan.", "Menghitung Δ" + V("r") + " dari dua vektor posisi."),
          (30, "Latihan mandiri. Ingatkan: waktu berhenti tetap dihitung.", "Mengerjakan Latihan 3."),
          (5, "Tiket keluar.", "Menjawab.")],
    latihan=[("Wajib", [("L", 3, 1, 5)]), ("Lanjutan", [("L", 3, 6, 9)]), ("Pengayaan", [("L", 3, 10, 12)])],
    miskonsepsi=[("Kecepatan rata-rata disamakan dengan kelajuan rata-rata.",
                  "Minta siswa selalu menulis dua baris terpisah: \"jarak = …\" dan \"perpindahan = …\" sebelum membagi dengan waktu."),
                 ("Kecepatan rata-rata pergi–pulang dihitung sebagai rata-rata dua kecepatan.",
                  "Pakai Latihan 3.12: hitung waktu tiap ruas dulu. Hasilnya 48 km/jam, bukan 50 km/jam."),
                 ("Waktu berhenti tidak dihitung.",
                  "Tanyakan: \"Apakah jam tetap berjalan saat kurir berhenti?\" Pakai Latihan 3.10.")],
    bantuan="Sediakan tabel dua kolom (jarak | perpindahan) untuk setiap soal. Mulai dari gerak satu dimensi (3.1–3.3) sebelum dua dimensi.",
    tantangan="Latihan 3.10–3.12, lalu buat soal sendiri dari rute rumah ke sekolah dengan peta digital.",
    tiket=[("Siswa berjalan 5 m ke utara lalu kembali 5 m ke selatan. Tentukan jarak dan perpindahannya.", "Jarak 10 m; perpindahan 0"),
           ("Siswa berjalan 9 m ke timur lalu 12 m ke utara dalam 15 s. Tentukan kelajuan rata-rata dan besar kecepatan rata-ratanya.",
            "1,4 m/s dan 1 m/s")],
    rumah="Halaman interaktif Tahap 3 (Menggabungkan).",
))

PERTEMUAN.append(dict(
    judul="Percepatan dan Lemparan Mendatar",
    bagian="Subbab 4 (bagian pertama: percepatan sebagai vektor, gerak per sumbu, lemparan mendatar)",
    tujuan=["Menghitung percepatan rata-rata sebagai vektor, termasuk pada benda yang berbalik atau berbelok.",
            "Menganalisis lemparan mendatar dengan memisahkan gerak mendatar (GLB) dan tegak (GLBB)."],
    persiapan=["Dua koin dan penggaris untuk demonstrasi \"jatuh bersamaan\".",
               "Bola kecil atau kelereng dan meja untuk mengukur jarak mendarat (opsional)."],
    pemantik=[("Koin X dijatuhkan dan koin Y disentil mendatar dari tepi meja pada saat yang sama. Mana yang lebih dulu menyentuh lantai?",
               "Bersamaan (hambatan udara kecil). Biasanya siswa menebak X lebih dulu. Dengarkan bunyi \"tik\" kedua koin."),
              ("Bola menumbuk dinding 6 m/s dan memantul 6 m/s. Apakah kecepatannya berubah?",
               "Berubah: arahnya berbalik, Δv = 12 m/s. Kelajuannya tetap.")],
    alur=[(10, "Ulas tiket keluar Pertemuan 3. Ajukan pemantik pertama; siswa menuliskan prediksi.",
           "Menulis prediksi dan alasannya."),
          (10, "Demonstrasi dua koin: letakkan penggaris di meja dengan satu ujung menjorok keluar tepi meja. Taruh koin X di atas ujung yang menjorok dan koin Y di meja tepat di depan ujung itu. Tahan bagian tengah penggaris sebagai poros, lalu pukul ujung lainnya mendatar: penggaris berputar, ujungnya menyentil Y keluar meja dan X jatuh lurus. Ulangi tiga kali.",
           "Mendengarkan bunyi, lalu membandingkan dengan prediksi."),
          (20, "Jelaskan percepatan sebagai Δ" + V("v") + "/Δt dengan tanda arah (Contoh 4.2), lalu lemparan mendatar (Contoh 4.1).",
           "Membuat tabel dua kolom: sumbu x (GLB) dan sumbu y (GLBB)."),
          (15, "Kegiatan opsional: gelindingkan kelereng dari tepi meja, ukur tinggi meja dan jarak mendarat, lalu hitung kecepatan kelereng saat meninggalkan meja.",
           "Mengukur h dan x, menghitung t = √(2h/g) lalu v = x/t."),
          (30, "Latihan mandiri.", "Mengerjakan butir Latihan 4 dan Latihan Campuran yang ditunjuk."),
          (5, "Tiket keluar.", "Menjawab.")],
    latihan=[("Wajib", [("L", 4, 1, 2), ("L", 4, 5, 5)]), ("Lanjutan", [("L", 4, 6, 8), ("C", 7, 7)]),
             ("Pengayaan", [("L", 4, 11, 12), ("C", 11, 11)])],
    miskonsepsi=[("Benda yang dilempar mendatar dianggap jatuh lebih lama karena lintasannya lebih panjang.",
                  "Ulangi demonstrasi koin. Waktu jatuh hanya ditentukan gerak tegak, yang sama untuk kedua koin."),
                 ("Percepatan nol bila kelajuan tetap (misalnya mobil berbelok).",
                  "Gambar " + V("v") + "<sub>awal</sub> dan " + V("v") + "<sub>akhir</sub> dengan pangkal disatukan; Δ" + V("v") + " adalah panah dari ujung ke ujung dan tidak nol (Latihan 4.7)."),
                 ("Perubahan kecepatan pada pantulan dihitung sebagai selisih kelajuan.",
                  "Wajibkan siswa menetapkan arah positif dan menulis tanda pada kedua kecepatan (Latihan 4.6).")],
    bantuan="Berikan tabel isian: sumbu x (v<sub>x</sub>, x) dan sumbu y (v<sub>y</sub>, y, t). Mulai dari Latihan 4.2 (jatuh bebas) sebelum 4.8.",
    tantangan="Latihan 4.11, 4.12, dan C.11; minta siswa menjelaskan mengapa kelajuan Y saat mendarat lebih besar daripada X.",
    tiket=[("Bola menggelinding keluar dari tepi meja setinggi 1,25 m dengan kecepatan mendatar 6 m/s (g = 10 m/s²). Berapa lama bola di udara dan seberapa jauh dari kaki meja ia mendarat?",
            "0,5 s; 3 m"),
           ("Benda bergerak 10 m/s ke kanan dengan percepatan tetap 2 m/s² ke kiri. Tentukan kecepatannya setelah 8 s.", "6 m/s ke kiri")],
    rumah="Selesaikan butir Latihan 4 yang ditunjuk.",
))

PERTEMUAN.append(dict(
    judul="Gerak Parabola",
    bagian="Subbab 4 (bagian kedua: gerak parabola, Contoh Bertahap 4)",
    tujuan=["Menganalisis gerak parabola per komponen: waktu ke puncak, tinggi maksimum, jarak mendatar, dan kecepatan pada saat tertentu."],
    persiapan=["Simulasi PhET \"Projectile Motion\" (University of Colorado Boulder, gratis, phet.colorado.edu) di proyektor, jika ada internet.",
               "Tanpa internet: botol semprot atau selang air di halaman untuk menunjukkan bentuk lintasan dan pengaruh sudut."],
    pemantik=[("Di titik tertinggi lintasan bola, berapa kecepatannya?",
               "Jawaban yang sering muncul: nol. Yang benar: v<sub>y</sub> = 0, tetapi v<sub>x</sub> tetap ada."),
              ("Dua bola ditendang dengan kelajuan sama pada sudut 30° dan 60°. Mana yang mendarat lebih jauh?",
               "Sama jauh (hambatan udara diabaikan), karena sin 60° = sin 120°. Yang bersudut 60° lebih lama di udara dan lebih tinggi.")],
    alur=[(10, "Ulas tiket keluar Pertemuan 4. Ajukan kedua pemantik; siswa menulis prediksi.", "Menulis prediksi."),
          (15, "Simulasi atau demonstrasi air: tunjukkan bentuk parabola, lalu bandingkan sudut 30° dan 60° dengan kelajuan sama.",
           "Mencatat jarak mendatar dan tinggi maksimum untuk tiap sudut; membandingkan dengan prediksi."),
          (20, "Jelaskan rumus parabola sebagai gabungan GLB dan GLBB. Turunkan t<sub>puncak</sub> dari v<sub>y</sub> = 0 dan h<sub>maks</sub> dari v<sub>y</sub>² = (v₀ sin α)² − 2gh.",
           "Melengkapi tabel komponen untuk satu tendangan."),
          (10, "Contoh Bertahap 4 berpasangan.", "Menghitung kelajuan 1 s setelah ditendang."),
          (30, "Latihan mandiri.", "Mengerjakan butir Latihan 4 yang ditunjuk."),
          (5, "Tiket keluar.", "Menjawab.")],
    latihan=[("Wajib", [("L", 4, 3, 4)]), ("Lanjutan", [("L", 4, 9, 9), ("C", 10, 10)]), ("Pengayaan", [("L", 4, 10, 10), ("T", 11, 11)])],
    miskonsepsi=[("Kecepatan di titik tertinggi nol.",
                  "Minta siswa menghitung v<sub>x</sub> di puncak dengan angka (Latihan 4.4); hasilnya tidak nol."),
                 ("Sudut lebih besar selalu menghasilkan jarak lebih jauh.",
                  "Bandingkan 30° dan 60° di simulasi; jarak terjauh pada 45° untuk tanah datar."),
                 ("Percepatan bola nol di titik tertinggi.",
                  "Tanyakan: jika percepatan nol di puncak, mengapa bola turun lagi? Percepatannya g ke bawah sepanjang lintasan.")],
    bantuan="Pakai hanya sudut 37° dan 53° dengan nilai sin dan cos yang tertulis; isi tabel komponen setiap 0,5 s untuk melihat v<sub>y</sub> berubah.",
    tantangan="Latihan 4.10 dan Soal Setara TKA T.11. Tantangan lisan: mengapa jarak terjauh dicapai pada 45°?",
    tiket=[("Bola ditendang 10 m/s dengan sudut 53° (sin 53° = 0,8; cos 53° = 0,6; g = 10 m/s²). Tentukan waktu ke puncak, tinggi maksimum, dan kelajuan di puncak.",
            "0,8 s; 3,2 m; 6 m/s"),
           ("Dengan data yang sama, tentukan jarak mendatar bola saat kembali ke tanah.", "9,6 m")],
    rumah="Halaman interaktif Tahap 4, nomor yang tentang gerak parabola.",
))

PERTEMUAN.append(dict(
    judul="Kecepatan Relatif",
    bagian="Subbab 5",
    tujuan=[S.SUB[4]["tujuan"]],
    persiapan=["Selembar kertas panjang (misalnya kertas kado atau sambungan HVS) dan spidol.",
               "Mobil mainan atau tutup botol (opsional)."],
    pemantik=[("Perahu diarahkan tegak lurus tepi sungai yang berarus. Apakah arus membuat perahu lebih lama sampai di seberang?",
               "Tidak. Arus hanya menggeser titik tiba ke hilir; waktu menyeberang ditentukan komponen kecepatan yang tegak lurus tepi."),
              ("Saat berlari di tengah hujan yang turun tegak, ke mana payung harus dimiringkan?",
               "Ke depan, karena menurut pelari hujan datang dari depan.")],
    alur=[(10, "Ulas tiket keluar Pertemuan 5. Ajukan pemantik pertama.", "Menulis prediksi."),
          (15, "Demonstrasi \"sungai kertas\": satu siswa menarik kertas panjang pelan-pelan ke samping (arus); siswa lain menggerakkan spidol lurus menjauh dari dirinya, tegak lurus arah tarikan, dengan laju tetap.",
           "Mengamati bahwa garis pada kertas miring: kecepatan spidol terhadap kertas berbeda dengan terhadap meja."),
          (20, "Jelaskan " + V("v") + "<sub>AB</sub> = " + V("v") + "<sub>A</sub> − " + V("v") + "<sub>B</sub> dan " + V("v") + "<sub>tanah</sub> = " + V("v") + "<sub>relatif</sub> + " + V("v") + "<sub>arus</sub> dengan Contoh 5.1 (sungai) dan 5.2 (hujan).",
           "Menggambar segitiga kecepatan untuk kedua contoh."),
          (10, "Contoh Bertahap 5 berpasangan.", "Menghitung kecepatan kapal terhadap air."),
          (30, "Latihan mandiri.", "Mengerjakan Latihan 5 dan Latihan Campuran yang ditunjuk."),
          (5, "Tiket keluar.", "Menjawab.")],
    latihan=[("Wajib", [("L", 5, 1, 5)]), ("Lanjutan", [("L", 5, 6, 9), ("C", 8, 9)]), ("Pengayaan", [("L", 5, 10, 12), ("C", 12, 12)])],
    miskonsepsi=[("Kecepatan relatif dihitung dengan mengurangkan kelajuan, bukan vektor.",
                  "Untuk gerak berlawanan arah, tulis tanda: 25 − (−20) = 45 m/s. Untuk gerak tegak lurus, gambar segitiganya (Latihan 5.9)."),
                 ("Arus dianggap memperlambat penyeberangan.",
                  "Kembali ke sungai kertas: waktu spidol mencapai sisi seberang tidak bergantung pada kecepatan tarikan."),
                 ("Untuk tiba tepat di seberang, sudut dihitung dengan tan θ = v<sub>arus</sub>/v<sub>perahu</sub>.",
                  "Gambar segitiganya: kecepatan perahu terhadap air adalah sisi miring, jadi yang dipakai sin θ.")],
    bantuan="Mulai dari gerak satu dimensi (Latihan 5.2–5.4) dengan tanda + dan −, baru masuk ke perahu dan pesawat. Sediakan kerangka segitiga kecepatan yang tinggal diberi label.",
    tantangan="Latihan 5.10–5.12 dan C.12. Tantangan lisan: apa yang terjadi bila perahu lebih lambat daripada arus?",
    tiket=[("Sungai selebar 40 m berarus 3 m/s. Perahu 4 m/s relatif terhadap air diarahkan tegak lurus tepi. Tentukan waktu menyeberang, pergeseran ke hilir, dan kelajuan perahu terhadap tepi.",
            "10 s; 30 m; 5 m/s"),
           ("Mobil A (15 m/s) dan mobil B (10 m/s) bergerak berlawanan arah dan akan berpapasan. Berapa kelajuan A menurut B?", "25 m/s")],
    rumah="Halaman interaktif Tahap 4 (Gerak relatif dan dua dimensi), nomor yang tersisa.",
))

PERTEMUAN.append(dict(
    judul="Latihan Campuran dan Soal Setara TKA",
    bagian="Latihan Campuran, Soal Setara TKA",
    tujuan=["Memilih cara yang tepat untuk soal yang dicampur.",
            "Menjawab soal setara TKA (pilihan ganda, pilihan ganda kompleks, benar–salah) dengan memeriksa setiap pilihan."],
    persiapan=["Kartu A–E (atau kertas berlabel) untuk menjawab serentak.",
               "Kotak informasi \"Tentang bagian ini\" pada halaman Soal Setara TKA modul siswa."],
    pemantik=[("Pada soal pilihan ganda, cukupkah berhenti setelah menemukan satu pilihan yang angkanya cocok?",
               "Tidak. Banyak pengecoh benar besarnya tetapi salah arah, sudut, atau waktunya. Periksa semua bagian pernyataan."),
              ("Apa yang harus ditulis lebih dulu sebelum menghitung soal vektor?",
               "Sketsa dan arah positif.")],
    alur=[(10, "Ulas tiket keluar Pertemuan 6. Bahas kebiasaan menjawab: sketsa, arah positif, uraikan per komponen.",
           "Menuliskan tiga langkah itu di pojok halaman."),
          (25, "Latihan Campuran: siswa bekerja sendiri, lalu membandingkan cara dengan teman sebangku sebelum melihat kunci.",
           "Untuk setiap soal, menulis dulu jenisnya: skalar/vektor, jarak/perpindahan, perlu komponen atau tidak."),
          (40, "Soal Setara TKA dengan pola \"pikir–pasang–bagi\": 3 menit sendiri, 2 menit berpasangan, lalu seluruh kelas mengangkat kartu A–E serentak. Untuk pilihan yang banyak dipilih tetapi salah, minta seorang siswa menjelaskan pilihannya, lalu kelas mencari kesalahannya.",
           "Menjawab, menandai keyakinan, dan menuliskan nama kesalahan di samping setiap pengecoh."),
          (10, "Rangkum dua atau tiga pengecoh yang paling banyak dipilih kelas.", "Mencatat di halaman Refleksi."),
          (5, "Tiket keluar.", "Menjawab.")],
    latihan=[("Wajib", [("C", 1, 9)]), ("Lanjutan", [("T", 1, 7)]), ("Pengayaan", [("C", 10, 12), ("T", 8, 13)])],
    miskonsepsi=[("Memilih pilihan pertama yang angkanya cocok.",
                  "Tunjukkan T.8 dan T.12: pilihan yang angkanya benar bisa salah pada bagian kedua pernyataan."),
                 ("Pada soal pilihan ganda kompleks, hanya memilih satu jawaban.",
                  "Ingatkan instruksi \"jawaban benar lebih dari satu\" dan minta siswa menilai setiap pernyataan Benar/Salah satu per satu."),
                 ("Pada soal strategi, berhenti setelah satu syarat terpenuhi (misalnya tiba di tempat yang benar tetapi terlambat).",
                  "Minta siswa menulis daftar syarat (tujuan dan batas waktu) dan mencentang setiap syarat untuk setiap strategi (T.9 dan T.12).")],
    bantuan="Kerjakan Latihan Campuran C.1–C.6 dan T.1, T.6, T.7 bersama guru dengan langkah tertulis di papan.",
    tantangan="Minta siswa menulis satu soal setara TKA sendiri dengan lima pilihan, masing-masing pengecoh berasal dari satu kesalahan yang diberi nama.",
    tiket=[("Pilih satu pengecoh dari Soal Setara TKA yang tadi hampir kamu pilih. Tuliskan kesalahan yang menghasilkan pengecoh itu.",
            "Jawaban terbuka; cocokkan dengan catatan \"Pilihan salah\" di kunci modul siswa."),
           ("Tuliskan tiga langkah yang kamu lakukan sebelum menghitung soal vektor.", "Sketsa, tetapkan arah positif, uraikan per komponen.")],
    rumah="Halaman interaktif Tahap 5 (Setara TKA). Persiapan Uji Kompetensi: baca ulang Ringkasan Rumus dan lima jebakan.",
))

PERTEMUAN.append(dict(
    judul="Uji Kompetensi",
    bagian="Uji Kompetensi, Refleksi dan Jadwal Mengulang",
    tujuan=["Mengukur ketercapaian semua tujuan bab."],
    persiapan=["Lembar Uji Kompetensi (halaman Uji Kompetensi modul siswa, atau salinan terpisah agar siswa tidak membuka kunci).",
               "Kisi-kisi, rubrik uraian, dan tabel analisis pengecoh di bagian Asesmen panduan ini.",
               "Modul siswa menyarankan 90 menit. Satu pertemuan menyisakan sekitar 80 menit; bila perlu, pindahkan dua soal uraian terakhir ke awal pertemuan berikutnya."],
    pemantik=[],
    alur=[(5, "Jelaskan aturan: tanpa membuka bagian lain modul, centang keyakinan setiap soal.", "Menyiapkan alat tulis."),
          (80, "Pengawasan. Catat siswa yang selesai jauh lebih cepat atau lambat.", "Mengerjakan 15 soal pilihan ganda dan 5 soal uraian."),
          (5, "Kumpulkan lembar. Tugaskan halaman Refleksi dan Jadwal Mengulang sebagai pekerjaan rumah.", "Mengumpulkan.")],
    latihan=[],
    miskonsepsi=[],
    bantuan="Siswa dengan kebutuhan khusus boleh diberi waktu tambahan atau mengerjakan uraian secara lisan.",
    tantangan="Siswa yang selesai lebih awal memeriksa ulang soal yang ditandai Ragu.",
    tiket=[],
    rumah="Halaman Refleksi dan Jadwal Mengulang di modul siswa.",
))

OPSIONAL = dict(
    judul="Tindak Lanjut: Remedial dan Pengayaan",
    isi=["Kelompokkan siswa menurut hasil Uji Kompetensi dan tabel analisis pengecoh, bukan hanya menurut nilai.",
         "<b>Kelompok remedial</b> (nilai di bawah KKTP sekolah, atau banyak jawaban salah yang ditandai Yakin): satu pertemuan dengan contoh bertahap ulang dan soal sejenis dari halaman interaktif, lalu tes ulang dengan soal setara.",
         "<b>Kelompok pengayaan</b>: soal tingkat sulit yang belum dikerjakan, Soal Setara TKA T.8–T.13, dan tugas menulis soal setara TKA sendiri.",
         "Gunakan Jadwal Mengulang di modul siswa: ulangan pertama besok, kedua sekitar seminggu kemudian, ketiga sekitar tiga minggu kemudian."],
)

# ------------------------------------------------------------------ misconception catalogue
# (misconception, how it shows up, items that reveal it, response)
MISKONSEPSI = [
    ("Besar vektor bisa negatif.", "Menulis |" + V("v") + "| = −10 m/s.", "1.3, Uji 2", "Besar = panjang panah. Tanda hanya pada komponen."),
    ("Resultan = jumlah besar vektor.", "3 dan 4 selalu menghasilkan 7 (atau selalu 5).", "2.1–2.3, Uji 4–5, T.1", "Demonstrasi tali; batas |A − B| ≤ R ≤ A + B."),
    ("sin dan cos tertukar.", "Komponen tegak dihitung dengan cos untuk sudut dari horizontal.", "1.4–1.5, Uji 3", "Sisi yang menempel pada sudut memakai cos; periksa sudut diukur dari sumbu mana."),
    ("Kelajuan rata-rata = besar kecepatan rata-rata.", "Membagi jarak dengan waktu untuk kecepatan rata-rata.", "3.6, Uji 7, T.5", "Tulis jarak dan perpindahan pada dua baris terpisah."),
    ("Rata-rata kecepatan = rata-rata dua angka kecepatan.", "(60 + 40)/2 = 50 km/jam.", "3.11–3.12", "Hitung waktu tiap ruas, lalu total perpindahan ÷ total waktu."),
    ("Kecepatan tetap bila kelajuan tetap.", "Percepatan nol saat mobil berbelok atau bola memantul.", "4.6–4.7, Uji 14, T.3", "Gambar Δ" + V("v") + " dari ujung " + V("v") + "<sub>awal</sub> ke ujung " + V("v") + "<sub>akhir</sub>."),
    ("Kecepatan di puncak parabola nol.", "Kelajuan di puncak dijawab 0.", "4.4, Uji 10", "Hitung v<sub>x</sub> di puncak dengan angka."),
    ("Benda yang dilempar mendatar jatuh lebih lama.", "Memilih \"bola yang dijatuhkan lebih dulu sampai\".", "4.11, T.13", "Demonstrasi dua koin."),
    ("Arus memperlambat penyeberangan.", "Membagi lebar sungai dengan |v<sub>perahu</sub> − v<sub>arus</sub>|.", "5.6, Uji 12, T.9–T.10", "Sungai kertas: waktu ditentukan komponen tegak lurus tepi."),
    ("Kecepatan relatif = selisih kelajuan.", "Mobil berpapasan 25 dan 20 m/s saling melihat 5 m/s.", "5.4, 5.9, Uji 13", "Tulis kecepatan dengan tanda atau komponen, lalu kurangkan vektornya."),
]

# ------------------------------------------------------------------ Uji Kompetensi blueprint
# PG number -> (sub-chapter, indicator); uraian number -> (sub-chapter, indicator, rubric parts [(points, criterion)])
KISI_PG = {
    1: (1, "Mengelompokkan besaran skalar dan vektor"),
    2: (1, "Menghitung besar vektor dari komponennya"),
    3: (1, "Menguraikan vektor menjadi komponen"),
    4: (2, "Menghitung resultan dua vektor tegak lurus"),
    5: (2, "Menghitung resultan dengan rumus cosinus"),
    6: (3, "Membedakan jarak dan perpindahan pada satu dimensi"),
    7: (3, "Membedakan kelajuan rata-rata dan kecepatan rata-rata"),
    8: (3, "Menghitung perpindahan dari dua vektor posisi"),
    9: (4, "Menerapkan GLBB pada pengereman"),
    10: (4, "Menentukan kelajuan di titik tertinggi parabola"),
    11: (4, "Menganalisis lemparan mendatar"),
    12: (5, "Menganalisis perahu yang menyeberang sungai berarus"),
    13: (5, "Menghitung kecepatan relatif satu dimensi"),
    14: (4, "Menghitung perubahan kecepatan sebagai vektor"),
    15: (5, "Menentukan arah hujan menurut pengamat yang bergerak"),
}
KISI_URAIAN = {
    1: (5, "Menjumlahkan kecepatan pesawat dan angin yang tegak lurus",
        [(1, "Menyusun penjumlahan tegak lurus √(120² + 50²)"), (1, "130 km/jam"), (1, "Mengubah 30 menit menjadi 0,5 jam"), (1, "65 km")]),
    2: (3, "Menghitung perpindahan dan kecepatan rata-rata dari vektor posisi",
        [(1, "Δ" + V("r") + " = (12" + i + " + 5" + j + ") m"), (1, "Besarnya 13 m"), (1, "Kecepatan rata-rata (2,4" + i + " + " + j + ") m/s"), (1, "Besarnya 2,6 m/s")]),
    3: (4, "Menghitung besaran gerak parabola",
        [(1, "Komponen v<sub>y</sub> = 18 m/s dan t<sub>puncak</sub> = 1,8 s"), (1, "h<sub>maks</sub> = 16,2 m"), (1, "Waktu di udara 3,6 s atau rumus R yang benar"), (1, "R = 86,4 m")]),
    4: (5, "Merancang arah perahu dan membandingkan dua cara menyeberang",
        [(1, "Arah 53° ke hulu dari garis tegak lurus tepi"), (1, "40 s"), (1, "Cara tercepat 24 s"), (1, "Terbawa 96 m")]),
    5: (5, "Menghitung kecepatan relatif dua dimensi",
        [(1, "Menyusun " + V("v") + "<sub>AB</sub> = (−12, 16) m/s"), (1, "20 m/s"), (1, "Memakai kecepatan relatif × waktu, atau posisi masing-masing setelah 10 s"), (1, "200 m")]),
}
SKOR_PG, SKOR_URAIAN = 2, 4  # points per item; total = 15·2 + 5·4 = 50, grade = 2 × score

RUBRIK_UMUM = [
    ("4", "Sketsa atau arah positif jelas, cara benar, hasil benar dengan satuan dan arah."),
    ("3", "Cara benar, tetapi ada satu salah hitung atau satuan/arah tidak ditulis."),
    ("2", "Sebagian cara benar (misalnya hanya satu dari dua pertanyaan), atau konsep benar dengan salah hitung berulang."),
    ("1", "Hanya menuliskan besaran yang diketahui atau sketsa yang relevan."),
    ("0", "Kosong atau tidak relevan."),
]

# ------------------------------------------------------------------ new numbers in this guide, re-derived in check()


def check():
    h, s = math.hypot, math.sqrt

    def close(a, b, t=1e-6):
        assert abs(a - b) <= t, (a, b)

    assert S.check()
    # meeting arithmetic and references
    for p in PERTEMUAN:
        assert sum(m for m, *_ in p["alur"]) == MENIT, p["judul"]
        for _, rs in p["latihan"]:
            for r in rs:
                if r[0] == "L":
                    assert 1 <= r[2] <= r[3] <= len(S.SUB[r[1] - 1]["latihan"]), r
                else:
                    assert 1 <= r[1] <= r[2] <= len({"C": S.CAMPURAN, "T": S.TKA}[r[0]]), r
    assert set(KISI_PG) == set(range(1, len(S.UJI_PG) + 1)) and set(KISI_URAIAN) == set(range(1, len(S.UJI_URAIAN) + 1))
    assert all(sum(p for p, _ in parts) == SKOR_URAIAN for _, _, parts in KISI_URAIAN.values())
    assert len(S.UJI_PG) * SKOR_PG + len(S.UJI_URAIAN) * SKOR_URAIAN == 50
    # prompts: 3-4-5 floor walk; rope demo limits for 3 and 4
    close(h(3, 4), 5); assert (4 - 3, 4 + 3) == (1, 7)
    # P1 exit ticket
    close(h(-6, 8), 10); close(30 * 0.8, 24)
    # P2 exit ticket
    close(s(7 ** 2 + 8 ** 2 + 2 * 7 * 8 * 0.5), 13); assert (9 - 6, 9 + 6) == (3, 15)
    # P2 challenge: two equal vectors F with resultant F·√2 -> 90°
    close(math.degrees(math.acos((2 - 2) / 2)), 90)
    # P3 exit ticket
    assert (5 + 5, 5 - 5) == (10, 0)
    close((9 + 12) / 15, 1.4); close(h(9, 12) / 15, 1)
    # P4 exit ticket
    t = s(2 * 1.25 / 10); close(t, 0.5); close(6 * t, 3)
    close(10 - 2 * 8, -6)
    # P5 exit ticket (v0 = 10 m/s, 53°)
    vx, vy = 10 * 0.6, 10 * 0.8
    close(vy / 10, 0.8); close(vy ** 2 / 20, 3.2); close(vx, 6)
    close(10 ** 2 * (2 * 0.8 * 0.6) / 10, 9.6); close(vx * 2 * vy / 10, 9.6)
    # P5 prompt: 30° and 60° land equally far
    close(math.sin(math.radians(60)), math.sin(math.radians(120)))
    # P6 exit ticket
    close(40 / 4, 10); close(3 * 10, 30); close(h(4, 3), 5); close(15 - (-10), 25)
    # P3 note on Latihan 3.12: 48 km/jam, not 50
    close(240 / (120 / 60 + 120 / 40), 48)
    return True
