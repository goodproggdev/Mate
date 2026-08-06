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

import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

import serie
import taylor
import multivariabile
import edo
import integrali
import grafico


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
    except Exception:
        return None
    return None

ARGOMENTI = [
    ("Serie numeriche", "serie"),
    ("Sviluppi di Taylor", "taylor"),
    ("Lagrange (multivariabile)", "lagrange"),
    ("EDO / Cauchy", "edo"),
    ("Integrali doppi", "integrali"),
]
NOMI = {chiave: nome for nome, chiave in ARGOMENTI}

GENERATORI = {
    "serie": serie.genera_serie_numerica,
    "taylor": taylor.genera_taylor,
    "lagrange": multivariabile.genera_lagrange,
    "edo": edo.genera_edo_lineare_secondo_ordine,
    "integrali": integrali.genera_integrale_doppio_polare,
}

SPIEGATORI = {
    "serie": serie.spiega_convergenza,
    "taylor": taylor.spiega_taylor,
    "lagrange": multivariabile.spiega_lagrange,
    "edo": edo.spiega_edo,
    "integrali": integrali.spiega_integrale,
}

SUGGERIMENTI = {
    "serie": "Scrivi: converge   oppure   diverge",
    "taylor": "Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2",
    "lagrange": "Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').",
    "edo": "Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)",
    "integrali": "Scrivi il valore (numerico o simbolico), es:  pi/2",
}

# Stato dell'esercizio corrente (un solo utente per pagina, come nella GUI desktop).
_stato = {"chiave": None, "es": None}


def nomi_argomenti_json():
    return json.dumps(ARGOMENTI)


def suggerimento(chiave):
    return SUGGERIMENTI.get(chiave, "")


def nuovo_esercizio(chiave):
    if chiave not in GENERATORI:
        return json.dumps({"errore": f"argomento sconosciuto: {chiave}"})
    es = GENERATORI[chiave]()
    # Caso raro (soprattutto per 'lagrange'): il sistema puo' non avere soluzioni reali
    # con i parametri casuali scelti. Rigeneriamo invece di mostrare un esercizio vuoto.
    tentativi = 0
    while chiave == "lagrange" and not es.get("punti") and tentativi < 5:
        es = GENERATORI[chiave]()
        tentativi += 1
    _stato["chiave"] = chiave
    _stato["es"] = es
    return json.dumps({
        "testo": es["testo"],
        "testo_latex": _enunciato_latex(chiave, es),
        "suggerimento": SUGGERIMENTI[chiave],
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
    corpo = _pretty(SPIEGATORI[chiave](es))
    return json.dumps({"corpo": corpo})


def mostra_grafico_png():
    chiave = _stato["chiave"]
    es = _stato["es"]
    if chiave is None or es is None:
        return json.dumps({"errore": "Genera prima un esercizio."})
    try:
        fig = grafico.GRAFICI[chiave](es)
    except Exception as e:
        return json.dumps({"errore": f"Non sono riuscito a disegnare il grafico: {e}"})

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    return json.dumps({"png_base64": b64})
