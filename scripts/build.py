"""Validate the question bank and build the static pages in docs/.

Usage:  python scripts/build.py              # build docs/ for GitHub Pages
        python scripts/build.py --artifact   # also write build/*.fragment.html for the claude.ai copies
Reads:  data/topics.json, data/questions.csv, data/maps/*.json, data/tka/*.json, data/modules/*.json,
        data/tka-types.json, templates/*.html
Writes: docs/questions.json, one docs/<name>.html per template (docs/tka.html carries the TKA banks),
        one docs/peta-<id>.html per subject map (rendered through templates/_map.html),
        one docs/modul-<id>.html per learning module (rendered through templates/_modul.html),
        and docs/modul-<id>.pdf for every printable module in print/<id>.pdf
Exits with status 1 (and writes nothing) if the data has errors.
"""
import csv
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["id", "simpul", "tingkat", "soal", "jawaban", "catatan"]
MIN_PER_TOPIC = 5
HEAD = ('<!doctype html>\n<html lang="id">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}</style>\n')
# The hosted claude.ai copies link to each other by URL instead of by file name.
ARTIFACT_URLS = {
    "peta.html": "https://claude.ai/artifact/D5VQvyvvDqr9rVwHTMX3eP",
    "bank.html": "https://claude.ai/artifact/Qs1xt8ZCrkrKMiHbq2BGFg",
    "simulasi.html": "https://claude.ai/artifact/VfVV7k9nBakQALRRybY526",
    "peta-fisika.html": "https://claude.ai/artifact/XxSteiwD99sQx37T8teYTh",
}
# Pages without a hosted copy are linked through the GitHub Pages site.
PAGES_URL = "https://nugross190.github.io/Bank-LCCM-Sejarah/"
HOSTED_LINKS = {**ARTIFACT_URLS, "index.html": PAGES_URL}
# Path of the site under github.io ("/Bank-LCCM-Sejarah/"), for pages that need absolute links (404.html).
SITE_BASE = urlparse(PAGES_URL).path


def load():
    topics = json.loads((ROOT / "data/topics.json").read_text(encoding="utf-8"))
    with open(ROOT / "data/questions.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            sys.exit(f"questions.csv header must be exactly: {','.join(FIELDS)}\nfound: {reader.fieldnames}")
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    return topics, rows


def validate(topics, rows):
    codes = {code for d in topics["domains"] for code in d["topics"]}
    errors, seen_ids, seen_q = [], set(), {}
    for n, r in enumerate(rows, start=2):  # line 1 is the header
        where = f"line {n} ({r['id'] or 'no id'})"
        if not r["id"]:
            errors.append(f"{where}: id is empty")
        elif r["id"] in seen_ids:
            errors.append(f"{where}: duplicate id")
        seen_ids.add(r["id"])
        if r["simpul"] not in codes:
            errors.append(f"{where}: unknown simpul '{r['simpul']}'")
        elif not r["id"].startswith(r["simpul"] + "-"):
            errors.append(f"{where}: id must start with its simpul ({r['simpul']}-)")
        if r["tingkat"] not in {"1", "2", "3"}:
            errors.append(f"{where}: tingkat must be 1, 2 or 3")
        if not r["soal"] or not r["jawaban"]:
            errors.append(f"{where}: soal and jawaban are required")
        key = r["soal"].lower()
        if key in seen_q:
            errors.append(f"{where}: same question as {seen_q[key]}")
        seen_q[key] = r["id"]
    return errors


def report(topics, rows):
    per_topic = Counter(r["simpul"] for r in rows)
    for d in topics["domains"]:
        total = sum(per_topic[c] for c in d["topics"])
        print(f"{d['id']}  {total:4d} soal  (bobot {d['weight']}%)")
        for code, title in d["topics"].items():
            flag = "  <- sedikit" if per_topic[code] < MIN_PER_TOPIC else ""
            print(f"   {code}  {per_topic[code]:3d}  {title}{flag}")
    print(f"Total {len(rows)} soal")


def load_maps():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/maps").glob("*.json"))}


def validate_map(name, m):
    """Return a list of problems in one subject map."""
    errors, codes = [], set()
    where = f"data/maps/{name}.json"
    for key in ("id", "subject", "title", "lead", "domains"):
        if not m.get(key):
            errors.append(f"{where}: missing '{key}'")
    if m.get("id") and m["id"] != name:
        errors.append(f"{where}: id '{m['id']}' must match the file name")
    for d in m.get("domains", []):
        for key in ("id", "name", "short", "topics"):
            if not d.get(key):
                errors.append(f"{where}: domain {d.get('id', '?')} missing '{key}'")
        for t in d.get("topics", []):
            code = t.get("code", "?")
            if code in codes:
                errors.append(f"{where}: duplicate code {code}")
            codes.add(code)
            if not code.startswith(d.get("id", "") + "-"):
                errors.append(f"{where}: {code} must start with its domain id ({d.get('id')}-)")
            for key in ("title", "scope", "src", "sum", "blocks"):
                if not t.get(key):
                    errors.append(f"{where}: {code} missing '{key}'")
            if t.get("tier") not in (1, 2, 3):
                errors.append(f"{where}: {code} tier must be 1, 2 or 3")
            for b in t.get("blocks", []):
                if not b.get("h") or not (b.get("li") or b.get("table")):
                    errors.append(f"{where}: {code} has a block without a heading or content")
                table = b.get("table")
                if table and any(len(r) != len(table["cols"]) for r in table["rows"]):
                    errors.append(f"{where}: {code} table '{b.get('h')}' has rows of the wrong length")
    for step in m.get("path", []):
        if step.get("to") not in codes:
            errors.append(f"{where}: path step '{step.get('title')}' points to unknown code {step.get('to')}")
    return errors


def load_tka():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/tka").glob("*.json"))}


TKA_FORMATS = {"pilihan-ganda", "pilihan-ganda-kompleks", "benar-salah"}
TKA_CONFIDENCE = {"tinggi", "sedang", "rendah", "tidak ada"}
TKA_ITEM_FIELDS = ("id", "nomor", "format", "kompetensi", "indikator", "soal", "opsi", "status_kunci",
                   "keyakinan_kunci", "alasan", "halaman")


def validate_tka(name, bank):
    """Return a list of problems in one TKA item bank (format: specs/tka-spec.md)."""
    errors = []
    where = f"data/tka/{name}.json"
    for key in ("id", "kode", "mapel", "ujian", "sumber", "soal"):
        if not bank.get(key):
            errors.append(f"{where}: missing '{key}'")
    if bank.get("id") and bank["id"] != name:
        errors.append(f"{where}: id '{bank['id']}' must match the file name")
    kode = bank.get("kode", "")
    if kode and not re.fullmatch(r"[A-Z]+[0-9]*", kode):
        errors.append(f"{where}: kode '{kode}' must be uppercase letters, then digits")
    for key in ("catatan", "teks"):
        if not isinstance(bank.get(key, []), list):
            errors.append(f"{where}: '{key}' must be a list")
    passages = set()
    for t in bank.get("teks", []):
        if not t.get("id") or t["id"] in passages:
            errors.append(f"{where}: teks entry with an empty or duplicate id ({t.get('id')})")
        if not isinstance(t.get("teks"), str) or not t["teks"].strip():
            errors.append(f"{where}: teks entry {t.get('id')} has no text in 'teks'")
        passages.add(t.get("id"))
    seen = set()
    for it in bank.get("soal", []):
        sid = it.get("id", "?")
        for key in TKA_ITEM_FIELDS:
            if key not in it:
                errors.append(f"{where}: {sid} missing '{key}'")
        if not re.fullmatch(re.escape(kode) + r"-\d{3}[A-C]?", sid):
            errors.append(f"{where}: {sid} must look like {kode}-NNN (optional A/B/C suffix)")
        if sid in seen:
            errors.append(f"{where}: duplicate id {sid}")
        seen.add(sid)
        if it.get("passage") is not None and it["passage"] not in passages:
            errors.append(f"{where}: {sid} refers to unknown teks '{it['passage']}'")
        fmt, opsi, kunci = it.get("format"), it.get("opsi", []), it.get("kunci")
        if fmt not in TKA_FORMATS:
            errors.append(f"{where}: {sid} format must be one of {', '.join(sorted(TKA_FORMATS))}")
        if it.get("keyakinan_kunci") not in TKA_CONFIDENCE:
            errors.append(f"{where}: {sid} keyakinan_kunci must be one of {', '.join(sorted(TKA_CONFIDENCE))}")
        if not isinstance(opsi, list) or len(opsi) < 2 or not all(isinstance(o, str) and o.strip() for o in opsi):
            errors.append(f"{where}: {sid} needs at least two non-empty options")
            continue
        n = len(opsi)
        if kunci is None:
            if it.get("keyakinan_kunci") != "tidak ada":
                errors.append(f"{where}: {sid} has no kunci, so keyakinan_kunci must be 'tidak ada'")
        elif fmt == "pilihan-ganda":
            if type(kunci) is not int or not 0 <= kunci < n:
                errors.append(f"{where}: {sid} kunci must be the index of one option")
        elif fmt == "pilihan-ganda-kompleks":
            if (not isinstance(kunci, list) or not kunci or kunci != sorted(set(kunci))
                    or not all(type(k) is int and 0 <= k < n for k in kunci)):
                errors.append(f"{where}: {sid} kunci must be a sorted list of option indexes")
        elif fmt == "benar-salah":
            if not isinstance(kunci, list) or len(kunci) != n or not all(isinstance(k, bool) for k in kunci):
                errors.append(f"{where}: {sid} kunci must be one true/false per statement")
        if fmt == "benar-salah" and not (isinstance(it.get("kolom"), list) and len(it["kolom"]) == 2):
            errors.append(f"{where}: {sid} benar-salah needs 'kolom' with two headings")
        text = it.get("soal", "") + " ".join(opsi)
        if "[Gambar]" in text and not it.get("gambar"):
            errors.append(f"{where}: {sid} has a [Gambar] marker but no 'gambar' description")
        table = it.get("tabel")
        if "[Tabel]" in it.get("soal", "") and not table:
            errors.append(f"{where}: {sid} has a [Tabel] marker but no 'tabel'")
        if table is not None and not (isinstance(table, list) and table
                                      and all(isinstance(r, list) and all(isinstance(c, str) for c in r) for r in table)):
            errors.append(f"{where}: {sid} tabel must be a list of rows of strings")
        if not (isinstance(it.get("halaman"), list) and it["halaman"] and all(type(h) is int for h in it["halaman"])):
            errors.append(f"{where}: {sid} halaman must be a non-empty list of page numbers")
    return errors


def load_modules():
    folder = ROOT / "data/modules"
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(folder.glob("*.json"))}


def load_tka_types():
    """{type code: type entry} from data/tka-types.json, across all subjects."""
    types = json.loads((ROOT / "data/tka-types.json").read_text(encoding="utf-8"))
    return {t["kode"]: t for s in types.values() for t in s["types"]}


MODULE_FORMATS = TKA_FORMATS | {"isian"}
MODULE_BLOCKS = ("p", "li", "tabel", "contoh", "svg", "jebakan")


def validate_module(name, mod, maps, tka_types):
    """Return a list of problems in one learning module (format: specs/module-spec.md)."""
    errors = []
    where = f"data/modules/{name}.json"
    for key in ("id", "kode", "subject", "title", "lead", "materi", "tahap"):
        if not mod.get(key):
            errors.append(f"{where}: missing '{key}'")
    if mod.get("id") and mod["id"] != name:
        errors.append(f"{where}: id '{mod['id']}' must match the file name")
    kode = mod.get("kode", "")
    if kode and not re.fullmatch(r"[A-Z]{2,5}", kode):
        errors.append(f"{where}: kode '{kode}' must be 2-5 uppercase letters")
    codes = None
    if mod.get("map"):
        if mod["map"] not in maps:
            errors.append(f"{where}: map '{mod['map']}' is not a file in data/maps/")
        else:
            codes = {t["code"] for d in maps[mod["map"]]["domains"] for t in d["topics"]}

    def check_code(code, owner):
        if codes is not None and code not in codes:
            errors.append(f"{where}: {owner} refers to unknown topic {code} in map '{mod['map']}'")

    lessons = set()
    for les in mod.get("materi", []):
        lid = les.get("id", "?")
        if lid in lessons:
            errors.append(f"{where}: duplicate materi id {lid}")
        lessons.add(lid)
        if not les.get("judul") or not les.get("isi"):
            errors.append(f"{where}: materi {lid} needs 'judul' and 'isi'")
        for code in les.get("simpul", []):
            check_code(code, f"materi {lid}")
        for blk in les.get("isi", []):
            kinds = [k for k in MODULE_BLOCKS if k in blk]
            if len(kinds) != 1:
                errors.append(f"{where}: materi {lid} has a block that is not exactly one of {', '.join(MODULE_BLOCKS)}")
                continue
            kind, val = kinds[0], blk[kinds[0]]
            if kind in ("li", "jebakan") and not (isinstance(val, list) and val):
                errors.append(f"{where}: materi {lid} '{kind}' must be a non-empty list")
            if kind == "tabel" and (not val.get("cols") or any(len(r) != len(val["cols"]) for r in val.get("rows", []))):
                errors.append(f"{where}: materi {lid} table has rows of the wrong length")
            if kind == "contoh" and not (val.get("soal") and val.get("langkah")):
                errors.append(f"{where}: materi {lid} contoh needs 'soal' and 'langkah'")
            if kind == "svg" and not (isinstance(val, str) and val.startswith("<svg") and val.endswith("</svg>")):
                errors.append(f"{where}: materi {lid} svg must be one <svg>...</svg> element")

    seen = set()
    for n, stage in enumerate(mod.get("tahap", []), start=1):
        if stage.get("tahap") != n:
            errors.append(f"{where}: stages must be numbered 1, 2, 3, ... in order (found {stage.get('tahap')} at {n})")
        if not stage.get("nama") or not stage.get("soal"):
            errors.append(f"{where}: stage {n} needs 'nama' and 'soal'")
        for it in stage.get("soal", []):
            sid = it.get("id", "?")
            if not re.fullmatch(re.escape(kode) + r"-\d{3}", sid):
                errors.append(f"{where}: {sid} must look like {kode}-NNN")
            if sid in seen:
                errors.append(f"{where}: duplicate id {sid}")
            seen.add(sid)
            for key in ("soal", "petunjuk"):
                if not it.get(key):
                    errors.append(f"{where}: {sid} missing '{key}'")
            if not (isinstance(it.get("pembahasan"), list) and it["pembahasan"]):
                errors.append(f"{where}: {sid} needs 'pembahasan' as a non-empty list of steps")
            if it.get("simpul"):
                check_code(it["simpul"], sid)
            if "[Tabel]" in it.get("soal", "") and not it.get("tabel"):
                errors.append(f"{where}: {sid} has a [Tabel] marker but no 'tabel'")
            fmt, kunci, opsi = it.get("format"), it.get("kunci"), it.get("opsi")
            if fmt not in MODULE_FORMATS:
                errors.append(f"{where}: {sid} format must be one of {', '.join(sorted(MODULE_FORMATS))}")
                continue
            if fmt == "isian":
                if type(kunci) not in (int, float) or not it.get("satuan"):
                    errors.append(f"{where}: {sid} isian needs a numeric 'kunci' and a 'satuan'")
                if "toleransi" in it and not (type(it["toleransi"]) in (int, float) and it["toleransi"] > 0):
                    errors.append(f"{where}: {sid} toleransi must be a positive number")
            else:
                if not isinstance(opsi, list) or len(opsi) < 2 or not all(isinstance(o, str) and o.strip() for o in opsi):
                    errors.append(f"{where}: {sid} needs at least two non-empty options")
                    continue
                k = len(opsi)
                if fmt == "pilihan-ganda" and not (type(kunci) is int and 0 <= kunci < k):
                    errors.append(f"{where}: {sid} kunci must be the index of one option")
                if fmt == "pilihan-ganda-kompleks" and not (
                        isinstance(kunci, list) and kunci and kunci == sorted(set(kunci))
                        and all(type(x) is int and 0 <= x < k for x in kunci)):
                    errors.append(f"{where}: {sid} kunci must be a sorted list of option indexes")
                if fmt == "benar-salah":
                    if not (isinstance(kunci, list) and len(kunci) == k and all(isinstance(x, bool) for x in kunci)):
                        errors.append(f"{where}: {sid} kunci must be one true/false per statement")
                    if not (isinstance(it.get("kolom"), list) and len(it["kolom"]) == 2):
                        errors.append(f"{where}: {sid} benar-salah needs 'kolom' with two headings")
            if "tka" in it:
                t = tka_types.get(it["tka"].get("tipe"))
                if not t:
                    errors.append(f"{where}: {sid} unknown TKA tipe '{it['tka'].get('tipe')}'")
                    continue
                if fmt not in t["format"]:
                    errors.append(f"{where}: {sid} format {fmt} not allowed for {t['kode']}")
                acuan = it["tka"].get("acuan", [])
                if not acuan or not set(acuan) <= set(t["contoh"]):
                    errors.append(f"{where}: {sid} acuan must list transcribed examples of {t['kode']}")
    return errors


def lint_module(name, mod):
    """Return warnings for soft rules in specs/module-spec.md. They do not stop the build."""
    warnings, where = [], f"data/modules/{name}.json"
    stages = mod.get("tahap", [])
    if len(stages) < 3:
        warnings.append(f"{where}: {len(stages)} stages (spec: at least 3)")
    for st in stages:
        if len(st.get("soal", [])) < 4:
            warnings.append(f"{where}: stage {st.get('tahap')} has {len(st.get('soal', []))} items (spec: at least 4)")
    if not any("tka" in it for st in stages for it in st.get("soal", [])):
        warnings.append(f"{where}: no TKA-style items")
    if not mod.get("blurb"):
        warnings.append(f"{where}: no 'blurb' for the home-page card")
    return warnings


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def lint_map(name, m):
    """Return warnings for soft rules in specs/map-spec.md (sizes, tier mix, traps). They do not stop the build."""
    warnings, where = [], f"data/maps/{name}.json"
    domains = m.get("domains", [])
    topics = [t for d in domains for t in d.get("topics", [])]
    if not 3 <= len(domains) <= 8:
        warnings.append(f"{where}: {len(domains)} domains (spec: 3-8)")
    if not 20 <= len(topics) <= 35:
        warnings.append(f"{where}: {len(topics)} topics (spec: 20-35)")
    for d in domains:
        if not 2 <= len(d.get("topics", [])) <= 10:
            warnings.append(f"{where}: domain {d.get('id')} has {len(d.get('topics', []))} topics (spec: 2-10)")
    if topics:
        share = {k: sum(t.get("tier") == k for t in topics) / len(topics) for k in (1, 2, 3)}
        if not (0.5 <= share[1] <= 0.7 and 0.2 <= share[2] <= 0.4 and share[3] <= 0.15):
            mix = ", ".join(f"tier {k} {share[k]:.0%}" for k in (1, 2, 3))
            warnings.append(f"{where}: tier mix {mix} (spec: 50-70% / 20-40% / <=15%)")
    if not m.get("blurb"):
        warnings.append(f"{where}: no 'blurb' for the home-page card")
    elif words(m["blurb"]) > 25:
        warnings.append(f"{where}: blurb has {words(m['blurb'])} words (spec: <=25)")
    for t in topics:
        code = t.get("code", "?")
        if words(t.get("sum", "")) > 30:
            warnings.append(f"{where}: {code} summary has {words(t['sum'])} words (spec: <=30)")
        if t.get("tier") == 1 and not t.get("traps"):
            warnings.append(f"{where}: {code} is tier 1 but has no traps")
        if len(t.get("blocks", [])) > 5:
            warnings.append(f"{where}: {code} has {len(t['blocks'])} blocks (spec: <=5)")
        for b in t.get("blocks", []):
            items = b.get("li", [])
            if len(items) > 8:
                warnings.append(f"{where}: {code} block '{b.get('h')}' has {len(items)} bullets (spec: <=8)")
            for item in items + t.get("traps", []):
                if words(item) > 35:
                    warnings.append(f"{where}: {code} bullet over 35 words: '{re.sub(r'<[^>]+>', '', item)[:50]}...'")
                if item.count("<b>") > 1:
                    warnings.append(f"{where}: {code} bullet with more than one bold: '{re.sub(r'<[^>]+>', '', item)[:50]}...'")
    return warnings


def map_pages(maps, links):
    """Return {file name: page body} for every subject map."""
    template = (ROOT / "templates/_map.html").read_text(encoding="utf-8")
    out = {}
    for m in maps.values():
        payload = json.dumps(m, ensure_ascii=False).replace("</", "<\\/")
        body = template.replace("__TITLE__", m["title"]).replace("/*__MAP__*/", "const MAP = " + payload + ";")
        for name, target in links.items():
            body = body.replace('href="' + name, 'href="' + target)
        out[f"peta-{m['id']}.html"] = body
    return out


def module_pdf(mod_id):
    """Path of a module's printable PDF (print/<id>.pdf, made by print/print.mjs), or None."""
    path = ROOT / "print" / f"{mod_id}.pdf"
    return path if path.exists() else None


def module_pages(modules, maps, links):
    """Return {file name: page body} for every learning module."""
    template = (ROOT / "templates/_modul.html").read_text(encoding="utf-8")
    out = {}
    for mod in modules.values():
        data = dict(mod)
        if module_pdf(mod["id"]):
            # Hosted copies have no PDF next to them, so they link to the one on GitHub Pages.
            data["pdf"] = (PAGES_URL if links else "") + f"modul-{mod['id']}.pdf"
        if mod.get("map") in maps:
            m = maps[mod["map"]]
            data["map_page"] = links.get(f"peta-{m['id']}.html", f"peta-{m['id']}.html")
            data["map_title"] = m["title"]
            data["topics"] = {t["code"]: t["title"] for d in m["domains"] for t in d["topics"]}
        payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        body = template.replace("__TITLE__", mod["title"]).replace("/*__MODULE__*/", "const MOD = " + payload + ";")
        for name, target in links.items():
            body = body.replace('href="' + name, 'href="' + target)
        out[f"modul-{mod['id']}.html"] = body
    return out


def subject_cards(maps, topics, n_questions, tka=None, modules=None):
    """HTML cards for the home page: the history kit, one card per subject map (with its modules), then the TKA banks."""
    e = html.escape
    sni = topics["domains"]
    n_topics = sum(len(d["topics"]) for d in sni)
    cards = [
        '<article class="subject" style="--c:var(--c-sejarah, var(--c-default))">'
        '<span class="kind">Lomba LCCM · ' + str(n_topics) + ' simpul · ' + str(n_questions) + ' soal</span>'
        '<h2>Kit Lomba Sejarah</h2>'
        '<p>Perangkat lomba bergaya Lomba Cerdas Cermat Museum: sejarah nasional, kebudayaan, serta permuseuman dan cagar budaya.</p>'
        '<div class="chips">' + "".join(f'<span>{e(d["short"])} {d["weight"]}%</span>' for d in sni) + '</div>'
        '<nav class="links" aria-label="Sejarah">'
        '<a class="primary" href="peta.html">Peta materi <span>praaksara–Reformasi</span></a>'
        '<a href="bank.html">Bank soal <span>latihan per simpul</span></a>'
        '<a href="simulasi.html">Simulasi babak <span>wajib dan rebutan</span></a>'
        '</nav></article>'
    ]
    for m in maps.values():
        n = sum(len(d["topics"]) for d in m["domains"])
        blurb = m.get("blurb") or ", ".join(d["name"] for d in m["domains"]) + "."
        cards.append(
            f'<article class="subject" style="--c:var(--c-{e(m["id"])}, var(--c-default))">'
            f'<span class="kind">{e(m["subject"])} · {n} simpul</span>'
            f'<h2>{e(m["subject"])}</h2>'
            f'<p>{e(blurb)}</p>'
            '<div class="chips">' + "".join(f'<span>{e(d["short"])}</span>' for d in m["domains"]) + '</div>'
            f'<nav class="links" aria-label="{e(m["subject"])}">'
            f'<a class="primary" href="peta-{e(m["id"])}.html">Peta materi <span>{n} simpul</span></a>'
            + "".join(f'<a href="modul-{e(mod["id"])}.html">{e(mod["title"])} '
                      f'<span>{sum(len(st["soal"]) for st in mod["tahap"])} latihan</span></a>'
                      for mod in (modules or {}).values() if mod.get("map") == m["id"])
            + '</nav></article>'
        )
    if tka:
        n_items = sum(len(b["soal"]) for b in tka.values())
        cards.append(
            '<article class="subject" style="--c:var(--c-tka, var(--c-default))">'
            f'<span class="kind">TKA 2025 · {len(tka)} mapel · {n_items} soal</span>'
            '<h2>Latihan TKA</h2>'
            '<p>Soal Tes Kemampuan Akademik SMA 2025 yang ditranskripsi dari berkas soal, dengan kunci usulan yang belum resmi.</p>'
            '<div class="chips">' + "".join(f'<span>{e(b["mapel"])}</span>' for b in tka.values()) + '</div>'
            '<nav class="links" aria-label="Latihan TKA">'
            '<a class="primary" href="tka.html">Latihan soal <span>pilih mapel</span></a>'
            '</nav></article>'
        )
    return "\n    ".join(cards)


def pages(topics, questions, links, maps=None, tka=None, modules=None):
    """Return {file name: page body} for every template, with cross-page links resolved through `links`.

    A template that contains /*__DATA__*/ gets the topics and questions injected there,
    and one that contains /*__TKA__*/ gets the TKA banks.
    Every href="<page>.html" that names a page in `links` is rewritten to its target.
    """
    data = dict(topics, map_url=links.get("peta.html", "peta.html"))
    payload = json.dumps({"topics": data, "questions": questions}, ensure_ascii=False).replace("</", "<\\/")
    tka = tka if tka is not None else load_tka()
    tka_payload = json.dumps(list(tka.values()), ensure_ascii=False).replace("</", "<\\/")
    out = {}
    for path in sorted((ROOT / "templates").glob("*.html")):
        if path.name.startswith("_"):  # shared templates, rendered by other steps
            continue
        body = path.read_text(encoding="utf-8")
        body = body.replace("/*__DATA__*/", "const DATA = " + payload + ";")
        body = body.replace("/*__TKA__*/", "const BANKS = " + tka_payload + ";")
        body = body.replace("__SITE_BASE__", SITE_BASE)
        if "<!--__SUBJECT_CARDS__-->" in body:
            cards = subject_cards(maps if maps is not None else load_maps(), topics, len(questions), tka,
                                  modules if modules is not None else load_modules())
            body = body.replace("<!--__SUBJECT_CARDS__-->", cards)
        for name, target in links.items():
            body = body.replace('href="' + name, 'href="' + target)
        out[path.name] = body
    return out


def build(topics, rows, maps, artifact, tka=None, modules=None):
    questions = [
        {"id": r["id"], "t": r["simpul"], "lv": int(r["tingkat"]), "q": r["soal"], "a": r["jawaban"], "x": r["catatan"]}
        for r in rows
    ]
    modules = modules if modules is not None else load_modules()
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding="utf-8")
    built = {**pages(topics, questions, {}, maps, tka, modules), **map_pages(maps, {}), **module_pages(modules, maps, {})}
    for name, body in built.items():
        (docs / name).write_text(HEAD + body, encoding="utf-8")
    for mod_id in modules:
        if module_pdf(mod_id):
            (docs / f"modul-{mod_id}.pdf").write_bytes(module_pdf(mod_id).read_bytes())
    # Tell GitHub Pages to publish docs/ as-is instead of running it through Jekyll.
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    print("Wrote docs/questions.json, " + ", ".join("docs/" + n for n in built))
    if artifact:
        out = ROOT / "build"
        out.mkdir(exist_ok=True)
        hosted = {**pages(topics, questions, HOSTED_LINKS, maps, tka, modules), **map_pages(maps, HOSTED_LINKS),
                  **module_pages(modules, maps, HOSTED_LINKS)}
        for name, body in hosted.items():
            if name in ARTIFACT_URLS:
                (out / name.replace(".html", ".fragment.html")).write_text(body, encoding="utf-8")
        print("Wrote build/*.fragment.html for " + ", ".join(ARTIFACT_URLS))


def main():
    topics, rows = load()
    maps = load_maps()
    tka = load_tka()
    modules = load_modules()
    tka_types = load_tka_types()
    errors = (validate(topics, rows) + [e for name, m in maps.items() for e in validate_map(name, m)]
              + [e for name, b in tka.items() for e in validate_tka(name, b)]
              + [e for name, mod in modules.items() for e in validate_module(name, mod, maps, tka_types)])
    if errors:
        print(f"{len(errors)} error(s) in data/:")
        print("\n".join("  " + e for e in errors))
        sys.exit(1)
    report(topics, rows)
    for name, m in maps.items():
        print(f"Peta {m['subject']}: {sum(len(d['topics']) for d in m['domains'])} simpul")
        for w in lint_map(name, m):
            print("  warning: " + w)
    for b in tka.values():
        low = sum(it["keyakinan_kunci"] in ("rendah", "tidak ada") for it in b["soal"])
        print(f"TKA {b['mapel']}: {len(b['soal'])} soal, {low} dengan kunci berkeyakinan rendah atau tanpa kunci")
    for name, mod in modules.items():
        items = [it for st in mod["tahap"] for it in st["soal"]]
        print(f"{mod['title']}: {len(mod['materi'])} materi, {len(mod['tahap'])} tahap, {len(items)} soal "
              f"({sum('tka' in it for it in items)} setara TKA)")
        for w in lint_module(name, mod):
            print("  warning: " + w)
    build(topics, rows, maps, "--artifact" in sys.argv[1:], tka, modules)


if __name__ == "__main__":
    main()
