"""Gera os AFNε (construção de Thompson) das regex de padroes.py em formato .jff (JFLAP).

Uso:  python tools/gerar_afne.py            -> escreve docs/diagramas/*.jff e testa
O teste simula cada AFNε e compara com re.fullmatch em milhares de cadeias.
"""
import os, random, sys
from xml.sax.saxutils import escape
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from padroes import PADROES

# ---------- parser (subconjunto usado nas 5 regex) ----------
DIG = frozenset("0123456789")

class P:
    def __init__(s, t): s.t, s.i = t, 0
    def peek(s): return s.t[s.i] if s.i < len(s.t) else None
    def eat(s): c = s.t[s.i]; s.i += 1; return c
    def alt(s):
        br = [s.cat()]
        while s.peek() == "|": s.eat(); br.append(s.cat())
        return br[0] if len(br) == 1 else ("alt", br)
    def cat(s):
        it = []
        while s.peek() not in (None, "|", ")"): it.append(s.rep())
        return ("cat", it)
    def rep(s):
        a = s.atom()
        while s.peek() in ("*", "+", "?", "{"):
            c = s.eat()
            if c == "*": a = ("star", a)
            elif c == "+": a = ("plus", a)
            elif c == "?": a = ("opt", a)
            else:
                j = s.t.index("}", s.i); b = s.t[s.i:j]; s.i = j + 1
                m, M = (int(b), int(b)) if "," not in b else (int(b.split(",")[0]), int(b.split(",")[1]))
                a = ("rep", a, m, M)
        return a
    def atom(s):
        c = s.eat()
        if c == "(":
            if s.t[s.i:s.i+2] == "?:": s.i += 2
            n = s.alt(); assert s.eat() == ")"; return n
        if c == "[": return ("cls", s.cls())
        if c == "\\":
            e = s.eat(); return ("cls", DIG if e == "d" else frozenset(e))
        return ("cls", frozenset(c))
    def cls(s):
        out = set()
        while s.peek() != "]":
            c = s.eat()
            if s.peek() == "-" and s.t[s.i+1] != "]":
                s.eat(); d = s.eat(); out |= {chr(x) for x in range(ord(c), ord(d)+1)}
            else: out.add(c)
        s.eat(); return frozenset(out)

# ---------- Thompson ----------
class NFA:
    def __init__(s): s.n = 0; s.e = []          # arestas (de, para, simbolo|None)
    def new(s): s.n += 1; return s.n - 1
    def add(s, a, b, x=None): s.e.append((a, b, x))
    def build(s, nd):
        k = nd[0]
        if k == "cls":
            a, b = s.new(), s.new()
            for ch in sorted(nd[1]): s.add(a, b, ch)
            return a, b
        if k == "cat":
            if not nd[1]:
                a, b = s.new(), s.new(); s.add(a, b); return a, b
            fr = [s.build(x) for x in nd[1]]
            for (_, e1), (s2, _) in zip(fr, fr[1:]): s.add(e1, s2)
            return fr[0][0], fr[-1][1]
        if k == "alt":
            a, b = s.new(), s.new()
            for x in nd[1]:
                fa, fb = s.build(x); s.add(a, fa); s.add(fb, b)
            return a, b
        if k in ("star", "plus", "opt"):
            a = s.new(); fa, fb = s.build(nd[1]); b = s.new()
            s.add(a, fa); s.add(fb, b)
            if k in ("star", "opt"): s.add(a, b)
            if k in ("star", "plus"): s.add(fb, fa)
            return a, b
        if k == "rep":
            _, x, m, M = nd
            return s.build(("cat", [x]*m + [("opt", x)]*(M-m)))
        raise ValueError(k)

def afne(pattern):
    n = NFA(); i, f = n.build(P(pattern).alt()); return n, i, f

def accepts(n, i, f, w):
    def clo(S):
        S = set(S); st = list(S)
        while st:
            q = st.pop()
            for a, b, x in n.e:
                if a == q and x is None and b not in S: S.add(b); st.append(b)
        return S
    cur = clo({i})
    for c in w:
        cur = clo({b for a, b, x in n.e if a in cur and x == c})
        if not cur: return False
    return f in cur

# ---------- .jff ----------
def jff(n, i, f):
    o = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?><structure>', "<type>fa</type>", "<automaton>"]
    for q in range(n.n):
        x, y = 70 + 110 * (q % 10), 70 + 130 * (q // 10)
        fl = "<initial/>" if q == i else ""
        fl += "<final/>" if q == f else ""
        o.append(f'<state id="{q}" name="q{q}"><x>{x}.0</x><y>{y}.0</y>{fl}</state>')
    for a, b, x in n.e:
        o.append(f"<transition><from>{a}</from><to>{b}</to>" + (f"<read>{escape(x)}</read>" if x else "<read/>") + "</transition>")
    o += ["</automaton>", "</structure>"]
    return "\n".join(o)

NOMES = {"CPF": "er01_cpf", "EMAIL": "er02_email", "TELEFONE": "er03_telefone", "CEP": "er04_cep", "DATA": "er05_data"}

def amostra(n, i, f, rnd):
    q, w = i, ""
    for _ in range(200):
        if q == f and rnd.random() < .3: return w
        out = [(b, x) for a, b, x in n.e if a == q]
        if not out: return w
        q, x = rnd.choice(out); w += x or ""
    return w

if __name__ == "__main__":
    dest = os.path.join(os.path.dirname(__file__), "..", "docs", "diagramas")
    os.makedirs(dest, exist_ok=True)
    rnd = random.Random(1)
    for nome, rx in PADROES.items():
        n, i, f = afne(rx.pattern)
        open(os.path.join(dest, NOMES[nome] + ".jff"), "w", encoding="utf-8").write(jff(n, i, f))
        alfa = sorted({x for _, _, x in n.e if x})
        pos = [amostra(n, i, f, rnd) for _ in range(1500)]
        neg = []
        for w in pos:
            if not w: continue
            k = rnd.randrange(len(w)); m = rnd.random()
            neg.append(w[:k] + w[k+1:] if m < .3 else w[:k] + rnd.choice(alfa + list("xZ !")) + w[k:] if m < .6 else w[:k] + rnd.choice(alfa) + w[k+1:])
        teste = pos + neg + ["".join(rnd.choice(alfa) for _ in range(rnd.randrange(0, 25))) for _ in range(1500)]
        ruins = [w for w in teste if accepts(n, i, f, w) != (rx.fullmatch(w) is not None)]
        neps = sum(1 for *_, x in n.e if x is None)
        print(f"{nome:9} estados={n.n:3} inicial=q{i} final=q{f} transições={len(n.e):4} (ε={neps}) testes={len(teste)} divergências={len(ruins)}")
        assert not ruins, ruins[:5]
    # verificação exaustiva de DDD e data
    n, i, f = afne(PADROES["TELEFONE"].pattern)
    for d in range(100):
        w = f"({d:02d}) 91234-5678"
        assert accepts(n, i, f, w) == (PADROES["TELEFONE"].fullmatch(w) is not None)
    n, i, f = afne(PADROES["DATA"].pattern)
    for d in range(100):
        for m in (1, 12, 13, 0):
            w = f"{d:02d}/{m:02d}/2000"
            assert accepts(n, i, f, w) == (PADROES["DATA"].fullmatch(w) is not None)
    print("OK: todos os AFNε equivalentes às regex.")