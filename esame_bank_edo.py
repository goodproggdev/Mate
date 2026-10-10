# -*- coding: utf-8 -*-
"""
Addendum 'EDO': problemi d'esame reali di equazioni differenziali (1° ordine: lineari,
separabili, Bernoulli; 2° ordine a coefficienti costanti col metodo di somiglianza) tratti
dai PDF degli appelli in ExEsami (Settembre 2021 ... Aprile 2026), con risoluzione completa
passo-passo. Ogni soluzione e' calcolata con sympy e VERIFICATA per sostituzione
nell'equazione e nelle condizioni iniziali al momento dell'import (assert).

Duplicati: un testo identico presente in piu' appelli compare una sola volta, con fonte
l'appello piu' recente. Se un'equazione compare in un appello senza condizioni di Cauchy e in
un altro con le condizioni, la voce riporta le condizioni (nel testo e' indicato quale appello).
"""
import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import sympy as sp

import esame_bank
from esame_bank import ESAME, _voce, _passo, _tex, _png

x = esame_bank.x
C = sp.Symbol('C')
c1s, c2s = sp.symbols('c_1 c_2')
r_ = sp.Symbol('r')


# ---------------------------------------------------------------------------
# utilita' comuni
# ---------------------------------------------------------------------------

def _num_ok(expr, xs, tol=1e-7):
    """True se |expr(x)| < tol in tutti i punti xs (verifica numerica del residuo)."""
    for xv in xs:
        v = complex(sp.N(expr.subs(x, sp.nsimplify(xv)), 30))
        if abs(v) > tol:
            return False
    return True


def _u(v):
    """Scrittura 'a parole' (unicode) di un valore sympy per i testi dei passi."""
    t = str(v)
    return t.replace("pi", "π").replace("E", "e").replace("sqrt", "√").replace("*", "·")


def _campioni(sol, xs):
    out = []
    for xv in xs:
        try:
            v = complex(sp.N(sol.subs(x, sp.nsimplify(xv)), 20))
        except Exception:
            continue
        if abs(v.imag) < 1e-9 and np.isfinite(v.real) and abs(v.real) < 1e6:
            out.append([float(xv), float(v.real)])
    return out


def _fig_sol(sol, punti, xmin, xmax, titolo):
    """Grafico della soluzione, con i punti delle condizioni iniziali evidenziati."""
    try:
        f = sp.lambdify(x, sol, 'numpy')
        xs = np.linspace(float(xmin), float(xmax), 500)
        with np.errstate(all='ignore'):
            ys = np.asarray(f(xs) + 0 * xs, dtype=complex)
        ys = np.where(np.abs(ys.imag) < 1e-9, ys.real, np.nan).astype(float)
        ys[~np.isfinite(ys)] = np.nan
        fig, ax = plt.subplots(figsize=(6, 4.4))
        ax.plot(xs, ys, linewidth=2, color='#2e5c8a')
        for (px, py, lab) in punti:
            ax.plot(float(px), float(py), 'ro', markersize=7, label=lab)
        fin = ys[np.isfinite(ys)]
        if fin.size:
            lo, hi = np.percentile(fin, [2, 98])
            pad = 0.25 * max(hi - lo, 1e-6)
            ax.set_ylim(lo - pad, hi + pad)
        ax.set_xlabel('x')
        ax.set_ylabel('y(x)')
        ax.set_title(titolo, fontsize=10)
        if punti:
            ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return _png(fig)
    except Exception:
        plt.close('all')
        return None


# ---------------------------------------------------------------------------
# EDO 2° ORDINE a coefficienti costanti: costruttore completo (omogenea, somiglianza
# con casi 1-5 e risonanza, sovrapposizione, Cauchy anche con condizioni in x0 != 0)
# ---------------------------------------------------------------------------

def T(tex, p=1, alpha=0, beta=0, trig=None, txt=None):
    """Un termine del secondo membro:  p(x) * e^(alpha x) * [cos|sin](beta x).
    tex = scrittura LaTeX; txt = scrittura 'a parole' (senza LaTeX) per i testi dei passi."""
    p = sp.sympify(p)
    alpha = sp.sympify(alpha)
    beta = sp.sympify(beta)
    expr = p * sp.exp(alpha * x)
    if trig == 'cos':
        expr = expr * sp.cos(beta * x)
    elif trig == 'sin':
        expr = expr * sp.sin(beta * x)
    return {"tex": tex, "txt": txt or tex, "p": p, "alpha": alpha, "beta": beta, "trig": trig, "expr": expr}


def _molteplicita(c2, c1, c0, z):
    P = c2 * r_**2 + c1 * r_ + c0
    if sp.simplify(P.subs(r_, z)) != 0:
        return 0
    if sp.simplify(sp.diff(P, r_).subs(r_, z)) != 0:
        return 1
    return 2


def _grado(t):
    return sp.degree(t["p"], x) if t["p"].has(x) else 0


def _caso(t):
    n = _grado(t)
    if t["beta"] == 0:
        if t["alpha"] == 0:
            return "Caso 1, polinomio di grado %d" % n if n > 0 else "Caso 1, costante"
        if n == 0:
            return "Caso 2, esponenziale A·e^(λx) con λ=%s" % t["alpha"]
        return "Caso 5, e^(λx)·p(x) con λ=%s e p di grado %d" % (t["alpha"], n)
    if t["alpha"] == 0 and n == 0:
        return "Caso 3, A·cos(ωx)+B·sin(ωx) con ω=%s" % t["beta"]
    if n == 0:
        return "Caso 4, e^(αx)(A cos βx+B sin βx) con α=%s, β=%s" % (t["alpha"], t["beta"])
    return ("caso misto, polinomio di grado %d per e^(αx) per trigonometrica con α=%s, β=%s "
            "(estensione dei Casi 4–5 del formulario)" % (n, t["alpha"], t["beta"]))


def _exp_tex(alpha):
    if alpha == 0:
        return ""
    if alpha == 1:
        return "e^{x}"
    if alpha == -1:
        return "e^{-x}"
    return "e^{" + _tex(alpha) + "x}"


def _poly_tex(syms):
    n = len(syms) - 1
    out = []
    for i, s in enumerate(syms):
        d = n - i
        nm = s.name
        out.append(nm if d == 0 else (nm + "x" if d == 1 else nm + "x^{%d}" % d))
    return "+".join(out)


def _trig_tex(be, f):
    bt = "" if be == 1 else _tex(be)
    return "\\" + f + " " + bt + "x"


def _ansatz(t, s, letters):
    """Ansatz del metodo di somiglianza per il termine t con molteplicita' s della radice.
    Restituisce (espressione sympy, latex, lista simboli)."""
    n = _grado(t)
    al, be = t["alpha"], t["beta"]
    pre_tex = "" if s == 0 else ("x" if s == 1 else "x^{%d}" % s)
    if be == 0:
        sy = [sp.Symbol(letters[i]) for i in range(n + 1)]
        P = sum(sy[i] * x**(n - i) for i in range(n + 1))
        expr = x**s * P * sp.exp(al * x)
        ptex = _poly_tex(sy)
        if n > 0 and (pre_tex or al != 0):
            ptex = "(" + ptex + ")"
        return expr, pre_tex + ptex + _exp_tex(al), sy
    sy = [sp.Symbol(letters[i]) for i in range(2 * (n + 1))]
    P = sum(sy[i] * x**(n - i) for i in range(n + 1))
    Q = sum(sy[n + 1 + i] * x**(n - i) for i in range(n + 1))
    expr = x**s * sp.exp(al * x) * (P * sp.cos(be * x) + Q * sp.sin(be * x))
    if n == 0:
        inner = sy[0].name + _trig_tex(be, "cos") + "+" + sy[1].name + _trig_tex(be, "sin")
    else:
        inner = ("(" + _poly_tex(sy[:n + 1]) + ")" + _trig_tex(be, "cos") + "+(" + _poly_tex(sy[n + 1:]) + ")"
                 + _trig_tex(be, "sin"))
    fuori = pre_tex + _exp_tex(al)
    if fuori:
        return expr, fuori + r"\left[" + inner + r"\right]", sy
    return expr, inner, sy


def _disp(expr, alpha, beta):
    """LaTeX di expr scritta come e^(alpha x) * ( ... ) con cos/sin/x raccolti."""
    inner = sp.expand(expr * sp.exp(-alpha * x))
    if beta != 0:
        inner = sp.collect(inner, [sp.cos(beta * x), sp.sin(beta * x)])
    else:
        inner = sp.collect(inner, x)
    tex = _tex(inner)
    if alpha == 0:
        return tex
    return _exp_tex(alpha) + r"\left(" + tex + r"\right)"


def _op(c2, c1, c0, f):
    return c2 * sp.diff(f, x, 2) + c1 * sp.diff(f, x) + c0 * f


def _lhs_tex(c2, c1, c0, nome="y"):
    parts = []
    for coef, der in ((c2, "''"), (c1, "'"), (c0, "")):
        if coef == 0:
            continue
        a = abs(coef)
        mag = "" if a == 1 else _tex(a)
        parts.append(("-" if coef < 0 else "+", mag + nome + der))
    s = ""
    for i, (sg, tt) in enumerate(parts):
        s += (("-" if sg == "-" else "") if i == 0 else sg) + tt
    return s


def _cond_tex(conds):
    out = []
    for (xk, k, v) in conds:
        sym = "y" if k == 0 else "y'"
        out.append("%s(%s)=%s" % (sym, _tex(xk), _tex(v)))
    return r",\ ".join(out)


def _mon_tex(m, be):
    i = m[0]
    parts = []
    if i == 1:
        parts.append("x")
    elif i > 1:
        parts.append("x^{%d}" % i)
    if be != 0:
        if m[1] > 0:
            parts.append(_trig_tex(be, "cos"))
        if m[2] > 0:
            parts.append(_trig_tex(be, "sin"))
    return "".join(parts) if parts else "1"


def _equazioni(Ly, t, sy):
    """Lista di (latex 'lhs = rhs' per monomio, equazione sympy) per il sistema dei coefficienti."""
    al, be = t["alpha"], t["beta"]
    Cc, Ss = sp.symbols('Cc Ss')
    L_in = sp.expand(Ly * sp.exp(-al * x))
    R_in = sp.expand(t["expr"] * sp.exp(-al * x))
    if be != 0:
        L_in = L_in.subs({sp.cos(be * x): Cc, sp.sin(be * x): Ss})
        R_in = R_in.subs({sp.cos(be * x): Cc, sp.sin(be * x): Ss})
        gens = (x, Cc, Ss)
    else:
        gens = (x,)
    PL = sp.Poly(L_in, *gens)
    PR = sp.Poly(R_in, *gens)
    mons = sorted(set(PL.monoms()) | set(PR.monoms()), reverse=True)
    out = []
    for m in mons:
        lc = PL.coeff_monomial(m)
        rc = PR.coeff_monomial(m)
        out.append((r"\text{coeff. di }" + _mon_tex(m, be) + r":\ " + _tex(sp.expand(lc)) + "=" + _tex(rc),
                    sp.Eq(lc, rc)))
    return out


def _edo2(fonte, testo, coefs, rhs_tex, terms, conds=None, nota_cond=None, xs_camp=None,
          xs_graf=(0, 4), suggerimento=None, classifica_extra=None):
    """coefs=(a2,a1,a0) per a2 y'' + a1 y' + a0 y = f; terms = lista di T(...); conds = lista di
    (x_k, ordine_derivata, valore)."""
    c2, c1, c0 = [sp.sympify(c) for c in coefs]
    f_tot = sum(t["expr"] for t in terms)
    lhs = _lhs_tex(c2, c1, c0)
    testo_latex = lhs + "=" + rhs_tex
    if conds:
        testo_latex += r",\quad " + _cond_tex(conds)
    passi = [_passo("Equazione:", testo_latex)]

    cl_txt = ("Classificazione: è un'equazione differenziale ordinaria LINEARE del SECONDO ORDINE a "
              "coefficienti COSTANTI, NON omogenea (il secondo membro non è identicamente nullo).")
    if classifica_extra:
        cl_txt += " " + classifica_extra
    passi.append(_passo(cl_txt, r"a\,y''+b\,y'+c\,y=f(x)\ \text{ con }\ a=" + _tex(c2) + ",\\ b=" + _tex(c1)
                         + ",\\ c=" + _tex(c0) + r",\ f(x)=" + rhs_tex))

    P = c2 * r_**2 + c1 * r_ + c0
    delta = sp.expand(c1**2 - 4 * c2 * c0)
    radici = sp.solve(sp.Eq(P, 0), r_)
    car = _tex(P) + "=0"
    delta_tex = (r"\Delta=b^2-4ac=(" + _tex(c1) + r")^2-4\cdot(" + _tex(c2) + r")\cdot(" + _tex(c0)
                 + ")=" + _tex(delta))
    if delta > 0:
        r1, r2 = sorted(radici, key=lambda z: float(z))
        rad_tex = r"r_1=" + _tex(r1) + r",\ r_2=" + _tex(r2) + r"\ \ (\text{reali e distinte})"
        y0 = c1s * sp.exp(r1 * x) + c2s * sp.exp(r2 * x)
        y0_tex = "c_1" + _exp_tex(r1) + "+c_2" + _exp_tex(r2)
        tipo_d = "Δ>0: due radici reali distinte"
    elif delta == 0:
        r1 = radici[0]
        rad_tex = r"r=" + _tex(r1) + r"\ \ (\text{reale doppia})"
        y0 = (c1s + c2s * x) * sp.exp(r1 * x)
        y0_tex = "(c_1+c_2x)" + _exp_tex(r1)
        tipo_d = "Δ=0: una radice reale doppia"
    else:
        al0 = sp.simplify(-c1 / (2 * c2))
        be0 = abs(sp.simplify(sp.sqrt(-delta) / (2 * c2)))
        rad_tex = (r"r=" + _tex(al0) + r"\pm " + ("" if be0 == 1 else _tex(be0)) +
                   r"i\ \ (\text{complesse coniugate})")
        y0 = sp.exp(al0 * x) * (c1s * sp.cos(be0 * x) + c2s * sp.sin(be0 * x))
        corpo = "c_1" + _trig_tex(be0, "cos") + "+c_2" + _trig_tex(be0, "sin")
        y0_tex = (_exp_tex(al0) + r"\left(" + corpo + r"\right)") if al0 != 0 else corpo
        tipo_d = "Δ<0: radici complesse coniugate α±iβ con α=%s, β=%s" % (al0, be0)
    passi.append(_passo("Passo 1 — equazione caratteristica dell'omogenea associata (si sostituisce "
                        "y=e^{rx}): " + tipo_d + ".",
                        car + r"\ \Rightarrow\ " + delta_tex + r"\ \Rightarrow\ " + rad_tex))
    passi.append(_passo("Integrale dell'omogenea associata (tabella Δ del formulario, sez. 15.2), con c₁, c₂ "
                        "costanti arbitrarie:", r"y_0(x)=" + y0_tex))

    passi.append(_passo("Passo 2 — forma della soluzione particolare (metodo di somiglianza, formulario "
                        "ufficiale, Casi 1–5): il secondo membro ha %s; per il principio "
                        "di sovrapposizione si cerca una particolare per ciascun termine. Per ognuno si "
                        "controlla la risonanza, cioè se l'esponente (λ, oppure α+iβ) coincide con una "
                        "delle radici del passo 1: in tal caso l'ansatz si moltiplica per x^s, con s "
                        "la molteplicità della radice." % ("un solo termine" if len(terms) == 1 else "%d termini (somma)" % len(terms)), None))
    sol_parz = []
    lettere = "ABCDEFGH"
    molti = len(terms) > 1
    for k, t in enumerate(terms, 1):
        z = t["alpha"] + sp.I * t["beta"] if t["beta"] != 0 else t["alpha"]
        s = _molteplicita(c2, c1, c0, z)
        if t["beta"] != 0:
            tst = "α+iβ = %s" % (str(sp.simplify(z)).replace("I", "i").replace("*", ""))
        else:
            tst = "λ = %s" % t["alpha"]
        if s == 0:
            ris = "%s NON coincide con nessuna radice: nessuna risonanza (s=0)" % tst
        elif s == 1:
            ris = ("%s coincide con una radice semplice: RISONANZA (s=1), si moltiplica "
                   "per x" % tst)
        else:
            ris = ("%s coincide con la radice doppia: RISONANZA doppia (s=2), si "
                   "moltiplica per x²" % tst)
        expr_a, tex_a, sy = _ansatz(t, s, lettere)
        nm = (r"y_{p%d}" % k) if molti else r"y_{p}"
        passi.append(_passo("Termine %s (%s): %s → ansatz" % (t["txt"], _caso(t), ris), nm + "=" + tex_a))
        d1 = sp.diff(expr_a, x)
        d2 = sp.diff(expr_a, x, 2)
        Ly = _op(c2, c1, c0, expr_a)
        passi.append(_passo("Sostituendo l'ansatz nell'equazione (considerando il solo termine %s a secondo "
                            "membro) servono le derivate prima e seconda dell'ansatz:" % t["txt"],
                            nm + "'=" + _disp(d1, t["alpha"], t["beta"]) + r",\quad " + nm + "''="
                            + _disp(d2, t["alpha"], t["beta"])))
        passi.append(_passo("Sostituendo y_p, y_p', y_p'' nel primo membro e raccogliendo i termini simili, "
                            "il risultato deve coincidere col termine noto (condizione di uguaglianza):",
                            _lhs_tex(c2, c1, c0, nm) + "=" + _disp(Ly, t["alpha"], t["beta"])
                            + r"\ \overset{!}{=}\ " + t["tex"]))
        coeffs = _equazioni(Ly, t, sy)
        eq_txt = r"\begin{cases}" + r"\\".join(e[0] for e in coeffs) + r"\end{cases}"
        sol_c = sp.solve([e[1] for e in coeffs], sy, dict=True)[0]
        passi.append(_passo("Uguagliando i coefficienti dei termini simili si ottiene un sistema lineare "
                            "nelle incognite %s:" % ", ".join(s_.name for s_ in sy), eq_txt))
        ypk = expr_a.subs(sol_c)
        assert sp.simplify(_op(c2, c1, c0, ypk) - t["expr"]) == 0, "ansatz non verifica il termine"
        passi.append(_passo("Risolvendo il sistema dei coefficienti e sostituendo i valori trovati nell'ansatz:",
                            r",\ ".join("%s=%s" % (s_.name, _tex(sol_c[s_])) for s_ in sy)
                            + r"\ \Rightarrow\ " + nm + "=" + _disp(ypk, t["alpha"], t["beta"])))
        sol_parz.append(ypk)
    yp = sum(sol_parz)
    if molti:
        passi.append(_passo("Sovrapposizione dei termini: la soluzione particolare completa è la somma delle "
                            "particolari trovate per ciascun termine del secondo membro:",
                            r"y_p=" + "+".join(r"y_{p%d}" % (i + 1) for i in range(len(terms))) + "="
                            + _tex(sp.expand(yp))))
    assert sp.simplify(_op(c2, c1, c0, yp) - f_tot) == 0
    ygen = y0 + yp
    passi.append(_passo("Soluzione generale: somma dell'omogenea associata e della particolare "
                        "(y = y₀ + y_p), con c₁, c₂ costanti arbitrarie:",
                        r"y(x)=y_0(x)+y_p(x)=" + _tex(sp.expand(ygen))))

    if conds:
        yder = sp.diff(ygen, x)
        passi.append(_passo(nota_cond or "Passo 3 — condizioni iniziali (problema di Cauchy): si impongono "
                            "sull'integrale completo; serve quindi anche la derivata y'.",
                            r"y'(x)=" + _tex(sp.expand(yder))))
        eqs, eqs_tex = [], []
        for (xk, k, v) in conds:
            ex = sp.simplify((ygen if k == 0 else yder).subs(x, xk))
            sym = "y" if k == 0 else "y'"
            eqs.append(sp.Eq(ex, v))
            eqs_tex.append("%s(%s)=%s=%s" % (sym, _tex(xk), _tex(ex), _tex(v)))
        passi.append(_passo("Imponendo le condizioni iniziali si ottiene un sistema lineare nelle "
                            "costanti c₁, c₂:", r"\begin{cases}" + r"\\".join(eqs_tex) + r"\end{cases}"))
        cs = sp.solve(eqs, [c1s, c2s], dict=True)[0]
        passi.append(_passo("Risolvendo il sistema lineare:", "c_1=" + _tex(cs[c1s]) + r",\ c_2=" + _tex(cs[c2s])))
        sol = sp.simplify(ygen.subs(cs))
        for (xk, k, v) in conds:
            assert sp.simplify(sp.diff(sol, x, k).subs(x, xk) - v) == 0, "condizione non soddisfatta"
        assert sp.simplify(_op(c2, c1, c0, sol) - f_tot) == 0
        passi.append(_passo("Soluzione del problema di Cauchy (si inseriscono i valori di c₁, c₂):",
                            r"y(x)=" + _tex(sp.expand(sol))))
        passi.append(_passo("Verifica per sostituzione: y soddisfa l'equazione (residuo nullo) e le "
                            "condizioni iniziali.",
                            _lhs_tex(c2, c1, c0) + "-(" + rhs_tex + r")\equiv 0,\quad " + _cond_tex(conds)
                            + r"\ \checkmark"))
        ans = sol
        sugg = suggerimento or "Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)"
        punti = [(xk, sol.subs(x, xk), "y(%s)=%s" % (_u(xk), _u(v))) for (xk, k, v) in conds if k == 0]
        titolo = "Soluzione del problema di Cauchy"
    else:
        ans = yp
        sugg = suggerimento or ("Il testo d'esame chiede la soluzione generale: scrivi SOLO la soluzione "
                                 "particolare y_p(x) del metodo di somiglianza (senza termini dell'omogenea), "
                                 "in sintassi Python, es: x*exp(-x)")
        passi.append(_passo("Per la verifica automatica: la parte c₁(...)+c₂(...) è l'omogenea associata "
                            "(valida per qualunque costante); la parte determinata dal termine noto è la "
                            "particolare del metodo di somiglianza:", r"y_p(x)=" + _tex(sp.expand(yp))))
        punti = []
        titolo = "Soluzione particolare y_p(x)"
    camp = _campioni(ans, xs_camp or [0, 0.3, 0.6, 1.0, 1.5, 2.0])
    png = _fig_sol(ans, punti, xs_graf[0], xs_graf[1], titolo)
    return _voce(fonte, testo, testo_latex, sugg, passi,
                 {"tipo": "funzione_su_campioni", "campioni": camp}, png)


# ---------------------------------------------------------------------------
# EDO 1° ORDINE: costruttori (lineare, Bernoulli, manuale per i separabili)
# ---------------------------------------------------------------------------

def _fin1(fonte, testo, testo_latex, passi, sol, F, x0, y0, xs_check, xs_camp, xs_graf,
          sugg=None, titolo="Soluzione del problema di Cauchy (primo ordine)"):
    """Verifica per sostituzione (residuo F(sol)=0 nei punti xs_check, condizione iniziale) e
    confeziona la voce. F: funzione che, data l'espressione y(x), restituisce il residuo."""
    res = F(sol)
    assert _num_ok(res, xs_check, 1e-6), "residuo non nullo: %s" % [sp.N(res.subs(x, sp.nsimplify(v))) for v in xs_check]
    assert abs(complex(sp.N(sol.subs(x, x0)) - y0)) < 1e-9, "condizione iniziale non soddisfatta"
    camp = _campioni(sol, xs_camp)
    png = _fig_sol(sol, [(x0, y0, "y(%s)=%s" % (_u(x0), _u(y0)))], xs_graf[0], xs_graf[1], titolo)
    return _voce(fonte, testo, testo_latex,
                 sugg or "Scrivi y(x) in sintassi Python, es: log(x)+3/x", passi,
                 {"tipo": "funzione_su_campioni", "campioni": camp}, png)


def _edo1_lineare(fonte, testo, eq_tex, P, Q, A, mu, x0, y0, xs_check, xs_camp, xs_graf,
                  normalizza=None, int_passi=None, nota_dom=None, auto=False, sugg=None, I=None,
                  F_orig=None, cond_tex=None):
    """Equazione lineare y' + P y = Q con fattore integrante mu=e^A (A primitiva di P, data)."""
    P, Q, A, mu = [sp.sympify(v) for v in (P, Q, A, mu)]
    assert sp.simplify(sp.diff(A, x) - P) == 0
    testo_latex = eq_tex + (r",\quad " + (cond_tex or "y(%s)=%s" % (_tex(x0), _tex(y0))))
    passi = [_passo("Equazione:", testo_latex)]
    cl = ("Classificazione: è un'equazione differenziale LINEARE del primo ordine a coefficienti variabili, "
          + ("OMOGENEA (Q=0)" if Q == 0 else "non omogenea") + ". Forma normale y' + P(x)·y = Q(x) con:")
    if normalizza:
        passi.append(_passo(normalizza[0].rstrip(":") + " (equazione lineare in forma normale):", normalizza[1]))
    passi.append(_passo(cl, r"P(x)=" + _tex(P) + r",\qquad Q(x)=" + _tex(Q)))
    nd = (" " + nota_dom) if nota_dom else ""
    passi.append(_passo("Passo 1 — fattore integrante μ(x)=e^{A(x)}, con A(x) primitiva di P(x) (formulario "
                        "ufficiale, tabella dei fattori integranti):" + nd,
                        r"A(x)=\int P(x)\,dx=\int " + _tex(P) + r"\,dx=" + _tex(A)
                        + r"\ \Rightarrow\ \mu(x)=e^{A(x)}=" + _tex(mu)))
    muQ = mu * Q
    passi.append(_passo("Passo 2 — moltiplicando l'equazione per il fattore integrante μ il primo membro diventa "
                        "la derivata del prodotto μ·y (infatti μ'=μP):",
                        r"\left(\mu\,y\right)'=\mu y'+\mu P y=\mu Q\ \Rightarrow\ \left(" + _tex(mu)
                        + r"\,y\right)'=" + _tex(muQ)))
    if I is None:
        I = sp.integrate(muQ, x)
    assert sp.simplify(sp.diff(I, x) - muQ) == 0
    if int_passi:
        for tp in int_passi:
            passi.append(_passo(*tp))
    passi.append(_passo("Passo 3 — integrando i due membri rispetto a x (integrando e moltiplicando "
                        "per 1/μ si ricava y):",
                        r"\mu\,y=\int " + _tex(muQ) + r"\,dx=" + _tex(I) + "+C"))
    ygen = sp.simplify((I + C) / mu)
    passi.append(_passo("Passo 4 — la soluzione generale è y(x) = (1/μ(x))·(∫μQ dx + C), con C costante "
                        "arbitraria:", r"y(x)=\frac{1}{\mu(x)}\left(" + _tex(I) + r"+C\right)=" + _tex(sp.expand(ygen))))
    if auto:
        nota = ("Il testo d'esame chiede solo la soluzione generale. Per la verifica automatica fissiamo "
                "noi una condizione iniziale (y(%s)=%s) e determiniamo C:" % (_u(x0), _u(y0)))
    else:
        nota = "Passo 5 — condizione iniziale (problema di Cauchy): imponendo y(%s)=%s si ricava C:" % (_u(x0), _u(y0))
    Cs = sp.solve(sp.Eq(ygen.subs(x, x0), y0), C)[0]
    passi.append(_passo(nota, "y(" + _tex(x0) + ")=" + _tex(sp.simplify(ygen.subs(x, x0))) + "=" + _tex(y0)
                        + r"\ \Rightarrow\ C=" + _tex(Cs)))
    sol = sp.simplify(ygen.subs(C, Cs))
    passi.append(_passo("Soluzione del problema di Cauchy (sostituendo il valore di C):" if not auto else
                        "Soluzione con questa condizione iniziale:", "y(x)=" + _tex(sp.expand(sol))))
    F = F_orig or (lambda s: sp.diff(s, x) + P * s - Q)
    passi.append(_passo("Verifica per sostituzione nell'equazione e nella condizione iniziale:",
                        r"y'+P\,y-Q\equiv0,\qquad y(" + _tex(x0) + ")=" + _tex(y0) + r"\ \checkmark"))
    return _fin1(fonte, testo, testo_latex, passi, sol, F, x0, y0, xs_check, xs_camp, xs_graf, sugg)


def _segno_tex(c):
    """'+c' oppure '-|c|' per scrivere t' + c t senza il brutto '+-'."""
    if c.could_extract_minus_sign():
        return "-" + _tex(-c)
    return "+" + _tex(c)


def _edo1_bernoulli(fonte, testo, eq_tex, P, Q, n, A, y_of_t, x0, y0, xs_check, xs_camp, xs_graf,
                    normalizza=None, nota_dom=None, auto=False, sugg=None, int_passi=None, nota_sol=None,
                    nota_t_pos=None):
    """Bernoulli y' + P y = Q y^n, n != 0,1; t = y^(1-n); y_of_t: t -> y (ramo scelto)."""
    P, Q, A, n = [sp.sympify(v) for v in (P, Q, A, n)]
    assert sp.simplify(sp.diff(A, x) - P) == 0
    testo_latex = eq_tex + r",\quad y(%s)=%s" % (_tex(x0), _tex(y0))
    passi = [_passo("Equazione:", testo_latex)]
    if normalizza:
        passi.append(_passo(*normalizza))
    passi.append(_passo("Classificazione: è un'equazione di Bernoulli, y' + P(x)·y = Q(x)·y^n, con esponente "
                        "n=%s (non lineare perché n≠0,1):" % n,
                        r"P(x)=" + _tex(P) + r",\ Q(x)=" + _tex(Q) + r",\ n=" + _tex(n)))
    e = 1 - n
    passi.append(_passo("Passo 1 — Bernoulli: si divide per y^n e si pone la sostituzione t=y^{1-n} (qui "
                        "1-n=%s), così t'=(1-n)·y^{-n}·y':" % e,
                        r"y^{-n}y'+P\,y^{1-n}=Q\ \Rightarrow\ t=y^{" + _tex(e) + r"},\ \ t'=" + _tex(e)
                        + r"\,y^{" + _tex(-n) + r"}y'"))
    Pt, Qt, At = sp.simplify(e * P), sp.simplify(e * Q), sp.simplify(e * A)
    passi.append(_passo("Passo 2 — Bernoulli: sostituendo si ottiene un'equazione LINEARE in t (t' + (1-n)P·t = "
                        "(1-n)Q):",
                        r"t'" + _segno_tex(Pt) + r"\,t=" + _tex(Qt)))
    mu = sp.simplify(sp.exp(At))
    muQ = mu * Qt
    nd = (" " + nota_dom) if nota_dom else ""
    passi.append(_passo("Passo 3 — Bernoulli, lineare in t: fattore integrante μ(t)=e^{∫(1-n)P dx}:" + nd,
                        r"\int " + _tex(Pt) + r"\,dx=" + _tex(At) + r"\ \Rightarrow\ \mu=" + _tex(mu)
                        + r"\ \Rightarrow\ (\mu\,t)'=\mu\,Q_t=" + _tex(muQ)))
    I = sp.integrate(muQ, x)
    assert sp.simplify(sp.diff(I, x) - muQ) == 0
    if int_passi:
        for tp in int_passi:
            passi.append(_passo(*tp))
    tgen = sp.simplify((I + C) / mu)
    passi.append(_passo("Integrando e moltiplicando per 1/μ (Bernoulli, soluzione dell'equazione lineare in t):",
                        r"\mu\,t=" + _tex(I) + r"+C\ \Rightarrow\ t(x)=" + _tex(sp.expand(tgen))))
    ygen = y_of_t(tgen)
    passi.append(_passo("Passo 4 — ripristinando y (Bernoulli: y=t^{1/(1-n)}) la soluzione generale è:" +
                        ((" " + nota_sol) if nota_sol else ""),
                        "y(x)=" + _tex(ygen)))
    t0 = sp.simplify(y0**e)
    Cs = sp.solve(sp.Eq(tgen.subs(x, x0), t0), C)
    assert len(Cs) == 1, Cs
    Cs = Cs[0]
    if auto:
        nota = ("Il testo d'esame chiede solo la soluzione generale. Per la verifica automatica fissiamo noi "
                "una condizione iniziale: y(%s)=%s equivale a t(%s)=%s, da cui C:" % (_u(x0), _u(y0), _u(x0), _u(t0)))
    else:
        nota = ("Passo 5 — condizione iniziale: y(%s)=%s equivale a t(%s)=%s^{%s}=%s; imponendola si ricava C:"
                % (_u(x0), _u(y0), _u(x0), _u(y0), _u(e), _u(t0)))
    passi.append(_passo(nota, r"t(" + _tex(x0) + ")=" + _tex(sp.simplify(tgen.subs(x, x0))) + "=" + _tex(t0)
                        + r"\ \Rightarrow\ C=" + _tex(Cs)))
    sol = sp.simplify(y_of_t(sp.simplify(tgen.subs(C, Cs))))
    passi.append(_passo("Soluzione del problema di Cauchy (Bernoulli, tornando a y):" if not auto else
                        "Soluzione con questa condizione iniziale (Bernoulli, tornando a y):",
                        "y(x)=" + _tex(sol)))
    if nota_t_pos:
        passi.append(_passo(*nota_t_pos))
    F = lambda s: sp.diff(s, x) + P * s - Q * s**n
    passi.append(_passo("Verifica per sostituzione nell'equazione e nella condizione iniziale:",
                        r"y'+P\,y-Q\,y^{" + _tex(n) + r"}\equiv0,\qquad y(" + _tex(x0) + ")=" + _tex(y0)
                        + r"\ \checkmark"))
    return _fin1(fonte, testo, testo_latex, passi, sol, F, x0, y0, xs_check, xs_camp, xs_graf, sugg)


# ===========================================================================
# DATI: EDO 1° ORDINE
# ===========================================================================
_pi = sp.pi
_log = sp.log
_E1 = ESAME["edo1"]

# --- 10 aprile 2026, lineare con coefficienti variabili e integrale per parti ----------------
_E1.append(_edo1_lineare(
    "10 aprile 2026",
    "[10 aprile 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y' - y/x = x²·sin(x), "
    "con y(π)=0.",
    r"y'-\frac{1}{x}\,y=x^2\sin x",
    -1 / x, x**2 * sp.sin(x), -_log(x), 1 / x, _pi, 0,
    [2, 3, 4, 5], [3.2, 3.6, 4.0, 5.0, 6.0, 7.0], (_pi, 3 * _pi),
    nota_dom="Il dato iniziale è in x=π>0, quindi lavoriamo su x>0 (A=-ln x, non ln|x|).",
    int_passi=[("Per calcolare ∫ x·sin x dx si integra per parti (u=x, dv=sin x dx ⇒ du=dx, v=-cos x):",
                r"\int x\sin x\,dx=-x\cos x+\int\cos x\,dx=-x\cos x+\sin x")],
    I=-x * sp.cos(x) + sp.sin(x)))

# --- 14 aprile 2026, lineare omogenea (anche a variabili separabili) --------------------------
_E1.append(_edo1_lineare(
    "14 aprile 2026",
    "[14 aprile 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y' = -(1/x)·y - (2/x²)·y, "
    "con y(1)=2.",
    r"y'=-\frac{1}{x}\,y-\frac{2}{x^2}\,y",
    1 / x + 2 / x**2, 0, _log(x) - 2 / x, x * sp.exp(-2 / x), 1, 2,
    [0.5, 1, 2, 3], [1.0, 1.5, 2.0, 3.0, 4.0], (1, 5),
    normalizza=("Riportiamo l'equazione alla forma normale y' + P(x)·y = Q(x) portando a sinistra i termini "
                "in y (è lineare OMOGENEA: Q=0; si potrebbe anche risolvere a variabili separabili):",
                r"y'+\left(\frac{1}{x}+\frac{2}{x^2}\right)y=0"),
    nota_dom="Il dato iniziale è in x=1>0: si lavora su x>0.",
    I=sp.Integer(0)))

# --- 11 maggio 2026, x^2 y' + 3 x y = x sin x (soluzione generale) ----------------------------
_E1.append(_edo1_lineare(
    "11 maggio 2026",
    "[11 maggio 2026, Esercizio 2] Risolvere la seguente equazione differenziale: x²·y' + 3x·y = x·sin(x). "
    "(Il testo chiede la soluzione generale; per la verifica automatica scrivi la soluzione che soddisfa "
    "y(π)=0.)",
    r"x^2y'+3xy=x\sin x",
    3 / x, sp.sin(x) / x, 3 * _log(x), x**3, _pi, 0,
    [2, 3, 4, 5], [3.2, 3.6, 4.0, 5.0, 6.0], (_pi, 3 * _pi),
    normalizza=("Si divide per x² (x≠0) per ottenere la forma normale y' + P(x)·y = Q(x):",
                r"y'+\frac{3}{x}\,y=\frac{\sin x}{x}"),
    nota_dom="Si lavora su x>0 (A=3 ln x, μ=x³).",
    int_passi=[("Per ∫ x²·sin x dx si integra per parti DUE volte (prima u=x², dv=sin x dx):",
                r"\int x^2\sin x\,dx=-x^2\cos x+2\int x\cos x\,dx"),
               ("Seconda integrazione per parti (u=x, dv=cos x dx):",
                r"\int x\cos x\,dx=x\sin x-\int\sin x\,dx=x\sin x+\cos x\ \Rightarrow\ "
                r"\int x^2\sin x\,dx=-x^2\cos x+2x\sin x+2\cos x")],
    I=-x**2 * sp.cos(x) + 2 * x * sp.sin(x) + 2 * sp.cos(x), auto=True,
    sugg="Il testo chiede la soluzione generale: scrivi la soluzione con y(π)=0, es: (-x**2*cos(x)+...)/x**3"))

# --- 4 dicembre 2025, y' = y tg x - sin x, y(-pi)=0 --------------------------------------------
_E1.append(_edo1_lineare(
    "4 dicembre 2025",
    "[4 dicembre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: "
    "y' = y·tg(x) - sin(x), con y(-π)=0.",
    r"y'=y\,\tan x-\sin x",
    -sp.tan(x), -sp.sin(x), _log(sp.cos(x)), sp.cos(x), -_pi, 0,
    [-3.5, -3.0, -2.5, -3.3], [-3.5, -3.3, -3.0, -2.8, -2.5], (-3.6, -2.7),
    normalizza=("Portiamo a sinistra il termine in y per avere la forma normale y' + P(x)·y = Q(x):",
                r"y'-\tan x\cdot y=-\sin x"),
    nota_dom=("Vicino a x=-π si ha cos x<0: A=-∫tan x dx=ln|cos x|, e μ=|cos x|; poiché moltiplicare per "
              "una costante (-1) non cambia nulla, si può usare μ=cos x (derivata: μ'=-sin x=μ·P)."),
    int_passi=[("Per ∫ (-sin x·cos x) dx si pone s=sin x (ds=cos x dx):",
                r"\int-\sin x\cos x\,dx=-\int s\,ds=-\frac{\sin^2x}{2}")],
    I=-sp.sin(x)**2 / 2))

# --- 13 settembre 2025 (= gennaio 2025, es. 6: (x-1)y' + y = 2x) --------------------------------
_E1.append(_edo1_lineare(
    "13 settembre 2025",
    "[13 settembre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: "
    "y' + y/(x-1) = 2x/(x-1), con y(2)=1. (Stesso problema di gennaio 2025, es. 6, scritto come "
    "(x-1)y' + y = 2x, y(2)=1, con richiesta di soluzione generale e Cauchy.)",
    r"y'+\frac{1}{x-1}\,y=\frac{2x}{x-1}",
    1 / (x - 1), 2 * x / (x - 1), _log(x - 1), x - 1, 2, 1,
    [1.5, 2, 3, 4], [2.0, 2.5, 3.0, 4.0, 5.0], (2, 6),
    normalizza=("Nella forma di gennaio 2025, (x-1)y' + y = 2x, si divide per (x-1) (x≠1): è la forma normale "
                "y' + P(x)·y = Q(x) già scritta qui.", r"(x-1)y'+y=2x\ \Longleftrightarrow\ y'+\frac{1}{x-1}y=\frac{2x}{x-1}"),
    nota_dom="Il dato iniziale è in x=2>1: si lavora su x>1 (A=ln(x-1)).",
    I=x**2))

# --- 16 settembre 2025, y' = -y cos x / sin x + 2 cos x, y(pi/4)=1 -----------------------------
_E1.append(_edo1_lineare(
    "16 settembre 2025",
    "[16 settembre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: "
    "y' = -y·cos(x)/sin(x) + 2cos(x), con y(π/4)=1.",
    r"y'=-y\,\frac{\cos x}{\sin x}+2\cos x",
    sp.cos(x) / sp.sin(x), 2 * sp.cos(x), _log(sp.sin(x)), sp.sin(x), _pi / 4, 1,
    [0.5, 0.8, 1.2, 2.0], [0.6, 0.785, 1.0, 1.4, 2.0], (0.3, 2.8),
    normalizza=("Portiamo a sinistra il termine in y (P(x)=cotg x):",
                r"y'+\frac{\cos x}{\sin x}\,y=2\cos x"),
    nota_dom="Intorno a x=π/4 si ha sin x>0: A=ln(sin x), μ=sin x.",
    int_passi=[("Per ∫ 2 sin x·cos x dx si pone s=sin x (ds=cos x dx):",
                r"\int2\sin x\cos x\,dx=\int 2s\,ds=s^2=\sin^2x")],
    I=sp.sin(x)**2))

# --- 23 ottobre 2025, y' + y/x = 2 arctg x, y(1)=-1 ---------------------------------------------
_E1.append(_edo1_lineare(
    "23 ottobre 2025",
    "[23 ottobre 2025, Esercizio 2] Risolvere il seguente problema di Cauchy: y' + y/x = 2·arctg(x), "
    "con y(1)=-1.",
    r"y'+\frac{1}{x}\,y=2\arctan x",
    1 / x, 2 * sp.atan(x), _log(x), x, 1, -1,
    [0.5, 1, 2, 3], [1.0, 1.5, 2.0, 3.0, 4.0], (1, 6),
    nota_dom="Il dato iniziale è in x=1>0: si lavora su x>0.",
    int_passi=[("Per ∫ 2x·arctg x dx si integra per parti (u=arctg x, dv=2x dx ⇒ du=dx/(1+x²), v=x²):",
                r"\int2x\arctan x\,dx=x^2\arctan x-\int\frac{x^2}{1+x^2}dx=x^2\arctan x-\int\left(1-\frac{1}{1+x^2}\right)dx"
                r"=x^2\arctan x-x+\arctan x=(x^2+1)\arctan x-x")],
    I=(x**2 + 1) * sp.atan(x) - x))

# --- 18 ottobre 2025 (testo corretto: y(e)=2) ---------------------------------------------------
_mu18 = x**x * sp.exp(-x)
_E1.append(_edo1_lineare(
    "18 ottobre 2025",
    "[18 ottobre 2025, Esercizio 2] (testo riletto dal PDF: la condizione è y(e)=2) Determinare l'unica "
    "soluzione del problema di Cauchy: y' + (log x)·y = log x, con y(e)=2.",
    r"y'+(\log x)\,y=\log x",
    _log(x), _log(x), x * _log(x) - x, _mu18, sp.E, 2,
    [1, 2, 3, 4], [1.0, 2.0, 2.718, 3.0, 4.0], (1, 4),
    nota_dom="Si lavora su x>0. ∫ln x dx = x ln x - x (per parti), quindi μ=e^{x ln x - x}=x^x·e^{-x}.",
    int_passi=[("Osserviamo che μ'=μ·P=μ·ln x: quindi μ·Q=μ·ln x è PROPRIO la derivata di μ, e l'integrale "
                "è immediato:", r"\int \mu\ln x\,dx=\int\mu'\,dx=\mu=x^x e^{-x}")],
    I=_mu18,
    F_orig=None))

# --- gennaio 2025, es. 3: x^5 y' + 7 x^4 y = x^4 - 1, y(1)=0 -------------------------------------
_E1.append(_edo1_lineare(
    "gennaio 2025",
    "[gennaio 2025, Esercizio 3] Dato il problema di Cauchy x⁵·y' + 7x⁴·y = x⁴ - 1, con y(1)=0: "
    "a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del "
    "problema di Cauchy.",
    r"x^5y'+7x^4y=x^4-1",
    7 / x, (x**4 - 1) / x**5, 7 * _log(x), x**7, 1, 0,
    [0.5, 1, 2, 3], [1.0, 1.5, 2.0, 3.0, 4.0], (1, 5),
    normalizza=("Si divide per x⁵ (x≠0) per ottenere la forma normale y' + P(x)·y = Q(x):",
                r"y'+\frac{7}{x}\,y=\frac{x^4-1}{x^5}"),
    nota_dom="Il dato iniziale è in x=1>0: si lavora su x>0 (A=7 ln x, μ=x⁷).",
    int_passi=[("Calcoliamo μ·Q = x⁷·(x⁴-1)/x⁵ = x²(x⁴-1) = x⁶ - x² e lo integriamo termine a termine:",
                r"\int(x^6-x^2)\,dx=\frac{x^7}{7}-\frac{x^3}{3}")],
    I=x**7 / 7 - x**3 / 3))

# --- gennaio 2025, es. 9: (1+x^4) y' + 4 x^3 y = 4 x^3, y(0)=5 -----------------------------------
_E1.append(_edo1_lineare(
    "gennaio 2025",
    "[gennaio 2025, Esercizio 9] Dato il problema di Cauchy (1+x⁴)·y' + 4x³·y = 4x³, con y(0)=5: "
    "a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del "
    "problema di Cauchy.",
    r"(1+x^4)y'+4x^3y=4x^3",
    4 * x**3 / (1 + x**4), 4 * x**3 / (1 + x**4), _log(1 + x**4), 1 + x**4, 0, 5,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 2.0, 3.0], (-3, 3),
    normalizza=("Si divide per (1+x⁴)>0 per avere la forma normale y' + P(x)·y = Q(x). Osservazione: il primo "
                "membro è già la derivata di (1+x⁴)·y, perché (1+x⁴)'=4x³:",
                r"y'+\frac{4x^3}{1+x^4}\,y=\frac{4x^3}{1+x^4},\qquad (1+x^4)y'+4x^3y=\left((1+x^4)y\right)'"),
    I=x**4))

# --- dicembre 2024 -------------------------------------------------------------------------------
_E1.append(_edo1_lineare(
    "dicembre 2024",
    "[dicembre 2024, Esercizio 2] Data l'equazione differenziale y' + y·cos(x) = sin(x)·cos(x): a) trovare "
    "la soluzione generale; b) risolvere il problema di Cauchy y(0)=1. (Stesso testo di dicembre 2023.)",
    r"y'+y\cos x=\sin x\cos x",
    sp.cos(x), sp.sin(x) * sp.cos(x), sp.sin(x), sp.exp(sp.sin(x)), 0, 1,
    [0, 1, 2, 3], [0, 0.5, 1.0, 2.0, 3.0], (-3, 3),
    int_passi=[("Per ∫ sin x·cos x·e^{sin x} dx si pone s=sin x (ds=cos x dx) e poi si integra per parti:",
                r"\int s\,e^{s}\,ds=(s-1)e^{s}=(\sin x-1)e^{\sin x}")],
    I=(sp.sin(x) - 1) * sp.exp(sp.sin(x))))

_E1.append(_edo1_lineare(
    "dicembre 2024",
    "[dicembre 2024, Esercizio 3] Data l'equazione differenziale y' = x/(x²+1)·y + x/(x²+1): a) trovare la "
    "soluzione generale; b) risolvere il problema di Cauchy y(0)=0.",
    r"y'=\frac{x}{x^2+1}\,y+\frac{x}{x^2+1}",
    -x / (x**2 + 1), x / (x**2 + 1), -_log(x**2 + 1) / 2, 1 / sp.sqrt(x**2 + 1), 0, 0,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 2.0, 3.0], (-3, 3),
    normalizza=("Portiamo a sinistra il termine in y:", r"y'-\frac{x}{x^2+1}\,y=\frac{x}{x^2+1}"),
    int_passi=[("Calcoliamo μ·Q = x/(x²+1)^{3/2} e integriamo con la sostituzione s=x²+1 (ds=2x dx):",
                r"\int x(x^2+1)^{-3/2}dx=\frac12\int s^{-3/2}ds=-s^{-1/2}=-\frac{1}{\sqrt{x^2+1}}")],
    I=-1 / sp.sqrt(x**2 + 1)))

_E1.append(_edo1_lineare(
    "dicembre 2024",
    "[dicembre 2024, Esercizio 4] Data l'equazione differenziale y' = 2y + e^(3x)/(e^x+1): a) trovare la "
    "soluzione generale; b) risolvere il problema di Cauchy y(0)=0.",
    r"y'=2y+\frac{e^{3x}}{e^x+1}",
    sp.Integer(-2), sp.exp(3 * x) / (sp.exp(x) + 1), -2 * x, sp.exp(-2 * x), 0, 0,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 1.5, 2.0], (-2, 2),
    normalizza=("Portiamo a sinistra il termine in y (P=-2 costante):", r"y'-2y=\frac{e^{3x}}{e^x+1}"),
    int_passi=[("Calcoliamo μ·Q = e^{-2x}·e^{3x}/(e^x+1) = e^x/(e^x+1), che è la derivata logaritmica del "
                "denominatore:", r"\int\frac{e^x}{e^x+1}dx=\ln(e^x+1)")],
    I=_log(sp.exp(x) + 1)))

_E1.append(_edo1_lineare(
    "dicembre 2024",
    "[dicembre 2024, Esercizio 5] Data l'equazione differenziale y' = -x/(x²+1)·y + 1/√(x²+1): a) trovare la "
    "soluzione generale; b) risolvere il problema di Cauchy y(0)=2.",
    r"y'=-\frac{x}{x^2+1}\,y+\frac{1}{\sqrt{x^2+1}}",
    x / (x**2 + 1), 1 / sp.sqrt(x**2 + 1), _log(x**2 + 1) / 2, sp.sqrt(x**2 + 1), 0, 2,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 2.0, 3.0], (-3, 3),
    normalizza=("Portiamo a sinistra il termine in y:", r"y'+\frac{x}{x^2+1}\,y=\frac{1}{\sqrt{x^2+1}}"),
    int_passi=[("Calcoliamo μ·Q = √(x²+1)·1/√(x²+1) = 1, il cui integrale è immediato:", r"\int1\,dx=x")],
    I=x))

# --- gennaio 2024, y' = xy + x^3 (soluzione generale) -------------------------------------------
_E1.append(_edo1_lineare(
    "gennaio 2024",
    "[gennaio 2024, Esercizio 1] Data l'equazione differenziale y' = xy + x³: a) classificarla e spiegare "
    "il perché della terminologia utilizzata; b) trovare la soluzione. (Il testo chiede la soluzione "
    "generale; per la verifica automatica scrivi la soluzione che soddisfa y(0)=0.)",
    r"y'=xy+x^3",
    -x, x**3, -x**2 / 2, sp.exp(-x**2 / 2), 0, 0,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 1.5, 2.0], (-2.5, 2.5),
    normalizza=("Portiamo a sinistra il termine in y (P(x)=-x):", r"y'-x\,y=x^3"),
    int_passi=[("Per ∫ x³·e^{-x²/2} dx si scrive x³=x²·x e si integra per parti (u=x², dv=x e^{-x²/2}dx ⇒ "
                "v=-e^{-x²/2}):",
                r"\int x^3e^{-x^2/2}dx=-x^2e^{-x^2/2}+2\int xe^{-x^2/2}dx=-(x^2+2)e^{-x^2/2}")],
    I=-(x**2 + 2) * sp.exp(-x**2 / 2), auto=True,
    sugg="Il testo chiede la soluzione generale: scrivi la soluzione con y(0)=0, es: -x**2-2+2*exp(x**2/2)"))

# --- settembre 2021, y' + y = sin x ---------------------------------------------------------------
_E1.append(_edo1_lineare(
    "settembre 2021",
    "[settembre 2021, Esercizio 10] Risolvere la seguente equazione differenziale ordinaria: y' + y = sin(x). "
    "(Il testo chiede la soluzione generale; per la verifica automatica scrivi la soluzione che soddisfa "
    "y(0)=0.)",
    r"y'+y=\sin x",
    sp.Integer(1), sp.sin(x), x, sp.exp(x), 0, 0,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 2.0, 3.0], (-1, 8),
    int_passi=[("Per ∫ e^x·sin x dx si integra per parti due volte (si ritrova lo stesso integrale a "
                "secondo membro e lo si porta a sinistra):",
                r"\int e^x\sin x\,dx=e^x\sin x-\int e^x\cos x\,dx=e^x\sin x-e^x\cos x-\int e^x\sin x\,dx"
                r"\ \Rightarrow\ \int e^x\sin x\,dx=\frac{e^x(\sin x-\cos x)}{2}")],
    I=sp.exp(x) * (sp.sin(x) - sp.cos(x)) / 2, auto=True,
    sugg="Il testo chiede la soluzione generale: scrivi la soluzione con y(0)=0, es: (sin(x)-cos(x))/2+exp(-x)/2"))


# --- BERNOULLI ---------------------------------------------------------------------------------
_E1.append(_edo1_bernoulli(
    "11 aprile 2026",
    "[11 aprile 2026, Esercizio 2] Risolvere la seguente equazione differenziale: x·y' = 4y - 2x²y². "
    "(Stesso testo di gennaio 2025, es. 11, dove si chiedeva anche la soluzione di Cauchy con y(1)=2: "
    "qui si risolve il problema di Cauchy con y(1)=2, che comprende la soluzione generale.)",
    r"x\,y'=4y-2x^2y^2",
    -4 / x, -2 * x, 2, -4 * _log(x), lambda t: 1 / t, 1, 2,
    [0.5, 1, 2, 3], [1.0, 1.5, 2.0, 3.0, 4.0], (0.3, 4),
    normalizza=("Dividiamo per x (x≠0) e portiamo a sinistra il termine in y per ottenere la forma "
                "y' + P(x)·y = Q(x)·y^n:", r"y'-\frac{4}{x}\,y=-2x\,y^2"),
    nota_dom="Il dato iniziale è in x=1>0: si lavora su x>0.",
    nota_sol="Si ricorda anche la soluzione costante y≡0, che era stata persa nella divisione per y^n."))

_E1.append(_edo1_bernoulli(
    "8 aprile 2026",
    "[8 aprile 2026, Esercizio 2] Risolvere la seguente equazione differenziale: y' - x·y = x·√y. "
    "(Il testo chiede la soluzione generale; per la verifica automatica scrivi la soluzione che soddisfa "
    "y(0)=4.)",
    r"y'-xy=x\sqrt{y}",
    -x, x, sp.Rational(1, 2), -x**2 / 2, lambda t: t**2, 0, 4,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 1.5, 2.0], (-2.5, 2.5),
    auto=True,
    sugg="Il testo chiede la soluzione generale: scrivi la soluzione con y(0)=4, es: (3*exp(x**2/4)-1)**2",
    nota_sol="(Con n=1/2>0 c'è anche la soluzione costante y≡0.) Si richiede t=√y≥0, cioè C·e^{x²/4}≥1.",
    int_passi=None))

_E1.append(_edo1_bernoulli(
    "9 maggio 2026",
    "[9 maggio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y' - 4y = 2e^x·√y, con y(0)=4.",
    r"y'-4y=2e^{x}\sqrt{y}",
    -4, 2 * sp.exp(x), sp.Rational(1, 2), -4 * x, lambda t: t**2, 0, 4,
    [-1, 0, 1, 2], [0, 0.5, 1.0, 1.5, 2.0], (-1, 2),
    nota_t_pos=("Controllo del segno: la sostituzione t=√y richiede t≥0. Qui t=e^x(3e^x-1)≥0 se e solo se "
                "x≥-ln 3, quindi la soluzione è valida (e il dato iniziale in x=0 è compreso) per x≥-ln 3.",
                r"t(x)=e^x\left(3e^x-1\right)\ge0\iff x\ge-\ln3")))

_E1.append(_edo1_bernoulli(
    "maggio 2025",
    "[maggio 2025, Esercizio 2] Risolvere la seguente equazione differenziale: y' = -(1+x)/(2x)·y + "
    "e^x/(2x)·y^(-1). (Il testo chiede la soluzione; per la verifica automatica scrivi la soluzione che "
    "soddisfa y(1)=1.)",
    r"y'=-\frac{1+x}{2x}\,y+\frac{e^{x}}{2x}\,y^{-1}",
    (1 + x) / (2 * x), sp.exp(x) / (2 * x), -1, _log(x) / 2 + x / 2, lambda t: sp.sqrt(t), 1, 1,
    [1, 1.5, 2, 3], [1.0, 1.5, 2.0, 2.5, 3.0], (1, 3.5),
    normalizza=("Portiamo a sinistra il termine in y: è un'equazione di Bernoulli con n=-1 (il termine y^{-1} "
                "è y^n con n=-1):", r"y'+\frac{1+x}{2x}\,y=\frac{e^x}{2x}\,y^{-1}"),
    auto=True, nota_dom="Si lavora su x>0.",
    sugg="Il testo chiede la soluzione: scrivi la soluzione con y(1)=1, es: sqrt((exp(2*x)/2+E-E**2/2)/(x*exp(x)))",
    nota_sol="Ramo positivo y=+√t (scelto perché y(1)>0); si richiede t>0."))

_E1.append(_edo1_bernoulli(
    "ottobre 2024",
    "[ottobre 2024, Esercizio 12] Data l'equazione differenziale y' = -(1+x)/(2x)·y - e^x/(2x)·y^(-1): "
    "a) trovare la soluzione generale; b) risolvere il problema di Cauchy y(1)=√e.",
    r"y'=-\frac{1+x}{2x}\,y-\frac{e^{x}}{2x}\,y^{-1}",
    (1 + x) / (2 * x), -sp.exp(x) / (2 * x), -1, _log(x) / 2 + x / 2, lambda t: sp.sqrt(t), 1, sp.sqrt(sp.E),
    [0.3, 0.6, 0.9], [0.2, 0.4, 0.6, 0.8, 1.0], (0.1, 1.3),
    normalizza=("Portiamo a sinistra il termine in y: Bernoulli con n=-1 (termine y^{-1}):",
                r"y'+\frac{1+x}{2x}\,y=-\frac{e^x}{2x}\,y^{-1}"),
    nota_dom="Si lavora su x>0.",
    nota_sol="Ramo positivo y=+√t (y(1)=√e>0). Serve t>0, cioè 3e²-e^{2x}>0, quindi x<1+(ln 3)/2.",
    nota_t_pos=("Controllo del segno: serve t>0 (altrimenti √t non è reale): t=(3e²-e^{2x})/(2x e^x)>0 se "
                "e^{2x}<3e², cioè x<1+(ln 3)/2≈1,55.", r"t>0\iff e^{2x}<3e^2\iff x<1+\tfrac{\ln3}{2}")))

_E1.append(_edo1_bernoulli(
    "6 dicembre 2025",
    "[6 dicembre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: y' = 2y - e^x·y², "
    "con y(1)=1.",
    r"y'=2y-e^{x}y^2",
    sp.Integer(-2), -sp.exp(x), 2, -2 * x, lambda t: 1 / t, 1, 1,
    [0.5, 1, 1.5, 2], [0.5, 1.0, 1.5, 2.0, 3.0], (0, 3),
    normalizza=("Portiamo a sinistra il termine in y: Bernoulli con n=2:", r"y'-2y=-e^{x}y^2"),
    nota_t_pos=("Controllo: la soluzione è y=1/t, definita dove t≠0; con C=e²(1-e/3)>0 si ha t=e^x/3+C e^{-2x}>0 "
                "per ogni x, quindi y è definita e positiva su tutto R.", r"C=e^2\left(1-\frac e3\right)>0\ \Rightarrow\ t(x)>0\ \ \forall x")))

_E1.append(_edo1_bernoulli(
    "13 dicembre 2025",
    "[13 dicembre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: "
    "y' = 2y·tg(x) + √y, con y(0)=1.",
    r"y'=2y\tan x+\sqrt{y}",
    -2 * sp.tan(x), sp.Integer(1), sp.Rational(1, 2), 2 * _log(sp.cos(x)), lambda t: t**2, 0, 1,
    [-0.5, 0, 0.5, 1.0], [-0.5, 0, 0.3, 0.6, 1.0, 1.3], (-1.2, 1.3),
    normalizza=("Portiamo a sinistra il termine in y: Bernoulli con n=1/2:", r"y'-2\tan x\cdot y=y^{1/2}"),
    nota_dom="Intorno a x=0 si ha cos x>0: A=-2∫tan x dx=2 ln(cos x).",
    nota_sol="(Con n=1/2>0 c'è anche la soluzione costante y≡0.) Si richiede t=√y≥0.",
    nota_t_pos=("Controllo del segno: t=(2+sin x)/(2cos x)>0 per x∈(-π/2,π/2): la soluzione è valida su "
                "tutto l'intervallo in cui cos x>0.", r"t=\frac{2+\sin x}{2\cos x}>0\ \text{ per }\ x\in\left(-\tfrac\pi2,\tfrac\pi2\right)")))

_E1.append(_edo1_bernoulli(
    "ottobre 2024",
    "[ottobre 2024, Esercizio 3] Data l'equazione differenziale y' = -(1/x)·y - (2/x²)·y²: a) trovare la "
    "soluzione generale; b) risolvere il problema di Cauchy y(1)=2.",
    r"y'=-\frac{1}{x}\,y-\frac{2}{x^2}\,y^2",
    1 / x, -2 / x**2, 2, _log(x), lambda t: 1 / t, 1, 2,
    [0.9, 1, 2, 3], [1.0, 1.5, 2.0, 3.0, 4.0], (0.85, 4),
    normalizza=("Portiamo a sinistra il termine in y: Bernoulli con n=2:", r"y'+\frac{1}{x}\,y=-\frac{2}{x^2}\,y^2"),
    nota_dom="Il dato iniziale è in x=1>0: si lavora su x>0.",
    nota_sol="Si ricorda anche la soluzione costante y≡0."))

_E1.append(_edo1_bernoulli(
    "ottobre 2024",
    "[ottobre 2024, Esercizio 6] Data l'equazione differenziale y' = (1/x)·y - y³: a) trovare la soluzione "
    "generale; b) risolvere il problema di Cauchy y(1)=√3.",
    r"y'=\frac{1}{x}\,y-y^3",
    -1 / x, sp.Integer(-1), 3, -_log(x), lambda t: 1 / sp.sqrt(t), 1, sp.sqrt(3),
    [1, 1.2, 2, 3], [1.0, 1.2, 1.5, 2.0, 3.0], (0.85, 4),
    normalizza=("Portiamo a sinistra il termine in y: Bernoulli con n=3:", r"y'-\frac{1}{x}\,y=-y^3"),
    nota_dom="Il dato iniziale è in x=1>0: si lavora su x>0.",
    nota_sol="Con t=y^{-2}>0 si ha y=±1/√t: si sceglie il ramo + perché y(1)=√3>0. Si ricorda anche y≡0.",
    nota_t_pos=("Controllo: t=(2x³-1)/(3x²)>0 se x³>1/2, cioè x>2^{-1/3}≈0,79: la soluzione è valida lì "
                "(include x=1).", r"t>0\iff x>2^{-1/3}")))

_E1.append(_edo1_bernoulli(
    "aprile 2025",
    "[aprile 2025, Esercizio 2] Dato il problema di Cauchy y' = y - e^x·√y, con y(0)=1: a) trovare la "
    "soluzione generale dell'equazione differenziale; b) trovare la soluzione del problema di Cauchy.",
    r"y'=y-e^{x}\sqrt{y}",
    sp.Integer(-1), -sp.exp(x), sp.Rational(1, 2), -x, lambda t: t**2, 0, 1,
    [-1, 0, 0.5, 1], [-1, -0.5, 0, 0.5, 1.0, 1.3], (-1.5, 1.4),
    normalizza=("Portiamo a sinistra il termine in y: Bernoulli con n=1/2:", r"y'-y=-e^{x}y^{1/2}"),
    nota_sol="(Con n=1/2>0 c'è anche la soluzione costante y≡0.) Si richiede t=√y≥0.",
    nota_t_pos=("Controllo del segno: t=2e^{x/2}-e^x=e^{x/2}(2-e^{x/2})≥0 se e^{x/2}≤2, cioè x≤2ln 2≈1,39: "
                "la soluzione è valida per x≤2 ln 2 (per x>2 ln 2 si dovrebbe prendere il ramo negativo, "
                "non ammesso).", r"t\ge0\iff e^{x/2}\le2\iff x\le2\ln2")))


# --- SEPARABILI (soluzioni scritte a mano, tutte verificate per sostituzione) ----------------------
def _sep_voce(fonte, testo, testo_latex, passi, sol, F, x0, y0, xs_check, xs_camp, xs_graf, sugg=None):
    return _fin1(fonte, testo, testo_latex, passi, sol, F, x0, y0, xs_check, xs_camp, xs_graf, sugg)


def _s1():
    # 15 maggio 2026 (= 7 maggio 2026, maggio 2025): y' = (1-e^-y)/(2x+1), y(0)=2
    sol = _log(1 + (sp.exp(2) - 1) * sp.sqrt(2 * x + 1))
    tl = r"y'=\frac{1-e^{-y}}{2x+1},\quad y(0)=2"
    passi = [
        _passo("Equazione:", tl),
        _passo("Classificazione: è un'equazione differenziale a VARIABILI SEPARABILI, y' = g(x)·h(y), con "
               "g(x)=1/(2x+1) e h(y)=1-e^{-y}.", r"y'=g(x)\,h(y),\quad g(x)=\frac{1}{2x+1},\ h(y)=1-e^{-y}"),
        _passo("Passo 1 — soluzioni costanti (stazionarie): si cercano gli zeri di h(y). Qui h(y)=0 ⇔ y=0, "
               "ma il dato iniziale y(0)=2 non vi appartiene: la soluzione cercata non è costante e si può "
               "dividere per h(y) (variabili separabili, formulario sez. 14.2).",
               r"1-e^{-y}=0\iff y=0\quad(\ne2)"),
        _passo("Passo 2 — separiamo le variabili (y a sinistra, x a destra), valido dove h(y)≠0:",
               r"\frac{dy}{1-e^{-y}}=\frac{dx}{2x+1}"),
        _passo("Passo 3 — riscriviamo il primo membro moltiplicando numeratore e denominatore per e^y; "
               "si riconosce la derivata logaritmica di e^y-1 (calcolando i due integrali):",
               r"\frac{1}{1-e^{-y}}=\frac{e^{y}}{e^{y}-1}\ \Rightarrow\ \int\frac{e^{y}}{e^{y}-1}dy=\ln|e^{y}-1|,"
               r"\qquad\int\frac{dx}{2x+1}=\frac12\ln|2x+1|"),
        _passo("Uguagliando le primitive (variabili separabili; costante arbitraria c):",
               r"\ln|e^{y}-1|=\tfrac12\ln|2x+1|+c"),
        _passo("Passo 4 — passando agli esponenziali (K=±e^c≠0) si ottiene la soluzione generale in forma "
               "implicita, poi esplicita:",
               r"e^{y}-1=K\sqrt{2x+1}\ \Rightarrow\ y(x)=\ln\left(1+K\sqrt{2x+1}\right)"),
        _passo("Passo 5 — condizione iniziale: imponendo y(0)=2 (e^{2}-1=K·1):",
               r"e^{2}-1=K\sqrt{1}\ \Rightarrow\ K=e^{2}-1"),
        _passo("Soluzione del problema di Cauchy (definita per 2x+1>0, cioè x>-1/2, perché il dato iniziale "
               "è in x=0):", r"y(x)=\ln\left(1+(e^{2}-1)\sqrt{2x+1}\right)"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale: y(0)=ln(1+e²-1)=2, e "
               "derivando e^{y}=1+(e²-1)√(2x+1) si ottiene e^{y}y'=(e²-1)/√(2x+1), e questo coincide con "
               "(e^y-1)/(2x+1) perché e^y-1=(e²-1)√(2x+1):",
               r"y'=\frac{e^{2}-1}{e^{y}\sqrt{2x+1}}=\frac{e^{y}-1}{e^{y}(2x+1)}=\frac{1-e^{-y}}{2x+1}\ \checkmark"),
    ]
    F = lambda s_: sp.diff(s_, x) - (1 - sp.exp(-s_)) / (2 * x + 1)
    return _sep_voce(
        "15 maggio 2026",
        "[15 maggio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y' = (1-e^(-y))/(2x+1), "
        "con y(0)=2. (Lo stesso testo compare il 7 maggio 2026 e a maggio 2025.)",
        tl, passi, sol, F, 0, 2, [-0.3, 0, 0.5, 2], [-0.4, 0, 0.5, 1.0, 2.0, 3.0], (-0.45, 4))


_E1.append(_s1())


def _s2():
    # gennaio 2025 es. 17: y' = x(y+1)/(y(x-1)), y(2)=1  (soluzione implicita)
    xs_ = x
    yv = sp.Symbol('y')
    rhs_imp = xs_ + _log(xs_ - 1) - 1 - _log(2)

    def y_num(xv):
        # y - ln(y+1) = RHS(x), ramo y>0 (quello che contiene il dato iniziale y(2)=1)
        f = sp.lambdify(yv, yv - _log(yv + 1) - rhs_imp.subs(xs_, xv), 'mpmath')
        import mpmath as mp
        return float(mp.findroot(lambda t: t - mp.log(t + 1) - float(rhs_imp.subs(xs_, xv)), 1.0 + 1.5 * (xv - 2)))

    val3 = y_num(3.0)
    tl = r"y'=\frac{x(y+1)}{y(x-1)},\quad y(2)=1"
    passi = [
        _passo("Equazione:", tl),
        _passo("Classificazione: è a VARIABILI SEPARABILI, y' = g(x)·h(y) con g(x)=x/(x-1) e h(y)=(y+1)/y.",
               r"y'=\frac{x}{x-1}\cdot\frac{y+1}{y}"),
        _passo("Passo 1 — variabili separabili, soluzioni costanti: h(y)=0 ⇔ y=-1, che non passa per il dato iniziale y(2)=1; "
               "inoltre y≠0 (h non definita) e x≠1. Intorno al dato iniziale (x=2, y=1) si ha x>1, y>0.",
               r"\frac{y+1}{y}=0\iff y=-1\ (\ne1)"),
        _passo("Passo 2 — separiamo le variabili (y a sinistra, x a destra):",
               r"\frac{y}{y+1}\,dy=\frac{x}{x-1}\,dx"),
        _passo("Passo 3 — calcolando i due integrali: si riscrive ciascun integrando con una divisione "
               "(y/(y+1)=1-1/(y+1) e x/(x-1)=1+1/(x-1)):",
               r"\int\left(1-\frac{1}{y+1}\right)dy=y-\ln|y+1|,\qquad\int\left(1+\frac{1}{x-1}\right)dx=x+\ln|x-1|"),
        _passo("Soluzione generale in forma IMPLICITA (costante c arbitraria; non si può esplicitare y con "
               "funzioni elementari):", r"y-\ln|y+1|=x+\ln|x-1|+c"),
        _passo("Passo 4 — condizione iniziale: imponendo y(2)=1 si ricava c:",
               r"1-\ln2=2+\ln1+c\ \Rightarrow\ c=-1-\ln2"),
        _passo("Soluzione del problema di Cauchy, in forma implicita (con x>1, y>0):",
               r"y-\ln(y+1)=x+\ln(x-1)-1-\ln2"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale: derivando implicitamente rispetto a x si ritrova l'equazione; "
               "il dato iniziale è soddisfatto perché per x=2, y=1 i due membri valgono 1-ln 2. Valore "
               "numerico utile (x=3 ⇒ y-ln(y+1)=2):",
               r"y'\left(1-\frac{1}{y+1}\right)=1+\frac{1}{x-1}\ \Rightarrow\ y'\,\frac{y}{y+1}=\frac{x}{x-1}\ \checkmark"
               r"\qquad y(3)\approx" + ("%.4f" % val3)),
    ]
    # verifica numerica per sostituzione nell'equazione (derivata implicita)
    import mpmath as mp
    for xv in (2.5, 3.0, 4.0):
        yy = y_num(xv)
        yp = xv * (yy + 1) / (yy * (xv - 1))
        h = 1e-6
        yy2 = y_num(xv + h)
        assert abs((yy2 - yy) / h - yp) < 1e-4
    assert abs(y_num(2.0) - 1.0) < 1e-12
    return _voce(
        "gennaio 2025",
        "[gennaio 2025, Esercizio 17] Data l'equazione differenziale y' = x(y+1)/(y(x-1)): a) trovare la "
        "soluzione generale; b) trovare la soluzione nel caso y(2)=1. (La soluzione è in forma implicita: "
        "per la verifica automatica scrivi il valore numerico di y(3).)",
        tl, "Scrivi il valore numerico di y(3), con almeno 3 cifre decimali (si risolve numericamente y-ln(y+1)=2).",
        passi, {"tipo": "numero", "atteso_numero": val3, "atteso_display": "%.4f" % val3},
        _fig_implicito())


def _fig_implicito():
    try:
        import mpmath as mp
        xs_ = np.linspace(1.05, 5, 120)
        ys_ = []
        for xv in xs_:
            try:
                ys_.append(float(mp.findroot(lambda t: t - mp.log(t + 1) - (xv + mp.log(xv - 1) - 1 - mp.log(2)),
                                              1.0 + 1.5 * (xv - 2) if xv > 1.3 else 0.5)))
            except Exception:
                ys_.append(np.nan)
        fig, ax = plt.subplots(figsize=(6, 4.4))
        ax.plot(xs_, ys_, linewidth=2, color='#2e5c8a')
        ax.plot(2, 1, 'ro', markersize=7, label="y(2)=1")
        ax.set_xlabel('x'); ax.set_ylabel('y')
        ax.set_title("Soluzione (ramo y>0 dell'equazione implicita)", fontsize=10)
        ax.legend(fontsize=8); ax.grid(alpha=0.3); fig.tight_layout()
        return _png(fig)
    except Exception:
        plt.close('all')
        return None


_E1.append(_s2())


def _s3():
    # maggio 2024: y' = 6x^2 (1-7e^-y), y(0)=ln 8
    sol = _log(7 + sp.exp(2 * x**3))
    tl = r"y'=6x^2\left(1-7e^{-y}\right),\quad y(0)=\ln8"
    passi = [
        _passo("Equazione:", tl),
        _passo("Classificazione: è a VARIABILI SEPARABILI, y'=g(x)h(y) con g(x)=6x² e h(y)=1-7e^{-y}.",
               r"g(x)=6x^2,\qquad h(y)=1-7e^{-y}"),
        _passo("Passo 1 — variabili separabili, soluzioni costanti: h(y)=0 ⇔ e^{-y}=1/7 ⇔ y=ln 7. Il dato iniziale y(0)=ln 8≠ln 7 "
               "non vi appartiene, quindi si può dividere per h(y) (formulario, variabili separabili).",
               r"1-7e^{-y}=0\iff y=\ln7\quad(\ne\ln8)"),
        _passo("Passo 2 — separiamo le variabili:", r"\frac{dy}{1-7e^{-y}}=6x^2\,dx"),
        _passo("Passo 3 — calcolando i due integrali: a sinistra si moltiplica per e^y (derivata logaritmica "
               "di e^y-7); a destra è una potenza:",
               r"\frac{1}{1-7e^{-y}}=\frac{e^{y}}{e^{y}-7}\ \Rightarrow\ \ln|e^{y}-7|=2x^3+c"),
        _passo("Passo 4 — condizione iniziale: imponendo y(0)=ln 8 si ricava c (e^{ln8}-7=1):",
               r"\ln|8-7|=0+c\ \Rightarrow\ c=0"),
        _passo("Esponenziando (e^y-7>0 intorno al dato iniziale, perché 8-7=1>0) e isolando y:",
               r"e^{y}-7=e^{2x^3}\ \Rightarrow\ y(x)=\ln\left(7+e^{2x^3}\right)"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale: y(0)=ln(7+1)=ln 8; derivando, y'=6x²e^{2x³}/(7+e^{2x³}) e "
               "6x²(1-7e^{-y})=6x²(1-7/(7+e^{2x³}))=6x²e^{2x³}/(7+e^{2x³}) ✓. (Attenzione: la soluzione "
               "stampata nel PDF, ln(7+2x³), è un refuso: la corretta è ln(7+e^{2x³}).)",
               r"y'=\frac{6x^2e^{2x^3}}{7+e^{2x^3}}=6x^2\left(1-\frac{7}{7+e^{2x^3}}\right)\ \checkmark"),
    ]
    F = lambda s_: sp.diff(s_, x) - 6 * x**2 * (1 - 7 * sp.exp(-s_))
    return _sep_voce(
        "maggio 2024",
        "[maggio 2024, Esercizio 2] Data l'equazione differenziale y' = 6x²(1-7e^(-y)): a) trovare la "
        "soluzione generale; b) risolvere il problema di Cauchy y(0)=ln 8. (Nota: la soluzione stampata nel "
        "PDF, ln(7+2x³), è un refuso.)",
        tl, passi, sol, F, 0, _log(8), [-1, 0, 0.5, 1], [-1, -0.5, 0, 0.5, 1.0, 1.5], (-1.5, 1.5))


_E1.append(_s3())


def _s4():
    # dicembre 2024 es. 6: e^(2y-x) y' = 1, y(0) = (1/2) ln 2
    sol = (x + _log(2)) / 2
    tl = r"e^{2y-x}\,y'=1,\quad y(0)=\tfrac12\ln2"
    passi = [
        _passo("Equazione:", tl),
        _passo("Classificazione: è a VARIABILI SEPARABILI: isolando y' si ha y' = e^{x-2y} = e^{x}·e^{-2y}.",
               r"y'=e^{x-2y}=e^{x}\cdot e^{-2y}"),
        _passo("Passo 1 — variabili separabili: nessuna soluzione costante da escludere (h(y)=e^{-2y}>0 mai nulla). "
               "Passo 2 — separiamo le variabili:", r"e^{2y}\,dy=e^{x}\,dx"),
        _passo("Passo 3 — calcolando i due integrali:", r"\frac12e^{2y}=e^{x}+c"),
        _passo("Soluzione generale (costante c arbitraria): esplicitando y (serve 2e^x+2c>0):",
               r"e^{2y}=2e^{x}+2c\ \Rightarrow\ y(x)=\frac12\ln\left(2e^{x}+2c\right)"),
        _passo("Passo 4 — condizione iniziale: imponendo y(0)=½ ln 2 (e^{2y(0)}=2):",
               r"2=2e^{0}+2c\ \Rightarrow\ c=0"),
        _passo("Soluzione del problema di Cauchy: con c=0, y=½ ln(2e^x)=½(ln 2 + x):",
               r"y(x)=\frac12\ln\left(2e^{x}\right)=\frac{x+\ln2}{2}"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale: y'=1/2 e e^(2y-x)=e^(ln 2)=2, quindi e^(2y-x)·y'=2·½=1 ✓; "
               "y(0)=½ ln 2 ✓.", r"e^{2y-x}\,y'=e^{\ln2}\cdot\frac12=1\ \checkmark"),
    ]
    F = lambda s_: sp.exp(2 * s_ - x) * sp.diff(s_, x) - 1
    return _sep_voce(
        "dicembre 2024",
        "[dicembre 2024, Esercizio 6] Data l'equazione differenziale e^(2y-x)·y' = 1: a) trovare la "
        "soluzione generale; b) risolvere il problema di Cauchy y(0)=(1/2)·ln 2.",
        tl, passi, sol, F, 0, _log(2) / 2, [-1, 0, 1, 2], [-1, 0, 0.5, 1.0, 2.0, 3.0], (-2, 4))


_E1.append(_s4())


def _s5():
    # ottobre 2023: (1+e^{2x}) y' = e^{2x} y, y(0)=1
    sol = sp.sqrt((1 + sp.exp(2 * x)) / 2)
    tl = r"(1+e^{2x})\,y'=e^{2x}y,\quad y(0)=1"
    passi = [
        _passo("Equazione:", tl),
        _passo("Classificazione: dividendo per 1+e^{2x}>0 si ha y' = e^{2x}/(1+e^{2x})·y: è a VARIABILI "
               "SEPARABILI (e anche lineare omogenea), con g(x)=e^{2x}/(1+e^{2x}) e h(y)=y.",
               r"y'=\frac{e^{2x}}{1+e^{2x}}\,y"),
        _passo("Passo 1 — variabili separabili, soluzione costante y≡0 (h(y)=y=0): non passa per il dato iniziale y(0)=1, quindi "
               "y≠0 e si può dividere per y (y>0 vicino a y(0)=1).", r"h(y)=y=0\iff y=0\quad(\ne1)"),
        _passo("Passo 2 — separiamo le variabili:", r"\frac{dy}{y}=\frac{e^{2x}}{1+e^{2x}}\,dx"),
        _passo("Passo 3 — calcolando i due integrali (a destra il numeratore è metà della derivata del "
               "denominatore):", r"\ln|y|=\frac12\ln\left(1+e^{2x}\right)+c"),
        _passo("Soluzione generale (K=±e^c): y(x)=K√(1+e^{2x}).", r"y(x)=K\sqrt{1+e^{2x}}"),
        _passo("Passo 4 — condizione iniziale: imponendo y(0)=1:", r"1=K\sqrt{2}\ \Rightarrow\ K=\frac{1}{\sqrt2}"),
        _passo("Soluzione del problema di Cauchy:", r"y(x)=\sqrt{\frac{1+e^{2x}}{2}}"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale: y'=e^{2x}/(√2√(1+e^{2x})) e (1+e^{2x})y' = e^{2x}√(1+e^{2x})/√2 = "
               "e^{2x}y ✓; y(0)=1 ✓.", r"(1+e^{2x})y'=\frac{e^{2x}\sqrt{1+e^{2x}}}{\sqrt2}=e^{2x}y\ \checkmark"),
    ]
    F = lambda s_: (1 + sp.exp(2 * x)) * sp.diff(s_, x) - sp.exp(2 * x) * s_
    return _sep_voce(
        "ottobre 2023",
        "[ottobre 2023, Esercizio 1] Risolvere il seguente problema di Cauchy: (1+e^(2x))·y' = e^(2x)·y, "
        "con y(0)=1.",
        tl, passi, sol, F, 0, 1, [-1, 0, 1, 2], [-2, -1, 0, 0.5, 1.0, 2.0], (-3, 3))


_E1.append(_s5())


def _s6():
    # settembre 2021 es. 9: y' = (1-y)(2-y) x ; per la verifica y(0)=0
    E = sp.exp(x**2 / 2)
    sol = 2 * (E - 1) / (2 * E - 1)
    tl = r"y'=(1-y)(2-y)\,x,\quad y(0)=0\ \ (\text{condizione scelta per la verifica})"
    passi = [
        _passo("Equazione (il testo d'esame chiede solo la soluzione generale; per la verifica automatica "
               "fissiamo y(0)=0):", tl),
        _passo("Classificazione: è a VARIABILI SEPARABILI, y'=g(x)h(y) con g(x)=x e h(y)=(1-y)(2-y).",
               r"g(x)=x,\qquad h(y)=(1-y)(2-y)"),
        _passo("Passo 1 — variabili separabili, soluzioni costanti: h(y)=0 ⇔ y=1 oppure y=2 (sono soluzioni dell'equazione). Il "
               "nostro dato iniziale y(0)=0 non è né 1 né 2, quindi (per l'unicità) la soluzione cercata sta "
               "nella striscia y<1 e si può dividere per h(y).", r"y\equiv1,\quad y\equiv2\ \text{(soluzioni stazionarie)}"),
        _passo("Passo 2 — separiamo le variabili:", r"\frac{dy}{(1-y)(2-y)}=x\,dx"),
        _passo("Passo 3 — calcolando i due integrali: a sinistra si usano i fratti semplici "
               "1/((1-y)(2-y)) = 1/(1-y) - 1/(2-y):",
               r"\int\left(\frac{1}{1-y}-\frac{1}{2-y}\right)dy=-\ln|1-y|+\ln|2-y|=\ln\left|\frac{2-y}{1-y}\right|,"
               r"\qquad\int x\,dx=\frac{x^2}{2}"),
        _passo("Soluzione generale in forma implicita, poi esplicita (K=±e^c):",
               r"\frac{2-y}{1-y}=Ke^{x^2/2}\ \Rightarrow\ 2-y=Ke^{x^2/2}(1-y)\ \Rightarrow\ "
               r"y(x)=\frac{Ke^{x^2/2}-2}{Ke^{x^2/2}-1}"),
        _passo("Passo 4 — condizione iniziale: imponendo y(0)=0 (K=(2-0)/(1-0)=2):",
               r"\frac{2-0}{1-0}=Ke^{0}\ \Rightarrow\ K=2"),
        _passo("Soluzione: da (2-y)=2e^{x²/2}(1-y) si ricava y(2e^{x²/2}-1)=2e^{x²/2}-2:",
               r"y(x)=\frac{2\left(e^{x^2/2}-1\right)}{2e^{x^2/2}-1}"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale: y(0)=0 ✓, e il residuo y'-(1-y)(2-y)x è nullo (controllato con "
               "sympy).", r"y'-(1-y)(2-y)\,x\equiv0\ \checkmark"),
    ]
    F = lambda s_: sp.diff(s_, x) - (1 - s_) * (2 - s_) * x
    return _sep_voce(
        "settembre 2021",
        "[settembre 2021, Esercizio 9] Risolvere la seguente equazione differenziale ordinaria: "
        "y' = (1-y)(2-y)·x. (Il testo chiede la soluzione generale; per la verifica automatica scrivi la "
        "soluzione che soddisfa y(0)=0.)",
        tl, passi, sol, F, 0, 0, [-1, 0, 0.5, 1], [-2, -1, 0, 0.5, 1.0, 2.0], (-3, 3),
        sugg="Scrivi la soluzione con y(0)=0, es: 2*(exp(x**2/2)-1)/(2*exp(x**2/2)-1)")


_E1.append(_s6())


# ===========================================================================
# DATI: EDO 2° ORDINE
# ===========================================================================
_E2 = ESAME["edo"]
_sin1 = lambda: T(r"\sin x", 1, 0, 1, 'sin', txt="sin(x)")
_cos1 = lambda: T(r"\cos x", 1, 0, 1, 'cos', txt="cos(x)")
_R = sp.Rational
_pi = sp.pi

# --- 9 aprile 2026 (= 2 dicembre 2025 con Cauchy; gennaio 2024, dicembre 2024) -----------------------
_E2.append(_edo2(
    "9 aprile 2026",
    "[9 aprile 2026, Esercizio 2] Risolvere la seguente equazione differenziale: y'' + y = x² + sin(x). "
    "(Lo stesso testo compare il 2 dicembre 2025 con il problema di Cauchy y(0)=-3, y'(π)=1/2 — le due "
    "condizioni sono in punti DIVERSI — e in gennaio 2024 / dicembre 2024 come ricerca dell'integrale "
    "generale: qui si risolve anche il problema di Cauchy.)",
    (1, 0, 1), r"x^2+\sin x",
    [T("x^2", x**2, txt="x²"), _sin1()],
    conds=[(0, 0, -3), (_pi, 1, _R(1, 2))],
    nota_cond="Passo 3 — condizioni iniziali del problema di Cauchy (assegnate in due punti diversi: y in x=0 e "
              "y' in x=π): si impongono sull'integrale completo; serve la derivata y'.",
    xs_graf=(-1, 7)))

# --- 14 maggio 2026 (= ottobre 2023): y'' + y' = x - x^3 --------------------------------------------
_E2.append(_edo2(
    "14 maggio 2026",
    "[14 maggio 2026, Esercizio 2] Risolvere la seguente equazione differenziale: y'' + y' = x - x³. "
    "(Stesso testo di ottobre 2023, es. 2.)",
    (1, 1, 0), r"x-x^3",
    [T("x-x^3", x - x**3, txt="x - x³")]))

# --- 16 maggio 2026 (= maggio 2025): y'' + y = 5 e^x cos x ------------------------------------------
_E2.append(_edo2(
    "16 maggio 2026",
    "[16 maggio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' + y = 5e^x·cos(x), con "
    "y(0)=1, y'(0)=1. (Stesso testo di maggio 2025. Attenzione: l'esponente è e^x, non e^{2x}.)",
    (1, 0, 1), r"5e^{x}\cos x",
    [T(r"5e^{x}\cos x", 5, 1, 1, 'cos', txt="5e^x·cos(x)")],
    conds=[(0, 0, 1), (0, 1, 1)]))

# --- gennaio 2026 --------------------------------------------------------------------------------------
_E2.append(_edo2(
    "24 gennaio 2026",
    "[24 gennaio 2026, Esercizio 2] Dato il problema di Cauchy y'' + 2y' + y = (x² + 3x - 1)·e^(-x), con "
    "y(0)=1, y'(0)=1: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la "
    "soluzione del problema di Cauchy.",
    (1, 2, 1), r"(x^2+3x-1)e^{-x}",
    [T(r"(x^2+3x-1)e^{-x}", x**2 + 3 * x - 1, -1, txt="(x²+3x-1)e^(-x)")],
    conds=[(0, 0, 1), (0, 1, 1)]))

_E2.append(_edo2(
    "21 gennaio 2026",
    "[21 gennaio 2026, Esercizio 2] Dato il problema di Cauchy y'' - 10y' + 25y = (x² - 2)·e^(5x), con "
    "y(0)=1, y'(0)=1: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la "
    "soluzione del problema di Cauchy.",
    (1, -10, 25), r"(x^2-2)e^{5x}",
    [T(r"(x^2-2)e^{5x}", x**2 - 2, 5, txt="(x²-2)e^(5x)")],
    conds=[(0, 0, 1), (0, 1, 1)]))

_E2.append(_edo2(
    "20 gennaio 2026",
    "[20 gennaio 2026, Esercizio 2] Dato il problema di Cauchy y'' + 4y' + 3y = (x² - 1)·e^(-3x), con "
    "y(0)=0, y'(0)=0: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la "
    "soluzione del problema di Cauchy.",
    (1, 4, 3), r"(x^2-1)e^{-3x}",
    [T(r"(x^2-1)e^{-3x}", x**2 - 1, -3, txt="(x²-1)e^(-3x)")],
    conds=[(0, 0, 0), (0, 1, 0)]))

_E2.append(_edo2(
    "19 gennaio 2026",
    "[19 gennaio 2026, Esercizio 2] Dato il problema di Cauchy y'' + 2y' + 2y = e^(-x)·cos(x) + 3x, con "
    "y(0)=0, y'(0)=0: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la "
    "soluzione del problema di Cauchy.",
    (1, 2, 2), r"e^{-x}\cos x+3x",
    [T(r"e^{-x}\cos x", 1, -1, 1, 'cos', txt="e^(-x)·cos(x)"), T("3x", 3 * x, txt="3x")],
    conds=[(0, 0, 0), (0, 1, 0)]))

_E2.append(_edo2(
    "16 gennaio 2026",
    "[16 gennaio 2026, Esercizio 2] (testo riletto dal PDF; il PDF riporta «y'' - 2y' + 5 = e^x sin x», con "
    "la y mancante: si interpreta come y'' - 2y' + 5y) Dato il problema di Cauchy y'' - 2y' + 5y = "
    "e^x·sin(x), con y(0)=1, y'(0)=1: a) trovare la soluzione generale; b) trovare la soluzione del "
    "problema di Cauchy.",
    (1, -2, 5), r"e^{x}\sin x",
    [T(r"e^{x}\sin x", 1, 1, 1, 'sin', txt="e^x·sin(x)")],
    conds=[(0, 0, 1), (0, 1, 1)]))

# --- dicembre 2025 -------------------------------------------------------------------------------------
_E2.append(_edo2(
    "9 dicembre 2025",
    "[9 dicembre 2025, Esercizio 2] Dato il problema di Cauchy y'' + 5y' + 6y = e^(-2x) + 6x², con y(0)=1, "
    "y'(0)=1: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del "
    "problema di Cauchy. (Stesso testo del 3 dicembre 2025.)",
    (1, 5, 6), r"e^{-2x}+6x^2",
    [T("e^{-2x}", 1, -2, txt="e^(-2x)"), T("6x^2", 6 * x**2, txt="6x²")],
    conds=[(0, 0, 1), (0, 1, 1)]))

_E2.append(_edo2(
    "5 dicembre 2025",
    "[5 dicembre 2025, Esercizio 2] Determinare l'unica soluzione del seguente problema di Cauchy: "
    "y'' + y' - 2y = -e^x, con y(0)=0, y'(0)=0.",
    (1, 1, -2), r"-e^{x}",
    [T("-e^{x}", -1, 1, txt="-e^x")],
    conds=[(0, 0, 0), (0, 1, 0)]))

_E2.append(_edo2(
    "1 dicembre 2025",
    "[1 dicembre 2025, Esercizio 2] Dato il problema di Cauchy y'' - 2y' + 5y = e^x·cos(3x), con y(0)=1, "
    "y'(0)=1: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del "
    "problema di Cauchy. (Stesso testo di aprile 2025.)",
    (1, -2, 5), r"e^{x}\cos 3x",
    [T(r"e^{x}\cos 3x", 1, 1, 3, 'cos', txt="e^x·cos(3x)")],
    conds=[(0, 0, 1), (0, 1, 1)]))

# --- settembre 2025 ------------------------------------------------------------------------------------
_E2.append(_edo2(
    "15 settembre 2025",
    "[15 settembre 2025, Esercizio 2] Determinare l'unica soluzione del seguente problema di Cauchy: "
    "y'' - 3y' + 2y = e^(2x)(3x + 1), con y(0)=2, y'(0)=3. (La stessa equazione compare in gennaio 2025, "
    "es. 14, e in maggio 2024, es. 3, con richiesta di omogenea associata e soluzione generale.)",
    (1, -3, 2), r"e^{2x}(3x+1)",
    [T(r"e^{2x}(3x+1)", 3 * x + 1, 2, txt="(3x+1)e^(2x)")],
    conds=[(0, 0, 2), (0, 1, 3)]))

_E2.append(_edo2(
    "17 settembre 2025",
    "[17 settembre 2025, Esercizio 2] Determinare l'unica soluzione del seguente problema di Cauchy: "
    "y'' + 3y' + 2y = x² + e^x, con y(0)=0, y'(0)=1. (Stessa equazione e stesse condizioni di luglio 2024, "
    "es. 2.)",
    (1, 3, 2), r"x^2+e^{x}",
    [T("x^2", x**2, txt="x²"), T("e^{x}", 1, 1, txt="e^x")],
    conds=[(0, 0, 0), (0, 1, 1)]))

_E2.append(_edo2(
    "18 settembre 2025",
    "[18 settembre 2025, Esercizio 2] Determinare l'unica soluzione del seguente problema di Cauchy: "
    "y'' + 4y = x²·e^(-x), con y(0)=3/125, y'(0)=-3/125. (Stesso testo di luglio 2024, es. 4.)",
    (1, 0, 4), r"x^2e^{-x}",
    [T("x^2e^{-x}", x**2, -1, txt="x²e^(-x)")],
    conds=[(0, 0, _R(3, 125)), (0, 1, -_R(3, 125))]))

_E2.append(_edo2(
    "20 settembre 2025",
    "[20 settembre 2025, Esercizio 2] Determinare l'unica soluzione del seguente problema di Cauchy: "
    "y'' + y' - 2y = 2x + e^(-x), con y(0)=1, y'(0)=1/2.",
    (1, 1, -2), r"2x+e^{-x}",
    [T("2x", 2 * x, txt="2x"), T("e^{-x}", 1, -1, txt="e^(-x)")],
    conds=[(0, 0, 1), (0, 1, _R(1, 2))]))

# --- ottobre 2025 --------------------------------------------------------------------------------------
_E2.append(_edo2(
    "29 ottobre 2025",
    "[29 ottobre 2025, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' + 4y' + 8y = 2x + 1, "
    "con y(0)=0, y'(0)=π/4.",
    (1, 4, 8), r"2x+1",
    [T("2x+1", 2 * x + 1, txt="2x+1")],
    conds=[(0, 0, 0), (0, 1, _pi / 4)], xs_graf=(0, 5)))

_E2.append(_edo2(
    "25 ottobre 2025",
    "[25 ottobre 2025, Esercizio 2] (testo riletto dal PDF) Risolvere il seguente problema di Cauchy: "
    "y'' - y' - 2y = -3e^(-x) - 2e^x, con y(0)=0, y'(0)=3. (Attenzione: gli esponenti sono e^{-x} ed e^{x}; "
    "solo il primo termine è in risonanza.)",
    (1, -1, -2), r"-3e^{-x}-2e^{x}",
    [T("-3e^{-x}", -3, -1, txt="-3e^(-x)"), T("-2e^{x}", -2, 1, txt="-2e^x")],
    conds=[(0, 0, 0), (0, 1, 3)]))

_E2.append(_edo2(
    "22 ottobre 2025",
    "[22 ottobre 2025, Esercizio 2] Risolvere la seguente equazione differenziale: "
    "y'' + 6y' + 8y = e^(2x) + √π·x². (Il testo chiede la soluzione generale.)",
    (1, 6, 8), r"e^{2x}+\sqrt{\pi}\,x^2",
    [T("e^{2x}", 1, 2, txt="e^(2x)"), T(r"\sqrt{\pi}\,x^2", sp.sqrt(_pi) * x**2, txt="√π·x²")]))

_E2.append(_edo2(
    "21 ottobre 2025",
    "[21 ottobre 2025, Esercizio 2] Determinare l'unica soluzione del seguente problema di Cauchy: "
    "y'' - y' - 2y = sin(2x), con y(0)=0, y'(0)=1.",
    (1, -1, -2), r"\sin 2x",
    [T(r"\sin 2x", 1, 0, 2, 'sin', txt="sin(2x)")],
    conds=[(0, 0, 0), (0, 1, 1)]))

# --- aprile 2025 ---------------------------------------------------------------------------------------
_E2.append(_edo2(
    "aprile 2025",
    "[aprile 2025, Esercizio 2] Dato il problema di Cauchy y'' + 3y' - 4y = e^x + x, con y(0)=1/20, y'(0)=0: "
    "a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del problema "
    "di Cauchy.",
    (1, 3, -4), r"e^{x}+x",
    [T("e^{x}", 1, 1, txt="e^x"), T("x", x, txt="x")],
    conds=[(0, 0, _R(1, 20)), (0, 1, 0)]))

_E2.append(_edo2(
    "aprile 2025",
    "[aprile 2025, Esercizio 2] Dato il problema di Cauchy y'' - 6y' + 10y = 9e^(3x)·sin(x), con y(0)=0, "
    "y'(0)=1: a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del "
    "problema di Cauchy. (Risonanza: 3+i è radice dell'equazione caratteristica.)",
    (1, -6, 10), r"9e^{3x}\sin x",
    [T(r"9e^{3x}\sin x", 9, 3, 1, 'sin', txt="9e^(3x)·sin(x)")],
    conds=[(0, 0, 0), (0, 1, 1)]))

# --- maggio 2025 ---------------------------------------------------------------------------------------
_E2.append(_edo2(
    "maggio 2025",
    "[maggio 2025, Esercizio 2] Dato il problema di Cauchy y'' - 2y' + y = x·e^x, con y(0)=0, y'(0)=1: "
    "a) trovare la soluzione generale dell'equazione differenziale; b) trovare la soluzione del problema "
    "di Cauchy. (Stesso testo di dicembre 2023, es. 3, e luglio 2023, es. 12.)",
    (1, -2, 1), r"x\,e^{x}",
    [T(r"x\,e^{x}", x, 1, txt="x·e^x")],
    conds=[(0, 0, 0), (0, 1, 1)]))

_E2.append(_edo2(
    "maggio 2025",
    "[maggio 2025, Esercizio 2] Risolvere la seguente equazione differenziale: y'' - 9y = (12x - 4)·e^(3x). "
    "(Il testo chiede la soluzione generale.)",
    (1, 0, -9), r"(12x-4)e^{3x}",
    [T(r"(12x-4)e^{3x}", 12 * x - 4, 3, txt="(12x-4)e^(3x)")]))

# --- ottobre 2024 --------------------------------------------------------------------------------------
_E2.append(_edo2(
    "ottobre 2024",
    "[ottobre 2024, Esercizio 18] Data l'equazione differenziale y'' + 2y' + 5y = e^(-x)·cos(2x): a) "
    "trovare la soluzione generale; b) risolvere il problema di Cauchy y(0)=1, y'(0)=0. (Risonanza: -1+2i è "
    "radice dell'equazione caratteristica.)",
    (1, 2, 5), r"e^{-x}\cos 2x",
    [T(r"e^{-x}\cos 2x", 1, -1, 2, 'cos', txt="e^(-x)·cos(2x)")],
    conds=[(0, 0, 1), (0, 1, 0)]))

_E2.append(_edo2(
    "ottobre 2024",
    "[ottobre 2024, Esercizio 19] Data l'equazione differenziale y'' + 2y' + 6y = e^(-x)·sin(2x): a) "
    "trovare la soluzione generale; b) risolvere il problema di Cauchy y(0)=1, y'(0)=0. (Radici "
    "-1±i√5: NON c'è risonanza perché α+iβ=-1+2i non coincide con -1+i√5.)",
    (1, 2, 6), r"e^{-x}\sin 2x",
    [T(r"e^{-x}\sin 2x", 1, -1, 2, 'sin', txt="e^(-x)·sin(2x)")],
    conds=[(0, 0, 1), (0, 1, 0)]))

# --- luglio 2024 -----------------------------------------------------------------------------------------
_E2.append(_edo2(
    "luglio 2024",
    "[luglio 2024, Esercizio 1] Data l'equazione differenziale y'' + 4y' + 5y = e^(2x)·cos(x): a) "
    "classificarla; b) trovare la soluzione dell'omogenea associata; c) trovare la soluzione generale.",
    (1, 4, 5), r"e^{2x}\cos x",
    [T(r"e^{2x}\cos x", 1, 2, 1, 'cos', txt="e^(2x)·cos(x)")],
    classifica_extra="(Punto a del testo: classificazione.)"))

_E2.append(_edo2(
    "luglio 2024",
    "[luglio 2024, Esercizio 3] Data l'equazione differenziale y'' + 3y' + 2y = x²·e^x: a) trovare la "
    "soluzione dell'omogenea associata; b) trovare la soluzione generale; c) risolvere il problema di Cauchy "
    "y(0)=-2/27, y'(0)=-23/27.",
    (1, 3, 2), r"x^2e^{x}",
    [T(r"x^2e^{x}", x**2, 1, txt="x²e^x")],
    conds=[(0, 0, -_R(2, 27)), (0, 1, -_R(23, 27))]))

# --- aprile 2024 -----------------------------------------------------------------------------------------
_E2.append(_edo2(
    "aprile 2024",
    "[aprile 2024, Esercizio 1] Data l'equazione differenziale y'' - y = x·e^(2x): a) trovare la soluzione "
    "dell'omogenea associata; b) trovare la soluzione particolare e l'integrale generale; c) calcolare la "
    "soluzione del problema di Cauchy y(0)=0, y'(0)=0.",
    (1, 0, -1), r"x\,e^{2x}",
    [T(r"x\,e^{2x}", x, 2, txt="x·e^(2x)")],
    conds=[(0, 0, 0), (0, 1, 0)]))

_E2.append(_edo2(
    "aprile 2024",
    "[aprile 2024, Esercizio 2] Data l'equazione differenziale y'' + 6y' + 9 = 4e^x (così stampata nel PDF, "
    "con la costante 9 e senza y: la soluzione stampata è coerente con questa lettura, cioè y'' + 6y' = "
    "4e^x - 9): a) trovare la soluzione dell'omogenea associata; b) trovare la particolare e l'integrale "
    "generale; c) calcolare la soluzione del problema di Cauchy y(0)=0, y'(0)=1.",
    (1, 6, 0), r"4e^{x}-9",
    [T("4e^{x}", 4, 1, txt="4e^x"), T("-9", -9, txt="-9 (costante)")],
    conds=[(0, 0, 0), (0, 1, 1)],
    classifica_extra="Nota: portando 9 a destra, il secondo membro è 4e^x - 9 e il coefficiente di y è 0."))

_E2.append(_edo2(
    "aprile 2024",
    "[aprile 2024, Esercizio 3] Data l'equazione differenziale y'' + y' = x + 2: a) trovare la soluzione "
    "dell'omogenea associata; b) trovare la particolare e l'integrale generale; c) calcolare la soluzione "
    "del problema di Cauchy y(0)=0, y'(0)=2.",
    (1, 1, 0), r"x+2",
    [T("x+2", x + 2, txt="x+2")],
    conds=[(0, 0, 0), (0, 1, 2)]))

_E2.append(_edo2(
    "aprile 2024",
    "[aprile 2024, Esercizio 4] Data l'equazione differenziale y'' + y = -3e^x·sin(x): a) trovare la "
    "soluzione dell'omogenea associata; b) trovare la particolare e l'integrale generale; c) calcolare la "
    "soluzione del problema di Cauchy y(0)=0, y'(π)=0 (condizioni in punti diversi).",
    (1, 0, 1), r"-3e^{x}\sin x",
    [T(r"-3e^{x}\sin x", -3, 1, 1, 'sin', txt="-3e^x·sin(x)")],
    conds=[(0, 0, 0), (_pi, 1, 0)], xs_graf=(-1, 5),
    nota_cond="Passo 3 — condizioni iniziali (y in x=0, y' in x=π): si impongono sull'integrale completo; "
              "serve la derivata y'."))

_E2.append(_edo2(
    "aprile 2024",
    "[aprile 2024, Esercizio 6] Data l'equazione differenziale y'' + 4y' = x - 1: a) trovare la soluzione "
    "dell'omogenea associata; b) trovare la particolare e l'integrale generale; c) calcolare la soluzione "
    "del problema di Cauchy y(0)=0, y'(π)=0 (come stampato nel PDF; la soluzione stampata nel PDF, "
    "y = 21/64 - (21/64)e^(-4x) + x²/8 - 5x/16, corrisponde invece a y'(0)=1: probabile refuso).",
    (1, 4, 0), r"x-1",
    [T("x-1", x - 1, txt="x-1")],
    conds=[(0, 0, 0), (_pi, 1, 0)], xs_graf=(-1, 5),
    nota_cond="Passo 3 — condizioni iniziali (y in x=0, y' in x=π, come stampato): si impongono sull'integrale "
              "completo; serve la derivata y'."))

# --- maggio 2024 -----------------------------------------------------------------------------------------
_E2.append(_edo2(
    "maggio 2024",
    "[maggio 2024, Esercizio 1] Data l'equazione differenziale y'' - 6y' + 9y = 4x·e^(3x): a) trovare la "
    "soluzione dell'omogenea associata; b) trovare la particolare e l'integrale generale.",
    (1, -6, 9), r"4x\,e^{3x}",
    [T(r"4x\,e^{3x}", 4 * x, 3, txt="4x·e^(3x)")]))

_E2.append(_edo2(
    "maggio 2024",
    "[maggio 2024, Esercizio 4] Data l'equazione differenziale y'' + 2y' + y = 2x²: a) trovare la "
    "soluzione dell'omogenea associata; b) trovare la particolare e l'integrale generale; c) calcolare la "
    "soluzione del problema di Cauchy y(0)=12, y'(0)=0.",
    (1, 2, 1), r"2x^2",
    [T("2x^2", 2 * x**2, txt="2x²")],
    conds=[(0, 0, 12), (0, 1, 0)]))

# --- gennaio 2025 ----------------------------------------------------------------------------------------
_E2.append(_edo2(
    "gennaio 2025",
    "[gennaio 2025, Esercizio 20] Data l'equazione differenziale y'' + 49y = cos(x): a) trovare la "
    "soluzione dell'omogenea associata; b) trovare la soluzione generale; c) trovare la soluzione nel caso "
    "y(0)=1/48, y'(0)=7.",
    (1, 0, 49), r"\cos x",
    [_cos1()],
    conds=[(0, 0, _R(1, 48)), (0, 1, 7)]))

# --- gennaio 2024 ----------------------------------------------------------------------------------------
_E2.append(_edo2(
    "gennaio 2024",
    "[gennaio 2024, Esercizio 2] Data l'equazione differenziale y'' - 3y' + 2y = x²: a) classificarla e "
    "spiegare il perché della terminologia utilizzata; b) trovare la soluzione dell'omogenea associata; "
    "c) trovare la soluzione particolare della non omogenea.",
    (1, -3, 2), r"x^2",
    [T("x^2", x**2, txt="x²")]))

_E2.append(_edo2(
    "gennaio 2024",
    "[gennaio 2024, Esercizio 4] Data l'equazione differenziale y'' + 4y' + 4y = e^(-2x): a) classificarla; "
    "b) trovare la soluzione dell'omogenea associata; c) trovare la soluzione particolare della non "
    "omogenea (doppia risonanza).",
    (1, 4, 4), r"e^{-2x}",
    [T("e^{-2x}", 1, -2, txt="e^(-2x)")]))

# --- dicembre 2023 ---------------------------------------------------------------------------------------
_E2.append(_edo2(
    "dicembre 2023",
    "[dicembre 2023, Esercizio 1] Risolvere il seguente problema di Cauchy: 4y'' + 9y = 5·sin(x), con "
    "y(0)=0, y'(0)=5/2. (Coefficiente 4 davanti a y'': si divide per 4 nell'equazione caratteristica.)",
    (4, 0, 9), r"5\sin x",
    [T(r"5\sin x", 5, 0, 1, 'sin', txt="5 sin(x)")],
    conds=[(0, 0, 0), (0, 1, _R(5, 2))], xs_graf=(0, 8)))

_E2.append(_edo2(
    "dicembre 2023",
    "[dicembre 2023, Esercizio 4] Risolvere il seguente problema di Cauchy: 2y'' - 5y' + 2y = 3x·e^(2x), "
    "con y(0)=1, y'(0)=3.",
    (2, -5, 2), r"3x\,e^{2x}",
    [T(r"3x\,e^{2x}", 3 * x, 2, txt="3x·e^(2x)")],
    conds=[(0, 0, 1), (0, 1, 3)]))

# --- luglio 2023 -----------------------------------------------------------------------------------------
_E2.append(_edo2(
    "luglio 2023",
    "[luglio 2023, Esercizio 15] Risolvere il seguente problema di Cauchy: 2y'' - 5y' + 2y = 3e^(2x), con "
    "y(0)=1, y'(0)=3.",
    (2, -5, 2), r"3e^{2x}",
    [T(r"3e^{2x}", 3, 2, txt="3e^(2x)")],
    conds=[(0, 0, 1), (0, 1, 3)]))

_E2.append(_edo2(
    "luglio 2023",
    "[luglio 2023, Esercizio 3] Risolvere il seguente problema di Cauchy: y'' + 2y' + y = x² + 3x - 1, con "
    "y(0)=1, y'(0)=3.",
    (1, 2, 1), r"x^2+3x-1",
    [T("x^2+3x-1", x**2 + 3 * x - 1, txt="x²+3x-1")],
    conds=[(0, 0, 1), (0, 1, 3)]))

_E2.append(_edo2(
    "luglio 2023",
    "[luglio 2023, Esercizio 6] Risolvere la seguente equazione differenziale: y'' + y = 3·cos(x) "
    "(risonanza: ±i sono le radici).",
    (1, 0, 1), r"3\cos x",
    [T(r"3\cos x", 3, 0, 1, 'cos', txt="3cos(x)")]))

_E2.append(_edo2(
    "luglio 2023",
    "[luglio 2023, Esercizio 9] Risolvere la seguente equazione differenziale: y'' + y' - 2y = 3e^(-2x) "
    "(risonanza semplice: -2 è una radice).",
    (1, 1, -2), r"3e^{-2x}",
    [T(r"3e^{-2x}", 3, -2, txt="3e^(-2x)")]))

# --- ottobre 2023 (= luglio 2021, es. 3) -----------------------------------------------------------------
_E2.append(_edo2(
    "ottobre 2023",
    "[ottobre 2023, Esercizio 3] Risolvere la seguente equazione differenziale: y'' - y' - 2y = 2e^(-x). "
    "(Stesso testo di luglio 2021, es. 3.)",
    (1, -1, -2), r"2e^{-x}",
    [T(r"2e^{-x}", 2, -1, txt="2e^(-x)")]))

_E2.append(_edo2(
    "ottobre 2023",
    "[ottobre 2023, Esercizio 4] Risolvere la seguente equazione differenziale: y'' + 4y' = x - cos(2x).",
    (1, 4, 0), r"x-\cos 2x",
    [T("x", x, txt="x"), T(r"-\cos 2x", -1, 0, 2, 'cos', txt="-cos(2x)")]))

# --- dicembre 2021 ---------------------------------------------------------------------------------------
_E2.append(_edo2(
    "dicembre 2021",
    "[dicembre 2021, Esercizio 3] Risolvere il seguente problema di Cauchy: y'' + 4y' + 8y = 2x + 1, con "
    "y(0)=0, y'(π)=π/4 (condizioni in punti diversi).",
    (1, 4, 8), r"2x+1",
    [T("2x+1", 2 * x + 1, txt="2x+1")],
    conds=[(0, 0, 0), (_pi, 1, _pi / 4)], xs_graf=(0, 5),
    nota_cond="Passo 3 — condizioni iniziali (y in x=0, y' in x=π): si impongono sull'integrale completo; "
              "serve la derivata y'."))

_E2.append(_edo2(
    "dicembre 2021",
    "[dicembre 2021, Esercizio 5] Risolvere il seguente problema di Cauchy: y'' + 2y' + 5y = e^(-x), con "
    "y(0)=1, y'(0)=0.",
    (1, 2, 5), r"e^{-x}",
    [T("e^{-x}", 1, -1, txt="e^(-x)")],
    conds=[(0, 0, 1), (0, 1, 0)]))

_E2.append(_edo2(
    "dicembre 2021",
    "[dicembre 2021, Esercizio 7] Risolvere la seguente equazione differenziale ordinaria: "
    "y'' - y' - 6y = x·e^(-3x).",
    (1, -1, -6), r"x\,e^{-3x}",
    [T(r"x\,e^{-3x}", x, -3, txt="x·e^(-3x)")]))

_E2.append(_edo2(
    "dicembre 2021",
    "[dicembre 2021, Esercizio 11] Risolvere il seguente problema di Cauchy: y'' - y' - 6y = -e^(4x) + 6, "
    "con y(0)=0, y'(0)=1/3.",
    (1, -1, -6), r"-e^{4x}+6",
    [T("-e^{4x}", -1, 4, txt="-e^(4x)"), T("6", 6, txt="6 (costante)")],
    conds=[(0, 0, 0), (0, 1, _R(1, 3))]))

# --- settembre 2021 --------------------------------------------------------------------------------------
_E2.append(_edo2(
    "settembre 2021",
    "[settembre 2021, Esercizio 11] Risolvere la seguente equazione differenziale ordinaria: "
    "y'' + y' + (1/4)·y = cos(x). (Radice doppia -1/2.)",
    (1, 1, _R(1, 4)), r"\cos x",
    [_cos1()]))

_E2.append(_edo2(
    "settembre 2021",
    "[settembre 2021, Esercizio 12] Risolvere il seguente problema di Cauchy: y'' + 9y = 3·sin(x), con "
    "y(0)=2, y'(0)=6.",
    (1, 0, 9), r"3\sin x",
    [T(r"3\sin x", 3, 0, 1, 'sin', txt="3sin(x)")],
    conds=[(0, 0, 2), (0, 1, 6)], xs_graf=(0, 8)))


def _bern_zero():
    # aprile 2025: y' = 2y - x sqrt(y), y(0)=0 -> unica soluzione y == 0 (caso 'trabocchetto')
    tl = r"y'=2y-x\sqrt{y},\quad y(0)=0"
    passi = [
        _passo("Equazione:", tl),
        _passo("Classificazione: è un'equazione di Bernoulli, y' + P(x)·y = Q(x)·y^n, con P=-2, Q=-x e "
               "esponente n=1/2 (il termine √y è y^{1/2}):", r"y'-2y=-x\,y^{1/2}"),
        _passo("Passo 1 — Bernoulli: per y>0 si divide per y^{1/2} e si pone la sostituzione t=y^{1-n}=y^{1/2}=√y, "
               "così t'=y^{-1/2}y'/2:", r"t=\sqrt{y},\quad y=t^2,\quad y'=2t\,t'\ \Rightarrow\ 2t\,t'-2t^2=-x\,t"),
        _passo("Passo 2 — Bernoulli: dividendo per 2t (t≠0) si ottiene un'equazione LINEARE in t:",
               r"t'-t=-\frac{x}{2}"),
        _passo("Passo 3 — Bernoulli, lineare in t: fattore integrante μ=e^{-x}, (μ t)'=-(x/2)e^{-x}; "
               "integrando per parti ∫x e^{-x}dx=-(x+1)e^{-x}:",
               r"\left(e^{-x}t\right)'=-\frac{x}{2}e^{-x}\ \Rightarrow\ e^{-x}t=\frac{(x+1)e^{-x}}{2}+C"
               r"\ \Rightarrow\ t(x)=\frac{x+1}{2}+Ce^{x}"),
        _passo("Passo 4 — Bernoulli, condizione iniziale: y(0)=0 equivale a t(0)=0; imponendola:",
               r"t(0)=\frac12+C=0\ \Rightarrow\ C=-\frac12\ \Rightarrow\ t(x)=\frac{x+1-e^{x}}{2}"),
        _passo("ATTENZIONE (trabocchetto): t=√y deve essere ≥0, ma per la disuguaglianza e^x≥1+x si ha "
               "t(x)=(x+1-e^x)/2≤0 per ogni x, con t=0 SOLO in x=0. Quindi la funzione y=t² NON è soluzione "
               "dell'equazione: infatti √y=|t|=-t e si trova y'=2t t'=2t²-x t=2y+x√y≠2y-x√y se x≠0.",
               r"\sqrt{y}=|t|=-t\ \Rightarrow\ y'=2y+x\sqrt{y}\ne2y-x\sqrt{y}\quad(x\ne0)"),
        _passo("Passo 5 — la soluzione costante y≡0 (persa nella divisione per y^{1/2}) invece verifica "
               "l'equazione e il dato iniziale. Unicità: per x<0 il secondo membro 2y-x√y=2y+|x|√y è ≥0, "
               "quindi y è non decrescente e, con y≥0 e y(0)=0, resta y≡0 per x≤0; per x>0 vicino a y=0 si ha "
               "y'≈-x√y<0, quindi y non può diventare positiva. L'unica soluzione è:",
               r"y(x)\equiv0"),
        _passo("Verifica per sostituzione nell'equazione e nella condizione iniziale:",
               r"y'=0,\quad 2y-x\sqrt{y}=0\ \Rightarrow\ 0=0,\qquad y(0)=0\ \checkmark"),
    ]
    F = lambda s_: sp.diff(s_, x) - 2 * s_ + x * sp.sqrt(s_)
    return _fin1(
        "aprile 2025",
        "[aprile 2025, Esercizio 2] Dato il problema di Cauchy y' = 2y - x·√y, con y(0)=0: a) trovare la "
        "soluzione generale dell'equazione differenziale; b) trovare la soluzione del problema di Cauchy. "
        "(Occhio al trabocchetto: la formula del metodo di Bernoulli non dà una soluzione ammissibile.)",
        tl, passi, sp.Integer(0), F, 0, 0, [-1, -0.5, 0, 0.5, 1], [-1, -0.5, 0, 0.5, 1.0, 2.0], (-2, 2),
        sugg="Scrivi y(x) (la soluzione è costante), es: 0")


_E1.append(_bern_zero())
