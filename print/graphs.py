"""Motion model and fixed graph templates for printable modules.

One Motion (segments of constant acceleration) drives everything: s(t), v(t), a(t),
the graphs and the answer keys, so a graph and its key cannot disagree. Items never
draw a graph by hand: they pick a TEMPLATE (fixed axes and grid) and add motions,
data points or straight lines (tangents, best-fit lines) to it.
"""
from dataclasses import dataclass, field


@dataclass
class Motion:
    s0: float = 0.0
    v0: float = 0.0
    segs: list = field(default_factory=list)   # [(duration, acceleration), ...]
    label: str = ""
    color: str = "#1f3a68"

    def _walk(self):
        t, s, v = 0.0, self.s0, self.v0
        for dur, a in self.segs:
            yield t, s, v, dur, a
            s += v * dur + 0.5 * a * dur * dur
            v += a * dur
            t += dur

    @property
    def t_end(self):
        return sum(d for d, _ in self.segs)

    def state(self, t):
        """(s, v) at time t; after the last segment the object keeps its final state."""
        last = None
        for t0, s, v, dur, a in self._walk():
            last = (t0, s, v, dur, a)
            if t <= t0 + dur + 1e-12:
                u = t - t0
                return s + v * u + 0.5 * a * u * u, v + a * u
        t0, s, v, dur, a = last
        return s + v * dur + 0.5 * a * dur * dur, v + a * dur

    def s(self, t):
        return self.state(t)[0]

    def v(self, t):
        return self.state(t)[1]

    def a(self, t):
        for t0, s, v, dur, a in self._walk():
            if t < t0 + dur - 1e-12:
                return a
        return self.segs[-1][1]

    def corners(self):
        out, t = [0.0], 0.0
        for d, _ in self.segs:
            t += d
            out.append(t)
        return out

    def distance(self, t1, t2, n=4000):
        tot, prev = 0.0, self.s(t1)
        for k in range(1, n + 1):
            cur = self.s(t1 + (t2 - t1) * k / n)
            tot += abs(cur - prev)
            prev = cur
        return tot


@dataclass
class Template:
    name: str
    kind: str           # "s", "v", "a"
    t_max: float
    t_step: float
    y_min: float
    y_max: float
    y_step: float

    @property
    def ylabel(self):
        return {"s": "s (m)", "v": "v (m/s)", "a": "a (m/s²)"}[self.kind]


TEMPLATES = {t.name: t for t in [
    # GLB
    Template("glb-st", "s", 10, 1, 0, 50, 5),
    Template("glb-st2", "s", 10, 1, -20, 30, 5),
    Template("glb-vt", "v", 10, 1, -10, 10, 2),
    # GLBB
    Template("glbb-vt", "v", 10, 1, 0, 20, 2),
    Template("glbb-vt2", "v", 10, 1, -10, 10, 2),
    Template("glbb-st", "s", 10, 1, 0, 100, 10),
    Template("glbb-at", "a", 10, 1, -6, 6, 1),
    # combined motion and real cases
    Template("gab-vt", "v", 20, 2, 0, 30, 5),
    Template("gab-st", "s", 20, 2, 0, 400, 50),
    # motion-tracking data
    Template("data-st", "s", 4, 0.5, 0, 2, 0.25),
    Template("data-vt", "v", 4, 0.5, 0, 1.6, 0.2),
]}


def fmt(x):
    s = f"{x:g}"
    return s.replace("-", "−").replace(".", ",")


def check_on_grid(m: Motion, tp: Template):
    """Every segment boundary sits on a t gridline, and v or a there sits on a y gridline,
    so students can read values exactly. s values may fall between gridlines."""
    problems = []
    for t in m.corners():
        if abs(t / tp.t_step - round(t / tp.t_step)) > 1e-9:
            problems.append(f"t = {t} is not on a t gridline")
        if tp.kind == "a":
            ys = [m.a(max(0.0, t - 1e-6)), m.a(t)]
        else:
            ys = [m.s(t) if tp.kind == "s" else m.v(t)]
        for y in ys:
            if tp.kind != "s" and abs(y / tp.y_step - round(y / tp.y_step)) > 1e-9:
                problems.append(f"{tp.kind}({t}) = {y} is not on a gridline")
            if not (tp.y_min - 1e-9 <= y <= tp.y_max + 1e-9):
                problems.append(f"{tp.kind}({t}) = {y} is outside {tp.name}")
    if m.t_end > tp.t_max + 1e-9:
        problems.append(f"motion lasts longer than {tp.name}")
    return problems


def render(tp, motions=(), points=(), lines=(), shade=None, marks=(), width=300, height=190, note=""):
    """Draw a template with motions on it.

    points: [(t, y)] data dots. lines: [(t1, y1, t2, y2, dashed)] straight lines (tangent, best fit).
    shade: (motion_index, t1, t2) area under a v–t line. marks: [(t, y, label)].
    """
    for m in motions:
        p = check_on_grid(m, tp)
        assert not p, p
    L, R, T, B = 44, 14, 14, 30
    W, H = width - L - R, height - T - B
    X = lambda t: L + W * t / tp.t_max
    Y = lambda y: T + H * (tp.y_max - y) / (tp.y_max - tp.y_min)
    s = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-family="Inter,DejaVu Sans,sans-serif">']
    nt = round(tp.t_max / tp.t_step)
    ny = round((tp.y_max - tp.y_min) / tp.y_step)
    for k in range(nt + 1):
        s.append(f'<line x1="{X(k*tp.t_step):.1f}" y1="{T}" x2="{X(k*tp.t_step):.1f}" y2="{T+H}" stroke="#d5dbe6" stroke-width="0.7"/>')
    for k in range(ny + 1):
        y = tp.y_min + k * tp.y_step
        s.append(f'<line x1="{L}" y1="{Y(y):.1f}" x2="{L+W}" y2="{Y(y):.1f}" stroke="#d5dbe6" stroke-width="0.7"/>')
    y0 = Y(0) if tp.y_min <= 0 <= tp.y_max else T + H
    s.append(f'<line x1="{L}" y1="{y0:.1f}" x2="{L+W+6}" y2="{y0:.1f}" stroke="#1f2430" stroke-width="1.3"/>')
    s.append(f'<line x1="{L}" y1="{T+H}" x2="{L}" y2="{T-6}" stroke="#1f2430" stroke-width="1.3"/>')
    for k in range(nt + 1):
        t = k * tp.t_step
        s.append(f'<text x="{X(t):.1f}" y="{T+H+11}" font-size="7.5" text-anchor="middle" fill="#4b5260">{fmt(t)}</text>')
    for k in range(ny + 1):
        y = round(tp.y_min + k * tp.y_step, 6)
        s.append(f'<text x="{L-4}" y="{Y(y)+3:.1f}" font-size="7.5" text-anchor="end" fill="#4b5260">{fmt(y)}</text>')
    s.append(f'<text x="{L+W+4}" y="{T+H+24}" font-size="8.5" text-anchor="end" fill="#1f2430">t (s)</text>')
    s.append(f'<text x="6" y="{T-3}" font-size="8.5" fill="#1f2430">{tp.ylabel}</text>')
    if shade:
        mi, t1, t2 = shade
        m = motions[mi]
        pts = [(t1, 0)] + [(t1 + (t2 - t1) * k / 60, m.v(t1 + (t2 - t1) * k / 60)) for k in range(61)] + [(t2, 0)]
        s.append('<polygon points="' + " ".join(f"{X(t):.1f},{Y(y):.1f}" for t, y in pts) + '" fill="#2e5597" fill-opacity="0.15"/>')
    for m in motions:
        if tp.kind == "a":
            t = 0.0
            for d, a in m.segs:
                s.append(f'<line x1="{X(t):.1f}" y1="{Y(a):.1f}" x2="{X(t+d):.1f}" y2="{Y(a):.1f}" stroke="{m.color}" stroke-width="2.2"/>')
                t += d
            yl = m.segs[-1][1]
        else:
            f = m.s if tp.kind == "s" else m.v
            n = max(2, int(m.t_end * 24))
            pts = [(m.t_end * k / n, f(m.t_end * k / n)) for k in range(n + 1)]
            s.append(f'<polyline fill="none" stroke="{m.color}" stroke-width="2.2" stroke-linejoin="round" points="' + " ".join(f"{X(t):.1f},{Y(y):.1f}" for t, y in pts) + '"/>')
            yl = f(m.t_end)
        if m.label:
            s.append(f'<text x="{X(m.t_end)+3:.1f}" y="{Y(yl)-4:.1f}" font-size="9" font-weight="700" fill="{m.color}">{m.label}</text>')
    for t1, y1, t2, y2, dashed in lines:
        dash = ' stroke-dasharray="5 3"' if dashed else ""
        s.append(f'<line x1="{X(t1):.1f}" y1="{Y(y1):.1f}" x2="{X(t2):.1f}" y2="{Y(y2):.1f}" stroke="#c0502a" stroke-width="1.6"{dash}/>')
    for t, y in points:
        s.append(f'<circle cx="{X(t):.1f}" cy="{Y(y):.1f}" r="2.2" fill="#1f2430"/>')
    for t, y, lab in marks:
        s.append(f'<circle cx="{X(t):.1f}" cy="{Y(y):.1f}" r="2.6" fill="#1f2430"/><text x="{X(t)+4:.1f}" y="{Y(y)-5:.1f}" font-size="9" fill="#1f2430">{lab}</text>')
    if note:
        s.append(f'<text x="{L+W}" y="{T+8}" font-size="8.5" text-anchor="end" fill="#1f3a68" font-weight="700">{note}</text>')
    s.append("</svg>")
    return "".join(s)
