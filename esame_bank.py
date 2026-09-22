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

Copertura: non tutti gli esercizi individuati nelle dispense sono stati inclusi (molti
erano danneggiati dall'estrazione OCR delle formule); questa e' una selezione di quelli
che si sono potuti decifrare (rileggendo le pagine originali quando serviva) e
verificare con sicurezza, rappresentativa dello stile e della difficolta' di ciascun
argomento. Taylor non ha problemi reali (non compare in nessun appello trovato).
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
    # dpi 88 + palette adattiva a 96 colori: per grafici "tecnici" (linee, curve,
    # riempimenti semi-trasparenti) e' visivamente indistinguibile dal PNG pieno,
    # ma pesa circa 1/4-1/5 in meno (verificato a campione). Con ~140 grafici nel
    # banco fa la differenza tra un file da ~20MB e uno da ~4MB da scaricare/
    # tenere in cache offline sul telefono.
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=88, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    from PIL import Image
    im = Image.open(buf).convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=96)
    out = io.BytesIO()
    im.save(out, format="PNG", optimize=True)
    out.seek(0)
    return base64.b64encode(out.read()).decode("ascii")


def _voce(fonte, testo, testo_latex, suggerimento, passi, risposta, grafico_png=None):
    return {
        "testo": testo, "testo_latex": testo_latex, "suggerimento": suggerimento,
        "passi": passi, "grafico_png": grafico_png, "risposta": risposta, "fonte": fonte,
    }


ESAME = {"serie": [], "taylor": [], "lagrange": [], "punti_liberi": [], "edo": [],
          "edo1": [], "integrali": [], "continuita": []}

# ---------------------------------------------------------------------------
# SERIE (3 problemi, appello di ottobre 2025)
# ---------------------------------------------------------------------------

def _serie_generico(fonte, testo, testo_latex, passi, valore_somma):
    risposta = {"tipo": "numero", "atteso_numero": float(sp.N(valore_somma)),
                "atteso_display": str(valore_somma)}
    return _voce(fonte, testo, testo_latex,
                 "Scrivi il valore della somma (numerico o simbolico), es: 1/5.",
                 passi, risposta, None)


def _serie_telescopica():
    n_ = sp.symbols('n', positive=True, integer=True)
    termine = sp.Integer(2) / (4*n_**2 + 8*n_ + 3)
    fatt = sp.factor(4*n_**2 + 8*n_ + 3)
    parziali = sp.apart(termine, n_)
    somma = sp.summation(termine, (n_, 2, sp.oo))
    testo = ("[22 ottobre 2025, Esercizio 3] Data la serie Σ (n≥2) 2/(4n²+8n+3), verificare che si "
             "tratta di una serie telescopica e calcolarne la somma.")
    testo_latex = r"\sum_{n\ge2}\frac{2}{4n^2+8n+3}"
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 — fattorizziamo il denominatore:", "4n^2+8n+3 = " + _tex(fatt)),
        _passo("Passo 2 — scomponiamo in fratti semplici: si ottiene la forma tipica "
               "1/(2n+1) - 1/(2n+3), cioè una serie TELESCOPICA (i cui termini si elidono a coppie):",
               r"\frac{2}{(2n+1)(2n+3)} = " + _tex(parziali)),
        _passo("Passo 3 — la somma parziale N-esima si 'accorcia': tutti i termini centrali si "
               "cancellano a due a due, restano solo il primo e l'ultimo:",
               r"\sum_{n=2}^{N}\left(\frac{1}{2n+1}-\frac{1}{2n+3}\right) = \frac15-\frac{1}{2N+3}"),
        _passo("Passo 4 — per N→∞ il secondo termine tende a 0, quindi la serie converge:",
               "\\text{somma} = " + _tex(somma)),
    ]
    return _serie_generico("22 ottobre 2025", testo, testo_latex, passi, somma)


def _serie_geometrica():
    n_ = sp.symbols('n', positive=True, integer=True)
    termine = sp.Rational(2)**(1-2*n_) / sp.Rational(3)**(n_-2)
    termine_semplificato = sp.simplify(termine)
    ratio = sp.Rational(1, 12)
    primo_termine = termine.subs(n_, 2)
    somma = sp.summation(termine, (n_, 2, sp.oo))
    testo = ("[25 ottobre 2025, Esercizio 3] Data la serie Σ (n≥2) 2^(1-2n)/3^(n-2), dopo averla "
             "ricondotta a una serie geometrica, studiarne la convergenza e calcolarne la somma.")
    testo_latex = r"\sum_{n\ge2}\frac{2^{1-2n}}{3^{n-2}}"
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 — separiamo le potenze in base n raccogliendo le costanti:",
               r"\frac{2^{1-2n}}{3^{n-2}} = 2\cdot3^2\cdot\left(\frac14\right)^n\left(\frac13\right)^n"
               " = " + _tex(termine_semplificato)),
        _passo("Passo 2 — è una serie geometrica di ragione q=1/12:",
               "q = " + _tex(ratio) + r",\ \ |q|<1 \Rightarrow \textbf{CONVERGE}"),
        _passo("Passo 3 — il primo termine (per n=2, dove parte la sommatoria) vale:",
               "a_2 = " + _tex(primo_termine)),
        _passo("Passo 4 — somma di una serie geometrica: (primo termine)/(1-ragione):",
               r"\text{somma} = \frac{" + _tex(primo_termine) + "}{1-" + _tex(ratio) + "} = "
               + _tex(somma)),
    ]
    return _serie_generico("25 ottobre 2025", testo, testo_latex, passi, somma)


def _serie_parametrica():
    xs = sp.symbols('x')
    q = (1 - xs + xs**2) / (xs + 1)
    q_at_1 = sp.nsimplify(q.subs(xs, 1))
    testo = ("[29 ottobre 2025, Esercizio 3] Data la serie Σ (n≥1) [(1-x+x²)/(x+1)]^n, determinare "
             "per quali valori reali di x la serie diverge. (Per la verifica automatica qui sotto: "
             "indica se per x=1 la serie CONVERGE o DIVERGE — la discussione completa per ogni x è "
             "nei passaggi della soluzione.)")
    testo_latex = r"\sum_{n\ge1}\left(\frac{1-x+x^2}{x+1}\right)^n"
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 — è una serie geometrica di ragione q(x) = (1-x+x²)/(x+1), definita per "
               "x≠-1 (il numeratore x²-x+1 ha discriminante negativo, quindi è sempre positivo).",
               None),
        _passo("Passo 2 — una serie geometrica converge se e solo se |q|<1, e diverge se |q|≥1 "
               "(anche nel caso limite q=±1, dove il termine generale non tende a 0).", None),
        _passo("Passo 3 — per x>-1 si ha q>0 (stesso segno del numeratore): risolviamo q≥1:",
               r"\frac{x^2-x+1}{x+1}\ge1 \iff x^2-2x\ge0 \iff x\le0 \text{ oppure } x\ge2"),
        _passo("Passo 4 — per x<-1 si ha q<0 (denominatore negativo): risolviamo q≤-1; l'algebra si "
               "riduce a x²+2≥0, SEMPRE vera. Quindi per ogni x<-1 la serie diverge sempre.",
               r"\frac{x^2-x+1}{x+1}\le-1 \iff x^2+2\ge0\ \ (\text{sempre vero})"),
        _passo("Conclusione — la serie converge SOLO per 0<x<2 (dove |q|<1); diverge per ogni altro "
               "x reale (con x≠-1, dove non è definita):",
               r"\textbf{diverge per } x\in(-\infty,0]\cup[2,+\infty),\ x\ne-1"),
        _passo(f"Verifica per x=1 (nell'intervallo di convergenza 0<x<2): q(1)={_tex(q_at_1)}, "
               "|q|<1 → CONVERGE.", None),
    ]
    risposta = {"tipo": "scelta", "atteso": "converge"}
    return _voce("29 ottobre 2025", testo, testo_latex,
                 "Scrivi 'converge' o 'diverge' (riferito al caso x=1).", passi, risposta, None)


ESAME["serie"].append(_serie_telescopica())
ESAME["serie"].append(_serie_geometrica())
ESAME["serie"].append(_serie_parametrica())
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


def _continuita_dicembre():
    f_expr = y**2*(x-2)
    testo = ("[6 dicembre 2025, Esercizio 1] Data la funzione f(x,y) = y²(x-2): a) studiare e "
             "rappresentare graficamente il segno; b) determinare gli eventuali punti di massimo e "
             "minimo utilizzando la matrice Hessiana; c) studiare continuità e differenziabilità; "
             "d) determinare, se esiste, il piano tangente in (-1,-2).")
    testo_latex = r"f(x,y) = y^2(x-2)"
    fx = sp.diff(f_expr, x); fy = sp.diff(f_expr, y)
    hess = sp.hessian(f_expr, (x, y))
    passi = [_passo("Funzione (polinomiale):", testo_latex)]
    passi.append(_passo("Passo a) — segno: y² ≥ 0 sempre, quindi il segno di f dipende solo dal "
                         "fattore (x-2):",
                         r"f\ge0 \iff x\ge2,\qquad f\le0 \iff x\le2,\qquad f=0 \iff x=2 \text{ o } y=0"))
    passi.append(_passo("Passo b) — annulliamo il gradiente per trovare i punti stazionari:",
                         _tex(fx) + "=0,\\quad" + _tex(fy) + "=0"))
    passi.append(_passo("Il sistema (y²=0, 2y(x-2)=0) impone y=0 per QUALSIASI x: i punti stazionari "
                         "non sono isolati, ma formano l'intera retta y=0 (caso degenere).", None))
    passi.append(_passo("Matrice Hessiana generale, e ristretta alla retta y=0:",
                         "H(x,y) = " + _tex(hess) + r",\quad H(x,0) = " + _tex(hess.subs(y, 0))))
    passi.append(_passo("Lungo y=0 si ha sempre det H = 0: il test dell'Hessiano NON decide da solo. "
                         "Studiando il segno direttamente, f(x0,y)-f(x0,0)=y^2(x0-2): per x0>2 è un "
                         "minimo (debole) locale, per x0<2 un massimo (debole) locale, per x0=2 f è "
                         "identicamente nulla su entrambe le rette che si incrociano lì (nessun "
                         "estremo stretto in alcun caso).", None))
    passi.append(_passo("Passo c) — continuità e differenziabilità: f è un POLINOMIO (somma e "
                         "prodotto di funzioni continue e derivabili con continuità), quindi è "
                         "automaticamente continua e differenziabile (di classe C^∞) in TUTTO R², "
                         "incluso (0,0) — a differenza degli esercizi precedenti (funzioni definite a "
                         "tratti vicino all'origine), qui non serve nessuna analisi di limite.", None))
    f_m1m2 = f_expr.subs({x: -1, y: -2})
    fx_m1m2 = fx.subs({x: -1, y: -2}); fy_m1m2 = fy.subs({x: -1, y: -2})
    piano = sp.expand(f_m1m2 + fx_m1m2*(x+1) + fy_m1m2*(y+2))
    passi.append(_passo("Passo d) — piano tangente in (-1,-2): valori di f e delle derivate parziali "
                         "in quel punto:",
                         f"f(-1,-2)={_tex(f_m1m2)},\\ f_x(-1,-2)={_tex(fx_m1m2)},\\ "
                         f"f_y(-1,-2)={_tex(fy_m1m2)}"))
    passi.append(_passo("Piano tangente:", "z = " + _tex(piano)))

    es_fake = {"f": f_expr, "continua": True, "differenziabile": True}
    try:
        fig = _grafico.grafico_continuita(es_fake)
        png = _png(fig)
    except Exception:
        png = None
    risposta = {"tipo": "continuita", "continua": True, "differenziabile": True}
    return _voce("6 dicembre 2025", testo, testo_latex,
                 "Scrivi: continua,differenziabile", passi, risposta, png)


ESAME["continuita"].append(_continuita_aprile())
ESAME["continuita"].append(_continuita_maggio())
ESAME["continuita"].append(_continuita_dicembre())

# -*- coding: utf-8 -*-
"""
Addendum: problemi reali tratti da MMpI_temi_esame_EDO_luglio_2025.pdf (una raccolta di
esercizi d'esame di EDO, con soluzioni manoscritte usate come controllo incrociato) e da
Luglio 2026.pdf (6 appelli completi: 18,20,21,22,23,25 luglio 2026, 3 esercizi ciascuno).
Diversi problemi di EDO compaiono IDENTICI in entrambi i PDF (lo stesso problema riusato
in piu' sessioni d'esame): sono stati inclusi una sola volta.
"""

# ---------------------------------------------------------------------------
# EDO 2 ORDINE -- nuovi problemi con Cauchy (A, B, G)
# ---------------------------------------------------------------------------

ESAME["edo"].append(_edo2_generico(
    "20 luglio 2026",
    "[luglio 2025 / 20 luglio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: "
    "y'' - 2y' + y = x cos x, con y(0)=0, y'(0)=1.",
    -2, 1, r"x\cos x", x*sp.cos(x), 0, 1,
    ansatz_passi=[
        _passo("Radice: r=1 doppia (molteplicita' 2, reale).", None),
        _passo("Termine x*cos(x) (polinomio di 1 grado per trigonometrica, w=1): la radice r=1 e' "
               "reale, non della forma +-i*w=+-i -> NO risonanza -> ansatz",
               r"y_p = (Ax+B)\cos x + (Cx+D)\sin x"),
    ]))

ESAME["edo"].append(_edo2_generico(
    "18 luglio 2026",
    "[luglio 2025 / 18 luglio 2026, Esercizio 2] Dopo averla classificata, risolvere il "
    "seguente problema di Cauchy: y'' + 9y = xe^(3x) + cos(3x), con y(0)=0, y'(0)=0.",
    0, 9, r"xe^{3x}+\cos(3x)", x*sp.exp(3*x)+sp.cos(3*x), 0, 0,
    ansatz_passi=[
        _passo("Radici: r=+-3i (complesse coniugate, parte reale nulla -- equazione omogenea "
               "associata di un oscillatore armonico).", None),
        _passo("Termine x*e^(3x) (Caso 5, polinomio grado 1 per esponenziale, lambda=3): lambda=3 NON e' tra "
               "le radici +-3i (che sono immaginarie pure) -> NO risonanza -> ansatz",
               r"y_{p1} = (Ax+B)e^{3x}"),
        _passo("Termine cos(3x) (Caso 3, w=3): le radici sono ESATTAMENTE +-3i, cioe' coincidono con "
               "+-iw -> RISONANZA -> si moltiplica per x -> ansatz",
               r"y_{p2} = x(A\cos 3x + B\sin 3x)"),
    ]))

ESAME["edo"].append(_edo2_generico(
    "25 luglio 2026",
    "[luglio 2025 / 25 luglio 2026, Esercizio 2] Determinare l'unica soluzione dell'equazione "
    "differenziale y'' - 2y' + 5y = 3e^x sin(x), sapendo che y(0)=1 e y'(0)=4.",
    -2, 5, r"3e^{x}\sin x", 3*sp.exp(x)*sp.sin(x), 1, 4,
    ansatz_passi=[
        _passo("Radici: r=1+-2i (complesse coniugate).", None),
        _passo("Termine 3e^x*sin(x) (Caso 4, alpha=1,beta=1): alpha+i*beta=1+i NON coincide con 1+-2i "
               "(la parte immaginaria e' diversa, beta=1!=2) -> NO risonanza -> ansatz",
               r"y_p = e^{x}(A\cos x+B\sin x)"),
    ]))

# ---------------------------------------------------------------------------
# EDO 2 ORDINE -- nuovi problemi SENZA condizioni di Cauchy (solo soluzione
# generale, come richiesto nel testo d'esame originale): la verifica automatica
# qui sotto chiede solo la soluzione particolare y_p(x) (cioe' l'omogenea con le
# costanti arbitrarie C1=C2=0), l'unica parte univocamente determinata.
# ---------------------------------------------------------------------------

def _edo2_solo_particolare(fonte, testo, a, b, forzante_tex, forzante, ansatz_passi=None):
    Y = sp.Function('y')
    eq = sp.Eq(Y(x).diff(x, 2) + a*Y(x).diff(x) + b*Y(x), forzante)
    sol_gen = sp.dsolve(eq, Y(x))
    C1, C2 = sp.symbols('C1 C2')
    y_p = sp.simplify(sol_gen.rhs.subs({C1: 0, C2: 0}))
    residuo = sp.simplify(y_p.diff(x, 2) + a*y_p.diff(x) + b*y_p - forzante)
    assert residuo == 0, f"y_p non verifica l'equazione: residuo={residuo}"

    r = sp.symbols('r')
    radici = sp.solve(sp.Eq(r**2 + a*r + b, 0), r)

    def _termine(coeff, simbolo):
        if coeff == 0:
            return ""
        segno = "+" if coeff > 0 else "-"
        c = abs(coeff)
        cifra = "" if c == 1 else str(c)
        return f"{segno}{cifra}{simbolo}"

    testo_latex = "y''" + _termine(a, "y'") + _termine(b, "y") + "=" + forzante_tex
    passi = [_passo("Equazione (il testo d'esame chiede solo la soluzione generale, non un "
                     "problema di Cauchy):", testo_latex)]
    passi.append(_passo("Passo 1 -- equazione caratteristica:",
                         f"r^2+{a}r+{b}=0 \\Rightarrow " + _tex(radici)))
    if ansatz_passi:
        passi.append(_passo("Passo 2 -- forma della soluzione particolare (metodo di somiglianza, "
                             "dal formulario): per ogni termine del termine noto, verifichiamo se "
                             "coincide con una radice dell'equazione caratteristica (risonanza):",
                             None))
        passi.extend(ansatz_passi)
    passi.append(_passo("Soluzione generale (omogenea con costanti arbitrarie C1,C2, sommata alla "
                         "particolare):", "y(x)=" + _tex(sol_gen.rhs)))
    passi.append(_passo("La parte omogenea C1(...)+C2(...) e' gia' di per se' soluzione dell'equazione "
                         "omogenea associata (=0) per QUALSIASI valore di C1,C2: la sola parte "
                         "univocamente determinata dal termine noto e' la soluzione particolare, "
                         "ottenuta ponendo C1=C2=0 nella formula sopra:",
                         "y_p(x)=" + _tex(y_p)))

    es_fake = {"soluzione_attesa": sp.Eq(Y(x), y_p), "y0": y_p.subs(x, 0)}
    try:
        fig = _grafico.grafico_edo(es_fake)
        png = _png(fig)
    except Exception:
        png = None

    punti_x = [0.0, 0.3, 0.6, 1.0, 1.5, 2.0]
    campioni = []
    for xv in punti_x:
        try:
            val = complex(y_p.subs(x, xv).evalf())
            if abs(val.imag) < 1e-8:
                campioni.append([xv, float(val.real)])
        except Exception:
            pass
    risposta = {"tipo": "funzione_su_campioni", "campioni": campioni}
    return _voce(fonte, testo, testo_latex,
                 "Scrivi SOLO la soluzione particolare y_p(x) (poni C1=C2=0), in sintassi Python, "
                 "es: exp(-x)*(1+x)",
                 passi, risposta, png)


ESAME["edo"].append(_edo2_solo_particolare(
    "luglio 2025",
    "[luglio 2025, Esercizio 2] Risolvere la seguente equazione differenziale: "
    "y'' - y' - 2y = e^(-x) + x^2 + cos(x).",
    -1, -2, r"e^{-x}+x^2+\cos x", sp.exp(-x)+x**2+sp.cos(x),
    ansatz_passi=[
        _passo("Radici: r=-1 e r=2 (reali distinte).", None),
        _passo("Termine e^(-x) (Caso 2, lambda=-1): lambda=-1 E' una delle radici (molteplicita' 1) -> "
               "RISONANZA -> si moltiplica per x -> ansatz", r"y_{p1} = Ax\,e^{-x}"),
        _passo("Termine x^2 (Caso 1, polinomio grado 2): 0 non e' radice -> NO risonanza -> ansatz",
               r"y_{p2} = Ax^2+Bx+C"),
        _passo("Termine cos(x) (Caso 3, w=1): le radici sono reali (-1 e 2), non della forma +-i "
               "-> NO risonanza -> ansatz", r"y_{p3} = A\cos x+B\sin x"),
    ]))

ESAME["edo"].append(_edo2_solo_particolare(
    "luglio 2025",
    "[luglio 2025, Esercizio 3] Risolvere la seguente equazione differenziale: "
    "y'' - 4y' + 13y = 5cos(3x).",
    -4, 13, r"5\cos(3x)", 5*sp.cos(3*x),
    ansatz_passi=[
        _passo("Radici: r=2+-3i (complesse coniugate).", None),
        _passo("Termine 5cos(3x) (Caso 3, w=3): 0+-3i NON coincide con 2+-3i (parte reale diversa, "
               "2!=0) -> NO risonanza -> ansatz", r"y_p = A\cos 3x+B\sin 3x"),
    ]))

ESAME["edo"].append(_edo2_solo_particolare(
    "21 luglio 2026",
    "[luglio 2025 / 21 luglio 2026, Esercizio 2] Dopo averla classificata, risolvere la "
    "seguente equazione differenziale: y'' - 4y' + 4y = (2x-3)e^(2x).",
    -4, 4, r"(2x-3)e^{2x}", (2*x-3)*sp.exp(2*x),
    ansatz_passi=[
        _passo("Radice: r=2 doppia (molteplicita' 2).", None),
        _passo("Termine (2x-3)e^(2x) (Caso 5, e^(lambda x)*p(x) con lambda=2, p grado 1): lambda=2 E' radice con "
               "molteplicita' 2 -> RISONANZA doppia -> si moltiplica per x^2 -> ansatz",
               r"y_p = x^2(Ax+B)e^{2x}"),
    ]))

# ---------------------------------------------------------------------------
# EDO 1 ORDINE -- nuovi problemi (C, H)
# ---------------------------------------------------------------------------

ESAME["edo1"].append(_edo1_generico(
    "22 luglio 2026",
    "[luglio 2025 / 22 luglio 2026, Esercizio 2] Trovare l'unica soluzione dell'equazione "
    "differenziale y' = -y/x + xy^2log(x), sapendo che y(1)=1/2.",
    sp.Eq(Y_(x).diff(x) + Y_(x)/x - x*Y_(x)**2*sp.log(x), 0), 1, sp.Rational(1, 2),
    [1.2, 1.5, 2.0, 0.8, 0.6, 0.4],
    r"y' = -\tfrac{y}{x} + xy^2\log x", "di Bernoulli (non lineare, esponente n=2)",
    "si linearizza dividendo per y^2 e ponendo t=y^(-1) (t'=-y'y^(-2)): si ottiene "
    "un'equazione lineare in t, risolta con il fattore integrante."))


def _edo1_bernoulli_cubica():
    """y' - y/(2x) - x*y^(1/3) = 0, y(1)=1 -- Bernoulli con n=1/3: sympy.dsolve non riesce a
    imporre le condizioni iniziali automaticamente su questa forma (branch +-), quindi la
    sostituzione t=y^(2/3) e la costante C si risolvono qui a mano (verificate sotto per
    sostituzione diretta nell'equazione originale, invece di fidarsi del solver). Si usa un
    simbolo locale POSITIVO (xp) solo per la verifica simbolica: senza l'ipotesi x>0, sympy
    non riesce a semplificare le radici frazionarie e il residuo non si annulla per pigrizia
    algebrica, non perche' la soluzione sia sbagliata (verificato anche numericamente sotto)."""
    xp = sp.symbols('xp', positive=True)
    t_espr_p = sp.Rational(2, 5)*xp**2 + sp.Rational(3, 5)*xp**sp.Rational(1, 3)
    y_sol_p = t_espr_p**sp.Rational(3, 2)
    residuo = sp.simplify(y_sol_p.diff(xp) - y_sol_p/(2*xp) - xp*y_sol_p**sp.Rational(1, 3))
    assert residuo == 0, f"residuo non nullo: {residuo}"
    assert y_sol_p.subs(xp, 1) == 1
    for xv in [sp.Rational(1, 2), sp.Integer(2), sp.Integer(5)]:
        num_res = complex((y_sol_p.diff(xp) - y_sol_p/(2*xp) - xp*y_sol_p**sp.Rational(1, 3))
                           .subs(xp, xv).evalf())
        assert abs(num_res) < 1e-9, f"residuo numerico non nullo in x={xv}: {num_res}"

    t_espr = t_espr_p.subs(xp, x)
    y_sol = y_sol_p.subs(xp, x)
    y_gen_C = sp.symbols('C1')
    t_gen = sp.Rational(2, 5)*x**2 + y_gen_C*x**sp.Rational(1, 3)
    y_gen = t_gen**sp.Rational(3, 2)

    testo = ("[23 luglio 2026, Esercizio 2] Dato il seguente problema di Cauchy: "
             "y' - y/(2x) - x*y^(1/3) = 0, y(1)=1: a) trovare la soluzione generale "
             "dell'equazione differenziale; b) trovare la soluzione del problema di Cauchy.")
    testo_latex = r"y' - \tfrac{y}{2x} - x\,y^{1/3} = 0,\quad y(1)=1"
    passi = [_passo("Equazione:", testo_latex)]
    passi.append(_passo("Passo 1 -- e' un'equazione di Bernoulli con esponente n=1/3: dividiamo "
                         "ambo i membri per y^(1/3) e poniamo t=y^(1-n)=y^(2/3):",
                         r"y'y^{-1/3} - \tfrac{1}{2x}y^{2/3} = x,\qquad t=y^{2/3},\ \ "
                         r"t' = \tfrac23 y^{-1/3}y'"))
    passi.append(_passo("Sostituendo (y'y^(-1/3) = (3/2)t'), l'equazione diventa lineare in t:",
                         r"\tfrac32 t' - \tfrac{t}{2x} = x \ \iff\ t' - \tfrac{t}{3x} = \tfrac23 x"))
    passi.append(_passo("Passo 2 -- fattore integrante mu(x)=e^(-int dx/(3x))=x^(-1/3):",
                         r"(t\,x^{-1/3})' = \tfrac23 x\cdot x^{-1/3} = \tfrac23 x^{2/3}"))
    passi.append(_passo("Integrando e moltiplicando per x^(1/3):",
                         r"t\,x^{-1/3} = \tfrac25 x^{5/3} + C \ \Rightarrow\ "
                         r"t(x) = \tfrac25 x^2 + C\,x^{1/3}"))
    passi.append(_passo("Passo 3 -- ripristinando y=t^(3/2), la soluzione generale e':",
                         "y(x) = " + _tex(y_gen)))
    passi.append(_passo("Passo 4 -- imponendo y(1)=1: t(1)=1^(2/3)=1, quindi 2/5+C=1 -> C=3/5:",
                         "C=" + _tex(sp.Rational(3, 5))))
    passi.append(_passo("Soluzione del problema di Cauchy:", "y(x) = " + _tex(y_sol)))

    Y = sp.Function('y')
    es_fake = {"soluzione_attesa": sp.Eq(Y(x), y_sol), "x0": 1, "y0": 1, "tipo": "bernoulli_var"}
    try:
        fig = _grafico.grafico_edo_primo_ordine(es_fake)
        png = _png(fig)
    except Exception:
        png = None

    campioni = []
    for xv in [1.0, 1.3, 1.6, 2.0, 2.5, 3.0]:
        try:
            val = complex(y_sol.subs(x, xv).evalf())
            if abs(val.imag) < 1e-8:
                campioni.append([xv, float(val.real)])
        except Exception:
            pass
    risposta = {"tipo": "funzione_su_campioni", "campioni": campioni}
    return _voce("23 luglio 2026", testo, testo_latex,
                 "Scrivi y(x) in sintassi Python, es: ((2*x**2+3*x**(1/3))/5)**(3/2)",
                 passi, risposta, png)


ESAME["edo1"].append(_edo1_bernoulli_cubica())

# ---------------------------------------------------------------------------
# INTEGRALI DOPPI -- nuovi problemi (Q, R, S)
# ---------------------------------------------------------------------------

import numpy as _np


def _fig_18lug_Q():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    xx = _np.linspace(0, 1.3, 200)
    ax.plot(xx, 2*_np.sqrt(xx), color='#2e5c8a', label="y = 2 sqrt(x)")
    ax.plot(xx, 2*xx**3, color='#c0392b', label="y = 2x^3")
    xf = _np.linspace(0, 1, 200)
    ax.fill_between(xf, 2*xf**3, 2*_np.sqrt(xf), alpha=0.35, color='#8a6d1a')
    ax.set_xlim(-0.2, 1.4); ax.set_ylim(-0.2, 2.2)
    ax.axhline(0, color='gray', linewidth=0.4); ax.axvline(0, color='gray', linewidth=0.4)
    ax.legend(fontsize=8); ax.set_aspect('equal', 'box')
    ax.set_title("Dominio D (18 luglio 2026)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "18 luglio 2026",
    "[18 luglio 2026, Esercizio 3] Dato il seguente integrale doppio di f(x,y)=x+y sul "
    "dominio D = {(x,y) in R^2: y <= 2 sqrt(x), y >= 2x^3}, disegnare e descrivere il dominio e "
    "calcolarne il valore.",
    r"y\le2\sqrt{x},\ \ y\ge2x^3", "x+y", sp.Rational(39, 35), _fig_18lug_Q,
    passi_extra=[_passo("Intersezione delle due curve: 2sqrt(x)=2x^3 <=> sqrt(x)=x^3, risolvendo per x>0 si "
                         "trova x=1 (e x=0); per 0<x<1 la parabola cubica y=2x^3 sta sotto la "
                         "radice y=2sqrt(x) (es. in x=0.5: 2x^3=0.25 < 2sqrt(x)=1.41).", None),
                 _passo("Integrando prima su y (tra le due curve), poi su x tra 0 e 1:",
                        r"\int_0^1\int_{2x^3}^{2\sqrt{x}}(x+y)\,dy\,dx")]))


def _fig_21lug_R():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    O, A, B = (0, 0), (1, 0), (1, 2)
    tri = plt.Polygon([O, A, B], closed=True, alpha=0.35, color='#8a6d1a')
    ax.add_patch(tri)
    for (px, py), lbl in [(O, 'O(0,0)'), (A, 'A(1,0)'), (B, 'B(1,2)')]:
        ax.plot(px, py, 'ko', markersize=6)
        ax.annotate(lbl, (px, py), textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.set_xlim(-0.5, 2); ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.4); ax.axvline(0, color='gray', linewidth=0.4)
    ax.set_title("Dominio D: triangolo (21 luglio 2026)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "21 luglio 2026",
    "[21 luglio 2026, Esercizio 3] Calcolare il seguente integrale doppio di f(x,y)=x^2e^(xy) "
    "sul dominio D = triangolo di vertici O(0,0), A(1,0), B(1,2). E' obbligatorio disegnare e "
    "colorare il dominio.",
    r"\text{triangolo di vertici } O(0,0),\,A(1,0),\,B(1,2)", "x^2e^{xy}",
    sp.Rational(-3, 4) + sp.exp(2)/4, _fig_21lug_R,
    passi_extra=[_passo("Il lato OB e' la retta y=2x: per x in [0,1], y varia tra 0 (lato OA) e "
                         "2x (lato OB).", None),
                 _passo("Integrando prima su y, poi su x -- l'integrale interno si risolve subito "
                         "perche' x^2e^(xy) e' (a meno di 1/x) la derivata rispetto a y di x*e^(xy):",
                         r"\int_0^1\int_0^{2x} x^2e^{xy}\,dy\,dx = "
                         r"\int_0^1\left[xe^{xy}\right]_0^{2x}dx = \int_0^1\left(xe^{2x^2}-x\right)dx")]))


def _fig_22lug_S():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    verts = [(0, 1), (1, 2), (2, 1), (2, 0)]
    quad = plt.Polygon(verts, closed=True, alpha=0.35, color='#8a6d1a')
    ax.add_patch(quad)
    for (px, py) in verts:
        ax.plot(px, py, 'ko', markersize=6)
        ax.annotate(f"({px},{py})", (px, py), textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.set_xlim(-0.5, 3); ax.set_ylim(-0.5, 2.7)
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.4); ax.axvline(0, color='gray', linewidth=0.4)
    ax.set_title("Dominio D: quadrilatero (22 luglio 2026)", fontsize=9.5)
    fig.tight_layout()
    return fig


ESAME["integrali"].append(_integrale_generico(
    "22 luglio 2026",
    "[22 luglio 2026, Esercizio 3] Calcolare il seguente integrale doppio: doppio integrale su D di y dx dy, dove "
    "D e' il quadrilatero di vertici (0,1), (1,2), (2,1), (2,0).",
    r"\text{quadrilatero di vertici } (0,1),(1,2),(2,1),(2,0)", "y", sp.Integer(2), _fig_22lug_S,
    passi_extra=[_passo("I 4 lati: da (0,1) a (1,2) la retta y=x+1; da (1,2) a (2,1) la retta "
                         "y=-x+3; da (2,1) a (2,0) il segmento verticale x=2; da (2,0) a (0,1) la "
                         "retta y=1-x/2 (che fa da bordo INFERIORE per tutto x in [0,2]).", None),
                 _passo("Si integra separatamente per x in [0,1] (tetto y=x+1) e x in [1,2] (tetto "
                        "y=-x+3), con lo stesso bordo inferiore y=1-x/2:",
                        r"\int_0^1\!\!\int_{1-x/2}^{x+1}\!y\,dy\,dx + "
                        r"\int_1^2\!\!\int_{1-x/2}^{-x+3}\!y\,dy\,dx")]))

# ---------------------------------------------------------------------------
# SERIE -- nuovi problemi (M, N, O)
# ---------------------------------------------------------------------------


def _serie_fattoriale_ratio():
    n_ = sp.symbols('n', positive=True, integer=True)
    a_n = sp.factorial(n_)**2 / (n_**3 * sp.factorial(2*n_))
    a_n1 = a_n.subs(n_, n_+1)
    ratio = sp.simplify(a_n1/a_n)
    lim = sp.limit(ratio, n_, sp.oo)
    testo = ("[20 luglio 2026, Esercizio 3] Studiare il carattere della serie "
             "sommatoria (n>=1) (n!)^2/(n^3(2n)!).")
    testo_latex = r"\sum_{n\ge1}\frac{(n!)^2}{n^3(2n)!}"
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 -- termini tutti positivi e con fattoriali: usiamo il criterio del "
               "rapporto. Rapporto a_(n+1)/a_n:",
               r"\frac{a_{n+1}}{a_n} = " + _tex(ratio)),
        _passo("Passo 2 -- limite per n->infinito:", r"\lim_{n\to\infty}\frac{a_{n+1}}{a_n} = " + _tex(lim)),
        _passo(f"Passo 3 -- essendo il limite {_tex(lim)} < 1, per il criterio del rapporto la "
               "serie CONVERGE.", None),
    ]
    risposta = {"tipo": "scelta", "atteso": "converge"}
    return _voce("20 luglio 2026", testo, testo_latex,
                 "Scrivi 'converge' o 'diverge'.", passi, risposta, None)


ESAME["serie"].append(_serie_fattoriale_ratio())


def _serie_geometrica_parametrica_2026():
    testo = ("[23 luglio 2026, Esercizio 3] Data la serie geometrica "
             "sommatoria (n>=1) [8/(6x-x^2-8)]^n, determinare per quali valori di x la serie "
             "converge. (Per la verifica automatica qui sotto: indica se per x=-1 la serie "
             "CONVERGE o DIVERGE -- la discussione completa per ogni x e' nei passaggi della "
             "soluzione.)")
    testo_latex = r"\sum_{n\ge1}\left(\frac{8}{6x-x^2-8}\right)^n"
    xs = sp.symbols('x')
    q = 8/(6*xs - xs**2 - 8)
    fatt = sp.factor(6*xs - xs**2 - 8)
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 -- e' geometrica di ragione q(x)=8/(6x-x^2-8); fattorizzando il "
               "denominatore:", r"6x-x^2-8 = " + _tex(fatt) + r"\ \Rightarrow\ q(x)=\frac{8}{"
               + _tex(fatt) + "}"),
        _passo("Passo 2 -- dominio: q(x) non e' definita per x=2 e x=4 (denominatore nullo).", None),
        _passo("Passo 3 -- una serie geometrica converge se e solo se |q(x)|<1; risolvendo "
               "q(x)^2<1 (equivalente a |q|<1, evitando di discutere il segno del denominatore "
               "caso per caso):",
               r"q(x)^2<1 \iff \frac{64}{(x-2)^2(x-4)^2}<1"),
        _passo("Risolvendo la disequazione si ottiene:", r"x<0 \ \text{ oppure } \ x>6"),
        _passo("Conclusione -- la serie converge per x in (-infinito,0) unito (6,+infinito) (intervalli che escludono "
               "automaticamente anche x=2 e x=4, dove non e' comunque definita).", None),
    ]
    passi.append(_passo("Verifica per x=-1 (nell'intervallo di convergenza x<0): "
                         "q(-1)=8/(-6-1-8)=8/-15, |q|<1 -> CONVERGE.", None))
    risposta = {"tipo": "scelta", "atteso": "converge"}
    return _voce("23 luglio 2026", testo, testo_latex,
                 "Scrivi 'converge' o 'diverge' (riferito al caso x=-1).", passi, risposta, None)


ESAME["serie"].append(_serie_geometrica_parametrica_2026())


def _serie_esponenziale_fattoriale():
    n_ = sp.symbols('n', positive=True, integer=True)
    a_n = 2**(n_+1) / (sp.factorial(n_-1) * n_**n_)
    a_n1 = a_n.subs(n_, n_+1)
    ratio = sp.simplify(a_n1/a_n)
    lim = sp.limit(ratio, n_, sp.oo)
    testo = "[25 luglio 2026, Esercizio 3] Studiare il carattere della serie sommatoria (n>=2) 2^(n+1)/((n-1)!*n^n)."
    testo_latex = r"\sum_{n\ge2}\frac{2^{n+1}}{(n-1)!\,n^n}"
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 -- termini positivi con fattoriali e potenze n-esime: criterio del "
               "rapporto. Rapporto a_(n+1)/a_n:",
               r"\frac{a_{n+1}}{a_n} = " + _tex(ratio)),
        _passo("Passo 2 -- limite per n->infinito (n^n al denominatore cresce piu' velocemente di "
               "qualunque esponenziale o fattoriale al numeratore):",
               r"\lim_{n\to\infty}\frac{a_{n+1}}{a_n} = " + _tex(lim)),
        _passo(f"Passo 3 -- essendo il limite {_tex(lim)} < 1, per il criterio del rapporto la "
               "serie CONVERGE.", None),
    ]
    risposta = {"tipo": "scelta", "atteso": "converge"}
    return _voce("25 luglio 2026", testo, testo_latex,
                 "Scrivi 'converge' o 'diverge'.", passi, risposta, None)


ESAME["serie"].append(_serie_esponenziale_fattoriale())

# ---------------------------------------------------------------------------
# LAGRANGE -- nuovo problema (P)
# ---------------------------------------------------------------------------


def _lagrange_orlato_parabola():
    f = (x-3)**2*y + (y-6)**2 - 9
    g = (x-3)**2 + y - 7
    px, py, lv = sp.Integer(3), sp.Integer(7), sp.Integer(2)
    val = f.subs({x: px, y: py})
    cl = _mv._classifica_hessiana_orlata(f, g, px, py, lv)

    testo = ("[21 luglio 2026, Esercizio 1] Utilizzando il metodo dell'Hessiano orlato, "
             "determinare e classificare i punti critici della funzione f(x,y)=(x-3)^2y+(y-6)^2-9 "
             "soggetta al vincolo g(x,y)=(x-3)^2+y-7. Descrivere e rappresentare il vincolo.")
    testo_latex = r"f(x,y)=(x-3)^2y+(y-6)^2-9,\quad g(x,y)=(x-3)^2+y-7=0"
    fx, fy = sp.diff(f, x), sp.diff(f, y)
    gx, gy = sp.diff(g, x), sp.diff(g, y)
    passi = [
        _passo("Il vincolo g(x,y)=0 riscritto esplicitando y:",
               r"(x-3)^2+y-7=0 \iff y = 7-(x-3)^2"),
        _passo("E' una PARABOLA con la concavita' rivolta verso il basso, vertice in (3,7) -- non e' "
               "un insieme compatto (si estende indefinitamente verso il basso), quindi il "
               "teorema di Weierstrass non garantisce automaticamente l'esistenza di massimo e "
               "minimo assoluti su di essa.", None),
        _passo("Sistema di Lagrange: gradiente(f)=lambda*gradiente(g), g=0.",
               f"{_tex(fx)}=\\lambda\\cdot{_tex(gx)},\\quad {_tex(fy)}=\\lambda\\cdot{_tex(gy)},"
               f"\\quad {_tex(g)}=0"),
        _passo("Dalla prima equazione, 2(x-3)y=2lambda(x-3): se x!=3 si semplifica per (x-3) ottenendo "
               "y=lambda, che sostituito nella seconda equazione porta a una contraddizione col "
               "vincolo (7-12 non torna): l'UNICA soluzione e' x=3. Sostituendo x=3 nel "
               "vincolo si trova y=7, e dalla seconda equazione lambda=2:",
               f"(x,y)=({_tex(px)},{_tex(py)}),\\ \\lambda={_tex(lv)}\\ \\Rightarrow\\ f={_tex(val)}"),
        _passo("Classifichiamo con l'Hessiano orlato (dal formulario): posto L=f-lambda*g,",
               r"\overline{H}=\begin{pmatrix}0&g_x'&g_y'\\g_x'&L_{xx}''&L_{xy}''\\"
               r"g_y'&L_{yx}''&L_{yy}''\end{pmatrix},\ \ \overline{H}>0\Rightarrow\text{max rel.},"
               r"\ \overline{H}<0\Rightarrow\text{min rel.}"),
        _passo(f"Nel punto (3,7):", f"\\det\\overline{{H}}={_tex(cl['det'])}\\ \\Rightarrow\\ "
               f"\\textbf{{{cl['tipo']}}}"),
    ]

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    xx = np.linspace(-2, 8, 200)
    ax.plot(xx, 7-(xx-3)**2, color='#c0392b', linewidth=2, label="vincolo: y=7-(x-3)^2")
    ax.plot(float(px), float(py), 'ko', markersize=7)
    ax.annotate(f"f={val}  ({cl['tipo']})", (float(px), float(py)),
                textcoords="offset points", xytext=(7, 7), fontsize=8)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.legend(loc='lower center', fontsize=8)
    ax.set_title("Vincolo (parabola) e punto stazionario")
    fig.tight_layout()
    png = _png(fig)

    risposta = {"tipo": "punti_valore",
                "punti_attesi": [[float(px), float(py), float(val)]],
                "valore_max": None, "valore_min": float(val)}
    return _voce("21 luglio 2026", testo, testo_latex,
                 "Un punto per riga, formato x,y (es: 3,7).", passi, risposta, png)


ESAME["lagrange"].append(_lagrange_orlato_parabola())

# ---------------------------------------------------------------------------
# PUNTI STAZIONARI LIBERI -- nuovo problema (T)
# ---------------------------------------------------------------------------

ESAME["punti_liberi"].append(_punti_liberi_generico(
    "23 luglio 2026",
    "[23 luglio 2026, Esercizio 1] Data la funzione f(x,y) = (x-y)/(1+x^2+y^2), determinare il "
    "dominio, studiare il segno e studiare la natura dei punti stazionari.",
    (x-y)/(1+x**2+y**2),
    nota_extra=("Dominio: il denominatore 1+x^2+y^2 e' sempre >=1>0, quindi f e' definita su TUTTO "
                "R^2 (nessuna restrizione). Segno: poiche' il denominatore e' sempre positivo, il "
                "segno di f coincide con quello del numeratore: f>0 per x>y, f<0 per x<y, f=0 "
                "sulla retta x=y (bisettrice del I e III quadrante).")))

# ---------------------------------------------------------------------------
# CONTINUITA' E DIFFERENZIABILITA' -- nuovi problemi (I, J, K, L)
# ---------------------------------------------------------------------------


def _continuita_non_differenziabile(fonte, testo, testo_latex, f_expr, fx0, fy0, nota_non_diff):
    """Schema comune per le funzioni definite a tratti in cui f risulta CONTINUA ma NON
    differenziabile in (0,0): la verifica per sostituzione polare mostra che f(r,theta)->0
    uniformemente (continuita'), ma il resto [f - fx*x - fy*y]/r NON tende a 0 uniformemente
    (dipende da theta), quindi f non ammette piano tangente in (0,0)."""
    passi = [_passo("Funzione:", testo_latex)]
    passi.append(_passo("Passo 1 -- passando in coordinate polari (x=r cos(theta), y=r sin(theta)) e "
                         "sviluppando per r->0, si verifica che f(r,theta)->0 uniformemente rispetto a "
                         "theta (bound indipendente da theta): f e' CONTINUA in (0,0).", None))
    passi.append(_passo("Passo 2 -- derivate parziali in (0,0) per definizione (limite del "
                         "rapporto incrementale lungo gli assi):",
                         f"f_x(0,0)={_tex(fx0)},\\quad f_y(0,0)={_tex(fy0)}"))
    passi.append(_passo("Passo 3 -- test di differenziabilita': calcoliamo "
                         r"\frac{f(x,y)-f_x(0,0)x-f_y(0,0)y}{r} in coordinate polari, per r->0:",
                         None))
    passi.append(_passo(nota_non_diff, None))
    passi.append(_passo("Il resto, diviso per r, NON tende a 0 uniformemente (dipende da theta e non "
                         "si annulla per alcuni valori di theta): f e' quindi CONTINUA ma NON "
                         "DIFFERENZIABILE in (0,0) -- nessun piano tangente in quel punto.", None))

    es_fake = {"f": f_expr, "continua": True, "differenziabile": False}
    try:
        fig = _grafico.grafico_continuita(es_fake)
        png = _png(fig)
    except Exception:
        png = None
    risposta = {"tipo": "continuita", "continua": True, "differenziabile": False}
    return _voce(fonte, testo, testo_latex,
                 "Scrivi: continua, non differenziabile", passi, risposta, png)


ESAME["continuita"].append(_continuita_non_differenziabile(
    "18 luglio 2026",
    "[18 luglio 2026, Esercizio 1] Data la funzione f(x,y) = arctan(x^3-y^3)/(x^2+y^2) per "
    "(x,y)!=(0,0), f(0,0)=0, studiarne continuita' e differenziabilita'. Sono ammessi solo il "
    "metodo del passaggio in coordinate polari o la verifica con il fascio di rette.",
    r"f(x,y) = \begin{cases}\dfrac{\arctan(x^3-y^3)}{x^2+y^2} & (x,y)\ne(0,0) \\ "
    r"0 & (x,y)=(0,0)\end{cases}",
    sp.atan(x**3-y**3)/(x**2+y**2), sp.Integer(1), sp.Integer(-1),
    "Usando arctan(t) circa t per t piccolo, si trova f(r,theta) circa r(cos^3(theta)-sin^3(theta))+O(r^3): il resto "
    "[f-x+y]/r si riconduce, al primo ordine, a (cos(theta)-sin(theta))(cos(theta)sin(theta)), che vale ad esempio "
    "circa -0.058 per theta=pi/3 (quindi diverso da 0)."))

ESAME["continuita"].append(_continuita_non_differenziabile(
    "22 luglio 2026",
    "[22 luglio 2026, Esercizio 1] Studiare continuita' e differenziabilita' della seguente "
    "funzione f(x,y) = (x-y)(x^2-y^2)^2(x+y+4)^2/(x^2+y^2)^2 per (x,y)!=(0,0), f(0,0)=0. E' ammesso "
    "solo il metodo del passaggio in coordinate polari o la verifica con il fascio di rette.",
    r"f(x,y) = \begin{cases}\dfrac{(x-y)(x^2-y^2)^2(x+y+4)^2}{(x^2+y^2)^2} & (x,y)\ne(0,0) \\ "
    r"0 & (x,y)=(0,0)\end{cases}",
    (x-y)*(x**2-y**2)**2*(x+y+4)**2/(x**2+y**2)**2, sp.Integer(16), sp.Integer(-16),
    "Riscrivendo (x^2-y^2)^2=(x-y)^2(x+y)^2, il numeratore e' (x-y)^3(x+y)^2(x+y+4)^2: vicino "
    "all'origine (x+y+4)^2 circa 16 (fattore quasi costante), quindi f circa 16r(cos(theta)-sin(theta))^3(cos(theta)+sin(theta))^2. "
    "Il resto [f-16x+16y]/r, calcolato con piu' precisione, vale ad esempio 6-6*sqrt(3) circa -4.39 per "
    "theta=pi/6 (quindi diverso da 0)."))

ESAME["continuita"].append(_continuita_non_differenziabile(
    "25 luglio 2026",
    "[25 luglio 2026, Esercizio 1] Data la funzione f(x,y) = y(1-cos(xy))/log(1+x^4+y^4) per "
    "(x,y)!=(0,0), f(0,0)=0, studiarne continuita' e differenziabilita'. Sono ammessi solo il "
    "metodo del passaggio in coordinate polari o la verifica tramite fascio di rette.",
    r"f(x,y) = \begin{cases}\dfrac{y(1-\cos(xy))}{\log(1+x^4+y^4)} & (x,y)\ne(0,0) \\ "
    r"0 & (x,y)=(0,0)\end{cases}",
    y*(1-sp.cos(x*y))/sp.log(1+x**4+y**4), sp.Integer(0), sp.Integer(0),
    "Usando 1-cos(t) circa t^2/2 e log(1+s) circa s per t,s piccoli, si trova f(x,y) circa x^2y^3/(2(x^4+y^4)), cioe' "
    "in polari f(r,theta) circa r*[sin^3(theta)cos^2(theta)/(2(sin^4(theta)+cos^4(theta)))] (il denominatore sin^4(theta)+cos^4(theta) non si "
    "annulla mai, essendo sempre >=1/2). Poiche' fx(0,0)=fy(0,0)=0, il resto f/r tende proprio a "
    "questa quantita', che vale ad esempio sqrt(2)/8 circa 0.177 per theta=pi/4 (quindi diverso da 0)."))


def _continuita_dominio_piano_tangente():
    f_expr = sp.sqrt(4/(x**2+y**2) - 1)
    px, py = sp.Integer(1), sp.Integer(1)
    fx = sp.diff(f_expr, x); fy = sp.diff(f_expr, y)
    f1 = f_expr.subs({x: px, y: py})
    fx1 = sp.simplify(fx.subs({x: px, y: py}))
    fy1 = sp.simplify(fy.subs({x: px, y: py}))
    piano = sp.simplify(f1 + fx1*(x-px) + fy1*(y-py))

    testo = ("[20 luglio 2026, Esercizio 1] Data la funzione f(x,y) = sqrt(4/(x^2+y^2) - 1), "
             "disegnare e colorare il dominio. E' possibile calcolare il piano tangente al suo "
             "grafico nel punto (1,1)? In caso affermativo, determinarne l'equazione.")
    testo_latex = r"f(x,y) = \sqrt{\dfrac{4}{x^2+y^2}-1}"
    passi = [_passo("Funzione:", testo_latex)]
    passi.append(_passo("Passo 1 -- dominio: serve che l'argomento della radice sia >=0 e che il "
                         "denominatore non si annulli:",
                         r"\frac{4}{x^2+y^2}\ge1 \ \text{ e }\ x^2+y^2\ne0 \iff 0<x^2+y^2\le4"))
    passi.append(_passo("Il dominio e' il disco chiuso di raggio 2 centrato nell'origine, PRIVATO "
                         "dell'origine stessa (dove il denominatore si annulla): una corona "
                         "circolare degenere.", None))
    passi.append(_passo("Passo 2 -- il punto (1,1) ha x^2+y^2=2, che soddisfa 0<2<=4 STRETTAMENTE "
                         "(non e' sul bordo x^2+y^2=4): e' un punto INTERNO al dominio, dove f e' "
                         "derivabile con continuita' (l'argomento della radice vale 4/2-1=1>0, "
                         "quindi niente radice di 0 che darebbe problemi di derivabilita'). Il "
                         "piano tangente ESISTE.", None))
    passi.append(_passo("Passo 3 -- derivate parziali in (1,1):",
                         f"f(1,1)={_tex(f1)},\\ f_x(1,1)={_tex(fx1)},\\ f_y(1,1)={_tex(fy1)}"))
    passi.append(_passo("Piano tangente in (1,1,f(1,1)):", "z = " + _tex(piano)))

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    theta = np.linspace(0, 2*np.pi, 200)
    ax.fill(2*np.cos(theta), 2*np.sin(theta), alpha=0.35, color='#8a6d1a', label="dominio: 0<x^2+y^2<=4")
    ax.plot(0, 0, 'wo', markersize=8, markeredgecolor='black', label="origine ESCLUSA")
    ax.plot(1, 1, 'ko', markersize=7, label="punto (1,1)")
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6)
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.4); ax.axvline(0, color='gray', linewidth=0.4)
    ax.legend(fontsize=8, loc='upper right')
    ax.set_title("Dominio di f (20 luglio 2026)", fontsize=9.5)
    fig.tight_layout()
    png = _png(fig)

    risposta = {"tipo": "continuita", "continua": True, "differenziabile": True}
    return _voce("20 luglio 2026", testo, testo_latex,
                 "Scrivi: continua,differenziabile", passi, risposta, png)


ESAME["continuita"].append(_continuita_dominio_piano_tangente())
