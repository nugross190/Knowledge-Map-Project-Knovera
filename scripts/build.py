"""Validate the site data and build the static pages in docs/.

Usage:  python scripts/build.py              # validate, print the report, and rebuild docs/
        python scripts/build.py --artifact   # also write build/*.fragment.html for the claude.ai copies
Reads:  data/topics.json and data/questions.csv (history kit), data/maps/*.json, data/questions/*.csv,
        data/tka/*.json, data/tka-types.json, data/modules/*.json, data/subjects.json, print/<id>.pdf, and
        templates/*.html with their shared parts: templates/_theme.css (added to every page), templates/_feed.css
        and _feed.js (the swipe feed, where a template includes them) and templates/_icons.json (subject icons).
Writes: docs/: one page per template, peta-<id>.html per map, bank-<id>.html per subject bank, modul-<id>.html (and
        modul-<id>.pdf) per module, questions.json and .nojekyll. Only files whose content changed are rewritten,
        and generated files that are no longer built are removed, so a second run changes nothing.
Exits with status 1, writing nothing, if the data has errors.
"""
import argparse
import csv
import functools
import html
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["id", "simpul", "tingkat", "soal", "jawaban", "catatan"]
SUBJECT_FIELDS = FIELDS + ["konteks"]  # data/questions/<map id>.csv; konteks is optional (specs/question-spec.md §6)
MIN_PER_TOPIC = 5
MIN_KONTEKS_SHARE = 0.20  # question-spec 6: subject banks have about 20-30% konteks items
MIN_LEVEL1_SHARE = 0.35   # question-spec 3: subject banks with konteks items run about 35-40% level 1
HEAD = ('<!doctype html>\n<html lang="id">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}</style>\n')
# Grades a topic's `src` covers (map-spec 3). Kelas X is Fase E; kelas XI and XII are Fase F.
GRADES = ("X", "XI", "XII")
GRADE_LABELS = {
    "Kelas X": ["X"], "Kelas XI": ["XI"], "Kelas XII": ["XII"],
    "Kelas X–XI": ["X", "XI"], "Kelas XI–XII": ["XI", "XII"], "Kelas X dan XII": ["X", "XII"],
    "Kelas X–XII": list(GRADES), "Semua kelas": list(GRADES),
}
# The hosted claude.ai copies link to each other by URL instead of by file name.
ARTIFACT_URLS = {
    "peta.html": "https://claude.ai/artifact/D5VQvyvvDqr9rVwHTMX3eP",
    "bank.html": "https://claude.ai/artifact/Qs1xt8ZCrkrKMiHbq2BGFg",
    "simulasi.html": "https://claude.ai/artifact/VfVV7k9nBakQALRRybY526",
    "peta-fisika.html": "https://claude.ai/artifact/XxSteiwD99sQx37T8teYTh",
}
# The GitHub Pages site; pages without a hosted copy are linked there. A project site moves with the repository
# name and GitHub does not redirect the old address, so this must follow any rename of the repository.
PAGES_URL = "https://nugross190.github.io/Knowledge-Map-Project-Knovera/"
# Path of the site under github.io ("/Knowledge-Map-Project-Knovera/"), for pages that need absolute links (404.html).
SITE_BASE = urlparse(PAGES_URL).path
# A template pulls in a shared file from templates/ with /*@include _name.ext*/ (in its <style> or <script>).
INCLUDE = re.compile(r"/\*@include (_[\w.-]+)\*/")
# Suffixes of the files the build owns in its output folders; others (a CNAME, say) are never removed.
GENERATED = (".html", ".pdf", ".json")


# ---------- loading ----------

def load():
    topics = json.loads((ROOT / "data/topics.json").read_text(encoding="utf-8"))
    with open(ROOT / "data/questions.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            sys.exit(f"questions.csv header must be exactly: {','.join(FIELDS)}\nfound: {reader.fieldnames}")
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    return topics, rows


def load_maps():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/maps").glob("*.json"))}


def load_subject_banks():
    """{map id: rows} for every data/questions/<map id>.csv."""
    banks = {}
    for path in sorted((ROOT / "data/questions").glob("*.csv")):
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != SUBJECT_FIELDS:
                sys.exit(f"{path.name} header must be exactly: {','.join(SUBJECT_FIELDS)}\nfound: {reader.fieldnames}")
            banks[path.stem] = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    return banks


def load_tka():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/tka").glob("*.json"))}


def load_tka_types():
    """{type code: type entry} from data/tka-types.json, across all subjects."""
    types = json.loads((ROOT / "data/tka-types.json").read_text(encoding="utf-8"))
    return {t["kode"]: t for s in types.values() for t in s["types"]}


def load_modules():
    folder = ROOT / "data/modules"
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(folder.glob("*.json"))}


def load_roster():
    """data/subjects.json: the subject roster and the home page tabs."""
    path = ROOT / "data/subjects.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_subjects():
    return load_roster().get("subjects", [])


def load_groups():
    """The home page tabs (Umum, IPA, IPS, Bahasa, Tingkat Lanjut), in order, from data/subjects.json."""
    return load_roster().get("groups", [])


@functools.lru_cache(maxsize=None)
def load_icons():
    """Subject icons: inner SVG markup for a 48x48 stroke drawing, keyed by map id (templates/_icons.json)."""
    return json.loads((ROOT / "templates/_icons.json").read_text(encoding="utf-8"))


@dataclass
class Site:
    """Everything the build reads from data/, loaded once."""
    topics: dict      # history kit: domains, weights, topic codes
    rows: list        # history kit questions
    maps: dict        # {map id: subject map}
    banks: dict       # {map id: subject question rows}
    tka: dict         # {bank id: TKA bank}
    tka_types: dict   # {type code: TKA item type}
    modules: dict     # {module id: learning module}
    subjects: list    # the roster
    groups: list      # the home page tabs


def load_site():
    topics, rows = load()
    roster = load_roster()
    return Site(topics, rows, load_maps(), load_subject_banks(), load_tka(), load_tka_types(), load_modules(),
                roster.get("subjects", []), roster.get("groups", []))


# ---------- validation ----------

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


def map_topics(m):
    """A subject map in the shape of data/topics.json, so the bank code can treat both alike.
    Domain weights are each domain's share of the map's topics."""
    total = sum(len(d["topics"]) for d in m["domains"])
    return {"map_url": f"peta-{m['id']}.html", "domains": [
        {"id": d["id"], "name": d["name"], "short": d["short"], "weight": 100 * len(d["topics"]) / total,
         "topics": {t["code"]: t["title"] for t in d["topics"]}} for d in m["domains"]]}


def validate_subject_banks(banks, maps):
    errors = []
    for name, rows in banks.items():
        if name not in maps:
            errors.append(f"data/questions/{name}.csv: no map data/maps/{name}.json")
            continue
        if not rows:
            errors.append(f"data/questions/{name}.csv: no questions; add some or remove the file")
            continue
        errors += [f"data/questions/{name}.csv " + e for e in validate(map_topics(maps[name]), rows)]
    return errors


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
            if t.get("src") and t["src"] not in GRADE_LABELS:
                errors.append(f"{where}: {code} src '{t['src']}' must be one of: {', '.join(GRADE_LABELS)}")
            if t.get("tier") not in (1, 2, 3):
                errors.append(f"{where}: {code} tier must be 1, 2 or 3")
            if "lanjut" in t and not isinstance(t["lanjut"], bool):
                errors.append(f"{where}: {code} 'lanjut' must be true or false")
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
    if any(t.get("lanjut") for t in topics) and not m.get("lanjut_note"):
        warnings.append(f"{where}: topics tagged 'lanjut' but no 'lanjut_note' saying what the tag means here")
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


def validate_subjects(subjects, maps, tka, groups=None):
    """Return problems in data/subjects.json, the roster that the status report follows."""
    errors, where, seen = [], "data/subjects.json", set()
    group_ids = {g["id"] for g in (groups if groups is not None else load_groups())}
    for s in subjects:
        sid = s.get("id", "?")
        if sid in seen:
            errors.append(f"{where}: duplicate id {sid}")
        seen.add(sid)
        if not s.get("name") or not s.get("kelompok"):
            errors.append(f"{where}: {sid} needs 'name' and 'kelompok'")
        if not s.get("short"):
            errors.append(f"{where}: {sid} needs 'short', the name on its home page card")
        if s.get("group") not in group_ids:
            errors.append(f"{where}: {sid} group must be one of: {', '.join(sorted(group_ids))}")
        for g in s.get("also", []):
            if g not in group_ids or g == s.get("group"):
                errors.append(f"{where}: {sid} lists bad extra group {g}")
        if s.get("lanjut_of") and s.get("group") != "lanjut":
            errors.append(f"{where}: {sid} is a Tingkat Lanjut subject and belongs in group 'lanjut'")
        if bool(s.get("map")) == bool(s.get("lanjut_of")):
            errors.append(f"{where}: {sid} needs exactly one of 'map' or 'lanjut_of'")
        if s.get("lanjut_of") and s["lanjut_of"] not in maps:
            errors.append(f"{where}: {sid} is lanjut_of unknown map {s['lanjut_of']}")
        for t in s.get("tka", []):
            if t not in tka:
                errors.append(f"{where}: {sid} lists unknown TKA bank {t}")
    listed = {s.get("map") for s in subjects}
    errors += [f"{where}: map {name} is not listed; add the subject to the roster" for name in maps if name not in listed]
    used = {t for s in subjects for t in s.get("tka", [])}
    errors += [f"{where}: TKA bank {name} is not listed under any subject" for name in tka if name not in used]
    return errors


def validate_site(site):
    """Every problem in data/ that stops the build."""
    return (validate(site.topics, site.rows)
            + [e for name, m in site.maps.items() for e in validate_map(name, m)]
            + [e for name, b in site.tka.items() for e in validate_tka(name, b)]
            + [e for name, mod in site.modules.items() for e in validate_module(name, mod, site.maps, site.tka_types)]
            + validate_subject_banks(site.banks, site.maps)
            + validate_subjects(site.subjects, site.maps, site.tka, site.groups))


# ---------- report ----------

def report(topics, rows):
    per_topic = Counter(r["simpul"] for r in rows)
    for d in topics["domains"]:
        total = sum(per_topic[c] for c in d["topics"])
        print(f"{d['id']}  {total:4d} soal  (bobot {d['weight']}%)")
        for code, title in d["topics"].items():
            flag = "  <- sedikit" if per_topic[code] < MIN_PER_TOPIC else ""
            print(f"   {code}  {per_topic[code]:3d}  {title}{flag}")
    print(f"Total {len(rows)} soal")


def subject_status(subjects, maps, banks, tka):
    """Return the per-subject progress lines that main() prints on every build."""
    lines, done = [], 0
    for s in subjects:
        parts = []
        if s.get("lanjut_of"):
            m = maps[s["lanjut_of"]]
            tagged = sum(bool(t.get("lanjut")) for d in m["domains"] for t in d["topics"])
            parts.append(f"tag di peta {m['id']}: {tagged} simpul" if tagged else f"belum ada tag di peta {m['id']}")
            done += bool(tagged)
        elif s["map"] in maps:
            m = maps[s["map"]]
            parts.append(f"peta {sum(len(d['topics']) for d in m['domains'])} simpul")
            rows = banks.get(s["map"])
            if rows:
                k = sum(bool(r["konteks"]) for r in rows)
                parts.append(f"bank {len(rows)} soal ({k / len(rows):.0%} konteks)")
            else:
                parts.append("belum ada bank")
            done += 1
        else:
            parts.append("belum ada peta" + (f" ({s['note']})" if s.get("note") else ""))
        if s.get("tka"):
            parts.append(f"TKA {len(s['tka'])} naskah")
        lines.append(f"  {s['name'][:44]:<44} {' | '.join(parts)}")
    head = f"Status mapel (data/subjects.json): {done} dari {len(subjects)} sudah tercakup"
    return [head] + lines


def print_report(site):
    """The console report: question counts, lint warnings, bank, TKA and module summaries, and the subject status."""
    report(site.topics, site.rows)
    for name, m in site.maps.items():
        print(f"Peta {m['subject']}: {sum(len(d['topics']) for d in m['domains'])} simpul")
        for w in lint_map(name, m):
            print("  warning: " + w)
    for name, bank_rows in site.banks.items():
        per_topic = Counter(r["simpul"] for r in bank_rows)
        thin = [t["code"] for d in site.maps[name]["domains"] for t in d["topics"] if per_topic[t["code"]] < MIN_PER_TOPIC]
        levels = Counter(r["tingkat"] for r in bank_rows)
        konteks = sum(bool(r["konteks"]) for r in bank_rows)
        print(f"Bank {site.maps[name]['subject']}: {len(bank_rows)} soal, {konteks} konteks, "
              f"tingkat 1/2/3 = {levels['1']}/{levels['2']}/{levels['3']}")
        if thin:
            print(f"  warning: fewer than {MIN_PER_TOPIC} questions: " + ", ".join(thin))
        if konteks / len(bank_rows) < MIN_KONTEKS_SHARE:
            print(f"  warning: konteks is {konteks / len(bank_rows):.0%} (spec: at least {MIN_KONTEKS_SHARE:.0%})")
        if levels["1"] / len(bank_rows) < MIN_LEVEL1_SHARE:
            print(f"  warning: level 1 is {levels['1'] / len(bank_rows):.0%} (spec: at least {MIN_LEVEL1_SHARE:.0%})")
    for b in site.tka.values():
        low = sum(it["keyakinan_kunci"] in ("rendah", "tidak ada") for it in b["soal"])
        print(f"TKA {b['mapel']}: {len(b['soal'])} soal, {low} dengan kunci berkeyakinan rendah atau tanpa kunci")
    for name, mod in site.modules.items():
        items = [it for st in mod["tahap"] for it in st["soal"]]
        print(f"{mod['title']}: {len(mod['materi'])} materi, {len(mod['tahap'])} tahap, {len(items)} soal "
              f"({sum('tka' in it for it in items)} setara TKA)")
        for w in lint_module(name, mod):
            print("  warning: " + w)
    print("\n".join(subject_status(site.subjects, site.maps, site.banks, site.tka)))


# ---------- rendering ----------

def script_json(value):
    """`value` as JSON for a <script> block. "</" and "<!--" are escaped so no text in the data can end the script
    early or switch the HTML parser into its comment-like script states; the JSON still parses to the same value."""
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\u0021--")


@functools.lru_cache(maxsize=None)
def read_template(name):
    """templates/<name> with its shared parts in place: each /*@include _file*/ marker replaced by templates/_file,
    and the light theme (templates/_theme.css) at the end of the first <style> block, so it overrides the page's own."""
    folder = ROOT / "templates"
    text = (folder / name).read_text(encoding="utf-8")
    text = INCLUDE.sub(lambda m: (folder / m.group(1)).read_text(encoding="utf-8"), text)
    return text.replace("</style>", (folder / "_theme.css").read_text(encoding="utf-8") + "</style>", 1)


def rewrite_links(body, links):
    """Point every href="<file>" in a page at its target in `links`; local builds pass {} and keep file names.
    Every key ends in its extension, so a key only matches an href to that file (plus any ?query or #fragment)."""
    for name, target in links.items():
        body = body.replace('href="' + name, 'href="' + target)
    return body


def module_pdf(mod_id):
    """Path of a module's printable PDF (print/<id>.pdf, made by print/print.mjs), or None."""
    path = ROOT / "print" / f"{mod_id}.pdf"
    return path if path.exists() else None


def page_names(site):
    """The file name of every page and PDF the site publishes."""
    names = [p.name for p in sorted((ROOT / "templates").glob("*.html")) if not p.name.startswith("_")]
    names += [f"peta-{i}.html" for i in site.maps] + [f"bank-{i}.html" for i in site.banks]
    names += [f"modul-{i}.html" for i in site.modules] + [f"modul-{i}.pdf" for i in site.modules if module_pdf(i)]
    return names


def hosted_links(site):
    """Links for the claude.ai copies: a page with a hosted copy by its claude.ai URL, every other page and PDF on
    the GitHub Pages site (the home page by the site's own address)."""
    return {name: ARTIFACT_URLS.get(name) or (PAGES_URL if name == "index.html" else PAGES_URL + name)
            for name in page_names(site)}


def question_json(rows):
    out = []
    for r in rows:
        q = {"id": r["id"], "t": r["simpul"], "lv": int(r["tingkat"]), "q": r["soal"], "a": r["jawaban"], "x": r["catatan"]}
        if r.get("konteks"):
            q["k"] = r["konteks"]
        out.append(q)
    return out


def bank_pages(banks, maps, links):
    """Return {file name: page body} for every subject question bank."""
    template = read_template("bank.html")
    out = {}
    for name, rows in banks.items():
        m = maps[name]
        topics = dict(map_topics(m), map_url=links.get(f"peta-{name}.html", f"peta-{name}.html"))
        cfg = {"key": f"bank-soal-{name}-v1", "title": f"Bank Soal {m['subject']}", "map_title": m["title"],
               "mix": "Campuran", "weight_label": "penguasaan rata-rata, berbobot jumlah simpul",
               "lead": "Tanya-jawab singkat untuk mengulang " + m["subject"] + ". Setiap soal memakai kode simpul yang sama "
                       "dengan peta materinya. Soal bertanda Konteks berangkat dari situasi sehari-hari di sekitar kita.",
               "footer": "Hasil latihan tersimpan di peramban ini saja. Soal disusun dari peta materi " + m["subject"] +
                         " dan sumber yang dicantumkan di sana; fakta bertahun disebut tahunnya."}
        payload = script_json({"topics": topics, "questions": question_json(rows), "bank": cfg})
        body = template.replace("/*__DATA__*/", "const DATA = " + payload + ";")
        body = body.replace("<title>Bank Soal Lomba Sejarah</title>", f"<title>{html.escape(cfg['title'])}</title>")
        out[f"bank-{name}.html"] = rewrite_links(body, links)
    return out


def with_grades(m):
    """Copy of a map with each topic's grades (["X", "XI"]) read from its src, for the page's grade filter."""
    domains = [dict(d, topics=[dict(t, grades=GRADE_LABELS[t["src"]]) for t in d["topics"]]) for d in m["domains"]]
    return dict(m, domains=domains, icon=load_icons().get(m["id"], ""))


def icon_svg(markup):
    return ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">' + markup + '</svg>')


def map_pages(maps, links, banks=None):
    """Return {file name: page body} for every subject map."""
    template = read_template("_map.html")
    banks = banks if banks is not None else load_subject_banks()
    out = {}
    for m in maps.values():
        m = with_grades(m)
        if m["id"] in banks:
            m = dict(m, bank=links.get(f"bank-{m['id']}.html", f"bank-{m['id']}.html"))
        body = template.replace("__TITLE__", html.escape(m["title"], quote=False))
        body = body.replace("/*__MAP__*/", "const MAP = " + script_json(m) + ";")
        out[f"peta-{m['id']}.html"] = rewrite_links(body, links)
    return out


def module_pages(modules, maps, links, tka_types=None):
    """Return {file name: page body} for every learning module."""
    template = read_template("_modul.html")
    tka_types = tka_types if tka_types is not None else load_tka_types()
    out = {}
    for mod in modules.values():
        data = dict(mod)
        pdf = f"modul-{mod['id']}.pdf"
        if module_pdf(mod["id"]):
            data["pdf"] = links.get(pdf, pdf)
        if mod.get("map") in maps:
            m = maps[mod["map"]]
            data["map_page"] = links.get(f"peta-{m['id']}.html", f"peta-{m['id']}.html")
            data["map_title"] = m["title"]
            data["topics"] = {t["code"]: t["title"] for d in m["domains"] for t in d["topics"]}
        # The level of each TKA type the module uses, from data/tka-types.json, for the "Setara TKA" badges.
        used = sorted({it["tka"]["tipe"] for st in mod["tahap"] for it in st["soal"] if "tka" in it})
        data["tka_levels"] = {code: tka_types[code]["level"] for code in used if code in tka_types}
        body = template.replace("__TITLE__", html.escape(mod["title"], quote=False))
        body = body.replace("/*__MODULE__*/", "const MOD = " + script_json(data) + ";")
        out[f"modul-{mod['id']}.html"] = rewrite_links(body, links)
    return out


def home_sections(maps, topics, n_questions, tka=None, modules=None, banks=None, subjects=None, groups=None, links=None):
    """Return (html, data) for the home page: subject cards in one panel per group tab, and the tools section.

    Every subject sits in its primary group's panel and in each panel listed under `also`, where it carries its
    primary group's name as a flag. Tingkat Lanjut subjects open the parent map with only the tagged topics.
    `data` feeds the page script: topic codes per grade (for the grade chooser and progress) and bank links.
    """
    e = html.escape
    banks = banks or {}
    subjects = subjects if subjects is not None else load_subjects()
    groups = groups if groups is not None else load_groups()
    links = links or {}
    icons = load_icons()
    names = {g["id"]: g["name"] for g in groups}
    data, panels = {}, {g["id"]: [] for g in groups}
    for s in subjects:
        mid = s.get("map") or s.get("lanjut_of")
        if mid not in maps:
            continue
        m = maps[mid]
        lanjut = bool(s.get("lanjut_of"))
        topics_ = [t for d in m["domains"] for t in d["topics"] if not lanjut or t.get("lanjut")]
        if not topics_:  # a Tingkat Lanjut subject whose parent map has no tagged topics yet
            continue
        grades = ["XI", "XII"] if lanjut else list(GRADES)
        by_grade = {g: [t["code"] for t in topics_ if g in GRADE_LABELS[t["src"]]] for g in grades}
        page = f"peta-{mid}.html"
        href = links.get(page, page) + ("?lanjut=1" if lanjut else "")
        has_bank = mid in banks and not lanjut
        data[s["id"]] = {"map": mid, "name": s["short"], "href": href, "lanjut": lanjut,
                         "grades": by_grade, "codes": [t["code"] for t in topics_],
                         "bank": links.get(f"bank-{mid}.html", f"bank-{mid}.html") if has_bank else ""}
        counts = " · ".join(f"{g} {len(c)}" for g, c in by_grade.items())
        for gid in [s["group"]] + s.get("also", []):
            flag = f'<span class="flag">{e(names[s["group"]])}</span>' if gid != s["group"] else ""
            panels[gid].append(
                f'<a class="sub" href="{e(href)}" data-sid="{e(s["id"])}">'
                f'<span class="ico">{icon_svg(icons.get(mid, icons["modul"]))}</span>'
                f'<span class="sname">{e(s["short"])}{flag}</span>'
                f'<span class="smeta">{len(topics_)} simpul' + (f" · {len(banks[mid])} soal" if has_bank else "") + '</span>'
                f'<span class="sgrades">Kelas {counts}</span>'
                '<span class="sprog" hidden><i></i></span><span class="sdone" hidden></span></a>')
    tabs = "".join(
        f'<button class="gtab" type="button" role="tab" id="tab-{e(g["id"])}" aria-controls="panel-{e(g["id"])}" '
        f'aria-selected="{"true" if i == 0 else "false"}">{e(g["name"])} <span>{len(panels[g["id"]])}</span></button>'
        for i, g in enumerate(groups))
    body = "".join(
        f'<section class="gpanel" role="tabpanel" id="panel-{e(g["id"])}" aria-labelledby="tab-{e(g["id"])}">'
        f'<h3 class="gname">{e(g["name"])}</h3><p class="gnote">{e(g["note"])}</p>'
        f'<div class="subs">{"".join(panels[g["id"]])}</div></section>'
        for g in groups)
    sni = topics["domains"]
    tools = [
        f'<article class="tool"><span class="ico">{icon_svg(icons["lomba"])}</span><h3>Kit Lomba Sejarah</h3>'
        f'<p>Perangkat Lomba Cerdas Cermat Museum: {sum(len(d["topics"]) for d in sni)} simpul, {n_questions} soal, '
        'dan simulasi babak wajib serta rebutan.</p><nav class="tlinks" aria-label="Kit Lomba Sejarah">'
        '<a class="btn primary" href="peta.html">Peta lomba</a><a class="btn" href="bank.html">Bank soal</a>'
        '<a class="btn" href="simulasi.html">Simulasi babak</a></nav></article>']
    if tka:
        n_items = sum(len(b["soal"]) for b in tka.values())
        tools.append(
            f'<article class="tool"><span class="ico">{icon_svg(icons["tka"])}</span><h3>Latihan TKA</h3>'
            f'<p>Soal TKA SMA 2025 dari {len(tka)} naskah, {n_items} soal, dengan kunci usulan yang belum resmi.</p>'
            '<nav class="tlinks" aria-label="Latihan TKA"><a class="btn primary" href="tka.html">Latihan soal</a>'
            '<a class="btn" href="tka.html?mode=geser">Mode geser</a></nav></article>')
    for mod in (modules or {}).values():
        n_items = sum(len(st["soal"]) for st in mod["tahap"])
        tools.append(
            f'<article class="tool"><span class="ico">{icon_svg(icons["modul"])}</span><h3>{e(mod["title"])}</h3>'
            f'<p>Modul belajar {e(maps[mod["map"]]["subject"]) if mod.get("map") in maps else ""}: '
            f'{len(mod["materi"])} materi dan {n_items} latihan bertahap sampai setara TKA.</p>'
            f'<nav class="tlinks" aria-label="{e(mod["title"])}"><a class="btn primary" href="modul-{e(mod["id"])}.html">Buka modul</a></nav></article>')
    stats = {"subjects": len(data), "topics": sum(len(d["topics"]) for m in maps.values() for d in m["domains"]),
             "questions": sum(len(r) for r in banks.values()) + n_questions,
             "tka": sum(len(b["soal"]) for b in (tka or {}).values())}
    sections = {"tabs": tabs, "panels": body, "tools": "\n".join(tools)}
    return sections, {"subjects": data, "stats": stats}


def pages(topics, questions, links, maps=None, tka=None, modules=None, banks=None, subjects=None, groups=None):
    """Return {file name: page body} for every template, with cross-page links resolved through `links`.

    A template that contains /*__DATA__*/ gets the history topics and questions injected there, one that contains
    /*__TKA__*/ gets the TKA banks, and the home page (<!--__TABS__-->) gets its subject cards and data.
    Data not passed in is loaded from data/.
    """
    maps = maps if maps is not None else load_maps()
    tka = tka if tka is not None else load_tka()
    modules = modules if modules is not None else load_modules()
    banks = banks if banks is not None else load_subject_banks()
    history = script_json({"topics": dict(topics, map_url=links.get("peta.html", "peta.html")), "questions": questions})
    banks_json = script_json(list(tka.values()))
    out = {}
    for path in sorted((ROOT / "templates").glob("*.html")):
        if path.name.startswith("_"):  # shared templates, rendered by other steps
            continue
        body = read_template(path.name)
        body = body.replace("/*__DATA__*/", "const DATA = " + history + ";")
        body = body.replace("/*__TKA__*/", "const BANKS = " + banks_json + ";")
        body = body.replace("__SITE_BASE__", SITE_BASE)
        if "<!--__TABS__-->" in body:
            sections, home = home_sections(maps, topics, len(questions), tka, modules, banks, subjects, groups, links)
            for key, part in sections.items():
                body = body.replace(f"<!--__{key.upper()}__-->", part)
            for key, n in home["stats"].items():
                body = body.replace(f"__N_{key.upper()}__", f"{n:,}".replace(",", "."))
            body = body.replace("/*__HOME__*/", "const HOME = " + script_json(home) + ";")
        out[path.name] = rewrite_links(body, links)
    return out


def render_site(site, links):
    """{file name: page body} for every page, with cross-page links resolved through `links` ({} for docs/)."""
    return {**pages(site.topics, question_json(site.rows), links, site.maps, site.tka, site.modules, site.banks,
                    site.subjects, site.groups),
            **map_pages(site.maps, links, site.banks),
            **bank_pages(site.banks, site.maps, links),
            **module_pages(site.modules, site.maps, links, site.tka_types)}


def site_files(site):
    """{file name: content} for everything docs/ holds."""
    files = {name: HEAD + body for name, body in render_site(site, {}).items()}
    files["questions.json"] = json.dumps(question_json(site.rows), ensure_ascii=False, indent=1)
    for mod_id in site.modules:
        if module_pdf(mod_id):
            files[f"modul-{mod_id}.pdf"] = module_pdf(mod_id).read_bytes()
    files[".nojekyll"] = ""  # tells GitHub Pages to publish docs/ as-is instead of running it through Jekyll
    return files


# ---------- writing ----------

def write_files(files, out):
    """Write `files` ({name: str or bytes}) into the folder `out`: only files whose bytes changed are rewritten, and
    generated files (GENERATED suffixes) that are not in `files` are removed. Returns (changed, removed) names."""
    out.mkdir(parents=True, exist_ok=True)
    changed = []
    for name, content in files.items():
        data = content.encode("utf-8") if isinstance(content, str) else content
        path = out / name
        if not path.is_file() or path.read_bytes() != data:
            path.write_bytes(data)  # bytes, so the output is the same on every OS (no newline translation)
            changed.append(name)
    removed = sorted(p.name for p in out.iterdir() if p.is_file() and p.suffix in GENERATED and p.name not in files)
    for name in removed:
        (out / name).unlink()
    return changed, removed


def build(site, out=None, fragments=None):
    """Write the site into `out` (default docs/) and, when `fragments` names a folder, the claude.ai copies of the
    pages in ARTIFACT_URLS there as <name>.fragment.html. Returns {folder: (changed, removed)}."""
    out = Path(out) if out else ROOT / "docs"
    result = {out: write_files(site_files(site), out)}
    if fragments:
        hosted = render_site(site, hosted_links(site))
        files = {name.replace(".html", ".fragment.html"): body for name, body in hosted.items() if name in ARTIFACT_URLS}
        result[Path(fragments)] = write_files(files, Path(fragments))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate the site data, print the report, and rebuild docs/.")
    parser.add_argument("--artifact", action="store_true", help="also write build/*.fragment.html for the claude.ai copies")
    args = parser.parse_args(argv)
    site = load_site()
    errors = validate_site(site)
    if errors:
        print(f"{len(errors)} error(s) in data/:")
        print("\n".join("  " + e for e in errors))
        return 1
    print_report(site)
    for folder, (changed, removed) in build(site, fragments=ROOT / "build" if args.artifact else None).items():
        shown = ": " + ", ".join(changed) if 0 < len(changed) <= 10 else ""
        print(f"{folder.relative_to(ROOT)}/: {len(changed)} file(s) updated{shown}"
              + (f"; removed {', '.join(removed)}" if removed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
