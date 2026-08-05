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

import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

import serie
import taylor
import multivariabile
import edo
import integrali
import grafico

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
    _stato["chiave"] = chiave
    _stato["es"] = es
    return json.dumps({"testo": es["testo"], "suggerimento": SUGGERIMENTI[chiave]})


def verifica(risposta):
    """Rispecchia esattamente App.verifica() di gui.py."""
    chiave = _stato["chiave"]
    es = _stato["es"]
    if chiave is None or es is None:
        return json.dumps({"errore": "Genera prima un esercizio."})

    risposta = (risposta or "").strip()
    if not risposta:
        return json.dumps({"errore": "Scrivi una risposta prima di verificare."})

    try:
        if chiave == "serie":
            r = serie.verifica_convergenza(es, risposta)
            corpo = r["spiegazione"]
        elif chiave == "taylor":
            r = taylor.verifica_taylor(es, risposta)
            corpo = f"Sviluppo atteso: {r['sviluppo_atteso']}"
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
        elif chiave == "edo":
            r = edo.verifica_edo(es, risposta)
            corpo = f"Soluzione attesa: {r['soluzione_attesa']}"
        elif chiave == "integrali":
            r = integrali.verifica_integrale(es, risposta)
            corpo = f"Valore atteso: {r['valore_atteso']}"
        else:
            return json.dumps({"errore": "argomento sconosciuto"})
    except Exception as e:
        return json.dumps({"errore": f"Non sono riuscito a interpretare la risposta: {e}"})

    if "errore" in r:
        return json.dumps({"errore": r["errore"]})

    return json.dumps({"corretto": bool(r["corretto"]), "corpo": corpo})


def mostra_soluzione():
    chiave = _stato["chiave"]
    es = _stato["es"]
    if chiave is None or es is None:
        return json.dumps({"errore": "Genera prima un esercizio."})
    corpo = SPIEGATORI[chiave](es)
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
