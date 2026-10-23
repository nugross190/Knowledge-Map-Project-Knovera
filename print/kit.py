"""Helpers shared by printable-module content files."""
import random


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
