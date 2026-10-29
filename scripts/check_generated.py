"""Validate generated TKA items in data/tka-generated/ (rules: specs/tka-generation.md).

Usage: python scripts/check_generated.py [files...]   (default: every data/tka-generated/*.json)
Exit code 1 when any file has a problem.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402  (reuses the TKA bank validator)

GEN = build.ROOT / "data/tka-generated"
load_types = build.load_tka_types  # each type code → its declared formats and examples


def check(path, types):
    bank = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    for item in bank.get("soal", []):
        item.setdefault("halaman", [])
    # The bank validator expects halaman as a list of integers; generated items have none.
    problems += [p for p in build.validate_tka(path.stem, bank)
                 if "halaman" not in p and "must look like" not in p]
    problems = [p.replace(f"data/tka/{path.stem}.json", f"data/tka-generated/{path.name}") for p in problems]
    kode = bank.get("kode", "")
    if not kode.endswith("G"):
        problems.append(f"{path.name}: kode '{kode}' must end in G for generated banks")
    for item in bank.get("soal", []):
        sid = item.get("id", "?")
        if not re.fullmatch(re.escape(kode) + r"-G\d{3}", sid):
            problems.append(f"{path.name}: {sid} must be {kode}-GNNN")
        if item.get("asal") != "generated":
            problems.append(f"{path.name}: {sid} needs asal 'generated'")
        if item.get("status_kunci") != "usulan":
            problems.append(f"{path.name}: {sid} status_kunci must be 'usulan'")
        t = types.get(item.get("tipe"))
        if not t:
            problems.append(f"{path.name}: {sid} has unknown tipe {item.get('tipe')!r}")
            continue
        if item.get("format") not in t["format"]:
            problems.append(f"{path.name}: {sid} format {item.get('format')} not allowed for {t['kode']}")
        acuan = item.get("acuan") or []
        if not 1 <= len(acuan) <= 3 or any(a not in t["contoh"] for a in acuan):
            problems.append(f"{path.name}: {sid} acuan must list 1-3 examples of {t['kode']}")
    return problems


def main(args):
    types = load_types()
    files = [Path(a) for a in args] or sorted(GEN.glob("*.json"))
    if not files:
        print("No generated banks found in data/tka-generated/.")
        return 0
    bad = False
    for f in files:
        problems = check(f, types)
        if problems:
            bad = True
            print(f"{f.name}: {len(problems)} problem(s)")
            for p in problems:
                print("  -", p)
        else:
            n = len(json.loads(f.read_text(encoding="utf-8"))["soal"])
            print(f"{f.name}: OK, {n} item(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
