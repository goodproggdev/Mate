"""
Esercizi su integrali doppi (Riemann per funzioni di piu' variabili), con cambio di
variabili in coordinate polari.
"""
import random
import sympy as sp

x, y, r, theta = sp.symbols('x y r theta')


_POOLS_INTEGRALI = {
    'facile': {'tipi': ['cerchio_pieno'], 'R_pieno': [1, 2, 3], 'R_corona': [1, 2, 3],
               'integ_pieno': [x**2 + y**2, sp.Integer(1)], 'integ_corona': [sp.Integer(1)]},
    'medio': {'tipi': ['cerchio_pieno', 'corona_circolare'], 'R_pieno': [1, 2], 'R_corona': [1, 2, 3],
              'integ_pieno': [x**2 + y**2, x * y, sp.sqrt(x**2 + y**2)],
              'integ_corona': [x**2 + y**2, sp.Integer(1)]},
    'difficile': {'tipi': ['corona_circolare', 'cerchio_pieno'], 'R_pieno': [2, 3], 'R_corona': [1, 2, 3, 4],
                  'integ_pieno': [x*y, sp.sqrt(x**2 + y**2), (x**2 + y**2)**2],
                  'integ_corona': [x*y, (x**2 + y**2)**2, sp.sqrt(x**2 + y**2)]},
}


def genera_integrale_doppio_polare(difficolta='medio'):
    pool = _POOLS_INTEGRALI.get(difficolta, _POOLS_INTEGRALI['medio'])
    tipo = random.choice(pool['tipi'])

    if tipo == 'cerchio_pieno':
        R = random.choice(pool['R_pieno'])
        integranda_xy = random.choice(pool['integ_pieno'])
        dominio_testo = f"D = {{ (x,y) : x^2 + y^2 <= {R**2} }}"
        r_min, r_max = 0, R
    else:
        R1, R2 = sorted(random.sample(pool['R_corona'], 2))
        integranda_xy = random.choice(pool['integ_corona'])
        dominio_testo = f"D = {{ (x,y) : {R1}^2 <= x^2+y^2 <= {R2}^2 }}"
        r_min, r_max = R1, R2

    testo = (f"Calcolare l'integrale doppio di f(x,y) = {integranda_xy} su {dominio_testo}, "
             f"usando le coordinate polari.")
    integranda_polare = sp.simplify(integranda_xy.subs({x: r*sp.cos(theta), y: r*sp.sin(theta)}))
    integranda_jacobiano = sp.simplify(integranda_polare * r)
    integrale_interno = sp.simplify(sp.integrate(integranda_jacobiano, (r, r_min, r_max)))
    integrale_totale = sp.integrate(integrale_interno, (theta, 0, 2*sp.pi))

    return {
        'testo': testo, 'tipo': tipo, 'integranda_xy': integranda_xy, 'difficolta': difficolta,
        'dominio_testo': dominio_testo, 'r_min': r_min, 'r_max': r_max,
        'integranda_polare': integranda_polare, 'integranda_jacobiano': integranda_jacobiano,
        'integrale_interno': integrale_interno, 'valore_atteso': sp.simplify(integrale_totale),
    }


def verifica_integrale(esercizio, risposta_str):
    try:
        risposta = sp.sympify(risposta_str)
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}
    diff = sp.simplify(risposta - esercizio['valore_atteso'])
    ok = diff == 0
    return {'corretto': ok, 'valore_atteso': esercizio['valore_atteso']}


def spiega_integrale(esercizio):
    """Ricostruisce il cambio in coordinate polari e il calcolo passo-passo dell'integrale."""
    righe = [
        f"Dominio: {esercizio['dominio_testo']}.   Integranda: f(x,y) = {esercizio['integranda_xy']}.",
        "",
        "Passo 1 — cambio di variabili in coordinate polari: x = r*cos(theta), y = r*sin(theta), "
        "con Jacobiano dx dy = r dr dtheta.",
        f"  f in coordinate polari: f(r,theta) = {esercizio['integranda_polare']}",
        f"  Integranda con Jacobiano: f(r,theta) * r = {esercizio['integranda_jacobiano']}",
        "",
        f"Passo 2 — estremi di integrazione: essendo il dominio a simmetria circolare/anulare, "
        f"r varia in [{esercizio['r_min']}, {esercizio['r_max']}] e theta nell'intero angolo giro [0, 2*pi].",
        "",
        "Passo 3 — integriamo prima rispetto a r (integrale interno):",
        f"  Integrale da {esercizio['r_min']} a {esercizio['r_max']} di "
        f"[{esercizio['integranda_jacobiano']}] dr = {esercizio['integrale_interno']}",
        "",
        "Passo 4 — integriamo il risultato rispetto a theta (integrale esterno):",
        f"  Integrale da 0 a 2*pi di ({esercizio['integrale_interno']}) dtheta = "
        f"{esercizio['valore_atteso']}",
    ]
    return "\n".join(righe)
