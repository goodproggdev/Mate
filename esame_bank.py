# -*- coding: utf-8 -*-
"""
Banco 'Esame': problemi presi da veri appelli d'esame di Metodi Matematici per
l'Ingegneria (Uninettuno), estratti dai testi ufficiali (Ottobre 2025, Dicembre 2025,
Gennaio 2026, Aprile 2026, Maggio 2026) forniti dall'utente. Ogni voce e' stata
risolta e verificata simbolicamente con sympy prima di essere inclusa qui (i calcoli
di verifica sono stati eseguiti a parte; qui restano solo enunciato, soluzione e
spiegazione gia' pronti). A differenza del banco procedurale, questi esercizi sono
scritti a mano uno per uno (non generati da un pool), perche' ciascuno riproduce un
problema specifico e non parametrico.

Copertura: non tutti i ~90 esercizi individuati nelle 6 dispense sono stati inclusi
(molti erano danneggiati dall'estrazione OCR delle formule, specialmente le funzioni
a tratti di 'continuita'); questa e' una selezione di quelli che si sono potuti
decifrare e verificare con sicurezza, rappresentativa dello stile e della difficolta'
di ciascun argomento. Taylor non ha problemi reali (non compare in nessun appello
trovato) e Serie non ha, per ora, esempi reali sufficientemente leggibili.
"""
import io
import base64

import sympy as sp
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import numpy as np

import multivariabile as _mv
import grafico as _grafico
import edo as _edo
import continuita_differenziabilita as _cd

x, y = sp.symbols('x y')


def _passo(testo, latex=None):
    return {"testo": testo, "latex": latex}


def _tex(v):
    return sp.latex(v)


def _png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=105, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def _voce(fonte, testo, testo_latex, suggerimento, passi, risposta, grafico_png=None):
    return {
        "testo": testo, "testo_latex": testo_latex, "suggerimento": suggerimento,
        "passi": passi, "grafico_png": grafico_png, "risposta": risposta, "fonte": fonte,
    }


ESAME = {"serie": [], "taylor": [], "lagrange": [], "punti_liberi": [], "edo": [],
          "edo1": [], "integrali": [], "continuita": []}

# ---------------------------------------------------------------------------
# LAGRANGE (1 problema: 18 ottobre 2025, Esercizio 1)
# ---------------------------------------------------------------------------

def _lagrange_1():
    f = x - y**2 + 2*x**2
    g = x**2 + y**2 + 2*x
    # punti e moltiplicatori lambda (verificati con sympy: sistema di Lagrange risolto a parte)
    punti = [(-sp.Rational(1,2), -sp.sqrt(3)/2, sp.Rational(-3,4)),
             (-sp.Rational(1,2),  sp.sqrt(3)/2, sp.Rational(-3,4)),
             (sp.Integer(0), sp.Integer(0), sp.Integer(0)),
             (sp.Integer(-2), sp.Integer(0), sp.Integer(6))]
    lambdas = [sp.Integer(-1), sp.Integer(-1), sp.Rational(1,2), sp.Rational(7,2)]
    classificazioni = [_mv._classifica_hessiana_orlata(f, g, px, py, lv)
                        for (px, py, _), lv in zip(punti, lambdas)]
    testo = ("[18 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = x - y^2 + 2x^2 soggetta al "
             "vincolo g(x,y) = x^2 + y^2 + 2x = 0: a) disegnare il vincolo descrivendone le "
             "caratteristiche; b) determinare gli eventuali punti di massimo e di minimo utilizzando "
             "il metodo dei moltiplicatori di Lagrange e la matrice Hessiana orlata.")
    testo_latex = (r"f(x,y) = x - y^2 + 2x^2,\quad g(x,y) = x^2+y^2+2x = 0")
    passi = [
        _passo("Il vincolo g(x,y)=0 riscritto completando il quadrato:",
               r"x^2+2x+y^2=0 \iff (x+1)^2+y^2=1"),
        _passo("È una circonferenza di centro (-1,0) e raggio 1: chiusa e limitata (compatta).", None),
        _passo("Sistema di Lagrange: gradiente(f) = lambda*gradiente(g), g=0.",
               r"1+4x=\lambda(2x+2),\quad -2y=\lambda(2y),\quad (x+1)^2+y^2=1"),
        _passo("Risolvendo il sistema si trovano 4 punti stazionari, con il relativo moltiplicatore "
               "lambda e il valore di f:", None),
    ]
    for (px, py, val), lv in zip(punti, lambdas):
        passi.append(_passo("", f"(x,y)=({_tex(px)}, {_tex(py)}),\\ \\lambda={_tex(lv)}"
                              f"\\ \\Rightarrow\\ f={_tex(val)}"))
    passi.append(_passo("Classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto "
                         "L=f-\\lambda g,",
                         r"\overline{H}=\begin{pmatrix}0&g_x'&g_y'\\g_x'&L_{xx}''&L_{xy}''\\"
                         r"g_y'&L_{yx}''&L_{yy}''\end{pmatrix},\ \ \overline{H}>0\Rightarrow\text{max rel.},"
                         r"\ \overline{H}<0\Rightarrow\text{min rel.}"))
    for (px, py, val), lv, cl in zip(punti, lambdas, classificazioni):
        passi.append(_passo("", f"(x,y)=({_tex(px)}, {_tex(py)}):\\quad \\det\\overline{{H}}="
                              f"{_tex(cl['det'])}\\ \\Rightarrow\\ \\textbf{{{cl['tipo']}}}"))
    passi.append(_passo("Il vincolo è compatto: per Weierstrass f ammette massimo e minimo assoluto "
                         "(confrontando TUTTI i valori di f nei punti stazionari, anche quelli "
                         "relativi):",
                         r"\max f = 6 \text{ in } (-2,0), \qquad \min f = -\tfrac34 \text{ in } "
                         r"(-\tfrac12,\pm\tfrac{\sqrt3}{2})"))

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(-1+np.cos(theta), np.sin(theta), color='#c0392b', linewidth=2, label="vincolo: (x+1)²+y²=1")
    for px, py, val in punti:
        pxf, pyf = float(px), float(py)
        ax.plot(pxf, pyf, 'ko', markersize=7)
        ax.annotate(f"f={val}", (pxf, pyf), textcoords="offset points", xytext=(7, 7), fontsize=8)
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.legend(loc='upper right', fontsize=8)
    ax.set_title("Vincolo (circonferenza) e punti stazionari")
    fig.tight_layout()
    png = _png(fig)

    risposta = {"tipo": "punti_valore",
                "punti_attesi": [[float(p[0]), float(p[1]), float(p[2])] for p in punti],
                "valore_max": 6.0, "valore_min": -0.75}
    return _voce("18 ottobre 2025", testo, testo_latex,
                 "Un punto per riga, formato x,y (es: -2,0).", passi, risposta, png)


ESAME["lagrange"].append(_lagrange_1())
# ---------------------------------------------------------------------------
# PUNTI STAZIONARI LIBERI (4 problemi)
# ---------------------------------------------------------------------------
def _punti_liberi_generico(fonte, testo, f_expr, nota_extra=None):
    grad = [sp.diff(f_expr, v) for v in (x, y)]
    pts_grezzi = sp.solve(grad, [x, y], dict=True)
    classificazioni = _mv._classifica_punti_critici(f_expr, pts_grezzi)
    hess = sp.hessian(f_expr, (x, y))

    testo_latex = r"f(x,y) = " + _tex(sp.expand(f_expr) if f_expr.is_polynomial(x, y) else f_expr)
    passi = [_passo("Funzione:", testo_latex)]
    passi.append(_passo("Passo 1 — annulliamo il gradiente per trovare i punti stazionari:",
                         _tex(grad[0]) + "=0,\\quad" + _tex(grad[1]) + "=0"))
    passi.append(_passo("Passo 2 — matrice Hessiana:", "H(x,y) = " + _tex(hess)))
    for c in classificazioni:
        px, py = c["punto"]
        H = hess.subs({x: px, y: py})
        passi.append(_passo(f"Punto ({_tex(px)}, {_tex(py)}):",
                             "H=" + _tex(H) + r",\ \det H=" + _tex(H.det())
                             + r",\ \mathrm{tr}\,H=" + _tex(H.trace())
                             + r"\ \Rightarrow\ \textbf{" + c["tipo"].upper() + "}"))
    if nota_extra:
        passi.append(_passo(nota_extra, None))

    es_fake = {"f": f_expr, "classificazioni": classificazioni}
    try:
        fig = _grafico.grafico_punto_critico(es_fake)
        png = _png(fig)
    except Exception:
        png = None

    attesi = [[float(c["punto"][0]), float(c["punto"][1]), c["tipo"]] for c in classificazioni]
    risposta = {"tipo": "punti_classificati", "attesi": attesi}
    return _voce(fonte, testo, testo_latex,
                 "Un punto per riga, formato x,y,tipo (es: 0,0,minimo).", passi, risposta, png)


ESAME["punti_liberi"].append(_punti_liberi_generico(
    "22 ottobre 2025",
    "[22 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = xy·e^(-(x²+y²)), determinare gli "
    "eventuali punti di massimo e di minimo utilizzando la matrice Hessiana.",
    x*y*sp.exp(-(x**2+y**2))))

ESAME["punti_liberi"].append(_punti_liberi_generico(
    "23 ottobre 2025",
    "[23 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = (x-y)·e^(-(x²+y²)), determinare gli "
    "eventuali punti di massimo e di minimo utilizzando la matrice Hessiana.",
    (x-y)*sp.exp(-(x**2+y**2))))

ESAME["punti_liberi"].append(_punti_liberi_generico(
    "16 gennaio 2026",
    "[16 gennaio 2026, Esercizio 1] Data la funzione f(x,y) = x^3 + 3xy^2 - 15x - 12y, studiare la "
    "natura dei punti stazionari.",
    x**3 + 3*x*y**2 - 15*x - 12*y))

ESAME["punti_liberi"].append(_punti_liberi_generico(
    "17 gennaio 2026",
    "[17 gennaio 2026, Esercizio 1] Data la funzione f(x,y) = (y-3x²)(y-x²), studiare il segno e "
    "rappresentarlo graficamente; studiare la natura dei punti stazionari.",
    (y - 3*x**2)*(y - x**2),
    nota_extra=("Attenzione: qui l'Hessiano nell'origine ha determinante nullo (caso indeterminato). "
                "Lungo OGNI retta y=mx per l'origine, f(x,mx)=x^2(mx-3x)(mx-x) ha il segno di x^2 "
                "vicino a 0 (quindi sembra un minimo). Ma lungo la parabola y=2x^2 si ha "
                "f(x,2x^2)=(2x^2-3x^2)(2x^2-x^2)=-x^4<0: la funzione è NEGATIVA vicino all'origine "
                "lungo questo cammino. Quindi (0,0) NON è un minimo locale, nonostante lo sembri "
                "lungo ogni retta: è un punto stazionario che l'Hessiano da solo non basta a "
                "classificare, e il test lungo le rette è fuorviante (classico controesempio).")))
# ---------------------------------------------------------------------------
# EDO 2° ORDINE / CAUCHY (6 problemi)
# ---------------------------------------------------------------------------
def _edo2_generico(fonte, testo, a, b, forzante_tex, forzante, y0, y1, ansatz_passi=None):
    Y = sp.Function('y')
    eq = sp.Eq(Y(x).diff(x, 2) + a*Y(x).diff(x) + b*Y(x), forzante)
    sol_gen = sp.dsolve(eq, Y(x))
    sol = sp.dsolve(eq, Y(x), ics={Y(0): y0, Y(x).diff(x).subs(x, 0): y1})

    r = sp.symbols('r')
    radici = sp.solve(sp.Eq(r**2 + a*r + b, 0), r)
    def _termine(coeff, simbolo):
        if coeff == 0:
            return ""
        segno = "+" if coeff > 0 else "-"
        c = abs(coeff)
        cifra = "" if c == 1 else str(c)
        return f"{segno}{cifra}{simbolo}"

    testo_latex = ("y''" + _termine(a, "y'") + _termine(b, "y") + "=" + forzante_tex
                   + r",\quad y(0)=" + _tex(y0) + r",\ y'(0)=" + _tex(y1))
    passi = [_passo("Equazione:", testo_latex)]
    passi.append(_passo("Passo 1 — equazione caratteristica:",
                         f"r^2+{a}r+{b}=0 \\Rightarrow " + _tex(radici)))
    if ansatz_passi:
        passi.append(_passo("Passo 2 — forma della soluzione particolare (metodo di somiglianza, "
                             "dal formulario): per ogni termine del termine noto, verifichiamo se "
                             "coincide con una radice dell'equazione caratteristica (risonanza):",
                             None))
        passi.extend(ansatz_passi)
    passi.append(_passo("Soluzione generale (omogenea + particolare, sovrapponendo eventuali più "
                         "termini del termine noto):",
                         "y(x)=" + _tex(sol_gen.rhs)))
    passi.append(_passo("Passo 3 — imponendo le condizioni iniziali:",
                         "y(x)=" + _tex(sol.rhs)))

    es_fake = {"soluzione_attesa": sol, "y0": y0}
    try:
        fig = _grafico.grafico_edo(es_fake)
        png = _png(fig)
    except Exception:
        png = None

    punti_x = [0.0, 0.3, 0.6, 1.0, 1.5, 2.0]
    campioni = []
    for xv in punti_x:
        try:
            val = complex(sol.rhs.subs(x, xv).evalf())
            if abs(val.imag) < 1e-8:
                campioni.append([xv, float(val.real)])
        except Exception:
            pass
    risposta = {"tipo": "funzione_su_campioni", "campioni": campioni}
    return _voce(fonte, testo, testo_latex, "Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)",
                 passi, risposta, png)


ESAME["edo"].append(_edo2_generico(
    "25 ottobre 2025",
    "[25 ottobre 2025, Esercizio 2] Risolvere il seguente problema di Cauchy: "
    "y'' - y' - 2y = -3e^(2x) - 2e^(-x), con y(0)=0, y'(0)=3. (doppia risonanza: entrambi i "
    "termini forzanti coincidono con le due radici dell'equazione caratteristica)",
    -1, -2, r"-3e^{2x}-2e^{-x}", -3*sp.exp(2*x)-2*sp.exp(-x), 0, 3,
    ansatz_passi=[
        _passo("Radici: r=2 e r=-1 (Caso 2 del formulario, esponenziale A·e^(λx)).", None),
        _passo("Termine -3e^(2x): λ=2 È radice → RISONANZA → ansatz",
               r"y_{p1} = c_1\,x\,e^{2x}"),
        _passo("Termine -2e^(-x): λ=-1 È radice → RISONANZA → ansatz",
               r"y_{p2} = c_2\,x\,e^{-x}"),
    ]))

ESAME["edo"].append(_edo2_generico(
    "14 gennaio 2026",
    "[14 gennaio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: "
    "y'' + 2y' + y = 3x^2 + e^(-x)sin(x), con y(0)=17, y'(0)=-10.",
    2, 1, r"3x^2+e^{-x}\sin x", 3*x**2+sp.exp(-x)*sp.sin(x), 17, -10,
    ansatz_passi=[
        _passo("Radice: r=-1 doppia (radice reale, non complessa).", None),
        _passo("Termine 3x² (Caso 1, polinomio grado 2): 0 non è radice → NO risonanza → ansatz",
               r"y_{p1} = Ax^2+Bx+C"),
        _passo("Termine e^(-x)sin(x) (Caso 4, e^(αx)(A cosβx+B sinβx) con α=-1,β=1): α+iβ=-1+i "
               "NON è radice (la radice è -1, reale) → NO risonanza → ansatz",
               r"y_{p2} = e^{-x}(D\cos x+E\sin x)"),
    ]))

ESAME["edo"].append(_edo2_generico(
    "16 gennaio 2026",
    "[16 gennaio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: "
    "y'' - 2y' + 5y = e^x·cos(x), con y(0)=1, y'(0)=1.",
    -2, 5, r"e^{x}\cos x", sp.exp(x)*sp.cos(x), 1, 1,
    ansatz_passi=[
        _passo("Radici: r=1±2i (complesse coniugate).", None),
        _passo("Termine e^x·cos(x) (Caso 4, α=1,β=1): α+iβ=1+i NON coincide con 1±2i "
               "→ NO risonanza → ansatz",
               r"y_p = e^{x}(A\cos x+B\sin x)"),
    ]))

ESAME["edo"].append(_edo2_generico(
    "17 gennaio 2026",
    "[17 gennaio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: "
    "y'' - 4y' + 4y = (x+3)e^(2x), con y(0)=1, y'(0)=-1. (risonanza: radice doppia r=2 uguale "
    "alla frequenza del termine forzante)",
    -4, 4, r"(x+3)e^{2x}", (x+3)*sp.exp(2*x), 1, -1,
    ansatz_passi=[
        _passo("Radice: r=2 doppia (molteplicità 2).", None),
        _passo("Termine (x+3)e^(2x) (Caso 5, e^(λx)·p(x) con λ=2, p grado 1): λ=2 È radice con "
               "molteplicità 2 → RISONANZA doppia → si moltiplica per x² → ansatz",
               r"y_p = x^2(Ax+B)e^{2x}"),
    ]))

ESAME["edo"].append(_edo2_generico(
    "9 maggio 2026",
    "[9 maggio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: "
    "y'' + y = 5e^(2x)cos(x), con y(0)=1, y'(0)=1.",
    0, 1, r"5e^{2x}\cos x", 5*sp.exp(2*x)*sp.cos(x), 1, 1,
    ansatz_passi=[
        _passo("Radici: r=±i (complesse coniugate, parte reale nulla).", None),
        _passo("Termine 5e^(2x)cos(x) (Caso 4, α=2,β=1): α+iβ=2+i NON coincide con ±i "
               "→ NO risonanza → ansatz",
               r"y_p = e^{2x}(A\cos x+B\sin x)"),
    ]))
# ---------------------------------------------------------------------------
# EDO 1° ORDINE / CAUCHY (2 problemi)
# ---------------------------------------------------------------------------

def _edo1_generico(fonte, testo, eq, x0, y0, punti_x, testo_eq_latex, tipo_metodo, note_metodo):
    Y = sp.Function('y')
    sol_gen = sp.dsolve(eq, Y(x))
    sol = sp.dsolve(eq, Y(x), ics={Y(x0): y0})

    testo_latex = testo_eq_latex + r",\quad y(" + _tex(x0) + ")=" + _tex(y0)
    passi = [_passo("Equazione:", testo_latex)]
    passi.append(_passo(f"Passo 1 — equazione {tipo_metodo}: {note_metodo}", None))
    passi.append(_passo("Passo 2 — soluzione generale (costante arbitraria C1):",
                         "y(x) = " + _tex(sol_gen.rhs)))
    passi.append(_passo("Passo 3 — imponendo la condizione iniziale:",
                         "y(x) = " + _tex(sol.rhs)))

    es_fake = {"soluzione_attesa": sol, "x0": x0, "y0": y0,
               "tipo": "lineare_var" if x0 != 0 else "lineare"}
    try:
        fig = _grafico.grafico_edo_primo_ordine(es_fake)
        png = _png(fig)
    except Exception:
        png = None

    campioni = []
    for xv in punti_x:
        try:
            val = complex(sol.rhs.subs(x, xv).evalf())
            if abs(val.imag) < 1e-8:
                campioni.append([xv, float(val.real)])
        except Exception:
            pass
    risposta = {"tipo": "funzione_su_campioni", "campioni": campioni}
    return _voce(fonte, testo, testo_latex, "Scrivi y(x) in sintassi Python, es: log(x)+3/x",
                 passi, risposta, png)


Y_ = sp.Function('y')
ESAME["edo1"].append(_edo1_generico(
    "20 ottobre 2025",
    "[20 ottobre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: "
    "y' + y/x = log(x)/x, con y(1)=2.",
    sp.Eq(Y_(x).diff(x) + Y_(x)/x, sp.log(x)/x), 1, 2, [1.1, 1.4, 1.8, 2.3, 3.0, 4.0],
    r"y' + \tfrac{y}{x} = \tfrac{\log x}{x}", "lineare del primo ordine a coefficienti variabili",
    "si risolve con il fattore integrante μ(x) = e^{∫(1/x)dx} = x."))

ESAME["edo1"].append(_edo1_generico(
    "18 ottobre 2025",
    "[18 ottobre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: "
    "y' + (log x)·y = log x, con y(2)=2.",
    sp.Eq(Y_(x).diff(x) + sp.log(x)*Y_(x), sp.log(x)), 2, 2, [2.1, 2.3, 2.5, 1.7, 1.4, 1.1],
    r"y' + (\log x)\,y = \log x", "lineare del primo ordine a coefficienti variabili",
    "si risolve con il fattore integrante μ(x) = e^{∫\\log x\\,dx} = e^{x\\log x - x} "
    "(l'integrale di log x si fa per parti)."))
# ---------------------------------------------------------------------------
# INTEGRALI DOPPI (4 problemi, tutti su domini cartesiani -- non polari: negli
# esami reali il dominio e' quasi sempre descritto da rette/parabole/coniche in
# coordinate cartesiane, non da corone circolari come nel generatore procedurale)
# ---------------------------------------------------------------------------

def _integrale_generico(fonte, testo, dominio_desc_latex, integranda_latex, valore,
                         disegno_fn, passi_extra=None):
    testo_latex = r"\iint_D " + integranda_latex + r"\,dA,\quad D: " + dominio_desc_latex
    passi = [_passo("Dominio e integranda:", testo_latex)]
    if passi_extra:
        passi.extend(passi_extra)
    passi.append(_passo("Valore dell'integrale:", "= " + _tex(valore)))

    fig = disegno_fn()
    png = _png(fig) if fig is not None else None

    risposta = {"tipo": "numero", "atteso_numero": float(sp.N(valore)), "atteso_display": str(valore)}
    return _voce(fonte, testo, testo_latex, "Scrivi il valore (numerico o simbolico), es: pi/2",
                 passi, risposta, png)


def _fig_20ott():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    yy = np.linspace(-1, 1.5, 200)
    ax.plot(yy/2+0.5, yy, color='#2e5c8a', label="x = y/2 + 1/2")
    ax.plot(yy**2-1, yy, color='#c0392b', label="x = y² - 1")
    y0, y1 = -1, 1.5
    yfill = np.linspace(y0, y1, 200)
    ax.fill_betweenx(yfill, yfill**2-1, yfill/2+0.5, alpha=0.35, color='#8a6d1a')
    ax.set_xlim(-1.5, 2); ax.set_ylim(-1.5, 2)
    ax.axhline(0, color='gray', linewidth=0.5); ax.axvline(0, color='gray', linewidth=0.5)
    ax.legend(fontsize=8); ax.set_aspect('equal', 'box')
    ax.set_title("Dominio D (20 ottobre 2025)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "20 ottobre 2025",
    "[20 ottobre 2025, Esercizio 3] Dato il dominio D = {(x,y) ∈ R²: x ≤ y/2+1/2, x ≥ y²-1}, "
    "disegnare il dominio descrivendo le caratteristiche delle curve e calcolare l'area di D "
    "(l'integrale doppio di 1 su D).",
    r"x \le \tfrac{y}{2}+\tfrac12,\ \ x \ge y^2-1", "1", sp.Rational(125, 48), _fig_20ott,
    passi_extra=[_passo("Intersezione retta-parabola: risolvendo y/2+1/2 = y²-1 si trovano y=-1 e y=3/2.",
                         None),
                 _passo("Integrando rispetto a x tra la parabola e la retta, poi rispetto a y:",
                        r"\int_{-1}^{3/2}\left[\left(\tfrac{y}{2}+\tfrac12\right)-(y^2-1)\right]dy")]))


def _fig_23ott():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    theta = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.sqrt(5)*np.cos(theta), np.sqrt(5)*np.sin(theta), color='#2e5c8a', label="x²+y²=5")
    yy = np.linspace(-2, 2, 200)
    ax.plot(1-yy, yy, color='#c0392b', label="x+y=1")
    ax.axhline(2, color='#1a7f37', label="y=2")
    yfill = np.linspace(-1, 2, 200)
    xlo = 1-yfill
    xhi = np.sqrt(np.clip(5-yfill**2, 0, None))
    ax.fill_betweenx(yfill, xlo, xhi, alpha=0.35, color='#8a6d1a')
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.axhline(0, color='gray', linewidth=0.4); ax.axvline(0, color='gray', linewidth=0.4)
    ax.legend(fontsize=8); ax.set_aspect('equal', 'box')
    ax.set_title("Dominio D (23 ottobre 2025)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "23 ottobre 2025",
    "[23 ottobre 2025, Esercizio 3] Dato l'integrale doppio di f(x,y)=x sul dominio "
    "D = {(x,y) ∈ R²: y ≤ 2, x²+y² ≤ 5, x+y ≥ 1}, disegnare il dominio e calcolarne il valore.",
    r"y\le2,\ x^2+y^2\le5,\ x+y\ge1", "x", sp.Rational(9, 2), _fig_23ott))


def _fig_16gen():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    A, B, C = (0, 4), (1, 1), (4, 0)
    tri = plt.Polygon([A, B, C], closed=True, alpha=0.35, color='#8a6d1a')
    ax.add_patch(tri)
    for (px, py), lbl in [(A, 'A(0,4)'), (B, 'B(1,1)'), (C, 'C(4,0)')]:
        ax.plot(px, py, 'ko', markersize=6)
        ax.annotate(lbl, (px, py), textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.set_xlim(-1, 5); ax.set_ylim(-1, 5)
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.4); ax.axvline(0, color='gray', linewidth=0.4)
    ax.set_title("Dominio D: triangolo (16 gennaio 2026)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "16 gennaio 2026",
    "[16 gennaio 2026, Esercizio 3] Dato l'integrale doppio di f(x,y)=xy sul dominio D = parte di "
    "piano delimitata dalle rette x+y=4, 3x+y=4 e x+3y=4, disegnare il dominio e calcolarne il "
    "valore.",
    r"\text{triangolo di vertici } (0,4),(1,1),(4,0)", "xy", sp.Rational(26, 3), _fig_16gen))


def _fig_17gen():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    xx = np.linspace(0.4, 6, 300)
    ax.plot(xx, 10/xx, color='#c0392b', label="xy=10")
    theta = np.linspace(0, np.pi/2, 200)
    ax.plot(np.sqrt(29)*np.cos(theta), np.sqrt(29)*np.sin(theta), color='#2e5c8a', label="x²+y²=29")
    xf = np.linspace(2, 5, 200)
    ax.fill_between(xf, 10/xf, np.sqrt(np.clip(29-xf**2, 0, None)), alpha=0.35, color='#8a6d1a')
    ax.set_xlim(0, 6); ax.set_ylim(0, 6)
    ax.set_aspect('equal', 'box')
    ax.legend(fontsize=8)
    ax.set_title("Dominio D, I quadrante (17 gennaio 2026)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "17 gennaio 2026",
    "[17 gennaio 2026, Esercizio 3] Dato l'integrale doppio di f(x,y)=xy sul dominio "
    "D = {(x,y) ∈ R², I quadrante: xy ≥ 10, x²+y² ≤ 29}, descrivere le curve, disegnare il "
    "dominio e calcolarne il valore.",
    r"xy\ge10,\ x^2+y^2\le29\ (x,y>0)", "xy", sp.Rational(609, 8) - 50*sp.log(sp.Rational(5, 2)),
    _fig_17gen,
    passi_extra=[_passo("Le curve xy=10 e x²+y²=29 si intersecano in (2,5) e (5,2): per x tra 2 e 5, "
                        "y varia tra l'iperbole (sotto) e la circonferenza (sopra).",
                        r"\int_2^5\int_{10/x}^{\sqrt{29-x^2}} xy\,dy\,dx")]))
# ---------------------------------------------------------------------------
# CONTINUITA' E DIFFERENZIABILITA' (2 problemi)
# ---------------------------------------------------------------------------
def _continuita_aprile():
    r2 = x**2 + y**2
    f_expr = x*sp.sin(r2)/r2 + 2*x
    testo = ("[11 aprile 2026, Esercizio 1] Data la funzione f(x,y) = x·sin(x²+y²)/(x²+y²) + 2x per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in (0,0). "
             "Determinare, se esiste, il piano tangente alla funzione nel punto (1,0).")
    testo_latex = (r"f(x,y) = \begin{cases}\dfrac{x\sin(x^2+y^2)}{x^2+y^2}+2x & (x,y)\ne(0,0) \\ "
                    r"0 & (x,y)=(0,0)\end{cases}")
    r, theta = sp.symbols('r theta', positive=True)
    fp = sp.simplify(f_expr.subs({x: r*sp.cos(theta), y: r*sp.sin(theta)}))
    passi = [_passo("Funzione:", testo_latex)]
    passi.append(_passo("Passo 1 — sin(t)/t → 1 per t→0, quindi vicino a (0,0) f si comporta come "
                         "una funzione liscia: sostituendo in polari il limite è 0 uniformemente:",
                         r"f(r,\theta) \to 0\ \ (r\to0^+)"))
    passi.append(_passo("Passo 2 — f E' continua in (0,0). Calcoliamo le derivate parziali per "
                         "definizione:", r"f_x(0,0)=3,\quad f_y(0,0)=0"))
    passi.append(_passo("Il resto [f - 3x]/r → 0 (essendo sin(t)/t - 1 = O(t²), quindi il resto è "
                         "O(r^4)): f E' anche differenziabile in (0,0).", None))
    passi.append(_passo("Passo 3 — nel punto (1,0), lontano dall'origine, f è manifestamente liscia "
                         "(il denominatore x²+y² non si annulla): calcoliamo il piano tangente con "
                         "le derivate parziali ordinarie.", None))
    fx = sp.diff(f_expr, x); fy = sp.diff(f_expr, y)
    fx10 = sp.simplify(fx.subs({x: 1, y: 0})); fy10 = sp.simplify(fy.subs({x: 1, y: 0}))
    f10 = sp.simplify(f_expr.subs({x: 1, y: 0}))
    passi.append(_passo("Valori in (1,0):",
                         f"f(1,0)={_tex(f10)},\\ f_x(1,0)={_tex(fx10)},\\ f_y(1,0)={_tex(fy10)}"))
    piano = sp.simplify(f10) + fx10*(x-1) + fy10*y
    passi.append(_passo("Piano tangente in (1,0,f(1,0)):", "z = " + _tex(piano)))

    es_fake = {"f": f_expr, "continua": True, "differenziabile": True}
    try:
        fig = _grafico.grafico_continuita(es_fake)
        png = _png(fig)
    except Exception:
        png = None
    risposta = {"tipo": "continuita", "continua": True, "differenziabile": True}
    return _voce("11 aprile 2026", testo, testo_latex,
                 "Scrivi: continua,differenziabile", passi, risposta, png)


def _continuita_maggio():
    f_expr = sp.sin(x**2*y**2)/(x**4+y**2)
    testo = ("[9 maggio 2026, Esercizio 1] Data la funzione f(x,y) = sin(x²y²)/(x⁴+y²) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in (0,0) "
             "(non sono ammesse maggiorazioni).")
    testo_latex = (r"f(x,y) = \begin{cases}\dfrac{\sin(x^2y^2)}{x^4+y^2} & (x,y)\ne(0,0) \\ "
                    r"0 & (x,y)=(0,0)\end{cases}")
    passi = [_passo("Funzione:", testo_latex)]
    passi.append(_passo("Passo 1 — poiché |sin(t)| ≤ |t|, si ha |sin(x²y²)| ≤ x²y², quindi:",
                         r"\left|\frac{\sin(x^2y^2)}{x^4+y^2}\right| \le \frac{x^2y^2}{x^4+y^2}"))
    passi.append(_passo("Passo 2 — in coordinate polari, x²y²/(x⁴+y²) → 0 per r→0 indipendentemente "
                         "da θ (si verifica anche lungo il cammino 'pericoloso' y=kx²: il limite "
                         "resta 0 per ogni k). Quindi f E' continua in (0,0).", None))
    passi.append(_passo("Passo 3 — derivate parziali in (0,0):", r"f_x(0,0)=0,\quad f_y(0,0)=0"))
    passi.append(_passo("Passo 4 — il resto f(x,y)/r → 0 anch'esso (stessa maggiorazione, un ordine "
                         "di r più stringente): f E' anche differenziabile in (0,0).",
                         r"\textbf{piano tangente: } z=0"))

    es_fake = {"f": f_expr, "continua": True, "differenziabile": True}
    try:
        fig = _grafico.grafico_continuita(es_fake)
        png = _png(fig)
    except Exception:
        png = None
    risposta = {"tipo": "continuita", "continua": True, "differenziabile": True}
    return _voce("9 maggio 2026", testo, testo_latex,
                 "Scrivi: continua,differenziabile", passi, risposta, png)


ESAME["continuita"].append(_continuita_aprile())
ESAME["continuita"].append(_continuita_maggio())
