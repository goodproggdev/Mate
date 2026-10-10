# -*- coding: utf-8 -*-
"""
Addendum al banco 'Esame': SERIE NUMERICHE e CONTINUITA'/DIFFERENZIABILITA'/PIANO TANGENTE
tratti dai PDF in ExEsami (Settembre 2025, Gennaio 2025, Maggio 2025, Aprile 2025/2026,
Maggio 2026, Ottobre 2025, Dicembre 2025, Ottobre 2024, Luglio 2024, Maggio 2024, Aprile 2024,
Dicembre 2024, Dicembre 2023, Ottobre 2023, Dicembre 2021, Settembre 2021, ...).
Ogni esercizio compare una sola volta (i testi ripetuti in piu' appelli sono stati riuniti,
indicando come fonte l'appello piu' recente); ogni risultato e' stato verificato con sympy e
con valutazioni numeriche (raggi, parabole) prima di scrivere la conclusione.
Si aggancia a esame_bank.ESAME e NON modifica altri file.
"""
import sympy as sp

import esame_bank
from esame_bank import ESAME, _voce, _passo, _tex, _png, _serie_generico, plt, np

_N0 = {k: len(v) for k, v in ESAME.items()}   # lunghezze prima di aggiungere le nostre voci
_mv = esame_bank._mv
_grafico = esame_bank._grafico

x, y = esame_bank.x, esame_bank.y
n_ = sp.symbols('n', positive=True, integer=True)
r_, th_ = sp.symbols('r theta', positive=True)


# ===========================================================================
# SERIE -- helper
# ===========================================================================
def _serie_scelta(fonte, testo, testo_latex, passi, atteso, suggerimento):
    return _voce(fonte, testo, testo_latex, suggerimento, passi,
                 {"tipo": "scelta", "atteso": atteso}, None)


def _serie_geom_param(fonte, testo, testo_latex, q, n0, passi_algebra, concl_testo, concl_latex,
                      x_test, con_somma=False, nota_dominio=None, nota_dominio_latex=None):
    """Serie geometrica sum_{n>=n0} q(x)^n con parametro x: |q|<1, eventuale somma.
    'passi_algebra' e' la lista (scritta a mano) dei passaggi che risolvono |q(x)|<1.
    Se con_somma, la risposta verificabile e' il valore della somma in x=x_test (che deve
    stare nell'insieme di convergenza); altrimenti e' 'converge/diverge' in x=x_test."""
    xs = sp.symbols('x')
    qv = q.subs(xs, x_test)
    passi = [_passo("Serie:", testo_latex)]
    dom_txt = ("Passo 1 — riconosciamo una serie geometrica di ragione q(x) (la potenza n-esima "
               "di una quantità che dipende solo da x):")
    passi.append(_passo(dom_txt, r"q(x)=" + _tex(q)))
    if nota_dominio:
        passi.append(_passo(nota_dominio, nota_dominio_latex))
    passi.append(_passo("Passo 2 — criterio per la serie geometrica di ragione q(x) (formulario ufficiale, "
                        "serie notevoli): converge se e solo se |q(x)|<1; per |q(x)|≥1 il termine "
                        "q(x)^n non tende a 0 e la serie diverge (o è indeterminata).",
                        r"\sum_{n\ge n_0} q^n\ \text{converge} \iff |q|<1"))
    for _pa in passi_algebra:
        if "q(x)" not in (_pa["testo"] or ""):
            _pa = dict(_pa)
            _pa["testo"] = _pa["testo"].replace(" — ", " — ragione q(x): ", 1)
        passi.append(_pa)
    passi.append(_passo(concl_testo, concl_latex))
    somma = None
    if con_somma:
        somma = sp.simplify(q**n0 / (1 - q))
        primo = _tex(sp.simplify(q**n0))
        passi.append(_passo("Passo finale — somma della serie geometrica di ragione q(x) nell'insieme di "
                            "convergenza: primo termine diviso (1 − ragione), con primo termine "
                            "q(x)^{n_0} (qui la somma parte da n=" + str(n0) + "):",
                            r"S(x)=\frac{q^{" + str(n0) + r"}}{1-q}=\frac{" + primo + "}{1-" +
                            _tex(q) + "}=" + _tex(somma)))
        sv = sp.nsimplify(somma.subs(xs, x_test))
        passi.append(_passo(f"Verifica per x={_tex(x_test)} (dentro l'insieme di convergenza): "
                            "ragione q(x) e somma:",
                            "q=" + _tex(sp.nsimplify(qv)) + r",\ |q|<1\ \Rightarrow\ S=" + _tex(sv)))
        risposta = {"tipo": "numero", "atteso_numero": float(sp.N(sv)), "atteso_display": str(sv)}
        sugg = "Scrivi il valore della somma per il valore di x indicato (es: 7/8)."
        return _voce(fonte, testo, testo_latex, sugg, passi, risposta, None)
    conv = abs(sp.N(qv)) < 1
    passi.append(_passo(f"Verifica per x={_tex(x_test)}:",
                        "q=" + _tex(sp.nsimplify(qv)) + (r",\ |q|<1\ \Rightarrow\ \textbf{CONVERGE}" if conv
                                                       else r",\ |q|\ge1\ \Rightarrow\ \textbf{DIVERGE}")))
    return _serie_scelta(fonte, testo, testo_latex, passi, "converge" if conv else "diverge",
                         "Scrivi 'converge' o 'diverge' (riferito al caso x indicato).")


def _serie_telescopica_gen(fonte, testo, testo_latex, termine, n0, fattori_latex, apart_latex,
                           somma_parziale_latex, somma_parziale_expr, risposta_valore,
                           passi_extra=None, nota_lim=None):
    """Serie telescopica: fratti semplici, somma parziale S_N (verificata con sympy per N=1..8),
    limite per N->infinito. 'risposta_valore' e' la somma (o altra grandezza richiesta)."""
    N = sp.symbols('N', positive=True, integer=True)
    somma = sp.summation(termine, (n_, n0, sp.oo))
    for NN in range(n0, n0 + 8):
        parz = sum(termine.subs(n_, k) for k in range(n0, NN + 1))
        assert sp.simplify(parz - somma_parziale_expr.subs(N, NN)) == 0, (testo, NN)
    passi = [
        _passo("Serie:", testo_latex),
        _passo("Passo 1 — fattorizziamo il denominatore (per riconoscere i fattori che poi si "
               "elideranno):", fattori_latex),
        _passo("Passo 2 — scomponiamo in fratti semplici (determinando i coefficienti): ogni "
               "termine è la differenza di due frazioni, una con n e una con n spostato — serie "
               "TELESCOPICA (i termini si elidono a coppie).", apart_latex),
        _passo("Passo 3 — scriviamo la somma parziale N-esima: i termini centrali si cancellano a "
               "due a due e se ne conservano solo pochi, all'inizio e alla fine:", somma_parziale_latex),
        _passo("Passo 4 — la parte finale della somma parziale tende a 0 per N→∞ (il denominatore "
               "cresce), quindi la serie converge e la sua somma è il limite della somma parziale:",
               r"S=\lim_{N\to\infty}S_N=" + _tex(somma)),
    ]
    if passi_extra:
        passi.extend(passi_extra)
    return somma, passi


# ===========================================================================
# SERIE -- 11 settembre 2025, Es. 2 (anche Gennaio 2025 n.19, Maggio 2025): segni alterni e fattoriali
# ===========================================================================
def _serie_alterna_fattoriale():
    a_n = (-1)**n_ * 2**(n_ + 1) / (3**(n_ + 2) * sp.factorial(n_))
    mod = 2**(n_ + 1) / (3**(n_ + 2) * sp.factorial(n_))
    rapp = sp.simplify(mod.subs(n_, n_ + 1) / mod)
    lim = sp.limit(rapp, n_, sp.oo)
    somma = sp.summation(a_n, (n_, 1, sp.oo))
    assert sp.simplify(somma - sp.Rational(2, 9) * (sp.exp(-sp.Rational(2, 3)) - 1)) == 0
    testo = ("[11 settembre 2025, Esercizio 2] Studiare il comportamento della seguente serie: "
             "Σ (n≥1) (-1)^n · 2^(n+1) / (3^(n+2) · n!). (Stesso testo nei compiti di Gennaio 2025 "
             "n.19 e di Maggio 2025.)")
    tl = r"\sum_{n\ge1}(-1)^n\,\frac{2^{n+1}}{3^{n+2}\,n!}"
    passi = [
        _passo("Serie:", tl),
        _passo("Passo 1 — la serie è a segni alterni (fattore (−1)^n) e contiene un fattoriale: il modo "
               "più rapido è studiare la serie dei moduli con il criterio del rapporto; se converge "
               "essa, la serie di partenza converge ASSOLUTAMENTE e quindi converge (formulario, "
               "sez. 9.2).",
               r"|a_n|=\frac{2^{n+1}}{3^{n+2}\,n!}"),
        _passo("Passo 2 — rapporto fra termini consecutivi (si semplificano le potenze con la "
               "stessa base e il fattoriale: (n+1)! = (n+1)·n!):",
               r"\frac{|a_{n+1}|}{|a_n|}=\frac{2^{n+2}}{3^{n+3}(n+1)!}\cdot\frac{3^{n+2}\,n!}{2^{n+1}}"
               r"=\frac{2}{3(n+1)}"),
        _passo("Passo 3 — limite del rapporto per n→∞:",
               r"\lim_{n\to\infty}\frac{|a_{n+1}|}{|a_n|}=\lim_{n\to\infty}\frac{2}{3(n+1)}=" + _tex(lim)),
        _passo("Passo 4 — per il criterio del rapporto, essendo il limite 0<1 la serie dei moduli "
               "converge: la serie data converge assolutamente, quindi converge (a segni alterni non "
               "servono ulteriori verifiche con Leibniz).",
               r"L=0<1\ \Rightarrow\ \sum|a_n|\ \text{converge}\ \Rightarrow\ \textbf{CONVERGE}"),
        _passo("Per curiosità si può anche calcolare la somma: raccogliendo 2/9 compare lo sviluppo di "
               "e^t con t=−2/3 (privato del termine n=0, che vale 1):",
               r"\sum_{n\ge1}(-1)^n\frac{2^{n+1}}{3^{n+2}n!}=\frac29\sum_{n\ge1}\frac{(-2/3)^n}{n!}"
               r"=\frac29\left(e^{-2/3}-1\right)\approx" + f"{float(sp.N(somma)):.4f}"),
    ]
    return _serie_scelta("11 settembre 2025", testo, tl, passi, "converge",
                         "Scrivi 'converge' o 'diverge'.")


ESAME["serie"].append(_serie_alterna_fattoriale())


# ===========================================================================
# SERIE -- 18 settembre 2025, Es. 3: criterio del rapporto
# ===========================================================================
def _serie_rapporto_18set():
    a_n = sp.factorial(n_)**2 / 2**(n_**2)
    rapp = sp.simplify(sp.expand_func(a_n.subs(n_, n_ + 1) / a_n))
    lim = sp.limit(rapp, n_, sp.oo)
    testo = ("[18 settembre 2025, Esercizio 3] Utilizzando SOLO il criterio del rapporto, studiare il "
             "carattere della seguente serie: Σ (n≥1) (n!)² / 2^(n²).")
    tl = r"\sum_{n\ge1}\frac{(n!)^2}{2^{n^2}}"
    passi = [
        _passo("Serie:", tl),
        _passo("Passo 1 — termini positivi con fattoriali ed esponenziali: applichiamo il criterio del "
               "rapporto, quindi calcoliamo a_{n+1}/a_n. Usiamo ((n+1)!)² = (n+1)²(n!)² e "
               "(n+1)² = n²+2n+1 nell'esponente di 2:",
               r"\frac{a_{n+1}}{a_n}=\frac{((n+1)!)^2}{2^{(n+1)^2}}\cdot\frac{2^{n^2}}{(n!)^2}"
               r"=\frac{(n+1)^2\,2^{n^2}}{2^{n^2+2n+1}}"),
        _passo("Passo 2 — rapporto semplificato: si elidono le potenze di 2 (2^{n²}):",
               r"\frac{a_{n+1}}{a_n}=\frac{(n+1)^2}{2^{2n+1}}=" + _tex(rapp)),
        _passo("Passo 3 — limite del rapporto per n→∞: l'esponenziale 2^{2n+1} cresce molto più "
               "velocemente di qualunque polinomio, quindi il rapporto tende a 0:",
               r"\lim_{n\to\infty}\frac{(n+1)^2}{2^{2n+1}}=" + _tex(lim)),
        _passo("Passo 4 — per il criterio del rapporto, essendo il limite 0<1, la serie CONVERGE.",
               r"L=0<1\ \Rightarrow\ \textbf{CONVERGE}"),
    ]
    return _serie_scelta("18 settembre 2025", testo, tl, passi, "converge",
                         "Scrivi 'converge' o 'diverge'.")


ESAME["serie"].append(_serie_rapporto_18set())


# ===========================================================================
# SERIE GEOMETRICHE CON PARAMETRO x
# ===========================================================================
_X = sp.symbols('x')


def _geom_g1():
    q = 1 / (3 * _X**2 - 1)
    testo = ("[maggio 2025, Esercizio 3] Data la seguente serie geometrica Σ (n≥0) [1/(3x²−1)]^n, "
             "determinare per quali valori di x la serie converge. (Per la verifica automatica: indica "
             "se per x=1/2 la serie CONVERGE o DIVERGE — la discussione per ogni x è nei passaggi.)")
    tl = r"\sum_{n\ge0}\left(\frac{1}{3x^2-1}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per 3x²−1≠0. Imponiamo |q(x)|<1, cioè |3x²−1|>1 "
               "(passando ai reciproci la disuguaglianza si inverte):",
               r"\left|\frac{1}{3x^2-1}\right|<1 \iff |3x^2-1|>1"),
        _passo("Passo 4 — togliamo il valore assoluto: due casi, 3x²−1>1 oppure 3x²−1<−1:",
               r"3x^2-1>1 \ \text{ oppure }\ 3x^2-1<-1 \iff x^2>\frac23\ \text{ oppure }\ x^2<0"),
        _passo("Passo 5 — il secondo caso (x²<0) è impossibile; resta x²>2/3, cioè |x|>√(2/3)=√6/3:",
               r"x^2>\frac23 \iff x<-\frac{\sqrt6}{3}\ \text{ oppure }\ x>\frac{\sqrt6}{3}"),
    ]
    return _serie_geom_param(
        "maggio 2025", testo, tl, q, 0, alg,
        "Conclusione — la serie converge per |x|>√6/3 (zone dove |q(x)|<1); diverge altrove "
        "(compresi i punti x=±√3/3, dove la ragione non è definita, e il caso |q|≥1):",
        r"\textbf{converge per } x<-\frac{\sqrt6}{3}\ \text{ o }\ x>\frac{\sqrt6}{3},\qquad "
        r"\textbf{diverge per } |x|\le\frac{\sqrt6}{3}",
        sp.Rational(1, 2))


ESAME["serie"].append(_geom_g1())


def _geom_g2():
    q = 1 / (1 - sp.log(-_X))
    testo = ("[maggio 2025, Esercizio 3] Data la seguente serie geometrica Σ (n≥0) "
             "[1/(1−ln(−x))]^n, determinare per quali valori di x la serie converge. (Per la verifica "
             "automatica: indica se per x=−2 la serie CONVERGE o DIVERGE.)")
    tl = r"\sum_{n\ge0}\left(\frac{1}{1-\ln(-x)}\right)^n"
    alg = [
        _passo("Passo 3 — |q(x)|<1 equivale a |1−ln(−x)|>1 (reciproci). Con t=ln(−x) significa "
               "|1−t|>1:",
               r"\left|\frac{1}{1-\ln(-x)}\right|<1 \iff |1-\ln(-x)|>1"),
        _passo("Passo 4 — due casi: 1−t>1 oppure 1−t<−1, cioè t<0 oppure t>2:",
               r"1-t>1 \iff t<0,\qquad 1-t<-1 \iff t>2"),
        _passo("Passo 5 — torniamo a x: ln(−x)<0 ⇔ 0<−x<1, mentre ln(−x)>2 ⇔ −x>e². Quindi, "
               "ricordando che ln(−x) richiede x<0:",
               r"\ln(-x)<0 \iff -1<x<0,\qquad \ln(-x)>2 \iff x<-e^2"),
    ]
    return _serie_geom_param(
        "maggio 2025", testo, tl, q, 0, alg,
        "Conclusione — la serie converge per −1<x<0 oppure x<−e²; diverge per −e²≤x≤−1 "
        "(dove |q|≥1; in x=−e la ragione non è definita) e non è definita per x≥0:",
        r"\textbf{converge per } x\in(-\infty,-e^2)\cup(-1,0)",
        sp.Integer(-2),
        nota_dominio="Dominio della ragione: ln(−x) richiede x<0, e il denominatore deve essere ≠0: "
                     "1−ln(−x)≠0 ⇔ x≠−e.",
        nota_dominio_latex=r"x<0,\qquad 1-\ln(-x)\ne0 \iff x\ne-e")


ESAME["serie"].append(_geom_g2())


def _geom_g3():
    q = 1 / (1 - 2 * _X**2)
    testo = ("[maggio 2025, Esercizio 3] Data la serie Σ (n≥0) [1/(1−2x²)]^n: a) determinare per quali "
             "valori di x essa converge; b) calcolarne la somma. (Per la verifica automatica: indica "
             "la somma per x=2.)")
    tl = r"\sum_{n\ge0}\left(\frac{1}{1-2x^2}\right)^n"
    alg = [
        _passo("Passo 3 — |q(x)|<1 equivale a |1−2x²|>1 (la ragione è definita per x²≠1/2):",
               r"\left|\frac{1}{1-2x^2}\right|<1 \iff |1-2x^2|>1"),
        _passo("Passo 4 — due casi: 1−2x²>1 oppure 1−2x²<−1:",
               r"1-2x^2>1 \iff x^2<0\ (\text{impossibile}),\qquad 1-2x^2<-1 \iff x^2>1"),
        _passo("Passo 5 — resta solo x²>1, cioè |x|>1:", r"x<-1\ \text{ oppure }\ x>1"),
    ]
    return _serie_geom_param(
        "maggio 2025", testo, tl, q, 0, alg,
        "Conclusione a) — la serie converge per |x|>1; diverge per |x|≤1 (con x=±1/√2 punti in cui la "
        "ragione non esiste):",
        r"\textbf{converge per } x<-1\ \text{ o }\ x>1",
        sp.Integer(2), con_somma=True)


ESAME["serie"].append(_geom_g3())


def _geom_g4():
    q = 1 / (1 - 4 * _X**2)
    testo = ("[gennaio 2025, Esercizio 2] Data la seguente serie geometrica Σ (n≥0) [1/(1−4x²)]^n, "
             "determinare per quali valori di x la serie converge e calcolarne la somma (la richiesta "
             "della somma compare in Aprile 2024; Dicembre 2024 chiede solo la convergenza). (Per la "
             "verifica automatica: indica la somma per x=1.)")
    tl = r"\sum_{n\ge0}\left(\frac{1}{1-4x^2}\right)^n"
    alg = [
        _passo("Passo 3 — |q(x)|<1 equivale a |1−4x²|>1 (la ragione è definita per x²≠1/4):",
               r"\left|\frac{1}{1-4x^2}\right|<1 \iff |1-4x^2|>1"),
        _passo("Passo 4 — due casi: 1−4x²>1 (impossibile, darebbe x²<0) oppure 1−4x²<−1, cioè x²>1/2:",
               r"1-4x^2<-1 \iff x^2>\frac12 \iff |x|>\frac{\sqrt2}{2}"),
    ]
    return _serie_geom_param(
        "gennaio 2025", testo, tl, q, 0, alg,
        "Conclusione — la serie converge per |x|>√2/2 e diverge per |x|≤√2/2:",
        r"\textbf{converge per } x<-\frac{\sqrt2}{2}\ \text{ o }\ x>\frac{\sqrt2}{2}",
        sp.Integer(1), con_somma=True)


ESAME["serie"].append(_geom_g4())


def _geom_g5():
    q = (1 + _X + _X**2) / (1 + _X)
    testo = ("[gennaio 2025, Esercizio 5] Data la seguente serie geometrica Σ (n≥1) "
             "[(1+x+x²)/(1+x)]^n, determinare per quali valori di x la serie converge. (Per la "
             "verifica automatica: indica se per x=−2 la serie CONVERGE o DIVERGE. Stesso testo in "
             "Ottobre 2024, n.11.)")
    tl = r"\sum_{n\ge1}\left(\frac{1+x+x^2}{1+x}\right)^n"
    alg = [
        _passo("Passo 3 — il numeratore x²+x+1 ha discriminante negativo, quindi è sempre positivo; "
               "il segno della ragione q(x) è quindi quello di x+1 (x≠−1):",
               r"\Delta=1-4=-3<0\ \Rightarrow\ x^2+x+1>0\ \ \forall x"),
        _passo("Passo 4 — caso x>−1: q(x)>0, quindi |q|<1 equivale a q<1, cioè x²+x+1<x+1 ⇔ x²<0, "
               "IMPOSSIBILE. (Anzi q(x)≥1 sempre, con q(0)=1.)",
               r"q<1 \iff x^2+x+1<x+1 \iff x^2<0\ \ (\text{mai})"),
        _passo("Passo 5 — caso x<−1: q(x)<0, quindi |q|<1 equivale a q>−1. Moltiplicando per x+1<0 la "
               "disuguaglianza si inverte: x²+x+1<−(x+1) ⇔ x²+2x+2<0 ⇔ (x+1)²+1<0, ancora "
               "IMPOSSIBILE.",
               r"q>-1 \iff x^2+x+1<-(x+1) \iff (x+1)^2+1<0\ \ (\text{mai})"),
    ]
    return _serie_geom_param(
        "gennaio 2025", testo, tl, q, 1, alg,
        "Conclusione — in nessun caso |q(x)|<1: la serie NON converge per alcun x reale (diverge per "
        "ogni x≠−1; per x=−1 non è definita):",
        r"|q(x)|\ge1\ \ \forall x\ne-1\ \Rightarrow\ \textbf{la serie diverge per ogni } x\ne-1",
        sp.Integer(-2),
        nota_dominio="La ragione è definita per x≠−1 (denominatore).",
        nota_dominio_latex=r"x+1\ne0")


ESAME["serie"].append(_geom_g5())


def _geom_g6():
    q = (_X + 2) / (1 - _X)
    testo = ("[gennaio 2025, Esercizio 8] Data la seguente serie geometrica Σ (n≥1) [(x+2)/(1−x)]^n, "
             "determinare per quali valori di x la serie converge e calcolarne la somma (la somma è "
             "richiesta nel compito di Luglio 2024, per n≥0, con lo stesso criterio). (Per la "
             "verifica automatica: indica la somma, con n da 1, per x=−1.)")
    tl = r"\sum_{n\ge1}\left(\frac{x+2}{1-x}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per x≠1. Imponiamo |q(x)|<1, cioè |x+2|<|1−x|; "
               "elevando al quadrato (entrambi i membri sono ≥0, quindi l'equivalenza vale):",
               r"|x+2|<|1-x| \iff (x+2)^2<(1-x)^2"),
        _passo("Passo 4 — sviluppiamo i quadrati: i termini in x² si elidono:",
               r"x^2+4x+4<1-2x+x^2 \iff 6x<-3 \iff x<-\frac12"),
    ]
    return _serie_geom_param(
        "gennaio 2025", testo, tl, q, 1, alg,
        "Conclusione — la serie converge per x<−1/2 e diverge per x≥−1/2 (x=1 escluso):",
        r"\textbf{converge per } x<-\frac12",
        sp.Integer(-1), con_somma=True)


ESAME["serie"].append(_geom_g6())


def _geom_g7():
    q = (2 + _X) / (3 - _X)
    testo = ("[luglio 2024, Serie n.1] Data la serie Σ (n≥0) [(2+x)/(3−x)]^n: determinare per quali "
             "valori di x essa converge e calcolarne la somma. (Per la verifica automatica: indica la "
             "somma per x=0.)")
    tl = r"\sum_{n\ge0}\left(\frac{2+x}{3-x}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per x≠3. Imponiamo |q(x)|<1 ⇔ |2+x|<|3−x| ⇔ "
               "(2+x)²<(3−x)² (elevando al quadrato):",
               r"(2+x)^2<(3-x)^2 \iff 4x+4<9-6x"),
        _passo("Passo 4 — i termini in x² si elidono e resta una disequazione di primo grado:",
               r"10x<5 \iff x<\frac12"),
    ]
    return _serie_geom_param(
        "luglio 2024", testo, tl, q, 0, alg,
        "Conclusione — la serie converge per x<1/2 (x=3 non è nell'insieme) e diverge per x≥1/2:",
        r"\textbf{converge per } x<\frac12",
        sp.Integer(0), con_somma=True)


ESAME["serie"].append(_geom_g7())


def _geom_g8():
    q = (2 + _X) / (1 - _X)
    testo = ("[luglio 2024, Serie n.2] Data la serie Σ (n≥0) [(2+x)/(1−x)]^n: determinare per quali "
             "valori di x essa converge e calcolarne la somma. (Per la verifica automatica: indica la "
             "somma per x=−2.)")
    tl = r"\sum_{n\ge0}\left(\frac{2+x}{1-x}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per x≠1. Imponiamo |q(x)|<1 ⇔ |2+x|<|1−x| ⇔ "
               "(2+x)²<(1−x)²:",
               r"x^2+4x+4<x^2-2x+1 \iff 6x<-3 \iff x<-\frac12"),
    ]
    return _serie_geom_param(
        "luglio 2024", testo, tl, q, 0, alg,
        "Conclusione — la serie converge per x<−1/2:",
        r"\textbf{converge per } x<-\frac12",
        sp.Integer(-2), con_somma=True)


ESAME["serie"].append(_geom_g8())


def _geom_g9():
    q = 1 / (1 - sp.exp(_X))
    testo = ("[dicembre 2024, Serie n.1] Data la serie Σ (n≥0) [1/(1−e^x)]^n, determinare per quali "
             "valori di x essa converge. (Nel compito di Aprile 2024 compare la variante 1/(e^x−1), "
             "con la richiesta della somma; qui si calcola anche la somma. Per la verifica "
             "automatica: indica la somma per x=ln 3.)")
    tl = r"\sum_{n\ge0}\left(\frac{1}{1-e^x}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per x≠0. Imponiamo |q(x)|<1 ⇔ |1−e^x|>1:",
               r"\left|\frac{1}{1-e^x}\right|<1 \iff |1-e^x|>1"),
        _passo("Passo 4 — due casi: 1−e^x>1 (impossibile, perché e^x>0) oppure 1−e^x<−1, cioè "
               "e^x>2; applicando il logaritmo (funzione crescente):",
               r"1-e^x<-1 \iff e^x>2 \iff x>\ln 2"),
    ]
    return _serie_geom_param(
        "dicembre 2024", testo, tl, q, 0, alg,
        "Conclusione — la serie converge per x>ln 2 e diverge per x≤ln 2:",
        r"\textbf{converge per } x>\ln 2",
        sp.log(3), con_somma=True)


ESAME["serie"].append(_geom_g9())


def _geom_g9b():
    q = 1 / (sp.exp(_X) - 1)
    testo = ("[aprile 2024, Serie n.2] Data la serie Σ (n≥0) [1/(e^x−1)]^n: a) determinare per quali "
             "valori di x essa converge; b) calcolarne la somma. (Per la verifica automatica: indica la "
             "somma per x=ln 3.)")
    tl = r"\sum_{n\ge0}\left(\frac{1}{e^x-1}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per x≠0. Imponiamo |q(x)|<1 ⇔ |e^x−1|>1:",
               r"\left|\frac{1}{e^x-1}\right|<1 \iff |e^x-1|>1"),
        _passo("Passo 4 — due casi: e^x−1>1 ⇔ e^x>2, oppure e^x−1<−1 ⇔ e^x<0 (impossibile). "
               "Con il logaritmo:",
               r"e^x-1>1 \iff e^x>2 \iff x>\ln2"),
    ]
    return _serie_geom_param(
        "aprile 2024", testo, tl, q, 0, alg,
        "Conclusione a) — la serie converge per x>ln 2 e diverge per x≤ln 2:",
        r"\textbf{converge per } x>\ln 2",
        sp.log(3), con_somma=True)


ESAME["serie"].append(_geom_g9b())


def _geom_g10():
    q = (_X - 1) / _X
    testo = ("[ottobre 2024, Esercizio 17] Data la seguente serie geometrica Σ (n≥1) [(x−1)/x]^n, "
             "determinare per quali valori di x la serie converge. (Per la verifica automatica: indica "
             "la somma della serie, con n da 1, per x=2; la somma completa per ogni x è nei passaggi.)")
    tl = r"\sum_{n\ge1}\left(\frac{x-1}{x}\right)^n"
    alg = [
        _passo("Passo 3 — la ragione è definita per x≠0. Imponiamo |q(x)|<1 ⇔ |x−1|<|x| ⇔ "
               "(x−1)²<x² (elevando al quadrato):",
               r"|x-1|<|x| \iff x^2-2x+1<x^2 \iff 1<2x \iff x>\frac12"),
    ]
    return _serie_geom_param(
        "ottobre 2024", testo, tl, q, 1, alg,
        "Conclusione — la serie converge per x>1/2 (x=0 è escluso automaticamente) e diverge per "
        "x≤1/2:",
        r"\textbf{converge per } x>\frac12",
        sp.Integer(2), con_somma=True)


ESAME["serie"].append(_geom_g10())


def _geom_g11():
    q = 1 / (1 - sp.log(_X))
    testo = ("[aprile 2024, Serie n.4] Data la serie Σ (n≥1) [1/(1−log x)]^n: a) determinare per quali "
             "valori di x essa converge; b) calcolarne la somma. (Per la verifica automatica: indica la "
             "somma, con n da 1, per x=e³.)")
    tl = r"\sum_{n\ge1}\left(\frac{1}{1-\log x}\right)^n"
    alg = [
        _passo("Passo 3 — |q(x)|<1 equivale a |1−log x|>1. Due casi (con t=log x): 1−t>1 ⇔ t<0, "
               "oppure 1−t<−1 ⇔ t>2:",
               r"\log x<0\ \text{ oppure }\ \log x>2"),
        _passo("Passo 4 — torniamo a x (log richiede x>0, e e^t è crescente): "
               "log x<0 ⇔ 0<x<1, log x>2 ⇔ x>e²:",
               r"0<x<1\ \text{ oppure }\ x>e^2"),
    ]
    return _serie_geom_param(
        "aprile 2024", testo, tl, q, 1, alg,
        "Conclusione a) — la serie converge per 0<x<1 oppure x>e²; diverge per 1≤x≤e² (dove "
        "|q|≥1, con x=e escluso perché la ragione non è definita). Il risultato stampato nel PDF "
        "dice 'x<1 ∨ x>e²', ma bisogna ricordare la condizione di esistenza x>0:",
        r"\textbf{converge per } x\in(0,1)\cup(e^2,+\infty)",
        sp.exp(3), con_somma=True,
        nota_dominio="Condizioni di esistenza: log x richiede x>0 e il denominatore deve essere ≠0, "
                     "cioè 1−log x≠0 ⇔ x≠e.",
        nota_dominio_latex=r"x>0,\qquad x\ne e")


ESAME["serie"].append(_geom_g11())


# ===========================================================================
# SERIE TELESCOPICHE E ALTRO
# ===========================================================================
_N = sp.symbols('N', positive=True, integer=True)


def _tele_2n1():
    termine = 1 / ((2 * n_ - 1) * (2 * n_ + 1))
    testo = ("[maggio 2025, Esercizio 3] Data la serie Σ (n≥1) 1/((2n−1)(2n+1)): a) verificare che si "
             "tratta della serie telescopica e calcolarne la somma; b) trovare una serie che abbia per "
             "somma 3/7. (Stessa serie scritta come 1/(4n²−1) nel compito di Maggio 2024; con S=1/2 "
             "in Aprile 2024.)")
    tl = r"\sum_{n\ge1}\frac{1}{(2n-1)(2n+1)}"
    extra = [
        _passo("Parte b) — per ottenere una serie con somma assegnata 3/7 scegliamo la serie "
               "geometrica Σ (n≥1) q^n, la cui somma è q/(1−q) (primo termine q, ragione q); "
               "imponiamo che valga 3/7 e ricaviamo la ragione:",
               r"\frac{q}{1-q}=\frac37 \iff 7q=3-3q \iff q=\frac{3}{10}"),
        _passo("Essendo |q|=3/10<1 la serie geometrica di ragione q converge davvero, e la sua somma è quella "
               "richiesta (controllo):",
               r"\sum_{n\ge1}\left(\frac{3}{10}\right)^n=\frac{3/10}{1-3/10}=\frac{3/10}{7/10}=\frac37"),
    ]
    somma, passi = _serie_telescopica_gen(
        "maggio 2025", testo, tl, termine, 1,
        r"(2n-1)(2n+1)=4n^2-1\ \ (\text{già fattorizzato: fattori che differiscono di }2)",
        r"\frac{1}{(2n-1)(2n+1)}=\frac12\left(\frac{1}{2n-1}-\frac{1}{2n+1}\right)\quad"
        r"\left(\tfrac{A}{2n-1}+\tfrac{B}{2n+1}:\ A=\tfrac12,\ B=-\tfrac12\right)",
        r"S_N=\frac12\left[\left(1-\frac13\right)+\left(\frac13-\frac15\right)+\dots+"
        r"\left(\frac{1}{2N-1}-\frac{1}{2N+1}\right)\right]=\frac12\left(1-\frac{1}{2N+1}\right)=\frac{N}{2N+1}",
        _N / (2 * _N + 1), None, passi_extra=extra)
    return _voce("maggio 2025", testo, tl,
                 "Scrivi il valore della somma (parte a), es: 1/5.", passi,
                 {"tipo": "numero", "atteso_numero": float(somma), "atteso_display": str(somma)}, None)


ESAME["serie"].append(_tele_2n1())


def _tele_3n2():
    termine = 1 / ((3 * n_ - 2) * (3 * n_ + 1))
    testo = ("[aprile 2024, Serie n.5] Data la serie Σ (n≥1) 1/((3n−2)(3n+1)): a) verificare che si "
             "tratta della serie telescopica e calcolarne la somma; b) trovare una serie che abbia per "
             "somma 5/7.")
    tl = r"\sum_{n\ge1}\frac{1}{(3n-2)(3n+1)}"
    extra = [
        _passo("Parte b) — cerchiamo una serie geometrica Σ (n≥0) q^n, la cui somma è 1/(1−q) "
               "(primo termine 1, ragione q); imponiamo che valga 5/7:",
               r"\frac{1}{1-q}=\frac57 \iff 5-5q=7 \iff q=-\frac25"),
        _passo("Essendo |q|=2/5<1 la serie geometrica di ragione q converge e ha davvero somma 5/7 (controllo):",
               r"\sum_{n\ge0}\left(-\frac25\right)^n=\frac{1}{1+2/5}=\frac57"),
    ]
    somma, passi = _serie_telescopica_gen(
        "aprile 2024", testo, tl, termine, 1,
        r"(3n-2)(3n+1)\ \ (\text{già fattorizzato: i due fattori differiscono di }3)",
        r"\frac{1}{(3n-2)(3n+1)}=\frac13\left(\frac{1}{3n-2}-\frac{1}{3n+1}\right)\quad"
        r"\left(A=\tfrac13,\ B=-\tfrac13\right)",
        r"S_N=\frac13\left[\left(1-\frac14\right)+\left(\frac14-\frac17\right)+\dots+"
        r"\left(\frac{1}{3N-2}-\frac{1}{3N+1}\right)\right]=\frac13\left(1-\frac{1}{3N+1}\right)",
        (1 - 1 / (3 * _N + 1)) / 3, None, passi_extra=extra)
    return _voce("aprile 2024", testo, tl,
                 "Scrivi il valore della somma (parte a), es: 1/5.", passi,
                 {"tipo": "numero", "atteso_numero": float(somma), "atteso_display": str(somma)}, None)


ESAME["serie"].append(_tele_3n2())


def _tele_n_n3():
    termine = 1 / (n_ * (n_ + 3))
    testo = ("[maggio 2024, Serie n.4] Data la serie Σ (n≥1) 1/(n(n+3)): verificare che si tratta "
             "della serie telescopica e studiarne il carattere.")
    tl = r"\sum_{n\ge1}\frac{1}{n(n+3)}"
    somma, passi = _serie_telescopica_gen(
        "maggio 2024", testo, tl, termine, 1,
        r"n(n+3)\ \ (\text{già fattorizzato: i due fattori differiscono di }3)",
        r"\frac{1}{n(n+3)}=\frac13\left(\frac1n-\frac{1}{n+3}\right)\quad\left(A=\tfrac13,\ B=-\tfrac13\right)",
        r"S_N=\frac13\sum_{n=1}^{N}\left(\frac1n-\frac{1}{n+3}\right)=\frac13\left[1+\frac12+\frac13-"
        r"\left(\frac{1}{N+1}+\frac{1}{N+2}+\frac{1}{N+3}\right)\right]",
        (sp.Rational(11, 6) - 1 / (_N + 1) - 1 / (_N + 2) - 1 / (_N + 3)) / 3, None,
        passi_extra=[_passo("Quindi la somma parziale S_N tende a un limite finito: la serie CONVERGE e ha per somma 1/3·(1+1/2+1/3):",
                            r"S=\frac13\cdot\frac{11}{6}=\frac{11}{18}\ \Rightarrow\ \textbf{CONVERGE}")])
    return _serie_scelta("maggio 2024", testo, tl, passi, "converge", "Scrivi 'converge' o 'diverge'.")


ESAME["serie"].append(_tele_n_n3())


def _tele_3_n2_3n():
    termine = 3 / (n_**2 + 3 * n_)
    testo = ("[maggio 2024, Serie n.2] Data la serie Σ 3/(n²+3n) (la somma parte da n=1: per n=0 il "
             "termine non è definito, quindi lo 0 scritto nel testo è un refuso): a) verificare se si "
             "tratta di una serie telescopica; b) calcolare la somma dei primi tre termini.")
    tl = r"\sum_{n\ge1}\frac{3}{n^2+3n}"
    somma, passi = _serie_telescopica_gen(
        "maggio 2024", testo, tl, termine, 1,
        r"n^2+3n=n(n+3)",
        r"\frac{3}{n(n+3)}=\frac1n-\frac{1}{n+3}\quad(A=1,\ B=-1)",
        r"S_N=\sum_{n=1}^{N}\left(\frac1n-\frac{1}{n+3}\right)=1+\frac12+\frac13-"
        r"\left(\frac{1}{N+1}+\frac{1}{N+2}+\frac{1}{N+3}\right)",
        sp.Rational(11, 6) - 1 / (_N + 1) - 1 / (_N + 2) - 1 / (_N + 3), None)
    s3 = sum(termine.subs(n_, k) for k in (1, 2, 3))
    assert s3 == sp.Rational(73, 60)
    passi.append(_passo("Parte b) — somma dei primi tre termini (n=1,2,3): basta sommare i tre termini "
                        "(oppure usare S_3 con la formula della somma parziale, N=3):",
                        r"S_3=\frac34+\frac{3}{10}+\frac{3}{18}=\frac34+\frac{3}{10}+\frac16=\frac{73}{60}"
                        r"\ \left(=\tfrac{11}{6}-\tfrac14-\tfrac15-\tfrac16\right)"))
    return _voce("maggio 2024", testo, tl,
                 "Scrivi la somma dei primi tre termini (parte b), es: 3/5.", passi,
                 {"tipo": "numero", "atteso_numero": float(s3), "atteso_display": str(s3)}, None)


ESAME["serie"].append(_tele_3_n2_3n())


def _serie_maggio2024_AB():
    A = (2 + n_) / (1 + n_ + n_)
    B = (-1)**n_ * (2 + n_) / (1 + n_ + n_**2)
    limA = sp.limit(A, n_, sp.oo)
    assert limA == sp.Rational(1, 2)
    t = sp.symbols('t', positive=True)
    fb = (t + 2) / (t**2 + t + 1)
    derb = sp.simplify(sp.diff(fb, t))
    assert sp.simplify(derb + (t**2 + 4*t + 1) / (t**2 + t + 1)**2) == 0
    testo = ("[maggio 2024, Serie n.1] Date le serie (A) Σ (n≥1) (2+n)/(1+n+n) e (B) Σ (n≥1) "
             "(−1)^n (2+n)/(1+n+n²): studiare il carattere di A e di B specificando il criterio "
             "utilizzato. (Il denominatore di A è riportato nel testo come 1+n+n: se fosse 1+n+n² "
             "l'esito resterebbe divergente, per confronto asintotico con la serie armonica.) "
             "(Per la verifica automatica: indica il carattere della serie A.)")
    tl = (r"(A)\ \sum_{n\ge1}\frac{2+n}{1+n+n}\qquad (B)\ \sum_{n\ge1}(-1)^n\frac{2+n}{1+n+n^2}")
    passi = [
        _passo("Serie:", tl),
        _passo("Serie A, passo 1 — condizione necessaria: studiamo il termine generale a_n e il suo limite "
               "per n→∞ (se non tende a 0 la serie non può convergere). Qui il denominatore è 1+2n:",
               r"a_n=\frac{2+n}{1+2n}\ \Rightarrow\ \lim_{n\to\infty}a_n=" + _tex(limA)),
        _passo("Serie A, passo 2 — il termine generale tende a 1/2≠0, quindi la serie a termini "
               "positivi DIVERGE (condizione necessaria di convergenza violata).",
               r"\lim a_n=\frac12\ne0\ \Rightarrow\ \textbf{A DIVERGE}"),
        _passo("Serie B, passo 1 — è a segni alterni: poniamo b_n=(n+2)/(n²+n+1)>0 e applichiamo il "
               "criterio di Leibniz (sez. 9.2): serve b_n→0 e b_n decrescente.",
               r"b_n=\frac{n+2}{n^2+n+1},\qquad \lim_{n\to\infty}b_n=0"),
        _passo("Serie B, passo 2 — Leibniz richiede la decrescenza: la funzione f(t)=(t+2)/(t²+t+1) ha derivata negativa per "
               "t>0, quindi b_n è decrescente:",
               r"f'(t)=\frac{-(t^2+4t+1)}{(t^2+t+1)^2}<0\ \ (t>0)"),
        _passo("Serie B, passo 3 — per il criterio di Leibniz la serie B CONVERGE. Non converge "
               "assolutamente: |(−1)^n b_n|=b_n ~ 1/n e la serie armonica diverge (confronto "
               "asintotico), quindi converge solo semplicemente.",
               r"\lim_{n\to\infty}\frac{b_n}{1/n}=1\ \Rightarrow\ \sum b_n\ \text{diverge};\quad"
               r"\textbf{B converge (non assolutamente)}"),
    ]
    return _serie_scelta("maggio 2024", testo, tl, passi, "diverge",
                         "Scrivi 'converge' o 'diverge' (riferito alla serie A).")


ESAME["serie"].append(_serie_maggio2024_AB())


# ===========================================================================
# CONTINUITA' / DIFFERENZIABILITA' / PIANO TANGENTE -- helper
# ===========================================================================
def _png_cont(f_expr, continua, differenziabile):
    try:
        fig = _grafico.grafico_continuita({"f": f_expr, "continua": continua,
                                           "differenziabile": differenziabile})
        return _png(fig)
    except Exception:
        return None


def _chk_pol(f_expr, f_pol, tol=1e-8):
    """Controlla (numericamente) che l'espressione in coordinate polari f_pol(r,theta) coincida
    con f(x,y) dopo x=r cos(theta), y=r sin(theta): evita refusi nei passaggi."""
    for rv, tv in [(0.3, 0.4), (0.7, 2.0), (0.2, 4.0), (0.5, 5.5), (0.9, 1.1)]:
        a = complex(sp.N(f_expr.subs({x: rv * sp.cos(tv), y: rv * sp.sin(tv)})))
        b = complex(sp.N(f_pol.subs({r_: rv, th_: tv})))
        assert abs(a - b) < tol, (f_expr, rv, tv, a, b)


def _voce_cont(fonte, testo, tl, passi, f_graf, continua, differenziabile, sugg=None):
    return _voce(fonte, testo, tl, sugg or "Scrivi: continua, non differenziabile",
                 passi, {"tipo": "continuita", "continua": continua,
                         "differenziabile": differenziabile},
                 _png_cont(f_graf, continua, differenziabile))


def _piano_passi(f_expr, px, py, intro, nome="f"):
    """Passi 'piano tangente' nel punto (px,py): derivate parziali, valori, equazione z=..."""
    fx = sp.diff(f_expr, x)
    fy = sp.diff(f_expr, y)
    sub = {x: px, y: py}
    f0 = sp.simplify(f_expr.subs(sub))
    fx0 = sp.simplify(fx.subs(sub))
    fy0 = sp.simplify(fy.subs(sub))
    piano = sp.expand(f0 + fx0 * (x - px) + fy0 * (y - py))
    P = f"({_tex(px)},{_tex(py)})"
    return [
        _passo(intro + " Le derivate parziali prime sono continue in un intorno di " + P +
               " (f è composta di funzioni elementari derivabili con continuità): per il teorema del "
               "differenziale totale f è differenziabile in quel punto e il PIANO TANGENTE esiste, di "
               "equazione z = f(x0,y0) + f_x(x0,y0)(x−x0) + f_y(x0,y0)(y−y0) (formulario ufficiale).",
               r"z=f(x_0,y_0)+f_x(x_0,y_0)(x-x_0)+f_y(x_0,y_0)(y-y_0),\quad (x_0,y_0)=" + P),
        _passo("Derivate parziali prime (regole di derivazione di prodotti, composte e quozienti):",
               r"f_x=" + _tex(sp.simplify(fx)) + r",\qquad f_y=" + _tex(sp.simplify(fy))),
        _passo("Valori di f e delle derivate parziali nel punto " + P + ":",
               f"f{P}={_tex(f0)},\\quad f_x{P}={_tex(fx0)},\\quad f_y{P}={_tex(fy0)}"),
        _passo("Sostituiamo nella formula: equazione del piano tangente al grafico in " + P + ":",
               "z=" + _tex(f0) + "+(" + _tex(fx0) + r")\,(x-(" + _tex(px) + r"))+(" + _tex(fy0)
               + r")\,(y-(" + _tex(py) + r"))\ \Longrightarrow\ z=" + _tex(piano)),
    ], piano


# ===========================================================================
# CONTINUITA' -- 16 maggio 2026 (+ 29 ottobre 2025, dicembre 2021): x y/sqrt(x^2+y^2) e^{x^2/(x^2+y^2)}
# ===========================================================================
def _cont_16mag():
    f = x * y / sp.sqrt(x**2 + y**2) * sp.exp(x**2 / (x**2 + y**2))
    f_pol = r_ * sp.sin(th_) * sp.cos(th_) * sp.exp(sp.cos(th_)**2)
    _chk_pol(f, f_pol)
    fx_f = y**3 * (3 * x**2 + y**2) / (x**2 + y**2)**sp.Rational(5, 2) * sp.exp(x**2 / (x**2 + y**2))
    fy_f = x**3 * (x**2 - y**2) / (x**2 + y**2)**sp.Rational(5, 2) * sp.exp(x**2 / (x**2 + y**2))
    assert sp.simplify(sp.diff(f, x) - fx_f) == 0 and sp.simplify(sp.diff(f, y) - fy_f) == 0
    testo = ("[16 maggio 2026, Esercizio 1] Data la funzione f(x,y) = xy/√(x²+y²)·e^(x²/(x²+y²)) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in R² e calcolare le "
             "derivate parziali generiche (non sono ammesse maggiorazioni). Nella variante del 29 ottobre "
             "2025 (stessa funzione, presente anche in Dicembre 2021) si chiede inoltre il piano tangente "
             "nel punto (1;0).")
    tl = (r"f(x,y)=\begin{cases}\dfrac{xy}{\sqrt{x^2+y^2}}\,e^{\frac{x^2}{x^2+y^2}} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    piano_p, piano = _piano_passi(f, sp.Integer(1), sp.Integer(0),
                                  "Passo 5 — piano tangente nel punto (1;0), lontano dall'origine: là il "
                                  "denominatore x²+y² vale 1≠0.")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ (r>0) "
               "e studiamo il limite per r→0⁺. Il fattore xy/√(x²+y²) diventa r sinθ cosθ e "
               "l'esponente x²/(x²+y²) diventa cos²θ, che non dipende da r:",
               r"f(r,\theta)=r\sin\theta\cos\theta\,e^{\cos^2\theta}"),
        _passo("Il fattore g(θ)=sinθ cosθ e^{cos²θ} è una funzione continua e limitata di θ, "
               "indipendente da r, quindi f(r,θ)=r·g(θ)→0 per r→0⁺ UNIFORMEMENTE in θ: "
               "il limite esiste, vale 0=f(0,0) e f è CONTINUA in (0,0).",
               r"\lim_{r\to0^+}r\,g(\theta)=0=f(0,0)\ \Rightarrow\ \textbf{continua in }(0,0)"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione (rapporto incrementale lungo gli "
               "assi): sull'asse x (y=0) e sull'asse y (x=0) la funzione è identicamente nulla, quindi",
               r"f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=\lim_{h\to0}\frac{0}{h}=0,\qquad "
               r"f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-f(0,0)}{h}=0"),
        _passo("Passo 3 — test di differenziabilità: calcoliamo il resto diviso r, cioè "
               "[f − f_x(0,0)x − f_y(0,0)y]/√(x²+y²), in coordinate polari:",
               r"\frac{f(x,y)-0\cdot x-0\cdot y}{\sqrt{x^2+y^2}}=\frac{r\,g(\theta)}{r}="
               r"\sin\theta\cos\theta\,e^{\cos^2\theta}"),
        _passo("Il limite per r→0⁺ DIPENDE da θ: per θ=0 vale 0, ma per θ=π/4 vale (1/2)e^{1/2}≈0,82≠0. "
               "Quindi il resto diviso r non tende a 0: f NON è differenziabile in (0,0).",
               r"\theta=0:\ 0\qquad\ne\qquad\theta=\frac\pi4:\ \frac12\,e^{1/2}\approx0{,}82"
               r"\ \Rightarrow\ \textbf{continua ma NON differenziabile in }(0,0)"),
        _passo("Passo 4 — derivate parziali generiche (per (x,y)≠(0,0)): derivando il prodotto e la "
               "composta e semplificando (x²+y²)^{1/2}·(x²+y²)² = (x²+y²)^{5/2}:",
               r"f_x=\frac{y^3(3x^2+y^2)}{(x^2+y^2)^{5/2}}\,e^{\frac{x^2}{x^2+y^2}},\qquad "
               r"f_y=\frac{x^3(x^2-y^2)}{(x^2+y^2)^{5/2}}\,e^{\frac{x^2}{x^2+y^2}}"),
        _passo("Osservazione: le derivate parziali non sono continue in (0,0) (per esempio lungo y=x "
               "f_x vale una costante ≠0=f_x(0,0)): coerente con la non differenziabilità, perché C¹ "
               "implicherebbe differenziabile.",
               r"f_x(x,x)=\frac{x^3\cdot4x^2}{(2x^2)^{5/2}}e^{1/2}=\frac{\sqrt2}{2}\,e^{1/2}\ \ (x>0)"
               r"\ \not\to\ 0"),
    ] + piano_p
    return _voce_cont("16 maggio 2026", testo, tl, passi, f, True, False,
                      "Scrivi: continua, non differenziabile (riferito all'origine)")


ESAME["continuita"].append(_cont_16mag())


# ===========================================================================
# CONTINUITA' -- 14 maggio 2026 (+ 10 aprile 2026, maggio 2025): (1-cos(y+sin x))/sin(sqrt(x^2+y^2))
# ===========================================================================
def _cont_14mag():
    f = (1 - sp.cos(y + sp.sin(x))) / sp.sin(sp.sqrt(x**2 + y**2))
    f_pol = (1 - sp.cos(r_ * sp.sin(th_) + sp.sin(r_ * sp.cos(th_)))) / sp.sin(r_)
    _chk_pol(f, f_pol)
    testo = ("[14 maggio 2026, Esercizio 1] Data la funzione f(x,y) = (1−cos(y+sin x))/sin(√(x²+y²)) "
             "per (x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in R² (non sono "
             "ammesse maggiorazioni). (Stesso testo del 10 aprile 2026 e di Maggio 2025.)")
    tl = (r"f(x,y)=\begin{cases}\dfrac{1-\cos(y+\sin x)}{\sin\left(\sqrt{x^2+y^2}\right)} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ e "
               "studiamo il limite per r→0⁺. L'argomento del coseno diventa u(r,θ)=r sinθ+sin(r cosθ):",
               r"f(r,\theta)=\frac{1-\cos\big(r\sin\theta+\sin(r\cos\theta)\big)}{\sin r}"),
        _passo("Usiamo gli sviluppi di Mac Laurin (limiti notevoli): sin(r cosθ) vale circa r cosθ, quindi "
               "u vale circa r(sinθ+cosθ); 1−cos u vale circa u²/2 e sin r circa r. Il numeratore è dell'ordine di r², il "
               "denominatore di r:",
               r"f(r,\theta)\approx\frac{\tfrac12\,r^2(\sin\theta+\cos\theta)^2}{r}"
               r"=\frac r2(\sin\theta+\cos\theta)^2\xrightarrow[r\to0^+]{}0"),
        _passo("Il limite è 0 indipendentemente da θ (il fattore (sinθ+cosθ)² è limitato da 2): "
               "uniformemente rispetto a θ, quindi f è CONTINUA in (0,0).",
               r"|f(r,\theta)|\lesssim r\to0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione, lungo l'asse x: f(h,0)="
               "(1−cos(sin h))/sin|h| ≈ (h²/2)/|h| = |h|/2, quindi il rapporto incrementale vale ±1/2 "
               "a seconda del segno di h (destra e sinistra DIVERSI):",
               r"\frac{f(h,0)-f(0,0)}{h}\approx\frac{|h|}{2h}=\begin{cases}+\frac12 & h\to0^+\\ "
               r"-\frac12 & h\to0^-\end{cases}\ \Rightarrow\ \nexists\,f_x(0,0)"),
        _passo("Lungo l'asse y vale lo stesso: f(0,h)=(1−cos h)/sin|h| ≈ (h²/2)/|h| = |h|/2 e il "
               "rapporto incrementale non ha limite per h→0 (±1/2):",
               r"\frac{f(0,h)-f(0,0)}{h}\approx\frac{|h|}{2h}\ \Rightarrow\ \nexists\,f_y(0,0)"),
        _passo("Passo 3 — test di differenziabilità: se f fosse differenziabile in (0,0) esisterebbero "
               "f_x e f_y (sono i coefficienti del differenziale). Non esistono: f è "
               "CONTINUA ma NON DIFFERENZIABILE in (0,0) (il grafico ha una punta a cono: "
               "f≈(r/2)(sinθ+cosθ)² è lineare in r, non in x,y).",
               r"\nexists f_x(0,0),\ \nexists f_y(0,0)\ \Rightarrow\ \textbf{continua ma NON differenziabile}"),
    ]
    return _voce_cont("14 maggio 2026", testo, tl, passi, f, True, False)


ESAME["continuita"].append(_cont_14mag())


# ===========================================================================
# CONTINUITA' -- 11 maggio 2026 (+ luglio 2024, maggio 2025): y log(3 + xy/(x^2+y^2))
# ===========================================================================
def _cont_11mag():
    f = y * sp.log(3 + x * y / (x**2 + y**2))
    f_pol = r_ * sp.sin(th_) * sp.log(3 + sp.sin(th_) * sp.cos(th_))
    _chk_pol(f, f_pol)
    testo = ("[11 maggio 2026, Esercizio 1] Data la funzione f(x,y) = y·log(3 + xy/(x²+y²)) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in R² (non sono "
             "ammesse maggiorazioni). (Stesso testo in Maggio 2025 e, con richiesta anche delle derivate "
             "parziali in (0,0), in Luglio 2024.)")
    tl = (r"f(x,y)=\begin{cases}y\,\log\!\left(3+\dfrac{xy}{x^2+y^2}\right) & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ. Il "
               "rapporto xy/(x²+y²) non dipende da r: vale sinθ cosθ:",
               r"f(r,\theta)=r\sin\theta\,\log\big(3+\sin\theta\cos\theta\big)"),
        _passo("L'argomento del logaritmo è compreso tra 3−1/2=5/2 e 3+1/2=7/2, sempre positivo: "
               "g(θ)=sinθ log(3+sinθcosθ) è continua e limitata in θ e non dipende da r. Quindi "
               "f=r·g(θ)→0 per r→0⁺, uniformemente in θ: f è CONTINUA in (0,0).",
               r"\lim_{r\to0^+}r\,g(\theta)=0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sull'asse x si ha y=0 e "
               "f(h,0)=0; sull'asse y (x=0) l'argomento del log vale 3 e f(0,h)=h log 3:",
               r"f_x(0,0)=\lim_{h\to0}\frac{0}{h}=0,\qquad "
               r"f_y(0,0)=\lim_{h\to0}\frac{h\log3}{h}=\log3"),
        _passo("Passo 3 — test di differenziabilità: resto diviso r in polari, [f − 0·x − (log 3)·y]/r:",
               r"\frac{f-y\log3}{r}=\sin\theta\left[\log\big(3+\sin\theta\cos\theta\big)-\log3\right]"
               r"=\sin\theta\,\log\!\left(1+\frac{\sin\theta\cos\theta}{3}\right)"),
        _passo("Il resto diviso r NON dipende da r e NON è identicamente nullo: per θ=0 vale 0, ma per "
               "θ=π/4 vale (√2/2)·log(7/6)≈0,109≠0. Il limite per r→0⁺ non è 0: f NON è "
               "differenziabile in (0,0) (pur essendo continua e con derivate parziali).",
               r"\theta=0:\ 0\quad\ne\quad\theta=\frac\pi4:\ \frac{\sqrt2}{2}\log\frac76\approx0{,}109"
               r"\ \Rightarrow\ \textbf{continua ma NON differenziabile}"),
    ]
    return _voce_cont("11 maggio 2026", testo, tl, passi, f, True, False)


ESAME["continuita"].append(_cont_11mag())


# ===========================================================================
# CONTINUITA' -- maggio 2025: (x-y)(x^2-y^2)^2 (x+y+4)^2/(x^2+y^2)
# ===========================================================================
def _cont_mag25_a():
    f = (x - y) * (x**2 - y**2)**2 * (x + y + 4)**2 / (x**2 + y**2)
    f_pol = r_**3 * (sp.cos(th_) - sp.sin(th_)) * (sp.cos(th_)**2 - sp.sin(th_)**2)**2 * \
        (r_ * (sp.cos(th_) + sp.sin(th_)) + 4)**2
    _chk_pol(f, f_pol)
    testo = ("[maggio 2025, Esercizio 1] Data la funzione f(x,y) = (x−y)(x²−y²)²(x+y+4)²/(x²+y²) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne continuità e differenziabilità. (Attenzione: il "
             "denominatore è (x²+y²) alla prima, a differenza del compito del 22 luglio 2026.)")
    tl = (r"f(x,y)=\begin{cases}\dfrac{(x-y)(x^2-y^2)^2(x+y+4)^2}{x^2+y^2} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ. Il "
               "numeratore ha grado 1+4=5 in (x,y) (il fattore (x+y+4)² vale circa 16 vicino all'origine), "
               "il denominatore è r²: i fattori in r si semplificano e resta r³:",
               r"f(r,\theta)=\frac{r^5(\cos\theta-\sin\theta)(\cos^2\theta-\sin^2\theta)^2"
               r"\big(r(\cos\theta+\sin\theta)+4\big)^2}{r^2}=r^3\,h(r,\theta)"),
        _passo("Il fattore h(r,θ)=(cosθ−sinθ)(cos²θ−sin²θ)²(r(cosθ+sinθ)+4)² è limitato (per r≤1 vale "
               "|h|≤√2·1·(√2+4)²): f(r,θ)→0 per r→0⁺ uniformemente in θ, quindi f è CONTINUA in (0,0).",
               r"|f(r,\theta)|\le C\,r^3\to0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sull'asse x f(h,0)=h·h⁴(h+4)²/h²="
               "h³(h+4)², sull'asse y f(0,h)=(−h)h⁴(h+4)²/h²=−h³(h+4)²:",
               r"f_x(0,0)=\lim_{h\to0}\frac{h^3(h+4)^2}{h}=0,\qquad "
               r"f_y(0,0)=\lim_{h\to0}\frac{-h^3(h+4)^2}{h}=0"),
        _passo("Passo 3 — test di differenziabilità: il resto diviso r vale r²·h(r,θ), che tende a 0 "
               "uniformemente in θ:",
               r"\frac{f-0\cdot x-0\cdot y}{r}=r^2\,h(r,\theta)\ \to\ 0\quad(r\to0^+)"),
        _passo("Il resto diviso r tende a 0 per ogni θ: f è DIFFERENZIABILE in (0,0), con piano "
               "tangente z=0 (differenziale nullo).",
               r"\textbf{continua e differenziabile in }(0,0),\qquad \text{piano tangente: } z=0"),
    ]
    return _voce_cont("maggio 2025", testo, tl, passi, f, True, True,
                      "Scrivi: continua, differenziabile")


ESAME["continuita"].append(_cont_mag25_a())


# ===========================================================================
# CONTINUITA' -- maggio 2025: radice cubica di x^2 y (1-xy), piano tangente in (2;2)
# ===========================================================================
def _cont_mag25_cbrt():
    h = x**2 * y * (1 - x * y)
    f_graf = sp.sign(h) * sp.Abs(h)**sp.Rational(1, 3)
    cr = sp.cbrt(24)
    f22 = -2 * sp.cbrt(3)
    fx22 = -10 * sp.cbrt(3) / 9
    fy22 = -7 * sp.cbrt(3) / 9
    # controllo numerico (derivate con radice cubica reale)
    fnum = lambda a, b: float(np.cbrt(float(h.subs({x: a, y: b}))))
    e = 1e-6
    assert abs((fnum(2 + e, 2) - fnum(2 - e, 2)) / (2 * e) - float(fx22)) < 1e-5
    assert abs((fnum(2, 2 + e) - fnum(2, 2 - e)) / (2 * e) - float(fy22)) < 1e-5
    assert abs(fnum(2, 2) - float(f22)) < 1e-9
    piano = sp.expand(f22 + fx22 * (x - 2) + fy22 * (y - 2))
    testo = ("[maggio 2025, Esercizio 1] Studiare la continuità e la differenziabilità della funzione "
             "f(x,y) = ∛(x²y(1−xy)) nel punto O(0;0). Verificare se esiste il piano tangente al grafico "
             "di f nel punto (2;2) e, in caso affermativo, scriverne l'equazione.")
    tl = r"f(x,y)=\sqrt[3]{x^2y\,(1-xy)}"
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità: la radice cubica è definita e continua su TUTTO R (anche per "
               "radicando negativo) e il radicando x²y(1−xy) è un polinomio, quindi continuo. La "
               "composizione di funzioni continue è continua: f è continua in tutto R², in particolare "
               "in (0,0), dove vale f(0,0)=0.",
               r"f=\sqrt[3]{p(x,y)},\ \ p(x,y)=x^2y-x^3y^2\ \text{polinomio}\ \Rightarrow\ "
               r"f\in C^0(\mathbb{R}^2)"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sugli assi il radicando si "
               "annulla (x=0 oppure y=0), quindi f è nulla sugli assi:",
               r"f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-0}{h}=0,\qquad f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-0}{h}=0"),
        _passo("Passo 3 — test di differenziabilità: con f_x=f_y=0 il candidato differenziale è nullo e "
               "occorre che il resto diviso r, cioè f(x,y)/√(x²+y²), tenda a 0. Proviamo lungo la retta "
               "y=x (r=√2|x|): il radicando diventa x³(1−x²), quindi f(x,x)=x·∛(1−x²):",
               r"\frac{f(x,x)}{\sqrt{x^2+x^2}}=\frac{x\sqrt[3]{1-x^2}}{\sqrt2\,|x|}\ \longrightarrow\ "
               r"\pm\frac{1}{\sqrt2}\ne0\quad(x\to0^\pm)"),
        _passo("Il resto diviso r non tende a 0 (lungo y=x vale ±1/√2; in polari tende a ∛(cos²θ sinθ), "
               "che dipende da θ): f è CONTINUA ma NON DIFFERENZIABILE in (0,0). Il grafico ha una punta "
               "in O perché la radice cubica ha derivata infinita nell'origine.",
               r"\lim_{r\to0^+}\frac{f(r\cos\theta,r\sin\theta)}{r}=\sqrt[3]{\cos^2\theta\,\sin\theta}"
               r"\ne0\ \Rightarrow\ \textbf{non differenziabile in }(0,0)"),
        _passo("Passo 4 — piano tangente in (2;2): ivi il radicando vale p(2,2)=8−32=−24≠0. La radice "
               "cubica è derivabile in ogni punto diverso da 0, quindi f è C¹ in un intorno di (2;2): "
               "è differenziabile e il piano tangente ESISTE. Derivata della radice cubica: "
               "(∛p)'=p'/(3·∛(p²)).",
               r"f=\sqrt[3]{p},\quad f_x=\frac{p_x}{3\sqrt[3]{p^2}},\quad f_y=\frac{p_y}{3\sqrt[3]{p^2}},"
               r"\quad p_x=2xy-3x^2y^2,\ p_y=x^2-2x^3y"),
        _passo("Valori nel punto (2;2) per il piano tangente: p=−24, p_x=8−48=−40, p_y=4−32=−28, ∛(p²)=∛576=4∛9:",
               r"f(2,2)=\sqrt[3]{-24}=-2\sqrt[3]3,\quad f_x(2,2)=\frac{-40}{3\cdot4\sqrt[3]9}="
               r"-\frac{10\sqrt[3]3}{9},\quad f_y(2,2)=\frac{-28}{12\sqrt[3]9}=-\frac{7\sqrt[3]3}{9}"),
        _passo("Equazione del piano tangente in (2;2): z = f + f_x(x−2) + f_y(y−2):",
               r"z=-2\sqrt[3]3-\frac{10\sqrt[3]3}{9}(x-2)-\frac{7\sqrt[3]3}{9}(y-2)"),
    ]
    return _voce_cont("maggio 2025", testo, tl, passi, f_graf, True, False,
                      "Scrivi: continua, non differenziabile (riferito all'origine)")


ESAME["continuita"].append(_cont_mag25_cbrt())


# ===========================================================================
# CONTINUITA' -- 21 ottobre 2025: x^2 (y-2)  (segno, Hessiana, continuita', piano tangente in (1,-2))
# ===========================================================================
def _cont_21ott():
    f = x**2 * (y - 2)
    piano_p, piano = _piano_passi(f, sp.Integer(1), sp.Integer(-2),
                                  "Passo d) — piano tangente in (1,−2): f è un polinomio.")
    testo = ("[21 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = x²(y−2): a) studiare e "
             "rappresentare graficamente il segno; b) determinare gli eventuali punti di massimo e minimo "
             "utilizzando la matrice Hessiana; c) studiare continuità e differenziabilità; d) "
             "determinare, se esiste, il piano tangente in (1,−2).")
    tl = r"f(x,y)=x^2(y-2)"
    fx, fy = sp.diff(f, x), sp.diff(f, y)
    hess = sp.hessian(f, (x, y))
    passi = [
        _passo("Funzione (polinomiale):", tl),
        _passo("Passo a) — segno: x²≥0 sempre, quindi il segno di f dipende solo dal fattore (y−2):",
               r"f\ge0\iff y\ge2,\qquad f\le0\iff y\le2,\qquad f=0\iff x=0\ \text{ o }\ y=2"),
        _passo("Rappresentazione del segno: la retta y=2 (zeri di f) e l'asse x=0 dividono il piano; f è positiva "
               "nel semipiano y>2 e negativa nel semipiano y<2 (l'asse x=0 appartiene all'insieme "
               "degli zeri).", None),
        _passo("Passo b) — annulliamo il gradiente per trovare i punti stazionari:",
               _tex(fx) + "=0,\\quad " + _tex(fy) + "=0"),
        _passo("Il sistema (2x(y−2)=0, x²=0) impone x=0 per QUALSIASI y: i punti stazionari non sono "
               "isolati ma formano l'intera retta x=0 (asse y).",
               r"x^2=0\iff x=0,\ \ y\in\mathbb{R}\ \text{libero}"),
        _passo("Matrice Hessiana generale e ristretta alla retta x=0:",
               "H(x,y)=" + _tex(hess) + r",\quad H(0,y_0)=" + _tex(hess.subs({x: 0, y: sp.Symbol('y_0')}))
               + r",\ \det H(0,y_0)=0"),
        _passo("Su tutta la retta x=0 si ha det H = 0: il test dell'Hessiana NON decide. Studiamo "
               "direttamente il segno di f(x,y)−f(0,y0)=x²(y−2) in un intorno di (0,y0): per y0>2 è ≥0 "
               "(minimo, debole), per y0<2 è ≤0 (massimo, debole); per y0=2 il fattore (y−2) cambia "
               "segno vicino al punto, quindi f assume valori sia positivi sia negativi: (0,2) è una "
               "sella (degenere).",
               r"f(x,y)-f(0,y_0)=x^2(y-2)\ \begin{cases}\ge0 & y_0>2\ (\text{minimo})\\ \le0 & y_0<2\ "
               r"(\text{massimo})\\ \text{segno variabile} & y_0=2\ (\text{sella})\end{cases}"),
        _passo("Passo c) — continuità e differenziabilità: f è un POLINOMIO, quindi di classe C^∞ in "
               "tutto R² (le derivate parziali sono continue): è continua e differenziabile ovunque, "
               "senza bisogno di studiare limiti.",
               r"f\in\mathcal{C}^\infty(\mathbb{R}^2)\ \Rightarrow\ \textbf{continua e differenziabile}"),
    ] + piano_p
    return _voce_cont("21 ottobre 2025", testo, tl, passi, f, True, True,
                      "Scrivi: continua, differenziabile")


ESAME["continuita"].append(_cont_21ott())


# ===========================================================================
# PIANO TANGENTE + NATURA DEI PUNTI STAZIONARI (Aprile 2025/2026, dicembre 2025)
# ===========================================================================
def _stazionari_tg(fonte, testo, tl, f, P, intro_piano, passi_gradiente, punti, speciali=None,
                   note_hess=None):
    """Esercizio 'piano tangente in P + natura dei punti stazionari'. 'passi_gradiente' sono i passi
    (scritti a mano) che risolvono grad f = 0; 'punti' e' la lista dei punti stazionari trovati
    (verificata con sympy); 'speciali' = {(px,py): (tipo, testo, latex)} per i casi con Hessiano
    nullo."""
    fx, fy = sp.diff(f, x), sp.diff(f, y)
    hess = sp.hessian(f, (x, y))
    sol = sp.solve([fx, fy], [x, y], dict=True)
    kk = lambda p: (float(sp.N(p[0])), float(sp.N(p[1])))
    trovati = sorted(((sp.simplify(s[x]), sp.simplify(s[y])) for s in sol
                      if sp.im(s[x]) == 0 and sp.im(s[y]) == 0), key=kk)
    attesi = sorted(((sp.nsimplify(px), sp.nsimplify(py)) for px, py in punti), key=kk)
    assert [tuple(map(sp.simplify, p)) for p in trovati] == [tuple(map(sp.simplify, p)) for p in attesi], \
        (trovati, attesi)
    piano_p, piano = _piano_passi(f, P[0], P[1], intro_piano)
    passi = [_passo("Funzione:", tl)]
    passi.extend(piano_p)
    passi.append(_passo("Passo b) — punti stazionari: annulliamo il gradiente (derivate parziali prime "
                        "uguali a 0):",
                        r"\begin{cases}f_x=" + _tex(sp.simplify(fx)) + r"=0\\ f_y=" + _tex(sp.simplify(fy))
                        + r"=0\end{cases}"))
    passi.extend(passi_gradiente)
    passi.append(_passo("Matrice Hessiana (derivate parziali seconde):",
                        "H(x,y)=" + _tex(sp.simplify(hess))))
    classificazioni = []
    attesi_ris = []
    for (px, py) in sorted(punti, key=lambda p: (float(sp.N(p[0])), float(sp.N(p[1])))):
        H = sp.simplify(hess.subs({x: px, y: py}))
        det = sp.simplify(H.det())
        tr = sp.simplify(H.trace())
        fxx = H[0, 0]
        key = (sp.nsimplify(px), sp.nsimplify(py))
        if speciali and key in speciali:
            tipo, ttxt, tlat = speciali[key]
            passi.append(_passo(f"Punto ({_tex(px)}, {_tex(py)}): " + ttxt,
                                "H=" + _tex(H) + r",\ \det H=" + _tex(det) + r"\ \Rightarrow\ " + tlat))
        else:
            if det > 0 and fxx > 0:
                tipo = "minimo"
            elif det > 0 and fxx < 0:
                tipo = "massimo"
            elif det < 0:
                tipo = "sella"
            else:
                raise AssertionError("Hessiano nullo non gestito")
            fval = sp.simplify(f.subs({x: px, y: py}))
            passi.append(_passo(f"Punto ({_tex(px)}, {_tex(py)}): valutiamo la matrice Hessiana H: det H "
                                + ("<0 ⇒ sella" if tipo == "sella" else
                                   (">0 e f_xx>0 ⇒ minimo" if tipo == "minimo" else ">0 e f_xx<0 ⇒ massimo")) + ":",
                                "H=" + _tex(H) + r",\ \det H=" + _tex(det) + r",\ f_{xx}=" + _tex(fxx)
                                + r"\ \Rightarrow\ \textbf{" + tipo.upper() + r"},\ f=" + _tex(fval)))
        classificazioni.append({"punto": (px, py), "tipo": tipo})
        attesi_ris.append([float(sp.N(px)), float(sp.N(py)), tipo])
    if note_hess:
        passi.append(_passo(note_hess[0], note_hess[1]))
    try:
        fig = _grafico.grafico_punto_critico({"f": f, "classificazioni": classificazioni})
        png = _png(fig)
    except Exception:
        png = None
    return _voce(fonte, testo, tl, "Un punto per riga, formato x,y,tipo (es: 0,0,minimo).", passi,
                 {"tipo": "punti_classificati", "attesi": attesi_ris}, png)


def _tg_dic25():
    f = (y - 1)**2 + x * sp.exp(x + 1) * (y - 1)
    testo = ("[9 dicembre 2025, Esercizio 1] Data la funzione f(x,y) = (y−1)² + x·e^(x+1)·(y−1): "
             "a) determinare il piano tangente al grafico di f nel punto P(0,0) [2 punti]; b) studiare "
             "la natura dei punti stazionari [8 punti]. (La sola parte b) è l'Esercizio 1 del 2 aprile "
             "2026; la parte a) compare in Aprile 2025.)")
    tl = r"f(x,y)=(y-1)^2+x\,e^{x+1}(y-1)"
    grad = [
        _passo("Annullando il gradiente: la prima equazione è un prodotto: f_x=e^{x+1}(y−1)(1+x)=0 (l'esponenziale non si "
               "annulla mai), quindi y=1 oppure x=−1. Apriamo i due rami e sostituiamo nella seconda "
               "equazione f_y=2(y−1)+x e^{x+1}=0:",
               r"f_x=e^{x+1}(y-1)(x+1)=0\iff y=1\ \text{ oppure }\ x=-1"),
        _passo("Ramo y=1: f_y=x e^{x+1}=0 ⇒ x=0, punto (0,1). Ramo x=−1: f_y=2(y−1)−1·e^0=0 ⇒ "
               "y=3/2, punto (−1,3/2). Punti stazionari:",
               r"(0,1)\qquad\text{e}\qquad\left(-1,\tfrac32\right)"),
    ]
    return _stazionari_tg("9 dicembre 2025", testo, tl, f, (sp.Integer(0), sp.Integer(0)),
                          "Passo a) — piano tangente in P(0,0): f è prodotto/somma di funzioni elementari.",
                          grad, [(0, 1), (-1, sp.Rational(3, 2))])


ESAME["continuita"].append(_tg_dic25())


def _tg_apr25():
    f = -(1 - x)**2 + y * sp.exp(y + 1) * (1 - x)
    testo = ("[aprile 2025, Esercizio 1] Data la funzione f(x,y) = −(1−x)² + y·e^(y+1)·(1−x): a) "
             "determinare il piano tangente al grafico di f nel punto P(1,1) [2 punti]; b) studiare la "
             "natura dei punti stazionari [8 punti].")
    tl = r"f(x,y)=-(1-x)^2+y\,e^{y+1}(1-x)"
    grad = [
        _passo("Annullando il gradiente: la seconda equazione è un prodotto: f_y=e^{y+1}(1+y)(1−x)=0 (l'esponenziale non si "
               "annulla), quindi y=−1 oppure x=1. Apriamo i due rami e sostituiamo nella prima "
               "equazione f_x=2(1−x)−y e^{y+1}=0:",
               r"f_y=e^{y+1}(y+1)(1-x)=0\iff y=-1\ \text{ oppure }\ x=1"),
        _passo("Ramo x=1: f_x=−y e^{y+1}=0 ⇒ y=0, punto (1,0). Ramo y=−1: f_x=2(1−x)+1=0 ⇒ "
               "x=3/2, punto (3/2,−1). Punti stazionari:",
               r"(1,0)\qquad\text{e}\qquad\left(\tfrac32,-1\right)"),
    ]
    return _stazionari_tg("aprile 2025", testo, tl, f, (sp.Integer(1), sp.Integer(1)),
                          "Passo a) — piano tangente in P(1,1): f è prodotto/somma di funzioni elementari.",
                          grad, [(1, 0), (sp.Rational(3, 2), -1)])


ESAME["continuita"].append(_tg_apr25())


def _tg_8apr():
    f = (y + 3) * (1 + x)**2 - 4 * (y + 3)
    testo = ("[8 aprile 2026, Esercizio 1] Data la funzione f(x,y) = (y+3)(1+x)² − 4(y+3) studiare la "
             "natura dei punti stazionari [7 punti]. Determinare, se esiste, l'equazione del piano "
             "tangente alla funzione nel punto (0,0) [3 punti].")
    tl = r"f(x,y)=(y+3)(1+x)^2-4(y+3)"
    grad = [
        _passo("Gradiente nullo — raccogliendo (y+3): f=(y+3)[(1+x)²−4]=(y+3)(x−1)(x+3). Dalla seconda equazione "
               "f_y=(1+x)²−4=0 si ottiene x=1 oppure x=−3 (in entrambi i casi 1+x=±2≠0); sostituendo "
               "nella prima f_x=2(y+3)(1+x)=0 serve y+3=0:",
               r"f_y=(1+x)^2-4=0\iff x=1\ \text{ o }\ x=-3;\qquad f_x=2(y+3)(1+x)=0\Rightarrow y=-3"),
        _passo("Punti stazionari (entrambi con y=−3):", r"(1,-3)\qquad\text{e}\qquad(-3,-3)"),
    ]
    return _stazionari_tg("8 aprile 2026", testo, tl, f, (sp.Integer(0), sp.Integer(0)),
                          "Piano tangente in (0,0): f è un polinomio.", grad, [(1, -3), (-3, -3)])


ESAME["continuita"].append(_tg_8apr())


def _tg_9apr():
    f = x**3 / 8 * (sp.Rational(1, 3) + x * y**2) - 2 * y**2
    testo = ("[9 aprile 2026, Esercizio 1] Data la funzione f(x,y) = (x³/8)(1/3 + xy²) − 2y² studiare la "
             "natura dei punti stazionari [7 punti]. Determinare, se esiste, l'equazione del piano "
             "tangente alla funzione nel punto (−2,0) [3 punti].")
    tl = r"f(x,y)=\frac{x^3}{8}\left(\frac13+xy^2\right)-2y^2=\frac{x^3}{24}+\frac{x^4y^2}{8}-2y^2"
    grad = [
        _passo("Gradiente nullo — sviluppiamo f=x³/24+x⁴y²/8−2y²: f_x=x²/8+x³y²/2=x²(1/8+xy²/2) e f_y=x⁴y/4−4y="
               "y(x⁴/4−4). Dalla seconda: y=0 oppure x⁴=16, cioè x=±2. Apriamo i rami:",
               r"f_y=y\left(\frac{x^4}{4}-4\right)=0\iff y=0\ \text{ oppure }\ x=\pm2"),
        _passo("Ramo y=0: f_x=x²/8=0 ⇒ x=0, punto (0,0). Ramo x=2: f_x=1/2+4y²>0, mai nullo. Ramo "
               "x=−2: f_x=1/2−4y²=0 ⇒ y²=1/8, y=±√2/4. Punti stazionari:",
               r"(0,0),\qquad\left(-2,\,\tfrac{\sqrt2}{4}\right),\qquad\left(-2,\,-\tfrac{\sqrt2}{4}\right)"),
    ]
    spec = {(sp.Integer(0), sp.Integer(0)): (
        "sella",
        "det H=0: il test dell'Hessiana non decide. Studiamo f lungo l'asse x (y=0): f(x,0)=x³/24 "
        "cambia segno passando per l'origine (negativa per x<0, positiva per x>0). Quindi in ogni "
        "intorno di (0,0) f assume valori sia maggiori sia minori di f(0,0)=0: l'origine NON è né "
        "massimo né minimo (punto di sella degenere, come il flesso di x³).",
        r"f(x,0)=\frac{x^3}{24}\ \text{cambia segno}\ \Rightarrow\ \textbf{non estremante (sella degenere)}")}
    return _stazionari_tg("9 aprile 2026", testo, tl, f, (sp.Integer(-2), sp.Integer(0)),
                          "Piano tangente in (−2,0): f è un polinomio.", grad,
                          [(0, 0), (-2, sp.sqrt(2) / 4), (-2, -sp.sqrt(2) / 4)], speciali=spec)


ESAME["continuita"].append(_tg_9apr())


# ===========================================================================
# CONTINUITA' -- dicembre 2023: x sin(x^2 y)/(x^2+y^2) + 2x, piano tangente in (1;0)
# ===========================================================================
def _cont_dic23():
    f = x * sp.sin(x**2 * y) / (x**2 + y**2) + 2 * x
    f_pol = sp.cos(th_) * sp.sin(r_**3 * sp.cos(th_)**2 * sp.sin(th_)) / r_ + 2 * r_ * sp.cos(th_)
    _chk_pol(f, f_pol)
    piano_p, piano = _piano_passi(f, sp.Integer(1), sp.Integer(0),
                                  "Passo 5 — piano tangente nel punto (1;0), lontano dall'origine: là il "
                                  "denominatore x²+y² vale 1≠0.")
    testo = ("[dicembre 2023, Continuità e differenziabilità n.1] Data la funzione f(x,y) = "
             "x·sin(x²y)/(x²+y²) + 2x per (x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la "
             "differenziabilità. Verificare se esiste il piano tangente al grafico di f nel punto (1;0) "
             "e, in caso affermativo, scriverne l'equazione.")
    tl = (r"f(x,y)=\begin{cases}\dfrac{x\sin(x^2y)}{x^2+y^2}+2x & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ; "
               "l'argomento del seno diventa x²y=r³cos²θ sinθ:",
               r"f(r,\theta)=\frac{\cos\theta\,\sin\!\big(r^3\cos^2\theta\sin\theta\big)}{r}+2r\cos\theta"),
        _passo("Usiamo sin t ≈ t per t→0 (qui t=r³cos²θ sinθ→0): il primo addendo è ≈ "
               "cosθ·r³cos²θ sinθ/r = r²cos³θ sinθ; quindi f(r,θ) ≈ r²cos³θ sinθ + 2r cosθ → 0 per "
               "r→0⁺, uniformemente in θ. Dunque f è CONTINUA in (0,0).",
               r"f(r,\theta)\approx r^2\cos^3\theta\sin\theta+2r\cos\theta\ \xrightarrow[r\to0^+]{}0=f(0,0)"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sull'asse x (y=0) il seno è nullo "
               "e f(h,0)=2h; sull'asse y (x=0) f(0,h)=0:",
               r"f_x(0,0)=\lim_{h\to0}\frac{2h}{h}=2,\qquad f_y(0,0)=\lim_{h\to0}\frac{0}{h}=0"),
        _passo("Passo 3 — test di differenziabilità: resto diviso r, cioè [f − 2x − 0·y]/r, in polari "
               "(il termine 2x si elide):",
               r"\frac{f-2x}{r}=\frac{\cos\theta\,\sin\!\big(r^3\cos^2\theta\sin\theta\big)}{r^2}"
               r"\approx r\cos^3\theta\sin\theta\ \xrightarrow[r\to0^+]{}0"),
        _passo("Il resto diviso r tende a 0 (uniformemente in θ, perché |cos³θ sinθ|≤1): f è "
               "DIFFERENZIABILE in (0,0), con differenziale 2x e piano tangente z=2x nell'origine.",
               r"\textbf{continua e differenziabile in }(0,0),\qquad z=2x\ \text{(piano tangente in }O)"),
    ] + piano_p
    return _voce_cont("dicembre 2023", testo, tl, passi, f, True, True,
                      "Scrivi: continua, differenziabile (riferito all'origine)")


ESAME["continuita"].append(_cont_dic23())


# ===========================================================================
# CONTINUITA' -- ottobre 2023 (= 28 luglio 2021): (y-x)^3/(x^2+y^2+x^2 y^2): segno, continuita', diff.
# ===========================================================================
def _cont_ott23():
    f = (y - x)**3 / (x**2 + y**2 + x**2 * y**2)
    f_pol = r_ * (sp.sin(th_) - sp.cos(th_))**3 / (1 + r_**2 * sp.cos(th_)**2 * sp.sin(th_)**2)
    _chk_pol(f, f_pol)
    testo = ("[ottobre 2023, Continuità e differenziabilità n.1] Data la funzione f(x,y) = "
             "(y−x)³/(x²+y²+x²y²) per (x,y)≠(0,0), f(0,0)=0, studiarne il segno, la continuità e la "
             "differenziabilità. (Stesso testo del 28 luglio 2021.)")
    tl = (r"f(x,y)=\begin{cases}\dfrac{(y-x)^3}{x^2+y^2+x^2y^2} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Segno: il denominatore x²+y²+x²y² è sempre >0 per (x,y)≠(0,0) (somma di quadrati), "
               "quindi il segno di f è quello di (y−x)³, cioè quello di y−x:",
               r"f>0\iff y>x,\qquad f<0\iff y<x,\qquad f=0\iff y=x"),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ. Il "
               "numeratore ha grado 3, il denominatore r²(1+r²cos²θ sin²θ):",
               r"f(r,\theta)=\frac{r^3(\sin\theta-\cos\theta)^3}{r^2\left(1+r^2\cos^2\theta\sin^2\theta\right)}"
               r"=\frac{r(\sin\theta-\cos\theta)^3}{1+r^2\cos^2\theta\sin^2\theta}"),
        _passo("Il denominatore è ≥1 e |sinθ−cosθ|³≤2√2, quindi |f(r,θ)|≤2√2·r→0 per r→0⁺, "
               "uniformemente in θ: f è CONTINUA in (0,0).",
               r"|f(r,\theta)|\le2\sqrt2\,r\to0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sull'asse x f(h,0)=−h³/h²=−h, "
               "sull'asse y f(0,h)=h³/h²=h:",
               r"f_x(0,0)=\lim_{h\to0}\frac{-h}{h}=-1,\qquad f_y(0,0)=\lim_{h\to0}\frac{h}{h}=1"),
        _passo("Passo 3 — test di differenziabilità: resto diviso r, cioè [f + x − y]/r, in polari. "
               "Per r→0⁺ il denominatore tende a 1, quindi il limite è (sinθ−cosθ)³ + (cosθ−sinθ):",
               r"\frac{f+x-y}{r}\to(\sin\theta-\cos\theta)^3-(\sin\theta-\cos\theta)="
               r"-2\sin\theta\cos\theta\,(\sin\theta-\cos\theta)"),
        _passo("Il limite dipende da θ: vale 0 per θ=0 (e θ=π/4, π/2), ma per θ=π/3 vale "
               "−2·(√3/2)(1/2)·((√3−1)/2)=−(3−√3)/4≈−0,32≠0. Il resto diviso r non tende a 0: f è "
               "CONTINUA ma NON DIFFERENZIABILE in (0,0).",
               r"\theta=\frac\pi3:\ -\frac{3-\sqrt3}{4}\approx-0{,}32\ne0\ \Rightarrow\ "
               r"\textbf{continua ma NON differenziabile}"),
    ]
    return _voce_cont("ottobre 2023", testo, tl, passi, f, True, False)


ESAME["continuita"].append(_cont_ott23())


# ===========================================================================
# CONTINUITA' -- dicembre 2021: log(1+x^2) cbrt(y^2)/(x^2+y^2)
# ===========================================================================
def _cont_dic21_log():
    f = sp.log(1 + x**2) * sp.cbrt(y**2) / (x**2 + y**2)
    testo = ("[dicembre 2021, Esercizio 4] Data la funzione f(x,y) = log(1+x²)·∛(y²)/(x²+y²) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità.")
    tl = (r"f(x,y)=\begin{cases}\dfrac{\log(1+x^2)\sqrt[3]{y^2}}{x^2+y^2} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ; "
               "∛(y²)=r^{2/3}|sinθ|^{2/3}:",
               r"f(r,\theta)=\frac{\log\!\big(1+r^2\cos^2\theta\big)\,r^{2/3}|\sin\theta|^{2/3}}{r^2}"),
        _passo("Usando log(1+t) ≈ t per t→0 (qui t=r²cos²θ→0) il numeratore vale ≈ "
               "r²cos²θ·r^{2/3}|sinθ|^{2/3} e quindi f(r,θ) ≈ r^{2/3}cos²θ|sinθ|^{2/3}→0 per r→0⁺, "
               "uniformemente in θ (il fattore in θ è limitato da 1): f è CONTINUA in (0,0).",
               r"f(r,\theta)\approx r^{2/3}\cos^2\theta\,|\sin\theta|^{2/3}\to0=f(0,0)"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sull'asse x (y=0) f=0; "
               "sull'asse y (x=0) log(1+0)=0, quindi ancora f=0:",
               r"f_x(0,0)=\lim_{h\to0}\frac{0}{h}=0,\qquad f_y(0,0)=\lim_{h\to0}\frac{0}{h}=0"),
        _passo("Passo 3 — test di differenziabilità: resto diviso r, cioè f/r, in polari. Dalla "
               "stima precedente:",
               r"\frac{f}{r}\approx r^{-1/3}\cos^2\theta\,|\sin\theta|^{2/3}"),
        _passo("Per θ=π/4 (cosθ sinθ≠0) il resto diviso r vale ≈ (1/2)(√2/2)^{2/3}·r^{-1/3}→+∞ "
               "per r→0⁺: non tende a 0 (diverge!). Verifica lungo la retta y=x: "
               "f(x,x)/(√2|x|)≈1/(2√2|x|^{1/3})→∞. Quindi f è CONTINUA ma NON DIFFERENZIABILE in (0,0).",
               r"\left.\frac{f}{r}\right|_{y=x}\approx\frac{1}{2\sqrt2\,|x|^{1/3}}\to+\infty\ \Rightarrow\ "
               r"\textbf{continua ma NON differenziabile}"),
    ]
    return _voce_cont("dicembre 2021", testo, tl, passi, f, True, False)


ESAME["continuita"].append(_cont_dic21_log())


# ===========================================================================
# CONTINUITA' -- dicembre 2021: x y (x^2-y^2)/(x^4+y^2)  (cammino parabolico)
# ===========================================================================
def _cont_dic21_parab():
    f = x * y * (x**2 - y**2) / (x**4 + y**2)
    testo = ("[dicembre 2021, Esercizio 6] Data la funzione f(x,y) = xy(x²−y²)/(x⁴+y²) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità.")
    tl = (r"f(x,y)=\begin{cases}\dfrac{xy(x^2-y^2)}{x^4+y^2} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): maggioriamo. Poiché |x²−y²|≤x²+y², si ha "
               "|f|≤|xy|(x²+y²)/(x⁴+y²). Spezziamo in due addendi e usiamo x⁴+y²≥2x²|y| (AM-GM) per "
               "il primo e y²≤x⁴+y² per il secondo:",
               r"|f|\le\frac{|x|\,x^2|y|}{x^4+y^2}+\frac{|x||y|\,y^2}{x^4+y^2}"
               r"\le\frac{|x|}{2}+|x||y|\ \to\ 0"),
        _passo("Il limite è 0 = f(0,0) per ogni modo di avvicinarsi all'origine, quindi f è CONTINUA in "
               "(0,0) (in polari: f(r,θ)=r²cosθ sinθ(cos²θ−sin²θ)/(r²cos⁴θ+sin²θ), che per θ fissato "
               "con sinθ≠0 tende a 0).",
               r"\lim_{(x,y)\to(0,0)}f(x,y)=0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sugli assi (y=0 oppure x=0) il "
               "numeratore xy(x²−y²) si annulla, quindi f=0 e:",
               r"f_x(0,0)=0,\qquad f_y(0,0)=0"),
        _passo("Passo 3 — test di differenziabilità: resto diviso r, cioè f/√(x²+y²). Lungo ogni "
               "retta y=mx tende a 0 (per m≠0 il denominatore è ≈m²x²; per m=0 f=0), quindi il test "
               "sulle rette non basta e bisogna provare un cammino curvo, la parabola y=x²:",
               r"f(x,x^2)=\frac{x\cdot x^2\,(x^2-x^4)}{x^4+x^4}=\frac{x\,(1-x^2)}{2}"),
        _passo("Sulla parabola, con r=√(x²+x⁴)≈|x|, il resto diviso r vale (x(1−x²)/2)/|x|→±1/2≠0 "
               "(limiti destro e sinistro diversi e non nulli): non tende a 0. Dunque f è CONTINUA ma "
               "NON DIFFERENZIABILE in (0,0), nonostante il test lungo ogni retta desse 0.",
               r"\frac{f(x,x^2)}{\sqrt{x^2+x^4}}\to\pm\frac12\ne0\ \Rightarrow\ "
               r"\textbf{continua ma NON differenziabile}"),
    ]
    return _voce_cont("dicembre 2021", testo, tl, passi, f, True, False)


ESAME["continuita"].append(_cont_dic21_parab())


# ===========================================================================
# CONTINUITA' -- settembre 2021: (x+3y)^3/sqrt(x^2+y^2) + log(1+y^2)
# ===========================================================================
def _cont_set21_a():
    f = (x + 3 * y)**3 / sp.sqrt(x**2 + y**2) + sp.log(1 + y**2)
    f_pol = r_**2 * (sp.cos(th_) + 3 * sp.sin(th_))**3 + sp.log(1 + r_**2 * sp.sin(th_)**2)
    _chk_pol(f, f_pol)
    testo = ("[settembre 2021, Esercizio 1] Data la funzione f(x,y) = (x+3y)³/√(x²+y²) + log(1+y²) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità.")
    tl = (r"f(x,y)=\begin{cases}\dfrac{(x+3y)^3}{\sqrt{x^2+y^2}}+\log(1+y^2) & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ; "
               "(x+3y)³=r³(cosθ+3sinθ)³ e √(x²+y²)=r:",
               r"f(r,\theta)=r^2(\cos\theta+3\sin\theta)^3+\log\!\big(1+r^2\sin^2\theta\big)"),
        _passo("Maggioriamo: |cosθ+3sinθ|≤√10 e log(1+t)≤t per t≥0, quindi |f|≤10√10·r²+r²→0 "
               "per r→0⁺ uniformemente in θ: f è CONTINUA in (0,0).",
               r"|f(r,\theta)|\le\left(10\sqrt{10}+1\right)r^2\to0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: f(h,0)=h³/|h|=h|h| e "
               "f(0,h)=27h³/|h|+log(1+h²)=27h|h|+log(1+h²):",
               r"f_x(0,0)=\lim_{h\to0}\frac{h|h|}{h}=\lim_{h\to0}|h|=0,\qquad "
               r"f_y(0,0)=\lim_{h\to0}\left(27|h|+\frac{\log(1+h^2)}{h}\right)=0"),
        _passo("Passo 3 — test di differenziabilità: con f_x=f_y=0 il resto diviso r è f/r:",
               r"\frac{f}{r}=r(\cos\theta+3\sin\theta)^3+\frac{\log(1+r^2\sin^2\theta)}{r}"
               r"\le\left(10\sqrt{10}+1\right)r\to0"),
        _passo("Il resto diviso r tende a 0 uniformemente in θ: f è DIFFERENZIABILE in (0,0), con "
               "piano tangente z=0.",
               r"\textbf{continua e differenziabile in }(0,0),\qquad z=0"),
    ]
    return _voce_cont("settembre 2021", testo, tl, passi, f, True, True,
                      "Scrivi: continua, differenziabile")


ESAME["continuita"].append(_cont_set21_a())


# ===========================================================================
# CONTINUITA' -- settembre 2021: (x^3 y + 2 x^2 y^2)/(x^2+y^2)^{3/2}
# ===========================================================================
def _cont_set21_b():
    f = (x**3 * y + 2 * x**2 * y**2) / (x**2 + y**2)**sp.Rational(3, 2)
    f_pol = r_ * (sp.cos(th_)**3 * sp.sin(th_) + 2 * sp.cos(th_)**2 * sp.sin(th_)**2)
    _chk_pol(f, f_pol)
    testo = ("[settembre 2021, Esercizio 2] Data la funzione f(x,y) = (x³y+2x²y²)/(x²+y²)^(3/2) per "
             "(x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità.")
    tl = (r"f(x,y)=\begin{cases}\dfrac{x^3y+2x^2y^2}{(x^2+y^2)^{3/2}} & (x,y)\ne(0,0)\\ "
          r"0 & (x,y)=(0,0)\end{cases}")
    passi = [
        _passo("Funzione:", tl),
        _passo("Passo 1 — continuità in (0,0): passiamo in coordinate polari x=r cosθ, y=r sinθ. Il "
               "numeratore ha grado 4, il denominatore (r²)^{3/2}=r³:",
               r"f(r,\theta)=\frac{r^4\left(\cos^3\theta\sin\theta+2\cos^2\theta\sin^2\theta\right)}{r^3}"
               r"=r\left(\cos^3\theta\sin\theta+2\cos^2\theta\sin^2\theta\right)"),
        _passo("La parentesi è limitata (in modulo ≤3): f(r,θ)→0 per r→0⁺ uniformemente in θ, quindi "
               "f è CONTINUA in (0,0).",
               r"|f(r,\theta)|\le3r\to0=f(0,0)\ \Rightarrow\ \textbf{continua}"),
        _passo("Passo 2 — derivate parziali in (0,0) per definizione: sugli assi il numeratore si "
               "annulla, quindi f=0 e:",
               r"f_x(0,0)=0,\qquad f_y(0,0)=0"),
        _passo("Passo 3 — test di differenziabilità: resto diviso r, cioè f/r, in polari:",
               r"\frac{f}{r}=\cos^3\theta\sin\theta+2\cos^2\theta\sin^2\theta"),
        _passo("Il resto diviso r NON dipende da r ed è diverso da 0 per molti θ: per θ=π/4 vale "
               "(√2/2)³(√2/2)+2·(1/2)(1/2)=1/4+1/2=3/4≠0. Non tende a 0: f è CONTINUA ma NON "
               "DIFFERENZIABILE in (0,0).",
               r"\theta=\frac\pi4:\ \frac14+\frac12=\frac34\ne0\ \Rightarrow\ "
               r"\textbf{continua ma NON differenziabile}"),
    ]
    return _voce_cont("settembre 2021", testo, tl, passi, f, True, False)


ESAME["continuita"].append(_cont_set21_b())


# ---------------------------------------------------------------------------
# Rifinitura LaTeX: nessun '<' seguito da una lettera (verrebbe letto come tag HTML) -> \lt
# ---------------------------------------------------------------------------
import re as _re


def _fix_lt(t):
    return _re.sub(r"<(?=[A-Za-z])", r"\\lt ", t) if isinstance(t, str) else t


for _k, _v in ESAME.items():
    for _e in _v[_N0.get(_k, 0):]:
        _e["testo_latex"] = _fix_lt(_e["testo_latex"])
        for _p in _e["passi"]:
            _p["latex"] = _fix_lt(_p["latex"])
