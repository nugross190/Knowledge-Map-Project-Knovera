"""Helpers shared by printable-module content files."""
import random
import re


def n(x, d=2):
    """Indonesian number format: 1.087,5 and −3."""
    x = round(x + 0.0, d)
    if abs(x - round(x)) < 1e-9:
        s = f"{int(round(x)):,}".replace(",", ".")
    else:
        s = f"{x:,.{d}f}".rstrip("0").rstrip(".")
        s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return s.replace("-", "−")


def fr(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'


def Q(lv, q, a, e, fig=None, opts=None, kfig=None):
    """A practice item. fig: graph in the stem; opts: key of graph options (A–D); kfig: graph in the key."""
    return dict(lv=lv, q=q, a=a, e=e, fig=fig, opts=opts, kfig=kfig)


def noisy(f, ts, amp, seed):
    """Deterministic 'measured' data: f(t) plus uniform noise of ±amp, rounded to 0,01."""
    r = random.Random(seed)
    return [(t, round(f(t) + r.uniform(-amp, amp), 2)) for t in ts]


def lsq_slope(pts):
    k = len(pts)
    mt = sum(t for t, _ in pts) / k
    my = sum(y for _, y in pts) / k
    return sum((t - mt) * (y - my) for t, y in pts) / sum((t - mt) ** 2 for t, _ in pts)


def close(a, b, tol=1e-6):
    if abs(a - b) > tol:
        raise AssertionError((a, b))


_LABELS = re.compile(r"(?<![\w])([A-E](?:\s*(?:,|dan)\s*[A-E])*)\s*:")


def _remap_labels(text, mapping):
    """Rename option letters in 'X: ...' / 'X, Y: ...' groups of a wrong-option note, then order the groups."""
    if not text:
        return text
    starts = [m.start() for m in _LABELS.finditer(text)]
    if not starts or starts[0] != 0:
        return re.sub(_LABELS, lambda m: re.sub(r"[A-E]", lambda x: mapping[x.group()], m.group(1)) + ":", text)
    parts = [text[a:b].strip() for a, b in zip(starts, starts[1:] + [len(text)])]
    out = []
    for p in parts:
        m = _LABELS.match(p)
        group = re.sub(r"[A-E]", lambda x: mapping[x.group()], m.group(1))
        letters = sorted(re.findall(r"[A-E]", group))
        joined = (", ".join(letters[:-1]) + " dan " + letters[-1]) if " dan " in m.group(1) else ", ".join(letters)
        out.append((letters[0], joined + ":" + p[m.end():]))
    return " ".join(t for _, t in sorted(out))


def stray_letters(text):
    """Option letters in a wrong-option note that are not part of a label group (should be none)."""
    return re.findall(r"(?<![\w])[A-E](?![\w])", _LABELS.sub("", text or ""))


def balance_keys(tka, uji, seed):
    """Rotate the options of single-answer items so their keys spread evenly over A–E.

    Rotation keeps the distractors' order. Wrong-option notes are relabelled to match.
    Graph-option items (opsi given as a key into GRAPH_OPTS) and multi-answer items are left as they are.
    """
    rng = random.Random(seed)

    def targets(count):
        seq = []
        while len(seq) < count:
            block = list(range(5))
            rng.shuffle(block)
            seq += block
        return seq

    def rotate(opsi, key, target):
        k = len(opsi)
        shift = (target - key) % k
        new = [None] * k
        for i, o in enumerate(opsi):
            new[(i + shift) % k] = o
        mapping = {"ABCDE"[i]: "ABCDE"[(i + shift) % k] for i in range(k)}
        return new, (key + shift) % k, mapping

    tka_out = []
    single = [t for t in tka if t["fmt"] == "pg" and not isinstance(t["opsi"], str)]
    tseq = iter(targets(len(single)))
    for t in tka:
        if t in single:
            t = dict(t)
            t["opsi"], t["kunci"], mp = rotate(t["opsi"], t["kunci"], next(tseq) % len(t["opsi"]))
            t["salah"] = _remap_labels(t["salah"], mp)
        tka_out.append(t)
    useq = iter(targets(len(uji)))
    uji_out = []
    for q, opsi, key, e, sl in uji:
        opsi, key, mp = rotate(opsi, key, next(useq) % len(opsi))
        uji_out.append((q, opsi, key, e, _remap_labels(sl, mp)))
    return tka_out, uji_out
