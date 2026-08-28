"""
Esercizi su continuita' e differenziabilita' di funzioni di due variabili definite a
tratti, con singolarita' nell'origine (tipico esercizio 1 degli scritti recenti:
"studiare la continuita' e la differenziabilita' in (0,0)", talvolta seguito da
"determinare l'equazione del piano tangente" quando la funzione risulta differenziabile).

Il metodo usato qui e' quello rigoroso (niente maggiorazioni euristiche):
 1) sostituzione in coordinate polari x=r*cos(theta), y=r*sin(theta) e studio del
    limite per r->0+ a theta fissato: se dipende da theta, il limite direzionale NON
    esiste ed f e' gia' discontinua nell'origine;
 2) se il limite a theta fissato e' 0 (indipendente da theta), questo NON basta a
    concludere che f sia continua: bisogna anche escludere che il limite cambi lungo
    cammini curvi (es. y = k*x^2 oppure y = k*x^3), che il test "a theta fissato" non
    vede. Per questo ogni funzione del banco e' etichettata con il cammino di
    controllo giusto (nessuno / parabola / cubica) deciso a priori;
 3) se f e' continua, si calcolano le derivate parziali in (0,0) per definizione di
    limite (f(x,0)/x e f(0,y)/y), e si studia il resto [f(x,y) - fx*x - fy*y] / r in
    polari: se tende a 0 indipendentemente da theta, f e' differenziabile (e il piano
    tangente e' z = fx*x + fy*y); altrimenti no.
"""
import sympy as sp

x, y, r, theta, k = sp.symbols('x y r theta k', real=True)


def _polar(expr):
    return sp.simplify(expr.subs({x: r * sp.cos(theta), y: r * sp.sin(theta)}))


# Ogni voce: (etichetta, f(x,y) per (x,y) != (0,0), metodo di controllo aggiuntivo)
# metodo in {'nessuno', 'parabola', 'cubica'}: cammino curvo da testare quando il
# limite a theta fissato risulta (misleadingly) indipendente da theta.
_POOLS_CONTINUITA = {
    'facile': [
        (x * y / (x**2 + y**2), 'nessuno'),
        (x**2 + y**2, 'nessuno'),
        (x**2 * y / (x**2 + y**2), 'nessuno'),
        (x**3 / (x**2 + y**2), 'nessuno'),
        (x**2 * y**2 / (x**2 + y**2), 'nessuno'),
    ],
    'medio': [
        ((x**2 - y**2) / (x**2 + y**2), 'nessuno'),
        (y**3 / (x**2 + y**2), 'nessuno'),
        (x * y**2 / (x**2 + y**4), 'nessuno'),
        (x * y * (x**2 - y**2) / (x**2 + y**2), 'nessuno'),
        (x * y / sp.sqrt(x**2 + y**2), 'nessuno'),
    ],
    'difficile': [
        (x**2 * y / (x**4 + y**2), 'parabola'),
        (x**3 * y / (x**6 + y**2), 'cubica'),
        ((x**3 + y**3) / (x**2 + y**2), 'nessuno'),
        (x**2 * y**3 / (x**4 + y**6), 'nessuno'),
        (y**4 / (x**2 + y**2), 'nessuno'),
    ],
}


def _passo(testo, latex=None):
    return {'testo': testo, 'latex': latex}


def genera_continuita(difficolta='medio', indice=0):
    """indice seleziona quale delle 5 funzioni curate per quella difficolta' usare
    (0..4): a differenza degli altri argomenti, qui il banco e' fisso/curato (non
    parametrico casuale) perche' la classificazione di continuita'/differenziabilita'
    va verificata rigorosamente per ciascuna funzione, non generata a caso."""
    pool = _POOLS_CONTINUITA.get(difficolta, _POOLS_CONTINUITA['medio'])
    f_expr, metodo = pool[indice % len(pool)]

    testo = (
        "Studiare la continuita' e la differenziabilita' in (0,0) della funzione\n"
        f"f(x,y) = {f_expr}  per (x,y) != (0,0),   f(0,0) = 0.\n"
        "(non sono ammesse maggiorazioni: usare sostituzioni esatte)"
    )

    p = _polar(f_expr)
    lim_theta = sp.simplify(sp.limit(p, r, 0, '+'))
    dipende_da_theta = lim_theta.has(theta)

    continua = None
    evidenza_non_continua = None
    cammino_controllo = None

    if dipende_da_theta:
        continua = False
        v0 = sp.simplify(lim_theta.subs(theta, 0))
        v1 = sp.simplify(lim_theta.subs(theta, sp.pi / 4))
        evidenza_non_continua = {
            'tipo': 'direzionale', 'theta_a': 0, 'val_a': v0,
            'theta_b': sp.pi / 4, 'val_b': v1,
        }
    else:
        if metodo == 'nessuno':
            continua = True
        else:
            var_esp = 2 if metodo == 'parabola' else 3
            cammino = k * x**var_esp
            val_cammino = sp.simplify(f_expr.subs(y, cammino))
            lim_cammino = sp.simplify(sp.limit(val_cammino, x, 0))
            cammino_controllo = {'metodo': metodo, 'espressione': cammino, 'limite_in_k': lim_cammino}
            # i due casi 'parabola'/'cubica' del banco sono scelti apposta come trappole: il
            # limite lungo il cammino curvo dipende da k, quindi la funzione NON e' continua.
            continua = not lim_cammino.has(k)

    es = {
        'testo': testo, 'f': f_expr, 'difficolta': difficolta, 'indice': indice,
        'metodo_controllo': metodo, 'lim_theta_fisso': lim_theta,
        'continua': continua, 'evidenza_non_continua': evidenza_non_continua,
        'cammino_controllo': cammino_controllo,
    }

    if continua:
        fx0 = sp.limit(f_expr.subs(y, 0) / x, x, 0)
        fy0 = sp.limit(f_expr.subs(x, 0) / y, y, 0)
        resto = sp.simplify(f_expr - fx0 * x - fy0 * y)
        p2 = sp.simplify(_polar(resto) / r)
        lim2 = sp.simplify(sp.limit(p2, r, 0, '+'))
        differenziabile = not lim2.has(theta) and sp.simplify(lim2) == 0
        es['fx0'] = fx0
        es['fy0'] = fy0
        es['differenziabile'] = differenziabile
        if differenziabile:
            es['piano_tangente'] = fx0 * x + fy0 * y
        else:
            v0 = sp.simplify(lim2.subs(theta, 0))
            v1 = sp.simplify(lim2.subs(theta, sp.pi / 2))
            es['evidenza_non_diff'] = {'theta_a': 0, 'val_a': v0, 'theta_b': sp.pi / 2, 'val_b': v1}
    else:
        es['differenziabile'] = None  # non ha senso chiedersi la differenziabilita'

    return es


def spiega_continuita(esercizio):
    f_expr = esercizio['f']
    righe = [f"f(x,y) = {f_expr}  per (x,y) != (0,0),  f(0,0) = 0.", ""]
    righe.append("Passo 1 — sostituzione in coordinate polari x=r*cos(theta), y=r*sin(theta):")
    righe.append(f"  f(r,theta) = {esercizio['lim_theta_fisso']}   (limite per r->0+, a theta fissato)")

    if esercizio['evidenza_non_continua']:
        ev = esercizio['evidenza_non_continua']
        righe.append("")
        righe.append("Passo 2 — il limite dipende da theta: il limite direzionale non e' unico, quindi "
                     "il limite (x,y)->(0,0) NON esiste.")
        righe.append(f"  theta={ev['theta_a']}: limite = {ev['val_a']}     "
                     f"theta={ev['theta_b']}: limite = {ev['val_b']}   (valori diversi)")
        righe.append("")
        righe.append("Conclusione: f NON e' continua in (0,0).")
        return "\n".join(righe)

    if esercizio['cammino_controllo']:
        cc = esercizio['cammino_controllo']
        righe.append("")
        righe.append("Passo 2 — il limite a theta fissato e' 0, ma questo NON basta: bisogna "
                     "escludere anche cammini curvi. Proviamo il cammino "
                     f"y = k*x^{2 if cc['metodo']=='parabola' else 3}:")
        righe.append(f"  f(x, {cc['espressione']}) -> limite per x->0 = {cc['limite_in_k']}  "
                     "(dipende da k: cambia a seconda della curva scelta)")
        righe.append("")
        righe.append("Conclusione: f NON e' continua in (0,0) (il test lungo le rette e' fuorviante: "
                     "serve verificare anche i cammini curvi).")
        return "\n".join(righe)

    righe.append("")
    righe.append("Passo 2 — il limite e' identicamente 0 per ogni theta, ed e' maggiorato da una "
                 "quantita' che tende a 0 con r indipendentemente da theta: quindi f E' continua in (0,0).")
    righe.append("")
    righe.append("Passo 3 — calcoliamo le derivate parziali in (0,0) per definizione:")
    righe.append(f"  fx(0,0) = lim_(x->0) f(x,0)/x = {esercizio['fx0']}")
    righe.append(f"  fy(0,0) = lim_(y->0) f(0,y)/y = {esercizio['fy0']}")
    righe.append("")
    righe.append("Passo 4 — studiamo il resto [f(x,y) - fx(0,0)x - fy(0,0)y] / r in coordinate polari:")

    if esercizio['differenziabile']:
        righe.append("  il limite per r->0+ e' 0, indipendentemente da theta.")
        righe.append("")
        righe.append("Conclusione: f E' differenziabile in (0,0).")
        righe.append(f"Piano tangente in (0,0,0):  z = {esercizio['piano_tangente']}")
    else:
        ev = esercizio['evidenza_non_diff']
        righe.append(f"  theta={ev['theta_a']}: limite = {ev['val_a']}     "
                     f"theta={ev['theta_b']}: limite = {ev['val_b']}   (valori diversi -> il limite non esiste)")
        righe.append("")
        righe.append("Conclusione: f e' continua ma NON differenziabile in (0,0).")
    return "\n".join(righe)


def verifica_continuita(esercizio, risposta_continua, risposta_differenziabile=None):
    """risposta_continua/risposta_differenziabile: bool o None (se non richiesto)."""
    ok = (bool(risposta_continua) == bool(esercizio['continua']))
    if esercizio['continua'] and risposta_differenziabile is not None:
        ok = ok and (bool(risposta_differenziabile) == bool(esercizio['differenziabile']))
    return {
        'corretto': ok, 'continua_atteso': esercizio['continua'],
        'differenziabile_atteso': esercizio.get('differenziabile'),
    }
