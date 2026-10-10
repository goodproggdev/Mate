# -*- coding: utf-8 -*-
"""
Banco 'Esame' -- OTTIMIZZAZIONE (massimi e minimi vincolati e liberi).

Problemi reali estratti dai PDF degli appelli (Uninettuno, Metodi Matematici per
l'Ingegneria) non ancora presenti in esame_bank.py. Ogni risultato e' calcolato con sympy
(e, per i vincolati compatti, ricontrollato numericamente campionando la curva).
Aggiunge voci a ESAME["lagrange"] e ESAME["punti_liberi"].
"""
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

import esame_bank
from esame_bank import (ESAME, _voce, _passo, _tex, _png,
                        _passo_regolarita_latex, _passo_lagrangiana_latex)
import multivariabile as _mv

x, y = esame_bank.x, esame_bank.y
lam = _mv.lam

_COL_VINC = '#c0392b'
_COL_PT = '#1f3b57'


# ---------------------------------------------------------------------------
# utilita' generali
# ---------------------------------------------------------------------------

def _pt(px, py):
    return "(" + _tex(px) + ",\\," + _tex(py) + ")"


def _shift(var, c):
    """'x' con centro c -> '(x-3)', '(x+2)' oppure 'x'."""
    c = sp.nsimplify(c)
    if c == 0:
        return var
    return "(" + var + ("-" + _tex(c) if c > 0 else "+" + _tex(-c)) + ")"


def _ptxt(v):
    """Valore sympy -> testo semplice leggibile (senza LaTeX) per i campi 'testo' dei passi."""
    t = str(sp.nsimplify(v))
    t = t.replace("sqrt(", "√(").replace("**", "^").replace("*", "·")
    return t


def _mat(M):
    """Matrice sympy -> LaTeX con parentesi tonde (pmatrix)."""
    return sp.latex(M, mat_delim='', mat_str='pmatrix')


def _fmt(v):
    """Numero/espressione -> stringa breve per le etichette dei grafici."""
    vv = sp.nsimplify(v)
    if vv.is_Rational:
        return str(vv)
    return "%.4g" % float(sp.N(v))


def _reali(sols):
    """Tiene solo le soluzioni (dict) con x,y reali e le restituisce come coppie ordinate."""
    out = []
    for s in sols:
        if x not in s or y not in s:
            continue
        a, b = sp.nsimplify(sp.simplify(s[x])), sp.nsimplify(sp.simplify(s[y]))
        if a.has(sp.I) or b.has(sp.I):
            continue
        if a.free_symbols or b.free_symbols:
            continue
        out.append((a, b))
    return out


def _ordina(punti):
    uniq = []
    for p in punti:
        if not any(sp.simplify(p[0] - q[0]) == 0 and sp.simplify(p[1] - q[1]) == 0 for q in uniq):
            uniq.append((sp.nsimplify(p[0]), sp.nsimplify(p[1])))
    return sorted(uniq, key=lambda p: (float(sp.N(p[0])), float(sp.N(p[1]))))


def _campioni_curva(g, box, n=1400):
    """Punti (x,y) campionati sulla curva g=0 (via contour di matplotlib) nel riquadro box."""
    xs = np.linspace(box[0], box[1], n)
    ys = np.linspace(box[2], box[3], n)
    X, Y = np.meshgrid(xs, ys)
    G = np.asarray(sp.lambdify((x, y), g, 'numpy')(X, Y), dtype=float) * np.ones_like(X)
    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, G, [0])
    segs = [s for s in cs.allsegs[0]]
    plt.close(fig)
    if not segs:
        return np.zeros((0, 2))
    return np.vstack(segs)


# ---------------------------------------------------------------------------
# descrizione del vincolo (Passo 1): circonferenza, ellisse, retta, parabola
# ---------------------------------------------------------------------------

def _v_circ(g, cx, cy, r, completa=True, extra=None):
    cx, cy, r = sp.nsimplify(cx), sp.nsimplify(cy), sp.nsimplify(r)
    lat = (_tex(g) + "=0\\iff " + _shift("x", cx) + "^2+" + _shift("y", cy) + "^2=" + _tex(r**2))
    if completa:
        t1 = ("Passo 1 — riconosciamo il vincolo g(x,y)=0: completando i quadrati si riconosce "
              "una somma di quadrati uguale a una costante positiva, cioè una circonferenza:")
    else:
        t1 = ("Passo 1 — riconosciamo il vincolo g(x,y)=0: somma di quadrati uguale a una costante "
              "positiva, cioè una circonferenza:")
    passi = [_passo(t1, lat),
             _passo("Caratteristiche della curva: circonferenza di centro C e raggio r. È una curva "
                    "chiusa e limitata, quindi un insieme COMPATTO (chiuso e limitato); si traccia "
                    "con il compasso (figura sotto):",
                    r"C=" + _pt(cx, cy) + r",\quad r=" + _tex(r)
                    + r",\quad x\in[" + _tex(cx - r) + "," + _tex(cx + r) + r"],\ y\in["
                    + _tex(cy - r) + "," + _tex(cy + r) + "]")]
    if extra:
        passi.extend(extra)
    return passi


def _v_ellisse(g, cx, cy, a, b, extra=None):
    cx, cy, a, b = [sp.nsimplify(t) for t in (cx, cy, a, b)]
    lat = (_tex(g) + "=0\\iff \\frac{" + _shift("x", cx) + "^2}{" + _tex(a**2) + "}+\\frac{"
           + _shift("y", cy) + "^2}{" + _tex(b**2) + "}=1")
    passi = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: dividendo per il termine noto si "
                    "porta nella forma canonica dell'ellisse x²/a²+y²/b²=1 (somma di quadrati con "
                    "coefficienti positivi diversi):", lat),
             _passo("Caratteristiche della curva: ellisse di centro C e semiassi a (lungo x) e b "
                    "(lungo y), con i quattro vertici agli estremi degli assi; è chiusa e limitata, "
                    "quindi un insieme COMPATTO:",
                    r"C=" + _pt(cx, cy) + r",\ a=" + _tex(a) + r",\ b=" + _tex(b)
                    + r",\ \text{vertici: }" + _pt(cx + a, cy) + "," + _pt(cx - a, cy) + ","
                    + _pt(cx, cy + b) + "," + _pt(cx, cy - b))]
    if extra:
        passi.extend(extra)
    return passi


def _v_retta(g, m, q, extra=None):
    m, q = sp.nsimplify(m), sp.nsimplify(q)
    inter = ""
    if m != 0:
        inter = r",\ \text{asse }x:\ " + _pt(sp.nsimplify(-q / m), 0)
    passi = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: equazione di primo grado in x e y, "
                    "cioè una RETTA; la riscriviamo in forma esplicita:",
                    _tex(g) + "=0\\iff y=" + _tex(sp.expand(m * x + q))),
             _passo("Caratteristiche della curva: retta di coefficiente angolare m e intercetta q; "
                    "è chiusa ma NON limitata, quindi NON compatta (il teorema di Weierstrass non si "
                    "applica). Interseca gli assi nei punti:",
                    r"m=" + _tex(m) + r",\ q=" + _tex(q) + inter + r",\ \text{asse }y:\ " + _pt(0, q))]
    if extra:
        passi.extend(extra)
    return passi


def _v_parabola_y(g, a, h, k, extra=None):
    """Parabola y = a (x-h)^2 + k (asse verticale)."""
    a, h, k = sp.nsimplify(a), sp.nsimplify(h), sp.nsimplify(k)
    ex = sp.expand(a * (x - h)**2 + k)
    forma = _tex(a) + _shift("x", h) + "^2" + ("+" if k >= 0 else "") + _tex(k)
    forma = forma.replace("1" + _shift("x", h), _shift("x", h)) if a == 1 else forma
    passi = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: y compare al primo grado e x al secondo, "
                    "cioè una PARABOLA con asse verticale; esplicitiamo y e completiamo il quadrato:",
                    _tex(g) + "=0\\iff y=" + _tex(ex) + "=" + forma),
             _passo("Caratteristiche della curva: parabola con concavità rivolta "
                    + ("verso l'alto" if a > 0 else "verso il basso") + ", vertice V e asse la retta "
                    "x=" + _ptxt(h) + ". Non è limitata, quindi NON è compatta (Weierstrass non "
                    "applicabile):",
                    r"V=" + _pt(h, k) + r",\quad \text{asse: }x=" + _tex(h) + r",\quad y\to"
                    + ("+" if a > 0 else "-") + r"\infty\ (x\to\pm\infty)")]
    if extra:
        passi.extend(extra)
    return passi


# ---------------------------------------------------------------------------
# VINCOLATI: costruttore generale
# ---------------------------------------------------------------------------

def _lag(fonte, n, enunciato, testo_latex, f, g, vinc_passi, *, compatto, box,
         punti=None, singolari=None, nota_sistema=None, passi_assoluti=None,
         val_max='auto', val_min='auto', fattori_ignora=(), lambdas=None,
         titolo_curva="vincolo g=0", hint=None, verifica=True,
         passo_extra_regolarita=None, prefisso_passi=None, conclusione_extra=None):
    """Costruisce una voce ESAME['lagrange'] con tutti i passaggi (Passi 1-7)."""
    fx, fy = sp.diff(f, x), sp.diff(f, y)
    gx, gy = sp.diff(g, x), sp.diff(g, y)
    trasc = f.has(sp.exp, sp.log)
    cross = sp.factor(sp.simplify(fx * gy - fy * gx)) if trasc else sp.factor(sp.expand(fx * gy - fy * gx))

    passi = list(prefisso_passi or [])
    passi.append(_passo("Funzione e vincolo:", testo_latex))
    passi.extend(vinc_passi)
    passi.append(_passo_regolarita_latex(g, x, y, 2))
    if passo_extra_regolarita:
        passi.extend(passo_extra_regolarita)
    passi.append(_passo_lagrangiana_latex(f, g, x, y, 3))

    # --- Passo 4: sistema e sua risoluzione senza perdere casi ---
    passi.append(_passo(
        "Passo 4 — in forma vettoriale: i gradienti sono paralleli, gradiente(f) = λ·gradiente(g), "
        "insieme a g=0. Scriviamo il sistema componente per componente:",
        r"\begin{cases}" + _tex(fx) + r"=\lambda\left(" + _tex(gx) + r"\right)\\"
        + _tex(fy) + r"=\lambda\left(" + _tex(gy) + r"\right)\\" + _tex(g) + r"=0\end{cases}"))
    if nota_sistema is not None:
        passi.extend(nota_sistema)
        cand = _ordina(punti)
    else:
        passi.append(_passo(
            "Risolviamo il sistema senza perdere casi eliminando λ: i due gradienti sono paralleli "
            "se e solo se il loro \"prodotto incrociato\" si annulla (nei punti regolari, dove ∇g≠0, "
            "equivale alle prime due equazioni). Fattorizziamo:",
            r"f_x\,g_y-f_y\,g_x=0\iff " + _tex(cross) + "=0"))
        num = sp.fraction(sp.together(cross))[0]
        facs = [(fc, m_) for fc, m_ in sp.factor_list(num)[1]
                if not (fc.func is sp.exp or fc.is_Pow and fc.base == sp.E)]
        raccolti = []
        k = 0
        for fac, mult in facs:
            if not (fac.has(x) or fac.has(y)):
                continue
            if any(sp.simplify(fac - ig) == 0 for ig in fattori_ignora):
                continue
            k += 1
            try:
                sols = _reali(sp.solve([fac, g], [x, y], dict=True))
            except Exception:
                sols = []
            raccolti.extend(sols)
            elenco = (",\\ ".join(_pt(a, b) for a, b in _ordina(sols)) if sols
                      else r"\text{nessuna soluzione reale}")
            passi.append(_passo(
                f"Caso {k}: annulliamo il fattore {k}-esimo (formula a destra) e lo mettiamo a sistema con g=0:",
                _tex(fac) + r"=0\ \text{ e }\ " + _tex(g) + r"=0\ \Rightarrow\ " + elenco))
        cand = _ordina(punti if punti is not None else raccolti)
    sing = list(singolari or [])

    # --- moltiplicatori e valori ---
    lam_pts = []
    for (px, py) in cand:
        gxv, gyv = gx.subs({x: px, y: py}), gy.subs({x: px, y: py})
        fxv, fyv = fx.subs({x: px, y: py}), fy.subs({x: px, y: py})
        lv = sp.simplify(fxv / gxv) if sp.simplify(gxv) != 0 else sp.simplify(fyv / gyv)
        if lambdas is not None and (px, py) in lambdas:
            lv = lambdas[(px, py)]
        assert sp.simplify(fxv - lv * gxv) == 0 and sp.simplify(fyv - lv * gyv) == 0, (fonte, px, py)
        assert sp.simplify(g.subs({x: px, y: py})) == 0, (fonte, px, py, 'non sul vincolo')
        val = sp.simplify(f.subs({x: px, y: py}))
        lam_pts.append((px, py, lv, val, fxv, fyv, gxv, gyv))
    passi.append(_passo("Passo 5 — le soluzioni sono i punti stazionari vincolati; per ciascuno ricaviamo "
                        "il moltiplicatore λ da una delle due equazioni e verifichiamo che ∇f=λ∇g "
                        "(a destra il valore di f nel punto):", None))
    for (px, py, lv, val, fxv, fyv, gxv, gyv) in lam_pts:
        passi.append(_passo("", r"(x,y)=" + _pt(px, py) + r",\ \lambda=" + _tex(lv)
                              + r":\ \nabla f=(" + _tex(fxv) + "," + _tex(fyv) + r")=\lambda\nabla g=("
                              + _tex(sp.simplify(lv * gxv)) + "," + _tex(sp.simplify(lv * gyv))
                              + r")\ \Rightarrow\ f=" + _tex(val)))
    sing_vals = []
    for (px, py, txt) in sing:
        val = sp.simplify(f.subs({x: px, y: py}))
        sing_vals.append((px, py, val))
        passi.append(_passo(txt, r"(x,y)=" + _pt(px, py) + r":\ f=" + _tex(val)))

    # --- Hessiano orlato ---
    Lxx = sp.diff(f, x, 2) - lam * sp.diff(g, x, 2)
    Lxy = sp.diff(f, x, y) - lam * sp.diff(g, x, y)
    Lyy = sp.diff(f, y, 2) - lam * sp.diff(g, y, 2)
    Hb = sp.Matrix([[0, gx, gy], [gx, Lxx, Lxy], [gy, Lxy, Lyy]])
    passi.append(_passo(
        "Passo 6 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario), con L=f-λg: "
        "se det H̄>0 il punto è un massimo relativo vincolato, se det H̄<0 un minimo relativo vincolato "
        "(se det H̄=0 il test non decide). Matrice generale:",
        r"\overline{H}=\begin{pmatrix}0&g_x&g_y\\g_x&L_{xx}&L_{xy}\\g_y&L_{xy}&L_{yy}\end{pmatrix}="
        + _mat(Hb)))
    classi = []
    for (px, py, lv, val, *_r) in lam_pts:
        cl = _mv._classifica_hessiana_orlata(f, g, px, py, lv)
        classi.append(cl)
        Hn = Hb.subs({x: px, y: py, lam: lv})
        passi.append(_passo(
            f"Nel punto ({_ptxt(px)}, {_ptxt(py)}) con λ={_ptxt(lv)}:",
            r"\overline{H}=" + _mat(Hn) + r",\quad \det\overline{H}=" + _tex(cl['det'])
            + r"\ \Rightarrow\ \textbf{" + cl['tipo'] + "}"))

    # --- assoluti ---
    tutti = [(px, py, val) for (px, py, lv, val, *_r) in lam_pts] + sing_vals
    if compatto:
        vmaxv = sp.simplify(max([t[2] for t in tutti], key=lambda v: float(sp.N(v))))
        vminv = sp.simplify(min([t[2] for t in tutti], key=lambda v: float(sp.N(v))))
        elenco = ",\\ ".join("f" + _pt(px, py) + "=" + _tex(val) for px, py, val in tutti)
        passi.append(_passo(
            "Passo 7 — il vincolo è compatto (chiuso e limitato) e f è continua: per Weierstrass "
            "esistono massimo e minimo assoluti, e si trovano confrontando i valori di f in TUTTI i "
            "punti stazionari (anche quelli che l'orlato classifica come relativi):", elenco))
        pmax = [(px, py) for px, py, v in tutti if sp.simplify(v - vmaxv) == 0]
        pmin = [(px, py) for px, py, v in tutti if sp.simplify(v - vminv) == 0]
        passi.append(_passo(
            "Conclusione (Weierstrass) — massimo assoluto e minimo assoluto:",
            r"\max f=" + _tex(vmaxv) + r"\ \text{in }" + ",".join(_pt(*p) for p in pmax)
            + r";\qquad \min f=" + _tex(vminv) + r"\ \text{in }" + ",".join(_pt(*p) for p in pmin)))
        if val_max == 'auto':
            val_max = vmaxv
        if val_min == 'auto':
            val_min = vminv
    else:
        if passi_assoluti:
            passi.extend(passi_assoluti)
        if val_max == 'auto':
            val_max = None
        if val_min == 'auto':
            val_min = None

    # --- verifica numerica indipendente (campionando la curva) ---
    if verifica and compatto:
        C = _campioni_curva(g, box)
        fl = sp.lambdify((x, y), f, 'numpy')
        with np.errstate(all='ignore'):
            vals = np.asarray(fl(C[:, 0], C[:, 1]), dtype=float)
        vm, vn = float(sp.N(val_max)), float(sp.N(val_min))
        assert abs(np.nanmax(vals) - vm) < 3e-2 * max(1, abs(vm)), (fonte, np.nanmax(vals), vm)
        assert abs(np.nanmin(vals) - vn) < 3e-2 * max(1, abs(vn)), (fonte, np.nanmin(vals), vn)

    # --- figura ---
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    xs = np.linspace(box[0], box[1], 700)
    ys = np.linspace(box[2], box[3], 700)
    X, Y = np.meshgrid(xs, ys)
    G = np.asarray(sp.lambdify((x, y), g, 'numpy')(X, Y), dtype=float) * np.ones_like(X)
    ax.contour(X, Y, G, [0], colors=_COL_VINC, linewidths=2.2)
    ax.plot([], [], color=_COL_VINC, linewidth=2.2, label=titolo_curva)
    for (px, py, lv, val, *_r) in lam_pts:
        ax.plot(float(px), float(py), 'o', color=_COL_PT, markersize=7)
        ax.annotate("f=" + _fmt(val), (float(px), float(py)), textcoords="offset points",
                    xytext=(7, 7), fontsize=8)
    for (px, py, val) in sing_vals:
        ax.plot(float(px), float(py), 's', color='#8e44ad', markersize=7)
        ax.annotate("f=" + _fmt(val) + " (a parte)", (float(px), float(py)), textcoords="offset points",
                    xytext=(7, -12), fontsize=8)
    ax.set_xlim(box[0], box[1]); ax.set_ylim(box[2], box[3])
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.5); ax.axvline(0, color='gray', linewidth=0.5)
    ax.legend(loc='best', fontsize=8)
    ax.set_title("Vincolo e punti stazionari (" + fonte + ")", fontsize=9.5)
    fig.tight_layout()
    png = _png(fig)

    attesi = [[float(sp.N(px)), float(sp.N(py)), float(sp.N(val))] for px, py, val in tutti]
    risposta = {"tipo": "punti_valore", "punti_attesi": attesi,
                "valore_max": None if val_max is None else float(sp.N(val_max)),
                "valore_min": None if val_min is None else float(sp.N(val_min))}
    testo = "[" + fonte + ", Esercizio " + str(n) + "] " + enunciato
    return _voce(fonte, testo, testo_latex,
                 hint or "Un punto per riga, formato x,y (es: 1,0): tutti i punti stazionari vincolati.",
                 passi, risposta, png)


# ---------------------------------------------------------------------------
# LIBERI: costruttore generale
# ---------------------------------------------------------------------------

def _tipo_hess(f, px, py):
    """(H, det, fxx, tipo) nel punto (px,py) con il teorema dell'Hessiana."""
    H = sp.hessian(f, (x, y)).subs({x: px, y: py}).applyfunc(sp.simplify)
    det = sp.simplify(H.det())
    fxx = H[0, 0]
    if sp.simplify(det) == 0:
        tipo = 'indeterminato'
    else:
        d = float(sp.N(det))
        a = float(sp.N(fxx))
        if d < 0:
            tipo = 'sella'
        elif a > 0:
            tipo = 'minimo'
        else:
            tipo = 'massimo'
    return H, det, fxx, tipo


def _passi_liberi(f, punti, *, risol=None, override=None, post=None, num0=1, intro_gradiente=None):
    """Passi 'annulliamo il gradiente' -> Hessiana -> classificazione. Restituisce (passi, tipi)."""
    fx, fy = sp.diff(f, x), sp.diff(f, y)
    passi = []
    sfx = sp.factor(sp.simplify(fx)) if f.has(sp.exp, sp.log) else sp.factor(fx)
    sfy = sp.factor(sp.simplify(fy)) if f.has(sp.exp, sp.log) else sp.factor(fy)
    passi.append(_passo(intro_gradiente or
                        f"Passo {num0} — annulliamo il gradiente per trovare i punti stazionari "
                        "(condizione necessaria per un estremo libero):",
                        r"\begin{cases}f_x=" + _tex(sfx) + r"=0\\ f_y=" + _tex(sfy) + r"=0\end{cases}"))
    if risol:
        passi.extend(risol)
    else:
        elenco = ",\\ ".join(_pt(a, b) for a, b in punti)
        passi.append(_passo("Risolvendo il sistema si trovano i punti stazionari:", elenco))
    fxx, fxy, fyy = sp.diff(f, x, 2), sp.diff(f, x, y), sp.diff(f, y, 2)
    Hg = sp.hessian(f, (x, y)).applyfunc(sp.simplify)
    passi.append(_passo(
        f"Passo {num0 + 1} — calcoliamo le derivate parziali seconde e scriviamo la matrice Hessiana:",
        r"f_{xx}=" + _tex(sp.simplify(fxx)) + r",\ f_{xy}=" + _tex(sp.simplify(fxy)) + r",\ f_{yy}="
        + _tex(sp.simplify(fyy)) + r"\ \Rightarrow\ H(x,y)=" + _mat(Hg)))
    passi.append(_passo(
        f"Passo {num0 + 2} — per ogni punto stazionario valutiamo l'Hessiana (teorema dell'Hessiana, dal "
        "formulario): det H>0 e f_xx>0 ⇒ minimo; det H>0 e f_xx<0 ⇒ massimo; det H<0 ⇒ sella; "
        "det H=0 ⇒ il test non decide.", None))
    tipi = []
    for (px, py) in punti:
        H, det, fxxv, tipo = _tipo_hess(f, px, py)
        extra = None
        if override and (px, py) in override:
            tipo, extra = override[(px, py)]
        tipi.append(tipo)
        concl = r"\textbf{" + tipo.upper() + "}"
        if override and (px, py) in override and sp.simplify(det) == 0:
            concl = r"\text{test inconcludente; studio diretto: }" + concl
        passi.append(_passo(
            f"Punto ({_ptxt(px)}, {_ptxt(py)}):",
            r"H=" + _mat(H) + r",\ \det H=" + _tex(det) + r",\ f_{xx}=" + _tex(fxxv)
            + r"\ \Rightarrow\ " + concl))
        if extra:
            passi.extend(extra)
    if post:
        passi.extend(post)
    return passi, tipi


def _verifica_locale(f, px, py, tipo, fonte):
    """Controllo numerico indipendente della natura di (px,py) campionando f su piccole circonferenze."""
    fl = sp.lambdify((x, y), f, 'numpy')
    f0 = float(fl(float(px), float(py)))
    th = np.linspace(0, 2*np.pi, 40001)
    segni = set()
    for r in (2e-1, 1e-1, 5e-2):
        with np.errstate(all='ignore'):
            v = np.asarray(fl(float(px) + r*np.cos(th), float(py) + r*np.sin(th)), dtype=float) - f0
        v = v[np.isfinite(v)]
        sc = max(1e-300, np.max(np.abs(v)))
        if (v > 1e-12*sc).any():
            segni.add('+')
        if (v < -1e-12*sc).any():
            segni.add('-')
    if tipo == 'minimo':
        ok = segni <= {'+'}
    elif tipo == 'massimo':
        ok = segni <= {'-'}
    elif tipo == 'sella':
        ok = segni == {'+', '-'}
    else:
        ok = True
    assert ok, (fonte, px, py, tipo, segni)


def _fig_liberi(f, box, punti, tipi, titolo, extra_linee=None, mask=None, levels=22, segno=False):
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    xs = np.linspace(box[0], box[1], 500)
    ys = np.linspace(box[2], box[3], 500)
    X, Y = np.meshgrid(xs, ys)
    with np.errstate(all='ignore'):
        Z = np.asarray(sp.lambdify((x, y), f, 'numpy')(X, Y), dtype=float) * np.ones_like(X)
    Z = np.where(np.isfinite(Z), Z, np.nan)
    lim = np.nanpercentile(np.abs(Z), 92) if np.isfinite(Z).any() else 1.0
    Zc = np.clip(Z, -lim, lim)
    if segno:
        from matplotlib.patches import Patch
        ax.contourf(X, Y, np.sign(Z), levels=[-1.5, -0.5, 0.5, 1.5], colors=['#aed6f1', '#ffffff', '#f5b7b1'])
        ax.contour(X, Y, Zc, levels=[0], colors='k', linewidths=1.2)
        ax.legend(handles=[Patch(color='#f5b7b1', label='f>0'), Patch(color='#aed6f1', label='f<0')],
                  fontsize=8, loc='upper right')
    else:
        cs = ax.contourf(X, Y, Zc, levels=levels, cmap='RdBu_r', alpha=0.85)
        ax.contour(X, Y, Zc, levels=[0], colors='k', linewidths=1.2)
        fig.colorbar(cs, ax=ax, shrink=0.75, label="f")
    col = {'minimo': '#1a7f37', 'massimo': '#c0392b', 'sella': '#8e44ad', 'indeterminato': '#f39c12'}
    for (px, py), t in zip(punti, tipi):
        ax.plot(float(px), float(py), 'o', color=col.get(t, 'k'), markeredgecolor='k', markersize=8)
        ax.annotate(t, (float(px), float(py)), textcoords="offset points", xytext=(6, 6), fontsize=8)
    if extra_linee:
        for el in extra_linee:
            if len(el) == 5:
                xa, ya, xb, yb, lab = el
                ax.plot([xa, xb], [ya, yb], '--', color='#2e5c8a', linewidth=1.6, label=lab)
            else:
                xs_, ys_, lab = el
                ax.plot(xs_, ys_, '-', color='#1a7f37', linewidth=3, label=lab)
        ax.legend(fontsize=7, loc='best')
    ax.set_xlim(box[0], box[1]); ax.set_ylim(box[2], box[3])
    ax.set_aspect('equal', 'box')
    ax.set_title(titolo, fontsize=9.5)
    fig.tight_layout()
    return _png(fig)


def _liberi(fonte, n, enunciato, f, punti, *, pre=None, risol=None, override=None, post=None,
            box=(-3, 3, -3, 3), hint=None, extra_attesi=None, nota_testo=None, num0=1,
            extra_linee=None, testo_latex=None, levels=22, intro_gradiente=None, fig_titolo=None, segno=False):
    """Costruisce una voce ESAME['punti_liberi'] con tutti i passaggi."""
    punti = _ordina(punti)
    testo_latex = testo_latex or (r"f(x,y)=" + _tex(sp.expand(f) if f.is_polynomial(x, y) else f))
    passi = [_passo("Funzione:", testo_latex)]
    if pre:
        passi.extend(pre)
    pp, tipi = _passi_liberi(f, punti, risol=risol, override=override, post=post, num0=num0,
                             intro_gradiente=intro_gradiente)
    passi.extend(pp)
    png = _fig_liberi(f, box, punti, tipi, fig_titolo or ("Livelli di f e punti stazionari (" + fonte + ")"),
                      extra_linee=extra_linee, levels=levels, segno=segno)
    attesi = [[float(sp.N(px)), float(sp.N(py)), t] for (px, py), t in zip(punti, tipi)]
    if extra_attesi:
        attesi.extend(extra_attesi)
    for px, py, t in attesi:
        _verifica_locale(f, px, py, t, fonte)
    risposta = {"tipo": "punti_classificati", "attesi": attesi}
    testo = "[" + fonte + ", Esercizio " + str(n) + "] " + enunciato + (" " + nota_testo if nota_testo else "")
    return _voce(fonte, testo, testo_latex,
                 hint or "Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, "
                         "sella, indeterminato.",
                 passi, risposta, png)

# ---------------------------------------------------------------------------
# VINCOLATI -- batch A: vincoli compatti (circonferenze ed ellissi), sistema risolto per fattori
# ---------------------------------------------------------------------------

def _enun(fdesc, gdesc, a="disegnare il vincolo descrivendone le caratteristiche",
          b="determinare gli eventuali punti di massimo e di minimo utilizzando il metodo dei "
            "moltiplicatori di Lagrange e la matrice Hessiana orlata"):
    return (f"Data la funzione f(x,y) = {fdesc} soggetta al vincolo g(x,y) = {gdesc} = 0: "
            f"a) {a}; b) {b}.")


def _tl(f, g, gtxt=None):
    return r"f(x,y)=" + _tex(f) + r",\quad g(x,y)=" + (gtxt or _tex(g)) + "=0"


def _batch_A():
    out = []
    # 1) 15 maggio 2026 (= 11 settembre 2025, 7 maggio 2026): xy su ellisse 4x^2+9y^2=16
    f = x*y; g = 4*x**2 + 9*y**2 - 16
    out.append(_lag("15 maggio 2026", 1, _enun("xy", "4x²+9y²-16"), _tl(f, g), f, g,
                    _v_ellisse(g, 0, 0, 2, sp.Rational(4, 3)), compatto=True, box=(-2.6, 2.6, -2.2, 2.2),
                    titolo_curva="4x²+9y²=16"))
    # 2) 20 settembre 2025: x + y^2 su x^2+y^2=25
    f = x + y**2; g = x**2 + y**2 - 25
    out.append(_lag("20 settembre 2025", 1, _enun("x+y²", "x²+y²-25"), _tl(f, g), f, g,
                    _v_circ(g, 0, 0, 5, completa=False), compatto=True, box=(-6.5, 6.5, -6.5, 6.5),
                    titolo_curva="x²+y²=25"))
    # 3) 18 settembre 2025: x^2 - y - 2x su x^2+y^2-2x=0
    f = x**2 - y - 2*x; g = x**2 + y**2 - 2*x
    out.append(_lag("18 settembre 2025", 1, _enun("x²-y-2x", "x²+y²-2x"), _tl(f, g), f, g,
                    _v_circ(g, 1, 0, 1), compatto=True, box=(-0.6, 2.6, -1.6, 1.6),
                    titolo_curva="(x-1)²+y²=1"))
    # 8) 1 dicembre 2025: x+y su x^2+y^2-4x-4y-1=0
    f = x + y; g = x**2 + y**2 - 4*x - 4*y - 1
    out.append(_lag("1 dicembre 2025", 1, _enun("x+y", "x²+y²-4x-4y-1"), _tl(f, g), f, g,
                    _v_circ(g, 2, 2, 3), compatto=True, box=(-2, 6, -2, 6),
                    titolo_curva="(x-2)²+(y-2)²=9"))
    # 10) aprile 2025: x^2+y^2 su (x-1)^2+(y-2)^2=20
    f = x**2 + y**2; g = (x - 1)**2 + (y - 2)**2 - 20
    out.append(_lag("aprile 2025", 1, _enun("x²+y²", "(x-1)²+(y-2)²-20"), _tl(f, g), f, g,
                    _v_circ(g, 1, 2, 2*sp.sqrt(5), completa=False), compatto=True, box=(-4.5, 6.5, -3, 7),
                    titolo_curva="(x-1)²+(y-2)²=20"))
    # 13) dicembre 2024: -x^3-4xy^2+16x+1 su x^2+y^2=4
    f = -x**3 - 4*x*y**2 + 16*x + 1; g = x**2 + y**2 - 4
    out.append(_lag("dicembre 2024", 1, _enun("-x³-4xy²+16x+1", "x²+y²-4",
                    b="determinare tutti i punti stazionari e quali, tra quelli trovati, sono di massimo e "
                      "di minimo assoluto (metodo di Lagrange e Hessiano orlato)"),
                    _tl(f, g), f, g, _v_circ(g, 0, 0, 2, completa=False), compatto=True,
                    box=(-2.8, 2.8, -2.8, 2.8), titolo_curva="x²+y²=4"))
    # 15) dicembre 2024: y^3+4x^2y-4y su x^2+y^2=1
    f = y**3 + 4*x**2*y - 4*y; g = x**2 + y**2 - 1
    out.append(_lag("dicembre 2024", 5, _enun("y³+4x²y-4y", "x²+y²-1",
                    b="determinare tutti i punti stazionari e quali, tra quelli trovati, sono di massimo e "
                      "di minimo assoluto"),
                    _tl(f, g), f, g, _v_circ(g, 0, 0, 1, completa=False), compatto=True,
                    box=(-1.5, 1.5, -1.5, 1.5), titolo_curva="x²+y²=1"))
    # 17) ottobre 2024: x^2+3y su x^2/4+y^2/9=1
    f = x**2 + 3*y; g = x**2/4 + y**2/9 - 1
    out.append(_lag("ottobre 2024", 4, _enun("x²+3y", "x²/4+y²/9-1"), _tl(f, g), f, g,
                    _v_ellisse(g, 0, 0, 2, 3), compatto=True, box=(-2.8, 2.8, -3.6, 3.6),
                    titolo_curva="x²/4+y²/9=1"))
    # 18) ottobre 2024: xy su x^2+4y^2=1
    f = x*y; g = x**2 + 4*y**2 - 1
    out.append(_lag("ottobre 2024", 10, _enun("xy", "x²+4y²-1"), _tl(f, g), f, g,
                    _v_ellisse(g, 0, 0, 1, sp.Rational(1, 2)), compatto=True, box=(-1.4, 1.4, -0.9, 0.9),
                    titolo_curva="x²+4y²=1"))
    # 20) luglio 2024: 5/4(x^2+y^2)+3/2 xy su x^2+y^2=4
    f = sp.Rational(5, 4)*(x**2 + y**2) + sp.Rational(3, 2)*x*y; g = x**2 + y**2 - 4
    out.append(_lag("luglio 2024", 2, _enun("(5/4)(x²+y²)+(3/2)xy", "x²+y²-4"), _tl(f, g), f, g,
                    _v_circ(g, 0, 0, 2, completa=False), compatto=True, box=(-2.8, 2.8, -2.8, 2.8),
                    titolo_curva="x²+y²=4"))
    # 21) maggio 2024: x^4+y^4-8(x^2+y^2) su x^2+y^2=9
    f = x**4 + y**4 - 8*(x**2 + y**2); g = x**2 + y**2 - 9
    out.append(_lag("maggio 2024", 1, _enun("x⁴+y⁴-8(x²+y²)", "x²+y²-9"), _tl(f, g), f, g,
                    _v_circ(g, 0, 0, 3, completa=False), compatto=True, box=(-4, 4, -4, 4),
                    titolo_curva="x²+y²=9"))
    # 23) gennaio 2024: 2x^2-2y^2+22x su x^2+7y^2=11
    f = 2*x**2 - 2*y**2 + 22*x; g = x**2 + 7*y**2 - 11
    out.append(_lag("gennaio 2024", 4, _enun("2x²-2y²+22x", "x²+7y²-11",
                    a="disegnare D",
                    b="studiare la natura dei punti stazionari con il metodo dei moltiplicatori di "
                      "Lagrange e con la matrice Hessiana orlata"),
                    _tl(f, g), f, g, _v_ellisse(g, 0, 0, sp.sqrt(11), sp.sqrt(sp.Rational(11, 7))),
                    compatto=True, box=(-3.8, 3.8, -2.2, 2.2), titolo_curva="x²+7y²=11"))
    # 26) ottobre 2023: (x-3)^2+(y-3)^2-1 su x^2+y^2=16
    f = (x - 3)**2 + (y - 3)**2 - 1; g = x**2 + y**2 - 16
    out.append(_lag("ottobre 2023", 1, "Data la funzione f(x,y) = (x-3)²+(y-3)²-1, soggetta al vincolo "
                    "g(x,y) = x²+y²-16 = 0, determinare con il metodo della Lagrangiana e con l'Hessiano "
                    "orlato la natura dei punti stazionari.",
                    _tl(f, g), f, g, _v_circ(g, 0, 0, 4, completa=False), compatto=True,
                    box=(-5, 5, -5, 5), titolo_curva="x²+y²=16"))
    # 28) luglio 2023: x^2+2y^2 su x^2+y^2=1
    f = x**2 + 2*y**2; g = x**2 + y**2 - 1
    out.append(_lag("luglio 2023", 13, "Data la funzione f(x,y) = x²+2y², soggetta al vincolo "
                    "g(x,y) = x²+y²-1 = 0, determinare con il metodo della Lagrangiana e con l'Hessiano "
                    "orlato la natura dei punti stazionari.",
                    _tl(f, g), f, g, _v_circ(g, 0, 0, 1, completa=False), compatto=True,
                    box=(-1.5, 1.5, -1.5, 1.5), titolo_curva="x²+y²=1"))
    return out

# ---------------------------------------------------------------------------
# VINCOLATI -- batch B: vincoli non compatti (rette, parabole, ...) e casi con trattazione dedicata
# ---------------------------------------------------------------------------

def _passo_noncompatto(testo_lim, lat_lim):
    return _passo("Passo 7 — il vincolo NON è compatto (non è limitato): il teorema di Weierstrass non si "
                  "applica, quindi non è garantita l'esistenza di massimo e minimo assoluti. " + testo_lim,
                  lat_lim)


def _batch_B():
    out = []

    # --- 17 settembre 2025: xy su parabola y = 3x^2-4x-1 ---
    f = x*y; g = 3*x**2 - 4*x - 1 - y
    pa = [_passo_noncompatto(
        "Sostituiamo y=3x²-4x-1 in f e studiamo la funzione di una sola variabile agli estremi:",
        r"h(x)=f(x,3x^2-4x-1)=3x^3-4x^2-x,\qquad \lim_{x\to+\infty}h=+\infty,\ \ \lim_{x\to-\infty}h=-\infty"),
          _passo("Conclusione: f non è limitata né superiormente né inferiormente sul vincolo, quindi NON "
                 "esistono massimo né minimo assoluti; i punti trovati sono solo estremi relativi "
                 "(massimo e minimo locale di h).", None)]
    out.append(_lag("17 settembre 2025", 1, _enun("xy", "3x²-4x-1-y"), _tl(f, g), f, g,
                    _v_parabola_y(g, 3, sp.Rational(2, 3), -sp.Rational(7, 3)), compatto=False,
                    box=(-1.5, 2.5, -3, 4), passi_assoluti=pa, titolo_curva="y=3x²-4x-1"))

    # --- gennaio 2025 (es. 4): x^2 y su parabola y = x^2+2x-2 ---
    f = x**2*y; g = x**2 + 2*x - y - 2
    pa = [_passo_noncompatto(
        "Restringiamo f al vincolo (y=x²+2x-2) e studiamo gli estremi di h(x)=x²(x²+2x-2):",
        r"h(x)=x^4+2x^3-2x^2,\qquad \lim_{x\to\pm\infty}h=+\infty"),
          _passo("Conclusione: f non ha massimo assoluto (h→+∞). Poiché h→+∞ per x→±∞, il minimo assoluto "
                 "esiste ed è il più piccolo dei valori nei punti stazionari: si confrontano i tre valori.",
                 r"f(0,-2)=0,\ \ f(\tfrac12,-\tfrac34)=-\tfrac{3}{16},\ \ f(-2,-2)=-8\ \Rightarrow\ "
                 r"\min f=-8\ \text{in }(-2,-2),\quad \max f\ \text{non esiste}")]
    out.append(_lag("gennaio 2025", 4, _enun("x²y", "x²+2x-y-2"), _tl(f, g), f, g,
                    _v_parabola_y(g, 1, -1, -3), compatto=False, box=(-4, 3, -4, 6),
                    passi_assoluti=pa, val_max=None, val_min=sp.Integer(-8), titolo_curva="y=x²+2x-2"))

    # --- aprile 2024 (es. 2): e^x + e^y su x+y=2 ---
    f = sp.exp(x) + sp.exp(y); g = x + y - 2
    pa = [_passo_noncompatto(
        "Restringiamo f alla retta (y=2-x): h(x)=e^x+e^(2-x) tende a +∞ sia per x→+∞ sia per x→-∞:",
        r"h(x)=e^x+e^{2-x},\qquad \lim_{x\to\pm\infty}h=+\infty"),
          _passo("Conclusione: non esiste il massimo assoluto; poiché h→+∞ agli estremi e c'è un solo punto "
                 "stazionario, (1,1) è il minimo assoluto (h convessa).",
                 r"\min f=f(1,1)=2e,\qquad \max f\ \text{non esiste}")]
    out.append(_lag("aprile 2024", 2, "Utilizzando il metodo dei moltiplicatori di Lagrange e la matrice "
                    "Hessiana orlata determinare i punti di massimo e di minimo della funzione f(x,y) = "
                    "e^x+e^y soggetta al vincolo x+y=2.", _tl(f, g), f, g, _v_retta(g, -1, 2),
                    compatto=False, box=(-2, 4, -2, 4), passi_assoluti=pa, val_max=None,
                    val_min=2*sp.E, titolo_curva="x+y=2"))

    # --- luglio 2023 (es. 1): x^2+y^2 su x^2 y = 2 ---
    f = x**2 + y**2; g = x**2*y - 2
    v = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: esplicitando y si ottiene una curva del tipo "
                "y=k/x² (non è una conica):", r"x^2y-2=0\iff y=\frac{2}{x^2}\quad(x\ne0)"),
         _passo("Caratteristiche della curva: definita per x≠0, sempre y>0, simmetrica rispetto all'asse y "
                "(funzione pari); è formata da due rami, uno per x>0 e uno per x<0, con asintoti l'asse y "
                "(y→+∞ per x→0) e l'asse x (y→0 per x→±∞). Non è limitata: NON compatta.",
                r"y=\frac{2}{x^2}>0,\quad y\to+\infty\ (x\to0),\quad y\to0^+\ (x\to\pm\infty)")]
    pa = [_passo_noncompatto(
        "Restringiamo f al vincolo (y=2/x²): h(x)=x²+4/x⁴ tende a +∞ sia per x→0 sia per x→±∞:",
        r"h(x)=x^2+\frac{4}{x^4},\qquad \lim_{x\to0}h=+\infty,\ \ \lim_{x\to\pm\infty}h=+\infty"),
          _passo("Conclusione: f non ha massimo assoluto; il minimo assoluto esiste (h→+∞ agli estremi) ed è "
                 "il valore comune dei due punti stazionari, simmetrici rispetto all'asse y.",
                 r"\min f=3\ \text{in }(\pm\sqrt2,1),\qquad \max f\ \text{non esiste}")]
    out.append(_lag("luglio 2023", 1, "Data la funzione f(x,y) = x²+y², soggetta al vincolo g(x,y) = x²y-2 = 0, "
                    "determinare con il metodo della Lagrangiana e con l'Hessiano orlato la natura dei "
                    "punti stazionari.", _tl(f, g), f, g, v, compatto=False, box=(-3, 3, -0.5, 6),
                    passi_assoluti=pa, val_max=None, val_min=sp.Integer(3), titolo_curva="x²y=2"))

    # --- 16 settembre 2025: x^3+4xy^2-4x su x^2+y^2=1 (Hessiano nullo da tralasciare) ---
    f = x**3 + 4*x*y**2 - 4*x; g = x**2 + y**2 - 1
    out.append(_lag("16 settembre 2025", 1,
                    "Data la funzione f(x,y) = x³+4xy²-4x soggetta al vincolo g(x,y) = x²+y²-1 = 0: "
                    "a) disegnare il vincolo descrivendone le caratteristiche; b) determinare gli eventuali "
                    "punti di massimo e di minimo (tralasciare lo studio dei punti con Hessiano nullo).",
                    _tl(f, g), f, g, _v_circ(g, 0, 0, 1, completa=False), compatto=True,
                    box=(-1.5, 1.5, -1.5, 1.5), titolo_curva="x²+y²=1"))
    return out

# ---------------------------------------------------------------------------
# VINCOLATI -- batch C: ellissi con esponenziali, iperbole, casi con trattazione dedicata
# ---------------------------------------------------------------------------

def _batch_C():
    out = []

    # --- 14 gennaio 2026: e^{x^2+y^2} sull'ellisse x^2+(y-1/2)^2/4=1 ---
    f = sp.exp(x**2 + y**2); g = x**2 + (y - sp.Rational(1, 2))**2/4 - 1
    out.append(_lag("14 gennaio 2026", 1,
                    "Data la funzione f(x,y) = e^(x²+y²) soggetta al vincolo g(x,y) = x²+(1/4)(y-1/2)²-1 = 0: "
                    "a) descrivere le caratteristiche del vincolo e disegnarlo; b) determinare tutti i punti "
                    "stazionari; c) determinare quali sono, tra quelli trovati, i punti di massimo e di "
                    "minimo assoluto.",
                    _tl(f, g), f, g, _v_ellisse(g, 0, sp.Rational(1, 2), 1, 2), compatto=True,
                    box=(-1.6, 1.6, -2.2, 3.2), titolo_curva="x²+(y-1/2)²/4=1"))

    # --- dicembre 2024 (es. 4): e^{-x^2-y^2} su (x-1)^2+4y^2=4 ---
    f = sp.exp(-x**2 - y**2); g = (x - 1)**2 + 4*y**2 - 4
    out.append(_lag("dicembre 2024", 4,
                    "Data la funzione f(x,y) = e^(-x²-y²) soggetta al vincolo g(x,y) = (x-1)²+4y²-4 = 0: "
                    "a) determinare tutti i punti stazionari; b) determinare quali sono, tra quelli "
                    "trovati, i punti di massimo e di minimo assoluto.",
                    _tl(f, g), f, g, _v_ellisse(g, 1, 0, 2, 1), compatto=True, box=(-1.8, 3.8, -1.8, 1.8),
                    titolo_curva="(x-1)²+4y²=4"))

    # --- luglio 2024 (es. 1): e^{x^2+2xy-y^2} su x^2/4+y^2/6=1 ---
    f = sp.exp(x**2 + 2*x*y - y**2); g = x**2/4 + y**2/6 - 1
    out.append(_lag("luglio 2024", 1,
                    "Data la funzione f(x,y) = e^(x²+2xy-y²) soggetta al vincolo x²/4+y²/6 = 1: "
                    "a) disegnare il vincolo descrivendone le caratteristiche; b) utilizzando il metodo dei "
                    "moltiplicatori di Lagrange, determinare gli eventuali punti di massimo e minimo.",
                    _tl(f, g, r"\frac{x^2}{4}+\frac{y^2}{6}-1"), f, g,
                    _v_ellisse(g, 0, 0, 2, sp.sqrt(6)), compatto=True, box=(-2.8, 2.8, -3.2, 3.2),
                    titolo_curva="x²/4+y²/6=1"))

    # --- dicembre 2023 (es. 1): 3xy^2-2xy+1 sull'iperbole xy-3+y=0 ---
    f = 3*x*y**2 - 2*x*y + 1; g = x*y - 3 + y
    v = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: raccogliendo y si ottiene y(x+1)=3, cioè "
                "l'equazione esplicita di un'iperbole equilatera traslata:",
                r"xy-3+y=0\iff y(x+1)=3\iff y=\frac{3}{x+1}\quad(x\ne-1)"),
         _passo("Caratteristiche della curva: iperbole di centro (-1,0) con asintoti la retta verticale "
                "x=-1 e la retta orizzontale y=0; due rami (uno con x>-1 e y>0, l'altro con x<-1 e y<0). "
                "Non è limitata: NON compatta (Weierstrass non applicabile).",
                r"\text{centro }(-1,0),\quad \text{asintoti: }x=-1,\ y=0,\quad y\to\pm\infty\ (x\to-1^{\pm})")]
    pa = [_passo_noncompatto(
        "Restringiamo f al vincolo (y=3/(x+1)) e studiamo h(x) sui due rami:",
        r"h(x)=f\!\left(x,\tfrac{3}{x+1}\right)=-\frac{5x^2-23x-1}{(x+1)^2}=-5+\frac{33x+6}{(x+1)^2}"),
          _passo("Per x→±∞ si ha h→-5, mentre per x→-1 (da entrambi i lati) h→-∞. Sul ramo x>-1, h parte da "
                 "-∞, ha un solo punto stazionario (x=7/11) e tende a -5 (<61/12): quindi il punto "
                 "stazionario è il massimo assoluto. Sul ramo x<-1 si ha h<-5<61/12. Il minimo assoluto "
                 "NON esiste (h→-∞).",
                 r"\max f=f\!\left(\tfrac{7}{11},\tfrac{11}{6}\right)=\tfrac{61}{12},\qquad \min f\ \text{non esiste}")]
    out.append(_lag("dicembre 2023", 1,
                    "Data la funzione f(x,y) = 3xy²-2xy+1, determinare il massimo e il minimo di f in "
                    "D = {(x,y) ∈ R²: xy-3+y = 0}.", _tl(f, g), f, g, v, compatto=False,
                    box=(-5, 5, -8, 8), passi_assoluti=pa, val_max=sp.Rational(61, 12), val_min=None,
                    titolo_curva="y=3/(x+1)"))

    # --- 15 settembre 2025: e^x + e^y su x^2+y^2=1 (sistema con funzioni trascendenti) ---
    f = sp.exp(x) + sp.exp(y); g = x**2 + y**2 - 1
    ns = [_passo("Risolviamo il sistema eliminando λ: imponendo che i gradienti siano paralleli (prodotto incrociato nullo) e "
                 "dividendo per e^(x+y)>0 si ottiene un'equazione in cui x e y compaiono simmetricamente:",
                 r"f_xg_y-f_yg_x=2ye^{x}-2xe^{y}=0\iff \frac{y}{e^{y}}=\frac{x}{e^{x}}\iff xe^{-x}=ye^{-y}"),
          _passo("Studiamo φ(t)=t·e^(-t): la derivata φ'(t)=(1-t)e^(-t) è positiva per t<1, quindi φ è "
                 "strettamente crescente su (-∞,1]. Sulla circonferenza x,y∈[-1,1]⊂(-∞,1], dunque φ(x)=φ(y) "
                 "è possibile solo se x=y:",
                 r"\varphi(t)=te^{-t},\ \varphi'(t)=(1-t)e^{-t}\gt0\ (t\lt1)\ \Rightarrow\ x=y"),
          _passo("Sostituiamo x=y nell'equazione della circonferenza (sistema ridotto):",
                 r"x=y,\ \ x^2+y^2=1\ \Rightarrow\ 2x^2=1\ \Rightarrow\ x=y=\pm\tfrac{1}{\sqrt2}=\pm\tfrac{\sqrt2}{2}")]
    out.append(_lag("15 settembre 2025", 1, _enun("e^x+e^y", "x²+y²-1"), _tl(f, g), f, g,
                    _v_circ(g, 0, 0, 1, completa=False), compatto=True, box=(-1.5, 1.5, -1.5, 1.5),
                    nota_sistema=ns, punti=[(-sp.sqrt(2)/2, -sp.sqrt(2)/2), (sp.sqrt(2)/2, sp.sqrt(2)/2)],
                    titolo_curva="x²+y²=1"))

    # --- 13 settembre 2025: sqrt(xy) su 2x+y=6 ---
    f = sp.sqrt(x*y); g = 2*x + y - 6
    v = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: equazione di primo grado, cioè una RETTA; in "
                "forma esplicita:", _tex(g) + r"=0\iff y=6-2x"),
         _passo("Caratteristiche della curva: retta di coefficiente angolare -2 e intercetta 6, che taglia "
                "gli assi in (3,0) e (0,6). La funzione f=√(xy) è definita solo per xy≥0: sulla retta ciò "
                "richiede x(6-2x)≥0, cioè 0≤x≤3. Quindi l'insieme su cui lavoriamo è il SEGMENTO di estremi "
                "(0,6) e (3,0) (chiuso e limitato, dunque compatto).",
                r"D=\{2x+y=6,\ xy\ge0\}=\{(x,6-2x):\,0\le x\le3\}\ \ \text{(segmento da }(0,6)\text{ a }(3,0))")]
    ns = [_passo("Risolviamo il sistema nei punti interni al segmento (0<x<3, dove xy>0), dove f è derivabile con "
                 "f_x=y/(2√(xy)), f_y=x/(2√(xy)). Eliminiamo λ con il prodotto "
                 "incrociato (g_x=2, g_y=1):",
                 r"f_xg_y-f_yg_x=\frac{y}{2\sqrt{xy}}-\frac{2x}{2\sqrt{xy}}=\frac{y-2x}{2\sqrt{xy}}=0\iff y=2x"),
          _passo("Mettiamo a sistema con la retta: sostituendo y=2x in 2x+y=6 si ha 4x=6:",
                 r"y=2x,\ \ 2x+y=6\ \Rightarrow\ x=\tfrac32,\ y=3\ \ (\text{interno al segmento})")]
    sing = [(0, 6, "Estremo (0,6) del segmento: qui xy=0 e f non è derivabile, quindi il metodo di "
                   "Lagrange non può vederlo: lo valutiamo direttamente."),
            (3, 0, "Estremo (3,0) del segmento: stessa situazione (xy=0), valutiamo direttamente f.")]
    out.append(_lag("13 settembre 2025", 1,
                    "Data la funzione f(x,y) = √(xy) soggetta al vincolo g(x,y) = 2x+y-6 = 0: a) disegnare il "
                    "vincolo descrivendone le caratteristiche; b) determinare gli eventuali punti di massimo "
                    "e di minimo utilizzando il metodo dei moltiplicatori di Lagrange e la matrice Hessiana "
                    "orlata.", _tl(f, g), f, g, v, compatto=True, box=(-1, 4, -1, 7), nota_sistema=ns,
                    punti=[(sp.Rational(3, 2), 3)], singolari=sing, titolo_curva="2x+y=6", verifica=False))

    # --- ottobre 2024 (es. 1): log x + log y su 3-x^2-y=0 ---
    f = sp.log(x) + sp.log(y); g = 3 - x**2 - y
    ex = [_passo("Dominio di f: servono x>0 e y>0. Sulla parabola y=3-x²>0 richiede x²<3: i punti ammissibili "
                 "sono quelli dell'arco con 0<x<√3, che è un insieme APERTO (agli estremi f→-∞).",
                 r"x>0,\ y=3-x^2>0\iff 0\lt x\lt\sqrt3")]
    v = _v_parabola_y(g, -1, 0, 3, extra=ex)
    ns = [_passo("Risolviamo il sistema: eliminiamo λ con il prodotto incrociato (f_x=1/x, f_y=1/y, g_x=-2x, g_y=-1) e sostituiamo "
                 "y=3-x² dal vincolo:",
                 r"f_xg_y-f_yg_x=-\frac1x+\frac{2x}{y}=0\ \Rightarrow\ -\frac1x+\frac{2x}{3-x^2}=0"
                 r"\iff 3x^2=3\iff x=\pm1"),
          _passo("Solo x=1 è nel dominio di f (x>0); x=-1 si scarta. Dal vincolo y=3-1=2:",
                 r"(x,y)=(1,2)")]
    pa = [_passo_noncompatto(
        "L'arco ammissibile è aperto: restringendo f (y=3-x²) si ottiene h(x)=ln x+ln(3-x²) su 0<x<√3, che "
        "tende a -∞ in entrambi gli estremi.",
        r"h(x)=\ln x+\ln(3-x^2),\qquad \lim_{x\to0^+}h=-\infty,\ \ \lim_{x\to\sqrt3^-}h=-\infty"),
          _passo("Conclusione: l'unico punto stazionario è il massimo assoluto (h→-∞ agli estremi); il minimo "
                 "assoluto NON esiste.",
                 r"\max f=f(1,2)=\ln2,\qquad \min f\ \text{non esiste}")]
    out.append(_lag("ottobre 2024", 1,
                    "Data la funzione f(x,y) = log x + log y soggetta al vincolo g(x,y) = 3-x²-y = 0: "
                    "a) disegnare il vincolo e descriverne le caratteristiche; b) determinare eventuali punti "
                    "di massimo e/o minimo vincolato.", _tl(f, g), f, g, v, compatto=False,
                    box=(-2, 2, -1, 4), nota_sistema=ns, punti=[(1, 2)], passi_assoluti=pa,
                    val_max=sp.log(2), val_min=None, titolo_curva="y=3-x²"))

    # --- gennaio 2025 (es. 10): y sulla lemniscata (x^2+y^2)^2 = 2(x^2-y^2) ---
    f = y; g = (x**2 + y**2)**2 - 2*(x**2 - y**2)
    v = [_passo("Passo 1 — riconosciamo il vincolo g(x,y)=0: in coordinate polari (x=r cosθ, y=r sinθ) "
                "l'equazione diventa r⁴=2r²cos2θ:",
                r"(x^2+y^2)^2=2(x^2-y^2)\iff r^2=2\cos 2\theta"),
         _passo("Caratteristiche della curva: LEMNISCATA di Bernoulli, curva a forma di otto simmetrica "
                "rispetto a entrambi gli assi, con il nodo nell'origine; interseca l'asse x in (±√2,0) e "
                "l'asse y solo in (0,0). Poiché r²≤2 è chiusa e limitata, quindi COMPATTA (come dice il "
                "testo).",
                r"|r|\le\sqrt2,\quad \text{asse }x:\ (\pm\sqrt2,0),\quad \text{nodo }(0,0)")]
    ns = [_passo("Risolviamo il sistema: nella seconda equazione 1=λ·g_y il moltiplicatore non può essere nullo, e nella prima "
                 "0=λ·g_x si ha g_x=4x(x²+y²-1)=0: quindi x=0 oppure x²+y²=1. Esaminiamo i due casi con g=0.",
                 r"g_x=4x(x^2+y^2-1),\quad g_y=4y(x^2+y^2+1)"),
          _passo("Caso 1: x=0. Il vincolo diventa y⁴+2y²=0, cioè y=0: ma in (0,0) si ha ∇g=(0,0) e la "
                 "seconda equazione 1=λ·0 è impossibile: nessuna soluzione del sistema (l'origine è il punto "
                 "singolare, trattato a parte).",
                 r"x=0\ \Rightarrow\ y^4+2y^2=0\iff y=0"),
          _passo("Caso 2: x²+y²=1. Sostituendo x²=1-y² nel vincolo si ottiene un'equazione in y:",
                 r"x^2+y^2=1\ \Rightarrow\ 1-2(1-2y^2)=0\iff 4y^2=1\iff y=\pm\tfrac12,\ \ x=\pm\tfrac{\sqrt3}{2}")]
    pts = [(sp.sqrt(3)/2*sx, sp.Rational(1, 2)*sy) for sx in (1, -1) for sy in (1, -1)]
    sing = [(0, 0, "Il nodo (0,0) è un punto singolare del vincolo (∇g=(0,0)): il metodo di Lagrange non lo "
                   "trova, ma appartiene alla curva e va confrontato valutando f direttamente.")]
    out.append(_lag("gennaio 2025", 10,
                    "Data la funzione f(x,y) = y soggetta al vincolo g(x,y) = (x²+y²)²-2(x²-y²) = 0: "
                    "a) determinare i punti stazionari; b) tenendo conto che il vincolo è chiuso e limitato "
                    "determinare i punti di massimo e di minimo assoluto.", _tl(f, g), f, g, v, compatto=True,
                    box=(-1.7, 1.7, -1.0, 1.0), nota_sistema=ns, punti=pts, singolari=sing,
                    titolo_curva="lemniscata"))

    # --- dicembre 2023 (es. 4) e dicembre 2021 (es. 9): liberi + vincolati sulla circonferenza ---
    for fonte, n, f, sw in (("dicembre 2023", 4, sp.log(1 + x**2) + y**2/4 - x**2/4, False),
                            ("dicembre 2021", 9, sp.log(1 + y**2) + x**2/4 - y**2/4, True)):
        g = x**2 + y**2 - 1
        u, w = (y, x) if sw else (x, y)   # u: variabile nel logaritmo; w: l'altra
        pts_lib = [(0, 0), (sp.sqrt(3), 0), (-sp.sqrt(3), 0)]
        if sw:
            pts_lib = [(0, 0), (0, sp.sqrt(3)), (0, -sp.sqrt(3))]
        fu = sp.diff(f, u); fw = sp.diff(f, w)
        risol = [_passo(f"Dalla derivata in {w} si ottiene {w}=0; dalla derivata in {u}, dopo aver raccolto "
                        f"{u}, il secondo fattore dà {u}²=3 (il fattore 1+{u}² non si annulla mai):",
                        r"f_" + str(u) + "=" + _tex(sp.factor(sp.simplify(fu))) + r"=0\iff "
                        + str(u) + r"=0\ \text{ oppure }\ " + str(u) + r"^2=3;\qquad f_" + str(w) + "="
                        + _tex(sp.simplify(fw)) + "=0\\iff " + str(w) + "=0"),
                 _passo("I punti stazionari liberi sono quindi:",
                        ",\\ ".join(_pt(a, b) for a, b in _ordina(pts_lib)))]
        pre = [_passo("Parte a) — punti stazionari LIBERI di f su tutto il piano e loro natura (teorema "
                      "dell'Hessiana).", None)]
        pp, tipi_lib = _passi_liberi(f, _ordina(pts_lib), risol=risol, num0=1)
        pre.extend(pp)
        pre.append(_passo("Parte b) — massimo e minimo di f sulla circonferenza D: x²+y²=1 con il metodo "
                          "dei moltiplicatori di Lagrange e l'Hessiano orlato.", None))
        tl = r"f(x,y)=" + _tex(f)
        enun = (f"Data la funzione f(x,y) = log(1+{u}²)+{w}²/4-{u}²/4: a) determinare i punti stazionari e "
                "la loro natura; b) determinare il massimo e il minimo di f in D = {(x,y) ∈ R²: x²+y²=1}.")
        out.append(_lag(fonte, n, enun, tl, f, g, _v_circ(g, 0, 0, 1, completa=False), compatto=True,
                        box=(-1.5, 1.5, -1.5, 1.5), titolo_curva="x²+y²=1", prefisso_passi=pre,
                        hint="Parte b): un punto per riga, formato x,y (es: 1,0): punti stazionari sulla "
                             "circonferenza. (I punti liberi della parte a) sono nella soluzione.)"))
    return out

# ---------------------------------------------------------------------------
# LIBERI -- batch D: funzioni polinomiali con famiglie di punti stazionari / Hessiano nullo
# ---------------------------------------------------------------------------

_NOTA_FAM = ("(Per la verifica automatica: classifica i punti stazionari isolati e inoltre i punti "
             "{pts} delle famiglie di punti non isolati.)")


def _nota_fam(reps):
    return _NOTA_FAM.format(pts=", ".join(f"({a},{b})" for a, b, _t in reps))


def _batch_D():
    out = []
    R_ = sp.Rational

    # --- 2 dicembre 2025: x^2 y (2x-3y+6) ---
    f = x**2*y*(2*x - 3*y + 6)
    risol = [
        _passo("Risolviamo il sistema fattorizzando: dalla seconda equazione compaiono due casi (x=0 oppure "
               "x-3y+3=0); sostituiamo ciascuno nella prima.",
               r"f_x=6xy(x-y+2),\quad f_y=2x^2(x-3y+3)"),
        _passo("Caso x=0: entrambe le equazioni sono soddisfatte per OGNI valore di y: tutta la retta x=0 "
               "(asse y) è fatta di punti stazionari (non isolati).",
               r"x=0\ \Rightarrow\ f_x=0,\ f_y=0\ \ \forall y"),
        _passo("Caso x=3y-3: sostituendo nella prima equazione si ottiene un'equazione di terzo grado in y "
               "che si fattorizza:",
               r"6(3y-3)\,y\,(2y-1)=0\iff y=1\ (\text{dà }x=0,\text{ già nella retta}),\ y=0\ (x=-3),\ y=\tfrac12\ (x=-\tfrac32)"),
        _passo("Punti stazionari: la retta x=0 e i due punti isolati (-3,0) e (-3/2,1/2).",
               r"x=0\ (\forall y),\quad (-3,0),\quad \left(-\tfrac32,\tfrac12\right)")]
    post = [
        _passo("Attenzione: sui punti della retta x=0 si ha f_xx=12xy-6y²+12y=6y(2-y), f_xy=0 e f_yy=-6x²=0, "
               "quindi det H=0 (determinante nullo): il test dell'Hessiana non decide e si studia il segno di "
               "f nell'intorno. Poiché f=x²·y(2x-3y+6) e x²≥0, intorno a (0,b) il segno di f è quello di "
               "y(2x-3y+6), che in (0,b) vale 3b(2-b):",
               r"\det H(0,b)=0\ \ \forall b;\qquad \operatorname{sgn}f\ \text{vicino a }(0,b)=\operatorname{sgn}\,3b(2-b)"),
        _passo("Conclusione sulla retta x=0: se 0<b<2 si ha f≥0=f(0,b) (minimo, non stretto); se b<0 oppure "
               "b>2 si ha f≤0=f(0,b) (massimo, non stretto); per b=0 e b=2 il fattore 3b(2-b) cambia segno "
               "attorno al punto: f assume valori di segno opposto, quindi sono selle.",
               r"(0,b):\ \begin{cases}0\lt b\lt2 & \text{minimo}\\ b\lt0\ \vee\ b\gt2 & \text{massimo}\\ b=0,\ b=2 & \text{sella}\end{cases}")]
    reps = [(0, 1, 'minimo'), (0, 3, 'massimo'), (0, 2, 'sella')]
    out.append(_liberi("2 dicembre 2025", 1,
                       "Data la funzione f(x,y) = x²y(2x-3y+6) studiare la natura dei punti stazionari.",
                       f, [(-3, 0), (R_(-3, 2), R_(1, 2))], risol=risol, post=post, box=(-5, 3, -2.5, 4.5),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(0, -2.5, 0, 4.5, "x=0 (punti stazionari)")]))

    # --- 3 dicembre 2025: (y-1)^2 (x^2+y-1) ---
    f = (y - 1)**2*(x**2 + y - 1)
    risol = [
        _passo("Fattorizziamo: f_x=2x(y-1)², f_y=(y-1)(2x²+3y-3). La prima si annulla per x=0 oppure y=1: "
               "se y=1 anche la seconda è nulla per ogni x; se x=0 la seconda diventa 3(y-1)²=0, cioè ancora "
               "y=1.",
               r"y=1:\ f_x=0,\ f_y=0\ \ \forall x;\qquad x=0:\ f_y=3(y-1)^2=0\iff y=1"),
        _passo("L'insieme dei punti stazionari è quindi l'intera retta y=1 (nessun punto isolato).",
               r"\{(x,1):\ x\in\mathbb{R}\}")]
    post = [
        _passo("Attenzione: sulla retta y=1 si ha f_xx=2(y-1)²=0, f_xy=4x(y-1)=0, quindi det H=0 (determinante "
               "nullo): l'Hessiana non decide. Studiamo il segno di f vicino a (a,1), scrivendo y-1=t "
               "(f=t²(x²+t)):",
               r"f(x,1+t)=t^2\,(x^2+t),\qquad \det H(a,1)=0\ \ \forall a"),
        _passo("Se a≠0: per t piccolo x²+t≈a²>0, quindi f≥0=f(a,1) vicino al punto: minimo (non stretto). Se "
               "a=0: f=t²(x²+t) vale t³<0 per t<0, x=0 e vale x²t²>0 per t>0: segni opposti, quindi (0,1) è "
               "una sella.",
               r"a\ne0:\ \text{minimo};\qquad a=0:\ f(0,1+t)=t^3\ \text{cambia segno}\Rightarrow\text{sella}")]
    reps = [(1, 1, 'minimo'), (-2, 1, 'minimo'), (0, 1, 'sella')]
    out.append(_liberi("3 dicembre 2025", 1,
                       "Data la funzione f(x,y) = (y-1)²(x²+y-1) studiare la natura dei punti stazionari.",
                       f, [], risol=risol, post=post, box=(-3, 3, -1.2, 3.2),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-3, 1, 3, 1, "y=1 (punti stazionari)")]))

    # --- 11 aprile 2026 (anche 5 dicembre 2025): x^3 y^2 - x^4 y^2 - x^3 y^3 ---
    f = x**3*y**2 - x**4*y**2 - x**3*y**3
    risol = [
        _passo("Raccogliamo: f=x³y²(1-x-y), da cui f_x=x²y²(3-4x-3y) e f_y=x³y(2-2x-3y). Le due equazioni si "
               "annullano insieme per x=0 (qualunque y) e per y=0 (qualunque x): due rette di punti "
               "stazionari, gli assi coordinati.",
               r"f_x=x^2y^2(3-4x-3y),\quad f_y=x^3y(2-2x-3y)"),
        _passo("Fuori dagli assi (x≠0, y≠0) devono annullarsi le parentesi: sistema lineare 4x+3y=3, "
               "2x+3y=2. Sottraendo: 2x=1.",
               r"\begin{cases}4x+3y=3\\2x+3y=2\end{cases}\Rightarrow x=\tfrac12,\ y=\tfrac13"),
        _passo("Punti stazionari: i due assi e il punto isolato (1/2,1/3).",
               r"x=0\ (\forall y),\quad y=0\ (\forall x),\quad \left(\tfrac12,\tfrac13\right)")]
    post = [
        _passo("Attenzione: sugli assi l'Hessiana ha determinante nullo (sull'asse x: f_xx=f_xy=0; "
               "sull'asse y tutte le derivate seconde sono nulle), quindi il test non decide: si studia il "
               "segno di f=x³y²(1-x-y). Sull'asse x vicino a (a,0) si ha y²≥0 e il segno è quello di a³(1-a).",
               r"y=0,\ x=a:\ \operatorname{sgn}f=\operatorname{sgn}\,a^3(1-a)\ \Rightarrow\ "
               r"\begin{cases}0\lt a\lt1 & \text{minimo}\\ a\lt0\ \vee\ a\gt1 & \text{massimo}\\ a=0,\ 1 & \text{sella}\end{cases}"),
        _passo("Sull'asse y vicino a (0,b): il fattore x³ cambia segno con x e il resto vale b²(1-b)≠0 per "
               "b≠0,1: f assume segni opposti, quindi sella. Anche per b=0 (f≈x³y²) e per b=1 (f≈-x³(x+y-1) "
               "assume entrambi i segni) si hanno selle.",
               r"(0,b):\ f\approx x^3\,b^2(1-b)\ \text{cambia segno}\ \Rightarrow\ \text{sella}\ \ \forall b")]
    reps = [(R_(1, 2), 0, 'minimo'), (-1, 0, 'massimo'), (2, 0, 'massimo'), (1, 0, 'sella'),
            (0, 2, 'sella'), (0, 0, 'sella')]
    out.append(_liberi("11 aprile 2026", 1,
                       "Data la funzione f(x,y) = x³y²-x⁴y²-x³y³ studiare la natura dei punti stazionari.",
                       f, [(R_(1, 2), R_(1, 3))], risol=risol, post=post, box=(-1.5, 2, -1.5, 2),
                       extra_attesi=[[float(a), float(b), t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-1.5, 0, 2, 0, "y=0"), (0, -1.5, 0, 2, "x=0")]))

    # --- 5 dicembre 2025: 4y^2 - 4x^2 y^2 - y^4 ---
    f = 4*y**2 - 4*x**2*y**2 - y**4
    risol = [
        _passo("Fattorizziamo: f_x=-8xy², f_y=4y(2-2x²-y²). Dalla prima: x=0 oppure y=0. Se y=0 anche la "
               "seconda si annulla per ogni x: tutto l'asse x. Se x=0 la seconda dà 4y(2-y²)=0.",
               r"y=0:\ f_x=f_y=0\ \forall x;\qquad x=0:\ 4y(2-y^2)=0\iff y=0,\ \pm\sqrt2"),
        _passo("Punti stazionari: l'asse x (famiglia) e i due punti isolati (0,±√2).",
               r"\{(a,0)\},\quad (0,\sqrt2),\quad (0,-\sqrt2)")]
    post = [
        _passo("Attenzione: sull'asse x si ha f_xx=-8y²=0, f_xy=-16xy=0: det H=0 (determinante nullo), il "
               "test non decide. Poiché f=y²(4-4x²-y²), vicino a (a,0) il segno di f è quello di 4(1-a²).",
               r"f=y^2(4-4x^2-y^2),\qquad \operatorname{sgn}f\ \text{vicino a }(a,0)=\operatorname{sgn}(1-a^2)"),
        _passo("Se |a|<1: f≥0=f(a,0), minimo (non stretto); se |a|>1: f≤0, massimo (non stretto); se "
               "a=±1 il fattore 4-4x²-y² cambia segno attorno al punto: sella.",
               r"|a|\lt1:\ \text{minimo};\quad |a|\gt1:\ \text{massimo};\quad a=\pm1:\ \text{sella}")]
    reps = [(0, 0, 'minimo'), (2, 0, 'massimo'), (1, 0, 'sella')]
    out.append(_liberi("5 dicembre 2025", 1,
                       "Data la funzione f(x,y) = 4y²-4x²y²-y⁴, studiare la natura dei punti stazionari.",
                       f, [(0, sp.sqrt(2)), (0, -sp.sqrt(2))], risol=risol, post=post, box=(-2.5, 2.5, -2.2, 2.2),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-2.5, 0, 2.5, 0, "y=0 (punti stazionari)")]))

    # --- 13 dicembre 2025: y^2 (x^2+5) + y^4 - 2 x y^3 ---
    f = y**2*(x**2 + 5) + y**4 - 2*x*y**3
    risol = [
        _passo("Prima di derivare notiamo una riscrittura utile: raccogliendo y² compare un quadrato "
               "perfetto,",
               r"f=y^2\left(x^2-2xy+y^2+5\right)=y^2\left[(x-y)^2+5\right]"),
        _passo("Gradiente: f_x=2xy²-2y³=2y²(x-y), f_y=2y(x²+5)+4y³-6xy²=2y(x²-3xy+2y²+5). La prima dà y=0 "
               "oppure x=y; se x=y la seconda diventa 2y(y²-3y²+2y²+5)=10y=0, cioè y=0. Quindi y=0 e la "
               "seconda si annulla: tutto l'asse x.",
               r"y=0:\ f_x=f_y=0\ \forall x;\qquad x=y:\ f_y=10y=0\Rightarrow y=0"),
        _passo("Punti stazionari: tutti e soli i punti (a,0) dell'asse x (nessun punto isolato).",
               r"\{(a,0):\ a\in\mathbb{R}\}")]
    post = [
        _passo("Attenzione: su y=0 si ha f_xx=2y²=0 e f_xy=4xy-6y²=0, quindi det H=0 (determinante nullo): "
               "il test non decide. Ma dalla riscrittura f=y²[(x-y)²+5] è evidente che f≥0 ovunque e "
               "f=0 esattamente per y=0.",
               r"f=y^2\left[(x-y)^2+5\right]\ge0,\qquad f=0\iff y=0"),
        _passo("Conclusione: ogni punto (a,0) è un punto di minimo assoluto (non stretto), con f=0.",
               r"(a,0):\ f(a,0)=0=\min f\ \ \forall a\in\mathbb{R}\ \Rightarrow\ \text{minimo}")]
    reps = [(0, 0, 'minimo'), (2, 0, 'minimo'), (-3, 0, 'minimo')]
    out.append(_liberi("13 dicembre 2025", 1,
                       "Data la funzione f(x,y) = y²(x²+5)+y⁴-2xy³, studiare la natura dei punti stazionari.",
                       f, [], risol=risol, post=post, box=(-3, 3, -2, 2),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-3, 0, 3, 0, "y=0 (minimi)")]))

    # --- 24 gennaio 2026: y^2 (x^6 - 2y^2 + y^4) ---
    f = y**2*(x**6 - 2*y**2 + y**4)
    risol = [
        _passo("Sviluppiamo f=x⁶y²-2y⁴+y⁶ e deriviamo: f_x=6x⁵y², f_y=2y(x⁶-4y²+3y⁴). La prima dà x=0 "
               "oppure y=0. Se y=0 la seconda si annulla per ogni x (tutto l'asse x). Se x=0 la seconda è "
               "2y³(3y²-4)=0: y=0 oppure y²=4/3.",
               r"f_x=6x^5y^2,\quad f_y=2y\,(x^6-4y^2+3y^4);\qquad x=0:\ 2y^3(3y^2-4)=0\iff y=0,\ \pm\tfrac{2}{\sqrt3}"),
        _passo("Punti stazionari: l'asse x (famiglia) e i due punti isolati (0,±2/√3).",
               r"\{(a,0)\},\quad \left(0,\tfrac{2}{\sqrt3}\right),\quad \left(0,-\tfrac{2}{\sqrt3}\right)")]
    post = [
        _passo("Attenzione: nei punti (0,±2/√3) si ha f_xx=30x⁴y²=0 e f_xy=12x⁵y=0, quindi det H=0 "
               "(determinante nullo) anche se f_yy>0: il test non decide. Scriviamo f=x⁶y²+g(y) con "
               "g(y)=y⁶-2y⁴: il primo addendo è ≥0, mentre g ha in y=±2/√3 un minimo (g'=2y³(3y²-4), "
               "g''=-24y²+30y⁴, che in y²=4/3 vale 64/3>0).",
               r"f(x,y)=x^6y^2+g(y)\ge g(y)\ge g\!\left(\tfrac{2}{\sqrt3}\right),\qquad g''\!\left(\tfrac{2}{\sqrt3}\right)=-32+\tfrac{160}{3}=\tfrac{64}{3}\gt0"),
        _passo("Quindi f(x,y)≥f(0,±2/√3) con uguaglianza solo nel punto: sono minimi (stretti). "
               "Sull'asse x vicino a (a,0): f=y²(a⁶-2y²+y⁴)≥0 se a≠0, minimo (non stretto); in (0,0) "
               "f(x,x²)=x⁸(x²-2+x⁴)<0 e f(x,x⁴)=x¹⁴(1-2x²+x¹⁰)>0 per x piccolo: segni opposti, sella.",
               r"(a,0),\ a\ne0:\ \text{minimo};\qquad (0,0):\ f(x,x^2)\lt0,\ f(x,x^4)\gt0\ \Rightarrow\ \text{sella}")]
    reps = [(1, 0, 'minimo'), (0, 0, 'sella')]
    out.append(_liberi("24 gennaio 2026", 1,
                       "Data la funzione f(x,y) = y²(x⁶-2y²+y⁴) studiare la natura dei punti stazionari.",
                       f, [(0, 2/sp.sqrt(3)), (0, -2/sp.sqrt(3))], risol=risol, post=post,
                       box=(-1.6, 1.6, -1.8, 1.8),
                       override={(0, 2/sp.sqrt(3)): ('minimo', None), (0, -2/sp.sqrt(3)): ('minimo', None)},
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-1.6, 0, 1.6, 0, "y=0 (punti stazionari)")]))

    # --- 20 gennaio 2026: x/y + y/x ---
    f = x/y + y/x
    pre = [_passo("Dominio: i due denominatori devono essere non nulli, quindi x≠0 e y≠0: il dominio è il "
                  "piano privato dei due assi (quattro quadranti aperti).",
                  r"D=\{(x,y)\in\mathbb{R}^2:\ x\ne0,\ y\ne0\}")]
    risol = [
        _passo("Derivate: f_x=1/y-y/x²=(x²-y²)/(x²y), f_y=-x/y²+1/x=(y²-x²)/(xy²). Entrambe si annullano "
               "se e solo se x²=y², cioè y=x oppure y=-x (con x≠0).",
               r"f_x=\frac{x^2-y^2}{x^2y},\quad f_y=\frac{y^2-x^2}{xy^2}\ \Rightarrow\ y=\pm x"),
        _passo("I punti stazionari sono le due bisettrici, origine esclusa (famiglie non isolate).",
               r"\{(a,a):a\ne0\}\ \cup\ \{(a,-a):a\ne0\}")]
    post = [
        _passo("Attenzione: sulle bisettrici si ha det H=0 (determinante nullo): ad esempio in (a,a) "
               "f_xx=f_yy=2/a² e f_xy=-2/a², quindi f_xx f_yy-f_xy²=0. Il test non decide: poniamo t=x/y, "
               "così f=t+1/t, funzione di sola t.",
               r"H(a,a)=\frac{2}{a^2}\begin{pmatrix}1&-1\\-1&1\end{pmatrix},\ \det H=0;\qquad f=t+\frac1t,\ t=\frac xy"),
        _passo("Per t>0 vale t+1/t≥2 con uguaglianza per t=1 (cioè y=x): su y=x la funzione ha un minimo "
               "(non stretto, f=2). Per t<0 vale t+1/t≤-2 con uguaglianza per t=-1 (y=-x): su y=-x massimo "
               "(non stretto, f=-2).",
               r"y=x:\ f=2=\min\ (t\gt0);\qquad y=-x:\ f=-2=\max\ (t\lt0)")]
    reps = [(1, 1, 'minimo'), (-2, -2, 'minimo'), (1, -1, 'massimo'), (3, -3, 'massimo')]
    out.append(_liberi("20 gennaio 2026", 1,
                       "Data la funzione f(x,y) = x/y + y/x studiare la natura dei punti stazionari.",
                       f, [], pre=pre, risol=risol, post=post, box=(-4, 4, -4, 4),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-4, -4, 4, 4, "y=x (minimi)"), (-4, 4, 4, -4, "y=-x (massimi)")],
                       levels=[-8, -6, -4, -3, -2.5, -2, 2, 2.5, 3, 4, 6, 8]))

    # --- 19 gennaio 2026: xy - x^4 - y^4 ---
    f = x*y - x**4 - y**4
    risol = [
        _passo("Gradiente: f_x=y-4x³, f_y=x-4y³. Dalla prima y=4x³; sostituendo nella seconda: "
               "x-4(4x³)³=x(1-256x⁸)=0.",
               r"y=4x^3\ \Rightarrow\ x-256x^9=x(1-256x^8)=0\iff x=0\ \text{ oppure }\ x=\pm\tfrac12"),
        _passo("Da y=4x³ si ricavano le ordinate: x=0→y=0; x=1/2→y=1/2; x=-1/2→y=-1/2.",
               r"(0,0),\quad \left(\tfrac12,\tfrac12\right),\quad \left(-\tfrac12,-\tfrac12\right)")]
    out.append(_liberi("19 gennaio 2026", 1,
                       "Data la funzione f(x,y) = xy-x⁴-y⁴ studiare la natura dei punti stazionari.",
                       f, [(0, 0), (R_(1, 2), R_(1, 2)), (R_(-1, 2), R_(-1, 2))], risol=risol, box=(-1.2, 1.2, -1.2, 1.2)))

    # --- 21 gennaio 2026 (anche gennaio 2025, es. 1): e^{x-y}(x^2-2y^2) ---
    f = sp.exp(x - y)*(x**2 - 2*y**2)
    risol = [
        _passo("Gradiente (esponenziale sempre >0, si semplifica): "
               "f_x=e^(x-y)(x²-2y²+2x), f_y=e^(x-y)(-x²+2y²-4y). Sommando le due equazioni (uguali a zero) "
               "si ottiene 2x-4y=0.",
               r"\begin{cases}x^2-2y^2+2x=0\\-x^2+2y^2-4y=0\end{cases}\ \Rightarrow\ 2x-4y=0\iff x=2y"),
        _passo("Sostituendo x=2y nella prima equazione: 4y²-2y²+4y=2y(y+2)=0.",
               r"2y^2+4y=0\iff y=0\ (x=0)\ \text{ oppure }\ y=-2\ (x=-4)"),
        _passo("Punti stazionari: (0,0) e (-4,-2).", r"(0,0),\quad (-4,-2)")]
    out.append(_liberi("21 gennaio 2026", 1,
                       "Data la funzione f(x,y) = e^(x-y)(x²-2y²) studiare la natura dei punti stazionari.",
                       f, [(0, 0), (-4, -2)], risol=risol, box=(-8, 3, -5, 3)))
    return out

# ---------------------------------------------------------------------------
# LIBERI -- batch E: esponenziali/logaritmi, studio del segno e del dominio, piano tangente, assoluti
# ---------------------------------------------------------------------------

def _batch_E():
    out = []
    R_ = sp.Rational

    # --- 2 aprile 2026: (y-1)^2 + x e^{x+1} (y-1) ---
    f = (y - 1)**2 + x*sp.exp(x + 1)*(y - 1)
    risol = [
        _passo("Derivate (e^(x+1)>0 non si annulla mai): f_x=(1+x)e^(x+1)(y-1), f_y=2(y-1)+x e^(x+1). "
               "La prima si annulla se x=-1 oppure y=1.",
               r"f_x=(1+x)e^{x+1}(y-1)=0\iff x=-1\ \text{ oppure }\ y=1"),
        _passo("Caso x=-1: la seconda diventa 2(y-1)-1=0, cioè y=3/2. Caso y=1: la seconda diventa "
               "x e^(x+1)=0, cioè x=0.",
               r"x=-1:\ 2(y-1)-1=0\Rightarrow y=\tfrac32;\qquad y=1:\ xe^{x+1}=0\Rightarrow x=0"),
        _passo("Punti stazionari:", r"\left(-1,\tfrac32\right),\quad (0,1)")]
    out.append(_liberi("2 aprile 2026", 1,
                       "Data la funzione f(x,y) = (y-1)² + x·e^(x+1)·(y-1), studiare la natura dei punti "
                       "stazionari.", f, [(-1, R_(3, 2)), (0, 1)], risol=risol, box=(-3.5, 2, -0.5, 3)))

    # --- 8 aprile 2026: (y+3)(1+x)^2 - 4(y+3) + piano tangente in (0,0) ---
    f = (y + 3)*(1 + x)**2 - 4*(y + 3)
    risol = [
        _passo("Raccogliamo (y+3): f=(y+3)[(1+x)²-4]=(y+3)(x+3)(x-1). Derivate: f_x=2(y+3)(1+x), "
               "f_y=(1+x)²-4=(x+3)(x-1).",
               r"f_x=2(y+3)(1+x),\quad f_y=(x+3)(x-1)"),
        _passo("Dalla seconda: x=1 oppure x=-3. In entrambi i casi 1+x≠0, quindi la prima richiede y=-3.",
               r"x=1\ \text{ o }\ x=-3,\quad 1+x\ne0\ \Rightarrow\ y+3=0\iff y=-3"),
        _passo("Punti stazionari:", r"(1,-3),\quad (-3,-3)")]
    f00 = f.subs({x: 0, y: 0}); fx00 = sp.diff(f, x).subs({x: 0, y: 0}); fy00 = sp.diff(f, y).subs({x: 0, y: 0})
    post = [
        _passo("Piano tangente in (0,0): f è un polinomio, quindi differenziabile ovunque e il piano "
               "tangente esiste; serve f e le derivate parziali prime nel punto (formulario ufficiale): "
               "z=f(x0,y0)+f_x(x0,y0)(x-x0)+f_y(x0,y0)(y-y0).",
               r"f(0,0)=" + _tex(f00) + r",\ f_x(0,0)=" + _tex(fx00) + r",\ f_y(0,0)=" + _tex(fy00)),
        _passo("Sostituendo:", r"z=" + _tex(sp.expand(f00 + fx00*x + fy00*y)))]
    out.append(_liberi("8 aprile 2026", 1,
                       "Data la funzione f(x,y) = (y+3)(1+x)² - 4(y+3) studiare la natura dei punti "
                       "stazionari. Determinare, se esiste, l'equazione del piano tangente alla funzione nel "
                       "punto (0,0).", f, [(1, -3), (-3, -3)], risol=risol, post=post, box=(-6, 4, -7, 1)))

    # --- 9 aprile 2026 (anche luglio 2024, es. 3): x^3/8 (1/3 + x y^2) - 2y^2 + piano tangente in (-2,0) ---
    f = x**3/8*(R_(1, 3) + x*y**2) - 2*y**2
    risol = [
        _passo("Sviluppiamo f=x³/24+x⁴y²/8-2y² e deriviamo: f_x=x²(1+4xy²)/8, f_y=y(x⁴-16)/4. La seconda "
               "si annulla per y=0 oppure x=±2; la prima per x=0 oppure 4xy²=-1.",
               r"f_x=\frac{x^2(1+4xy^2)}{8},\quad f_y=\frac{y(x^4-16)}{4}"),
        _passo("Se x=0, la seconda dà y=0: punto (0,0). Se 4xy²=-1 allora y≠0, quindi x⁴=16: x=2 darebbe "
               "y²=-1/8 (impossibile), x=-2 dà y²=1/8, cioè y=±√2/4.",
               r"x=0\Rightarrow y=0;\qquad x=-2:\ y^2=\tfrac18\Rightarrow y=\pm\tfrac{\sqrt2}{4};\qquad x=2:\ y^2=-\tfrac18\ \text{(no)}"),
        _passo("Punti stazionari:",
               r"(0,0),\quad \left(-2,\tfrac{\sqrt2}{4}\right),\quad \left(-2,-\tfrac{\sqrt2}{4}\right)")]
    ov = {(0, 0): ('sella', [_passo(
        "Attenzione: in (0,0) si ha f_xx=f_xy=0 e f_yy=-4, quindi det H=0 (determinante nullo): il test "
        "non decide. Studiamo f direttamente: lungo l'asse x (y=0) si ha f=x³/24, che cambia segno con x, "
        "quindi f assume valori positivi e negativi vicino a (0,0): è una sella.",
        r"f(x,0)=\frac{x^3}{24}\gtrless0\ \text{per }x\gtrless0\ \Rightarrow\ \text{sella}")])}
    fm20 = f.subs({x: -2, y: 0}); fxm20 = sp.diff(f, x).subs({x: -2, y: 0}); fym20 = sp.diff(f, y).subs({x: -2, y: 0})
    post = [
        _passo("Piano tangente in (-2,0): f è un polinomio (differenziabile), quindi il piano esiste. "
               "Valori nel punto:",
               r"f(-2,0)=" + _tex(fm20) + r",\ f_x(-2,0)=" + _tex(fxm20) + r",\ f_y(-2,0)=" + _tex(fym20)),
        _passo("Piano tangente: z=f+f_x(x+2)+f_y·y:", r"z=" + _tex(sp.expand(fm20 + fxm20*(x + 2) + fym20*y)))]
    out.append(_liberi("9 aprile 2026", 1,
                       "Data la funzione f(x,y) = (x³/8)(1/3 + xy²) - 2y² studiare la natura dei punti "
                       "stazionari. Determinare, se esiste, l'equazione del piano tangente alla funzione nel "
                       "punto (-2,0).", f, [(0, 0), (-2, sp.sqrt(2)/4), (-2, -sp.sqrt(2)/4)], risol=risol,
                       override=ov, post=post, box=(-3.5, 2, -1.5, 1.5)))

    # --- 21 ottobre 2025: x^2 (y-2) (segno, max/min, continuita', piano tangente in (1,-2)) ---
    f = x**2*(y - 2)
    pre = [_passo("Passo a) — segno: x²≥0, quindi il segno di f è quello del fattore (y-2) (tranne dove "
                  "x=0). Studiamo il segno e lo rappresentiamo nel piano (zone colorate nella figura):",
                  r"f\gt0\iff y\gt2\ (x\ne0),\quad f\lt0\iff y\lt2\ (x\ne0),\quad f=0\iff x=0\ \text{ o }\ y=2")]
    risol = [
        _passo("Passo b) — derivate: f_x=2x(y-2), f_y=x². La seconda si annulla solo per x=0, e allora anche "
               "la prima è nulla per ogni y: i punti stazionari formano tutta la retta x=0.",
               r"f_y=x^2=0\iff x=0\ \Rightarrow\ f_x=0\ \ \forall y\qquad(\text{asse }y)")]
    fx_, fy_ = sp.diff(f, x), sp.diff(f, y)
    f1m2 = f.subs({x: 1, y: -2}); fx1 = fx_.subs({x: 1, y: -2}); fy1 = fy_.subs({x: 1, y: -2})
    post = [
        _passo("Attenzione: sulla retta x=0 si ha f_xx=2(y-2), f_xy=2x=0, f_yy=0, quindi det H=2(y-2)·0-0²=0 "
               "(determinante nullo): il test non decide. Dallo studio del segno: vicino a (0,b) il segno di "
               "f è quello di (b-2) perché x²≥0.",
               r"\det H(0,b)=2(b-2)\cdot0-0^2=0;\qquad \operatorname{sgn}f\ \text{vicino a }(0,b)=\operatorname{sgn}(b-2)"),
        _passo("Se b<2: f≤0=f(0,b), massimo (non stretto); se b>2: f≥0, minimo (non stretto); se b=2 il "
               "fattore (y-2) cambia segno attorno al punto: sella.",
               r"(0,b):\ b\lt2\Rightarrow\text{massimo};\quad b\gt2\Rightarrow\text{minimo};\quad b=2\Rightarrow\text{sella}"),
        _passo("Passo c) — continuità e differenziabilità: f è un polinomio, quindi di classe C^∞ su tutto R² "
               "(le derivate parziali prime f_x, f_y sono continue): è continua e differenziabile "
               "ovunque.",
               r"f\in\mathcal{C}^{\infty}(\mathbb{R}^2)\ \Rightarrow\ \text{continua e differenziabile in }\mathbb{R}^2"),
        _passo("Passo d) — piano tangente in (1,-2): valori di f e delle derivate parziali nel punto:",
               r"f(1,-2)=" + _tex(f1m2) + r",\ f_x(1,-2)=" + _tex(fx1) + r",\ f_y(1,-2)=" + _tex(fy1)),
        _passo("Piano tangente z=f(x0,y0)+f_x(x0,y0)(x-x0)+f_y(x0,y0)(y-y0):",
               r"z=" + _tex(sp.expand(f1m2 + fx1*(x - 1) + fy1*(y + 2))))]
    reps = [(0, 0, 'massimo'), (0, 3, 'minimo'), (0, 2, 'sella')]
    out.append(_liberi("21 ottobre 2025", 1,
                       "Data la funzione f(x,y) = x²(y-2): a) studiare e rappresentare graficamente il segno "
                       "della funzione; b) determinare gli eventuali punti di massimo e di minimo "
                       "utilizzando la matrice Hessiana; c) studiare continuità e differenziabilità; d) "
                       "determinare, se esiste, il piano tangente in (1,-2).",
                       f, [], pre=pre, risol=risol, post=post, box=(-3, 3, -2, 5), segno=True,
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-3, 2, 3, 2, "y=2"), (0, -2, 0, 5, "x=0 (punti stazionari)")]))

    # --- 25 ottobre 2025: (x^2+xy) e^{y-x} ---
    f = (x**2 + x*y)*sp.exp(y - x)
    risol = [
        _passo("Derivate (e^(y-x)>0): f_x=e^(y-x)(2x+y-x²-xy), f_y=e^(y-x)·x(1+x+y). La seconda si annulla "
               "per x=0 oppure y=-1-x.",
               r"f_x=e^{y-x}(2x+y-x^2-xy),\quad f_y=e^{y-x}\,x\,(1+x+y)"),
        _passo("Caso x=0: la prima diventa y e^y=0, cioè y=0. Caso y=-1-x: la prima diventa "
               "2x-1-x-x²+x+x²=2x-1, quindi x=1/2 e y=-3/2.",
               r"x=0:\ ye^{y}=0\Rightarrow y=0;\qquad y=-1-x:\ 2x-1=0\Rightarrow x=\tfrac12,\ y=-\tfrac32"),
        _passo("Punti stazionari:", r"(0,0),\quad \left(\tfrac12,-\tfrac32\right)")]
    out.append(_liberi("25 ottobre 2025", 1,
                       "Data la funzione f(x,y) = (x²+xy)·e^(y-x), determinare gli eventuali punti di massimo "
                       "e di minimo utilizzando la matrice Hessiana.", f, [(0, 0), (R_(1, 2), R_(-3, 2))],
                       risol=risol, box=(-2.5, 3, -4, 2)))

    # --- 6 maggio 2025: (x^2+xy+2y^2) e^{x+y} ---
    f = (x**2 + x*y + 2*y**2)*sp.exp(x + y)
    risol = [
        _passo("Derivate (e^(x+y)>0 si può semplificare): "
               "f_x=e^(x+y)(x²+xy+2y²+2x+y), f_y=e^(x+y)(x²+xy+2y²+x+4y). Sottraendo le due equazioni "
               "(uguali a zero) si elimina il termine comune:",
               r"(2x+y)-(x+4y)=x-3y=0\iff x=3y"),
        _passo("Sostituendo x=3y nella seconda equazione: 9y²+3y²+2y²+3y+4y=14y²+7y=7y(2y+1)=0.",
               r"7y(2y+1)=0\iff y=0\ (x=0)\ \text{ oppure }\ y=-\tfrac12\ (x=-\tfrac32)"),
        _passo("Punti stazionari:", r"(0,0),\quad \left(-\tfrac32,-\tfrac12\right)")]
    out.append(_liberi("6 maggio 2025", 1,
                       "Data la funzione f(x,y) = (x²+xy+2y²)·e^(x+y) studiarne la natura dei punti "
                       "stazionari.", f, [(0, 0), (R_(-3, 2), R_(-1, 2))], risol=risol, box=(-4, 2, -3, 2)))

    # --- settembre 2021 (es. 4): (x^2+xy+2y^2) e^x ---
    f = (x**2 + x*y + 2*y**2)*sp.exp(x)
    risol = [
        _passo("Derivate (e^x>0): f_x=e^x(x²+xy+2y²+2x+y), f_y=e^x(x+4y). La seconda dà x=-4y.",
               r"f_y=e^x(x+4y)=0\iff x=-4y"),
        _passo("Sostituendo nella prima: 16y²-4y²+2y²-8y+y=14y²-7y=7y(2y-1)=0.",
               r"7y(2y-1)=0\iff y=0\ (x=0)\ \text{ oppure }\ y=\tfrac12\ (x=-2)"),
        _passo("Punti stazionari:", r"(0,0),\quad \left(-2,\tfrac12\right)")]
    out.append(_liberi("settembre 2021", 4,
                       "Data la seguente funzione reale di due variabili reali f(x,y) = (x²+xy+2y²)·e^x "
                       "determinare eventuali massimi e minimi.", f, [(0, 0), (-2, R_(1, 2))], risol=risol,
                       box=(-6, 3, -3, 3)))

    # --- ottobre 2023 (es. 2): e^{xy^2-2x^2+4y} ---
    f = sp.exp(x*y**2 - 2*x**2 + 4*y)
    risol = [
        _passo("L'esponenziale è sempre positivo: ∇f=e^h·∇h con h=xy²-2x²+4y, quindi ∇f=0 equivale a "
               "h_x=h_y=0.",
               r"h_x=y^2-4x=0,\qquad h_y=2xy+4=0"),
        _passo("Dalla prima x=y²/4; sostituendo nella seconda: y³/2+4=0, cioè y³=-8 e y=-2 (x=1).",
               r"x=\frac{y^2}{4}\ \Rightarrow\ \frac{y^3}{2}+4=0\iff y=-2,\ x=1"),
        _passo("Unico punto stazionario:", r"(1,-2)")]
    out.append(_liberi("ottobre 2023", 2,
                       "Data la funzione f(x,y) = e^(xy²-2x²+4y) determinare la natura dei punti stazionari.",
                       f, [(1, -2)], risol=risol, box=(-1, 3, -4, 0)))

    # --- ottobre 2024 (es. 7): x e^{-(x^2+y^2)} ---
    f = x*sp.exp(-(x**2 + y**2))
    risol = [
        _passo("Derivate (l'esponenziale è sempre positivo): f_x=(1-2x²)e^(-x²-y²), f_y=-2xy e^(-x²-y²). "
               "La seconda dà x=0 oppure y=0. Se x=0 la prima vale 1≠0: impossibile. Se y=0 la prima dà "
               "1-2x²=0.",
               r"y=0:\ 1-2x^2=0\iff x=\pm\tfrac{1}{\sqrt2}=\pm\tfrac{\sqrt2}{2}"),
        _passo("Punti stazionari:", r"\left(\tfrac{\sqrt2}{2},0\right),\quad \left(-\tfrac{\sqrt2}{2},0\right)")]
    out.append(_liberi("ottobre 2024", 7,
                       "Data la seguente funzione reale di due variabili reali f(x,y) = x·e^(-(x²+y²)) "
                       "determinare eventuali punti di massimo e/o minimo.",
                       f, [(sp.sqrt(2)/2, 0), (-sp.sqrt(2)/2, 0)], risol=risol, box=(-2.5, 2.5, -2, 2)))

    # --- ottobre 2024 (es. 13): -2xy^2 + y^3 - y^2 x^2 ---
    f = -2*x*y**2 + y**3 - y**2*x**2
    risol = [
        _passo("Raccogliamo y²: f=y²(y-x²-2x). Derivate: f_x=-2y²(1+x), f_y=y(3y-4x-2x²). La prima dà y=0 "
               "oppure x=-1. Se y=0 la seconda si annulla per ogni x (tutto l'asse x). Se x=-1 la seconda "
               "diventa y(3y+2)=0: y=0 (già sull'asse) oppure y=-2/3.",
               r"f_x=-2y^2(1+x),\quad f_y=y(3y-4x-2x^2);\qquad x=-1:\ y(3y+2)=0"),
        _passo("Punti stazionari: l'asse x (famiglia) e il punto isolato (-1,-2/3).",
               r"\{(a,0)\},\quad \left(-1,-\tfrac23\right)")]
    post = [
        _passo("Attenzione: su y=0 si ha f_xx=-2y²=0 e f_xy=-4y(1+x)=0, quindi det H=0 (determinante "
               "nullo): il test non decide. Poiché f=y²(y-x²-2x) e y²≥0, vicino a (a,0) il segno di f è "
               "quello di -a(a+2).",
               r"\operatorname{sgn}f\ \text{vicino a }(a,0)=\operatorname{sgn}\bigl(-a(a+2)\bigr)"),
        _passo("Se -2<a<0: f≥0=f(a,0), minimo (non stretto); se a<-2 oppure a>0: f≤0, massimo (non stretto); "
               "se a=0 o a=-2 il fattore cambia segno: sella.",
               r"-2\lt a\lt0:\ \text{minimo};\quad a\lt-2\ \vee\ a\gt0:\ \text{massimo};\quad a=0,-2:\ \text{sella}")]
    reps = [(-1, 0, 'minimo'), (1, 0, 'massimo'), (0, 0, 'sella'), (-3, 0, 'massimo')]
    out.append(_liberi("ottobre 2024", 13,
                       "Data la seguente funzione reale di due variabili reali f(x,y) = -2xy²+y³-y²x² "
                       "determinare eventuali punti di massimo e/o minimo.",
                       f, [(-1, R_(-2, 3))], risol=risol, post=post, box=(-4, 2.5, -2, 1.5),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-4, 0, 2.5, 0, "y=0 (punti stazionari)")]))

    # --- ottobre 2024 (es. 16): e^{-y}(y+1)(x^2+x-2) ---
    f = sp.exp(-y)*(y + 1)*(x**2 + x - 2)
    risol = [
        _passo("Derivate (e^(-y)>0), ricordando che d/dy[(y+1)e^(-y)]=-y e^(-y): "
               "f_x=e^(-y)(y+1)(2x+1), f_y=-y e^(-y)(x²+x-2)=-y e^(-y)(x+2)(x-1).",
               r"f_x=e^{-y}(y+1)(2x+1),\qquad f_y=-y\,e^{-y}(x+2)(x-1)"),
        _passo("Dalla prima: y=-1 oppure x=-1/2. Se y=-1 la seconda richiede x=-2 oppure x=1. Se x=-1/2 il "
               "fattore (x+2)(x-1)=-9/4≠0, quindi serve y=0.",
               r"y=-1:\ x=-2\ \text{ o }\ x=1;\qquad x=-\tfrac12:\ y=0"),
        _passo("Punti stazionari:", r"(-2,-1),\quad (1,-1),\quad \left(-\tfrac12,0\right)")]
    out.append(_liberi("ottobre 2024", 16,
                       "Data la seguente funzione reale di due variabili reali f(x,y) = e^(-y)(y+1)(x²+x-2) "
                       "determinare eventuali punti di massimo e/o minimo.",
                       f, [(-2, -1), (1, -1), (R_(-1, 2), 0)], risol=risol, box=(-4, 3, -3, 3)))

    # --- gennaio 2025 (es. 7): log(x^4/4 + y^2 + 4x^2 + 4) ---
    f = sp.log(x**4/4 + y**2 + 4*x**2 + 4)
    pre = [_passo("Dominio: l'argomento del logaritmo x⁴/4+y²+4x²+4 è sempre ≥4>0, quindi f è definita (e "
                  "derivabile) su tutto R².",
                  r"\frac{x^4}{4}+y^2+4x^2+4\ge4\gt0\ \ \forall(x,y)\in\mathbb{R}^2")]
    risol = [
        _passo("Derivate: f_x=(x³+8x)/A, f_y=2y/A, con A=x⁴/4+y²+4x²+4>0. La seconda dà y=0; la prima "
               "x(x²+8)=0 dà x=0 (x²+8>0 sempre).",
               r"f_x=\frac{x(x^2+8)}{A},\ f_y=\frac{2y}{A}\ \Rightarrow\ y=0,\ x=0"),
        _passo("Unico punto stazionario:", r"(0,0)")]
    post = [_passo("Osservazione: A≥4 con uguaglianza solo in (0,0) e log è crescente, quindi (0,0) è anche "
                   "minimo assoluto: f≥ln4.",
                   r"f(x,y)\ge\ln 4=f(0,0)")]
    out.append(_liberi("gennaio 2025", 7,
                       "Data la funzione f(x,y) = log(x⁴/4 + y² + 4x² + 4) determinare gli eventuali punti "
                       "di massimo e di minimo utilizzando la matrice Hessiana.", f, [(0, 0)], pre=pre,
                       risol=risol, post=post, box=(-3, 3, -3, 3)))
    return out

# ---------------------------------------------------------------------------
# LIBERI -- batch F: domini con logaritmi/frazioni, studio del segno, assoluti su un compatto
# ---------------------------------------------------------------------------

def _batch_F():
    out = []
    R_ = sp.Rational

    # --- 22 luglio 2025: 2(x^2+y^2)y - 24y + 2x^2 e assoluti sull'arco di parabola C ---
    f = 2*(x**2 + y**2)*y - 24*y + 2*x**2
    risol = [
        _passo("Derivate: f_x=4xy+4x=4x(y+1), f_y=2x²+6y²-24. La prima si annulla per x=0 oppure y=-1.",
               r"f_x=4x(y+1),\qquad f_y=2x^2+6y^2-24"),
        _passo("Caso x=0: la seconda dà 6y²=24, cioè y=±2. Caso y=-1: la seconda dà 2x²+6-24=0, cioè x²=9 e "
               "x=±3.",
               r"x=0:\ y=\pm2;\qquad y=-1:\ 2x^2=18\Rightarrow x=\pm3"),
        _passo("Punti stazionari:", r"(0,2),\quad (0,-2),\quad (3,-1),\quad (-3,-1)")]
    ys = (sp.sqrt(34) - 1)/3
    h = sp.Symbol('t')
    hh = 2*h**3 + 2*h**2 - 22*h
    hmin = sp.simplify(hh.subs(h, ys))
    arco_x = np.linspace(-np.sqrt(2), np.sqrt(2), 400)
    arco = [x_ for x_ in arco_x if abs(x_) >= 1]
    post = [
        _passo("Insieme C: da x²=y con 1≤y≤2 si ha 1≤x²≤2, cioè C è formato da DUE archi della parabola y=x², "
               "per x∈[-√2,-1] e per x∈[1,√2] (disegnati in verde nella figura). È un insieme chiuso e "
               "limitato, quindi compatto.",
               r"C=\{(x,x^2):\ 1\le|x|\le\sqrt2\},\qquad \text{estremi: }(\pm1,1),\ (\pm\sqrt2,2)"),
        _passo("Esistenza: f è continua (polinomio) e C è compatto: per il teorema di Weierstrass f ammette "
               "massimo e minimo assoluti su C. Nessuno dei punti stazionari trovati sta su C (nessuno "
               "verifica x²=y con 1≤y≤2), quindi gli estremi sono da cercare con la restrizione di f a C.",
               r"(0,\pm2),\ (\pm3,-1)\notin C"),
        _passo("Restrizione: su C vale x²=y, quindi f diventa una funzione della sola y (con y∈[1,2]; a ogni "
               "y corrispondono i due punti simmetrici x=±√y, con lo stesso valore):",
               r"h(y)=f(\pm\sqrt y,y)=2(y+y^2)y-24y+2y=2y^3+2y^2-22y,\quad y\in[1,2]"),
        _passo("Derivata: h'(y)=6y²+4y-22=2(3y²+2y-11), che si annulla per y*=(√34-1)/3≈1,61∈[1,2]: h "
               "decresce fino a y* e poi cresce. Confrontiamo y*, y=1 e y=2:",
               r"h(1)=-18,\quad h(2)=-20,\quad h(y^*)=\frac{202-136\sqrt{34}}{27}\approx-21{,}89"),
        _passo("Conclusione: il minimo assoluto su C è h(y*)≈-21,89, assunto nei due punti (±√y*,y*); il "
               "massimo assoluto è -18, assunto nei due punti (±1,1).",
               r"\min_C f=\frac{202-136\sqrt{34}}{27}\ \text{in }(\pm\sqrt{y^*},y^*),\qquad \max_C f=-18\ \text{in }(\pm1,1)")]
    out.append(_liberi("22 luglio 2025", 1,
                       "Determinare e classificare i punti critici della funzione f(x,y) = 2(x²+y²)y-24y+2x². "
                       "Dopo averlo disegnato, stabilire se ammette massimi e minimi assoluti nell'insieme "
                       "C = {(x,y) ∈ R²: x² = y, 1 ≤ y ≤ 2}.",
                       f, [(0, 2), (0, -2), (3, -1), (-3, -1)], risol=risol, post=post, box=(-4.5, 4.5, -3.5, 4),
                       extra_linee=[(list(np.linspace(1, np.sqrt(2), 60)), list(np.linspace(1, np.sqrt(2), 60)**2), "C (arco x>0)"),
                                    (list(np.linspace(-np.sqrt(2), -1, 60)), list(np.linspace(-np.sqrt(2), -1, 60)**2), "C (arco x<0)")]))

    # --- gennaio 2025 (es. 12): log[1 - xy(x^2+y^2-1)] -- solo punti stazionari ---
    A = 1 - x*y*(x**2 + y**2 - 1)
    f = sp.log(A)
    pts = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (R_(1, 2), R_(1, 2)), (R_(-1, 2), R_(-1, 2)),
           (R_(1, 2), R_(-1, 2)), (R_(-1, 2), R_(1, 2))]
    pre = [_passo("Dominio: serve A=1-xy(x²+y²-1)>0 (argomento del logaritmo positivo). È una regione del "
                  "piano delimitata dalla curva di equazione xy(x²+y²-1)=1; i punti stazionari trovati "
                  "vanno poi verificati nel dominio.",
                  r"D=\{(x,y):\ 1-xy(x^2+y^2-1)\gt0\}")]
    risol = [
        _passo("Derivate: f_x=-y(3x²+y²-1)/A, f_y=-x(x²+3y²-1)/A. Annulliamo i numeratori (A>0 nel "
               "dominio).",
               r"\begin{cases}y\,(3x^2+y^2-1)=0\\ x\,(x^2+3y^2-1)=0\end{cases}"),
        _passo("Caso y=0: la seconda diventa x(x²-1)=0, cioè x=0,±1. Caso x=0: la prima diventa y(y²-1)=0, "
               "cioè y=0,±1. Caso x≠0 e y≠0: devono annullarsi le parentesi, 3x²+y²=1 e x²+3y²=1: "
               "sottraendo si ottiene x²=y² e poi x²=y²=1/4.",
               r"y=0:\ x\in\{0,\pm1\};\quad x=0:\ y\in\{0,\pm1\};\quad x^2=y^2=\tfrac14\ \Rightarrow\ x=\pm\tfrac12,\ y=\pm\tfrac12"),
        _passo("Verifica nel dominio: in tutti e 9 i punti A>0 (A=1 nei primi cinque, A=9/8 in "
               "(1/2,1/2) e (-1/2,-1/2), A=7/8 in (1/2,-1/2) e (-1/2,1/2)). I punti stazionari sono "
               "quindi nove:",
               r"(0,0),\ (\pm1,0),\ (0,\pm1),\ \left(\pm\tfrac12,\pm\tfrac12\right)\ \text{(quattro combinazioni di segni)}")]
    for px, py in pts:
        assert A.subs({x: px, y: py}) > 0
    out.append(_liberi("gennaio 2025", 12,
                       "Data la funzione f(x,y) = log[1 - xy(x²+y²-1)] determinare i punti stazionari. Non è "
                       "richiesto lo studio della natura di tali punti.",
                       f, pts, pre=pre, risol=risol, box=(-1.6, 1.6, -1.6, 1.6),
                       nota_testo="(Per la verifica automatica indica comunque anche la natura di ciascun "
                                  "punto.)"))

    # --- gennaio 2025 (es. 15): x^2 y^3 (6-x-y): segno + punti stazionari e natura ---
    f = x**2*y**3*(6 - x - y)
    pre = [_passo("Passo a) — segno: x²≥0 (nullo solo per x=0), y³ ha il segno di y e (6-x-y) è positivo sotto "
                  "la retta x+y=6. Quindi (per x≠0) f>0 se y>0 e x+y<6 oppure y<0 e x+y>6; f<0 negli altri "
                  "casi; f=0 sulle rette x=0, y=0, x+y=6 (zone colorate in figura).",
                  r"f\gt0\iff\begin{cases}y\gt0,\ x+y\lt6\\ \text{oppure } y\lt0,\ x+y\gt6\end{cases}(x\ne0),"
                  r"\qquad f=0\iff x=0,\ y=0,\ x+y=6")]
    risol = [
        _passo("Passo b) — derivate: f_x=xy³(12-3x-2y), f_y=x²y²(18-3x-4y). Le due equazioni si annullano "
               "entrambe se x=0 (asse y) oppure se y=0 (asse x): due rette di punti stazionari.",
               r"f_x=xy^3(12-3x-2y),\qquad f_y=x^2y^2(18-3x-4y)"),
        _passo("Fuori dagli assi (x≠0, y≠0) devono annullarsi le parentesi: 3x+2y=12 e 3x+4y=18. "
               "Sottraendo: 2y=6.",
               r"\begin{cases}3x+2y=12\\3x+4y=18\end{cases}\Rightarrow y=3,\ x=2"),
        _passo("Punti stazionari: i due assi coordinati e il punto isolato (2,3).",
               r"x=0\ (\forall y),\quad y=0\ (\forall x),\quad (2,3)")]
    post = [
        _passo("Attenzione: sugli assi l'Hessiana ha determinante nullo (le derivate seconde hanno fattori x o "
               "y non compensati): il test non decide e si usa lo studio del segno. Vicino a (0,b) il "
               "fattore x²≥0, quindi il segno di f è quello di b³(6-b).",
               r"(0,b):\ \operatorname{sgn}f=\operatorname{sgn}\,b^3(6-b)\ \Rightarrow\ "
               r"\begin{cases}0\lt b\lt6 & \text{minimo}\\ b\lt0\ \vee\ b\gt6 & \text{massimo}\\ b=0,\ 6 & \text{sella}\end{cases}"),
        _passo("Vicino a (a,0): il fattore y³ cambia segno con y mentre il resto vale a²(6-a)≠0 se a≠0,6: "
               "f assume segni opposti, quindi sella; anche per a=0 (f≈6x²y³) e per a=6 (f≈-36y³(x+y-6), "
               "che assume entrambi i segni) si hanno selle.",
               r"(a,0):\ f\approx y^3\,a^2(6-a)\ \text{cambia segno}\ \Rightarrow\ \text{sella}\ \ \forall a")]
    reps = [(0, 3, 'minimo'), (0, -1, 'massimo'), (0, 7, 'massimo'), (0, 6, 'sella'), (1, 0, 'sella'),
            (0, 0, 'sella')]
    out.append(_liberi("gennaio 2025", 15,
                       "Data la funzione f(x,y) = x²y³(6-x-y): a) studiare il segno; b) determinare i punti "
                       "stazionari e studiarne la natura.",
                       f, [(2, 3)], pre=pre, risol=risol, post=post, box=(-3, 9, -4, 9), segno=True,
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-3, 9, 9, -3, "x+y=6"), (0, -4, 0, 9, "x=0"), (-3, 0, 9, 0, "y=0")]))

    # --- gennaio 2025 (es. 18) e aprile 2024 (es. 1): 2x^2y + 2xy^2 - x^2y^2 - 4xy ---
    f = 2*x**2*y + 2*x*y**2 - x**2*y**2 - 4*x*y
    risol = [
        _passo("Fattorizziamo: f=-xy(x-2)(y-2). Derivate: f_x=-2y(x-1)(y-2), f_y=-2x(y-1)(x-2). "
               "La prima si annulla per y=0, x=1 o y=2; la seconda per x=0, y=1 o x=2.",
               r"f_x=-2y(x-1)(y-2),\qquad f_y=-2x(y-1)(x-2)"),
        _passo("Incrociamo le possibilità (9 combinazioni): y=0 con x=0 o x=2; x=1 con y=1; y=2 con x=0 o "
               "x=2. Le altre combinazioni (ad esempio y=0 e y=1) sono incompatibili.",
               r"(0,0),\ (2,0),\ (1,1),\ (0,2),\ (2,2)")]
    out.append(_liberi("gennaio 2025", 18,
                       "Data la funzione f(x,y) = 2x²y+2xy²-x²y²-4xy, determinare i punti stazionari. Non è "
                       "richiesto lo studio della natura di tali punti. (Stessa funzione in aprile 2024: "
                       "determinare i punti di massimo e di minimo.)",
                       f, [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)], risol=risol, box=(-1, 3, -1, 3),
                       nota_testo="(Per la verifica automatica indica comunque anche la natura di ciascun "
                                  "punto.)"))

    # --- maggio 2024 (es. 2): 3x^2 y - y^3 + x^2 con Weierstrass sul rettangolo S ---
    f = 3*x**2*y - y**3 + x**2
    risol = [
        _passo("Derivate: f_x=6xy+2x=2x(3y+1), f_y=3x²-3y²=3(x²-y²). La prima dà x=0 oppure y=-1/3.",
               r"f_x=2x(3y+1),\qquad f_y=3(x^2-y^2)"),
        _passo("Caso x=0: la seconda diventa -3y²=0, quindi y=0. Caso y=-1/3: la seconda dà x²=y²=1/9, "
               "cioè x=±1/3.",
               r"x=0:\ y=0;\qquad y=-\tfrac13:\ x=\pm\tfrac13"),
        _passo("Punti stazionari:", r"(0,0),\quad \left(\tfrac13,-\tfrac13\right),\quad \left(-\tfrac13,-\tfrac13\right)")]
    ov = {(0, 0): ('sella', [_passo(
        "Attenzione: in (0,0) si ha f_xx=2, f_xy=0, f_yy=0, quindi det H=0 (determinante nullo): il test non "
        "decide. Studiamo f lungo l'asse y (x=0): f(0,y)=-y³ cambia segno con y, mentre lungo l'asse x "
        "f=x²≥0: valori di segno opposto, quindi (0,0) è una sella.",
        r"f(0,y)=-y^3\gtrless0\ \text{per }y\lessgtr0\ \Rightarrow\ \text{sella}")])}
    post = [
        _passo("Parte (b): l'insieme S=[0,1]×[0,2] è chiuso e limitato (compatto) e f è continua (polinomio): "
               "per il teorema di Weierstrass f ammette massimo e minimo assoluti in S.",
               r"S=[0,1]\times[0,2]\ \text{compatto},\ f\in C^0(S)\ \Rightarrow\ \exists\,\max_S f,\ \min_S f"),
        _passo("Per trovarli: gli unici punti stazionari (0,0) e (±1/3,-1/3) non sono interni a S (hanno "
               "y≤0), quindi gli estremi stanno sulla frontiera. Restringiamo f ai quattro lati:",
               r"x=0:\ -y^3\ (\in[-8,0]);\quad x=1:\ 1+3y-y^3\ (\max=3\text{ in }y=1,\ \min=-1\text{ in }y=2);"
               r"\quad y=0:\ x^2\ (\in[0,1]);\quad y=2:\ 7x^2-8\ (\in[-8,-1])"),
        _passo("Confrontando i valori sui lati: il massimo assoluto in S è 3, assunto in (1,1); il minimo "
               "assoluto è -8, assunto in (0,2).",
               r"\max_S f=f(1,1)=3,\qquad \min_S f=f(0,2)=-8")]
    out.append(_liberi("maggio 2024", 2,
                       "Data la funzione f(x,y) = 3x²y - y³ + x²: a) si determinino i punti stazionari e se ne "
                       "studi la natura; b) si dica, giustificando la risposta sulla base della teoria, se la "
                       "funzione ammette massimo assoluto e minimo assoluto nell'insieme "
                       "S = {(x,y) ∈ R²: 0 ≤ x ≤ 1, 0 ≤ y ≤ 2}.",
                       f, [(0, 0), (R_(1, 3), R_(-1, 3)), (R_(-1, 3), R_(-1, 3))], risol=risol, override=ov,
                       post=post, box=(-1.5, 1.5, -1.2, 2.4),
                       extra_linee=[([0, 1, 1, 0, 0], [0, 0, 2, 2, 0], "rettangolo S")]))

    # --- gennaio 2024 (es. 1): x^3 + y^3 - (1+x+y)^3 ---
    f = x**3 + y**3 - (1 + x + y)**3
    pre = [_passo("Dominio: f è un polinomio, quindi definita e derivabile su tutto R².",
                  r"\mathrm{dom}\,f=\mathbb{R}^2")]
    risol = [
        _passo("Derivate: f_x=3x²-3(1+x+y)², f_y=3y²-3(1+x+y)². Uguagliando a zero: x²=(1+x+y)² e "
               "y²=(1+x+y)². Quindi x²=y², cioè y=x oppure y=-x.",
               r"x^2=(1+x+y)^2=y^2\ \Rightarrow\ y=x\ \text{ oppure }\ y=-x"),
        _passo("Caso y=x: x²=(1+2x)², cioè x=1+2x (x=-1) oppure x=-(1+2x) (x=-1/3). Caso y=-x: "
               "x²=1, cioè x=±1.",
               r"y=x:\ x=-1\ \text{ o }\ x=-\tfrac13;\qquad y=-x:\ x=\pm1"),
        _passo("Punti stazionari:",
               r"(-1,-1),\quad \left(-\tfrac13,-\tfrac13\right),\quad (1,-1),\quad (-1,1)")]
    out.append(_liberi("gennaio 2024", 1,
                       "Data la funzione f(x,y) = x³ + y³ - (1+x+y)³: a) determinare il dominio; b) studiare "
                       "la natura dei punti stazionari.",
                       f, [(-1, -1), (R_(-1, 3), R_(-1, 3)), (1, -1), (-1, 1)], pre=pre, risol=risol,
                       box=(-2.5, 2, -2.5, 2)))

    # --- gennaio 2024 (es. 2): x^2 log(y-1) - 8y + y^2 ---
    f = x**2*sp.log(y - 1) - 8*y + y**2
    pre = [_passo("Dominio: il logaritmo richiede y-1>0, cioè y>1: il dominio è il semipiano aperto sopra "
                  "la retta y=1 (retta esclusa, tratteggiata in figura).",
                  r"D=\{(x,y)\in\mathbb{R}^2:\ y\gt1\}")]
    risol = [
        _passo("Derivate: f_x=2x·log(y-1), f_y=x²/(y-1)+2y-8. La prima si annulla per x=0 oppure "
               "log(y-1)=0, cioè y=2.",
               r"f_x=2x\ln(y-1),\qquad f_y=\frac{x^2}{y-1}+2y-8"),
        _passo("Caso x=0: la seconda dà 2y-8=0, y=4 (accettabile: 4>1). Caso y=2: la seconda dà x²+4-8=0, "
               "cioè x=±2.",
               r"x=0:\ y=4;\qquad y=2:\ x^2=4\Rightarrow x=\pm2"),
        _passo("Punti stazionari (tutti nel dominio):", r"(0,4),\quad (2,2),\quad (-2,2)")]
    out.append(_liberi("gennaio 2024", 2,
                       "Data la funzione f(x,y) = x² log(y-1) - 8y + y²: a) determinare il dominio e "
                       "disegnarlo; b) studiare la natura dei punti stazionari.",
                       f, [(0, 4), (2, 2), (-2, 2)], pre=pre, risol=risol, box=(-4, 4, 0.2, 6),
                       extra_linee=[(-4, 1, 4, 1, "y=1 (esclusa)")]))

    # --- gennaio 2024 (es. 3): log(x^2) log(y) ---
    f = sp.log(x**2)*sp.log(y)
    pre = [_passo("Dominio: log(x²) richiede x²>0, cioè x≠0; log y richiede y>0. Il dominio è il semipiano "
                  "y>0 privato dell'asse y (due quadranti aperti, I e II).",
                  r"D=\{(x,y):\ x\ne0,\ y\gt0\}")]
    risol = [
        _passo("Derivate: f_x=(2/x)·log y, f_y=log(x²)/y. La prima si annulla per log y=0, cioè y=1; la "
               "seconda per log(x²)=0, cioè x²=1.",
               r"f_x=\frac{2}{x}\ln y=0\iff y=1;\qquad f_y=\frac{\ln x^2}{y}=0\iff x=\pm1"),
        _passo("Punti stazionari (nel dominio):", r"(1,1),\quad (-1,1)")]
    out.append(_liberi("gennaio 2024", 3,
                       "Data la funzione f(x,y) = log(x²)·log(y): a) determinare il dominio e disegnarlo; b) "
                       "studiare la natura dei punti stazionari.",
                       f, [(1, 1), (-1, 1)], pre=pre, risol=risol, box=(-3, 3, 0.1, 4),
                       extra_linee=[(0, 0.1, 0, 4, "x=0 (esclusa)")]))

    # --- luglio 2023 (es. 7): (xy - 2x)/(x+3y) ---
    f = (x*y - 2*x)/(x + 3*y)
    pre = [_passo("Dominio: il denominatore deve essere non nullo, x+3y≠0: il dominio è tutto il piano "
                  "privato della retta x+3y=0 (y=-x/3), tratteggiata in figura.",
                  r"D=\{(x,y)\in\mathbb{R}^2:\ x+3y\ne0\}")]
    risol = [
        _passo("Derivate (quoziente): f_x=3y(y-2)/(x+3y)², f_y=x(x+6)/(x+3y)². I numeratori si annullano: "
               "y=0 o y=2, e x=0 o x=-6.",
               r"f_x=\frac{3y(y-2)}{(x+3y)^2},\qquad f_y=\frac{x(x+6)}{(x+3y)^2}"),
        _passo("Combinazioni: (0,0) e (-6,2) giacciono sulla retta x+3y=0 (fuori dal dominio): vanno "
               "scartate. Restano (-6,0) e (0,2).",
               r"(0,0):\ 0+0=0,\ (-6,2):\ -6+6=0\ \text{(esclusi)};\qquad (-6,0),\ (0,2)\ \text{ammessi}"),
        _passo("Punti stazionari:", r"(-6,0),\quad (0,2)")]
    out.append(_liberi("luglio 2023", 7,
                       "Data la funzione f(x,y) = (xy-2x)/(x+3y) determinare: i) l'insieme di definizione e "
                       "disegnarlo; ii) gli eventuali punti di massimo e/o di minimo.",
                       f, [(-6, 0), (0, 2)], pre=pre, risol=risol, box=(-9, 4, -4, 5),
                       extra_linee=[(-9, 3, 4, -4/3, "x+3y=0 (esclusa)")]))

    # --- settembre 2021 (es. 3): (x+y)(x-y)^2 ---
    f = (x + y)*(x - y)**2
    risol = [
        _passo("Derivate: f_x=(x-y)(3x+y), f_y=-(x-y)(x+3y). Hanno il fattore comune (x-y): si annullano "
               "entrambe lungo tutta la retta y=x. Fuori dalla retta dovrebbe essere 3x+y=0 e x+3y=0, "
               "che ha come unica soluzione l'origine (già sulla retta).",
               r"f_x=(x-y)(3x+y),\quad f_y=-(x-y)(x+3y)"),
        _passo("Punti stazionari: tutta la retta y=x (famiglia non isolata).",
               r"\{(a,a):\ a\in\mathbb{R}\}")]
    post = [
        _passo("Attenzione: su y=x si ha f_xx=4a, f_xy=-4a, f_yy=4a, quindi det H=16a²-16a²=0 (determinante "
               "nullo) e il test non decide. Studiamo il segno: (x-y)²≥0, quindi vicino a (a,a) il segno "
               "di f è quello di (x+y)≈2a.",
               r"\operatorname{sgn}f\ \text{vicino a }(a,a)=\operatorname{sgn}(x+y)\approx\operatorname{sgn}(2a)"),
        _passo("Se a>0: f≥0=f(a,a), minimo (non stretto); se a<0: f≤0, massimo (non stretto); se a=0 il "
               "fattore (x+y) cambia segno attorno all'origine: sella.",
               r"a\gt0:\ \text{minimo};\quad a\lt0:\ \text{massimo};\quad a=0:\ \text{sella}")]
    reps = [(1, 1, 'minimo'), (-1, -1, 'massimo'), (0, 0, 'sella')]
    out.append(_liberi("settembre 2021", 3,
                       "Data la seguente funzione reale di due variabili reali determinare eventuali massimi "
                       "e minimi: f(x,y) = (x+y)(x-y)².", f, [], risol=risol, post=post, box=(-3, 3, -3, 3),
                       extra_attesi=[[a, b, t] for a, b, t in reps], nota_testo=_nota_fam(reps),
                       extra_linee=[(-3, -3, 3, 3, "y=x (punti stazionari)")]))

    # --- luglio 2023 (es. 4): x e^{(x-1)y} - x ---
    f = x*sp.exp((x - 1)*y) - x
    risol = [
        _passo("Derivate: f_x=e^((x-1)y)(1+xy)-1, f_y=x(x-1)e^((x-1)y). La seconda (esponenziale >0) si "
               "annulla per x=0 oppure x=1.",
               r"f_x=e^{(x-1)y}(1+xy)-1,\qquad f_y=x(x-1)e^{(x-1)y}"),
        _passo("Caso x=0: la prima diventa e^(-y)-1=0, cioè y=0. Caso x=1: la prima diventa 1+y-1=y=0.",
               r"x=0:\ e^{-y}=1\Rightarrow y=0;\qquad x=1:\ y=0"),
        _passo("Punti stazionari:", r"(0,0),\quad (1,0)")]
    out.append(_liberi("luglio 2023", 4,
                       "Data la funzione f(x,y) = x·e^((x-1)y) - x determinare gli eventuali punti di massimo "
                       "e/o di minimo.", f, [(0, 0), (1, 0)], risol=risol, box=(-2, 3, -3, 3)))
    return out


# ---------------------------------------------------------------------------
# registrazione nel banco 'Esame'
# ---------------------------------------------------------------------------
import re as _re


def _igiene(voci):
    """Campi di testo semplice (non LaTeX): spazi attorno a '<' (niente '<' seguito da lettera)."""
    for _v in voci:
        _v["testo"] = _re.sub(r"\s*<\s*", " < ", _v["testo"])
        _v["suggerimento"] = _re.sub(r"\s*<\s*", " < ", _v["suggerimento"])
        for _p in _v["passi"]:
            if _p.get("testo"):
                _p["testo"] = _re.sub(r"\s*<\s*", " < ", _p["testo"])
    return voci


ESAME["lagrange"].extend(_igiene(_batch_A() + _batch_B() + _batch_C()))
ESAME["punti_liberi"].extend(_igiene(_batch_D() + _batch_E() + _batch_F()))
