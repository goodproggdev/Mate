# -*- coding: utf-8 -*-
"""
Post-elaborazione di esercizi.json: aggiunge a ogni passo della soluzione i riferimenti al
formulario ("form": ["id_blocco" oppure "id_blocco#n"]) con una breve nota ("form_nota").
Gli id puntano ai blocchi di formulario_blocks.json; "#n" evidenzia l'n-esimo punto della scaletta.
Si lancia dopo build_esame.py:  python3 annota_formulario.py
"""
import json, re, sys

R = {
 "serie": [
  (r"limite per n", ["serie_scaletta#4"], "Scaletta serie, punto 4: calcola il limite del criterio."),
  (r"termine generale", ["serie_scaletta#1"], "Scaletta serie, punto 1: scrivi a_n e controlla se tende a 0."),
  (r"armonica|serie p|\bp ?[>≤]|qui p", ["uff_serie"], "Tabella delle serie notevoli (formulario ufficiale): armonica generalizzata, converge se p>1."),
  (r"alternata|leibniz|assolut", ["serie_criteri"], "Criteri: Leibniz per segni alterni e convergenza assoluta (sez. 9.2)."),
  (r"rapporto|fattorial", ["serie_criteri", "serie_scaletta#3"], "Scaletta punto 3-4: fattoriali/esponenziali ⇒ criterio del rapporto, poi limite."),
  (r"radice|potenze n-esime", ["serie_criteri", "serie_scaletta#3"], "Scaletta punto 3: potenze n-esime ⇒ criterio della radice."),
  (r"confront|a_n/b_n", ["serie_criteri", "serie_scaletta#3"], "Criterio del confronto asintotico con la serie armonica generalizzata."),
  (r"fratti|parziale|accorcia|fattorizziamo il denominatore|secondo termine tende", ["serie_telescopica"], "Serie telescopica: fratti semplici e somma parziale (sez. 9.3)."),
  (r"geometric|ragione|q\(x\)|converge se e solo se \|q|dominio: q|risolvendo la disequazione|per x[<>]|verifica per x|primo termine|potenze in base|conclusione . la serie converge", ["serie_geometrica", "uff_serie", "serie_scaletta#7"], "Serie geometrica con parametro: |q|<1, somma = primo termine/(1−q) (formulario ufficiale + sez. 9.3)."),
 ],
 "taylor": [
  (r"^k = ", ["taylor#4", "uff_maclaurin"], "Passo 4 della scaletta: f^(k)(x0)/k! · (x−x0)^k per ogni k."),
  (r"formula generale|derivate successive|costruisco|sommando", ["taylor", "uff_maclaurin"], "Scaletta Taylor (sez. 8.5) e sviluppi noti di Mac Laurin (formulario ufficiale)."),
 ],
 "lagrange": [
  (r"^passo \d+ . il vincolo è compatto|^passo \d+ . il vincolo è chiuso|^conclusione|per weierstrass", ["compatto", "vinc_scaletta#8"], "Vincolo compatto ⇒ Weierstrass: max e min assoluti, confronta i valori di f (sez. 8.1 e scaletta punto 8)."),
  (r"orlato|hessiano orlat|^nel punto", ["uff_orlato", "vinc_scaletta#6", "determinanti"], "Hessiano orlato (formulario ufficiale): H̄>0 ⇒ massimo, H̄<0 ⇒ minimo; il determinante 3×3 si calcola con Sarrus/Laplace."),
  (r"regolarit", ["vinc_scaletta#2"], "Scaletta vincolati, punto 2: controllo di regolarità ∇g≠0."),
  (r"lagrangiana", ["vinc_scaletta#3"], "Scaletta vincolati, punto 3: Lagrangiana 𝓛=f−λg e sistema ∇𝓛=0."),
  (r"weierstrass|compatt|chiuso e limitato|non limitato", ["compatto", "vinc_scaletta#8"], "Vincolo compatto? ⇒ Weierstrass: max e min assoluti (sez. 8.1 e scaletta punto 8)."),
  (r"vincolo|circonferenza|parabola|retta|ellisse|completando", ["vinc_scaletta#1", "curve", "completa_quadrato"], "Scaletta punto 1: riconosci la curva del vincolo (sez. 8.1: tabella delle curve, completare il quadrato)."),
  (r"vettoriale|eliminare|dalla prima equazione|risolvendo|sistema|punti stazionari", ["vinc_scaletta#4"], "Scaletta punto 4: risolvi il sistema senza perdere casi (elimina λ con f_x g_y − f_y g_x = 0)."),
 ],
 "punti_liberi": [
  (r"annulliamo il gradiente", ["liberi_scaletta#1", "liberi_procedura"], "Scaletta liberi, punto 1: ∇f=0, fattorizza e apri un ramo per fattore."),
  (r"derivate parziali seconde|hessiana", ["liberi_scaletta#2", "uff_hessiano"], "Scaletta punto 2: derivate seconde e matrice Hessiana."),
  (r"per ogni punto|verifichiamo|^punto", ["liberi_scaletta#3", "uff_hessiano"], "Teorema dell'Hessiano (formulario ufficiale): H>0 e f_xx>0 min; H>0 e f_xx<0 max; H<0 sella."),
  (r"attenzione|nulla|indecid|determinante nullo", ["liberi_scaletta#5", "liberi_procedura"], "Se H=0 il test non decide: studia il segno di f attorno al punto (sez. 11.2)."),
  (r"dominio", ["dominio_2var"], "Dominio di f(x,y) (sez. 10.2)."),
 ],
 "edo": [
  (r"caratteristica|^radic", ["edo2_omogenea", "edo2_scaletta#1"], "Equazione caratteristica e tabella Δ → y_om (sez. 15.2, scaletta punto 1)."),
  (r"^termine|forma della soluzione particolare|ansatz per|risonan", ["uff_somiglianza", "edo2_somiglianza", "edo2_scaletta#3"], "Metodo di somiglianza (formulario ufficiale, Casi 1–5) + controllo della risonanza con le radici."),
  (r"sostituendo|uguagliando", ["edo2_somiglianza", "edo2_chiuse", "edo2_scaletta#4"], "Scaletta punto 4: sostituisci l'ansatz, uguaglia i coefficienti (formule chiuse in sez. 15.4)."),
  (r"sovrapposizione|soluzione generale", ["edo2_scaletta#5", "edo2_omogenea"], "Scaletta punto 5: y = y_om + y_p."),
  (r"condizioni iniziali|cauchy|sistema lineare", ["edo2_scaletta#6", "edo2_omogenea"], "Scaletta punto 6: Cauchy imposto sulla soluzione completa (sez. 15.2, passo finale)."),
  (r"omogenea", ["edo2_omogenea"], "Omogenea associata (sez. 15.2)."),
 ],
 "edo1": [
  (r"bernoulli|sostituzione v|ripristinando|linear.*in v|\bt\b.*t'", ["edo1_bernoulli", "edo1_scaletta#6"], "Bernoulli: v=y^(1−n) rende l'equazione lineare (sez. 14.2)."),
  (r"fattore integrante|coefficienti variabili|e lineare|è lineare|equazione lineare|lineare del primo|integrando e moltiplicando|soluzione generale e|soluzione generale è", ["uff_edo1_lineari", "edo1_lineare", "edo1_scaletta#5"], "EDO lineare (formulario ufficiale): y = e^A [∫ b e^(−A) dx + c]; tabella dei fattori integranti μ(x) in sez. 14.2."),
  (r"separabil|separiamo|isolando y", ["edo1_separabili", "edo1_scaletta#4"], "Variabili separabili: ∫dy/h(y) = ∫g(x)dx + c (sez. 14.2)."),
  (r"calcolando i due integrali|quindi \(a meno", ["integrali_base"], "Primitive di base (sez. 8.3)."),
  (r"condizione iniziale|passo finale|imponendo|cauchy", ["edo1_scaletta#7"], "Scaletta punto 7: Cauchy per ricavare la costante."),
  (r"soluzione generale|sostituendo", ["edo1_bernoulli", "edo1_scaletta#6"], "Bernoulli: dopo aver risolto in v si torna a y (sez. 14.2)."),
 ],
 "integrali": [
  (r"scrivo l'integrale|integrale iterato|estremi di integrazione|^passo \d+ . imposto", ["int_scaletta#5", "int_formule"], "Scaletta punto 5: scrivi l'integrale iterato con gli estremi (domini normali, sez. 13.2)."),
  (r"dominio normale|scelgo l'ordine|ordine di integrazione|scambi|inverto l'ordine", ["int_scaletta#4", "int_casi", "int_formule"], "Scaletta punto 4: scegli l'ordine che non obbliga a spezzare D; con integrande senza primitiva scambia (sez. 13.3)."),
  (r"^passo \d+ . integro|integro rispetto|integriamo rispetto", ["integrali_base", "int_scaletta#6"], "Scaletta punto 6: integra prima la variabile interna, poi l'esterna; primitive in sez. 8.3."),
  (r"dominio e integranda", ["int_scaletta#1", "disegno_dominio"], "Scaletta integrale doppio, punto 1: disegna D (procedura in sez. 8.6)."),
  (r"cambio in coordinate polari|polari|jacobiano", ["polari", "int_scaletta#3", "int_formule"], "Polari: dx dy = r dr dθ (sez. 8.1 e 13.2)."),
  (r"estremi di integrazione", ["int_scaletta#5", "polari"], "Scaletta punto 5: estremi (r ∈ [r1,r2], θ nel suo intervallo)."),
  (r"primitiva|valutata|valutiamo", ["integrali_base", "int_scaletta#6"], "Scaletta punto 6: integra prima la variabile interna; primitive in sez. 8.3."),
  (r"intersezion|lato|lati|le curve|tra la parabola|integrando|si integra", ["int_scaletta#2", "int_casi", "int_formule"], "Scaletta punti 2-5: intersezioni, scelta dell'ordine, estremi di un dominio normale (sez. 13.2-13.3)."),
 ],
 "continuita": [
  (r"dominio", ["dominio_2var", "cont_scaletta#8"], "Dominio di f(x,y): radicandi ≥0, denominatori ≠0, log>0 (sez. 10.2)."),
  (r"segno", ["cont_procedura"], "Procedura sez. 10.3, punto 1: segno di f."),
  (r"passo [a-d]\)? . (continuit|differenziab)|polinomio", ["cont_procedura", "cont_differenziale"], "Un polinomio è C¹ ⇒ differenziabile (teorema del differenziale totale, sez. 10.3)."),
  (r"maggior|am-gm|\|sin|arctan|cos\(t\)|circa|log\(1", ["cont_strumenti"], "Strumenti e limiti notevoli per le maggiorazioni (sez. 10.3)."),
  (r"gradiente|stazionari|hessian", ["liberi_scaletta#1", "uff_hessiano"], "Punti stazionari e Hessiana (formulario ufficiale, sez. 11)."),
  (r"piano tangente", ["uff_piano_tg", "cont_scaletta#6"], "Piano tangente (formulario ufficiale): z = f + f_x(x−x0) + f_y(y−y0)."),
  (r"derivate parziali", ["cont_scaletta#3", "cont_procedura"], "Scaletta punto 3: derivate parziali in (0,0) per definizione."),
  (r"resto|differenziabilit|rapporto", ["cont_scaletta#4", "cont_procedura"], "Scaletta punto 4: limite del resto diviso r in polari."),
  (r"limite dipende|non basta|cammino|curv", ["cont_scaletta#2", "cont_procedura"], "Scaletta punto 2: se il limite dipende da θ non è continua; se è 0 prova curve y=kx²."),
  (r"sostituiamo x=|polari|passiamo al limite|il limite è|limite per r|\bcontinu", ["cont_scaletta#1", "cont_procedura"], "Scaletta punto 1: coordinate polari e limite per r→0 (sez. 10.3, metodo A)."),
 ],
}

def annota(chiave, passi):
    rules = R.get(chiave, [])
    for p in passi:
        p.pop("form", None); p.pop("form_nota", None)
        t = (p.get("testo") or "").strip().lower()
        if not t:
            continue
        for rx, ids, nota in rules:
            if re.search(rx, t):
                p["form"] = ids
                p["form_nota"] = nota
                break

def main(path):
    d = json.load(open(path, encoding="utf8"))
    tot = ann = 0
    for k, livelli in d["esercizi"].items():
        for lv, lista in livelli.items():
            for e in lista:
                annota(k, e["passi"])
                for p in e["passi"]:
                    if (p.get("testo") or "").strip():
                        tot += 1
                        ann += 1 if p.get("form") else 0
    json.dump(d, open(path, "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
    print("passi con testo:", tot, " annotati con formulario:", ann)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "esercizi.json")
