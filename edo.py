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


def _costruisci_edo_primo_ordine(tipo, a, b, x0, y0):
    """tipo in {'lineare','lineare_var','bernoulli_xy2','bernoulli_var',
    'separabile_xy','separabile_1py2','separabile_x2y2'}. Restituisce (eq, testo_eq)."""
    if tipo == 'lineare':
        forzante = b if b is not None else sp.exp(2 * x)
        eq = sp.Eq(Y_(x).diff(x) + a * Y_(x), forzante)
        testo_eq = f"y' + {a}y = {forzante}"
    elif tipo in ('lineare_var', 'lineare_var2'):
        eq = sp.Eq(Y_(x).diff(x) + sp.Rational(a) * Y_(x) / x, x**b)
        testo_eq = f"y' + ({a}/x)y = x^{b}"
    elif tipo == 'separabile_xy':
        eq = sp.Eq(Y_(x).diff(x), a * x * Y_(x))
        testo_eq = f"y' = {a}xy"
    elif tipo == 'separabile_1py2':
        eq = sp.Eq(Y_(x).diff(x), a * (1 + Y_(x)**2) * x)
        testo_eq = f"y' = {a}x(1+y^2)"
    elif tipo == 'separabile_x2y2':
        eq = sp.Eq(Y_(x).diff(x), a * x**2 * Y_(x)**2)
        testo_eq = f"y' = {a}x^2y^2"
    elif tipo == 'bernoulli_xy2':
        eq = sp.Eq(Y_(x).diff(x) + Y_(x), a * x * Y_(x)**2)
        testo_eq = f"y' + y = {a}xy^2"
    elif tipo == 'bernoulli_var':
        eq = sp.Eq(Y_(x).diff(x) + sp.Rational(a) * Y_(x) / x, Y_(x)**2)
        testo_eq = f"y' + ({a}/x)y = y^2"
    else:
        raise ValueError(f"tipo sconosciuto: {tipo}")
    return eq, testo_eq


def Y_(v):
    return sp.Function('y')(v)


# Banco curato (deterministico) di problemi di Cauchy del primo ordine: lineari a
# coefficienti costanti o variabili (fattore integrante), Bernoulli, a variabili
# separabili. Ogni tupla e' (tipo, a, b, x0, y0); tutte verificate con sp.dsolve.
_POOLS_EDO1 = {
    'facile': [
        ('lineare', 2, 4, 0, 1),
        ('lineare', 1, 3, 0, 0),
        ('separabile_xy', 1, None, 0, 1),
        ('separabile_xy', 2, None, 0, 1),
        ('lineare', -1, 4, 0, 1),
    ],
    'medio': [
        ('lineare_var', 1, 2, 1, 1),
        ('bernoulli_xy2', 1, None, 0, 1),
        ('separabile_1py2', 1, None, 0, 0),
        ('lineare', -1, None, 0, 0),
        ('bernoulli_var', -1, None, 1, 1),
    ],
    'difficile': [
        ('lineare_var2', -2, 3, 1, 2),
        ('separabile_x2y2', 1, None, 0, 1),
        ('lineare_var', -1, 4, 1, 1),
        ('bernoulli_xy2', 2, None, 0, 1),
        ('separabile_1py2', 1, None, 0, 1),
    ],
}

_NOMI_TIPO_EDO1 = {
    'lineare': 'lineare del primo ordine (fattore integrante)',
    'lineare_var': 'lineare del primo ordine a coefficienti variabili (fattore integrante)',
    'lineare_var2': 'lineare del primo ordine a coefficienti variabili (fattore integrante)',
    'bernoulli_xy2': 'di Bernoulli',
    'bernoulli_var': 'di Bernoulli',
    'separabile_xy': 'a variabili separabili',
    'separabile_1py2': 'a variabili separabili',
    'separabile_x2y2': 'a variabili separabili',
}


def genera_edo_primo_ordine(difficolta='medio', indice=0):
    pool = _POOLS_EDO1.get(difficolta, _POOLS_EDO1['medio'])
    tipo, a, b, x0, y0 = pool[indice % len(pool)]
    eq, testo_eq = _costruisci_edo_primo_ordine(tipo, a, b, x0, y0)

    testo = (f"Risolvere il problema di Cauchy (equazione {_NOMI_TIPO_EDO1[tipo]}):  "
             f"{testo_eq},  con y({x0}) = {y0}.")

    Yx = Y_(x)
    soluzione_generale = sp.dsolve(eq, Yx)
    soluzione = sp.dsolve(eq, Yx, ics={Yx.func(x0): y0})

    return {
        'testo': testo, 'tipo': tipo, 'a': a, 'b': b, 'x0': x0, 'y0': y0,
        'difficolta': difficolta, 'indice': indice, 'equazione': eq,
        'soluzione_generale': soluzione_generale, 'soluzione_attesa': soluzione,
    }


def verifica_edo_primo_ordine(esercizio, risposta_str):
    try:
        y_utente = sp.sympify(risposta_str)
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}

    eq = esercizio['equazione']
    # sostituzione diretta di y_utente al posto di y(x) e y'(x) in entrambi i membri:
    yx = sp.Function('y')(x)
    espressione = (eq.lhs - eq.rhs).subs(yx.diff(x), sp.diff(y_utente, x)).subs(yx, y_utente)
    residuo = sp.simplify(espressione)
    eq_ok = (residuo == 0)
    ic_ok = sp.simplify(y_utente.subs(x, esercizio['x0']) - esercizio['y0']) == 0

    ok = bool(eq_ok) and bool(ic_ok)
    return {
        'corretto': ok, 'soddisfa_equazione': eq_ok, 'condizione_iniziale': ic_ok,
        'soluzione_attesa': esercizio['soluzione_attesa'],
    }


def spiega_edo_primo_ordine(esercizio):
    tipo = esercizio['tipo']
    x0, y0 = esercizio['x0'], esercizio['y0']
    eq = esercizio['equazione']
    righe = [f"Equazione {_NOMI_TIPO_EDO1[tipo]}:  {eq},   y({x0}) = {y0}.", ""]

    if tipo.startswith('lineare'):
        righe.append("Passo 1 — e' un'equazione lineare del primo ordine y' + p(x)y = q(x): si "
                     "risolve con il fattore integrante mu(x) = e^(integrale di p(x) dx).")
        righe.append(f"Passo 2 — soluzione generale (a meno della costante arbitraria C1):")
        righe.append(f"  y(x) = {esercizio['soluzione_generale'].rhs}")
        righe.append("Passo 3 — imponendo la condizione iniziale si determina C1 e si ottiene:")
        righe.append(f"  y(x) = {esercizio['soluzione_attesa'].rhs}")
    elif tipo.startswith('bernoulli'):
        righe.append("Passo 1 — e' un'equazione di Bernoulli y' + p(x)y = q(x)y^n: si divide per "
                     "y^n e si sostituisce v = y^(1-n), riconducendola a un'equazione lineare in v.")
        righe.append("Passo 2 — risolvendo l'equazione lineare in v e tornando a y si ottiene "
                     "(a meno della costante arbitraria):")
        righe.append(f"  y(x) = {esercizio['soluzione_generale'].rhs}")
        righe.append("Passo 3 — imponendo la condizione iniziale si determina la costante:")
        righe.append(f"  y(x) = {esercizio['soluzione_attesa'].rhs}")
    else:  # separabile
        righe.append("Passo 1 — e' un'equazione a variabili separabili y' = g(x)h(y): si separano "
                     "le variabili e si integrano entrambi i membri, dy/h(y) = g(x) dx.")
        righe.append("Passo 2 — integrando si ottiene (a meno della costante arbitraria):")
        righe.append(f"  y(x) = {esercizio['soluzione_generale'].rhs}")
        righe.append("Passo 3 — imponendo la condizione iniziale si determina la costante:")
        righe.append(f"  y(x) = {esercizio['soluzione_attesa'].rhs}")
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
