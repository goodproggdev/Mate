# -*- coding: utf-8 -*-
"""
Integrali doppi d'esame -- integrazione al banco 'Esame' (ESAME["integrali"]).

Qui sono raccolti gli integrali doppi dei veri appelli (PDF in ExEsami) che non
erano ancora nel banco. Ogni problema e' descritto da una "scheda" (integranda,
vincoli del dominio, curve, punti notevoli e scomposizione del dominio in pezzi
normali/polari/lineari); il motore qui sotto calcola con sympy tutti i passaggi
intermedi (primitiva interna, valutazione agli estremi, integrale esterno,
somma dei pezzi), costruisce la figura dal sistema di disequazioni e VERIFICA
il risultato con un'integrazione numerica a griglia indipendente (che usa
direttamente le disequazioni del testo, non la scomposizione a mano).
"""
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import esame_bank
from esame_bank import ESAME, _voce, _passo, _tex, _png, x, y

r_, t_, u_, w_ = sp.symbols('r theta u w', real=True)
r_ = sp.symbols('r', positive=True)

AVVISI = []          # discrepanze con i risultati stampati nei PDF (per il report)
_COL = ['#2e5c8a', '#c0392b', '#1a7f37', '#8e44ad', '#d35400', '#16a085', '#7f8c8d']


# ---------------------------------------------------------------------------
# utilita' LaTeX / calcolo
# ---------------------------------------------------------------------------
def _L(e):
    return sp.latex(e)


def _semp(e):
    e = sp.simplify(e)
    return e


def _prim(f, v):
    P = sp.integrate(f, v)
    if P.has(sp.Integral) or P.has(sp.Piecewise):
        raise ValueError("primitiva non elementare: %s" % (f,))
    return P


def _valuta(P, v, lo, hi):
    return _semp(P.subs(v, hi) - P.subs(v, lo))


def _ordina_tag(e):
    return e


# ---------------------------------------------------------------------------
# verifica numerica indipendente (usa i vincoli del testo)
# ---------------------------------------------------------------------------
def _numerico(f, vincoli, bbox, n=3000):
    xmin, xmax, ymin, ymax = bbox
    xs = xmin + (np.arange(n) + 0.5) * (xmax - xmin) / n
    ys = ymin + (np.arange(n) + 0.5) * (ymax - ymin) / n
    dA = (xmax - xmin) / n * (ymax - ymin) / n
    fn = sp.lambdify((x, y), f, 'numpy')
    hs = [sp.lambdify((x, y), h, 'numpy') for h in vincoli]
    tot = 0.0
    step = 250
    for i0 in range(0, n, step):
        X, Y = np.meshgrid(xs, ys[i0:i0 + step])
        m = np.ones(X.shape, bool)
        with np.errstate(all='ignore'):
            for h in hs:
                m &= (np.asarray(h(X, Y), dtype=float) >= -1e-12)
            val = np.asarray(fn(X, Y) * np.ones(X.shape), dtype=float)
        tot += float(np.nansum(np.where(m, val, 0.0))) * dA
    return tot


# ---------------------------------------------------------------------------
# figura dal sistema di disequazioni
# ---------------------------------------------------------------------------
def _figura(titolo, bbox, vincoli, curve, punti):
    xmin, xmax, ymin, ymax = bbox
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    X, Y = np.meshgrid(np.linspace(xmin, xmax, 900), np.linspace(ymin, ymax, 900))
    m = np.ones(X.shape, bool)
    with np.errstate(all='ignore'):
        for h in vincoli:
            hv = np.asarray(sp.lambdify((x, y), h, 'numpy')(X, Y), dtype=float)
            m &= (hv >= -1e-9)
    ax.contourf(X, Y, m.astype(float), levels=[0.5, 1.5], colors=['#8a6d1a'], alpha=0.35)
    handles = []
    for i, (g, lab) in enumerate(curve):
        col = _COL[i % len(_COL)]
        with np.errstate(all='ignore'):
            gv = np.asarray(sp.lambdify((x, y), g, 'numpy')(X, Y) * np.ones(X.shape), dtype=float)
        ax.contour(X, Y, gv, levels=[0], colors=[col], linewidths=1.6)
        handles.append(Line2D([0], [0], color=col, lw=1.6, label=lab))
    for (px, py, lab) in punti:
        ax.plot(float(px), float(py), 'ko', markersize=5)
        ax.annotate(lab, (float(px), float(py)), textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal', 'box')
    if handles:
        ax.legend(handles=handles, fontsize=7.5, loc='best')
    ax.set_title(titolo, fontsize=9.5)
    fig.tight_layout()
    return _png(fig)


# ---------------------------------------------------------------------------
# motore: pezzi di dominio
# ---------------------------------------------------------------------------
def _pezzo_cart(f, p, k):
    """Dominio normale: ext=(var,a,b), int=(lo,hi). Ritorna (passi, valore, k)."""
    v, a, b = p["ext"]
    lo, hi = p["int"]
    w = y if v == x else x
    asse = "x" if v == x else "y"
    passi = []
    et = p.get("etichetta")
    pre = (" [%s]" % et) if et else ""
    passi.append(_passo(
        "Passo %d — scrivo l'integrale iterato%s: il dominio è normale rispetto all'asse %s, quindi "
        "la variabile %s varia tra due costanti e %s tra due funzioni di %s (estremi di integrazione):"
        % (k, pre, asse, v, w, v),
        r"\int_{%s}^{%s}\left(\int_{%s}^{%s} %s\,d%s\right)d%s" % (_L(a), _L(b), _L(lo), _L(hi), _L(f), w, v)))
    k += 1
    P = _prim(f, w)
    F = _valuta(P, w, lo, hi)
    passi.append(_passo(
        "Passo %d — integro rispetto a %s (tenendo %s costante): calcolo la primitiva e la valuto "
        "(valutata agli estremi, F(estremo sup.) − F(estremo inf.)):" % (k, w, v),
        r"\int %s\,d%s=%s\ \Longrightarrow\ \Big[%s\Big]_{%s}^{%s}=%s"
        % (_L(f), w, _L(P), _L(P), _L(lo), _L(hi), _L(F))))
    k += 1
    for (tx, la) in p.get("extra_est", []):
        passi.append(_passo("Passo %d — %s" % (k, tx), la))
        k += 1
    Q = None
    try:
        Q = _prim(F, v)
    except Exception:
        Q = None
    val = _semp(sp.integrate(F, (v, a, b)))
    if Q is not None:
        lat = (r"\int %s\,d%s=%s\ \Longrightarrow\ \Big[%s\Big]_{%s}^{%s}=%s"
               % (_L(F), v, _L(Q), _L(Q), _L(a), _L(b), _L(val)))
    else:
        lat = r"\int_{%s}^{%s}%s\,d%s=%s" % (_L(a), _L(b), _L(F), v, _L(val))
    passi.append(_passo(
        "Passo %d — integro rispetto a %s sull'intervallo [%s, %s]: primitiva valutata agli estremi:"
        % (k, v, sp.sstr(a), sp.sstr(b)), lat))
    k += 1
    return passi, val, k


def _pezzo_pol(f, p, k):
    a, b = p["t"]
    lo, hi = p["r"]
    fp = _semp(f.subs({x: r_ * sp.cos(t_), y: r_ * sp.sin(t_)}, simultaneous=True) * r_)
    passi = []
    et = p.get("etichetta")
    pre = (" [%s]" % et) if et else ""
    passi.append(_passo(
        "Passo %d — passo alle coordinate polari%s: x = r cosθ, y = r sinθ, dx dy = r dr dθ "
        "(il fattore r è il determinante della trasformazione); sostituisco nell'integrando e scrivo gli "
        "estremi di integrazione di r e di θ (scaletta integrale doppio, punto 3):" % (k, pre),
        r"\int_{%s}^{%s}\left(\int_{%s}^{%s} %s\,dr\right)d\theta,\qquad f\cdot r=%s"
        % (_L(a), _L(b), _L(lo), _L(hi), _L(fp), _L(fp))))
    k += 1
    P = _prim(fp, r_)
    F = _valuta(P, r_, lo, hi)
    passi.append(_passo(
        "Passo %d — integro rispetto a r (θ costante): primitiva valutata agli estremi di r:" % k,
        r"\int %s\,dr=%s\ \Longrightarrow\ \Big[%s\Big]_{%s}^{%s}=%s"
        % (_L(fp), _L(P), _L(P), _L(lo), _L(hi), _L(F))))
    k += 1
    for (tx, la) in p.get("extra_est", []):
        passi.append(_passo("Passo %d — %s" % (k, tx), la))
        k += 1
    val = _semp(sp.integrate(F, (t_, a, b)))
    try:
        Q = _prim(F, t_)
        lat = (r"\int %s\,d\theta=%s\ \Longrightarrow\ \Big[%s\Big]_{%s}^{%s}=%s"
               % (_L(F), _L(Q), _L(Q), _L(a), _L(b), _L(val)))
    except Exception:
        lat = r"\int_{%s}^{%s}%s\,d\theta=%s" % (_L(a), _L(b), _L(F), _L(val))
    passi.append(_passo(
        "Passo %d — integro rispetto a θ: primitiva valutata agli estremi di θ:" % k, lat))
    k += 1
    return passi, val, k


def _pezzo_cv(f, p, k):
    """Cambio di variabili: u=..., w=... ; x(u,w), y(u,w); dominio u in [a,b], w in [lo,hi]."""
    xu, yu = p["xy"]
    (uu, a, b) = p["ext"]
    (ww, lo, hi) = p["int"]
    J = _semp(sp.Matrix([[sp.diff(xu, uu), sp.diff(xu, ww)], [sp.diff(yu, uu), sp.diff(yu, ww)]]).det())
    fg = _semp(f.subs({x: xu, y: yu}, simultaneous=True) * sp.Abs(J))
    passi = []
    passi.append(_passo(
        "Passo %d — cambio di variabili lineare: %s. Il valore assoluto del determinante della matrice "
        "di trasformazione è |det| = %s (fattore di area), quindi dx dy = %s du dw; riscrivo l'integrando "
        "nelle nuove variabili e gli estremi di integrazione (il dominio diventa %s):"
        % (k, p["testo_sost"], sp.sstr(sp.Abs(J)), sp.sstr(sp.Abs(J)), p["testo_dom"]),
        p["lat_sost"] + r"\ \Rightarrow\ " + r"\int_{%s}^{%s}\left(\int_{%s}^{%s}%s\,d%s\right)d%s"
        % (_L(a), _L(b), _L(lo), _L(hi), _L(fg), ww, uu)))
    k += 1
    P = _prim(fg, ww)
    F = _valuta(P, ww, lo, hi)
    passi.append(_passo(
        "Passo %d — integro rispetto a %s: primitiva valutata agli estremi:" % (k, ww),
        r"\int %s\,d%s=%s\ \Longrightarrow\ \Big[%s\Big]_{%s}^{%s}=%s"
        % (_L(fg), ww, _L(P), _L(P), _L(lo), _L(hi), _L(F))))
    k += 1
    val = _semp(sp.integrate(F, (uu, a, b)))
    try:
        Q = _prim(F, uu)
        lat = (r"\int %s\,d%s=%s\ \Longrightarrow\ \Big[%s\Big]_{%s}^{%s}=%s"
               % (_L(F), uu, _L(Q), _L(Q), _L(a), _L(b), _L(val)))
    except Exception:
        lat = r"\int_{%s}^{%s}%s\,d%s=%s" % (_L(a), _L(b), _L(F), uu, _L(val))
    passi.append(_passo(
        "Passo %d — integro rispetto a %s: primitiva valutata agli estremi:" % (k, uu), lat))
    k += 1
    return passi, val, k


def _esercizio(fonte, num, enunciato, dom_latex, f, pezzi, vincoli, bbox, curve, punti,
               geom, titolo, pdf_R=None, nota_R=None, f_latex=None, tol=2e-3, salta_numerico=False):
    """geom = lista di (testo, latex) per i passi geometrici (curve, intersezioni, scelta dell'ordine)."""
    testo = "[%s, Esercizio %s] %s" % (fonte, num, enunciato)
    fl = f_latex if f_latex is not None else _L(f)
    testo_latex = r"\iint_D " + fl + r"\,dA,\quad D: " + dom_latex
    passi = [_passo("Dominio e integranda:", testo_latex)]
    k = 1
    for (tx, la) in geom:
        passi.append(_passo("Passo %d — %s" % (k, tx), la))
        k += 1
    tot = 0
    vals = []
    for p in pezzi:
        tipo = p.get("tipo", "cart")
        fn = {"cart": _pezzo_cart, "pol": _pezzo_pol, "cv": _pezzo_cv}[tipo]
        ps, val, k = fn(f, p, k)
        passi.extend(ps)
        vals.append(val)
        tot = tot + val
    tot = _semp(tot)
    tot = sp.expand(tot.replace(lambda e: isinstance(e, sp.log) and e.args[0].is_Integer and e.args[0] > 3,
                                lambda e: sum(m * sp.log(q) for q, m in sp.factorint(e.args[0]).items())))
    if tot.has(sp.sinh) or tot.has(sp.cosh):
        tot = sp.expand(tot.rewrite(sp.exp))
    if len(pezzi) > 1:
        passi.append(_passo(
            "Passo %d — sommo i contributi dei pezzi in cui ho scomposto il dominio (integrale additivo "
            "sul dominio):" % k,
            " + ".join("(" + _L(v) + ")" for v in vals) + " = " + _L(tot)))
        k += 1
    # verifica numerica indipendente
    vn = float(sp.N(tot))
    if not salta_numerico:
        num_int = _numerico(f, vincoli, bbox)
        if abs(num_int - vn) > tol * max(1.0, abs(vn)):
            raise AssertionError("%s Es.%s: simbolico %.6f vs numerico %.6f" % (fonte, num, vn, num_int))
    if pdf_R is not None:
        vr = float(sp.N(pdf_R))
        if abs(vr - vn) > 1e-9 * max(1.0, abs(vn)):
            AVVISI.append("%s Es.%s: valore calcolato %s (=%.6f) vs risultato stampato %s (=%.6f)%s"
                          % (fonte, num, sp.sstr(tot), vn, sp.sstr(pdf_R), vr,
                             (" -- " + nota_R) if nota_R else ""))
    passi.append(_passo("Valore dell'integrale:", "= " + _tex(tot)))
    png = _figura(titolo, bbox, vincoli, curve, punti)
    risposta = {"tipo": "numero", "atteso_numero": vn, "atteso_display": str(tot)}
    return _voce(fonte, testo, testo_latex, "Scrivi il valore (numerico o simbolico), es: pi/2",
                 passi, risposta, png)


def _aggiungi(*a, **kw):
    ESAME["integrali"].append(_esercizio(*a, **kw))


R = sp.Rational
S2 = sp.sqrt(2)
S3 = sp.sqrt(3)
pi = sp.pi
E = sp.E


# ===========================================================================
# APRILE 2026
# ===========================================================================
_aggiungi(
    "11 aprile 2026", 3,
    "Dato l'integrale doppio di f(x,y)=1/(x+y+2)^2 sul dominio D = {(x,y) ∈ R²: 1 ≤ x ≤ 2; y ≥ 0; "
    "y ≤ 1/x}: a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; "
    "b) calcolarne il valore.",
    r"1\le x\le2,\ y\ge0,\ y\le\tfrac1x",
    1 / (x + y + 2)**2,
    [dict(ext=(x, 1, 2), int=(0, 1 / x))],
    [x - 1, 2 - x, y, 1 / x - y], (-0.2, 2.6, -0.3, 1.4),
    [(x - 1, "x=1"), (x - 2, "x=2"), (y, "y=0 (asse x)"), (x * y - 1, "xy=1")],
    [(1, 1, "(1,1)"), (2, 0.5, "(2,1/2)"), (1, 0, "(1,0)"), (2, 0, "(2,0)")],
    [("disegno e caratteristiche delle curve (scaletta integrale doppio, punto 1): x=1 e x=2 sono rette "
      "verticali, y=0 è l'asse x e y=1/x è un ramo di iperbole equilatera del I quadrante, decrescente, "
      "con gli assi come asintoti.", r"x=1,\quad x=2,\quad y=0,\quad y=\frac1x"),
     ("le curve si incontrano nei vertici (1,0), (2,0), (2,1/2) e (1,1): D è la regione sotto l'iperbole, "
      "tra le due rette verticali e sopra l'asse x.",
      r"y=\tfrac1x\ \Rightarrow\ x=1:\ y=1,\qquad x=2:\ y=\tfrac12"),
     ("scelgo l'ordine: D è un dominio normale rispetto all'asse x (per ogni x in [1,2] la y va dalla "
      "curva inferiore y=0 a quella superiore y=1/x). Integro prima in y perché l'integrando è una potenza "
      "di (x+y+2) e la primitiva rispetto a y è immediata.",
      r"D=\left\{1\le x\le2,\ 0\le y\le\tfrac1x\right\}")],
    "Dominio D (11 aprile 2026)")

_aggiungi(
    "8 aprile 2026", 3,
    "Dato l'integrale doppio di f(x,y)=x+y sul dominio D = {(x,y) ∈ R²: y ≥ 0; x ≥ 0; x²+y² ≤ 1; y ≤ x}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore.",
    r"y\ge0,\ x\ge0,\ x^2+y^2\le1,\ y\le x",
    x + y,
    [dict(tipo="pol", t=(0, pi / 4), r=(0, 1))],
    [y, x, 1 - x**2 - y**2, x - y], (-0.2, 1.25, -0.2, 1.25),
    [(x**2 + y**2 - 1, "x²+y²=1"), (y - x, "y=x"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (1, 0, "(1,0)"), (S2 / 2, S2 / 2, "(√2/2,√2/2)")],
    [("disegno e caratteristiche delle curve: x²+y²=1 è la circonferenza di centro l'origine e raggio 1; "
      "y=x è la bisettrice del I e III quadrante; x≥0 e y≥0 selezionano il I quadrante.",
      r"x^2+y^2=1,\quad y=x,\quad x\ge0,\ y\ge0"),
     ("D è lo spicchio di cerchio (settore circolare) compreso tra l'asse x (θ=0) e la bisettrice y=x "
      "(θ=π/4), con raggio fino a 1. Poiché il bordo è fatto di una circonferenza centrata in O e di rette "
      "per l'origine, scelgo le coordinate polari (scaletta integrale doppio, punto 3): x²+y²=r².",
      r"0\le\theta\le\tfrac{\pi}{4},\qquad 0\le r\le1")],
    "Dominio D (8 aprile 2026)")

_aggiungi(
    "16 maggio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=e^(-(x-y)) sul dominio D = {(x,y) ∈ R²: x ≥ 0; y ≥ x; y ≤ 2-2x}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore. "
    "(Lo stesso esercizio compare anche nell'appello del 14 aprile 2026, a ottobre 2024 e a luglio 2023.)",
    r"x\ge0,\ y\ge x,\ y\le2-2x",
    sp.exp(-(x - y)),
    [dict(ext=(x, 0, R(2, 3)), int=(x, 2 - 2 * x))],
    [x, y - x, 2 - 2 * x - y], (-0.3, 1.2, -0.3, 2.4),
    [(x, "x=0 (asse y)"), (y - x, "y=x"), (y - 2 + 2 * x, "y=2-2x")],
    [(0, 0, "O(0,0)"), (0, 2, "(0,2)"), (R(2, 3), R(2, 3), "(2/3,2/3)")],
    [("disegno e caratteristiche delle curve: x=0 è l'asse y; y=x è la bisettrice; y=2-2x è una retta "
      "decrescente (pendenza −2) che passa per (0,2) e (1,0). Sono tutte rette: D è un poligono.",
      r"x=0,\quad y=x,\quad y=2-2x"),
     ("vertici: x=0 e y=x danno O(0,0); x=0 e y=2-2x danno (0,2); y=x e y=2-2x danno x=2-2x, cioè "
      "x=2/3, y=2/3. D è il triangolo di vertici (0,0), (0,2), (2/3,2/3).",
      r"x=2-2x\ \Rightarrow\ x=\tfrac23,\ y=\tfrac23"),
     ("scelgo l'ordine: per x in [0,2/3] la y va dalla retta y=x (sotto) alla retta y=2-2x (sopra): "
      "dominio normale rispetto all'asse x con un solo pezzo (con dx dy ne servirebbero due).",
      r"D=\left\{0\le x\le\tfrac23,\ x\le y\le2-2x\right\}")],
    "Dominio D (16 maggio 2026)")

_aggiungi(
    "11 aprile 2026", 3,
    "Dato l'integrale doppio di f(x,y)=y/x sul dominio D = {(x,y) ∈ R²: y ≥ 0; xy-2 ≥ 0; x²+y²-5 ≤ 0}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore.",
    r"y\ge0,\ xy\ge2,\ x^2+y^2\le5",
    y / x,
    [dict(ext=(x, 1, 2), int=(2 / x, sp.sqrt(5 - x**2)))],
    [y, x * y - 2, 5 - x**2 - y**2], (0.0, 2.6, 0.0, 2.6),
    [(x * y - 2, "xy=2"), (x**2 + y**2 - 5, "x²+y²=5"), (y, "y=0")],
    [(1, 2, "(1,2)"), (2, 1, "(2,1)")],
    [("disegno e caratteristiche delle curve: xy=2 è un'iperbole equilatera (rami nel I e III quadrante, "
      "assi come asintoti); x²+y²=5 è la circonferenza di centro O e raggio √5; y≥0 è il semipiano superiore. "
      "Dato y≥0 e xy≥2 si ha x>0: D sta nel I quadrante.",
      r"xy=2,\qquad x^2+y^2=5,\qquad y\ge0"),
     ("intersezioni iperbole-circonferenza: da y=2/x si ottiene x²+4/x²=5, cioè x⁴−5x²+4=0, quindi "
      "x²=1 oppure x²=4: i punti sono (1,2) e (2,1).",
      r"x^2+\frac{4}{x^2}=5\iff x^4-5x^2+4=0\iff x^2\in\{1,4\}\ \Rightarrow\ (1,2),\ (2,1)"),
     ("D è la regione sopra l'iperbole e dentro la circonferenza: per x in [1,2] la y va da 2/x (sotto) a "
      "√(5−x²) (sopra). Dominio normale rispetto all'asse x.",
      r"D=\left\{1\le x\le2,\ \tfrac2x\le y\le\sqrt{5-x^2}\right\}")],
    "Dominio D (11 aprile 2026)")

_aggiungi(
    "9 aprile 2026", 3,
    "Dato l'integrale doppio di f(x,y)=x+y sul dominio D = {(x,y) ∈ R²: y ≥ 0; x ≥ 0; y ≥ x; y ≤ √x}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore.",
    r"y\ge0,\ x\ge0,\ y\ge x,\ y\le\sqrt x",
    x + y,
    [dict(ext=(x, 0, 1), int=(x, sp.sqrt(x)))],
    [x, y, y - x, sp.sqrt(x) - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x, "y=x"), (y - sp.sqrt(x), "y=√x")],
    [(0, 0, "O"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x è la bisettrice; y=√x è il ramo superiore della parabola "
      "x=y² (concava, passa per (0,0) e (1,1), tangente verticale in O).",
      r"y=x,\qquad y=\sqrt x\iff x=y^2\ (y\ge0)"),
     ("intersezione: √x=x ⇒ x=0 oppure x=1 (punti O(0,0) e (1,1)). Per 0<x<1 si ha √x>x (es. x=1/4: "
      "1/2>1/4), quindi y va dalla bisettrice (sotto) alla radice (sopra).",
      r"\sqrt x=x\iff x=x^2\iff x(x-1)=0\iff x=0\ \text{o}\ x=1"),
     ("D è normale rispetto all'asse x: un solo pezzo.",
      r"D=\{0\le x\le1,\ x\le y\le\sqrt x\}")],
    "Dominio D (9 aprile 2026)")

_aggiungi(
    "10 aprile 2026", 3,
    "Dato l'integrale doppio di f(x,y)=x sul dominio D = {(x,y) ∈ R²: x²+y² ≤ 1; y ≥ x²-1}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore.",
    r"x^2+y^2\le1,\ y\ge x^2-1",
    x,
    [dict(ext=(x, -1, 1), int=(x**2 - 1, sp.sqrt(1 - x**2)),
          extra_est=[("l'integrando ottenuto è una funzione DISPARI di x (somma di x√(1−x²), −x³ e x) e "
                      "l'intervallo [−1,1] è simmetrico: l'integrale vale 0. (Stessa conclusione per simmetria "
                      "già dall'inizio: D è simmetrico rispetto all'asse y e f=x è dispari in x.)", None)])],
    [1 - x**2 - y**2, y - x**2 + 1], (-1.5, 1.5, -1.5, 1.5),
    [(x**2 + y**2 - 1, "x²+y²=1"), (y - x**2 + 1, "y=x²-1")],
    [(-1, 0, "(-1,0)"), (1, 0, "(1,0)"), (0, -1, "(0,-1)")],
    [("disegno e caratteristiche delle curve: x²+y²=1 è la circonferenza unitaria; y=x²−1 è una parabola con "
      "vertice in (0,−1), concavità verso l'alto, che passa per (±1,0).",
      r"x^2+y^2=1,\qquad y=x^2-1"),
     ("intersezioni: sostituendo x²=y+1 nella circonferenza si ha y²+y=0, quindi y=0 (x=±1) oppure y=−1 "
      "(x=0): la parabola tocca la circonferenza in (−1,0), (1,0) e (0,−1) e sta dentro il cerchio nel "
      "mezzo. D è il cerchio privato della parte sotto la parabola.",
      r"(y+1)+y^2=1\iff y(y+1)=0\ \Rightarrow\ y=0\ (x=\pm1),\ \ y=-1\ (x=0)"),
     ("D è normale rispetto all'asse x: per x in [−1,1] la y va da x²−1 (parabola) a √(1−x²) (semicirconferenza "
      "superiore).",
      r"D=\left\{-1\le x\le1,\ x^2-1\le y\le\sqrt{1-x^2}\right\}")],
    "Dominio D (10 aprile 2026)")


# ===========================================================================
# GENNAIO 2026
# ===========================================================================
_aggiungi(
    "14 gennaio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=xy sul dominio D = {(x,y) ∈ R²: y ≥ 0; x²+y² ≤ 2x; x²+y² ≤ 1}: "
    "a) disegnare, descrivere le caratteristiche ed evidenziare il dominio; b) calcolarne il valore. "
    "(Esercizio ripetuto anche nell'appello di aprile 2025.)",
    r"y\ge0,\ x^2+y^2\le2x,\ x^2+y^2\le1",
    x * y,
    [dict(tipo="pol", t=(0, pi / 3), r=(0, 1), etichetta="θ da 0 a π/3: il bordo è la circonferenza unitaria"),
     dict(tipo="pol", t=(pi / 3, pi / 2), r=(0, 2 * sp.cos(t_)),
          etichetta="θ da π/3 a π/2: il bordo è la circonferenza x²+y²=2x")],
    [y, 2 * x - x**2 - y**2, 1 - x**2 - y**2], (-1.2, 2.2, -0.4, 1.3),
    [(x**2 + y**2 - 1, "x²+y²=1"), ((x - 1)**2 + y**2 - 1, "x²+y²=2x"), (y, "y=0")],
    [(0, 0, "O"), (1, 0, "(1,0)"), (R(1, 2), S3 / 2, "(1/2,√3/2)")],
    [("disegno e caratteristiche delle curve: x²+y²=1 è la circonferenza di centro O e raggio 1; "
      "x²+y²=2x equivale a (x−1)²+y²=1, circonferenza di centro (1,0) e raggio 1 (passa per O). D è la "
      "parte, nel semipiano y≥0, comune ai due cerchi (lente).",
      r"x^2+y^2=1,\qquad x^2+y^2=2x\iff(x-1)^2+y^2=1"),
     ("le due circonferenze si incontrano dove 1=2x, cioè x=1/2, y=±√3/2: il punto con y>0 è (1/2,√3/2), "
      "che in polari ha θ=π/3.",
      r"x^2+y^2=1,\ \ x^2+y^2=2x\ \Rightarrow\ x=\tfrac12,\ y=\tfrac{\sqrt3}{2}\ \Rightarrow\ \theta=\tfrac\pi3"),
     ("scelgo le coordinate polari (scaletta integrale doppio, punto 3): x²+y²≤1 diventa r≤1 e x²+y²≤2x "
      "diventa r≤2cosθ; quindi r varia tra 0 e il minimo tra 1 e 2cosθ. Per θ in [0,π/3] è 2cosθ≥1 (vale r≤1), "
      "per θ in [π/3,π/2] è 2cosθ≤1 (vale r≤2cosθ): due pezzi.",
      r"r\le\min\{1,\ 2\cos\theta\},\qquad y\ge0\iff0\le\theta\le\tfrac\pi2")],
    "Dominio D, lente nel semipiano y≥0 (14 gennaio 2026)")

_aggiungi(
    "19 gennaio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=xy/√(4-y²) sul dominio D = {(x,y) ∈ R²: x ≥ 0; 0 ≤ y ≤ 1; "
    "x²+y² ≥ 4; x²+4y² ≤ 16}: a) descrivere le curve, disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"x\ge0,\ 0\le y\le1,\ x^2+y^2\ge4,\ x^2+4y^2\le16",
    x * y / sp.sqrt(4 - y**2),
    [dict(ext=(y, 0, 1), int=(sp.sqrt(4 - y**2), 2 * sp.sqrt(4 - y**2)))],
    [x, y, 1 - y, x**2 + y**2 - 4, 16 - x**2 - 4 * y**2], (-0.3, 4.4, -0.3, 2.4),
    [(x**2 + y**2 - 4, "x²+y²=4"), (x**2 + 4 * y**2 - 16, "x²+4y²=16"), (y - 1, "y=1"), (x, "x=0")],
    [(2, 0, "(2,0)"), (4, 0, "(4,0)"), (S3, 1, "(√3,1)"), (2 * S3, 1, "(2√3,1)")],
    [("disegno e caratteristiche delle curve: x²+y²=4 è la circonferenza di raggio 2; x²+4y²=16, cioè "
      "x²/16+y²/4=1, è un'ellisse con semiassi 4 (su x) e 2 (su y); y=0 e y=1 sono rette orizzontali, x=0 è "
      "l'asse y.",
      r"x^2+y^2=4,\qquad \frac{x^2}{16}+\frac{y^2}{4}=1"),
     ("D è la porzione, nella striscia 0≤y≤1 e per x≥0, compresa tra la circonferenza (interna) e l'ellisse "
      "(esterna). Risolvendo per x: dalla circonferenza x=√(4−y²), dall'ellisse x=2√(4−y²): la seconda curva è "
      "esattamente il doppio della prima!",
      r"x\ge\sqrt{4-y^2},\qquad x\le\sqrt{16-4y^2}=2\sqrt{4-y^2}"),
     ("scelgo l'ordine dx dy (dominio normale rispetto all'asse y): y tra 0 e 1 e x tra le due curve; "
      "l'integrando contiene √(4−y²), che si semplifica proprio con gli estremi in x.",
      r"D=\left\{0\le y\le1,\ \sqrt{4-y^2}\le x\le2\sqrt{4-y^2}\right\}")],
    "Dominio D (19 gennaio 2026)")

_aggiungi(
    "20 gennaio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=x·e^(2y)/(y+2) sul dominio D = {(x,y) ∈ R²: x ≥ 0; y ≥ 0; "
    "x²+y² ≥ 4; x²+4y² ≤ 16}: a) descrivere le curve, disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"x\ge0,\ y\ge0,\ x^2+y^2\ge4,\ x^2+4y^2\le16",
    x * sp.exp(2 * y) / (y + 2),
    [dict(ext=(y, 0, 2), int=(sp.sqrt(4 - y**2), 2 * sp.sqrt(4 - y**2)),
          extra_est=[("semplifico l'integranda in y: (4−y²)=(2−y)(2+y), quindi il fattore (y+2) al "
                      "denominatore si cancella e resta (3/2)(2−y)e^{2y}, integrabile per parti.",
                      r"\frac{3}{2}\cdot\frac{(2-y)(2+y)}{y+2}e^{2y}=\frac32(2-y)e^{2y}")])],
    [x, y, x**2 + y**2 - 4, 16 - x**2 - 4 * y**2], (-0.3, 4.4, -0.3, 2.4),
    [(x**2 + y**2 - 4, "x²+y²=4"), (x**2 + 4 * y**2 - 16, "x²+4y²=16"), (x, "x=0"), (y, "y=0")],
    [(2, 0, "(2,0)"), (4, 0, "(4,0)"), (0, 2, "(0,2)")],
    [("disegno e caratteristiche delle curve: x²+y²=4 è la circonferenza di raggio 2; x²+4y²=16, cioè "
      "x²/16+y²/4=1, è un'ellisse di semiassi 4 e 2; x≥0, y≥0 selezionano il I quadrante. Le due curve si "
      "toccano in (0,2).",
      r"x^2+y^2=4,\qquad \frac{x^2}{16}+\frac{y^2}{4}=1"),
     ("nel I quadrante D è la corona compresa tra circonferenza ed ellisse; per ogni y in [0,2] la x va "
      "da √(4−y²) (circonferenza) a √(16−4y²)=2√(4−y²) (ellisse). L'ordine dx dy conviene perché l'integrando "
      "ha x al numeratore e nulla altro in x.",
      r"D=\left\{0\le y\le2,\ \sqrt{4-y^2}\le x\le2\sqrt{4-y^2}\right\}")],
    "Dominio D (20 gennaio 2026)")

_aggiungi(
    "21 gennaio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=1/∛(xy) sul dominio D = {(x,y) ∈ R²: 1/2 ≤ x ≤ 1; y ≥ x²; y ≤ √x}: "
    "a) descrivere le curve, disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"\tfrac12\le x\le1,\ y\ge x^2,\ y\le\sqrt x",
    x**(-R(1, 3)) * y**(-R(1, 3)),
    [dict(ext=(x, R(1, 2), 1), int=(x**2, sp.sqrt(x)))],
    [x - R(1, 2), 1 - x, y - x**2, sp.sqrt(x) - y], (0.0, 1.3, 0.0, 1.3),
    [(y - x**2, "y=x²"), (y - sp.sqrt(x), "y=√x"), (x - R(1, 2), "x=1/2"), (x - 1, "x=1")],
    [(R(1, 2), R(1, 4), "(1/2,1/4)"), (R(1, 2), S2 / 2, "(1/2,√2/2)"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x² è una parabola (convessa) e y=√x il suo 'riflesso' "
      "rispetto alla bisettrice (x=y²); si incontrano in (0,0) e (1,1). x=1/2 e x=1 sono rette verticali.",
      r"y=x^2,\qquad y=\sqrt x,\qquad x=\tfrac12,\quad x=1"),
     ("per 1/2≤x≤1 si ha x²≤√x, quindi y va dalla parabola (sotto) alla radice (sopra); D è la porzione di "
      "'lente' tra le due curve a destra della retta x=1/2.",
      r"D=\left\{\tfrac12\le x\le1,\ x^2\le y\le\sqrt x\right\}"),
     ("riscrivo l'integranda come prodotto di potenze, 1/∛(xy)=x^{−1/3}y^{−1/3}: integrando rispetto a y "
      "tratto x^{−1/3} come costante.",
      r"\frac{1}{\sqrt[3]{xy}}=x^{-1/3}\,y^{-1/3}")],
    "Dominio D (21 gennaio 2026)", f_latex=r"\frac{1}{\sqrt[3]{xy}}")

_aggiungi(
    "24 gennaio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=1/(1+x²) sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1; y ≥ 2x-2; y ≤ x²-1}: "
    "a) descrivere le curve, disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"0\le x\le1,\ y\ge2x-2,\ y\le x^2-1",
    1 / (1 + x**2),
    [dict(ext=(x, 0, 1), int=(2 * x - 2, x**2 - 1),
          extra_est=[("l'altezza (x²−1)−(2x−2)=(x−1)² è un quadrato: l'integrando diventa (1−x)²/(1+x²) e "
                      "si spezza con la divisione (1−2x+x²)/(1+x²)=1−2x/(1+x²).",
                      r"\frac{(x-1)^2}{1+x^2}=\frac{x^2+1-2x}{1+x^2}=1-\frac{2x}{1+x^2}")])],
    [x, 1 - x, y - 2 * x + 2, x**2 - 1 - y], (-0.3, 1.4, -2.4, 0.4),
    [(y - 2 * x + 2, "y=2x-2"), (y - x**2 + 1, "y=x²-1"), (x, "x=0"), (x - 1, "x=1")],
    [(0, -2, "(0,-2)"), (0, -1, "(0,-1)"), (1, 0, "(1,0)")],
    [("disegno e caratteristiche delle curve: y=2x−2 è una retta di pendenza 2 (passa per (0,−2) e (1,0)); "
      "y=x²−1 è una parabola con vertice (0,−1) che passa per (1,0); x=0 e x=1 sono rette verticali.",
      r"y=2x-2,\qquad y=x^2-1"),
     ("confronto delle due curve: (x²−1)−(2x−2)=x²−2x+1=(x−1)²≥0, quindi la parabola sta SOPRA la retta per "
      "ogni x e le due curve si toccano soltanto in x=1 (punto (1,0), dove sono anche tangenti: stessa "
      "pendenza 2). D è una regione a forma di 'spicchio' chiusa a sinistra da x=0.",
      r"x^2-1-(2x-2)=(x-1)^2\ge0,\qquad y'_{\text{parab.}}(1)=2=y'_{\text{retta}}"),
     ("D è normale rispetto all'asse x con un solo pezzo.",
      r"D=\left\{0\le x\le1,\ 2x-2\le y\le x^2-1\right\}")],
    "Dominio D (24 gennaio 2026)")


# ===========================================================================
# MAGGIO 2026
# ===========================================================================
_aggiungi(
    "15 maggio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=x/y sul dominio D = {(x,y) ∈ R²: log y ≤ x ≤ y, 2 ≤ y ≤ 3}: "
    "disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore. "
    "(Esercizio ripetuto anche nell'appello del 7 maggio 2026 e del 16 settembre 2025.)",
    r"\ln y\le x\le y,\ 2\le y\le3",
    x / y,
    [dict(ext=(y, 2, 3), int=(sp.log(y), y))],
    [y - 2, 3 - y, x - sp.log(y), y - x], (-0.2, 3.5, 1.5, 3.5),
    [(x - sp.log(y), "x=ln y"), (x - y, "x=y"), (y - 2, "y=2"), (y - 3, "y=3")],
    [(sp.log(2), 2, "(ln2,2)"), (2, 2, "(2,2)"), (sp.log(3), 3, "(ln3,3)"), (3, 3, "(3,3)")],
    [("disegno e caratteristiche delle curve: x=ln y è la funzione inversa dell'esponenziale scritta come x "
      "in funzione di y (logaritmo naturale, crescente e concava, passa per (0,1)); x=y è la bisettrice; "
      "y=2 e y=3 sono rette orizzontali. (Il simbolo 'log' è il logaritmo naturale.)",
      r"x=\ln y,\qquad x=y,\qquad y=2,\quad y=3"),
     ("per 2≤y≤3 si ha ln y<y (ln 2≈0,69<2; ln 3≈1,10<3), quindi x va dalla curva logaritmica (a sinistra) alla "
      "bisettrice (a destra): D è un dominio normale rispetto all'asse y, scritto già nella forma giusta.",
      r"D=\{2\le y\le3,\ \ln y\le x\le y\}"),
     ("scelgo l'ordine dx dy (y esterna, x interna): l'integrando x/y ha x a numeratore, quindi la primitiva in "
      "x è x²/(2y) e si valuta senza difficoltà agli estremi ln y e y.",
      r"\int\frac{x}{y}\,dx=\frac{x^2}{2y}")],
    "Dominio D (15 maggio 2026)")

_aggiungi(
    "9 maggio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=(x/y)·e^y sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1; y ≥ x²; y ≤ x}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore. "
    "(Esercizio ripetuto anche a dicembre 2023.)",
    r"0\le x\le1,\ y\ge x^2,\ y\le x",
    x / y * sp.exp(y),
    [dict(ext=(y, 0, 1), int=(y, sp.sqrt(y)))],
    [x, 1 - x, y - x**2, x - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x**2, "y=x²"), (y - x, "y=x"), (x - 1, "x=1")],
    [(0, 0, "O"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x² è una parabola (convessa) e y=x la bisettrice; si "
      "incontrano in (0,0) e (1,1) e per 0<x<1 la parabola sta SOTTO la bisettrice. D è lo spicchio "
      "compreso tra le due curve.",
      r"y=x^2,\qquad y=x,\qquad x^2\le y\le x"),
     ("scambio l'ordine d'integrazione (scaletta integrale doppio, punto 3): con dy dx l'integrale interno è "
      "∫ e^y/y dy, che NON ha primitiva elementare. Riscrivo D come dominio normale rispetto all'asse y: "
      "da y≤x e y≥x² si ha y≤x≤√y, con y in [0,1]; integrando prima in x si ottiene x/y·e^y → primitiva "
      "x²/(2y)·e^y.",
      r"x^2\le y\le x\iff y\le x\le\sqrt y,\qquad D=\left\{0\le y\le1,\ y\le x\le\sqrt y\right\}")],
    "Dominio D (9 maggio 2026)")

_aggiungi(
    "11 maggio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=x·√(x²+y²) sul dominio D = {(x,y) ∈ R²: x ≤ 0; y ≥ 0; x²+y² ≤ 1; "
    "x²+y² ≤ 2y}: a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; "
    "b) calcolarne il valore. (Esercizio ripetuto anche ad aprile 2025 e, con un refuso, a maggio 2024.)",
    r"x\le0,\ y\ge0,\ x^2+y^2\le1,\ x^2+y^2\le2y",
    x * sp.sqrt(x**2 + y**2),
    [dict(tipo="pol", t=(pi / 2, 5 * pi / 6), r=(0, 1), etichetta="θ da π/2 a 5π/6: il bordo è x²+y²=1"),
     dict(tipo="pol", t=(5 * pi / 6, pi), r=(0, 2 * sp.sin(t_)), etichetta="θ da 5π/6 a π: il bordo è x²+y²=2y")],
    [-x, y, 1 - x**2 - y**2, 2 * y - x**2 - y**2], (-1.4, 0.4, -0.3, 2.3),
    [(x**2 + y**2 - 1, "x²+y²=1"), (x**2 + (y - 1)**2 - 1, "x²+y²=2y"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (-1, 0, "(-1,0)"), (-S3 / 2, R(1, 2), "(-√3/2,1/2)"), (0, 1, "(0,1)")],
    [("disegno e caratteristiche delle curve: x²+y²=1 è la circonferenza unitaria; x²+y²=2y equivale a "
      "x²+(y−1)²=1, circonferenza di centro (0,1) e raggio 1 (passa per O e (0,2)); x≤0 è il semipiano "
      "sinistro. La condizione y≥0 è già implicata dalla seconda disequazione (2y≥x²+y²≥0).",
      r"x^2+y^2=1,\qquad x^2+y^2=2y\iff x^2+(y-1)^2=1"),
     ("le due circonferenze si incontrano dove 1=2y, cioè y=1/2, x=±√3/2: nel semipiano x≤0 il punto è "
      "(−√3/2,1/2), che in polari ha θ=5π/6 (cosθ=−√3/2, sinθ=1/2).",
      r"y=\tfrac12,\ x=-\tfrac{\sqrt3}{2}\ \Rightarrow\ \theta=\tfrac{5\pi}{6}"),
     ("scelgo le coordinate polari (scaletta integrale doppio, punto 3): x²+y²≤1 ⇒ r≤1 e x²+y²≤2y ⇒ "
      "r≤2sinθ, quindi r≤min{1,2sinθ}; x≤0 e y≥0 danno θ in [π/2,π]. Per θ in [π/2,5π/6] è 2sinθ≥1 (vale "
      "r≤1); per θ in [5π/6,π] è 2sinθ≤1 (vale r≤2sinθ): due pezzi.",
      r"r\le\min\{1,2\sin\theta\},\qquad \tfrac\pi2\le\theta\le\pi"),
     ("l'integranda in polari: x√(x²+y²)=r cosθ·r=r²cosθ, e col fattore r dell'elemento d'area diventa "
      "r³cosθ.", r"x\sqrt{x^2+y^2}\,dx\,dy=r\cos\theta\cdot r\cdot r\,dr\,d\theta=r^3\cos\theta\,dr\,d\theta")],
    "Dominio D (11 maggio 2026)")

_aggiungi(
    "14 maggio 2026", 3,
    "Dato l'integrale doppio di f(x,y)=3y sul dominio D = {(x,y) ∈ R²: x ≥ 0; y ≥ 0; x²+y² ≤ 3; y ≥ √(2x)}: "
    "a) disegnare, descrivere le caratteristiche delle curve ed evidenziare il dominio; b) calcolarne il valore. "
    "(Esercizio ripetuto anche il 13 dicembre 2025.)",
    r"x\ge0,\ y\ge0,\ x^2+y^2\le3,\ y\ge\sqrt{2x}",
    3 * y,
    [dict(ext=(x, 0, 1), int=(sp.sqrt(2 * x), sp.sqrt(3 - x**2)))],
    [x, y, 3 - x**2 - y**2, y - sp.sqrt(2 * x)], (-0.2, 2.0, -0.2, 2.0),
    [(x**2 + y**2 - 3, "x²+y²=3"), (y - sp.sqrt(2 * x), "y=√(2x)"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (0, S3, "(0,√3)"), (1, S2, "(1,√2)")],
    [("disegno e caratteristiche delle curve: x²+y²=3 è la circonferenza di centro O e raggio √3; "
      "y=√(2x) è il ramo superiore della parabola y²=2x (asse orizzontale, vertice in O); x≥0,y≥0 selezionano "
      "il I quadrante.",
      r"x^2+y^2=3,\qquad y=\sqrt{2x}\iff y^2=2x\ (y\ge0)"),
     ("intersezione: da y²=2x nella circonferenza x²+2x=3, cioè x²+2x−3=0, quindi x=1 (l'altra radice x=−3 "
      "non è accettabile) e y=√2. D è la regione sopra la parabola e dentro il cerchio, nel I quadrante.",
      r"x^2+2x-3=0\iff(x+3)(x-1)=0\ \Rightarrow\ x=1,\ y=\sqrt2"),
     ("per x in [0,1] la y va da √(2x) (parabola, sotto) a √(3−x²) (circonferenza, sopra); per x>1 la parabola "
      "supera la circonferenza e non c'è più dominio. Dominio normale rispetto all'asse x.",
      r"D=\left\{0\le x\le1,\ \sqrt{2x}\le y\le\sqrt{3-x^2}\right\}")],
    "Dominio D (14 maggio 2026)")


# ===========================================================================
# DICEMBRE 2025
# ===========================================================================
_aggiungi(
    "1 dicembre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=-e^(x+y) sul dominio D = triangolo di vertici O(0,0), A(0,π), B(2π,0): "
    "a) disegnare ed evidenziare il dominio; b) calcolarne il valore. (Esercizio ripetuto anche ad aprile 2025.)",
    r"\text{triangolo di vertici } O(0,0),\,A(0,\pi),\,B(2\pi,0)",
    -sp.exp(x + y),
    [dict(ext=(x, 0, 2 * pi), int=(0, pi - x / 2),
          extra_est=[("l'integrale in x si spezza in due esponenziali elementari: −e^{π}e^{x/2}+e^{x}; "
                      "ricordo ∫e^{kx}dx=e^{kx}/k.", None)])],
    [x, y, pi - x / 2 - y], (-0.6, 7.0, -0.6, 3.8),
    [(y - pi + x / 2, "retta AB: y=π-x/2"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (0, pi, "A(0,π)"), (2 * pi, 0, "B(2π,0)")],
    [("disegno e caratteristiche delle curve: i lati del triangolo sono l'asse y (OA), l'asse x (OB) e la "
      "retta AB, che passa per A(0,π) e B(2π,0): pendenza (0−π)/(2π−0)=−1/2, cioè y=π−x/2.",
      r"OA:\ x=0,\qquad OB:\ y=0,\qquad AB:\ y=\pi-\frac{x}{2}"),
     ("D è normale rispetto all'asse x: per x in [0,2π] la y va dal lato OB (y=0) alla retta AB.",
      r"D=\left\{0\le x\le2\pi,\ 0\le y\le\pi-\tfrac x2\right\}")],
    "Dominio D: triangolo (1 dicembre 2025)", f_latex=r"-e^{x+y}")

_aggiungi(
    "2 dicembre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=2x sul dominio D = {(x,y) ∈ R²: x ≥ 0; y ≥ √3/2; x²/4+y² ≤ 1}: "
    "disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore. "
    "(Esercizio ripetuto anche ad aprile 2025.)",
    r"x\ge0,\ y\ge\tfrac{\sqrt3}{2},\ \tfrac{x^2}{4}+y^2\le1",
    2 * x,
    [dict(ext=(y, S3 / 2, 1), int=(0, 2 * sp.sqrt(1 - y**2)))],
    [x, y - S3 / 2, 1 - x**2 / 4 - y**2], (-0.3, 2.4, 0.0, 1.3),
    [(x**2 / 4 + y**2 - 1, "x²/4+y²=1"), (y - S3 / 2, "y=√3/2"), (x, "x=0")],
    [(0, S3 / 2, "(0,√3/2)"), (0, 1, "(0,1)"), (1, S3 / 2, "(1,√3/2)")],
    [("disegno e caratteristiche delle curve: x²/4+y²=1 è un'ellisse di centro O con semiassi 2 (lungo x) e "
      "1 (lungo y); y=√3/2≈0,87 è una retta orizzontale; x=0 è l'asse y.",
      r"\frac{x^2}{4}+y^2=1,\qquad y=\frac{\sqrt3}{2},\qquad x=0"),
     ("intersezione retta-ellisse: con y=√3/2 si ha x²/4=1−3/4=1/4, quindi x=±1; nel semipiano x≥0 il "
      "punto è (1,√3/2). D è il 'segmento ellittico' (calotta) sopra la retta, nella parte destra x≥0.",
      r"\frac{x^2}{4}=1-\frac34=\frac14\ \Rightarrow\ x=1"),
     ("scelgo l'ordine dx dy (dominio normale rispetto all'asse y): per y in [√3/2,1] la x va da 0 a "
      "2√(1−y²) (dall'ellisse, x=2√(1−y²)). L'integrando 2x ha primitiva immediata in x.",
      r"D=\left\{\tfrac{\sqrt3}{2}\le y\le1,\ 0\le x\le2\sqrt{1-y^2}\right\}")],
    "Dominio D (2 dicembre 2025)")

_aggiungi(
    "9 dicembre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=x+2y sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 2; min{x²,x} ≤ y ≤ "
    "max{x²,x}}: a) disegnare, descrivere le caratteristiche ed evidenziare il dominio; b) calcolarne il valore. "
    "(Esercizio ripetuto anche il 3 dicembre 2025, a dicembre 2024 e a gennaio 2024.)",
    r"0\le x\le2,\ \min\{x^2,x\}\le y\le\max\{x^2,x\}",
    x + 2 * y,
    [dict(ext=(x, 0, 1), int=(x**2, x), etichetta="x in [0,1]: la parabola sta sotto la retta"),
     dict(ext=(x, 1, 2), int=(x, x**2), etichetta="x in [1,2]: la retta sta sotto la parabola")],
    [x, 2 - x, -(y - x**2) * (y - x)], (-0.2, 2.3, -0.3, 4.4),
    [(y - x**2, "y=x²"), (y - x, "y=x"), (x - 2, "x=2")],
    [(0, 0, "O"), (1, 1, "(1,1)"), (2, 2, "(2,2)"), (2, 4, "(2,4)")],
    [("disegno e caratteristiche delle curve: y=x² è una parabola con vertice in O; y=x è la bisettrice; "
      "x=0 e x=2 sono rette verticali. Le due curve si incontrano per x²=x, cioè in (0,0) e (1,1).",
      r"y=x^2,\qquad y=x,\qquad x^2=x\iff x=0\ \text{o}\ x=1"),
     ("il min e il max cambiano ruolo in x=1: per 0≤x≤1 si ha x²≤x (min=x², max=x); per 1≤x≤2 si ha x≤x² "
      "(min=x, max=x²). D è quindi l'unione di due 'spicchi' (uno tra le curve per x in [0,1] e uno per "
      "x in [1,2]) e va scomposto in DUE pezzi.",
      r"D=\{0\le x\le1,\ x^2\le y\le x\}\ \cup\ \{1\le x\le2,\ x\le y\le x^2\}")],
    "Dominio D (9 dicembre 2025)", pdf_R=R(11, 2))

_aggiungi(
    "4 dicembre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=x² sul dominio D = {(x,y) ∈ R²: y ≤ -x²+x/2+3; y ≥ -x²-x; y ≥ -x²+2x}: "
    "disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore. [Nota: nel testo "
    "stampato la prima disequazione compare con ≥, ma con tre ≥ il dominio sarebbe illimitato e l'integrale "
    "divergerebbe; con y ≤ −x²+x/2+3 si ottiene il risultato ufficiale R=4 dell'appello di aprile 2024, in cui "
    "compare lo stesso esercizio.]",
    r"y\le-x^2+\tfrac x2+3,\ y\ge-x^2-x,\ y\ge-x^2+2x",
    x**2,
    [dict(ext=(x, -2, 0), int=(-x**2 - x, -x**2 + x / 2 + 3), etichetta="x in [−2,0]: il bordo inferiore è y=−x²−x"),
     dict(ext=(x, 0, 2), int=(-x**2 + 2 * x, -x**2 + x / 2 + 3), etichetta="x in [0,2]: il bordo inferiore è y=−x²+2x")],
    [-x**2 + x / 2 + 3 - y, y + x**2 + x, y + x**2 - 2 * x], (-2.6, 2.6, -4.6, 3.8),
    [(y + x**2 - x / 2 - 3, "y=-x²+x/2+3"), (y + x**2 + x, "y=-x²-x"), (y + x**2 - 2 * x, "y=-x²+2x")],
    [(-2, -2, "(-2,-2)"), (0, 0, "(0,0)"), (2, 0, "(2,0)")],
    [("disegno e caratteristiche delle curve: sono tre parabole con la STESSA concavità (verso il basso, "
      "coefficiente −1 di x²), cioè traslate l'una dell'altra: y=−x²+x/2+3, y=−x²−x, y=−x²+2x. Conviene "
      "sottrarre −x² a tutto: y+x²=z diventa la regione tra le rette z=x/2+3 (sopra) e z=max{−x, 2x} (sotto).",
      r"y+x^2\le\tfrac x2+3,\qquad y+x^2\ge-x,\qquad y+x^2\ge2x"),
     ("intersezioni: −x=x/2+3 ⇒ x=−2 (punto (−2,−2)); 2x=x/2+3 ⇒ x=2 (punto (2,0)); −x=2x ⇒ x=0 "
      "(punto (0,0)). Per x≤0 è max{−x,2x}=−x; per x≥0 è max{−x,2x}=2x.",
      r"-x=\tfrac x2+3\Rightarrow x=-2,\quad 2x=\tfrac x2+3\Rightarrow x=2,\quad -x=2x\Rightarrow x=0"),
     ("D va scomposto in due pezzi (a sinistra e a destra di x=0) perché cambia la curva che fa da bordo "
      "inferiore; il bordo superiore è sempre y=−x²+x/2+3.",
      r"D=\{-2\le x\le0,\ -x^2-x\le y\le-x^2+\tfrac x2+3\}\cup\{0\le x\le2,\ -x^2+2x\le y\le-x^2+\tfrac x2+3\}")],
    "Dominio D (4 dicembre 2025)", pdf_R=4, f_latex="x^2")

_aggiungi(
    "5 dicembre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=2x/(4-y) sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1; x² ≤ y ≤ min{2x,1}}: "
    "disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore. "
    "(Esercizio ripetuto anche a luglio 2024, dicembre 2024 e gennaio 2024.)",
    r"0\le x\le1,\ x^2\le y\le\min\{2x,1\}",
    2 * x / (4 - y),
    [dict(ext=(y, 0, 1), int=(y / 2, sp.sqrt(y)))],
    [x, 1 - x, y - x**2, 2 * x - y, 1 - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x**2, "y=x²"), (y - 2 * x, "y=2x"), (y - 1, "y=1")],
    [(0, 0, "O"), (R(1, 2), 1, "(1/2,1)"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x² è una parabola con vertice in O; y=2x è una retta per O di "
      "pendenza 2; y=1 è una retta orizzontale. La retta e la parabola si incontrano in (0,0) e (2,4) (fuori "
      "dalla striscia 0≤x≤1); la retta incontra y=1 in (1/2,1) e la parabola incontra y=1 in (1,1).",
      r"y=x^2,\qquad y=2x,\qquad y=1"),
     ("il limite superiore min{2x,1} vale 2x per x≤1/2 e vale 1 per x≥1/2: scrivendo D come dominio "
      "normale rispetto a x servirebbero due pezzi. Scambio l'ordine d'integrazione (scaletta integrale "
      "doppio, punto 3): per ogni y in [0,1] la x va dalla retta (x=y/2, perché y≤2x) alla parabola "
      "(x=√y, perché y≥x²): un solo pezzo.",
      r"y\le2x\iff x\ge\tfrac y2,\quad y\ge x^2\iff x\le\sqrt y\ \Rightarrow\ D=\{0\le y\le1,\ \tfrac y2\le x\le\sqrt y\}")],
    "Dominio D (5 dicembre 2025)", pdf_R=R(1, 8))


# ===========================================================================
# SETTEMBRE - OTTOBRE 2025 (e luglio 2025)
# ===========================================================================
_aggiungi(
    "18 ottobre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=y sul dominio D = {(x,y) ∈ R²: x ≥ 0; y ≥ √3·x; x²+y² ≤ 36; "
    "x²+y²-4x ≥ 0}: disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore.",
    r"x\ge0,\ y\ge\sqrt3\,x,\ x^2+y^2\le36,\ x^2+y^2-4x\ge0",
    y,
    [dict(tipo="pol", t=(pi / 3, pi / 2), r=(4 * sp.cos(t_), 6))],
    [x, y - S3 * x, 36 - x**2 - y**2, x**2 + y**2 - 4 * x], (-0.6, 6.6, -0.6, 6.6),
    [(x**2 + y**2 - 36, "x²+y²=36"), ((x - 2)**2 + y**2 - 4, "x²+y²=4x"), (y - S3 * x, "y=√3 x"), (x, "x=0")],
    [(0, 0, "O"), (0, 6, "(0,6)"), (3, 3 * S3, "(3,3√3)"), (1, S3, "(1,√3)")],
    [("disegno e caratteristiche delle curve: x²+y²=36 è la circonferenza di centro O e raggio 6; "
      "x²+y²−4x=0 equivale a (x−2)²+y²=4, circonferenza di centro (2,0) e raggio 2 (passa per O e (4,0)); "
      "y=√3x è la retta per O di pendenza √3, cioè inclinata di 60° (θ=π/3); x=0 è l'asse y.",
      r"x^2+y^2=36,\qquad x^2+y^2-4x=0\iff(x-2)^2+y^2=4,\qquad y=\sqrt3\,x"),
     ("D è la regione nel I quadrante sopra la retta y=√3x, dentro la circonferenza grande e FUORI dal disco "
      "piccolo (x²+y²−4x≥0). La retta incontra il disco piccolo in O e in (1,√3) (θ=π/3).",
      r"y\ge\sqrt3x\iff\theta\ge\tfrac\pi3,\qquad x\ge0,\ y\ge0\ \Rightarrow\ \theta\le\tfrac\pi2"),
     ("scelgo le coordinate polari (scaletta integrale doppio, punto 3): x²+y²≤36 ⇒ r≤6; x²+y²−4x≥0 ⇒ "
      "r²≥4r cosθ ⇒ r≥4cosθ; θ varia tra π/3 e π/2 (retta y=√3x e asse y). Nell'intervallo si ha "
      "4cosθ≤2<6: l'estremo inferiore è sempre minore del superiore.",
      r"\tfrac\pi3\le\theta\le\tfrac\pi2,\qquad 4\cos\theta\le r\le6")],
    "Dominio D (18 ottobre 2025)")

_aggiungi(
    "21 ottobre 2025", 3,
    "Dato l'integrale doppio di f(x,y)=6xy²+log x sul dominio D = {(x,y) ∈ R²: 1 ≤ x ≤ e; 0 ≤ y ≤ x}: "
    "disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore.",
    r"1\le x\le e,\ 0\le y\le x",
    6 * x * y**2 + sp.log(x),
    [dict(ext=(x, 1, E), int=(0, x),
          extra_est=[("per l'ultimo integrale servono ∫x⁴dx=x⁵/5 e, per parti, ∫x ln x dx=(x²/2)ln x − x²/4 "
                      "(derivata di (x²/2)ln x = x ln x + x/2).",
                      r"\int x\ln x\,dx=\frac{x^2}{2}\ln x-\frac{x^2}{4}")])],
    [x - 1, E - x, y, x - y], (-0.3, 3.2, -0.3, 3.2),
    [(y - x, "y=x"), (y, "y=0"), (x - 1, "x=1"), (x - E, "x=e")],
    [(1, 0, "(1,0)"), (E, 0, "(e,0)"), (1, 1, "(1,1)"), (E, E, "(e,e)")],
    [("disegno e caratteristiche delle curve: x=1 e x=e sono rette verticali (e≈2,718); y=0 è l'asse x; "
      "y=x è la bisettrice. D è un trapezio con vertici (1,0), (e,0), (e,e), (1,1).",
      r"x=1,\quad x=e,\quad y=0,\quad y=x"),
     ("D è normale rispetto all'asse x: per x in [1,e] la y va da 0 a x. Integro prima in y (le potenze di y "
      "e il termine ln x, costante in y, sono immediati).",
      r"D=\{1\le x\le e,\ 0\le y\le x\}")],
    "Dominio D, trapezio (21 ottobre 2025)")

_aggiungi(
    "11 settembre 2025", 3,
    "Calcolare l'integrale doppio di f(x,y)=4x²+2y sul dominio D = quadrilatero di vertici O(0,0), "
    "A(3/2,3/2), B(1/2,5/2), C(-1,1). È obbligatorio il disegno del dominio. "
    "(Esercizio ripetuto anche a dicembre 2023.)",
    r"\text{quadrilatero di vertici } O(0,0),\,A(\tfrac32,\tfrac32),\,B(\tfrac12,\tfrac52),\,C(-1,1)",
    4 * x**2 + 2 * y,
    [dict(tipo="cv", xy=((w_ - u_) / 2, (u_ + w_) / 2), ext=(u_, 0, 2), int=(w_, 0, 3),
          testo_sost="pongo u=y−x e w=x+y, da cui x=(w−u)/2 e y=(u+w)/2",
          lat_sost=r"u=y-x,\ w=x+y\ \Rightarrow\ x=\frac{w-u}{2},\ y=\frac{u+w}{2}",
          testo_dom="il rettangolo 0≤u≤2, 0≤w≤3")],
    [y - x, 2 - y + x, x + y, 3 - x - y], (-1.6, 2.2, -0.4, 3.0),
    [(y - x, "OA: y=x"), (y - x - 2, "CB: y=x+2"), (y + x, "OC: y=-x"), (y + x - 3, "AB: y=3-x")],
    [(0, 0, "O"), (R(3, 2), R(3, 2), "A(3/2,3/2)"), (R(1, 2), R(5, 2), "B(1/2,5/2)"), (-1, 1, "C(-1,1)")],
    [("disegno e caratteristiche delle curve: i lati sono le rette per due vertici consecutivi. OA: pendenza "
      "(3/2)/(3/2)=1, y=x. AB: pendenza (5/2−3/2)/(1/2−3/2)=−1, y=3−x. BC: pendenza (1−5/2)/(−1−1/2)=1, "
      "y=x+2. CO: pendenza −1, y=−x.",
      r"OA:\ y=x,\quad AB:\ y=3-x,\quad BC:\ y=x+2,\quad CO:\ y=-x"),
     ("OA ∥ BC (pendenza 1) e AB ∥ CO (pendenza −1), e le due direzioni sono perpendicolari (1·(−1)=−1): "
      "D è un RETTANGOLO inclinato di 45°. Conviene un cambio di variabili lineare che lo raddrizza: "
      "u=y−x vale 0 su OA e 2 su BC; w=x+y vale 0 su CO e 3 su AB.",
      r"0\le y-x\le2,\qquad 0\le x+y\le3")],
    "Dominio D, rettangolo inclinato (11 settembre 2025)")

_aggiungi(
    "13 settembre 2025", 3,
    "Sia dato l'integrale doppio di f(x,y)=1 (area di D) dove D è la parte di piano del I quadrante delimitata "
    "dalle curve y=x², x=y², 8xy<1. Disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne "
    "il valore. (Esercizio ripetuto anche a ottobre 2023.)",
    r"y\ge x^2,\ x\ge y^2,\ 8xy\le1\ (x,y\ge0)",
    sp.Integer(1),
    [dict(ext=(x, 0, R(1, 4)), int=(x**2, sp.sqrt(x)), etichetta="x in [0,1/4]: tetto la parabola x=y²"),
     dict(ext=(x, R(1, 4), R(1, 2)), int=(x**2, 1 / (8 * x)), etichetta="x in [1/4,1/2]: tetto l'iperbole 8xy=1")],
    [x, y, y - x**2, x - y**2, 1 - 8 * x * y], (-0.05, 0.75, -0.05, 0.75),
    [(y - x**2, "y=x²"), (x - y**2, "x=y²"), (8 * x * y - 1, "8xy=1")],
    [(0, 0, "O"), (R(1, 2), R(1, 4), "(1/2,1/4)"), (R(1, 4), R(1, 2), "(1/4,1/2)")],
    [("disegno e caratteristiche delle curve: y=x² è una parabola ad asse verticale, x=y² è la parabola "
      "simmetrica (asse orizzontale); tra loro delimitano una 'lente' da (0,0) a (1,1) nel I quadrante. "
      "8xy=1 è l'iperbole equilatera y=1/(8x) (rami nel I e III quadrante).",
      r"y=x^2,\qquad x=y^2,\qquad xy=\tfrac18"),
     ("l'iperbole 'taglia' la lente: interseco con y=x² ⇒ 8x³=1 ⇒ x=1/2, y=1/4; interseco con x=y² ⇒ "
      "y=1/2, x=1/4. La parte con 8xy<1 è quella vicina all'origine, delimitata dai tre archi tra O, (1/2,1/4) e "
      "(1/4,1/2).",
      r"8x\cdot x^2=1\Rightarrow(\tfrac12,\tfrac14),\qquad 8y^2\cdot y=1\Rightarrow(\tfrac14,\tfrac12)"),
     ("descrizione a dominio normale rispetto all'asse x: la y parte sempre dalla parabola y=x². Per x in [0,1/4] "
      "il tetto è y=√x (parabola x=y²), perché l'iperbole sta più in alto; per x in [1/4,1/2] il tetto "
      "diventa l'iperbole y=1/(8x). Due pezzi. Per x>1/2 non c'è dominio (l'iperbole è sotto y=x²).",
      r"D=\{0\le x\le\tfrac14,\ x^2\le y\le\sqrt x\}\cup\{\tfrac14\le x\le\tfrac12,\ x^2\le y\le\tfrac{1}{8x}\}")],
    "Dominio D (13 settembre 2025)", f_latex="1")

_aggiungi(
    "15 settembre 2025", 3,
    "Sia dato l'integrale doppio di f(x,y)=1/(1+x) dove D è la parte di piano delimitata dalle curve di "
    "equazione x=y² e y=x². Disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore.",
    r"y\ge x^2,\ x\ge y^2",
    1 / (1 + x),
    [dict(ext=(x, 0, 1), int=(x**2, sp.sqrt(x)),
          extra_est=[("scompongo (√x−x²)/(1+x) in due integrali. Per il secondo, la divisione dà "
                      "x²/(1+x)=x−1+1/(1+x). Per il primo pongo t=√x (x=t², dx=2t dt): "
                      "∫₀¹√x/(1+x)dx=∫₀¹2t²/(1+t²)dt=∫₀¹(2−2/(1+t²))dt=2−π/2.",
                      r"\int_0^1\frac{\sqrt x}{1+x}dx=2-\frac\pi2,\qquad \int_0^1\frac{x^2}{1+x}dx=\frac12-1+\ln2=\ln2-\frac12")])],
    [y - x**2, x - y**2], (-0.2, 1.3, -0.2, 1.3),
    [(y - x**2, "y=x²"), (x - y**2, "x=y²")],
    [(0, 0, "O"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x² è la parabola ad asse verticale (vertice O, convessa); "
      "x=y² è la parabola ad asse orizzontale; si incontrano per x=x⁴ ⇒ x=0 o x=1: nei punti (0,0) e (1,1). "
      "Tra i due punti la regione limitata è una 'lente'.",
      r"y=x^2,\qquad x=y^2,\qquad x=x^4\iff x=0\ \text{o}\ x=1"),
     ("D = {y≥x², x≥y²}: nella lente la parabola y=x² sta sotto e il ramo y=√x sta sopra. Dominio normale "
      "rispetto all'asse x; l'integrando 1/(1+x) dipende solo da x, quindi l'integrale in y è una "
      "moltiplicazione per l'altezza √x−x².",
      r"D=\{0\le x\le1,\ x^2\le y\le\sqrt x\}")],
    "Dominio D, lente (15 settembre 2025)")

_aggiungi(
    "17 settembre 2025", 3,
    "Sia dato l'integrale doppio di f(x,y)=x/y sul dominio D = {(x,y) ∈ R²: x² ≤ y ≤ x³, 1 ≤ x ≤ 2}. "
    "Disegnare il dominio descrivendo le caratteristiche delle curve e calcolarne il valore.",
    r"1\le x\le2,\ x^2\le y\le x^3",
    x / y,
    [dict(ext=(x, 1, 2), int=(x**2, x**3))],
    [x - 1, 2 - x, y - x**2, x**3 - y], (0.0, 2.6, 0.0, 9.0),
    [(y - x**2, "y=x²"), (y - x**3, "y=x³"), (x - 1, "x=1"), (x - 2, "x=2")],
    [(1, 1, "(1,1)"), (2, 4, "(2,4)"), (2, 8, "(2,8)")],
    [("disegno e caratteristiche delle curve: y=x² è la parabola; y=x³ è la parabola cubica; x=1 e x=2 sono "
      "rette verticali. Per x≥1 si ha x³≥x² (si toccano in (0,0) e (1,1)), quindi y va da x² (sotto) a x³ (sopra): "
      "D è la regione 'a corno' tra le due curve per 1≤x≤2.",
      r"x^3\ge x^2\iff x^2(x-1)\ge0\iff x\ge1\ (\text{o } x=0)"),
     ("D è già scritto come dominio normale rispetto all'asse x. L'integrando x/y ha primitiva logaritmica in y: "
      "x·ln y (y>0).",
      r"D=\{1\le x\le2,\ x^2\le y\le x^3\}")],
    "Dominio D (17 settembre 2025)")

_aggiungi(
    "23 luglio 2025", 2,
    "Calcolare l'integrale doppio di f(x,y)=xy²+e^x sul dominio D = triangolo di vertici O(0,0), A(-2,3), "
    "B(2,3).",
    r"\text{triangolo di vertici } O(0,0),\,A(-2,3),\,B(2,3)",
    x * y**2 + sp.exp(x),
    [dict(ext=(y, 0, 3), int=(-2 * y / 3, 2 * y / 3),
          extra_est=[("osservazione: l'intervallo di x è simmetrico rispetto a 0, quindi la parte dispari "
                      "x y² dà contributo nullo (x²y²/2 vale lo stesso in ±2y/3), e resta solo "
                      "[e^x] tra −2y/3 e 2y/3.", None)])],
    [y, 3 - y, 2 * y / 3 - x, 2 * y / 3 + x], (-2.8, 2.8, -0.4, 3.5),
    [(y - 3 * x / 2, "OB: y=3x/2"), (y + 3 * x / 2, "OA: y=-3x/2"), (y - 3, "AB: y=3")],
    [(0, 0, "O"), (-2, 3, "A(-2,3)"), (2, 3, "B(2,3)")],
    [("disegno e caratteristiche delle curve: il lato AB è la retta orizzontale y=3; OA passa per O e "
      "A(−2,3): pendenza −3/2, y=−3x/2; OB passa per O e B(2,3): pendenza 3/2, y=3x/2. Il triangolo è "
      "isoscele e simmetrico rispetto all'asse y, con vertice in O.",
      r"AB:\ y=3,\qquad OA:\ y=-\tfrac32x,\qquad OB:\ y=\tfrac32x"),
     ("scrivo D come dominio normale rispetto all'asse y (un solo pezzo): per y in [0,3] la x va da "
      "x=−2y/3 (lato OA) a x=2y/3 (lato OB). Con dx dy servirebbero due pezzi (x in [−2,0] e [0,2]).",
      r"D=\{0\le y\le3,\ -\tfrac{2y}{3}\le x\le\tfrac{2y}{3}\}")],
    "Dominio D: triangolo (23 luglio 2025)")


# ===========================================================================
# APRILE 2025, GENNAIO 2025
# ===========================================================================
_aggiungi(
    "aprile 2025", 3,
    "Dato l'integrale doppio di f(x,y)=cos(y²)/y dove D è la parte di piano del primo quadrante compresa tra le "
    "curve di equazione x=0, x=y² e y=√(π/2): a) disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"0\le x\le y^2,\ 0\le y\le\sqrt{\tfrac\pi2}",
    sp.cos(y**2) / y,
    [dict(ext=(y, 0, sp.sqrt(pi / 2)), int=(0, y**2),
          extra_est=[("l'integranda ottenuta è y cos(y²): la derivata di sin(y²) è 2y cos(y²), quindi "
                      "∫y cos(y²)dy=½sin(y²) (sostituzione t=y²).",
                      r"\int y\cos(y^2)\,dy=\frac12\sin(y^2)+c")])],
    [y, x, y**2 - x, sp.sqrt(pi / 2) - y], (-0.2, 1.9, -0.2, 1.5),
    [(x - y**2, "x=y²"), (x, "x=0"), (y - sp.sqrt(pi / 2), "y=√(π/2)")],
    [(0, 0, "O"), (0, sp.sqrt(pi / 2), "(0,√(π/2))"), (pi / 2, sp.sqrt(pi / 2), "(π/2,√(π/2))")],
    [("disegno e caratteristiche delle curve: x=0 è l'asse y; x=y² è una parabola ad asse orizzontale con "
      "vertice in O (nel I quadrante: ramo y=√x); y=√(π/2)≈1,25 è una retta orizzontale. Si incontrano in "
      "O, in (0,√(π/2)) e in (π/2,√(π/2)).",
      r"x=0,\qquad x=y^2,\qquad y=\sqrt{\pi/2}"),
     ("scambio l'ordine d'integrazione (scaletta integrale doppio, punto 3): D è la regione tra l'asse y e la "
      "parabola, sotto la retta y=√(π/2). Con dy dx l'integrale interno sarebbe ∫cos(y²)/y dy, NON elementare "
      "(∫cos t/t dt). Conviene integrare prima in x: per y in [0,√(π/2)] la x va da 0 a y², e il fattore "
      "y² semplifica il denominatore y.",
      r"D=\left\{0\le y\le\sqrt{\tfrac\pi2},\ 0\le x\le y^2\right\}")],
    "Dominio D (aprile 2025)")

_aggiungi(
    "gennaio 2025", 13,
    "Dato l'integrale doppio di f(x,y)=x sul dominio D = {(x,y) ∈ R²: x ≥ 0; y ≥ 0; x²+y²-16 ≤ 0; x²+y²-4y ≥ 0}: "
    "a) disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"x\ge0,\ y\ge0,\ x^2+y^2\le16,\ x^2+y^2\ge4y",
    x,
    [dict(tipo="pol", t=(0, pi / 2), r=(4 * sp.sin(t_), 4))],
    [x, y, 16 - x**2 - y**2, x**2 + y**2 - 4 * y], (-0.4, 4.6, -0.4, 4.6),
    [(x**2 + y**2 - 16, "x²+y²=16"), (x**2 + (y - 2)**2 - 4, "x²+y²=4y"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (4, 0, "(4,0)"), (0, 4, "(0,4)")],
    [("disegno e caratteristiche delle curve: x²+y²=16 è la circonferenza di centro O e raggio 4; "
      "x²+y²−4y=0 equivale a x²+(y−2)²=4, circonferenza di centro (0,2) e raggio 2 (passa per O e (0,4), "
      "e tocca internamente la grande in (0,4)). D è il quarto di cerchio grande privato del mezzo cerchio "
      "piccolo (x≥0): una 'falce' a destra.",
      r"x^2+y^2=16,\qquad x^2+y^2-4y=0\iff x^2+(y-2)^2=4"),
     ("scelgo le coordinate polari (scaletta integrale doppio, punto 3): x²+y²≤16 ⇒ r≤4; x²+y²≥4y ⇒ "
      "r≥4sinθ; x≥0,y≥0 ⇒ θ in [0,π/2]. Poiché 4sinθ≤4, l'intervallo di r è sempre non vuoto.",
      r"0\le\theta\le\tfrac\pi2,\qquad 4\sin\theta\le r\le4")],
    "Dominio D (gennaio 2025)")

_aggiungi(
    "gennaio 2025", 16,
    "Dato l'integrale doppio di f(x,y)=3xy² sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1; y ≥ x³; y ≤ ∛x}: "
    "a) disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"0\le x\le1,\ y\ge x^3,\ y\le\sqrt[3]{x}",
    3 * x * y**2,
    [dict(ext=(x, 0, 1), int=(x**3, x**R(1, 3)))],
    [x, 1 - x, y - x**3, x**R(1, 3) - y], (-0.1, 1.25, -0.1, 1.25),
    [(y - x**3, "y=x³"), (y - x**R(1, 3), "y=∛x"), (x - 1, "x=1")],
    [(0, 0, "O"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x³ è la parabola cubica (crescente, convessa per x>0) e "
      "y=∛x è la sua funzione inversa (simmetrica rispetto alla bisettrice, tangente verticale in O). Si "
      "incontrano per x³=x^{1/3} ⇒ x=0 oppure x=1.",
      r"y=x^3,\qquad y=\sqrt[3]{x}\iff x=y^3,\qquad x^3=x^{1/3}\iff x=0\ \text{o}\ 1"),
     ("per 0<x<1 si ha x³<∛x (es. x=1/8: 1/512<1/2): y va dalla cubica (sotto) alla radice cubica (sopra). "
      "Dominio normale rispetto all'asse x.",
      r"D=\{0\le x\le1,\ x^3\le y\le\sqrt[3]x\}")],
    "Dominio D (gennaio 2025)")


# ===========================================================================
# 2024
# ===========================================================================
_aggiungi(
    "dicembre 2024", 2,
    "Dato l'integrale doppio di f(x,y)=x/(1+y) sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1/2; x² ≤ y ≤ x}: "
    "a) disegnare ed evidenziare il dominio; b) calcolarne il valore. (Esercizio ripetuto anche a gennaio 2024.)",
    r"0\le x\le\tfrac12,\ x^2\le y\le x",
    x / (1 + y),
    [dict(ext=(x, 0, R(1, 2)), int=(x**2, x),
          extra_est=[("per l'integrale in x uso l'integrazione per parti su x·ln(1+x) e la sostituzione "
                      "t=1+x² su x·ln(1+x²): ∫x ln(1+x²)dx=½[(1+x²)ln(1+x²)−(1+x²)]; "
                      "∫x ln(1+x)dx=(x²−1)/2·ln(1+x)−x²/4+x/2.", None)])],
    [x, R(1, 2) - x, y - x**2, x - y], (-0.1, 0.7, -0.1, 0.7),
    [(y - x**2, "y=x²"), (y - x, "y=x"), (x - R(1, 2), "x=1/2")],
    [(0, 0, "O"), (R(1, 2), R(1, 4), "(1/2,1/4)"), (R(1, 2), R(1, 2), "(1/2,1/2)")],
    [("disegno e caratteristiche delle curve: y=x² è la parabola, y=x la bisettrice (si incontrano in O e "
      "(1,1)); x=1/2 è una retta verticale. Per 0<x<1 la parabola sta sotto la bisettrice.",
      r"y=x^2,\qquad y=x,\qquad x=\tfrac12"),
     ("D è normale rispetto all'asse x; integro prima in y: l'integranda è x/(1+y), primitiva x·ln(1+y).",
      r"D=\{0\le x\le\tfrac12,\ x^2\le y\le x\}")],
    "Dominio D (dicembre 2024)",
    pdf_R=-R(3, 8) * sp.log(R(3, 2)) - R(5, 8) * sp.log(R(5, 4)) + R(5, 16))

_aggiungi(
    "dicembre 2024", 3,
    "Dato l'integrale doppio di f(x,y)=x³y−e^(x+y) sul dominio D = triangolo di vertici O(0,0), A(0,π), "
    "B(2π,0): a) disegnare ed evidenziare il dominio; b) calcolarne il valore. (Ripetuto anche a gennaio 2024.)",
    r"\text{triangolo di vertici } O(0,0),\,A(0,\pi),\,B(2\pi,0)",
    x**3 * y - sp.exp(x + y),
    [dict(ext=(x, 0, 2 * pi), int=(0, pi - x / 2))],
    [x, y, pi - x / 2 - y], (-0.6, 7.0, -0.6, 3.8),
    [(y - pi + x / 2, "AB: y=π-x/2"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (0, pi, "A(0,π)"), (2 * pi, 0, "B(2π,0)")],
    [("disegno e caratteristiche delle curve: lati OA (asse y), OB (asse x) e AB: retta per (0,π) e (2π,0), "
      "pendenza −1/2, y=π−x/2.", r"x=0,\qquad y=0,\qquad y=\pi-\frac x2"),
     ("D è normale rispetto all'asse x: per x in [0,2π], y va da 0 a π−x/2. L'integrale è somma di due: "
      "uno con x³y (polinomio) e uno con −e^{x+y} (esponenziale).",
      r"D=\{0\le x\le2\pi,\ 0\le y\le\pi-\tfrac x2\}")],
    "Dominio D: triangolo (dicembre 2024)",
    pdf_R=2 * pi**6 / 15 - sp.exp(2 * pi) + 2 * pi * sp.exp(pi) + 1,
    nota_R="il risultato stampato sembra contenere un refuso (termine 2πe^π)")

_aggiungi(
    "luglio 2024", 2,
    "Dato l'integrale doppio di f(x,y)=xy sul dominio D = {(x,y) ∈ R²: x²+y² ≤ 1; x²+y² ≤ 2x; y ≤ 0}: "
    "a) disegnare il dominio descrivendo le caratteristiche delle varie funzioni; b) determinarne il valore.",
    r"x^2+y^2\le1,\ x^2+y^2\le2x,\ y\le0",
    x * y,
    [dict(tipo="pol", t=(-pi / 3, 0), r=(0, 1), etichetta="θ in [−π/3,0]: bordo x²+y²=1"),
     dict(tipo="pol", t=(-pi / 2, -pi / 3), r=(0, 2 * sp.cos(t_)), etichetta="θ in [−π/2,−π/3]: bordo x²+y²=2x")],
    [-y, 1 - x**2 - y**2, 2 * x - x**2 - y**2], (-1.2, 2.2, -1.3, 0.4),
    [(x**2 + y**2 - 1, "x²+y²=1"), ((x - 1)**2 + y**2 - 1, "x²+y²=2x"), (y, "y=0")],
    [(0, 0, "O"), (1, 0, "(1,0)"), (R(1, 2), -S3 / 2, "(1/2,-√3/2)")],
    [("disegno e caratteristiche delle curve: x²+y²=1 è la circonferenza unitaria; x²+y²=2x è la circonferenza "
      "di centro (1,0) e raggio 1; y≤0 è il semipiano inferiore. D è la metà inferiore della lente.",
      r"x^2+y^2=1,\qquad(x-1)^2+y^2=1"),
     ("le circonferenze si incontrano in x=1/2, y=±√3/2: nel semipiano y≤0 è (1/2,−√3/2), θ=−π/3. In polari "
      "r≤min{1,2cosθ}, con θ in [−π/2,0]: per θ in [−π/3,0] vale r≤1, per θ in [−π/2,−π/3] vale r≤2cosθ "
      "(scaletta integrale doppio, punto 3). ATTENZIONE: nel semipiano y≤0 e x≥0 l'integranda xy è NEGATIVA, "
      "quindi il risultato è negativo.",
      r"\theta\in[-\tfrac\pi2,0],\qquad r\le\min\{1,2\cos\theta\}")],
    "Dominio D (luglio 2024)", pdf_R=R(5, 48),
    nota_R="il PDF stampa +5/48 ma xy<0 su D (x>0,y<0): il valore corretto è −5/48")

_aggiungi(
    "luglio 2024", 3,
    "Dato l'integrale doppio di f(x,y)=(3x−y)²(−x/4+y/4) sul dominio D = quadrilatero compreso tra le rette "
    "y=3x, y=x, y=3x−1, y=x+4: a) disegnare il dominio; b) determinarne il valore.",
    r"\text{parallelogramma tra } y=3x,\ y=3x-1,\ y=x,\ y=x+4",
    (3 * x - y)**2 * (-x / 4 + y / 4),
    [dict(tipo="cv", xy=((u_ + w_) / 2, (u_ + 3 * w_) / 2), ext=(u_, 0, 1), int=(w_, 0, 4),
          testo_sost="pongo u=3x−y e w=y−x, da cui x=(u+w)/2 e y=(u+3w)/2",
          lat_sost=r"u=3x-y,\ w=y-x\ \Rightarrow\ x=\frac{u+w}{2},\ y=\frac{u+3w}{2}",
          testo_dom="il rettangolo 0≤u≤1, 0≤w≤4")],
    [3 * x - y, 1 - 3 * x + y, y - x, 4 - y + x], (-0.5, 3.2, -0.5, 7.2),
    [(y - 3 * x, "y=3x"), (y - 3 * x + 1, "y=3x-1"), (y - x, "y=x"), (y - x - 4, "y=x+4")],
    [(0, 0, "(0,0)"), (R(1, 2), R(1, 2), "(1/2,1/2)"), (2, 6, "(2,6)"), (R(5, 2), R(13, 2), "(5/2,13/2)")],
    [("disegno e caratteristiche delle curve: sono 4 rette, a coppie parallele (pendenze 3 e 1): D è un "
      "parallelogramma. Vertici dalle intersezioni: (0,0), (1/2,1/2), (2,6), (5/2,13/2).",
      r"y=3x\parallel y=3x-1,\qquad y=x\parallel y=x+4"),
     ("nell'integrando compaiono proprio 3x−y e y−x (−x/4+y/4=(y−x)/4): le combinazioni che valgono "
      "costante sui lati. Conviene il cambio di variabili lineare u=3x−y (tra 0 e 1) e w=y−x (tra 0 e 4).",
      r"0\le3x-y\le1,\qquad 0\le y-x\le4")],
    "Dominio D, parallelogramma (luglio 2024)", pdf_R=R(1, 3),
    f_latex=r"(3x-y)^2\left(-\frac x4+\frac y4\right)")

_aggiungi(
    "maggio 2024", 1,
    "Calcolare l'integrale doppio di f(x,y)=1 (area) sul dominio D = {(x,y) ∈ R²: 3x ≤ y ≤ x/3; x ≤ 0; "
    "y ≥ −x−3}: a) disegnare il dominio descrivendo le caratteristiche delle varie funzioni; b) risolvere l'integrale.",
    r"3x\le y\le\tfrac x3,\ x\le0,\ y\ge-x-3",
    sp.Integer(1),
    [dict(ext=(x, R(-9, 4), R(-3, 4)), int=(-x - 3, x / 3), etichetta="x in [−9/4,−3/4]"),
     dict(ext=(x, R(-3, 4), 0), int=(3 * x, x / 3), etichetta="x in [−3/4,0]")],
    [-x, y - 3 * x, x / 3 - y, y + x + 3], (-3.0, 0.4, -3.0, 0.4),
    [(y - 3 * x, "y=3x"), (y - x / 3, "y=x/3"), (y + x + 3, "y=-x-3")],
    [(0, 0, "O"), (R(-3, 4), R(-9, 4), "(-3/4,-9/4)"), (R(-9, 4), R(-3, 4), "(-9/4,-3/4)")],
    [("disegno e caratteristiche delle curve: y=3x e y=x/3 sono rette per O (pendenza 3 e 1/3); y=−x−3 è una "
      "retta decrescente. Per x≤0 è 3x≤x/3, quindi D sta nel cono tra le due rette, sopra y=−x−3.",
      r"y=3x,\qquad y=\tfrac x3,\qquad y=-x-3"),
     ("vertici: y=3x e y=−x−3 ⇒ x=−3/4, y=−9/4; y=x/3 e y=−x−3 ⇒ x=−9/4, y=−3/4. D è il triangolo di vertici "
      "O, (−3/4,−9/4), (−9/4,−3/4) e va diviso in due pezzi in x=−3/4, dove cambia il bordo inferiore.",
      r"\tfrac{4x}{3}=-3\Rightarrow x=-\tfrac94,\qquad 4x=-3\Rightarrow x=-\tfrac34")],
    "Dominio D: triangolo (maggio 2024)", pdf_R=R(9, 4), f_latex="1")

_aggiungi(
    "aprile 2024", 2,
    "Dato l'integrale doppio di f(x,y)=x³+y sul dominio D = {(x,y) ∈ R²: x²+y² ≤ 2; x ≥ 0; y ≤ x²} "
    "(nel PDF compare il refuso 'yx²+y²≤2'): a) disegnare ed evidenziare il dominio; b) calcolarne il valore.",
    r"x^2+y^2\le2,\ x\ge0,\ y\le x^2",
    x**3 + y,
    [dict(ext=(x, 0, 1), int=(-sp.sqrt(2 - x**2), x**2), etichetta="x in [0,1]: tetto la parabola"),
     dict(ext=(x, 1, S2), int=(-sp.sqrt(2 - x**2), sp.sqrt(2 - x**2)), etichetta="x in [1,√2]: tetto la circonferenza")],
    [x, x**2 - y, 2 - x**2 - y**2], (-0.3, 1.8, -1.8, 1.8),
    [(x**2 + y**2 - 2, "x²+y²=2"), (y - x**2, "y=x²"), (x, "x=0")],
    [(1, 1, "(1,1)"), (S2, 0, "(√2,0)"), (0, -S2, "(0,-√2)"), (0, 0, "O")],
    [("disegno e caratteristiche delle curve: x²+y²=2 è la circonferenza di raggio √2; y=x² è la parabola; "
      "x≥0 è il semipiano destro. D è la metà destra del cerchio che sta SOTTO la parabola.",
      r"x^2+y^2=2,\qquad y=x^2,\qquad x\ge0"),
     ("intersezione parabola-circonferenza: x²+x⁴=2 ⇒ x²=1 (x²=−2 impossibile) ⇒ (1,1). Per x in [0,1] la "
      "parabola è il tetto e il fondo è la semicirconferenza inferiore y=−√(2−x²); per x in [1,√2] la parabola "
      "supera la circonferenza, quindi y va da −√(2−x²) a +√(2−x²): due pezzi.",
      r"x^2+x^4=2\iff x^2=1\ \Rightarrow\ (1,1)")],
    "Dominio D (aprile 2024)", pdf_R=8 * S2 / 15 - R(1, 10))


# ===========================================================================
# 2023 - 2024 (ottobre 2024, dicembre 2023, ottobre 2023, luglio 2023)
# ===========================================================================
_aggiungi(
    "ottobre 2024", 5,
    "Dato l'integrale doppio di f(x,y)=sin(y²) sul dominio D = triangolo di vertici O(0,0), A(0,1), B(1,1): "
    "a) disegnare ed evidenziare il dominio; b) determinare il valore dell'integrale.",
    r"\text{triangolo di vertici } O(0,0),\,A(0,1),\,B(1,1)",
    sp.sin(y**2),
    [dict(ext=(y, 0, 1), int=(0, y),
          extra_est=[("l'integranda y sin(y²) ha primitiva −½cos(y²) (sostituzione t=y²).",
                      r"\int y\sin(y^2)\,dy=-\tfrac12\cos(y^2)")])],
    [x, y - x, 1 - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x, "OB: y=x"), (y - 1, "AB: y=1"), (x, "OA: x=0")],
    [(0, 0, "O"), (0, 1, "A(0,1)"), (1, 1, "B(1,1)")],
    [("disegno e caratteristiche delle curve: OA è sull'asse y (x=0), AB sulla retta orizzontale y=1, OB "
      "sulla bisettrice y=x. D = {0≤x≤y, 0≤y≤1}.",
      r"x=0,\qquad y=1,\qquad y=x"),
     ("scambio l'ordine d'integrazione (scaletta integrale doppio, punto 3): sin(y²) non ha primitiva "
      "elementare rispetto a y, quindi NON si può integrare prima in y. Scrivo D come dominio normale rispetto "
      "all'asse y: per y in [0,1] la x va da 0 a y; integrando in x il fattore sin(y²) è costante e compare y.",
      r"D=\{0\le y\le1,\ 0\le x\le y\}\quad(\text{invece di }0\le x\le1,\ x\le y\le1)")],
    "Dominio D: triangolo (ottobre 2024)")

_aggiungi(
    "ottobre 2024", 8,
    "Dato l'integrale doppio di f(x,y)=√y·cos(x⁴) sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1; y ≥ 0; y ≤ x²}: "
    "a) disegnare ed evidenziare il dominio; b) determinare il valore dell'integrale. "
    "(Ripetuto anche a luglio 2023.)",
    r"0\le x\le1,\ y\ge0,\ y\le x^2",
    sp.sqrt(y) * sp.cos(x**4),
    [dict(ext=(x, 0, 1), int=(0, x**2),
          extra_est=[("l'integranda (2/3)x³cos(x⁴) ha primitiva (1/6)sin(x⁴) (sostituzione t=x⁴, dt=4x³dx).",
                      r"\int\tfrac23x^3\cos(x^4)\,dx=\tfrac16\sin(x^4)")])],
    [x, 1 - x, y, x**2 - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x**2, "y=x²"), (y, "y=0"), (x - 1, "x=1")],
    [(0, 0, "O"), (1, 0, "(1,0)"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x² è la parabola (vertice O), y=0 l'asse x, x=1 una retta "
      "verticale. D è la regione sotto la parabola, tra x=0 e x=1.",
      r"y=x^2,\qquad y=0,\qquad x=1"),
     ("l'ordine è dy dx (dominio normale rispetto all'asse x, y da 0 a x²): cos(x⁴) NON ha primitiva "
      "elementare in x, ma qui è costante nell'integrazione in y (che si fa subito: √y→(2/3)y^{3/2}) "
      "e dopo resta x³cos(x⁴), integrabile per sostituzione.",
      r"D=\{0\le x\le1,\ 0\le y\le x^2\}")],
    "Dominio D (ottobre 2024)")

_aggiungi(
    "dicembre 2023", 1,
    "Risolvere l'integrale doppio di f(x,y)=xy sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 5; y² ≤ 5−x; y² ≤ 4x; y ≥ 0}. "
    "È obbligatorio il disegno del dominio. (Variante: dicembre 2021, esercizio 10.)",
    r"0\le x\le5,\ y^2\le5-x,\ y^2\le4x,\ y\ge0",
    x * y,
    [dict(ext=(y, 0, 2), int=(y**2 / 4, 5 - y**2))],
    [x, 5 - x, y, 5 - x - y**2, 4 * x - y**2], (-0.3, 5.6, -0.3, 2.8),
    [(x + y**2 - 5, "x=5-y²"), (y**2 - 4 * x, "y²=4x"), (x, "x=0"), (x - 5, "x=5")],
    [(0, 0, "O"), (1, 2, "(1,2)"), (5, 0, "(5,0)")],
    [("disegno e caratteristiche delle curve: y²=4x è una parabola ad asse orizzontale con vertice in O; "
      "y²=5−x, cioè x=5−y², è una parabola ad asse orizzontale rivolta verso sinistra con vertice in (5,0). "
      "y≥0 seleziona i rami superiori.",
      r"y^2=4x\iff x=\tfrac{y^2}{4},\qquad y^2=5-x\iff x=5-y^2"),
     ("intersezione: y²/4=5−y² ⇒ 5y²/4=5 ⇒ y²=4 ⇒ y=2 (y≥0), x=1: il punto (1,2). Da y²≤4x si ha x≥y²/4 "
      "e da y²≤5−x si ha x≤5−y². Descrivo D come dominio normale rispetto all'asse y: un solo pezzo "
      "(rispetto a x servirebbero due pezzi, x in [0,1] e [1,5]).",
      r"\tfrac{y^2}{4}=5-y^2\iff y=2,\ x=1,\qquad D=\{0\le y\le2,\ \tfrac{y^2}{4}\le x\le5-y^2\}")],
    "Dominio D (dicembre 2023)")

_aggiungi(
    "dicembre 2023", 2,
    "Risolvere l'integrale doppio di f(x,y)=x·e^y sul dominio D = quadrilatero di vertici O(0,0), A(1,0), "
    "B(2,−1), C(1,1). È obbligatorio il disegno del dominio.",
    r"\text{quadrilatero di vertici } O(0,0),\,A(1,0),\,B(2,-1),\,C(1,1)",
    x * sp.exp(y),
    [dict(ext=(x, 0, 1), int=(0, x), etichetta="x in [0,1]"),
     dict(ext=(x, 1, 2), int=(1 - x, 3 - 2 * x), etichetta="x in [1,2]")],
    [x, 2 - x, sp.Piecewise((y, x <= 1), (y - (1 - x), True)),
     sp.Piecewise((x - y, x <= 1), ((3 - 2 * x) - y, True))], (-0.3, 2.4, -1.4, 1.4),
    [(y, "OA: y=0"), (y - x, "OC: y=x"), (y - 1 + x, "AB: y=1-x"), (y - 3 + 2 * x, "BC: y=3-2x")],
    [(0, 0, "O"), (1, 0, "A(1,0)"), (2, -1, "B(2,-1)"), (1, 1, "C(1,1)")],
    [("disegno e caratteristiche delle curve: OA sull'asse x (y=0); AB per (1,0),(2,−1): pendenza −1, "
      "y=1−x; BC per (2,−1),(1,1): pendenza −2, y=3−2x; CO per (1,1),(0,0): y=x.",
      r"OA:\ y=0,\quad AB:\ y=1-x,\quad BC:\ y=3-2x,\quad CO:\ y=x"),
     ("il quadrilatero NON è convesso: A è un vertice 'rientrante'. Scompongo con la retta verticale x=1 "
      "(passante per A e C): a sinistra (x in [0,1]) la y va da OA (y=0) a CO (y=x); a destra (x in [1,2]) "
      "da AB (y=1−x) a BC (y=3−2x): due pezzi.",
      r"D=\{0\le x\le1,\ 0\le y\le x\}\cup\{1\le x\le2,\ 1-x\le y\le3-2x\}")],
    "Dominio D: quadrilatero non convesso (dicembre 2023)")

_aggiungi(
    "dicembre 2023", 5,
    "Risolvere l'integrale doppio di f(x,y)=sin(y³) sul dominio D = {(x,y) ∈ R²: 0 ≤ x ≤ 1; y ≤ 1; y ≥ √x}. "
    "È obbligatorio il disegno del dominio.",
    r"0\le x\le1,\ y\le1,\ y\ge\sqrt x",
    sp.sin(y**3),
    [dict(ext=(y, 0, 1), int=(0, y**2),
          extra_est=[("l'integranda y² sin(y³) ha primitiva −⅓cos(y³) (sostituzione t=y³).",
                      r"\int y^2\sin(y^3)\,dy=-\tfrac13\cos(y^3)")])],
    [x, 1 - x, 1 - y, y - sp.sqrt(x)], (-0.2, 1.3, -0.2, 1.3),
    [(y - sp.sqrt(x), "y=√x"), (y - 1, "y=1"), (x, "x=0"), (x - 1, "x=1")],
    [(0, 0, "O"), (0, 1, "(0,1)"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=√x è il ramo superiore della parabola x=y² (vertice O); "
      "y=1 e x=0, x=1 sono rette. D è la regione sopra la radice e sotto y=1, tra x=0 e x=1.",
      r"y=\sqrt x\iff x=y^2\ (y\ge0),\qquad y=1"),
     ("scambio l'ordine d'integrazione (scaletta integrale doppio, punto 3): sin(y³) non ha primitiva "
      "elementare in y. Dal disegno: per y in [0,1] la x va da 0 alla parabola x=y² (da y≥√x si ha x≤y²).",
      r"y\ge\sqrt x\iff x\le y^2\ \Rightarrow\ D=\{0\le y\le1,\ 0\le x\le y^2\}")],
    "Dominio D (dicembre 2023)")

_aggiungi(
    "ottobre 2023", 1,
    "Risolvere l'integrale doppio di f(x,y)=6x²y+ln x sul dominio D = {(x,y) ∈ R²: 1 ≤ x ≤ e; y ≥ 0; y ≤ x}. "
    "È obbligatorio il disegno del dominio.",
    r"1\le x\le e,\ y\ge0,\ y\le x",
    6 * x**2 * y + sp.log(x),
    [dict(ext=(x, 1, E), int=(0, x))],
    [x - 1, E - x, y, x - y], (-0.3, 3.2, -0.3, 3.2),
    [(y - x, "y=x"), (y, "y=0"), (x - 1, "x=1"), (x - E, "x=e")],
    [(1, 0, "(1,0)"), (E, 0, "(e,0)"), (1, 1, "(1,1)"), (E, E, "(e,e)")],
    [("disegno e caratteristiche delle curve: x=1, x=e rette verticali; y=0 asse x; y=x bisettrice. D è il "
      "trapezio di vertici (1,0), (e,0), (e,e), (1,1).", r"x=1,\quad x=e,\quad y=0,\quad y=x"),
     ("D è normale rispetto all'asse x: x in [1,e], y da 0 a x.", r"D=\{1\le x\le e,\ 0\le y\le x\}")],
    "Dominio D, trapezio (ottobre 2023)")

_aggiungi(
    "ottobre 2023", 3,
    "Risolvere l'integrale doppio di f(x,y)=x·arctan(y/x) dove D è la parte di piano del primo quadrante compresa "
    "tra le curve y=x e x=√y. È obbligatorio il disegno del dominio.",
    r"x^2\le y\le x\ (0\le x\le1)",
    x * sp.atan(y / x),
    [dict(ext=(x, 0, 1), int=(x**2, x))],
    [x, 1 - x, y - x**2, x - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x, "y=x"), (y - x**2, "x=√y (y=x²)")],
    [(0, 0, "O"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=x è la bisettrice; x=√y equivale, per x≥0, a y=x², la "
      "parabola. Si incontrano in O e in (1,1); tra loro la parabola sta sotto la bisettrice.",
      r"y=x,\qquad x=\sqrt y\iff y=x^2\ (x\ge0)"),
     ("D = {0≤x≤1, x²≤y≤x}: dominio normale rispetto all'asse x. L'integranda in y: ∫arctan(y/x)dy si fa "
      "per parti: y·arctan(y/x) − (x/2)ln(x²+y²).",
      r"D=\{0\le x\le1,\ x^2\le y\le x\}")],
    "Dominio D (ottobre 2023)", salta_numerico=False)


# ===========================================================================
# LUGLIO 2023, DICEMBRE 2021, SETTEMBRE 2021
# ===========================================================================
_aggiungi(
    "luglio 2023", 5,
    "Risolvere l'integrale doppio di f(x,y)=(2/3)·x/(x²+1) dove D è il triangolo di vertici A(2,−5), B(2,1), "
    "C(−2,−1).",
    r"\text{triangolo di vertici } A(2,-5),\,B(2,1),\,C(-2,-1)",
    R(2, 3) * x / (x**2 + 1),
    [dict(ext=(x, -2, 2), int=(-x - 3, x / 2),
          extra_est=[("l'altezza (x/2)−(−x−3)=3x/2+3 moltiplicata per (2/3)x/(x²+1) dà x(x+2)/(x²+1)="
                      "1+(2x−1)/(x²+1): scompongo in 1 + 2x/(x²+1) − 1/(x²+1), con primitiva "
                      "x + ln(x²+1) − arctan x.",
                      r"\frac{x^2+2x}{x^2+1}=1+\frac{2x}{x^2+1}-\frac{1}{x^2+1}")])],
    [2 - x, y + x + 3, x / 2 - y], (-2.8, 2.8, -5.8, 1.8),
    [(y + x + 3, "CA: y=-x-3"), (y - x / 2, "CB: y=x/2"), (x - 2, "AB: x=2")],
    [(2, -5, "A(2,-5)"), (2, 1, "B(2,1)"), (-2, -1, "C(-2,-1)")],
    [("disegno e caratteristiche delle curve: AB è sulla retta verticale x=2; CA passa per (−2,−1),(2,−5): "
      "pendenza −1, y=−x−3; CB passa per (−2,−1),(2,1): pendenza 1/2, y=x/2.",
      r"AB:\ x=2,\qquad CA:\ y=-x-3,\qquad CB:\ y=\tfrac x2"),
     ("D è normale rispetto all'asse x (un solo pezzo): x in [−2,2], y da CA (sotto) a CB (sopra).",
      r"D=\{-2\le x\le2,\ -x-3\le y\le\tfrac x2\}")],
    "Dominio D: triangolo (luglio 2023)", f_latex=r"\frac23\cdot\frac{x}{x^2+1}")

_aggiungi(
    "luglio 2023", 8,
    "Risolvere l'integrale doppio di f(x,y)=(x²+y²)/(x+y) dove D è il triangolo di vertici O(0,0), A(1,0), B(0,1).",
    r"\text{triangolo di vertici } O(0,0),\,A(1,0),\,B(0,1)",
    (x**2 + y**2) / (x + y),
    [dict(tipo="cv", xy=((u_ + w_) / 2, (u_ - w_) / 2), ext=(u_, 0, 1), int=(w_, -u_, u_),
          testo_sost="pongo u=x+y e w=x−y, da cui x=(u+w)/2, y=(u−w)/2 (e x²+y²=(u²+w²)/2)",
          lat_sost=r"u=x+y,\ w=x-y\ \Rightarrow\ x=\frac{u+w}{2},\ y=\frac{u-w}{2},\ \ x^2+y^2=\frac{u^2+w^2}{2}",
          testo_dom="0≤u≤1, −u≤w≤u")],
    [x, y, 1 - x - y], (-0.2, 1.3, -0.2, 1.3),
    [(x + y - 1, "AB: x+y=1"), (x, "OB: x=0"), (y, "OA: y=0")],
    [(0, 0, "O"), (1, 0, "A(1,0)"), (0, 1, "B(0,1)")],
    [("disegno e caratteristiche delle curve: OA sull'asse x, OB sull'asse y, AB sulla retta x+y=1 "
      "(pendenza −1). D = {x≥0, y≥0, x+y≤1}.", r"x\ge0,\quad y\ge0,\quad x+y\le1"),
     ("in coordinate cartesiane l'integrale interno (x²+y²)/(x+y) è scomodo; l'integranda contiene x+y "
      "(che vale u costante sulle rette parallele ad AB) e x²+y². Un cambio di variabili lineare "
      "u=x+y, w=x−y semplifica: x≥0 ⇔ w≥−u, y≥0 ⇔ w≤u, x+y≤1 ⇔ u≤1.",
      r"x\ge0\iff w\ge-u,\quad y\ge0\iff w\le u,\quad x+y\le1\iff u\le1")],
    "Dominio D: triangolo (luglio 2023)")

_aggiungi(
    "luglio 2023", 14,
    "Risolvere l'integrale doppio di f(x,y)=y·e^x sul dominio D = {(x,y) ∈ R²: x−y²+4 ≥ 0; x+y²−4 ≤ 0}.",
    r"x\ge y^2-4,\ x\le4-y^2",
    y * sp.exp(x),
    [dict(ext=(y, -2, 2), int=(y**2 - 4, 4 - y**2),
          extra_est=[("l'integranda y(e^{4−y²}−e^{y²−4}) è una funzione DISPARI di y e l'intervallo [−2,2] è "
                      "simmetrico: l'integrale vale 0 (si vede anche da D simmetrico rispetto all'asse x e "
                      "f dispari in y).", None)])],
    [x - y**2 + 4, 4 - y**2 - x], (-4.6, 4.6, -2.6, 2.6),
    [(x - y**2 + 4, "x=y²-4"), (x + y**2 - 4, "x=4-y²")],
    [(-4, 0, "(-4,0)"), (4, 0, "(4,0)"), (0, 2, "(0,2)"), (0, -2, "(0,-2)")],
    [("disegno e caratteristiche delle curve: x=y²−4 è una parabola ad asse orizzontale che si apre verso "
      "destra con vertice in (−4,0); x=4−y² si apre verso sinistra con vertice in (4,0). D è la regione "
      "limitata a forma di 'lente' tra le due.",
      r"x\ge y^2-4,\qquad x\le4-y^2"),
     ("intersezioni: y²−4=4−y² ⇒ y²=4 ⇒ y=±2, x=0. Per ogni y in [−2,2] la x va da y²−4 a 4−y²: dominio "
      "normale rispetto all'asse y.",
      r"D=\{-2\le y\le2,\ y^2-4\le x\le4-y^2\}")],
    "Dominio D (luglio 2023)")

_aggiungi(
    "dicembre 2021", 2,
    "Risolvere l'integrale doppio di f(x,y)=x²/(1+y)² dove D è l'insieme limitato dalle curve y=x² e y=2x+3.",
    r"x^2\le y\le2x+3",
    x**2 / (1 + y)**2,
    [dict(ext=(x, -1, 3), int=(x**2, 2 * x + 3),
          extra_est=[("per x²/(2x+4) divido: x²/(2x+4)=x/2−1+2/(x+2) (verifica: (x/2−1)(2x+4)+4=x²).",
                      r"\frac{x^2}{2x+4}=\frac x2-1+\frac{2}{x+2},\qquad\frac{x^2}{1+x^2}=1-\frac{1}{1+x^2}")])],
    [y - x**2, 2 * x + 3 - y], (-1.8, 3.8, -0.5, 10.5),
    [(y - x**2, "y=x²"), (y - 2 * x - 3, "y=2x+3")],
    [(-1, 1, "(-1,1)"), (3, 9, "(3,9)")],
    [("disegno e caratteristiche delle curve: y=x² è la parabola; y=2x+3 è una retta di pendenza 2 che "
      "passa per (0,3) e (−3/2,0).", r"y=x^2,\qquad y=2x+3"),
     ("intersezioni: x²=2x+3 ⇒ x²−2x−3=0 ⇒ (x−3)(x+1)=0 ⇒ x=−1, x=3: i punti (−1,1) e (3,9). Tra le "
      "intersezioni la retta sta sopra la parabola: D è un 'segmento parabolico'.",
      r"x^2-2x-3=0\iff x=-1\ \text{o}\ x=3,\qquad D=\{-1\le x\le3,\ x^2\le y\le2x+3\}")],
    "Dominio D (dicembre 2021)")

_aggiungi(
    "dicembre 2021", 8,
    "Risolvere l'integrale doppio di f(x,y)=e^(y²) dove D è il triangolo di vertici (0,0), (−1,2), (1,2).",
    r"\text{triangolo di vertici } (0,0),\,(-1,2),\,(1,2)",
    sp.exp(y**2),
    [dict(ext=(y, 0, 2), int=(-y / 2, y / 2),
          extra_est=[("l'integranda y·e^{y²} ha primitiva ½e^{y²} (sostituzione t=y²).",
                      r"\int y\,e^{y^2}dy=\tfrac12e^{y^2}")])],
    [y, 2 - y, y / 2 - x, y / 2 + x], (-1.6, 1.6, -0.3, 2.4),
    [(y - 2, "y=2"), (y - 2 * x, "y=2x"), (y + 2 * x, "y=-2x")],
    [(0, 0, "O"), (-1, 2, "(-1,2)"), (1, 2, "(1,2)")],
    [("disegno e caratteristiche delle curve: il lato superiore è y=2; i lati obliqui passano per O e (±1,2): "
      "rette y=2x e y=−2x, cioè x=±y/2.", r"y=2,\qquad y=2x,\qquad y=-2x"),
     ("scambio l'ordine d'integrazione (scaletta integrale doppio, punto 3): e^{y²} non ha primitiva "
      "elementare in y, quindi integro prima in x: per y in [0,2] la x va da −y/2 a y/2 (lunghezza y).",
      r"D=\{0\le y\le2,\ -\tfrac y2\le x\le\tfrac y2\}")],
    "Dominio D: triangolo (dicembre 2021)")

_aggiungi(
    "settembre 2021", 5,
    "Risolvere l'integrale doppio di f(x,y)=xy dove D è il quadrato di vertici (0,1), (1,2), (2,1), (1,0).",
    r"\text{quadrato di vertici } (0,1),\,(1,2),\,(2,1),\,(1,0)",
    x * y,
    [dict(tipo="cv", xy=((u_ - w_) / 2, (u_ + w_) / 2), ext=(u_, 1, 3), int=(w_, -1, 1),
          testo_sost="pongo u=x+y e w=y−x, da cui x=(u−w)/2, y=(u+w)/2 (xy=(u²−w²)/4)",
          lat_sost=r"u=x+y,\ w=y-x\ \Rightarrow\ x=\frac{u-w}{2},\ y=\frac{u+w}{2}",
          testo_dom="il rettangolo 1≤u≤3, −1≤w≤1")],
    [y - x + 1, 1 - y + x, x + y - 1, 3 - x - y], (-0.4, 2.5, -0.4, 2.5),
    [(y - x - 1, "y=x+1"), (y - x + 1, "y=x-1"), (y + x - 1, "y=1-x"), (y + x - 3, "y=3-x")],
    [(0, 1, "(0,1)"), (1, 2, "(1,2)"), (2, 1, "(2,1)"), (1, 0, "(1,0)")],
    [("disegno e caratteristiche delle curve: i lati hanno pendenza ±1: (0,1)-(1,2): y=x+1; (1,2)-(2,1): "
      "y=3−x; (2,1)-(1,0): y=x−1; (1,0)-(0,1): y=1−x. Il quadrato è ruotato di 45° (una diagonale è "
      "orizzontale, l'altra verticale).", r"y=x+1,\quad y=3-x,\quad y=x-1,\quad y=1-x"),
     ("le coppie di lati parallele danno −1≤y−x≤1 e 1≤x+y≤3: il cambio lineare u=x+y, w=y−x trasforma "
      "il quadrato in un rettangolo (alternativa: tre pezzi cartesiani). Controllo: per simmetria rispetto "
      "al centro (1,1) il risultato è area·(1·1)=2, perché i termini lineari si annullano.",
      r"1\le x+y\le3,\qquad -1\le y-x\le1")],
    "Dominio D: quadrato (settembre 2021)")

_aggiungi(
    "settembre 2021", 6,
    "Risolvere l'integrale doppio di f(x,y)=xy dove D è il triangolo di vertici (0,0), (2,0), (1,1).",
    r"\text{triangolo di vertici } (0,0),\,(2,0),\,(1,1)",
    x * y,
    [dict(ext=(y, 0, 1), int=(y, 2 - y))],
    [y, x - y, 2 - x - y], (-0.3, 2.3, -0.3, 1.3),
    [(y - x, "y=x"), (y + x - 2, "y=2-x"), (y, "y=0")],
    [(0, 0, "O"), (2, 0, "(2,0)"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: la base è sull'asse x; i lati obliqui sono y=x (da O a (1,1)) "
      "e y=2−x (da (1,1) a (2,0)). Triangolo isoscele simmetrico rispetto a x=1.",
      r"y=0,\qquad y=x,\qquad y=2-x"),
     ("scrivo D come dominio normale rispetto all'asse y (un solo pezzo): per y in [0,1] la x va da y (lato "
      "sinistro) a 2−y (lato destro). Con dx dy servirebbero due pezzi.",
      r"D=\{0\le y\le1,\ y\le x\le2-y\}")],
    "Dominio D: triangolo (settembre 2021)")

_aggiungi(
    "settembre 2021", 7,
    "Risolvere l'integrale doppio di f(x,y)=y·√(x²+y²) sul dominio D = {(x,y) ∈ R²: x ≤ 1; x ≥ 0; 0 ≤ y ≤ x}.",
    r"0\le x\le1,\ 0\le y\le x",
    y * sp.sqrt(x**2 + y**2),
    [dict(tipo="pol", t=(0, pi / 4), r=(0, 1 / sp.cos(t_)))],
    [x, 1 - x, y, x - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - x, "y=x"), (y, "y=0"), (x - 1, "x=1")],
    [(0, 0, "O"), (1, 0, "(1,0)"), (1, 1, "(1,1)")],
    [("disegno e caratteristiche delle curve: y=0 asse x, y=x bisettrice, x=1 retta verticale: D è il "
      "triangolo di vertici O, (1,0), (1,1).", r"y=0,\qquad y=x,\qquad x=1"),
     ("scelgo le coordinate polari (scaletta integrale doppio, punto 3), perché compare √(x²+y²)=r: l'angolo "
      "va da 0 (asse x) a π/4 (bisettrice); la retta x=1 diventa r cosθ=1, cioè r=1/cosθ, e r va da 0 a "
      "1/cosθ.",
      r"0\le\theta\le\tfrac\pi4,\qquad 0\le r\le\frac{1}{\cos\theta}")],
    "Dominio D (settembre 2021)")

_aggiungi(
    "settembre 2021", 8,
    "Risolvere l'integrale doppio di f(x,y)=x·cos y sul dominio D = {(x,y) ∈ R²: y ≥ 0; x ≥ 0; y ≤ 1−x²}.",
    r"x\ge0,\ y\ge0,\ y\le1-x^2",
    x * sp.cos(y),
    [dict(ext=(x, 0, 1), int=(0, 1 - x**2),
          extra_est=[("l'integranda x sin(1−x²) ha primitiva ½cos(1−x²) (sostituzione t=1−x², dt=−2x dx).",
                      r"\int x\sin(1-x^2)\,dx=\tfrac12\cos(1-x^2)")])],
    [x, y, 1 - x**2 - y], (-0.2, 1.3, -0.2, 1.3),
    [(y - 1 + x**2, "y=1-x²"), (x, "x=0"), (y, "y=0")],
    [(0, 0, "O"), (1, 0, "(1,0)"), (0, 1, "(0,1)")],
    [("disegno e caratteristiche delle curve: y=1−x² è una parabola con vertice (0,1), concavità verso "
      "il basso, che taglia l'asse x in (±1,0); x≥0,y≥0 selezionano il I quadrante.",
      r"y=1-x^2,\qquad x\ge0,\ y\ge0"),
     ("D è normale rispetto all'asse x: x in [0,1], y da 0 a 1−x². Integro prima in y (cos y→sin y).",
      r"D=\{0\le x\le1,\ 0\le y\le1-x^2\}")],
    "Dominio D (settembre 2021)")
