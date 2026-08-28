"""
Bridge tra l'interfaccia web (JS/Pyodide) e i moduli Python originali del progetto
(serie.py, taylor.py, multivariabile.py, edo.py, integrali.py, grafico.py).

Nessuna logica matematica viene duplicata qui: questo file richiama esattamente le
stesse funzioni genera_X/verifica_X/spiega_X/grafico_X usate da main.py e gui.py,
e si limita a tradurre input/output in un formato comodo da consumare da JS
(stringhe e JSON), incluso il rendering dei grafici come PNG in base64 (perche' nel
browser non esiste una finestra Tkinter su cui disegnare).
"""
import json
import io
import base64

import sympy as sp

import serie
import taylor
import multivariabile
import edo
import integrali
import continuita_differenziabilita
# 'grafico' (e matplotlib) NON si importano qui: matplotlib e' un package pesante che
# nel browser conviene scaricare solo se e quando serve davvero un grafico (vedi
# mostra_grafico_png), non ad ogni avvio dell'app. L'import e' quindi rimandato lì.


def _tex(x):
    """Converte un'espressione sympy in LaTeX; per valori non-sympy la converte in stringa."""
    try:
        return sp.latex(x)
    except Exception:
        return str(x)


def _pretty(testo):
    """Piccolo restyling cosmetico del testo semplice (usato dove non generiamo LaTeX
    dedicato, es. le spiegazioni passo-passo): rende leggibili gli operatori Python."""
    if not isinstance(testo, str):
        return testo
    return testo.replace("**", "^").replace("*", "·")


def _enunciato_latex(chiave, es):
    """Costruisce una versione LaTeX (da rendere con KaTeX) dell'enunciato dell'esercizio,
    in aggiunta al testo semplice 'testo' (usato come fallback e dalla versione desktop)."""
    try:
        if chiave == "serie":
            n = serie.n
            return r"\sum_{n=1}^{\infty} " + _tex(es["termine_generale"])
        if chiave == "taylor":
            return (r"f(x) = " + _tex(es["funzione"])
                    + r",\quad x_0 = " + _tex(es["x0"])
                    + r",\quad \text{ordine } " + str(es["ordine"]))
        if chiave == "lagrange":
            f_tex = _tex(es["f"])
            if es["tipo_vincolo"] == "retta":
                vincolo_tex = r"x + y = " + _tex(es["vincolo_c"])
            else:
                vincolo_tex = r"x^2 + y^2 = " + _tex(es["vincolo_r"] ** 2)
            return r"f(x,y) = " + f_tex + r",\quad " + vincolo_tex
        if chiave == "edo":
            return (r"y'' + " + _tex(es["a"]) + r"y' + " + _tex(es["b"]) + r"y = " + _tex(es["forzante"])
                    + r",\quad y(0) = " + _tex(es["y0"]) + r",\ y'(0) = " + _tex(es["y1"]))
        if chiave == "integrali":
            if es["tipo"] == "cerchio_pieno":
                dominio_tex = r"D = \{(x,y): x^2+y^2 \le " + _tex(es["r_max"] ** 2) + r"\}"
            else:
                dominio_tex = (r"D = \{(x,y): " + _tex(es["r_min"] ** 2)
                                + r" \le x^2+y^2 \le " + _tex(es["r_max"] ** 2) + r"\}")
            return r"\iint_D " + _tex(es["integranda_xy"]) + r"\, dA, \quad " + dominio_tex
        if chiave == "punti_liberi":
            return r"f(x,y) = " + _tex(sp.expand(es["f"]))
        if chiave == "edo1":
            eq = es["equazione"]
            return (_tex(eq.lhs) + " = " + _tex(eq.rhs)
                    + r",\quad y(" + _tex(es["x0"]) + r") = " + _tex(es["y0"]))
        if chiave == "continuita":
            f_tex = _tex(es["f"])
            return (r"f(x,y) = \begin{cases} " + f_tex + r" & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}")
    except Exception:
        return None
    return None


def _passo(testo, latex=None):
    return {"testo": testo, "latex": latex}


def _spiega_serie_latex(es):
    """Ricostruisce spiega_convergenza() di serie.py passo per passo, in LaTeX."""
    n = serie.n
    tipo = es["tipo"]
    passi = [_passo("Termine generale:", r"a_n = " + _tex(es["termine_generale"]))]

    if tipo == "potenza_p":
        p = es["p"]
        passi.append(_passo("Passo 1 — riconosciamo la forma: è una serie armonica generalizzata.",
                             r"\sum \frac{1}{n^p}"))
        passi.append(_passo("Passo 2 — criterio: la serie p converge se e solo se p>1, diverge se p≤1.", None))
        esito = "p>1" if p > 1 else r"p\le 1"
        passi.append(_passo(f"Passo 3 — qui p = {p}, quindi:", esito))

    elif tipo == "geometrica_polinomiale":
        r_val, k = es["r"], es["k"]
        rapporto = sp.simplify(es["termine_generale"].subs(n, n + 1) / es["termine_generale"])
        limite = sp.limit(rapporto, n, sp.oo)
        passi.append(_passo("Passo 1 — applichiamo il criterio del rapporto:",
                             r"L=\lim_{n\to\infty}\frac{a_{n+1}}{a_n}"))
        passi.append(_passo("Passo 2 — calcoliamo il rapporto e il limite:",
                             r"\frac{a_{n+1}}{a_n}=" + _tex(rapporto) + r"\ \Rightarrow\ L=" + _tex(limite)))
        passi.append(_passo(f"Passo 3 — il fattore polinomiale n^{k} non influisce sul limite: "
                             f"L coincide con la ragione r = {r_val}.", None))
        if limite < 1:
            esito = r"L<1 \Rightarrow \text{CONVERGE}"
        elif limite > 1:
            esito = r"L>1 \Rightarrow \text{DIVERGE}"
        else:
            esito = r"L=1 \Rightarrow \text{criterio non decisivo}"
        passi.append(_passo("Passo 4 — conclusione del criterio del rapporto:", esito))

    elif tipo == "alternata":
        p = es["p"]
        passi.append(_passo("Passo 1 — la serie è alternata (compare (-1)^n); isoliamo il valore assoluto:",
                             r"|a_n| = \frac{1}{n^{" + _tex(p) + r"}}"))
        passi.append(_passo("Verifichiamo le due ipotesi del criterio di Leibniz: |a_n| è DECRESCENTE "
                             "(perché n^p, con p>0, è crescente in n, quindi 1/n^p è decrescente) ed "
                             "è INFINITESIMA (perché 1/n^p → 0 per n→∞).",
                             r"|a_{n+1}|<|a_n|,\qquad \lim_{n\to\infty}|a_n|=0"))
        passi.append(_passo("Passo 2 — essendo entrambe le ipotesi verificate, per il criterio di "
                             "Leibniz la serie converge (almeno condizionatamente).", None))
        passi.append(_passo("Passo 3 — verifichiamo la convergenza assoluta studiando la serie p:",
                             r"\sum \frac{1}{n^{" + _tex(p) + r"}}"))
        assoluta = (r"p>1 \Rightarrow \text{converge ANCHE assolutamente}" if p > 1
                    else r"p\le 1 \Rightarrow \text{SOLO condizionatamente convergente}")
        passi.append(_passo(f"Passo 4 — qui p = {p}:", assoluta))

    else:  # confronto_asintotico
        a_val, c = es["a"], es["c"]
        confronto = 1 / n
        rapporto = sp.simplify(es["termine_generale"] / confronto)
        limite = sp.limit(rapporto, n, sp.oo)
        passi.append(_passo("Passo 1 — per n grande confrontiamo con la serie armonica:", r"b_n=\frac1n"))
        passi.append(_passo("Passo 2 — calcoliamo il limite del rapporto a_n/b_n:",
                             r"L=\lim_{n\to\infty}\frac{a_n}{b_n}=" + _tex(limite)))
        passi.append(_passo("Passo 3 — poiché 0<L<∞, per il criterio del confronto asintotico le due serie "
                             "hanno lo stesso comportamento.", None))
        passi.append(_passo("Passo 4 — la serie armonica diverge, quindi anche la serie data diverge:",
                             r"\sum \frac1n \to \infty"))

    conclusione = r"\textbf{CONVERGE}" if es["converge"] else r"\textbf{DIVERGE}"
    passi.append(_passo("Conclusione: la serie", conclusione))
    return passi


def _spiega_taylor_latex(es):
    """Ricostruisce spiega_taylor() di taylor.py passo per passo, in LaTeX."""
    x = taylor.x
    f, x0, ordine = es["funzione"], es["x0"], es["ordine"]
    passi = [_passo("Formula generale:",
                     r"f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)")]
    passi.append(_passo("Passo 1 — calcolo le derivate successive e le valuto in x0:", None))

    termini = []
    for k in range(ordine + 1):
        dk = sp.diff(f, x, k)
        val = sp.simplify(dk.subs(x, x0))
        passi.append(_passo(f"k = {k}:",
                             r"f^{(" + str(k) + r")}(x)=" + _tex(dk)
                             + r"\ \Rightarrow\ f^{(" + str(k) + r")}(" + _tex(x0) + r")=" + _tex(val)))
        termini.append((k, val))

    passi.append(_passo("Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:", None))
    base_tex = "x" if x0 == 0 else ("(x-" + _tex(x0) + ")")
    for k, val in termini:
        coeff = sp.nsimplify(val / sp.factorial(k))
        termine_tex = _tex(coeff) if k == 0 else _tex(coeff) + base_tex + "^{" + str(k) + "}"
        passi.append(_passo(f"k = {k}:",
                             _tex(val) + "/" + str(k) + r"! = " + _tex(coeff) + r"\ \Rightarrow\ " + termine_tex))

    passi.append(_passo("Passo 3 — sommando tutti i termini, il polinomio di Taylor è:",
                         "P_{" + str(ordine) + "}(x) = " + _tex(es["sviluppo_atteso"])
                         + " + o(" + base_tex + "^{" + str(ordine) + "})"))
    return passi


def _spiega_lagrange_latex(es):
    """Ricostruisce spiega_lagrange() di multivariabile.py passo per passo, in LaTeX."""
    x, y = multivariabile.x, multivariabile.y
    f, g = es["f"], es["g"]
    grad_f = [sp.diff(f, v) for v in (x, y)]
    grad_g = [sp.diff(g, v) for v in (x, y)]

    passi = [_passo("Funzione e vincolo:",
                     "f(x,y)=" + _tex(sp.expand(f)) + r",\quad g(x,y)=" + _tex(g) + "=0")]
    passi.append(_passo("Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.",
                         r"\nabla f = \lambda \nabla g,\quad g=0"))
    passi.append(_passo("Sistema da risolvere:",
                         _tex(grad_f[0]) + r"=\lambda(" + _tex(grad_g[0]) + r")\quad,\quad "
                         + _tex(grad_f[1]) + r"=\lambda(" + _tex(grad_g[1]) + r")\quad,\quad "
                         + _tex(g) + "=0"))
    passi.append(_passo("Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due "
                         "gradienti paralleli, il loro \"prodotto incrociato\" deve annullarsi -- "
                         "equazione equivalente al sistema sopra, ma senza λ:",
                         _tex(sp.expand(grad_f[0] * grad_g[1] - grad_f[1] * grad_g[0])) + "=0"))
    passi.append(_passo("Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i "
                         "punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del "
                         "sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello "
                         "di g):", None))
    for (px, py, val), lam_v in zip(es["punti"], es["lambda_per_punto"]):
        gfx = grad_f[0].subs({x: px, y: py}); gfy = grad_f[1].subs({x: px, y: py})
        ggx = grad_g[0].subs({x: px, y: py}); ggy = grad_g[1].subs({x: px, y: py})
        passi.append(_passo("", "(x,y)=(" + _tex(px) + "," + _tex(py) + r"),\ \lambda=" + _tex(lam_v)
                             + r":\quad \nabla f=(" + _tex(gfx) + "," + _tex(gfy) + r")\ =\ \lambda\nabla g="
                             + r"(" + _tex(sp.simplify(lam_v * ggx)) + "," + _tex(sp.simplify(lam_v * ggy))
                             + r")\ \Rightarrow\ f=" + _tex(val)))

    passi.append(_passo("Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): "
                         "posto L=f-\\lambda g,",
                         r"\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ "
                         r"g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad "
                         r"\overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}"))
    for (px, py, val), lam_v, cl in zip(es["punti"], es["lambda_per_punto"], es["classificazioni_orlato"]):
        passi.append(_passo("", "(x,y)=(" + _tex(px) + "," + _tex(py) + r"),\ \lambda=" + _tex(lam_v)
                             + r":\quad \det\overline{H}=" + _tex(cl["det"]) + r"\ \Rightarrow\ "
                             + r"\textbf{" + cl["tipo"] + "}"))

    if es["tipo_vincolo"] == "cerchio":
        passi.append(_passo("Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). "
                             "Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano "
                             "TUTTI i valori di f nei punti stazionari, anche quelli relativi):",
                             r"\max f=" + _tex(es["valore_max"]) + r",\quad \min f=" + _tex(es["valore_min"])))
    else:
        passi.append(_passo("Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma "
                             "quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:",
                             r"\min f=" + _tex(es["valore_min"]) + r",\quad \max f:\ \text{non esiste}"))
    return passi


def _spiega_edo_latex(es):
    """Ricostruisce spiega_edo() di edo.py passo per passo, in LaTeX -- con lo svolgimento
    completo della particolare (per sostituzione dell'ansatz) e del sistema lineare per le
    condizioni iniziali, non solo il risultato finale (che resta comunque quello
    pre-verificato in es["soluzione_generale"]/es["soluzione_attesa"]: i passaggi aggiuntivi
    sono ricalcolati qui solo per mostrarli, e vengono scartati silenziosamente se per
    qualche motivo non tornano coerenti con quel risultato)."""
    x = edo.x
    a, b = es["a"], es["b"]
    forzante = es["forzante"]
    y0, y1 = es["y0"], es["y1"]
    r_sym = sp.symbols("r")
    radici = sp.solve(sp.Eq(r_sym ** 2 + a * r_sym + b, 0), r_sym)
    C1, C2 = sp.symbols("C1 C2")

    passi = [_passo("Equazione:",
                     "y''+" + _tex(a) + "y'+" + _tex(b) + "y=" + _tex(forzante)
                     + r",\quad y(0)=" + _tex(y0) + r",\ y'(0)=" + _tex(y1))]
    passi.append(_passo("Passo 1 — equazione caratteristica dell'omogenea associata:",
                         "r^2+" + _tex(a) + "r+" + _tex(b) + r"=0\ \Rightarrow\ " + _tex(radici)))

    y_om_alt = None
    if len(radici) == 1:
        r0 = radici[0]
        y_om = C1 * sp.exp(r0 * x) + C2 * x * sp.exp(r0 * x)
        passi.append(_passo("Radice reale doppia:",
                             "r=" + _tex(r0) + r"\ \Rightarrow\ y_{om}(x)=c_1e^{" + _tex(r0)
                             + "x}+c_2xe^{" + _tex(r0) + "x}"))
    elif all(rad.is_real for rad in radici):
        y_om = C1 * sp.exp(radici[0] * x) + C2 * sp.exp(radici[1] * x)
        y_om_alt = C1 * sp.exp(radici[1] * x) + C2 * sp.exp(radici[0] * x)
        passi.append(_passo("Radici reali distinte:",
                             r"y_{om}(x)=c_1e^{" + _tex(radici[0]) + "x}+c_2e^{" + _tex(radici[1]) + "x}"))
    else:
        alpha = sp.re(radici[0])
        beta = sp.Abs(sp.im(radici[0]))
        # sympy scrive sempre la parte omogenea come C1*sin(..)+C2*cos(..), in quest'ordine
        # (verificato empiricamente): costruiamo y_om con la stessa convenzione, altrimenti la
        # sottrazione sotto (per isolare y_p) non si cancella e resta sporca di C1/C2.
        y_om = sp.exp(alpha * x) * (C1 * sp.sin(beta * x) + C2 * sp.cos(beta * x))
        passi.append(_passo("Radici complesse coniugate:",
                             _tex(alpha) + r"\pm i" + _tex(beta)
                             + r"\ \Rightarrow\ y_{om}(x)=e^{" + _tex(alpha) + "x}\\left(c_1\\cos(" + _tex(beta)
                             + "x)+c_2\\sin(" + _tex(beta) + "x)\\right)"))

    passi.append(_passo("Passo 2 — forma della soluzione particolare (metodo di somiglianza): "
                         + edo._descrivi_ansatz(a, b, forzante), None))

    # y_p isolata per sottrazione dalla soluzione generale (stessi simboli C1,C2 di sympy);
    # verificata per sostituzione diretta nell'equazione prima di mostrarla, cosi' non si
    # rischia mai di esporre un passaggio inconsistente con la soluzione gia' calcolata.
    try:
        y_gen_expr = es["soluzione_generale"].rhs
        y_p = None
        # per radici reali distinte sympy a volte assegna C1/C2 alla radice "opposta"
        # rispetto all'ordine restituito dal nostro solve() qui sopra (capita con radici
        # irrazionali): proviamo entrambi gli abbinamenti e teniamo quello che si cancella
        # in una y_p pulita (senza C1/C2 residui).
        for tentativo in [y_om] + ([y_om_alt] if y_om_alt is not None else []):
            cand = sp.simplify(sp.expand(y_gen_expr - tentativo))
            residuo = sp.simplify(sp.diff(cand, x, 2) + a * sp.diff(cand, x) + b * cand - forzante)
            if residuo == 0 and cand != 0 and not cand.has(C1, C2):
                y_p = cand
                break
        if y_p is not None:
            passi.append(_passo("Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo "
                                 "dei coefficienti indeterminati) si trova la soluzione particolare:",
                                 "y_p(x) = " + _tex(y_p)))
    except Exception:
        pass

    passi.append(_passo("Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:",
                         "y(x)=" + _tex(es["soluzione_generale"].rhs)))

    # Sistema di Cauchy risolto esplicitamente (con controllo di coerenza col risultato
    # gia' precalcolato: se il confronto non tornasse identico, si torna silenziosamente
    # alla versione sintetica invece di mostrare un procedimento che sembra contraddirlo).
    mostrato = False
    try:
        y_gen_expr = es["soluzione_generale"].rhs
        dy_gen_expr = sp.diff(y_gen_expr, x)
        y0_espr = y_gen_expr.subs(x, 0)
        dy0_espr = dy_gen_expr.subs(x, 0)
        soluz = sp.solve([sp.Eq(y0_espr, y0), sp.Eq(dy0_espr, y1)], [C1, C2], dict=True)
        if soluz:
            costanti = soluz[0]
            y_finale = sp.simplify(y_gen_expr.subs(costanti))
            if sp.simplify(y_finale - es["soluzione_attesa"].rhs) == 0:
                passi.append(_passo("Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) "
                                     "in x=0 e li uguagliamo ai valori assegnati:",
                                     "y(0)=" + _tex(y0_espr) + "=" + _tex(y0)
                                     + r",\quad y'(0)=" + _tex(dy0_espr) + "=" + _tex(y1)))
                passi.append(_passo("Risolvendo il sistema lineare in C1, C2:",
                                     "C_1=" + _tex(costanti.get(C1, C1)) + r",\quad C_2="
                                     + _tex(costanti.get(C2, C2))))
                mostrato = True
    except Exception:
        pass
    if not mostrato:
        passi.append(_passo("Passo 4 — imponendo le condizioni iniziali:", None))

    passi.append(_passo("Soluzione del problema di Cauchy:",
                         "y(x)=" + _tex(es["soluzione_attesa"].rhs)))
    return passi


def _dominio_latex(es):
    if es["tipo"] == "cerchio_pieno":
        return r"D = \{(x,y): x^2+y^2 \le " + _tex(es["r_max"] ** 2) + r"\}"
    return (r"D = \{(x,y): " + _tex(es["r_min"] ** 2)
            + r" \le x^2+y^2 \le " + _tex(es["r_max"] ** 2) + r"\}")


def _spiega_integrali_latex(es):
    """Ricostruisce spiega_integrale() di integrali.py passo per passo, in LaTeX -- mostrando
    anche le primitive (integrali indefiniti) intermedie, non solo i valori gia' calcolati
    agli estremi. Se sympy non riuscisse a calcolarle in forma chiusa per qualche caso raro,
    si torna silenziosamente alla versione sintetica (comunque corretta)."""
    r, theta = integrali.r, integrali.theta
    passi = [_passo("Dominio e integranda:",
                     _dominio_latex(es) + r",\quad f(x,y)=" + _tex(es["integranda_xy"]))]
    passi.append(_passo("Passo 1 — cambio in coordinate polari (Jacobiano = r):",
                         r"x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta"))
    passi.append(_passo("f in coordinate polari, con Jacobiano incluso:",
                         r"f(r,\theta)\cdot r = " + _tex(es["integranda_jacobiano"])))
    passi.append(_passo(f"Passo 2 — estremi di integrazione: r ∈ [{es['r_min']}, {es['r_max']}], "
                         "θ nell'angolo giro [0, 2π].", None))

    try:
        primitiva_r = sp.simplify(sp.integrate(es["integranda_jacobiano"], r))
        passi.append(_passo("Passo 3 — calcoliamo prima la primitiva rispetto a r:",
                             r"\int " + _tex(es["integranda_jacobiano"]) + r"\,dr = " + _tex(primitiva_r)))
        passi.append(_passo("e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):",
                             r"\Big[" + _tex(primitiva_r) + r"\Big]_{" + _tex(es["r_min"]) + "}^{"
                             + _tex(es["r_max"]) + "} = " + _tex(es["integrale_interno"])))
    except Exception:
        passi.append(_passo("Passo 3 — integrale interno (rispetto a r):",
                             r"\int_{" + _tex(es["r_min"]) + "}^{" + _tex(es["r_max"]) + "} "
                             + _tex(es["integranda_jacobiano"]) + r"\,dr = " + _tex(es["integrale_interno"])))

    try:
        primitiva_theta = sp.simplify(sp.integrate(es["integrale_interno"], theta))
        passi.append(_passo("Passo 4 — allo stesso modo, la primitiva rispetto a θ:",
                             r"\int " + _tex(es["integrale_interno"]) + r"\,d\theta = "
                             + _tex(primitiva_theta)))
        passi.append(_passo("valutata tra 0 e 2π:",
                             r"\Big[" + _tex(primitiva_theta) + r"\Big]_0^{2\pi} = "
                             + _tex(es["valore_atteso"])))
    except Exception:
        passi.append(_passo("Passo 4 — integrale esterno (rispetto a θ):",
                             r"\int_0^{2\pi} " + _tex(es["integrale_interno"]) + r"\,d\theta = "
                             + _tex(es["valore_atteso"])))
    return passi


def _spiega_punti_liberi_latex(es):
    """Ricostruisce spiega_punto_critico() di multivariabile.py passo per passo, in LaTeX."""
    x, y = multivariabile.x, multivariabile.y
    f = es["f"]
    grad = [sp.diff(f, v) for v in (x, y)]
    fxx = sp.diff(f, x, 2); fyy = sp.diff(f, y, 2); fxy = sp.diff(f, x, y)
    hess = sp.hessian(f, (x, y))
    passi = [_passo("Funzione:", "f(x,y) = " + _tex(sp.expand(f)))]
    passi.append(_passo("Passo 1 — annulliamo il gradiente per trovare i punti stazionari:",
                         _tex(grad[0]) + "=0,\\quad" + _tex(grad[1]) + "=0"))
    passi.append(_passo("Passo 2 — calcoliamo le tre derivate parziali seconde:",
                         r"f_{xx}=" + _tex(fxx) + r",\quad f_{yy}=" + _tex(fyy)
                         + r",\quad f_{xy}=" + _tex(fxy)))
    passi.append(_passo("...e ne formiamo la matrice Hessiana:", "H(x,y) = " + _tex(hess)))
    passi.append(_passo("Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi "
                         "valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e "
                         "traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):", None))
    for c in es["classificazioni"]:
        px, py = c["punto"]
        gx = grad[0].subs({x: px, y: py}); gy = grad[1].subs({x: px, y: py})
        H = hess.subs({x: px, y: py})
        passi.append(_passo(f"Punto ({_tex(px)}, {_tex(py)}) — verifica del gradiente:",
                             r"f_x=" + _tex(gx) + r",\ f_y=" + _tex(gy)))
        passi.append(_passo("",
                             "H=" + _tex(H) + r",\ \det H=" + _tex(H.det())
                             + r",\ \mathrm{tr}\,H=" + _tex(H.trace())
                             + r"\ \Rightarrow\ \textbf{" + c["tipo"].upper() + "}"))
    return passi


def _spiega_edo1_latex(es):
    """Ricostruisce spiega_edo_primo_ordine() di edo.py passo per passo, in LaTeX -- con il
    calcolo esplicito del fattore integrante (o della sostituzione di Bernoulli, o dei due
    integrali della separazione di variabili), non solo il risultato finale. Il risultato
    finale mostrato resta sempre quello gia' pre-verificato in es["soluzione_generale"]/
    es["soluzione_attesa"]; i passaggi intermedi qui sono calcoli aggiuntivi (fattore
    integrante, primitive) mostrati per trasparenza, con un fallback alla versione sintetica
    se per qualche esercizio non si riescono a calcolare (raro, ma es. un'integrazione che
    sympy non sa risolvere in forma chiusa)."""
    eq = es["equazione"]
    x0, y0 = es["x0"], es["y0"]
    tipo = es["tipo"]
    x = edo.x
    Yx = edo.Y_(x)
    y_sym = sp.symbols("y")
    passi = [_passo("Equazione:", _tex(eq.lhs) + "=" + _tex(eq.rhs)
                     + r",\quad y(" + _tex(x0) + ")=" + _tex(y0))]

    dettagliato = False
    try:
        if tipo.startswith("lineare"):
            p_expr = sp.simplify(eq.lhs.coeff(Yx))
            q_expr = sp.simplify(eq.rhs)
            passi.append(_passo("Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:",
                                 "p(x)=" + _tex(p_expr) + r",\quad q(x)=" + _tex(q_expr)))
            integrale_p = sp.integrate(p_expr, x)
            mu = sp.simplify(sp.exp(integrale_p))
            passi.append(_passo("Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:",
                                 r"\int p(x)\,dx=" + _tex(integrale_p) + r"\ \Rightarrow\ \mu(x)="
                                 + _tex(mu)))
            integrando = sp.simplify(mu * q_expr)
            integrale_mu_q = sp.integrate(integrando, x)
            passi.append(_passo("Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; "
                                 "calcoliamo l'integrale:",
                                 r"\int \mu(x)q(x)\,dx=" + _tex(integrale_mu_q)))
            passi.append(_passo("Quindi (a meno della costante arbitraria C1):",
                                 "y(x) = " + _tex(es["soluzione_generale"].rhs)))
            dettagliato = True

        elif tipo.startswith("bernoulli"):
            n = 2
            p_expr = sp.simplify(eq.lhs.coeff(Yx))
            q_expr = sp.simplify(sp.cancel(eq.rhs / Yx ** n))
            passi.append(_passo(f"Passo 1 — è di Bernoulli, nella forma y' + p(x)y = q(x)y^{n}, con:",
                                 "p(x)=" + _tex(p_expr) + r",\quad q(x)=" + _tex(q_expr)
                                 + r",\quad n=" + str(n)))
            passi.append(_passo(f"Passo 2 — sostituzione v = y^(1-{n}) = 1/y: dividendo l'equazione per "
                                 f"y^{n} e sostituendo, si ottiene un'equazione LINEARE in v:",
                                 "v'+(" + _tex(-p_expr) + ")v=" + _tex(-q_expr)))
            passi.append(_passo("Passo 3 — si risolve questa equazione lineare in v con lo stesso metodo "
                                 "del fattore integrante (Passo 2-3 del caso 'lineare'), e infine si torna "
                                 "a y=1/v. La soluzione generale (costante arbitraria C1) è:",
                                 "y(x) = " + _tex(es["soluzione_generale"].rhs)))
            dettagliato = True

        else:  # separabile
            rhs = eq.rhs
            g_expr, h_expr_y = rhs.as_independent(Yx)
            h_expr = sp.simplify(h_expr_y.subs(Yx, y_sym))
            passi.append(_passo("Passo 1 — è a variabili separabili, y' = g(x)·h(y), con:",
                                 "g(x)=" + _tex(g_expr) + r",\quad h(y)=" + _tex(h_expr)))
            passi.append(_passo("Passo 2 — separiamo le variabili e integriamo entrambi i membri:",
                                 r"\int\frac{dy}{h(y)}=\int g(x)\,dx"))
            integrale_y = sp.integrate(1 / h_expr, y_sym)
            integrale_x = sp.integrate(g_expr, x)
            passi.append(_passo("Calcolando i due integrali:",
                                 r"\int\frac{dy}{h(y)}=" + _tex(integrale_y)
                                 + r"\qquad,\qquad \int g(x)\,dx=" + _tex(integrale_x) + "+C_1"))
            passi.append(_passo("Passo 3 — isolando y si ottiene la soluzione generale:",
                                 "y(x) = " + _tex(es["soluzione_generale"].rhs)))
            dettagliato = True
    except Exception:
        dettagliato = False

    if not dettagliato:
        if tipo.startswith("lineare"):
            passi.append(_passo("Passo 1 — equazione lineare del primo ordine: si risolve con il "
                                 "fattore integrante μ(x) = e^{∫p(x)dx}.", None))
        elif tipo.startswith("bernoulli"):
            passi.append(_passo("Passo 1 — equazione di Bernoulli: sostituendo v = y^{1-n} si riconduce "
                                 "a un'equazione lineare in v.", None))
        else:
            passi.append(_passo("Passo 1 — equazione a variabili separabili: si separano le variabili e "
                                 "si integrano entrambi i membri.", None))
        passi.append(_passo("Passo 2 — soluzione generale (costante arbitraria C1):",
                             "y(x) = " + _tex(es["soluzione_generale"].rhs)))

    passi.append(_passo("Passo finale — imponendo la condizione iniziale si ottiene:",
                         "y(x) = " + _tex(es["soluzione_attesa"].rhs)))
    return passi


def _spiega_continuita_latex(es):
    """Ricostruisce spiega_continuita() di continuita_differenziabilita.py, in LaTeX."""
    f_expr = es["f"]
    passi = [_passo("Funzione (a tratti, singolare in (0,0)):",
                     r"f(x,y) = " + _tex(f_expr) + r"\ \ (\ne(0,0)),\quad f(0,0)=0")]
    passi.append(_passo("Passo 1 — sostituzione in coordinate polari x=r\\cosθ, y=r\\sinθ:",
                         "f(r,\\theta) \\to " + _tex(es["lim_theta_fisso"]) + r"\ \ (r\to0^+)"))

    if es["evidenza_non_continua"]:
        ev = es["evidenza_non_continua"]
        passi.append(_passo("Passo 2 — il limite dipende da θ (limite direzionale non unico):",
                             r"\theta=" + _tex(ev["theta_a"]) + r":\ " + _tex(ev["val_a"])
                             + r"\quad\ne\quad \theta=" + _tex(ev["theta_b"]) + r":\ " + _tex(ev["val_b"])))
        passi.append(_passo("Conclusione:", r"\textbf{f NON è continua in (0,0)}"))
        return passi

    if es["cammino_controllo"]:
        cc = es["cammino_controllo"]
        passi.append(_passo("Passo 2 — il limite a θ fissato è 0, ma non basta: proviamo il cammino curvo",
                             "y = " + _tex(cc["espressione"])))
        passi.append(_passo("Lungo questo cammino:",
                             r"f(x," + _tex(cc["espressione"]) + r") \to " + _tex(cc["limite_in_k"])
                             + r"\ \ (x\to0,\ \text{dipende da } k)"))
        passi.append(_passo("Conclusione:", r"\textbf{f NON è continua in (0,0)} "
                             r"\text{ (il test lungo le rette era fuorviante)}"))
        return passi

    passi.append(_passo("Passo 2 — il limite è 0 indipendentemente da θ:",
                         r"\textbf{f è continua in (0,0)}"))
    passi.append(_passo("Passo 3 — derivate parziali in (0,0) per definizione:",
                         r"f_x(0,0)=" + _tex(es["fx0"]) + r",\quad f_y(0,0)=" + _tex(es["fy0"])))
    passi.append(_passo("Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:", None))

    if es["differenziabile"]:
        passi.append(_passo("Il limite per r→0+ è 0 indipendentemente da θ.",
                             r"\textbf{f è differenziabile in (0,0)}"))
        passi.append(_passo("Piano tangente in (0,0,0):", "z = " + _tex(es["piano_tangente"])))
    else:
        ev = es["evidenza_non_diff"]
        passi.append(_passo("Il resto dipende da θ:",
                             r"\theta=" + _tex(ev["theta_a"]) + r":\ " + _tex(ev["val_a"])
                             + r"\quad\ne\quad \theta=" + _tex(ev["theta_b"]) + r":\ " + _tex(ev["val_b"])))
        passi.append(_passo("Conclusione:", r"\textbf{f è continua ma NON differenziabile in (0,0)}"))
    return passi


SPIEGATORI_LATEX = {
    "serie": _spiega_serie_latex,
    "taylor": _spiega_taylor_latex,
    "lagrange": _spiega_lagrange_latex,
    "punti_liberi": _spiega_punti_liberi_latex,
    "edo": _spiega_edo_latex,
    "edo1": _spiega_edo1_latex,
    "integrali": _spiega_integrali_latex,
    "continuita": _spiega_continuita_latex,
}

ARGOMENTI = [
    ("Serie numeriche", "serie"),
    ("Sviluppi di Taylor", "taylor"),
    ("Lagrange (multivariabile)", "lagrange"),
    ("Punti stazionari liberi", "punti_liberi"),
    ("EDO 2° ordine / Cauchy", "edo"),
    ("EDO 1° ordine / Cauchy", "edo1"),
    ("Integrali doppi", "integrali"),
    ("Continuità e differenziabilità", "continuita"),
]
NOMI = {chiave: nome for nome, chiave in ARGOMENTI}

# Argomenti per cui NON esiste (per ora) un bucket 'Esame' con problemi reali tratti
# dai testi d'esame: Taylor non compare in nessun appello reale trovato nelle 6 PDF
# analizzate (Ottobre 2025 - Maggio 2026).
ARGOMENTI_SENZA_ESAME = {"taylor"}

GENERATORI = {
    "serie": serie.genera_serie_numerica,
    "taylor": taylor.genera_taylor,
    "lagrange": multivariabile.genera_lagrange,
    "punti_liberi": multivariabile.genera_punto_critico,
    "edo": edo.genera_edo_lineare_secondo_ordine,
    "edo1": edo.genera_edo_primo_ordine,
    "integrali": integrali.genera_integrale_doppio_polare,
    "continuita": continuita_differenziabilita.genera_continuita,
}

SPIEGATORI = {
    "serie": serie.spiega_convergenza,
    "taylor": taylor.spiega_taylor,
    "lagrange": multivariabile.spiega_lagrange,
    "punti_liberi": multivariabile.spiega_punto_critico,
    "edo": edo.spiega_edo,
    "edo1": edo.spiega_edo_primo_ordine,
    "integrali": integrali.spiega_integrale,
    "continuita": continuita_differenziabilita.spiega_continuita,
}

SUGGERIMENTI = {
    "serie": "Scrivi: converge   oppure   diverge",
    "taylor": "Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2",
    "lagrange": "Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').",
    "punti_liberi": "Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.",
    "edo": "Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)",
    "edo1": "Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)",
    "integrali": "Scrivi il valore (numerico o simbolico), es:  pi/2",
    "continuita": "Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua",
}

# Stato dell'esercizio corrente (un solo utente per pagina, come nella GUI desktop).
_stato = {"chiave": None, "es": None}


def nomi_argomenti_json():
    return json.dumps(ARGOMENTI)


def suggerimento(chiave):
    return SUGGERIMENTI.get(chiave, "")


DIFFICOLTA_VALIDE = ("facile", "medio", "difficile")


def nuovo_esercizio(chiave, difficolta="medio"):
    if chiave not in GENERATORI:
        return json.dumps({"errore": f"argomento sconosciuto: {chiave}"})
    if difficolta not in DIFFICOLTA_VALIDE:
        difficolta = "medio"
    es = GENERATORI[chiave](difficolta)
    # Caso raro (soprattutto per 'lagrange'): il sistema puo' non avere soluzioni reali
    # con i parametri casuali scelti. Rigeneriamo invece di mostrare un esercizio vuoto.
    tentativi = 0
    while chiave == "lagrange" and not es.get("punti") and tentativi < 5:
        es = GENERATORI[chiave](difficolta)
        tentativi += 1
    _stato["chiave"] = chiave
    _stato["es"] = es
    return json.dumps({
        "testo": es["testo"],
        "testo_latex": _enunciato_latex(chiave, es),
        "suggerimento": SUGGERIMENTI[chiave],
        "difficolta": difficolta,
    })


def verifica(risposta):
    """Rispecchia esattamente App.verifica() di gui.py."""
    chiave = _stato["chiave"]
    es = _stato["es"]
    if chiave is None or es is None:
        return json.dumps({"errore": "Genera prima un esercizio."})

    risposta = (risposta or "").strip()
    if not risposta:
        return json.dumps({"errore": "Scrivi una risposta prima di verificare."})

    corpo_latex = None
    try:
        if chiave == "serie":
            r = serie.verifica_convergenza(es, risposta)
            corpo = r["spiegazione"]
        elif chiave == "taylor":
            r = taylor.verifica_taylor(es, risposta)
            corpo = f"Sviluppo atteso: {r['sviluppo_atteso']}"
            corpo_latex = r"P_n(x) = " + _tex(r["sviluppo_atteso"])
        elif chiave == "lagrange":
            punti = []
            for riga in risposta.splitlines():
                riga = riga.strip()
                if not riga:
                    continue
                px, py = riga.split(",")
                punti.append((px.strip(), py.strip()))
            r = multivariabile.verifica_lagrange(es, punti)
            massimo = r["valore_max"] if r["valore_max"] is not None else "non esiste (vincolo illimitato)"
            corpo = (f"Punti attesi (x, y, f): {r['punti_attesi']}\n"
                     f"Massimo assoluto: {massimo}   "
                     f"Minimo assoluto: {r['valore_min']}")
            punti_tex = r",\ ".join(
                "(" + _tex(px) + ", " + _tex(py) + ", " + _tex(val) + ")"
                for px, py, val in r["punti_attesi"]
            )
            massimo_tex = _tex(r["valore_max"]) if r["valore_max"] is not None else r"\text{non esiste}"
            corpo_latex = (r"\text{Punti stazionari: } " + punti_tex
                            + r"\quad\text{Massimo} = " + massimo_tex
                            + r",\quad \text{Minimo} = " + _tex(r["valore_min"]))
        elif chiave == "edo":
            r = edo.verifica_edo(es, risposta)
            corpo = f"Soluzione attesa: {r['soluzione_attesa']}"
            corpo_latex = r"y(x) = " + _tex(r["soluzione_attesa"].rhs)
        elif chiave == "integrali":
            r = integrali.verifica_integrale(es, risposta)
            corpo = f"Valore atteso: {r['valore_atteso']}"
            corpo_latex = r"\text{Valore atteso: } " + _tex(r["valore_atteso"])
        else:
            return json.dumps({"errore": "argomento sconosciuto"})
    except Exception as e:
        return json.dumps({"errore": f"Non sono riuscito a interpretare la risposta: {e}"})

    if "errore" in r:
        return json.dumps({"errore": r["errore"]})

    return json.dumps({"corretto": bool(r["corretto"]), "corpo": corpo, "corpo_latex": corpo_latex})


def mostra_soluzione():
    chiave = _stato["chiave"]
    es = _stato["es"]
    if chiave is None or es is None:
        return json.dumps({"errore": "Genera prima un esercizio."})
    try:
        passi = SPIEGATORI_LATEX[chiave](es)
        return json.dumps({"passi": passi})
    except Exception:
        # fallback robusto: se la generazione del LaTeX fallisce per qualche motivo,
        # torniamo comunque alla spiegazione testuale originale (sempre corretta).
        corpo = _pretty(SPIEGATORI[chiave](es))
        return json.dumps({"corpo": corpo})


def mostra_grafico_png():
    chiave = _stato["chiave"]
    es = _stato["es"]
    if chiave is None or es is None:
        return json.dumps({"errore": "Genera prima un esercizio."})
    try:
        import matplotlib
        matplotlib.use("AGG")
        import matplotlib.pyplot as plt
        import grafico
        fig = grafico.GRAFICI[chiave](es)
    except Exception as e:
        return json.dumps({"errore": f"Non sono riuscito a disegnare il grafico: {e}"})

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    return json.dumps({"png_base64": b64})
