"""
Esercizi sugli sviluppi di Taylor / Mac Laurin e approssimazione di funzioni elementari.
"""
import random
import sympy as sp

x = sp.symbols('x')

FUNZIONI = [sp.exp(x), sp.sin(x), sp.cos(x), sp.log(1 + x), 1 / (1 - x), sp.sqrt(1 + x)]


def genera_taylor():
    f = random.choice(FUNZIONI)
    x0 = 0
    ordine = random.choice([2, 3, 4])
    testo = (f"Scrivere lo sviluppo di Taylor (Mac Laurin) di f(x) = {f} "
             f"centrato in x0={x0}, fino all'ordine {ordine} incluso (con resto di Peano).")
    poly = sp.series(f, x, x0, ordine + 1).removeO()
    return {
        'funzione': f, 'x0': x0, 'ordine': ordine,
        'testo': testo, 'sviluppo_atteso': sp.expand(poly),
    }


def verifica_taylor(esercizio, risposta_str):
    try:
        risposta = sp.sympify(risposta_str)
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}

    diff = sp.expand(risposta - esercizio['sviluppo_atteso'])
    # tronchiamo eventuali termini di ordine superiore che l'utente potrebbe aver incluso
    diff_troncato = sp.series(diff, x, esercizio['x0'], esercizio['ordine'] + 1).removeO()
    ok = sp.simplify(diff_troncato) == 0
    return {
        'corretto': ok,
        'sviluppo_atteso': esercizio['sviluppo_atteso'],
        'differenza_residua': diff_troncato,
    }


def spiega_taylor(esercizio):
    """Ricostruisce il calcolo delle derivate e l'assemblaggio del polinomio di Taylor."""
    f, x0, ordine = esercizio['funzione'], esercizio['x0'], esercizio['ordine']
    righe = [
        f"Formula generale: f(x) = Somma_{{k=0}}^{{n}} [f^(k)(x0)/k!] (x-x0)^k + o((x-x0)^n)",
        "",
        "Passo 1 — calcolo le derivate successive e le valuto in x0:",
    ]
    termini = []
    for k in range(ordine + 1):
        dk = sp.diff(f, x, k)
        val = sp.simplify(dk.subs(x, x0))
        righe.append(f"  f^({k})(x) = {dk}   ->   f^({k})({x0}) = {val}")
        termini.append((k, val))

    righe.append("")
    righe.append("Passo 2 — costruisco ogni termine f^(k)(x0)/k! * (x-x0)^k:")
    for k, val in termini:
        coeff = sp.nsimplify(val / sp.factorial(k))
        base = "x" if x0 == 0 else f"(x-{x0})"
        termine_str = f"{coeff}" if k == 0 else f"{coeff}*{base}^{k}"
        righe.append(f"  k={k}:  {val}/{k}! = {coeff}   ->   termine: {termine_str}")

    righe.append("")
    righe.append("Passo 3 — sommando tutti i termini si ottiene il polinomio di Taylor:")
    righe.append(f"  P_{ordine}(x) = {esercizio['sviluppo_atteso']} + o((x-{x0})^{ordine})")
    return "\n".join(righe)


def genera_limite_con_taylor():
    """Esercizio: calcolare un limite per x->0 usando gli sviluppi di Taylor."""
    coppie = [
        (sp.exp(x) - 1 - x, x**2, sp.Rational(1, 2)),
        (1 - sp.cos(x), x**2, sp.Rational(1, 2)),
        (sp.sin(x) - x, x**3, sp.Rational(-1, 6)),
        (sp.log(1 + x) - x, x**2, sp.Rational(-1, 2)),
    ]
    num, den, valore = random.choice(coppie)
    testo = f"Calcolare, usando gli sviluppi di Taylor:  limite per x->0 di ({num})/({den})"
    return {'testo': testo, 'valore_atteso': valore}


def verifica_limite(esercizio, risposta_str):
    try:
        r = sp.nsimplify(sp.sympify(risposta_str))
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}
    ok = sp.simplify(r - esercizio['valore_atteso']) == 0
    return {'corretto': ok, 'valore_atteso': esercizio['valore_atteso']}
