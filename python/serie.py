"""
Esercizi sulle serie numeriche e sui criteri di convergenza.
Argomento del programma: Serie, Criteri di Convergenza, Serie di potenze.
"""
import random
import sympy as sp

n = sp.symbols('n', positive=True, integer=True)


_POOLS_DIFFICOLTA = {
    'facile': {
        'tipi': ['potenza_p', 'alternata'],
        'p': [1, 2],
        'r': [sp.Rational(1, 2), 2],
        'k': [0],
        'a': [1, 2],
        'c': [1, 3],
    },
    'medio': {
        'tipi': ['potenza_p', 'geometrica_polinomiale', 'alternata', 'confronto_asintotico'],
        'p': [sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3],
        'r': [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), 2, 3, sp.Rational(3, 2)],
        'k': [0, 1, 2, 3],
        'a': [1, 2, 3],
        'c': [1, 3, 5],
    },
    'difficile': {
        'tipi': ['geometrica_polinomiale', 'alternata', 'confronto_asintotico'],
        'p': [sp.Rational(1, 2), sp.Rational(3, 2)],
        'r': [sp.Rational(3, 4), sp.Rational(4, 5), sp.Rational(5, 4), sp.Rational(6, 5)],
        'k': [2, 3, 4],
        'a': [2, 3, 4, 5],
        'c': [5, 7, 9, 11],
    },
}


def genera_serie_numerica(difficolta='medio'):
    """Genera un esercizio: 'studiare il carattere della serie'."""
    pool = _POOLS_DIFFICOLTA.get(difficolta, _POOLS_DIFFICOLTA['medio'])
    tipo = random.choice(pool['tipi'])

    parametri = {}

    if tipo == 'potenza_p':
        p = random.choice(pool['p'])
        converge = p > 1
        criterio = "Serie armonica generalizzata (serie p): converge se e solo se p > 1."
        testo = f"Studiare il carattere della serie:  Somma per n=1..infinito di 1/n^({p})"
        assoluta = converge
        termine_generale = 1 / n**p
        parametri['p'] = p

    elif tipo == 'geometrica_polinomiale':
        r = random.choice(pool['r'])
        k = random.choice(pool['k'])
        converge = r < 1
        criterio = ("Criterio del rapporto: lim a_(n+1)/a_n = r (il fattore polinomiale n^k "
                    "non cambia il risultato). Converge se r < 1, diverge se r > 1.")
        testo = f"Studiare il carattere della serie:  Somma per n=1..infinito di ({r})^n * n^({k})"
        assoluta = converge
        termine_generale = r**n * n**k
        parametri['r'] = r
        parametri['k'] = k

    elif tipo == 'alternata':
        p = random.choice(pool['p'])
        converge = True  # Leibniz: sempre convergente per p > 0
        assoluta = p > 1
        criterio = (f"Criterio di Leibniz: termini decrescenti e infinitesimi -> la serie converge "
                    f"(almeno condizionatamente). Converge assolutamente solo se p > 1 (qui p={p}).")
        testo = f"Studiare il carattere della serie:  Somma per n=1..infinito di (-1)^n / n^({p})"
        termine_generale = (-1)**n / n**p
        parametri['p'] = p

    else:  # confronto_asintotico
        a = random.choice(pool['a'])
        c = random.choice(pool['c'])
        converge = False  # ~ a/n -> diverge come la serie armonica
        assoluta = False
        criterio = ("Confronto asintotico: per n grande il termine si comporta come a/n "
                    "(serie armonica) -> la serie diverge.")
        testo = f"Studiare il carattere della serie:  Somma per n=1..infinito di ({a}n+1)/(n^2+{c})"
        termine_generale = (a * n + 1) / (n**2 + c)
        parametri['a'] = a
        parametri['c'] = c

    return {
        'tipo': tipo,
        'testo': testo,
        'converge': converge,
        'assoluta': assoluta,
        'suggerimento': criterio,
        'termine_generale': termine_generale,
        'difficolta': difficolta,
        **parametri,
    }


def verifica_convergenza(esercizio, risposta):
    """risposta: stringa 'converge' o 'diverge' (case-insensitive)."""
    r = risposta.strip().lower()
    corretto_atteso = 'converge' if esercizio['converge'] else 'diverge'
    ok = r.startswith(corretto_atteso[:5])
    return {
        'corretto': ok,
        'risposta_attesa': corretto_atteso,
        'spiegazione': esercizio['suggerimento'],
    }


def spiega_convergenza(esercizio):
    """Ricostruisce e motiva, passo per passo, lo studio del carattere della serie."""
    tipo = esercizio['tipo']
    righe = [f"Termine generale: a_n = {esercizio['termine_generale']}", ""]

    if tipo == 'potenza_p':
        p = esercizio['p']
        righe += [
            "Passo 1 — riconosciamo la forma: e' una serie armonica generalizzata (serie p) Σ 1/n^p.",
            "Passo 2 — criterio: la serie p converge se e solo se p > 1, diverge se p <= 1.",
            f"Passo 3 — qui p = {p}, quindi p {'> 1' if p > 1 else '<= 1'}.",
        ]

    elif tipo == 'geometrica_polinomiale':
        r_val, k = esercizio['r'], esercizio['k']
        rapporto = sp.simplify(esercizio['termine_generale'].subs(n, n + 1)
                                / esercizio['termine_generale'])
        limite = sp.limit(rapporto, n, sp.oo)
        righe += [
            "Passo 1 — applichiamo il criterio del rapporto: L = lim(n->inf) a_(n+1)/a_n.",
            f"Passo 2 — a_(n+1)/a_n = {rapporto}  ->  L = {limite}",
            f"Passo 3 — il fattore polinomiale n^{k} non influisce sul limite (tende a 1 nel rapporto): "
            f"L coincide con la ragione r = {r_val}.",
            f"Passo 4 — L = {limite} {'< 1' if limite < 1 else ('> 1' if limite > 1 else '= 1')}: "
            + ("per il criterio del rapporto la serie converge." if limite < 1
               else ("per il criterio del rapporto la serie diverge." if limite > 1
                     else "il criterio del rapporto non decide (servirebbe un altro criterio).")),
        ]

    elif tipo == 'alternata':
        p = esercizio['p']
        righe += [
            f"Passo 1 — la serie e' alternata: |a_n| = 1/n^{p} e' positivo, decrescente e -> 0 per n->inf.",
            "Passo 2 — per il criterio di Leibniz una serie alternata con termini decrescenti e "
            "infinitesimi converge (almeno condizionatamente).",
            f"Passo 3 — verifichiamo la convergenza assoluta: Σ 1/n^{p} e' una serie p, converge "
            "assolutamente se e solo se p > 1.",
            f"Passo 4 — qui p = {p} "
            + (f"> 1, quindi la serie converge ANCHE assolutamente."
               if p > 1 else "<= 1, quindi la serie e' SOLO condizionatamente convergente."),
        ]

    else:  # confronto_asintotico
        a_val, c = esercizio['a'], esercizio['c']
        confronto = 1 / n
        rapporto = sp.simplify(esercizio['termine_generale'] / confronto)
        limite = sp.limit(rapporto, n, sp.oo)
        righe += [
            "Passo 1 — per n grande il grado del numeratore (1) e' inferiore di 1 rispetto al "
            "denominatore (2): confrontiamo con b_n = 1/n (serie armonica).",
            f"Passo 2 — L = lim(n->inf) a_n/b_n = lim(n->inf) {rapporto} = {limite}",
            f"Passo 3 — poiche' 0 < L < infinito (L = {limite}), per il criterio del confronto "
            "asintotico le due serie hanno lo stesso comportamento.",
            "Passo 4 — Σ 1/n (serie armonica) diverge  ->  quindi anche la serie data diverge.",
        ]

    righe.append("")
    righe.append(f"Conclusione: la serie {'CONVERGE' if esercizio['converge'] else 'DIVERGE'}.")
    return "\n".join(righe)


def genera_serie_di_potenze():
    """Genera un esercizio sul raggio di convergenza di una serie di potenze."""
    x0 = random.choice([0, 1, -1, 2])
    a = random.choice([2, 3, sp.Rational(1, 2)])
    k = random.choice([0, 1])
    # c_n = a^n / n^k  ->  raggio R = 1/a (il fattore polinomiale non influisce sul raggio)
    R = sp.nsimplify(1 / a)
    testo = (f"Determinare il raggio di convergenza della serie di potenze:  "
             f"Somma per n=1..infinito di (x-{x0})^n / (({a})^n * n^{k})")
    return {'testo': testo, 'x0': x0, 'a': a, 'k': k, 'raggio_atteso': R}


def verifica_raggio(esercizio, risposta_str):
    try:
        r_utente = sp.nsimplify(sp.sympify(risposta_str))
    except Exception as e:
        return {'corretto': False, 'errore': f'Espressione non valida: {e}'}
    ok = sp.simplify(r_utente - esercizio['raggio_atteso']) == 0
    return {'corretto': ok, 'raggio_atteso': esercizio['raggio_atteso']}
