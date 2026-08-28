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

tot_esame = sum(len(v) for v in esame_bank.ESAME.values())
tot_proc = sum(len(vv) for banco in d["esercizi"].values()
               for k, vv in banco.items() if k != "esame")
print(f"Merge completato: {tot_proc} procedurali + {tot_esame} esame = {tot_proc + tot_esame} totali")
for arg in d["argomenti"]:
    n = len(d["esercizi"][arg["chiave"]].get("esame", []))
    print(f"  {arg['chiave']:14s} ha_esame={arg['ha_esame']!s:5s} esame={n}")
