"""Learning paths (data/jalur/<id>.json): answer generators and validation. Format: specs/jalur-spec.md.

Every generated variant stores its parameters in `p`. GEN[name](p) recomputes the fields that must not drift
(kunci, opsi, salah, langkah keys, cek_ap, satuan); validate_jalur() compares them with the stored variant, so a
hand edit that changes a number without changing its key stops the build. Numbers are handled as Decimal from
strings with a decimal comma, so no float rounding enters a key.

Usage:  python scripts/jalur.py            # validate every path and print a summary
"""
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMATS = ("isian", "bertahap", "pilihan-ganda", "pilihan-ganda-kompleks", "benar-salah")
BLOCKS = ("p", "li", "tabel", "contoh", "jebakan")
WIDGETS = ("satuan", "mistar", "jangka-sorong", "mikrometer", "angka-penting", "hitung-ap", "geser-koma", "awalan", "dimensi")
FIGURES = ("mistar", "jangka-sorong", "mikrometer")
CHECKED = ("kunci", "opsi", "salah", "cek_ap", "satuan", "toleransi")
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


# ---------- numbers ----------

def D(x):
    """Decimal from a number or a string with a decimal comma ("2,47", "−3")."""
    if isinstance(x, Decimal):
        return x
    return Decimal(str(x).replace("−", "-").replace(",", ".").replace(" ", ""))


def fmt(x, dp=None):
    """Indonesian decimal text: comma separator, no exponent, trailing zeros dropped unless dp is given."""
    x = D(x)
    if dp is not None:
        x = x.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)
        s = f"{x:f}"
    else:
        s = f"{x.normalize():f}" if x != 0 else "0"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
    return s.replace("-", "−").replace(".", ",")


def fmt_keep(x):
    """Decimal text that keeps the trailing zeros of a rounded value (4.0 -> "4,0")."""
    return f"{D(x):f}".replace("-", "−").replace(".", ",")


def num(x):
    """A Decimal as a JSON number (int when whole)."""
    x = D(x)
    return int(x) if x == x.to_integral_value() else float(x)


def pow10(n):
    return "10" + str(n).translate(SUP)


def sci(m, e):
    """'m × 10ⁿ' text."""
    return f"{fmt(m)} × {pow10(e)}"


def normalize(x):
    """(mantissa, exponent) with 1 <= |mantissa| < 10."""
    x = D(x)
    if x == 0:
        return Decimal(0), 0
    e = x.copy_abs().adjusted()
    return (x.scaleb(-e)).normalize(), e


def sig_figs(text):
    """Significant figures of a written number ("0,00520" -> 3). Integers with trailing zeros are ambiguous and
    rejected, as are signs and exponents: write such numbers in scientific notation instead (specs/jalur-spec.md 5)."""
    s = text.replace("−", "").replace(" ", "")
    if not re.fullmatch(r"\d+(,\d+)?", s):
        raise ValueError(f"not a plain decimal number: {text!r}")
    if "," not in s and len(s.lstrip("0")) > 1 and s.endswith("0"):
        raise ValueError(f"trailing zeros of an integer are ambiguous: {text!r}")
    digits = s.replace(",", "").lstrip("0")
    return len(digits) if digits else 1


def decimals(text):
    s = str(text).replace(".", ",")
    return len(s.split(",")[1]) if "," in s else 0


def _check_tie(x, quantum):
    """Refuse a rounding whose dropped part is exactly half a unit: textbooks round such a 5 differently."""
    rem = (D(x).copy_abs() / quantum) % 1
    if rem == Decimal("0.5"):
        raise ValueError(f"rounding {x} at {quantum} drops exactly a 5; choose other numbers")


def round_sig(x, n, strict=True):
    x = D(x)
    if x == 0:
        return x
    quantum = Decimal(1).scaleb(x.copy_abs().adjusted() - n + 1)
    if strict:
        _check_tie(x, quantum)
    return x.quantize(quantum, rounding=ROUND_HALF_UP)


def round_dp(x, dp, strict=True):
    quantum = Decimal(1).scaleb(-dp)
    if strict:
        _check_tie(x, quantum)
    return D(x).quantize(quantum, rounding=ROUND_HALF_UP)


def written_sig(x):
    """Significant figures of a Decimal as written (its exponent keeps trailing zeros: 7.40 -> 3)."""
    t = D(x).as_tuple()
    digits = "".join(map(str, t.digits)).lstrip("0")
    return max(1, len(digits))


# ---------- generators ----------

def _salah(*pairs, avoid=()):
    """[{nilai, m}] for each (value, misconception), skipping values equal to the key or to an earlier entry."""
    out, seen = [], {D(a) for a in avoid}
    for value, m in pairs:
        v = D(value)
        if v not in seen:
            out.append({"nilai": num(v), "m": m})
            seen.add(v)
    return out


def _rotate(options, pos):
    """Options with the first (correct) one moved to index pos; returns (opsi, kunci, mapping old -> new)."""
    k = len(options)
    order = list(range(1, k))
    order.insert(pos, 0)
    return [options[i] for i in order], pos, {old: new for new, old in enumerate(order)}


def _choice(entries, pos):
    """entries: [(text, misconception or None)], correct first. -> {opsi, kunci, salah}."""
    texts = [t for t, _ in entries]
    if len(set(texts)) != len(texts):
        raise ValueError(f"duplicate options: {texts}")
    opsi, kunci, where = _rotate(texts, pos)
    salah = {str(where[i]): m for i, (_, m) in enumerate(entries) if i and m}
    return {"opsi": opsi, "kunci": kunci, "salah": dict(sorted(salah.items()))}


def g_konversi(p):
    """Unit conversion by a power of ten: p {nilai, kali} -> nilai × kali."""
    return {"kunci": num(D(p["nilai"]) * D(p["kali"]))}


def g_bulat(p):
    """Rounding: p {nilai, dp}."""
    return {"kunci": num(round_dp(p["nilai"], p["dp"]))}


def g_satuan_tak_baku(p):
    """n non-standard units of u cm, answered in metres: p {u, n}."""
    cm = D(p["u"]) * D(p["n"])
    m = cm / 100
    return {"kunci": num(m), "satuan": "m", "salah": _salah((cm, "M03"), (cm / 10, "M03"), avoid=[m])}


def g_satuan_tahap(p):
    cm = D(p["u"]) * D(p["n"])
    return {"langkah": [{"kunci": num(cm)}, {"kunci": num(cm / 100), "salah": _salah((cm, "M03"), avoid=[cm / 100])}]}


TOL_CM_RULER = 0.04     # ruler read to 0,1 cm: only the exact reading passes
TOL_CM_CALIPER = 0.004  # caliper read to 0,01 cm
TOL_MM_MICRO = 0.004    # micrometer read to 0,01 mm


def g_mistar(p):
    """Object from a mm to b mm on a ruler: its length, in mm or (p.satuan "cm") in cm."""
    a, b = D(p["a"]), D(p["b"])
    L = b - a
    if p.get("satuan") == "cm":
        pairs = [(L, "M06")] + ([(b / 10, "M05")] if a else [])
        return {"kunci": num(L / 10), "satuan": "cm", "toleransi": TOL_CM_RULER, "salah": _salah(*pairs, avoid=[L / 10])}
    pairs = [(L / 10, "M06")] + ([(b, "M05")] if a else [])
    return {"kunci": num(L), "satuan": "mm", "salah": _salah(*pairs, avoid=[L])}


def g_mistar_tahap(p):
    a, b = D(p["a"]), D(p["b"])
    if p.get("satuan") == "cm":
        t = TOL_CM_RULER
        return {"langkah": [{"kunci": num(a / 10), "toleransi": t}, {"kunci": num(b / 10), "toleransi": t},
                            {"kunci": num((b - a) / 10), "toleransi": t,
                             "salah": _salah((b / 10, "M05"), (b - a, "M06"), avoid=[(b - a) / 10])}]}
    return {"langkah": [{"kunci": num(a)}, {"kunci": num(b)},
                        {"kunci": num(b - a), "salah": _salah((b, "M05"), ((b - a) / 10, "M06"), avoid=[b - a])}]}


def g_titik_nol(p):
    """Scale shows z before loading (negative: below zero) and r when loaded: true value r − z."""
    z, r = D(p["z"]), D(p["r"])
    true = r - z
    return {"kunci": num(true), "satuan": "kg", "salah": _salah((r, "M08"), (r + z, "M09"), avoid=[true])}


def _js(p):
    return D(p["mm"]) + D(p["k"]) / 10


def g_jangka_sorong(p):
    """Vernier caliper: main scale mm (line before the vernier zero), vernier line k (10 divisions, 0,1 mm = 0,01 cm)."""
    mm, k = D(p["mm"]), D(p["k"])
    x = _js(p)
    wrong = [(mm + k, "M10"), (mm + k / 100, "M11"), (mm + 1 + k / 10, "M12")]
    if p.get("satuan", "mm") == "cm":
        return {"kunci": num(x / 10), "satuan": "cm", "toleransi": TOL_CM_CALIPER,
                "salah": _salah((x, "M06"), *[(v / 10, m) for v, m in wrong], avoid=[x / 10])}
    return {"kunci": num(x), "satuan": "mm", "salah": _salah(*wrong, avoid=[x])}


def g_jangka_sorong_tahap(p):
    """Steps of a caliper reading. In cm (p.satuan "cm"): the cm number, the small lines after it, the vernier line,
    the result. In mm: the main scale, the vernier line, the result."""
    mm, k = D(p["mm"]), D(p["k"])
    x = _js(p)
    if p.get("satuan") == "cm":
        cm, ticks = mm // 10, mm % 10
        return {"langkah": [{"kunci": num(cm)}, {"kunci": num(ticks), "salah": _salah((ticks + 1, "M12"), avoid=[ticks])},
                            {"kunci": num(k)},
                            {"kunci": num(x / 10), "toleransi": TOL_CM_CALIPER,
                             "salah": _salah(((mm + k) / 10, "M10"), ((mm + k / 100) / 10, "M11"), (x, "M06"), avoid=[x / 10])}]}
    return {"langkah": [{"kunci": num(mm), "salah": _salah((mm + 1, "M12"), avoid=[mm])}, {"kunci": num(k)},
                        {"kunci": num(x), "salah": _salah((mm + k, "M10"), (mm + k / 100, "M11"), avoid=[x])}]}


def _mk(p):
    s, t = D(p["s"]), D(p["t"])
    if s % Decimal("0.5") or not (0 < t < 50):
        raise ValueError(f"micrometer needs s in steps of 0,5 and 0 < t < 50: {p}")
    return s, t, s + t / 100


def g_mikrometer(p):
    """Micrometer: sleeve reading s (with the half-millimetre line), thimble division t (50 divisions, 0,01 mm)."""
    s, t, x = _mk(p)
    half = s - Decimal("0.5") if s % 1 else s + Decimal("0.5")
    return {"kunci": num(x), "satuan": "mm", "toleransi": TOL_MM_MICRO,
            "salah": _salah((half + t / 100, "M14"), (s + t / 10, "M15"), avoid=[x])}


def g_mikrometer_tahap(p):
    """Steps of a micrometer reading: the last millimetre line, the half-millimetre line (0 or 0,5), the thimble line,
    the result."""
    s, t, x = _mk(p)
    whole, half = s // 1, s % 1
    return {"langkah": [{"kunci": num(whole)},
                        {"kunci": num(half), "toleransi": 0.04, "salah": _salah((Decimal("0.5") - half, "M14"), avoid=[half])},
                        {"kunci": num(t)},
                        {"kunci": num(x), "toleransi": TOL_MM_MICRO,
                         "salah": _salah((s + t / 10, "M15"), (x - half + (Decimal("0.5") - half), "M14"), avoid=[x])}]}


def g_ap_hitung(p):
    """Count the significant figures of p.x."""
    x = p["x"]
    n = sig_figs(x)
    digits = x.replace(",", "")
    pairs = []
    if x.startswith("0"):
        pairs.append((len(digits), "M17"))
    if "," in x and x.endswith("0"):
        pairs.append((len(digits.lstrip("0").rstrip("0")) or 1, "M18"))
    return {"kunci": n, "satuan": "angka penting", "salah": _salah(*pairs, avoid=[n])}


def g_ap_hitung_tahap(p):
    """Two steps: how many leading zeros (not significant), then how many significant figures."""
    x = p["x"]
    digits = x.replace(",", "")
    lead = len(digits) - len(digits.lstrip("0"))
    n = sig_figs(x)
    return {"langkah": [{"kunci": lead}, {"kunci": n, "salah": _salah((len(digits), "M17"), avoid=[n])}]}


def g_ap_pilih(p):
    """Which written number has exactly p.n significant figures. A wrong option is keyed to M17 when counting its
    leading zeros would give n, and to M18 when dropping its trailing decimal zeros would give n."""
    counts = [sig_figs(x) for x in p["opsi"]]
    if counts.count(p["n"]) != 1:
        raise ValueError(f"exactly one option must have {p['n']} significant figures: {counts}")
    k = counts.index(p["n"])
    salah = {}
    for i, x in enumerate(p["opsi"]):
        d = x.replace(",", "")
        if i == k:
            continue
        if x.startswith("0") and len(d) == p["n"]:
            salah[str(i)] = "M17"
        elif "," in x and x.endswith("0") and len(d.lstrip("0").rstrip("0")) == p["n"]:
            salah[str(i)] = "M18"
    return {"opsi": list(p["opsi"]), "kunci": k, "salah": salah}


OPS = {"×": lambda a, b: a * b, ":": lambda a, b: a / b, "+": lambda a, b: a + b, "−": lambda a, b: a - b}


def _ap_kali(p):
    a, b = p["a"], p["b"]
    exact = OPS[p["op"]](D(a), D(b))
    n = min(sig_figs(a), sig_figs(b))
    return exact, n, round_sig(exact, n)


def g_ap_kali(p):
    """Multiplication or division written to the fewest significant figures."""
    exact, n, key = _ap_kali(p)
    out = {"kunci": num(key), "cek_ap": n}
    if p.get("pg"):
        most = max(sig_figs(p["a"]), sig_figs(p["b"]))
        wrong = [(round_sig(exact, most, False), "M21"), (round_sig(exact, most + 1, False), "M19"),
                 (exact.normalize(), "M19")]
        if n > 1:
            wrong.append((round_sig(exact, n - 1, False), "M32"))
        entries = [(fmt_keep(key) + p.get("satuan_teks", ""), None)]
        for v, m in wrong:
            text = fmt_keep(v) + p.get("satuan_teks", "")
            whole_zero = v == v.to_integral_value() and fmt(v).endswith("0")  # ambiguous count: leave it out
            if text not in [t for t, _ in entries] and not whole_zero:
                entries.append((text, m))
        return _choice(entries, p["pg"]["posisi"])
    out["salah"] = _salah((exact, "M19"), (round_sig(exact, max(sig_figs(a) for a in (p["a"], p["b"])), False), "M21"),
                          avoid=[key])
    return out


def g_ap_kali_tahap(p):
    exact, n, key = _ap_kali(p)
    return {"langkah": [{"kunci": sig_figs(p["a"])}, {"kunci": sig_figs(p["b"])},
                        {"kunci": num(key), "salah": _salah((exact, "M19"), avoid=[key])}]}


def g_ap_tambah(p):
    """Addition or subtraction written to the fewest decimal places."""
    exact = OPS[p["op"]](D(p["a"]), D(p["b"]))
    dp = min(decimals(p["a"]), decimals(p["b"]))
    key = round_dp(exact, dp)
    by_sig = round_sig(exact, min(sig_figs(p["a"]), sig_figs(p["b"])), False)
    return {"kunci": num(key), "cek_ap": written_sig(key),
            "salah": _salah((exact, "M19"), (by_sig, "M20"), avoid=[key])}


def g_notasi(p):
    """Write p.x as a × 10ⁿ: two steps, a and n."""
    m, e = normalize(p["x"])
    if e == 0:
        raise ValueError("choose a number that needs a power of ten")
    return {"langkah": [{"kunci": num(m), "salah": _salah((m * 10, "M24"), (m / 10, "M24"), avoid=[m])},
                        {"kunci": e, "salah": _salah((-e, "M22"), (e + 1, "M23"), (e - 1, "M23"), avoid=[e])}]}


def g_notasi_tahap(p):
    """Three steps: how many places the comma moves, the mantissa a, the exponent n."""
    m, e = normalize(p["x"])
    if e == 0:
        raise ValueError("choose a number that needs a power of ten")
    return {"langkah": [{"kunci": abs(e)}, {"kunci": num(m), "salah": _salah((m * 10, "M24"), (m / 10, "M24"), avoid=[m])},
                        {"kunci": e, "salah": _salah((-e, "M22"), (e + 1, "M23"), (e - 1, "M23"), avoid=[e])}]}


def _sci_parts(p):
    (m1, e1), (m2, e2) = p["a"], p["b"]
    m1, m2 = D(m1), D(m2)
    if p["op"] == "×":
        raw_m, raw_e, bad_e = m1 * m2, e1 + e2, e1 * e2
    else:
        raw_m, raw_e, bad_e = m1 / m2, e1 - e2, e1 + e2
    m, shift = normalize(raw_m)
    return raw_m, raw_e, bad_e, m, raw_e + shift


def g_notasi_kali(p):
    """(m1 × 10^e1) op (m2 × 10^e2) in standard form, as a choice: correct, not normalized or exponent off by the
    normalising shift, exponent rule broken."""
    raw_m, raw_e, bad_e, m, e = _sci_parts(p)
    entries = [(sci(m, e), None)]
    if raw_m != m:
        entries.append((sci(raw_m, raw_e), "M24"))
        entries.append((sci(m, raw_e), "M23"))
    else:
        entries.append((sci(m, e + 1), "M23"))
        entries.append((sci(m, -e) if e else sci(m, e - 1), "M22"))
    entries.append((sci(m, bad_e + (e - raw_e)), "M25"))
    return _choice(entries, p["posisi"])


def g_notasi_kali_tahap(p):
    (m1, e1), (m2, e2) = p["a"], p["b"]
    raw_m, raw_e, bad_e, m, e = _sci_parts(p)
    return {"langkah": [{"kunci": num(raw_m)}, {"kunci": raw_e, "salah": _salah((bad_e, "M25"), avoid=[raw_e])},
                        {"kunci": e, "salah": _salah((raw_e, "M24"), avoid=[e])}]}


PREFIX = {"G": 9, "M": 6, "k": 3, "c": -2, "m": -3, "μ": -6, "n": -9, "p": -12}
NEIGHBOUR = {"G": "M", "M": "k", "k": "M", "c": "m", "m": "μ", "μ": "m", "n": "μ", "p": "n"}


def g_awalan(p):
    """p.nilai with prefix p.awalan, in base units, standard form, as a choice."""
    v, a, u = D(p["nilai"]), p["awalan"], p["satuan"]
    m, e = normalize(v * Decimal(10) ** PREFIX[a])
    m2, e2 = normalize(v * Decimal(10) ** PREFIX[NEIGHBOUR[a]])
    entries = [(f"{sci(m, e)} {u}", None), (f"{sci(m2, e2)} {u}", "M26")]
    if v != m:
        entries.append((f"{sci(v, PREFIX[a])} {u}", "M24"))
    entries.append((f"{sci(m, -e)} {u}", "M22"))
    return _choice(entries, p["posisi"])


def _solve_dims(target, factors):
    """Exponents x, y with factor1^x · factor2^y having the dimensions of target (dicts {dim: power})."""
    dims = sorted(set(target) | set(factors[0]) | set(factors[1]))
    rows = [(Fraction(factors[0].get(d, 0)), Fraction(factors[1].get(d, 0)), Fraction(target.get(d, 0))) for d in dims]
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            (a, b, c), (d, e, f) = rows[i], rows[j]
            det = a * e - b * d
            if det:
                x, y = (c * e - b * f) / det, (a * f - c * d) / det
                if all(r[0] * x + r[1] * y == r[2] for r in rows):
                    return x, y
                raise ValueError(f"no consistent exponents for {target} from {factors}")
    raise ValueError("dimensions do not determine the exponents")


def g_dimensi_pangkat(p):
    """Exponent p.tanya (0 = x, 1 = y) in target = k · f1ˣ · f2ʸ."""
    xy = _solve_dims(p["target"], p["faktor"])
    return {"kunci": num(Decimal(xy[p["tanya"]].numerator) / Decimal(xy[p["tanya"]].denominator)), "satuan": "(pangkat)"}


def g_tka_pipa(p):
    """Inner diameter of a pipe from a caliper reading of the outer diameter and a micrometer reading of the wall:
    which rods fit (strictly smaller)."""
    outer = _js(p["luar"])
    s, t, wall = _mk(p["tebal"])
    inner = outer - 2 * wall
    half = s - Decimal("0.5") if s % 1 else s + Decimal("0.5")
    wrong_half = outer - 2 * (half + t / 100)
    once = outer - wall
    values = [inner - Decimal("0.5"), inner - Decimal("0.1"), inner + Decimal("0.2"), wrong_half, once]
    if len(set(values)) != 5 or wrong_half < inner + Decimal("0.2") or once < wrong_half:
        raise ValueError(f"pipe numbers give overlapping options: {values}")
    order = sorted(range(5), key=lambda i: values[i])
    opsi = [fmt(values[i], 2) + " mm" for i in order]
    kunci = [n for n, i in enumerate(order) if values[i] < inner]
    names = {3: "M14", 4: "M31"}
    salah = {str(n): names[i] for n, i in enumerate(order) if i in names}
    return {"opsi": opsi, "kunci": kunci, "salah": salah}


def g_tka_kedalaman(p):
    """Depth read with the caliper's depth rod; a bolt of length p.baut (mm) is pushed in: how much sticks out.
    Options in mm, or in cm when p.satuan is "cm"."""
    depth, bolt = _js(p), D(p["baut"])
    mm, k = D(p["mm"]), D(p["k"])
    out = bolt - depth
    if out <= 0:
        raise ValueError("the bolt must stick out")
    cm = p.get("satuan") == "cm"
    show = (lambda v, dp: fmt(v / 10, dp + 1) + " cm") if cm else (lambda v, dp: fmt(v, dp) + " mm")
    entries = [(show(out, 1), None)]
    misread = mm + k
    entries.append(("Baut tidak menonjol" if misread >= bolt else show(bolt - misread, 1), "M10"))
    entries.append((show(bolt - (mm + 1 + k / 10), 1), "M12"))
    entries.append((show(bolt - (mm + k / 100), 2), "M11"))
    return _choice(entries, p["posisi"])


GEN = {
    "konversi": g_konversi, "bulat": g_bulat,
    "satuan-tak-baku": g_satuan_tak_baku, "satuan-tahap": g_satuan_tahap,
    "mistar": g_mistar, "mistar-tahap": g_mistar_tahap, "titik-nol": g_titik_nol,
    "jangka-sorong": g_jangka_sorong, "jangka-sorong-tahap": g_jangka_sorong_tahap,
    "mikrometer": g_mikrometer, "mikrometer-tahap": g_mikrometer_tahap,
    "ap-hitung": g_ap_hitung, "ap-hitung-tahap": g_ap_hitung_tahap, "ap-pilih": g_ap_pilih, "ap-kali": g_ap_kali, "ap-kali-tahap": g_ap_kali_tahap, "ap-tambah": g_ap_tambah,
    "notasi": g_notasi, "notasi-tahap": g_notasi_tahap, "notasi-kali": g_notasi_kali, "notasi-kali-tahap": g_notasi_kali_tahap, "awalan": g_awalan,
    "dimensi-pangkat": g_dimensi_pangkat, "tka-pipa": g_tka_pipa, "tka-kedalaman": g_tka_kedalaman,
}


# ---------- validation ----------

def load_jalur():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/jalur").glob("*.json"))}


def _numeric(x):
    return type(x) in (int, float)


def _check_blocks(blocks, owner, err):
    for blk in blocks or []:
        kinds = [k for k in BLOCKS if k in blk]
        if len(kinds) != 1:
            err(f"{owner} has a block that is not exactly one of {', '.join(BLOCKS)}")
            continue
        kind, val = kinds[0], blk[kinds[0]]
        if kind in ("li", "jebakan") and not (isinstance(val, list) and val):
            err(f"{owner} '{kind}' must be a non-empty list")
        if kind == "tabel" and (not val.get("cols") or any(len(r) != len(val["cols"]) for r in val.get("rows", []))):
            err(f"{owner} table has rows of the wrong length")
        if kind == "contoh" and not (val.get("soal") and val.get("langkah")):
            err(f"{owner} contoh needs 'soal' and 'langkah'")


def _check_salah_list(salah, owner, mis, err):
    if not isinstance(salah, list) or not all(isinstance(s, dict) and _numeric(s.get("nilai")) and s.get("m") in mis
                                              for s in salah):
        err(f"{owner} salah must be a list of {{nilai, m}} with known misconception ids")


def _check_variant(it, v, owner, mis, err):
    fmt_ = it["format"]
    if not v.get("soal"):
        err(f"{owner} missing 'soal'")
    if not (isinstance(v.get("pembahasan"), list) and v["pembahasan"]):
        err(f"{owner} needs 'pembahasan' as a non-empty list of steps")
    kunci, opsi = v.get("kunci"), v.get("opsi")
    if fmt_ == "isian":
        if not _numeric(kunci) or not v.get("satuan"):
            err(f"{owner} isian needs a numeric 'kunci' and a 'satuan'")
        if "toleransi" in v and not (_numeric(v["toleransi"]) and v["toleransi"] > 0):
            err(f"{owner} toleransi must be a positive number")
        if "salah" in v:
            _check_salah_list(v["salah"], owner, mis, err)
    elif fmt_ == "bertahap":
        steps = v.get("langkah")
        if not (isinstance(steps, list) and steps):
            err(f"{owner} bertahap needs 'langkah'")
            return
        for i, st in enumerate(steps, 1):
            if not st.get("teks") or not _numeric(st.get("kunci")):
                err(f"{owner} langkah {i} needs 'teks' and a numeric 'kunci'")
            if "salah" in st:
                _check_salah_list(st["salah"], f"{owner} langkah {i}", mis, err)
    else:
        if not isinstance(opsi, list) or len(opsi) < 2 or not all(isinstance(o, str) and o.strip() for o in opsi):
            err(f"{owner} needs at least two non-empty options")
            return
        k = len(opsi)
        if fmt_ == "pilihan-ganda" and not (type(kunci) is int and 0 <= kunci < k):
            err(f"{owner} kunci must be the index of one option")
        if fmt_ == "pilihan-ganda-kompleks" and not (isinstance(kunci, list) and kunci and kunci == sorted(set(kunci))
                                                     and all(type(x) is int and 0 <= x < k for x in kunci)):
            err(f"{owner} kunci must be a sorted list of option indexes")
        if fmt_ == "benar-salah":
            if not (isinstance(kunci, list) and len(kunci) == k and all(isinstance(x, bool) for x in kunci)):
                err(f"{owner} kunci must be one true/false per statement")
            if not (isinstance(it.get("kolom"), list) and len(it["kolom"]) == 2):
                err(f"{owner} benar-salah needs 'kolom' with two headings")
        if "salah" in v:
            sal = v["salah"]
            right = set(kunci) if isinstance(kunci, list) else {kunci}
            if not isinstance(sal, dict) or not all(
                    k_.isdigit() and int(k_) < k and int(k_) not in right and m in mis for k_, m in sal.items()):
                err(f"{owner} salah must map wrong option indexes to known misconception ids")


def _check_generated(it, v, owner, err):
    try:
        expected = GEN[it["gen"]](v.get("p") or {})
    except Exception as exc:  # a generator refusing its parameters is a data error
        err(f"{owner} generator {it['gen']} failed: {exc}")
        return
    for key in CHECKED:
        if key in expected and v.get(key) != expected[key]:
            err(f"{owner} {key} {v.get(key)!r} differs from generator {it['gen']}: {expected[key]!r}")
    if "langkah" in expected:
        steps = v.get("langkah") or []
        if len(steps) != len(expected["langkah"]):
            err(f"{owner} has {len(steps)} steps; generator {it['gen']} makes {len(expected['langkah'])}")
            return
        for i, (got, want) in enumerate(zip(steps, expected["langkah"]), 1):
            for key in ("kunci", "salah", "toleransi"):
                if key in want and got.get(key) != want[key]:
                    err(f"{owner} langkah {i} {key} {got.get(key)!r} differs from generator {it['gen']}: {want[key]!r}")


def validate_jalur(name, doc, maps, tka_types):
    """Every problem in one learning path that stops the build (specs/jalur-spec.md 6)."""
    errors = []
    where = f"data/jalur/{name}.json"

    def err(msg):
        errors.append(f"{where}: {msg}")

    for key in ("id", "kode", "subject", "title", "lead", "prasyarat", "unit", "akhir", "soal", "miskonsepsi"):
        if not doc.get(key):
            err(f"missing '{key}'")
    if errors:
        return errors
    if doc["id"] != name:
        err(f"id '{doc['id']}' must match the file name")
    kode = doc["kode"]
    if not re.fullmatch(r"[A-Z]{2,5}", kode):
        err(f"kode '{kode}' must be 2-5 uppercase letters")
    codes = None
    if doc.get("map"):
        if doc["map"] not in maps:
            err(f"map '{doc['map']}' is not a file in data/maps/")
        else:
            codes = {t["code"] for d in maps[doc["map"]]["domains"] for t in d["topics"]}
    mis = doc["miskonsepsi"]
    for mid, m in mis.items():
        if not re.fullmatch(r"M\d{2}", mid) or not (m.get("judul") and m.get("teks")):
            err(f"miskonsepsi {mid} needs an id like M01, a 'judul' and a 'teks'")

    items = {}
    for it in doc["soal"]:
        sid = it.get("id", "?")
        if not re.fullmatch(re.escape(kode) + r"-\d{3}", sid):
            err(f"{sid} must look like {kode}-NNN")
        if sid in items:
            err(f"duplicate id {sid}")
        items[sid] = it
        if it.get("format") not in FORMATS:
            err(f"{sid} format must be one of {', '.join(FORMATS)}")
            continue
        if codes is not None and it.get("simpul") and it["simpul"] not in codes:
            err(f"{sid} refers to unknown topic {it['simpul']}")
        hints = it.get("bantuan")
        if not (isinstance(hints, list) and 1 <= len(hints) <= 2 and all(isinstance(h, str) and h for h in hints)):
            err(f"{sid} needs 'bantuan': one or two hints")
        if not (isinstance(it.get("varian"), list) and it["varian"]):
            err(f"{sid} needs at least one variant")
            continue
        if it.get("gen") and it["gen"] not in GEN:
            err(f"{sid} unknown generator '{it['gen']}'")
        figs = it.get("fig")
        figs = [figs] if isinstance(figs, str) else (figs or [])
        for f in figs:
            jenis = f if isinstance(f, str) else f.get("jenis")
            if jenis not in FIGURES:
                err(f"{sid} unknown figure '{jenis}'")
        for n, v in enumerate(it["varian"], 1):
            owner = f"{sid} varian {n}"
            _check_variant(it, v, owner, mis, err)
            if (it.get("gen") in GEN or figs) and not isinstance(v.get("p"), dict):
                err(f"{owner} needs parameters 'p'")
            elif it.get("gen") in GEN:
                _check_generated(it, v, owner, err)
        if "tka" in it:
            t = tka_types.get(it["tka"].get("tipe"))
            if not t:
                err(f"{sid} unknown TKA tipe '{it['tka'].get('tipe')}'")
            else:
                if it["format"] not in t["format"]:
                    err(f"{sid} format {it['format']} not allowed for {t['kode']}")
                acuan = it["tka"].get("acuan", [])
                if not acuan or not set(acuan) <= set(t["contoh"]):
                    err(f"{sid} acuan must list transcribed examples of {t['kode']}")

    def ref(sid, owner, practice=False):
        if sid not in items:
            err(f"{owner} refers to unknown item {sid}")
        elif practice and len(items[sid].get("varian", [])) < 2:
            err(f"{owner}: practice family {sid} needs at least two variants (the help ladder shows a twin)")

    prereqs = set()
    unit_ids = {u.get("id") for u in doc["unit"]}
    for pr in doc["prasyarat"]:
        pid = pr.get("id", "?")
        prereqs.add(pid)
        if not (pr.get("judul") and pr.get("kenapa")):
            err(f"prasyarat {pid} needs 'judul' and 'kenapa'")
        if not (isinstance(pr.get("cek"), list) and len(pr["cek"]) == 2):
            err(f"prasyarat {pid} needs two 'cek' items")
        for sid in pr.get("cek", []):
            ref(sid, f"prasyarat {pid}", practice=True)
        for u in pr.get("untuk", []):
            if u not in unit_ids:
                err(f"prasyarat {pid} refers to unknown unit {u}")
        bridge = pr.get("jembatan") or {}
        if not bridge.get("isi") or not bridge.get("soal"):
            err(f"prasyarat {pid} needs a 'jembatan' with 'isi' and 'soal'")
        _check_blocks(bridge.get("isi"), f"prasyarat {pid} jembatan", err)
        if bridge.get("soal"):
            ref(bridge["soal"], f"prasyarat {pid} jembatan")

    seen_units = set()
    for u in doc["unit"]:
        uid = u.get("id", "?")
        if uid in seen_units:
            err(f"duplicate unit id {uid}")
        seen_units.add(uid)
        for key in ("judul", "kait", "media", "lihat", "bersama", "sendiri", "ringkas"):
            if not u.get(key):
                err(f"unit {uid} missing '{key}'")
        for code in u.get("simpul", []):
            if codes is not None and code not in codes:
                err(f"unit {uid} refers to unknown topic {code}")
        for pid in u.get("butuh", []):
            if pid not in prereqs:
                err(f"unit {uid} needs unknown prasyarat {pid}")
        if u.get("kait"):
            if not u["kait"].get("teks"):
                err(f"unit {uid} kait needs 'teks'")
            ref(u["kait"].get("soal"), f"unit {uid} kait")
        media = u.get("media") or {}
        for w in media.get("alat", []):
            if w not in WIDGETS:
                err(f"unit {uid} uses unknown widget '{w}'")
        _check_blocks(media.get("isi"), f"unit {uid} media", err)
        lihat = u.get("lihat") or {}
        if not (lihat.get("soal") and isinstance(lihat.get("langkah"), list) and lihat["langkah"]):
            err(f"unit {uid} lihat needs 'soal' and 'langkah'")
        if lihat.get("fig") and (lihat["fig"] not in FIGURES or not isinstance(lihat.get("p"), dict)):
            err(f"unit {uid} lihat figure needs a known 'fig' and 'p'")
        if u.get("bersama"):
            ref(u["bersama"], f"unit {uid} bersama")
            if u["bersama"] in items and items[u["bersama"]].get("format") != "bertahap":
                err(f"unit {uid} bersama {u['bersama']} must be a 'bertahap' item")
        for sid in u.get("sendiri", []):
            ref(sid, f"unit {uid} sendiri", practice=True)
    paket = doc.get("paket")
    if paket is not None:
        listed = [uid for pk in paket for uid in pk.get("unit", [])]
        for pk in paket:
            if not (pk.get("id") and pk.get("judul") and pk.get("unit")):
                err(f"paket {pk.get('id', '?')} needs 'id', 'judul' and 'unit'")
        if sorted(listed) != sorted(u.get("id") for u in doc["unit"]):
            err("paket must list every unit exactly once")
        elif listed != [u.get("id") for u in doc["unit"]]:
            err("unit order must follow the paket order")
    akhir = doc["akhir"]
    if not akhir.get("judul") or not akhir.get("soal"):
        err("akhir needs 'judul' and 'soal'")
    for sid in akhir.get("soal", []):
        ref(sid, "akhir")
    return errors


def lint_jalur(name, doc):
    """Soft rules: warnings that do not stop the build."""
    where, out = f"data/jalur/{name}.json", []
    used = {s["m"] for it in doc.get("soal", []) for v in it.get("varian", [])
            for s in (v.get("salah") if isinstance(v.get("salah"), list) else [])}
    used |= {m for it in doc.get("soal", []) for v in it.get("varian", [])
             for m in (v.get("salah").values() if isinstance(v.get("salah"), dict) else [])}
    used |= {s["m"] for it in doc.get("soal", []) for v in it.get("varian", []) for st in v.get("langkah", [])
             for s in st.get("salah", [])}
    unused = sorted(set(doc.get("miskonsepsi", {})) - used)
    if unused:
        out.append(f"{where}: misconceptions never shown: {', '.join(unused)}")
    referenced = set()
    for pr in doc.get("prasyarat", []):
        referenced |= set(pr.get("cek", [])) | {pr.get("jembatan", {}).get("soal")}
    for u in doc.get("unit", []):
        referenced |= {u.get("kait", {}).get("soal"), u.get("bersama")} | set(u.get("sendiri", []))
    referenced |= set(doc.get("akhir", {}).get("soal", []))
    orphans = [it["id"] for it in doc.get("soal", []) if it["id"] not in referenced]
    if orphans:
        out.append(f"{where}: items not used by any card: {', '.join(orphans)}")
    if not any("tka" in it for it in doc.get("soal", [])):
        out.append(f"{where}: no TKA-style items")
    if not doc.get("blurb"):
        out.append(f"{where}: no 'blurb' for the home-page card")
    return out


def summary(doc):
    variants = sum(len(it["varian"]) for it in doc["soal"])
    packs = f"{len(doc['paket'])} paket, " if doc.get("paket") else ""
    return (f"{doc['title']}: {len(doc['prasyarat'])} prasyarat, {packs}{len(doc['unit'])} unit, {len(doc['soal'])} soal "
            f"({variants} varian, {sum('tka' in it for it in doc['soal'])} setara TKA), "
            f"{len(doc['miskonsepsi'])} miskonsepsi")


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build  # noqa: E402  (for the maps and TKA types)
    maps, types = build.load_maps(), build.load_tka_types()
    bad = 0
    for name, doc in load_jalur().items():
        errors = validate_jalur(name, doc, maps, types)
        print(summary(doc) if not errors else f"{name}: {len(errors)} error(s)")
        for e in errors + lint_jalur(name, doc):
            print("  " + e)
        bad += bool(errors)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
