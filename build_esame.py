# -*- coding: utf-8 -*-
"""
Unisce il banco 'Esame' (esame_bank.py, problemi reali scritti a mano) dentro
esercizi.json, che deve gia' contenere il banco procedurale (generato da
precompute.py). Da rilanciare ogni volta che esame_bank.py cambia.
"""
import json

import bridge
import esame_bank

PATH = "esercizi.json"

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

# --- Moduli con i problemi aggiuntivi (uno per gruppo di argomenti) ---------------
import importlib, re
for _m in ("esame_bank_integrali", "esame_bank_edo", "esame_bank_ottimizzazione",
           "esame_bank_serie_continuita"):
    importlib.import_module(_m)

# Voci vecchie rilette sui PDF e risultate errate: sostituite dalle versioni corrette nei moduli sopra.
_DA_TOGLIERE = {
    ("edo", "[25 ottobre 2025, Esercizio 2]"),
    ("edo", "[9 maggio 2026, Esercizio 2]"),
    ("edo", "[16 gennaio 2026, Esercizio 2]"),
    ("edo1", "[18 ottobre 2025, Esercizio 2]"),
}
for _k in list(esame_bank.ESAME):
    esame_bank.ESAME[_k] = [v for v in esame_bank.ESAME[_k]
                            if not any(v["testo"].startswith(t) for (kk, t) in _DA_TOGLIERE if kk == _k)]

# --- Ordine: piu' recenti prima (data piu' alta citata nella fonte), a parita' ordine di inserimento ---
_MESI = {m: i + 1 for i, m in enumerate("gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre".split())}
def _data_fonte(v):
    best = (0, 0, 0)
    for g, m, a in re.findall(r"(?:(\d{1,2})\s+)?(" + "|".join(_MESI) + r")\s+(\d{4})", v["fonte"].lower()):
        best = max(best, (int(a), _MESI[m], int(g) if g else 0))
    return best
for _k in esame_bank.ESAME:
    esame_bank.ESAME[_k] = sorted(esame_bank.ESAME[_k], key=_data_fonte, reverse=True)

for chiave, voci in esame_bank.ESAME.items():
    if chiave not in d["esercizi"]:
        continue
    if voci:
        d["esercizi"][chiave]["esame"] = voci
    elif "esame" in d["esercizi"][chiave]:
        del d["esercizi"][chiave]["esame"]

for arg in d["argomenti"]:
    chiave = arg["chiave"]
    ha_contenuto = bool(esame_bank.ESAME.get(chiave))
    arg["ha_esame"] = ha_contenuto and chiave not in bridge.ARGOMENTI_SENZA_ESAME

# ---------------------------------------------------------------------------
# ID stabili: "chiave/difficolta/indice". Stabili perche' la generazione e'
# deterministica (seed fissi in precompute.py, ordine fisso in esame_bank.py),
# quindi rieseguendo la pipeline gli stessi esercizi finiscono sempre alla
# stessa posizione. Servono per tracciare i singoli esercizi sbagliati
# (funzione "Ripassa i tuoi errori").
# ---------------------------------------------------------------------------
for chiave, banco in d["esercizi"].items():
    for difficolta, voci in banco.items():
        for i, es in enumerate(voci):
            es["id"] = f"{chiave}/{difficolta}/{i}"

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)

# Riferimenti al formulario in ogni passo (campi "form" / "form_nota"): vedi annota_formulario.py
import annota_formulario
annota_formulario.main(PATH)

tot_esame = sum(len(v) for v in esame_bank.ESAME.values())
tot_proc = sum(len(vv) for banco in d["esercizi"].values()
               for k, vv in banco.items() if k != "esame")
print(f"Merge completato: {tot_proc} procedurali + {tot_esame} esame = {tot_proc + tot_esame} totali")
for arg in d["argomenti"]:
    n = len(d["esercizi"][arg["chiave"]].get("esame", []))
    print(f"  {arg['chiave']:14s} ha_esame={arg['ha_esame']!s:5s} esame={n}")
