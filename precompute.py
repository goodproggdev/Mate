"""
Script di precompute: genera il banco statico completo degli esercizi (esercizi.json)
chiamando direttamente i moduli Python nativi (nessun Pyodide qui: gira offline, una
tantum, con Python "vero" e sympy/matplotlib installati nel sandbox).

Per ogni esercizio salviamo tutto cio' che serve al frontend per funzionare SENZA
piu' eseguire Python nel browser:
  - testo / testo_latex : enunciato
  - suggerimento         : formato risposta atteso
  - passi                : spiegazione passo-passo (con LaTeX)
  - grafico_png          : immagine PNG in base64 (o null se non applicabile)
  - risposta             : dati per la verifica lato JS (vedi _risposta_* sotto)

La verifica delle risposte lato JS e' fatta con mathjs: per gli esercizi la cui
risposta e' una FUNZIONE (taylor, edo 2° e 1° ordine) confrontiamo l'espressione
scritta dall'utente con quella attesa per uguaglianza numerica su alcuni punti
campione (tecnica standard: due funzioni "ragionevoli" -es. polinomi di grado
basso, esponenziali, ecc.- che coincidono su abbastanza punti sono la stessa
funzione). Per gli altri argomenti la risposta e' un numero, una scelta o un
insieme di punti, verificata direttamente.
"""
import json
import io
import base64
import random

import sympy as sp
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

import serie
import taylor
import multivariabile
import edo
import integrali
import continuita_differenziabilita as cd
import grafico
import bridge

OUT_PATH = "esercizi.json"

DIFFICOLTA = ["facile", "medio", "difficile"]


def _num(v):
    """Converte un valore sympy in float Python (per confronti numerici lato JS)."""
    return float(sp.N(v))


def _tex(v):
    return sp.latex(v)


def _grafico_png(chiave, es):
    try:
        fig = grafico.GRAFICI[chiave](es)
    except Exception as e:
        print(f"  [!] grafico fallito per {chiave}: {e}")
        return None
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=105, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def _campioni_funzione(f_num_expr, var, punti_x):
    """Valuta un'espressione sympy in una lista di punti x, restituendo [[x,y],...]
    (solo punti dove il valore e' finito e reale)."""
    out = []
    for xv in punti_x:
        try:
            val = complex(f_num_expr.subs(var, xv).evalf())
            if abs(val.imag) > 1e-8:
                continue
            out.append([float(xv), float(val.real)])
        except Exception:
            continue
    return out


# ---------------------------------------------------------------------------
# Costruttori di 'risposta' (dati di verifica) per ciascun argomento
# ---------------------------------------------------------------------------

def _risposta_serie(es):
    return {"tipo": "scelta", "atteso": "converge" if es["converge"] else "diverge"}


def _risposta_taylor(es):
    x = taylor.x
    x0 = es["x0"]
    poly = es["sviluppo_atteso"]
    offsets = [-1.0, -0.6, -0.3, 0.3, 0.6, 1.0]
    punti_x = [x0 + o for o in offsets]
    campioni = _campioni_funzione(poly, x, punti_x)
    return {"tipo": "funzione_su_campioni", "campioni": campioni}


def _risposta_edo2(es):
    x = edo.x
    y_expr = es["soluzione_attesa"].rhs
    punti_x = [0.0, 0.4, 0.8, 1.2, 1.8, 2.5]
    campioni = _campioni_funzione(y_expr, x, punti_x)
    return {"tipo": "funzione_su_campioni", "campioni": campioni}


def _risposta_edo1(es):
    x = edo.x
    y_expr = es["soluzione_attesa"].rhs
    x0 = float(es["x0"])
    if es["tipo"] in ("lineare_var", "lineare_var2", "bernoulli_var"):
        punti_x = [x0 + o for o in (0.05, 0.3, 0.6, 1.0, 1.5, 2.0)]
    else:
        punti_x = [x0 + o for o in (-0.6, -0.3, 0.2, 0.5, 0.9, 1.3)]
    campioni = _campioni_funzione(y_expr, x, punti_x)
    return {"tipo": "funzione_su_campioni", "campioni": campioni}


def _risposta_lagrange(es):
    punti = [[_num(px), _num(py), _num(val)] for px, py, val in es["punti"]]
    return {
        "tipo": "punti_valore", "punti_attesi": punti,
        "valore_max": (_num(es["valore_max"]) if es["valore_max"] is not None else None),
        "valore_min": _num(es["valore_min"]),
    }


def _risposta_punti_liberi(es):
    attesi = [[_num(c["punto"][0]), _num(c["punto"][1]), c["tipo"]] for c in es["classificazioni"]]
    return {"tipo": "punti_classificati", "attesi": attesi}


def _risposta_integrali(es):
    val = es["valore_atteso"]
    return {"tipo": "numero", "atteso_numero": _num(val), "atteso_display": str(val)}


def _risposta_continuita(es):
    return {
        "tipo": "continuita", "continua": bool(es["continua"]),
        "differenziabile": (bool(es["differenziabile"]) if es.get("differenziabile") is not None else None),
    }


RISPOSTE = {
    "serie": _risposta_serie,
    "taylor": _risposta_taylor,
    "lagrange": _risposta_lagrange,
    "punti_liberi": _risposta_punti_liberi,
    "edo": _risposta_edo2,
    "edo1": _risposta_edo1,
    "integrali": _risposta_integrali,
    "continuita": _risposta_continuita,
}


def _costruisci_voce(chiave, es):
    testo_latex = bridge._enunciato_latex(chiave, es)
    passi = bridge.SPIEGATORI_LATEX[chiave](es)
    png = _grafico_png(chiave, es)
    risposta = RISPOSTE[chiave](es)
    return {
        "testo": es["testo"],
        "testo_latex": testo_latex,
        "suggerimento": bridge.SUGGERIMENTI[chiave],
        "passi": passi,
        "grafico_png": png,
        "risposta": risposta,
    }


# ---------------------------------------------------------------------------
# Generazione: argomenti "curati" (indice deterministico 0..4) vs argomenti
# ancora a generazione casuale (seed fisso + dedup, per riusare i generatori
# gia' testati senza doverli riscrivere come pool curati)
# ---------------------------------------------------------------------------

CURATI = {
    "punti_liberi": multivariabile.genera_punto_critico,
    "edo1": edo.genera_edo_primo_ordine,
    "continuita": cd.genera_continuita,
}

CASUALI = {
    "serie": serie.genera_serie_numerica,
    "taylor": taylor.genera_taylor,
    "lagrange": multivariabile.genera_lagrange,
    "edo": edo.genera_edo_lineare_secondo_ordine,
    "integrali": integrali.genera_integrale_doppio_polare,
}


def genera_procedurali():
    banco = {chiave: {} for _, chiave in bridge.ARGOMENTI}

    for chiave, gen in CURATI.items():
        for diff in DIFFICOLTA:
            voci = []
            for i in range(5):
                es = gen(diff, i)
                voci.append(_costruisci_voce(chiave, es))
                print(f"  {chiave}/{diff}/{i} ok")
            banco[chiave][diff] = voci

    for chiave, gen in CASUALI.items():
        for diff in DIFFICOLTA:
            random.seed(f"{chiave}-{diff}-v1")
            voci = []
            testi_visti = set()
            tentativi = 0
            while len(voci) < 5 and tentativi < 200:
                tentativi += 1
                es = gen(diff)
                if chiave == "lagrange" and not es.get("punti"):
                    continue
                if es["testo"] in testi_visti:
                    continue
                testi_visti.add(es["testo"])
                voci.append(_costruisci_voce(chiave, es))
                print(f"  {chiave}/{diff}/{len(voci)-1} ok")
            if len(voci) < 5:
                raise RuntimeError(f"non sono riuscito a generare 5 esercizi distinti per {chiave}/{diff}")
            banco[chiave][diff] = voci

    return banco


if __name__ == "__main__":
    banco = genera_procedurali()
    out = {
        "argomenti": [{"nome": nome, "chiave": chiave, "ha_esame": chiave not in bridge.ARGOMENTI_SENZA_ESAME}
                       for nome, chiave in bridge.ARGOMENTI],
        "esercizi": banco,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print("Scritto", OUT_PATH)
