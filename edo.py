"""
Esercizi su equazioni differenziali ordinarie: problemi di Cauchy, EDO lineari a coefficienti
costanti del secondo ordine (omogenee + termine forzante).
"""
import random
import sympy as sp

x = sp.symbols('x')


_POOLS_EDO = {
    'facile': {'a': [0], 'b': [1, 4], 'forzante': [sp.Integer(0), x], 'y0y1': [0, 1]},
    'medio': {'a': [0, 2, 4], 'b': [1, 4, 5], 'forzante': [sp.Integer(0), x, sp.exp(x), sp.cos(x)],
              'y0y1': [0, 1, -1, 2]},
    'difficile': {'a': [2, 4, 6], 'b': [4, 5, 6, 8, 10], 'forzante': [x, sp.exp(x), sp.cos(x)],
                  'y0y1': [0, 1, -1, 2, 3]},
}


def genera_edo_lineare_secondo_ordine(difficolta='medio'):
    pool = _POOLS_EDO.get(difficolta, _POOLS_EDO['medio'])
    a = random.choice(pool['a'])
    b = random.choice(pool['b'])
    y0 = random.choice(pool['y0y1'])
    y1 = random.choice(pool['y0y1'])
    forzante = random.choice(pool['forzante'])

    testo = (f"Risolvere il problema di Cauchy:  y'' + {a}y' + {b}y = {forzante},  "
             f"con y(0) = {y0}, y'(0) = {y1}.")

    Y = sp.Function('y')
    eq = sp.Eq(Y(x).diff(x, 2) + a * Y(x).diff(x) + b * Y(x), forzante)
    soluzione_generale = sp.dsolve(eq, Y(x))
    ics = {Y(0): y0, Y(x).diff(x).subs(x, 0): y1}
    soluzione = sp.dsolve(eq, Y(x), ics=ics)

    return {
        'testo': testo, 'a': a, 'b': b, 'y0': y0, 'y1': y1, 'difficolta': difficolta,
        'forzante': forzante, 'soluzione_generale': soluzione_generale,
        'soluzione_attesa': soluzione,
    }


def verifica_edo(esercizio, risposta_str):
    try:
        y_utente = sp.sympify(risposta_str)
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}

    a, b, forzante = esercizio['a'], esercizio['b'], esercizio['forzante']

    residuo = sp.simplify(sp.diff(y_utente, x, 2) + a * sp.diff(y_utente, x, 1)
                           + b * y_utente - forzante)
    eq_ok = (residuo == 0)
    ic1_ok = sp.simplify(y_utente.subs(x, 0) - esercizio['y0']) == 0
    ic2_ok = sp.simplify(sp.diff(y_utente, x).subs(x, 0) - esercizio['y1']) == 0

    ok = bool(eq_ok) and bool(ic1_ok) and bool(ic2_ok)
    return {
        'corretto': ok,
        'soddisfa_equazione': eq_ok,
        'condizione_y0': ic1_ok,
        'condizione_y1': ic2_ok,
        'soluzione_attesa': esercizio['soluzione_attesa'],
    }


def _descrivi_ansatz(a, b, forzante):
    """Descrive la forma della soluzione particolare e segnala eventuale risonanza."""
    if forzante == 0:
        return "y_p = 0 (il termine noto e' nullo, l'equazione e' gia' omogenea)."
    if forzante.is_polynomial(x):
        grado = sp.degree(forzante, x)
        risonanza = (b == 0)  # 0 e' radice solo se b = 0
        if risonanza:
            return (f"il termine noto e' un polinomio di grado {grado}, e 0 e' radice "
                     "dell'equazione caratteristica (risonanza): si cerca y_p = x * (polinomio "
                     f"generico di grado {grado}).")
        return (f"il termine noto e' un polinomio di grado {grado} e 0 non e' radice "
                "dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio "
                f"generico di grado {grado} (es. A*x + B).")
    if forzante.has(sp.exp(x)) and not forzante.has(sp.sin(x), sp.cos(x)):
        risonanza = sp.simplify(1 + a + b) == 0  # 1 e' radice se 1+a+b=0
        if risonanza:
            return ("il termine noto e' del tipo e^x, e 1 e' radice dell'equazione caratteristica "
                     "(risonanza): si cerca y_p = A*x*e^x.")
        return ("il termine noto e' del tipo e^x e 1 non e' radice dell'equazione caratteristica "
                 "(nessuna risonanza): si cerca y_p = A*e^x.")
    if forzante.has(sp.cos(x)) or forzante.has(sp.sin(x)):
        risonanza = (a == 0 and b == 1)  # +-i radici solo se r^2+1=0
        if risonanza:
            return ("il termine noto e' del tipo cos(x)/sin(x), e +-i sono radici dell'equazione "
                     "caratteristica (risonanza): si cerca y_p = x*(A*cos(x) + B*sin(x)).")
        return ("il termine noto e' del tipo cos(x)/sin(x) e +-i non sono radici dell'equazione "
                 "caratteristica (nessuna risonanza): si cerca y_p = A*cos(x) + B*sin(x).")
    return "forma di y_p da determinare in base al tipo di termine noto."


def spiega_edo(esercizio):
    """Ricostruisce equazione caratteristica, soluzione omogenea, ansatz e condizioni iniziali."""
    a, b = esercizio['a'], esercizio['b']
    forzante = esercizio['forzante']
    y0, y1 = esercizio['y0'], esercizio['y1']
    r = sp.symbols('r')
    radici = sp.solve(sp.Eq(r**2 + a * r + b, 0), r)

    righe = [
        f"Equazione: y'' + {a}y' + {b}y = {forzante},   y(0) = {y0}, y'(0) = {y1}.",
        "",
        "Passo 1 — equazione caratteristica dell'omogenea associata:",
        f"  r^2 + {a}r + {b} = 0   ->   radici: {radici}",
    ]

    if len(radici) == 1:
        r0 = radici[0]
        righe.append(f"  Radice reale doppia r = {r0}   ->   "
                     f"y_om(x) = C1*e^({r0}*x) + C2*x*e^({r0}*x)")
    elif all(rad.is_real for rad in radici):
        righe.append(f"  Radici reali distinte   ->   "
                     f"y_om(x) = C1*e^({radici[0]}*x) + C2*e^({radici[1]}*x)")
    else:
        alpha = sp.re(radici[0])
        beta = sp.Abs(sp.im(radici[0]))
        righe.append(f"  Radici complesse coniugate {alpha} +- i*{beta}   ->   "
                     f"y_om(x) = e^({alpha}*x) * (C1*cos({beta}*x) + C2*sin({beta}*x))")

    righe.append("")
    righe.append("Passo 2 — soluzione particolare y_p, in base alla forma del termine noto "
                 "(metodo di somiglianza / coefficienti indeterminati):")
    righe.append(f"  {_descrivi_ansatz(a, b, forzante)}")

    righe.append("")
    righe.append("Passo 3 — per il principio di sovrapposizione, la soluzione generale e' "
                 "y(x) = y_om(x) + y_p(x); sostituendo y_p nell'equazione si determinano i suoi "
                 "coefficienti, ottenendo:")
    righe.append(f"  y(x) = {esercizio['soluzione_generale'].rhs}")

    righe.append("")
    righe.append("Passo 4 — imponiamo le condizioni iniziali per determinare C1 e C2:")
    righe.append(f"  y(0) = {y0}      y'(0) = {y1}")
    righe.append(f"  Soluzione del problema di Cauchy:  y(x) = {esercizio['soluzione_attesa'].rhs}")
    return "\n".join(righe)


def genera_edo_variabili_separabili():
    """EDO del primo ordine integrabile per quadratura (variabili separabili)."""
    k = random.choice([1, 2, 3])
    y0 = random.choice([1, 2, 3])
    testo = f"Risolvere il problema di Cauchy:  y' = {k}*x*y,  con y(0) = {y0}."
    # y' = k x y  ->  y = y0 * exp(k x^2 / 2)
    soluzione_attesa = y0 * sp.exp(k * x**2 / sp.Integer(2))
    return {'testo': testo, 'k': k, 'y0': y0, 'soluzione_attesa': soluzione_attesa}


def verifica_edo_separabile(esercizio, risposta_str):
    try:
        y_utente = sp.sympify(risposta_str)
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}
    diff = sp.simplify(y_utente - esercizio['soluzione_attesa'])
    ok = diff == 0
    return {'corretto': ok, 'soluzione_attesa': esercizio['soluzione_attesa']}
