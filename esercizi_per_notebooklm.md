# Banco esercizi — Metodi Matematici

Raccolta completa degli esercizi del sito, organizzati per argomento e livello di difficoltà. Per ogni esercizio: testo, formato di risposta atteso, svolgimento passo-passo (con la spiegazione del *perché* si esegue ogni passaggio) e risposta corretta. Le immagini dei grafici sono state omesse: le info rilevanti per capire il ragionamento sono tutte nel testo e nei passi.

## Indice degli argomenti

- [Serie numeriche](#serie)
- [Sviluppi di Taylor](#taylor)
- [Lagrange (multivariabile)](#lagrange)
- [Punti stazionari liberi](#punti_liberi)
- [EDO 2° ordine / Cauchy](#edo)
- [EDO 1° ordine / Cauchy](#edo1)
- [Integrali doppi](#integrali)
- [Continuità e differenziabilità](#continuita)

---

## Serie numeriche  <a id="serie"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di 1/n^(3)

$$\sum_{n=1}^{\infty} \frac{1}{n^{3}}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{1}{n^{3}}$$
- Passo 1 — riconosciamo la forma: è una serie armonica generalizzata.  
  $$\sum \frac{1}{n^p}$$
- Passo 2 — criterio: la serie p converge se e solo se p>1, diverge se p≤1.
- Passo 3 — qui p = 3, quindi:  
  $$p>1$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 2
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di 1/n^(2)

$$\sum_{n=1}^{\infty} \frac{1}{n^{2}}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{1}{n^{2}}$$
- Passo 1 — riconosciamo la forma: è una serie armonica generalizzata.  
  $$\sum \frac{1}{n^p}$$
- Passo 2 — criterio: la serie p converge se e solo se p>1, diverge se p≤1.
- Passo 3 — qui p = 2, quindi:  
  $$p>1$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 3
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (-1)^n / n^(2)

$$\sum_{n=1}^{\infty} \frac{\left(-1\right)^{n}}{n^{2}}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{\left(-1\right)^{n}}{n^{2}}$$
- Passo 1 — la serie è alternata (compare (-1)^n); isoliamo il valore assoluto:  
  $$|a_n| = \frac{1}{n^{2}}$$
- Verifichiamo le due ipotesi del criterio di Leibniz: |a_n| è DECRESCENTE (perché n^p, con p>0, è crescente in n, quindi 1/n^p è decrescente) ed è INFINITESIMA (perché 1/n^p → 0 per n→∞).  
  $$|a_{n+1}|<|a_n|,\qquad \lim_{n\to\infty}|a_n|=0$$
- Passo 2 — essendo entrambe le ipotesi verificate, per il criterio di Leibniz la serie converge (almeno condizionatamente).
- Passo 3 — verifichiamo la convergenza assoluta studiando la serie p:  
  $$\sum \frac{1}{n^{2}}$$
- Passo 4 — qui p = 2:  
  $$p>1 \Rightarrow \text{converge ANCHE assolutamente}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 4
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (-1)^n / n^(1)

$$\sum_{n=1}^{\infty} \frac{\left(-1\right)^{n}}{n}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{\left(-1\right)^{n}}{n}$$
- Passo 1 — la serie è alternata (compare (-1)^n); isoliamo il valore assoluto:  
  $$|a_n| = \frac{1}{n^{1}}$$
- Verifichiamo le due ipotesi del criterio di Leibniz: |a_n| è DECRESCENTE (perché n^p, con p>0, è crescente in n, quindi 1/n^p è decrescente) ed è INFINITESIMA (perché 1/n^p → 0 per n→∞).  
  $$|a_{n+1}|<|a_n|,\qquad \lim_{n\to\infty}|a_n|=0$$
- Passo 2 — essendo entrambe le ipotesi verificate, per il criterio di Leibniz la serie converge (almeno condizionatamente).
- Passo 3 — verifichiamo la convergenza assoluta studiando la serie p:  
  $$\sum \frac{1}{n^{1}}$$
- Passo 4 — qui p = 1:  
  $$p\le 1 \Rightarrow \text{SOLO condizionatamente convergente}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 5
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di 1/n^(1)

$$\sum_{n=1}^{\infty} \frac{1}{n}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{1}{n}$$
- Passo 1 — riconosciamo la forma: è una serie armonica generalizzata.  
  $$\sum \frac{1}{n^p}$$
- Passo 2 — criterio: la serie p converge se e solo se p>1, diverge se p≤1.
- Passo 3 — qui p = 1, quindi:  
  $$p\le 1$$
- Conclusione: la serie  
  $$\textbf{DIVERGE}$$

**Risposta corretta:** **diverge**


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (-1)^n / n^(1/2)

$$\sum_{n=1}^{\infty} \frac{\left(-1\right)^{n}}{\sqrt{n}}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{\left(-1\right)^{n}}{\sqrt{n}}$$
- Passo 1 — la serie è alternata (compare (-1)^n); isoliamo il valore assoluto:  
  $$|a_n| = \frac{1}{n^{\frac{1}{2}}}$$
- Verifichiamo le due ipotesi del criterio di Leibniz: |a_n| è DECRESCENTE (perché n^p, con p>0, è crescente in n, quindi 1/n^p è decrescente) ed è INFINITESIMA (perché 1/n^p → 0 per n→∞).  
  $$|a_{n+1}|<|a_n|,\qquad \lim_{n\to\infty}|a_n|=0$$
- Passo 2 — essendo entrambe le ipotesi verificate, per il criterio di Leibniz la serie converge (almeno condizionatamente).
- Passo 3 — verifichiamo la convergenza assoluta studiando la serie p:  
  $$\sum \frac{1}{n^{\frac{1}{2}}}$$
- Passo 4 — qui p = 1/2:  
  $$p\le 1 \Rightarrow \text{SOLO condizionatamente convergente}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 2
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (1/2)^n * n^(3)

$$\sum_{n=1}^{\infty} 2^{- n} n^{3}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = 2^{- n} n^{3}$$
- Passo 1 — applichiamo il criterio del rapporto:  
  $$L=\lim_{n\to\infty}\frac{a_{n+1}}{a_n}$$
- Passo 2 — calcoliamo il rapporto e il limite:  
  $$\frac{a_{n+1}}{a_n}=\frac{\left(n + 1\right)^{3}}{2 n^{3}}\ \Rightarrow\ L=\frac{1}{2}$$
- Passo 3 — il fattore polinomiale n^3 non influisce sul limite: L coincide con la ragione r = 1/2.
- Passo 4 — conclusione del criterio del rapporto:  
  $$L<1 \Rightarrow \text{CONVERGE}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 3
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di 1/n^(3)

$$\sum_{n=1}^{\infty} \frac{1}{n^{3}}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{1}{n^{3}}$$
- Passo 1 — riconosciamo la forma: è una serie armonica generalizzata.  
  $$\sum \frac{1}{n^p}$$
- Passo 2 — criterio: la serie p converge se e solo se p>1, diverge se p≤1.
- Passo 3 — qui p = 3, quindi:  
  $$p>1$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 4
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (2)^n * n^(2)

$$\sum_{n=1}^{\infty} 2^{n} n^{2}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = 2^{n} n^{2}$$
- Passo 1 — applichiamo il criterio del rapporto:  
  $$L=\lim_{n\to\infty}\frac{a_{n+1}}{a_n}$$
- Passo 2 — calcoliamo il rapporto e il limite:  
  $$\frac{a_{n+1}}{a_n}=\frac{2 \left(n + 1\right)^{2}}{n^{2}}\ \Rightarrow\ L=2$$
- Passo 3 — il fattore polinomiale n^2 non influisce sul limite: L coincide con la ragione r = 2.
- Passo 4 — conclusione del criterio del rapporto:  
  $$L>1 \Rightarrow \text{DIVERGE}$$
- Conclusione: la serie  
  $$\textbf{DIVERGE}$$

**Risposta corretta:** **diverge**

#### Esercizio 5
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (2/3)^n * n^(2)

$$\sum_{n=1}^{\infty} \left(\frac{2}{3}\right)^{n} n^{2}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \left(\frac{2}{3}\right)^{n} n^{2}$$
- Passo 1 — applichiamo il criterio del rapporto:  
  $$L=\lim_{n\to\infty}\frac{a_{n+1}}{a_n}$$
- Passo 2 — calcoliamo il rapporto e il limite:  
  $$\frac{a_{n+1}}{a_n}=\frac{2 \left(n + 1\right)^{2}}{3 n^{2}}\ \Rightarrow\ L=\frac{2}{3}$$
- Passo 3 — il fattore polinomiale n^2 non influisce sul limite: L coincide con la ragione r = 2/3.
- Passo 4 — conclusione del criterio del rapporto:  
  $$L<1 \Rightarrow \text{CONVERGE}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (4/5)^n * n^(4)

$$\sum_{n=1}^{\infty} \left(\frac{4}{5}\right)^{n} n^{4}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \left(\frac{4}{5}\right)^{n} n^{4}$$
- Passo 1 — applichiamo il criterio del rapporto:  
  $$L=\lim_{n\to\infty}\frac{a_{n+1}}{a_n}$$
- Passo 2 — calcoliamo il rapporto e il limite:  
  $$\frac{a_{n+1}}{a_n}=\frac{4 \left(n + 1\right)^{4}}{5 n^{4}}\ \Rightarrow\ L=\frac{4}{5}$$
- Passo 3 — il fattore polinomiale n^4 non influisce sul limite: L coincide con la ragione r = 4/5.
- Passo 4 — conclusione del criterio del rapporto:  
  $$L<1 \Rightarrow \text{CONVERGE}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 2
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (3n+1)/(n^2+9)

$$\sum_{n=1}^{\infty} \frac{3 n + 1}{n^{2} + 9}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{3 n + 1}{n^{2} + 9}$$
- Passo 1 — per n grande confrontiamo con la serie armonica:  
  $$b_n=\frac1n$$
- Passo 2 — calcoliamo il limite del rapporto a_n/b_n:  
  $$L=\lim_{n\to\infty}\frac{a_n}{b_n}=3$$
- Passo 3 — poiché 0<L<∞, per il criterio del confronto asintotico le due serie hanno lo stesso comportamento.
- Passo 4 — la serie armonica diverge, quindi anche la serie data diverge:  
  $$\sum \frac1n \to \infty$$
- Conclusione: la serie  
  $$\textbf{DIVERGE}$$

**Risposta corretta:** **diverge**

#### Esercizio 3
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (-1)^n / n^(3/2)

$$\sum_{n=1}^{\infty} \frac{\left(-1\right)^{n}}{n^{\frac{3}{2}}}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{\left(-1\right)^{n}}{n^{\frac{3}{2}}}$$
- Passo 1 — la serie è alternata (compare (-1)^n); isoliamo il valore assoluto:  
  $$|a_n| = \frac{1}{n^{\frac{3}{2}}}$$
- Verifichiamo le due ipotesi del criterio di Leibniz: |a_n| è DECRESCENTE (perché n^p, con p>0, è crescente in n, quindi 1/n^p è decrescente) ed è INFINITESIMA (perché 1/n^p → 0 per n→∞).  
  $$|a_{n+1}|<|a_n|,\qquad \lim_{n\to\infty}|a_n|=0$$
- Passo 2 — essendo entrambe le ipotesi verificate, per il criterio di Leibniz la serie converge (almeno condizionatamente).
- Passo 3 — verifichiamo la convergenza assoluta studiando la serie p:  
  $$\sum \frac{1}{n^{\frac{3}{2}}}$$
- Passo 4 — qui p = 3/2:  
  $$p>1 \Rightarrow \text{converge ANCHE assolutamente}$$
- Conclusione: la serie  
  $$\textbf{CONVERGE}$$

**Risposta corretta:** **converge**

#### Esercizio 4
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (3n+1)/(n^2+5)

$$\sum_{n=1}^{\infty} \frac{3 n + 1}{n^{2} + 5}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{3 n + 1}{n^{2} + 5}$$
- Passo 1 — per n grande confrontiamo con la serie armonica:  
  $$b_n=\frac1n$$
- Passo 2 — calcoliamo il limite del rapporto a_n/b_n:  
  $$L=\lim_{n\to\infty}\frac{a_n}{b_n}=3$$
- Passo 3 — poiché 0<L<∞, per il criterio del confronto asintotico le due serie hanno lo stesso comportamento.
- Passo 4 — la serie armonica diverge, quindi anche la serie data diverge:  
  $$\sum \frac1n \to \infty$$
- Conclusione: la serie  
  $$\textbf{DIVERGE}$$

**Risposta corretta:** **diverge**

#### Esercizio 5
**Testo:** Studiare il carattere della serie:  Somma per n=1..infinito di (2n+1)/(n^2+11)

$$\sum_{n=1}^{\infty} \frac{2 n + 1}{n^{2} + 11}$$

**Formato risposta richiesto:** Scrivi: converge   oppure   diverge

**Svolgimento passo-passo:**

- Termine generale:  
  $$a_n = \frac{2 n + 1}{n^{2} + 11}$$
- Passo 1 — per n grande confrontiamo con la serie armonica:  
  $$b_n=\frac1n$$
- Passo 2 — calcoliamo il limite del rapporto a_n/b_n:  
  $$L=\lim_{n\to\infty}\frac{a_n}{b_n}=2$$
- Passo 3 — poiché 0<L<∞, per il criterio del confronto asintotico le due serie hanno lo stesso comportamento.
- Passo 4 — la serie armonica diverge, quindi anche la serie data diverge:  
  $$\sum \frac1n \to \infty$$
- Conclusione: la serie  
  $$\textbf{DIVERGE}$$

**Risposta corretta:** **diverge**


### Temi d'esame (problemi reali) (3 esercizi)

#### Esercizio 1
**Testo:** [22 ottobre 2025, Esercizio 3] Data la serie Σ (n≥2) 2/(4n²+8n+3), verificare che si tratta di una serie telescopica e calcolarne la somma.

$$\sum_{n\ge2}\frac{2}{4n^2+8n+3}$$

*Fonte: 22 ottobre 2025*

**Formato risposta richiesto:** Scrivi il valore della somma (numerico o simbolico), es: 1/5.

**Svolgimento passo-passo:**

- Serie:  
  $$\sum_{n\ge2}\frac{2}{4n^2+8n+3}$$
- Passo 1 — fattorizziamo il denominatore:  
  $$4n^2+8n+3 = \left(2 n + 1\right) \left(2 n + 3\right)$$
- Passo 2 — scomponiamo in fratti semplici: si ottiene la forma tipica 1/(2n+1) - 1/(2n+3), cioè una serie TELESCOPICA (i cui termini si elidono a coppie):  
  $$\frac{2}{(2n+1)(2n+3)} = - \frac{1}{2 n + 3} + \frac{1}{2 n + 1}$$
- Passo 3 — la somma parziale N-esima si 'accorcia': tutti i termini centrali si cancellano a due a due, restano solo il primo e l'ultimo:  
  $$\sum_{n=2}^{N}\left(\frac{1}{2n+1}-\frac{1}{2n+3}\right) = \frac15-\frac{1}{2N+3}$$
- Passo 4 — per N→∞ il secondo termine tende a 0, quindi la serie converge:  
  $$\text{somma} = \frac{1}{5}$$

**Risposta corretta:** **1/5**

#### Esercizio 2
**Testo:** [25 ottobre 2025, Esercizio 3] Data la serie Σ (n≥2) 2^(1-2n)/3^(n-2), dopo averla ricondotta a una serie geometrica, studiarne la convergenza e calcolarne la somma.

$$\sum_{n\ge2}\frac{2^{1-2n}}{3^{n-2}}$$

*Fonte: 25 ottobre 2025*

**Formato risposta richiesto:** Scrivi il valore della somma (numerico o simbolico), es: 1/5.

**Svolgimento passo-passo:**

- Serie:  
  $$\sum_{n\ge2}\frac{2^{1-2n}}{3^{n-2}}$$
- Passo 1 — separiamo le potenze in base n raccogliendo le costanti:  
  $$\frac{2^{1-2n}}{3^{n-2}} = 2\cdot3^2\cdot\left(\frac14\right)^n\left(\frac13\right)^n = 18 \cdot 12^{- n}$$
- Passo 2 — è una serie geometrica di ragione q=1/12:  
  $$q = \frac{1}{12},\ \ |q|<1 \Rightarrow \textbf{CONVERGE}$$
- Passo 3 — il primo termine (per n=2, dove parte la sommatoria) vale:  
  $$a_2 = \frac{1}{8}$$
- Passo 4 — somma di una serie geometrica: (primo termine)/(1-ragione):  
  $$\text{somma} = \frac{\frac{1}{8}}{1-\frac{1}{12}} = \frac{3}{22}$$

**Risposta corretta:** **3/22**

#### Esercizio 3
**Testo:** [29 ottobre 2025, Esercizio 3] Data la serie Σ (n≥1) [(1-x+x²)/(x+1)]^n, determinare per quali valori reali di x la serie diverge. (Per la verifica automatica qui sotto: indica se per x=1 la serie CONVERGE o DIVERGE — la discussione completa per ogni x è nei passaggi della soluzione.)

$$\sum_{n\ge1}\left(\frac{1-x+x^2}{x+1}\right)^n$$

*Fonte: 29 ottobre 2025*

**Formato risposta richiesto:** Scrivi 'converge' o 'diverge' (riferito al caso x=1).

**Svolgimento passo-passo:**

- Serie:  
  $$\sum_{n\ge1}\left(\frac{1-x+x^2}{x+1}\right)^n$$
- Passo 1 — è una serie geometrica di ragione q(x) = (1-x+x²)/(x+1), definita per x≠-1 (il numeratore x²-x+1 ha discriminante negativo, quindi è sempre positivo).
- Passo 2 — una serie geometrica converge se e solo se |q|<1, e diverge se |q|≥1 (anche nel caso limite q=±1, dove il termine generale non tende a 0).
- Passo 3 — per x>-1 si ha q>0 (stesso segno del numeratore): risolviamo q≥1:  
  $$\frac{x^2-x+1}{x+1}\ge1 \iff x^2-2x\ge0 \iff x\le0 \text{ oppure } x\ge2$$
- Passo 4 — per x<-1 si ha q<0 (denominatore negativo): risolviamo q≤-1; l'algebra si riduce a x²+2≥0, SEMPRE vera. Quindi per ogni x<-1 la serie diverge sempre.  
  $$\frac{x^2-x+1}{x+1}\le-1 \iff x^2+2\ge0\ \ (\text{sempre vero})$$
- Conclusione — la serie converge SOLO per 0<x<2 (dove |q|<1); diverge per ogni altro x reale (con x≠-1, dove non è definita):  
  $$\textbf{diverge per } x\in(-\infty,0]\cup[2,+\infty),\ x\ne-1$$
- Verifica per x=1 (nell'intervallo di convergenza 0<x<2): q(1)=\frac{1}{2}, |q|<1 → CONVERGE.

**Risposta corretta:** **converge**

---

## Sviluppi di Taylor  <a id="taylor"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = exp(x) centrato in x0=0, fino all'ordine 3 incluso (con resto di Peano).

$$f(x) = e^{x},\quad x_0 = 0,\quad \text{ordine } 3$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=e^{x}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=e^{x}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=e^{x}\ \Rightarrow\ f^{(2)}(0)=1$$
- k = 3:  
  $$f^{(3)}(x)=e^{x}\ \Rightarrow\ f^{(3)}(0)=1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$1/2! = \frac{1}{2}\ \Rightarrow\ \frac{1}{2}x^{2}$$
- k = 3:  
  $$1/3! = \frac{1}{6}\ \Rightarrow\ \frac{1}{6}x^{3}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{3}(x) = \frac{x^{3}}{6} + \frac{x^{2}}{2} + x + 1 + o(x^{3})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = cos(x) centrato in x0=0, fino all'ordine 2 incluso (con resto di Peano).

$$f(x) = \cos{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 2$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=0$$
- k = 2:  
  $$f^{(2)}(x)=- \cos{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=-1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$0/1! = 0\ \Rightarrow\ 0x^{1}$$
- k = 2:  
  $$-1/2! = - \frac{1}{2}\ \Rightarrow\ - \frac{1}{2}x^{2}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{2}(x) = 1 - \frac{x^{2}}{2} + o(x^{2})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = sin(x) centrato in x0=0, fino all'ordine 3 incluso (con resto di Peano).

$$f(x) = \sin{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 3$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=0$$
- k = 1:  
  $$f^{(1)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=0$$
- k = 3:  
  $$f^{(3)}(x)=- \cos{\left(x \right)}\ \Rightarrow\ f^{(3)}(0)=-1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$0/0! = 0\ \Rightarrow\ 0$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$0/2! = 0\ \Rightarrow\ 0x^{2}$$
- k = 3:  
  $$-1/3! = - \frac{1}{6}\ \Rightarrow\ - \frac{1}{6}x^{3}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{3}(x) = - \frac{x^{3}}{6} + x + o(x^{3})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = exp(x) centrato in x0=0, fino all'ordine 2 incluso (con resto di Peano).

$$f(x) = e^{x},\quad x_0 = 0,\quad \text{ordine } 2$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=e^{x}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=e^{x}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=e^{x}\ \Rightarrow\ f^{(2)}(0)=1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$1/2! = \frac{1}{2}\ \Rightarrow\ \frac{1}{2}x^{2}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{2}(x) = \frac{x^{2}}{2} + x + 1 + o(x^{2})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = sin(x) centrato in x0=0, fino all'ordine 2 incluso (con resto di Peano).

$$f(x) = \sin{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 2$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=0$$
- k = 1:  
  $$f^{(1)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=0$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$0/0! = 0\ \Rightarrow\ 0$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$0/2! = 0\ \Rightarrow\ 0x^{2}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{2}(x) = x + o(x^{2})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = cos(x) centrato in x0=0, fino all'ordine 2 incluso (con resto di Peano).

$$f(x) = \cos{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 2$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=0$$
- k = 2:  
  $$f^{(2)}(x)=- \cos{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=-1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$0/1! = 0\ \Rightarrow\ 0x^{1}$$
- k = 2:  
  $$-1/2! = - \frac{1}{2}\ \Rightarrow\ - \frac{1}{2}x^{2}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{2}(x) = 1 - \frac{x^{2}}{2} + o(x^{2})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = sqrt(x + 1) centrato in x0=0, fino all'ordine 3 incluso (con resto di Peano).

$$f(x) = \sqrt{x + 1},\quad x_0 = 0,\quad \text{ordine } 3$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\sqrt{x + 1}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=\frac{1}{2 \sqrt{x + 1}}\ \Rightarrow\ f^{(1)}(0)=\frac{1}{2}$$
- k = 2:  
  $$f^{(2)}(x)=- \frac{1}{4 \left(x + 1\right)^{\frac{3}{2}}}\ \Rightarrow\ f^{(2)}(0)=- \frac{1}{4}$$
- k = 3:  
  $$f^{(3)}(x)=\frac{3}{8 \left(x + 1\right)^{\frac{5}{2}}}\ \Rightarrow\ f^{(3)}(0)=\frac{3}{8}$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$\frac{1}{2}/1! = \frac{1}{2}\ \Rightarrow\ \frac{1}{2}x^{1}$$
- k = 2:  
  $$- \frac{1}{4}/2! = - \frac{1}{8}\ \Rightarrow\ - \frac{1}{8}x^{2}$$
- k = 3:  
  $$\frac{3}{8}/3! = \frac{1}{16}\ \Rightarrow\ \frac{1}{16}x^{3}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{3}(x) = \frac{x^{3}}{16} - \frac{x^{2}}{8} + \frac{x}{2} + 1 + o(x^{3})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = exp(x) centrato in x0=0, fino all'ordine 2 incluso (con resto di Peano).

$$f(x) = e^{x},\quad x_0 = 0,\quad \text{ordine } 2$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=e^{x}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=e^{x}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=e^{x}\ \Rightarrow\ f^{(2)}(0)=1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$1/2! = \frac{1}{2}\ \Rightarrow\ \frac{1}{2}x^{2}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{2}(x) = \frac{x^{2}}{2} + x + 1 + o(x^{2})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = 1/(1 - x) centrato in x0=0, fino all'ordine 3 incluso (con resto di Peano).

$$f(x) = \frac{1}{1 - x},\quad x_0 = 0,\quad \text{ordine } 3$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\frac{1}{1 - x}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=\frac{1}{\left(1 - x\right)^{2}}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=- \frac{2}{\left(x - 1\right)^{3}}\ \Rightarrow\ f^{(2)}(0)=2$$
- k = 3:  
  $$f^{(3)}(x)=\frac{6}{\left(x - 1\right)^{4}}\ \Rightarrow\ f^{(3)}(0)=6$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$2/2! = 1\ \Rightarrow\ 1x^{2}$$
- k = 3:  
  $$6/3! = 1\ \Rightarrow\ 1x^{3}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{3}(x) = x^{3} + x^{2} + x + 1 + o(x^{3})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = cos(x) centrato in x0=0, fino all'ordine 3 incluso (con resto di Peano).

$$f(x) = \cos{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 3$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=0$$
- k = 2:  
  $$f^{(2)}(x)=- \cos{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=-1$$
- k = 3:  
  $$f^{(3)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(3)}(0)=0$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$0/1! = 0\ \Rightarrow\ 0x^{1}$$
- k = 2:  
  $$-1/2! = - \frac{1}{2}\ \Rightarrow\ - \frac{1}{2}x^{2}$$
- k = 3:  
  $$0/3! = 0\ \Rightarrow\ 0x^{3}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{3}(x) = 1 - \frac{x^{2}}{2} + o(x^{3})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = sin(x) centrato in x0=0, fino all'ordine 5 incluso (con resto di Peano).

$$f(x) = \sin{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 5$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=0$$
- k = 1:  
  $$f^{(1)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=0$$
- k = 3:  
  $$f^{(3)}(x)=- \cos{\left(x \right)}\ \Rightarrow\ f^{(3)}(0)=-1$$
- k = 4:  
  $$f^{(4)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(4)}(0)=0$$
- k = 5:  
  $$f^{(5)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(5)}(0)=1$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$0/0! = 0\ \Rightarrow\ 0$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$0/2! = 0\ \Rightarrow\ 0x^{2}$$
- k = 3:  
  $$-1/3! = - \frac{1}{6}\ \Rightarrow\ - \frac{1}{6}x^{3}$$
- k = 4:  
  $$0/4! = 0\ \Rightarrow\ 0x^{4}$$
- k = 5:  
  $$1/5! = \frac{1}{120}\ \Rightarrow\ \frac{1}{120}x^{5}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{5}(x) = \frac{x^{5}}{120} - \frac{x^{3}}{6} + x + o(x^{5})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = exp(x) centrato in x0=-1, fino all'ordine 4 incluso (con resto di Peano).

$$f(x) = e^{x},\quad x_0 = -1,\quad \text{ordine } 4$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=e^{x}\ \Rightarrow\ f^{(0)}(-1)=e^{-1}$$
- k = 1:  
  $$f^{(1)}(x)=e^{x}\ \Rightarrow\ f^{(1)}(-1)=e^{-1}$$
- k = 2:  
  $$f^{(2)}(x)=e^{x}\ \Rightarrow\ f^{(2)}(-1)=e^{-1}$$
- k = 3:  
  $$f^{(3)}(x)=e^{x}\ \Rightarrow\ f^{(3)}(-1)=e^{-1}$$
- k = 4:  
  $$f^{(4)}(x)=e^{x}\ \Rightarrow\ f^{(4)}(-1)=e^{-1}$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$e^{-1}/0! = e^{-1}\ \Rightarrow\ e^{-1}$$
- k = 1:  
  $$e^{-1}/1! = e^{-1}\ \Rightarrow\ e^{-1}(x--1)^{1}$$
- k = 2:  
  $$e^{-1}/2! = \frac{1}{2 e}\ \Rightarrow\ \frac{1}{2 e}(x--1)^{2}$$
- k = 3:  
  $$e^{-1}/3! = \frac{1}{6 e}\ \Rightarrow\ \frac{1}{6 e}(x--1)^{3}$$
- k = 4:  
  $$e^{-1}/4! = \frac{1}{24 e}\ \Rightarrow\ \frac{1}{24 e}(x--1)^{4}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{4}(x) = \frac{x^{4}}{24 e} + \frac{x^{3}}{3 e} + \frac{5 x^{2}}{4 e} + \frac{8 x}{3 e} + \frac{65}{24 e} + o((x--1)^{4})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = sin(x) centrato in x0=0, fino all'ordine 4 incluso (con resto di Peano).

$$f(x) = \sin{\left(x \right)},\quad x_0 = 0,\quad \text{ordine } 4$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(0)}(0)=0$$
- k = 1:  
  $$f^{(1)}(x)=\cos{\left(x \right)}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=- \sin{\left(x \right)}\ \Rightarrow\ f^{(2)}(0)=0$$
- k = 3:  
  $$f^{(3)}(x)=- \cos{\left(x \right)}\ \Rightarrow\ f^{(3)}(0)=-1$$
- k = 4:  
  $$f^{(4)}(x)=\sin{\left(x \right)}\ \Rightarrow\ f^{(4)}(0)=0$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$0/0! = 0\ \Rightarrow\ 0$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$0/2! = 0\ \Rightarrow\ 0x^{2}$$
- k = 3:  
  $$-1/3! = - \frac{1}{6}\ \Rightarrow\ - \frac{1}{6}x^{3}$$
- k = 4:  
  $$0/4! = 0\ \Rightarrow\ 0x^{4}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{4}(x) = - \frac{x^{3}}{6} + x + o(x^{4})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = log(x + 1) centrato in x0=0, fino all'ordine 4 incluso (con resto di Peano).

$$f(x) = \log{\left(x + 1 \right)},\quad x_0 = 0,\quad \text{ordine } 4$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\log{\left(x + 1 \right)}\ \Rightarrow\ f^{(0)}(0)=0$$
- k = 1:  
  $$f^{(1)}(x)=\frac{1}{x + 1}\ \Rightarrow\ f^{(1)}(0)=1$$
- k = 2:  
  $$f^{(2)}(x)=- \frac{1}{\left(x + 1\right)^{2}}\ \Rightarrow\ f^{(2)}(0)=-1$$
- k = 3:  
  $$f^{(3)}(x)=\frac{2}{\left(x + 1\right)^{3}}\ \Rightarrow\ f^{(3)}(0)=2$$
- k = 4:  
  $$f^{(4)}(x)=- \frac{6}{\left(x + 1\right)^{4}}\ \Rightarrow\ f^{(4)}(0)=-6$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$0/0! = 0\ \Rightarrow\ 0$$
- k = 1:  
  $$1/1! = 1\ \Rightarrow\ 1x^{1}$$
- k = 2:  
  $$-1/2! = - \frac{1}{2}\ \Rightarrow\ - \frac{1}{2}x^{2}$$
- k = 3:  
  $$2/3! = \frac{1}{3}\ \Rightarrow\ \frac{1}{3}x^{3}$$
- k = 4:  
  $$-6/4! = - \frac{1}{4}\ \Rightarrow\ - \frac{1}{4}x^{4}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{4}(x) = - \frac{x^{4}}{4} + \frac{x^{3}}{3} - \frac{x^{2}}{2} + x + o(x^{4})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Scrivere lo sviluppo di Taylor di f(x) = sqrt(x + 1) centrato in x0=0, fino all'ordine 4 incluso (con resto di Peano).

$$f(x) = \sqrt{x + 1},\quad x_0 = 0,\quad \text{ordine } 4$$

**Formato risposta richiesto:** Scrivi il polinomio in sintassi Python, es:  1 + x + x**2/2

**Svolgimento passo-passo:**

- Formula generale:  
  $$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k+o((x-x_0)^n)$$
- Passo 1 — calcolo le derivate successive e le valuto in x0:
- k = 0:  
  $$f^{(0)}(x)=\sqrt{x + 1}\ \Rightarrow\ f^{(0)}(0)=1$$
- k = 1:  
  $$f^{(1)}(x)=\frac{1}{2 \sqrt{x + 1}}\ \Rightarrow\ f^{(1)}(0)=\frac{1}{2}$$
- k = 2:  
  $$f^{(2)}(x)=- \frac{1}{4 \left(x + 1\right)^{\frac{3}{2}}}\ \Rightarrow\ f^{(2)}(0)=- \frac{1}{4}$$
- k = 3:  
  $$f^{(3)}(x)=\frac{3}{8 \left(x + 1\right)^{\frac{5}{2}}}\ \Rightarrow\ f^{(3)}(0)=\frac{3}{8}$$
- k = 4:  
  $$f^{(4)}(x)=- \frac{15}{16 \left(x + 1\right)^{\frac{7}{2}}}\ \Rightarrow\ f^{(4)}(0)=- \frac{15}{16}$$
- Passo 2 — costruisco ogni termine f^(k)(x0)/k! · (x−x0)^k:
- k = 0:  
  $$1/0! = 1\ \Rightarrow\ 1$$
- k = 1:  
  $$\frac{1}{2}/1! = \frac{1}{2}\ \Rightarrow\ \frac{1}{2}x^{1}$$
- k = 2:  
  $$- \frac{1}{4}/2! = - \frac{1}{8}\ \Rightarrow\ - \frac{1}{8}x^{2}$$
- k = 3:  
  $$\frac{3}{8}/3! = \frac{1}{16}\ \Rightarrow\ \frac{1}{16}x^{3}$$
- k = 4:  
  $$- \frac{15}{16}/4! = - \frac{5}{128}\ \Rightarrow\ - \frac{5}{128}x^{4}$$
- Passo 3 — sommando tutti i termini, il polinomio di Taylor è:  
  $$P_{4}(x) = - \frac{5 x^{4}}{128} + \frac{x^{3}}{16} - \frac{x^{2}}{8} + \frac{x}{2} + 1 + o(x^{4})$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

---

## Lagrange (multivariabile)  <a id="lagrange"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 3*x**2 + y**2 vincolati a x^2 + y^2 = 1, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 3 x^{2} + y^{2},\quad x^2 + y^2 = 1$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=3 x^{2} + y^{2},\quad g(x,y)=x^{2} + y^{2} - 1=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$6 x=\lambda(2 x)\quad,\quad 2 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 1=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$8 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(0,-1),\ \lambda=1:\quad \nabla f=(0,-2)\ =\ \lambda\nabla g=(0,-2)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(0,1),\ \lambda=1:\quad \nabla f=(0,2)\ =\ \lambda\nabla g=(0,2)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(-1,0),\ \lambda=3:\quad \nabla f=(-6,0)\ =\ \lambda\nabla g=(-6,0)\ \Rightarrow\ f=3$$
-   
  $$(x,y)=(1,0),\ \lambda=3:\quad \nabla f=(6,0)\ =\ \lambda\nabla g=(6,0)\ \Rightarrow\ f=3$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(0,-1),\ \lambda=1:\quad \det\overline{H}=-16\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,1),\ \lambda=1:\quad \det\overline{H}=-16\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(-1,0),\ \lambda=3:\quad \det\overline{H}=16\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(1,0),\ \lambda=3:\quad \det\overline{H}=16\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=3,\quad \min f=1$$

**Risposta corretta:** punti e valori: (0, -1) → 1; (0, 1) → 1; (-1, 0) → 3; (1, 0) → 3 (valore massimo = 3, valore minimo = 1)

#### Esercizio 2
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + y**2 vincolati a x^2 + y^2 = 1, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + y^{2},\quad x^2 + y^2 = 1$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + y^{2},\quad g(x,y)=x^{2} + y^{2} - 1=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(2 x)\quad,\quad 2 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 1=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$4 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(0,-1),\ \lambda=1:\quad \nabla f=(0,-2)\ =\ \lambda\nabla g=(0,-2)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(0,1),\ \lambda=1:\quad \nabla f=(0,2)\ =\ \lambda\nabla g=(0,2)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(-1,0),\ \lambda=2:\quad \nabla f=(-4,0)\ =\ \lambda\nabla g=(-4,0)\ \Rightarrow\ f=2$$
-   
  $$(x,y)=(1,0),\ \lambda=2:\quad \nabla f=(4,0)\ =\ \lambda\nabla g=(4,0)\ \Rightarrow\ f=2$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(0,-1),\ \lambda=1:\quad \det\overline{H}=-8\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,1),\ \lambda=1:\quad \det\overline{H}=-8\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(-1,0),\ \lambda=2:\quad \det\overline{H}=8\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(1,0),\ \lambda=2:\quad \det\overline{H}=8\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=2,\quad \min f=1$$

**Risposta corretta:** punti e valori: (0, -1) → 1; (0, 1) → 1; (-1, 0) → 2; (1, 0) → 2 (valore massimo = 2, valore minimo = 1)

#### Esercizio 3
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = x**2 + 2*y**2 vincolati a x^2 + y^2 = 4, e classificare gli eventuali estremi assoluti.

$$f(x,y) = x^{2} + 2 y^{2},\quad x^2 + y^2 = 4$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=x^{2} + 2 y^{2},\quad g(x,y)=x^{2} + y^{2} - 4=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$2 x=\lambda(2 x)\quad,\quad 4 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 4=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$- 4 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(-2,0),\ \lambda=1:\quad \nabla f=(-4,0)\ =\ \lambda\nabla g=(-4,0)\ \Rightarrow\ f=4$$
-   
  $$(x,y)=(2,0),\ \lambda=1:\quad \nabla f=(4,0)\ =\ \lambda\nabla g=(4,0)\ \Rightarrow\ f=4$$
-   
  $$(x,y)=(0,-2),\ \lambda=2:\quad \nabla f=(0,-8)\ =\ \lambda\nabla g=(0,-8)\ \Rightarrow\ f=8$$
-   
  $$(x,y)=(0,2),\ \lambda=2:\quad \nabla f=(0,8)\ =\ \lambda\nabla g=(0,8)\ \Rightarrow\ f=8$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(-2,0),\ \lambda=1:\quad \det\overline{H}=-32\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(2,0),\ \lambda=1:\quad \det\overline{H}=-32\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,-2),\ \lambda=2:\quad \det\overline{H}=32\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(0,2),\ \lambda=2:\quad \det\overline{H}=32\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=8,\quad \min f=4$$

**Risposta corretta:** punti e valori: (-2, 0) → 4; (2, 0) → 4; (0, -2) → 8; (0, 2) → 8 (valore massimo = 8, valore minimo = 4)

#### Esercizio 4
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = x**2 + 3*y**2 vincolati a x^2 + y^2 = 4, e classificare gli eventuali estremi assoluti.

$$f(x,y) = x^{2} + 3 y^{2},\quad x^2 + y^2 = 4$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=x^{2} + 3 y^{2},\quad g(x,y)=x^{2} + y^{2} - 4=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$2 x=\lambda(2 x)\quad,\quad 6 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 4=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$- 8 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(-2,0),\ \lambda=1:\quad \nabla f=(-4,0)\ =\ \lambda\nabla g=(-4,0)\ \Rightarrow\ f=4$$
-   
  $$(x,y)=(2,0),\ \lambda=1:\quad \nabla f=(4,0)\ =\ \lambda\nabla g=(4,0)\ \Rightarrow\ f=4$$
-   
  $$(x,y)=(0,-2),\ \lambda=3:\quad \nabla f=(0,-12)\ =\ \lambda\nabla g=(0,-12)\ \Rightarrow\ f=12$$
-   
  $$(x,y)=(0,2),\ \lambda=3:\quad \nabla f=(0,12)\ =\ \lambda\nabla g=(0,12)\ \Rightarrow\ f=12$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(-2,0),\ \lambda=1:\quad \det\overline{H}=-64\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(2,0),\ \lambda=1:\quad \det\overline{H}=-64\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,-2),\ \lambda=3:\quad \det\overline{H}=64\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(0,2),\ \lambda=3:\quad \det\overline{H}=64\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=12,\quad \min f=4$$

**Risposta corretta:** punti e valori: (-2, 0) → 4; (2, 0) → 4; (0, -2) → 12; (0, 2) → 12 (valore massimo = 12, valore minimo = 4)

#### Esercizio 5
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = x**2 + 3*y**2 vincolati a x^2 + y^2 = 1, e classificare gli eventuali estremi assoluti.

$$f(x,y) = x^{2} + 3 y^{2},\quad x^2 + y^2 = 1$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=x^{2} + 3 y^{2},\quad g(x,y)=x^{2} + y^{2} - 1=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$2 x=\lambda(2 x)\quad,\quad 6 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 1=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$- 8 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(-1,0),\ \lambda=1:\quad \nabla f=(-2,0)\ =\ \lambda\nabla g=(-2,0)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(1,0),\ \lambda=1:\quad \nabla f=(2,0)\ =\ \lambda\nabla g=(2,0)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(0,-1),\ \lambda=3:\quad \nabla f=(0,-6)\ =\ \lambda\nabla g=(0,-6)\ \Rightarrow\ f=3$$
-   
  $$(x,y)=(0,1),\ \lambda=3:\quad \nabla f=(0,6)\ =\ \lambda\nabla g=(0,6)\ \Rightarrow\ f=3$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(-1,0),\ \lambda=1:\quad \det\overline{H}=-16\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(1,0),\ \lambda=1:\quad \det\overline{H}=-16\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,-1),\ \lambda=3:\quad \det\overline{H}=16\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(0,1),\ \lambda=3:\quad \det\overline{H}=16\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=3,\quad \min f=1$$

**Risposta corretta:** punti e valori: (-1, 0) → 1; (1, 0) → 1; (0, -1) → 3; (0, 1) → 3 (valore massimo = 3, valore minimo = 1)


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + 3*y**2 vincolati a x + y = 2, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + 3 y^{2},\quad x + y = 2$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + 3 y^{2},\quad g(x,y)=x + y - 2=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(1)\quad,\quad 6 y=\lambda(1)\quad,\quad x + y - 2=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$4 x - 6 y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(\frac{6}{5},\frac{4}{5}),\ \lambda=\frac{24}{5}:\quad \nabla f=(\frac{24}{5},\frac{24}{5})\ =\ \lambda\nabla g=(\frac{24}{5},\frac{24}{5})\ \Rightarrow\ f=\frac{24}{5}$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(\frac{6}{5},\frac{4}{5}),\ \lambda=\frac{24}{5}:\quad \det\overline{H}=-10\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
- Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:  
  $$\min f=\frac{24}{5},\quad \max f:\ \text{non esiste}$$

**Risposta corretta:** punti e valori: (1.2, 0.8) → 4.8 (valore minimo = 4.8)

#### Esercizio 2
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + y**2 vincolati a x^2 + y^2 = 1, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + y^{2},\quad x^2 + y^2 = 1$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + y^{2},\quad g(x,y)=x^{2} + y^{2} - 1=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(2 x)\quad,\quad 2 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 1=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$4 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(0,-1),\ \lambda=1:\quad \nabla f=(0,-2)\ =\ \lambda\nabla g=(0,-2)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(0,1),\ \lambda=1:\quad \nabla f=(0,2)\ =\ \lambda\nabla g=(0,2)\ \Rightarrow\ f=1$$
-   
  $$(x,y)=(-1,0),\ \lambda=2:\quad \nabla f=(-4,0)\ =\ \lambda\nabla g=(-4,0)\ \Rightarrow\ f=2$$
-   
  $$(x,y)=(1,0),\ \lambda=2:\quad \nabla f=(4,0)\ =\ \lambda\nabla g=(4,0)\ \Rightarrow\ f=2$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(0,-1),\ \lambda=1:\quad \det\overline{H}=-8\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,1),\ \lambda=1:\quad \det\overline{H}=-8\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(-1,0),\ \lambda=2:\quad \det\overline{H}=8\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(1,0),\ \lambda=2:\quad \det\overline{H}=8\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=2,\quad \min f=1$$

**Risposta corretta:** punti e valori: (0, -1) → 1; (0, 1) → 1; (-1, 0) → 2; (1, 0) → 2 (valore massimo = 2, valore minimo = 1)

#### Esercizio 3
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 3*x**2 + 2*y**2 vincolati a x + y = 4, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 3 x^{2} + 2 y^{2},\quad x + y = 4$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=3 x^{2} + 2 y^{2},\quad g(x,y)=x + y - 4=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$6 x=\lambda(1)\quad,\quad 4 y=\lambda(1)\quad,\quad x + y - 4=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$6 x - 4 y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(\frac{8}{5},\frac{12}{5}),\ \lambda=\frac{48}{5}:\quad \nabla f=(\frac{48}{5},\frac{48}{5})\ =\ \lambda\nabla g=(\frac{48}{5},\frac{48}{5})\ \Rightarrow\ f=\frac{96}{5}$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(\frac{8}{5},\frac{12}{5}),\ \lambda=\frac{48}{5}:\quad \det\overline{H}=-10\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
- Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:  
  $$\min f=\frac{96}{5},\quad \max f:\ \text{non esiste}$$

**Risposta corretta:** punti e valori: (1.6, 2.4) → 19.2 (valore minimo = 19.2)

#### Esercizio 4
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + 2*y**2 vincolati a x + y = 1, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + 2 y^{2},\quad x + y = 1$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + 2 y^{2},\quad g(x,y)=x + y - 1=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(1)\quad,\quad 4 y=\lambda(1)\quad,\quad x + y - 1=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$4 x - 4 y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(\frac{1}{2},\frac{1}{2}),\ \lambda=2:\quad \nabla f=(2,2)\ =\ \lambda\nabla g=(2,2)\ \Rightarrow\ f=1$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(\frac{1}{2},\frac{1}{2}),\ \lambda=2:\quad \det\overline{H}=-8\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
- Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:  
  $$\min f=1,\quad \max f:\ \text{non esiste}$$

**Risposta corretta:** punti e valori: (0.5, 0.5) → 1 (valore minimo = 1)

#### Esercizio 5
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + 3*y**2 vincolati a x + y = 3, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + 3 y^{2},\quad x + y = 3$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + 3 y^{2},\quad g(x,y)=x + y - 3=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(1)\quad,\quad 6 y=\lambda(1)\quad,\quad x + y - 3=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$4 x - 6 y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(\frac{9}{5},\frac{6}{5}),\ \lambda=\frac{36}{5}:\quad \nabla f=(\frac{36}{5},\frac{36}{5})\ =\ \lambda\nabla g=(\frac{36}{5},\frac{36}{5})\ \Rightarrow\ f=\frac{54}{5}$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(\frac{9}{5},\frac{6}{5}),\ \lambda=\frac{36}{5}:\quad \det\overline{H}=-10\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
- Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:  
  $$\min f=\frac{54}{5},\quad \max f:\ \text{non esiste}$$

**Risposta corretta:** punti e valori: (1.8, 1.2) → 10.8 (valore minimo = 10.8)


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + 5*y**2 vincolati a x^2 + y^2 = 9, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + 5 y^{2},\quad x^2 + y^2 = 9$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + 5 y^{2},\quad g(x,y)=x^{2} + y^{2} - 9=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(2 x)\quad,\quad 10 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 9=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$- 12 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(-3,0),\ \lambda=2:\quad \nabla f=(-12,0)\ =\ \lambda\nabla g=(-12,0)\ \Rightarrow\ f=18$$
-   
  $$(x,y)=(3,0),\ \lambda=2:\quad \nabla f=(12,0)\ =\ \lambda\nabla g=(12,0)\ \Rightarrow\ f=18$$
-   
  $$(x,y)=(0,-3),\ \lambda=5:\quad \nabla f=(0,-30)\ =\ \lambda\nabla g=(0,-30)\ \Rightarrow\ f=45$$
-   
  $$(x,y)=(0,3),\ \lambda=5:\quad \nabla f=(0,30)\ =\ \lambda\nabla g=(0,30)\ \Rightarrow\ f=45$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(-3,0),\ \lambda=2:\quad \det\overline{H}=-216\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(3,0),\ \lambda=2:\quad \det\overline{H}=-216\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,-3),\ \lambda=5:\quad \det\overline{H}=216\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(0,3),\ \lambda=5:\quad \det\overline{H}=216\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=45,\quad \min f=18$$

**Risposta corretta:** punti e valori: (-3, 0) → 18; (3, 0) → 18; (0, -3) → 45; (0, 3) → 45 (valore massimo = 45, valore minimo = 18)

#### Esercizio 2
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + 4*y**2 vincolati a x^2 + y^2 = 16, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + 4 y^{2},\quad x^2 + y^2 = 16$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + 4 y^{2},\quad g(x,y)=x^{2} + y^{2} - 16=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(2 x)\quad,\quad 8 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 16=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$- 8 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(-4,0),\ \lambda=2:\quad \nabla f=(-16,0)\ =\ \lambda\nabla g=(-16,0)\ \Rightarrow\ f=32$$
-   
  $$(x,y)=(4,0),\ \lambda=2:\quad \nabla f=(16,0)\ =\ \lambda\nabla g=(16,0)\ \Rightarrow\ f=32$$
-   
  $$(x,y)=(0,-4),\ \lambda=4:\quad \nabla f=(0,-32)\ =\ \lambda\nabla g=(0,-32)\ \Rightarrow\ f=64$$
-   
  $$(x,y)=(0,4),\ \lambda=4:\quad \nabla f=(0,32)\ =\ \lambda\nabla g=(0,32)\ \Rightarrow\ f=64$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(-4,0),\ \lambda=2:\quad \det\overline{H}=-256\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(4,0),\ \lambda=2:\quad \det\overline{H}=-256\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,-4),\ \lambda=4:\quad \det\overline{H}=256\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(0,4),\ \lambda=4:\quad \det\overline{H}=256\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=64,\quad \min f=32$$

**Risposta corretta:** punti e valori: (-4, 0) → 32; (4, 0) → 32; (0, -4) → 64; (0, 4) → 64 (valore massimo = 64, valore minimo = 32)

#### Esercizio 3
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = x**2 + 3*y**2 vincolati a x + y = 4, e classificare gli eventuali estremi assoluti.

$$f(x,y) = x^{2} + 3 y^{2},\quad x + y = 4$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=x^{2} + 3 y^{2},\quad g(x,y)=x + y - 4=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$2 x=\lambda(1)\quad,\quad 6 y=\lambda(1)\quad,\quad x + y - 4=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$2 x - 6 y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(3,1),\ \lambda=6:\quad \nabla f=(6,6)\ =\ \lambda\nabla g=(6,6)\ \Rightarrow\ f=12$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(3,1),\ \lambda=6:\quad \det\overline{H}=-8\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
- Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:  
  $$\min f=12,\quad \max f:\ \text{non esiste}$$

**Risposta corretta:** punti e valori: (3, 1) → 12 (valore minimo = 12)

#### Esercizio 4
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 2*x**2 + 5*y**2 vincolati a x + y = 6, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 2 x^{2} + 5 y^{2},\quad x + y = 6$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=2 x^{2} + 5 y^{2},\quad g(x,y)=x + y - 6=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$4 x=\lambda(1)\quad,\quad 10 y=\lambda(1)\quad,\quad x + y - 6=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$4 x - 10 y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(\frac{30}{7},\frac{12}{7}),\ \lambda=\frac{120}{7}:\quad \nabla f=(\frac{120}{7},\frac{120}{7})\ =\ \lambda\nabla g=(\frac{120}{7},\frac{120}{7})\ \Rightarrow\ f=\frac{360}{7}$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(\frac{30}{7},\frac{12}{7}),\ \lambda=\frac{120}{7}:\quad \det\overline{H}=-14\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
- Passo 4 — il vincolo è una retta: chiuso ma NON limitato. Essendo f una forma quadratica coerciva, tende a +∞ lungo la retta: esiste solo il minimo assoluto:  
  $$\min f=\frac{360}{7},\quad \max f:\ \text{non esiste}$$

**Risposta corretta:** punti e valori: (4.28571, 1.71429) → 51.4286 (valore minimo = 51.4286)

#### Esercizio 5
**Testo:** Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di f(x,y) = 3*x**2 + 5*y**2 vincolati a x^2 + y^2 = 9, e classificare gli eventuali estremi assoluti.

$$f(x,y) = 3 x^{2} + 5 y^{2},\quad x^2 + y^2 = 9$$

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: 1/2,1/2). Frazioni ok (usa '/').

**Svolgimento passo-passo:**

- Funzione e vincolo:  
  $$f(x,y)=3 x^{2} + 5 y^{2},\quad g(x,y)=x^{2} + y^{2} - 9=0$$
- Passo 1 — sistema di Lagrange: gradiente(f) = λ·gradiente(g), g = 0.  
  $$\nabla f = \lambda \nabla g,\quad g=0$$
- Sistema da risolvere:  
  $$6 x=\lambda(2 x)\quad,\quad 10 y=\lambda(2 y)\quad,\quad x^{2} + y^{2} - 9=0$$
- Un modo pratico per eliminare λ senza calcolarlo subito: essendo i due gradienti paralleli, il loro "prodotto incrociato" deve annullarsi -- equazione equivalente al sistema sopra, ma senza λ:  
  $$- 8 x y=0$$
- Passo 2 — risolvendo questa equazione insieme al vincolo g=0 si trovano i punti stazionari; per ciascuno, λ si ricava da una delle due equazioni del sistema. Verifica (il gradiente di f deve essere esattamente λ volte quello di g):
-   
  $$(x,y)=(-3,0),\ \lambda=3:\quad \nabla f=(-18,0)\ =\ \lambda\nabla g=(-18,0)\ \Rightarrow\ f=27$$
-   
  $$(x,y)=(3,0),\ \lambda=3:\quad \nabla f=(18,0)\ =\ \lambda\nabla g=(18,0)\ \Rightarrow\ f=27$$
-   
  $$(x,y)=(0,-3),\ \lambda=5:\quad \nabla f=(0,-30)\ =\ \lambda\nabla g=(0,-30)\ \Rightarrow\ f=45$$
-   
  $$(x,y)=(0,3),\ \lambda=5:\quad \nabla f=(0,30)\ =\ \lambda\nabla g=(0,30)\ \Rightarrow\ f=45$$
- Passo 3 — classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H} = \begin{pmatrix} 0 & g_x' & g_y' \\ g_x' & L_{xx}'' & L_{xy}'' \\ g_y' & L_{yx}'' & L_{yy}'' \end{pmatrix},\quad \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(-3,0),\ \lambda=3:\quad \det\overline{H}=-144\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(3,0),\ \lambda=3:\quad \det\overline{H}=-144\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0,-3),\ \lambda=5:\quad \det\overline{H}=144\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(0,3),\ \lambda=5:\quad \det\overline{H}=144\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Passo 4 — il vincolo è una circonferenza: chiuso e limitato (compatto). Per Weierstrass f ammette sia massimo sia minimo assoluto (si confrontano TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f=45,\quad \min f=27$$

**Risposta corretta:** punti e valori: (-3, 0) → 27; (3, 0) → 27; (0, -3) → 45; (0, 3) → 45 (valore massimo = 45, valore minimo = 27)


### Temi d'esame (problemi reali) (1 esercizi)

#### Esercizio 1
**Testo:** [18 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = x - y^2 + 2x^2 soggetta al vincolo g(x,y) = x^2 + y^2 + 2x = 0: a) disegnare il vincolo descrivendone le caratteristiche; b) determinare gli eventuali punti di massimo e di minimo utilizzando il metodo dei moltiplicatori di Lagrange e la matrice Hessiana orlata.

$$f(x,y) = x - y^2 + 2x^2,\quad g(x,y) = x^2+y^2+2x = 0$$

*Fonte: 18 ottobre 2025*

**Formato risposta richiesto:** Un punto per riga, formato x,y (es: -2,0).

**Svolgimento passo-passo:**

- Il vincolo g(x,y)=0 riscritto completando il quadrato:  
  $$x^2+2x+y^2=0 \iff (x+1)^2+y^2=1$$
- È una circonferenza di centro (-1,0) e raggio 1: chiusa e limitata (compatta).
- Sistema di Lagrange: gradiente(f) = lambda*gradiente(g), g=0.  
  $$1+4x=\lambda(2x+2),\quad -2y=\lambda(2y),\quad (x+1)^2+y^2=1$$
- Risolvendo il sistema si trovano 4 punti stazionari, con il relativo moltiplicatore lambda e il valore di f:
-   
  $$(x,y)=(- \frac{1}{2}, - \frac{\sqrt{3}}{2}),\ \lambda=-1\ \Rightarrow\ f=- \frac{3}{4}$$
-   
  $$(x,y)=(- \frac{1}{2}, \frac{\sqrt{3}}{2}),\ \lambda=-1\ \Rightarrow\ f=- \frac{3}{4}$$
-   
  $$(x,y)=(0, 0),\ \lambda=\frac{1}{2}\ \Rightarrow\ f=0$$
-   
  $$(x,y)=(-2, 0),\ \lambda=\frac{7}{2}\ \Rightarrow\ f=6$$
- Classifichiamo ogni punto con l'Hessiano orlato (dal formulario): posto L=f-\lambda g,  
  $$\overline{H}=\begin{pmatrix}0&g_x'&g_y'\\g_x'&L_{xx}''&L_{xy}''\\g_y'&L_{yx}''&L_{yy}''\end{pmatrix},\ \ \overline{H}>0\Rightarrow\text{max rel.},\ \overline{H}<0\Rightarrow\text{min rel.}$$
-   
  $$(x,y)=(- \frac{1}{2}, - \frac{\sqrt{3}}{2}):\quad \det\overline{H}=-18\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(- \frac{1}{2}, \frac{\sqrt{3}}{2}):\quad \det\overline{H}=-18\ \Rightarrow\ \textbf{minimo relativo vincolato}$$
-   
  $$(x,y)=(0, 0):\quad \det\overline{H}=12\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
-   
  $$(x,y)=(-2, 0):\quad \det\overline{H}=36\ \Rightarrow\ \textbf{massimo relativo vincolato}$$
- Il vincolo è compatto: per Weierstrass f ammette massimo e minimo assoluto (confrontando TUTTI i valori di f nei punti stazionari, anche quelli relativi):  
  $$\max f = 6 \text{ in } (-2,0), \qquad \min f = -\tfrac34 \text{ in } (-\tfrac12,\pm\tfrac{\sqrt3}{2})$$

**Risposta corretta:** punti e valori: (-0.5, -0.866025) → -0.75; (-0.5, 0.866025) → -0.75; (0, 0) → 0; (-2, 0) → 6 (valore massimo = 6, valore minimo = -0.75)

---

## Punti stazionari liberi  <a id="punti_liberi"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**2 + y**2

$$f(x,y) = x^{2} + y^{2}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{2} + y^{2}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$2 x=0,\quad2 y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=2,\quad f_{yy}=2,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}2 & 0\\0 & 2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}2 & 0\\0 & 2\end{matrix}\right],\ \det H=4,\ \mathrm{tr}\,H=4\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 0) → minimo

#### Esercizio 2
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = 2*x**2 - 4*x + y**2 + 2*y + 3

$$f(x,y) = 2 x^{2} - 4 x + y^{2} + 2 y + 3$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = 2 x^{2} - 4 x + y^{2} + 2 y + 3$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$4 x - 4=0,\quad2 y + 2=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=4,\quad f_{yy}=2,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}4 & 0\\0 & 2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (1, -1) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}4 & 0\\0 & 2\end{matrix}\right],\ \det H=8,\ \mathrm{tr}\,H=6\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (1, -1) → minimo

#### Esercizio 3
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = -x**2 - 4*x - 2*y**2 - 4

$$f(x,y) = - x^{2} - 4 x - 2 y^{2} - 4$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = - x^{2} - 4 x - 2 y^{2} - 4$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$- 2 x - 4=0,\quad- 4 y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=-2,\quad f_{yy}=-4,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}-2 & 0\\0 & -4\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (-2, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}-2 & 0\\0 & -4\end{matrix}\right],\ \det H=8,\ \mathrm{tr}\,H=-6\ \Rightarrow\ \textbf{MASSIMO}$$

**Risposta corretta:** (-2, 0) → massimo

#### Esercizio 4
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = 3*x**2 + y**2 - 4*y + 4

$$f(x,y) = 3 x^{2} + y^{2} - 4 y + 4$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = 3 x^{2} + y^{2} - 4 y + 4$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$6 x=0,\quad2 y - 4=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=6,\quad f_{yy}=2,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}6 & 0\\0 & 2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 2) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}6 & 0\\0 & 2\end{matrix}\right],\ \det H=12,\ \mathrm{tr}\,H=8\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 2) → minimo

#### Esercizio 5
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = -x**2 + 2*x - y**2 + 2*y - 2

$$f(x,y) = - x^{2} + 2 x - y^{2} + 2 y - 2$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = - x^{2} + 2 x - y^{2} + 2 y - 2$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$2 - 2 x=0,\quad2 - 2 y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=-2,\quad f_{yy}=-2,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}-2 & 0\\0 & -2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (1, 1) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}-2 & 0\\0 & -2\end{matrix}\right],\ \det H=4,\ \mathrm{tr}\,H=-4\ \Rightarrow\ \textbf{MASSIMO}$$

**Risposta corretta:** (1, 1) → massimo


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**2 - 3*x*y + y**2

$$f(x,y) = x^{2} - 3 x y + y^{2}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{2} - 3 x y + y^{2}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$2 x - 3 y=0,\quad- 3 x + 2 y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=2,\quad f_{yy}=2,\quad f_{xy}=-3$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}2 & -3\\-3 & 2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}2 & -3\\-3 & 2\end{matrix}\right],\ \det H=-5,\ \mathrm{tr}\,H=4\ \Rightarrow\ \textbf{SELLA}$$

**Risposta corretta:** (0, 0) → sella

#### Esercizio 2
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**2 - x*y + y**2

$$f(x,y) = x^{2} - x y + y^{2}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{2} - x y + y^{2}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$2 x - y=0,\quad- x + 2 y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=2,\quad f_{yy}=2,\quad f_{xy}=-1$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}2 & -1\\-1 & 2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}2 & -1\\-1 & 2\end{matrix}\right],\ \det H=3,\ \mathrm{tr}\,H=4\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 0) → minimo

#### Esercizio 3
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**2 - 2*x - y**2 - 4*y - 3

$$f(x,y) = x^{2} - 2 x - y^{2} - 4 y - 3$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{2} - 2 x - y^{2} - 4 y - 3$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$2 x - 2=0,\quad- 2 y - 4=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=2,\quad f_{yy}=-2,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}2 & 0\\0 & -2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (1, -2) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}2 & 0\\0 & -2\end{matrix}\right],\ \det H=-4,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$

**Risposta corretta:** (1, -2) → sella

#### Esercizio 4
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = 2*x**2 - 4*x*y + 3*y**2

$$f(x,y) = 2 x^{2} - 4 x y + 3 y^{2}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = 2 x^{2} - 4 x y + 3 y^{2}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$4 x - 4 y=0,\quad- 4 x + 6 y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=4,\quad f_{yy}=6,\quad f_{xy}=-4$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}4 & -4\\-4 & 6\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}4 & -4\\-4 & 6\end{matrix}\right],\ \det H=8,\ \mathrm{tr}\,H=10\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 0) → minimo

#### Esercizio 5
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**2 + 2*x - y**2 - 4*y + 3

$$f(x,y) = x^{2} + 2 x - y^{2} - 4 y + 3$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{2} + 2 x - y^{2} - 4 y + 3$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$2 x + 2=0,\quad- 2 y - 4=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=2,\quad f_{yy}=-2,\quad f_{xy}=0$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}2 & 0\\0 & -2\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (-1, -2) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}2 & 0\\0 & -2\end{matrix}\right],\ \det H=-4,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$

**Risposta corretta:** (-1, -2) → sella


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**3 - 3*x*y + y**3

$$f(x,y) = x^{3} - 3 x y + y^{3}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{3} - 3 x y + y^{3}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$3 x^{2} - 3 y=0,\quad- 3 x + 3 y^{2}=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=6 x,\quad f_{yy}=6 y,\quad f_{xy}=-3$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}6 x & -3\\-3 & 6 y\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}0 & -3\\-3 & 0\end{matrix}\right],\ \det H=-9,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$
- Punto (1, 1) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}6 & -3\\-3 & 6\end{matrix}\right],\ \det H=27,\ \mathrm{tr}\,H=12\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 0) → sella; (1, 1) → minimo

#### Esercizio 2
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**3 - 6*x*y + y**3

$$f(x,y) = x^{3} - 6 x y + y^{3}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{3} - 6 x y + y^{3}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$3 x^{2} - 6 y=0,\quad- 6 x + 3 y^{2}=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=6 x,\quad f_{yy}=6 y,\quad f_{xy}=-6$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}6 x & -6\\-6 & 6 y\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}0 & -6\\-6 & 0\end{matrix}\right],\ \det H=-36,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$
- Punto (2, 2) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}12 & -6\\-6 & 12\end{matrix}\right],\ \det H=108,\ \mathrm{tr}\,H=24\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 0) → sella; (2, 2) → minimo

#### Esercizio 3
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**3 - 9*x*y + y**3

$$f(x,y) = x^{3} - 9 x y + y^{3}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{3} - 9 x y + y^{3}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$3 x^{2} - 9 y=0,\quad- 9 x + 3 y^{2}=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=6 x,\quad f_{yy}=6 y,\quad f_{xy}=-9$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}6 x & -9\\-9 & 6 y\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}0 & -9\\-9 & 0\end{matrix}\right],\ \det H=-81,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$
- Punto (3, 3) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}18 & -9\\-9 & 18\end{matrix}\right],\ \det H=243,\ \mathrm{tr}\,H=36\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (0, 0) → sella; (3, 3) → minimo

#### Esercizio 4
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**3 - 3*x*y**2

$$f(x,y) = x^{3} - 3 x y^{2}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{3} - 3 x y^{2}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$3 x^{2} - 3 y^{2}=0,\quad- 6 x y=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=6 x,\quad f_{yy}=- 6 x,\quad f_{xy}=- 6 y$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}6 x & - 6 y\\- 6 y & - 6 x\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}0 & 0\\0 & 0\end{matrix}\right],\ \det H=0,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{INDETERMINATO}$$

**Risposta corretta:** (0, 0) → indeterminato

#### Esercizio 5
**Testo:** Trovare e classificare i punti stazionari di f(x,y) = x**4 - 4*x*y + y**4

$$f(x,y) = x^{4} - 4 x y + y^{4}$$

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo). Tipi: minimo, massimo, sella, indeterminato.

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{4} - 4 x y + y^{4}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$4 x^{3} - 4 y=0,\quad- 4 x + 4 y^{3}=0$$
- Passo 2 — calcoliamo le tre derivate parziali seconde:  
  $$f_{xx}=12 x^{2},\quad f_{yy}=12 y^{2},\quad f_{xy}=-4$$
- ...e ne formiamo la matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}12 x^{2} & -4\\-4 & 12 y^{2}\end{matrix}\right]$$
- Passo 3 — per ogni punto stazionario verifichiamo che annulli il gradiente, poi valutiamo H e ne studiamo il segno (det>0 e traccia>0 → minimo; det>0 e traccia<0 → massimo; det<0 → sella; det=0 → indeterminato):
- Punto (-1, -1) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}12 & -4\\-4 & 12\end{matrix}\right],\ \det H=128,\ \mathrm{tr}\,H=24\ \Rightarrow\ \textbf{MINIMO}$$
- Punto (0, 0) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}0 & -4\\-4 & 0\end{matrix}\right],\ \det H=-16,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$
- Punto (1, 1) — verifica del gradiente:  
  $$f_x=0,\ f_y=0$$
-   
  $$H=\left[\begin{matrix}12 & -4\\-4 & 12\end{matrix}\right],\ \det H=128,\ \mathrm{tr}\,H=24\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (-1, -1) → minimo; (0, 0) → sella; (1, 1) → minimo


### Temi d'esame (problemi reali) (4 esercizi)

#### Esercizio 1
**Testo:** [22 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = xy·e^(-(x²+y²)), determinare gli eventuali punti di massimo e di minimo utilizzando la matrice Hessiana.

$$f(x,y) = x y e^{- x^{2} - y^{2}}$$

*Fonte: 22 ottobre 2025*

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo).

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x y e^{- x^{2} - y^{2}}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$- 2 x^{2} y e^{- x^{2} - y^{2}} + y e^{- x^{2} - y^{2}}=0,\quad- 2 x y^{2} e^{- x^{2} - y^{2}} + x e^{- x^{2} - y^{2}}=0$$
- Passo 2 — matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}4 x^{3} y e^{- x^{2} - y^{2}} - 6 x y e^{- x^{2} - y^{2}} & 4 x^{2} y^{2} e^{- x^{2} - y^{2}} - 2 x^{2} e^{- x^{2} - y^{2}} - 2 y^{2} e^{- x^{2} - y^{2}} + e^{- x^{2} - y^{2}}\\4 x^{2} y^{2} e^{- x^{2} - y^{2}} - 2 x^{2} e^{- x^{2} - y^{2}} - 2 y^{2} e^{- x^{2} - y^{2}} + e^{- x^{2} - y^{2}} & 4 x y^{3} e^{- x^{2} - y^{2}} - 6 x y e^{- x^{2} - y^{2}}\end{matrix}\right]$$
- Punto (0, 0):  
  $$H=\left[\begin{matrix}0 & 1\\1 & 0\end{matrix}\right],\ \det H=-1,\ \mathrm{tr}\,H=0\ \Rightarrow\ \textbf{SELLA}$$
- Punto (- \frac{\sqrt{2}}{2}, - \frac{\sqrt{2}}{2}):  
  $$H=\left[\begin{matrix}- \frac{2}{e} & 0\\0 & - \frac{2}{e}\end{matrix}\right],\ \det H=\frac{4}{e^{2}},\ \mathrm{tr}\,H=- \frac{4}{e}\ \Rightarrow\ \textbf{MASSIMO}$$
- Punto (- \frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2}):  
  $$H=\left[\begin{matrix}\frac{2}{e} & 0\\0 & \frac{2}{e}\end{matrix}\right],\ \det H=\frac{4}{e^{2}},\ \mathrm{tr}\,H=\frac{4}{e}\ \Rightarrow\ \textbf{MINIMO}$$
- Punto (\frac{\sqrt{2}}{2}, - \frac{\sqrt{2}}{2}):  
  $$H=\left[\begin{matrix}\frac{2}{e} & 0\\0 & \frac{2}{e}\end{matrix}\right],\ \det H=\frac{4}{e^{2}},\ \mathrm{tr}\,H=\frac{4}{e}\ \Rightarrow\ \textbf{MINIMO}$$
- Punto (\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2}):  
  $$H=\left[\begin{matrix}- \frac{2}{e} & 0\\0 & - \frac{2}{e}\end{matrix}\right],\ \det H=\frac{4}{e^{2}},\ \mathrm{tr}\,H=- \frac{4}{e}\ \Rightarrow\ \textbf{MASSIMO}$$

**Risposta corretta:** (0, 0) → sella; (-0.707107, -0.707107) → massimo; (-0.707107, 0.707107) → minimo; (0.707107, -0.707107) → minimo; (0.707107, 0.707107) → massimo

#### Esercizio 2
**Testo:** [23 ottobre 2025, Esercizio 1] Data la funzione f(x,y) = (x-y)·e^(-(x²+y²)), determinare gli eventuali punti di massimo e di minimo utilizzando la matrice Hessiana.

$$f(x,y) = \left(x - y\right) e^{- x^{2} - y^{2}}$$

*Fonte: 23 ottobre 2025*

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo).

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = \left(x - y\right) e^{- x^{2} - y^{2}}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$- 2 x \left(x - y\right) e^{- x^{2} - y^{2}} + e^{- x^{2} - y^{2}}=0,\quad- 2 y \left(x - y\right) e^{- x^{2} - y^{2}} - e^{- x^{2} - y^{2}}=0$$
- Passo 2 — matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}4 x^{2} \left(x - y\right) e^{- x^{2} - y^{2}} - 4 x e^{- x^{2} - y^{2}} - 2 \left(x - y\right) e^{- x^{2} - y^{2}} & 4 x y \left(x - y\right) e^{- x^{2} - y^{2}} + 2 x e^{- x^{2} - y^{2}} - 2 y e^{- x^{2} - y^{2}}\\4 x y \left(x - y\right) e^{- x^{2} - y^{2}} + 2 x e^{- x^{2} - y^{2}} - 2 y e^{- x^{2} - y^{2}} & 4 y^{2} \left(x - y\right) e^{- x^{2} - y^{2}} + 4 y e^{- x^{2} - y^{2}} - 2 \left(x - y\right) e^{- x^{2} - y^{2}}\end{matrix}\right]$$
- Punto (- \frac{1}{2}, \frac{1}{2}):  
  $$H=\left[\begin{matrix}\frac{3}{e^{\frac{1}{2}}} & - \frac{1}{e^{\frac{1}{2}}}\\- \frac{1}{e^{\frac{1}{2}}} & \frac{3}{e^{\frac{1}{2}}}\end{matrix}\right],\ \det H=\frac{8}{e},\ \mathrm{tr}\,H=\frac{6}{e^{\frac{1}{2}}}\ \Rightarrow\ \textbf{MINIMO}$$
- Punto (\frac{1}{2}, - \frac{1}{2}):  
  $$H=\left[\begin{matrix}- \frac{3}{e^{\frac{1}{2}}} & e^{- \frac{1}{2}}\\e^{- \frac{1}{2}} & - \frac{3}{e^{\frac{1}{2}}}\end{matrix}\right],\ \det H=\frac{8}{e},\ \mathrm{tr}\,H=- \frac{6}{e^{\frac{1}{2}}}\ \Rightarrow\ \textbf{MASSIMO}$$

**Risposta corretta:** (-0.5, 0.5) → minimo; (0.5, -0.5) → massimo

#### Esercizio 3
**Testo:** [16 gennaio 2026, Esercizio 1] Data la funzione f(x,y) = x^3 + 3xy^2 - 15x - 12y, studiare la natura dei punti stazionari.

$$f(x,y) = x^{3} + 3 x y^{2} - 15 x - 12 y$$

*Fonte: 16 gennaio 2026*

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo).

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = x^{3} + 3 x y^{2} - 15 x - 12 y$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$3 x^{2} + 3 y^{2} - 15=0,\quad6 x y - 12=0$$
- Passo 2 — matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}6 x & 6 y\\6 y & 6 x\end{matrix}\right]$$
- Punto (-2, -1):  
  $$H=\left[\begin{matrix}-12 & -6\\-6 & -12\end{matrix}\right],\ \det H=108,\ \mathrm{tr}\,H=-24\ \Rightarrow\ \textbf{MASSIMO}$$
- Punto (-1, -2):  
  $$H=\left[\begin{matrix}-6 & -12\\-12 & -6\end{matrix}\right],\ \det H=-108,\ \mathrm{tr}\,H=-12\ \Rightarrow\ \textbf{SELLA}$$
- Punto (1, 2):  
  $$H=\left[\begin{matrix}6 & 12\\12 & 6\end{matrix}\right],\ \det H=-108,\ \mathrm{tr}\,H=12\ \Rightarrow\ \textbf{SELLA}$$
- Punto (2, 1):  
  $$H=\left[\begin{matrix}12 & 6\\6 & 12\end{matrix}\right],\ \det H=108,\ \mathrm{tr}\,H=24\ \Rightarrow\ \textbf{MINIMO}$$

**Risposta corretta:** (-2, -1) → massimo; (-1, -2) → sella; (1, 2) → sella; (2, 1) → minimo

#### Esercizio 4
**Testo:** [17 gennaio 2026, Esercizio 1] Data la funzione f(x,y) = (y-3x²)(y-x²), studiare il segno e rappresentarlo graficamente; studiare la natura dei punti stazionari.

$$f(x,y) = 3 x^{4} - 4 x^{2} y + y^{2}$$

*Fonte: 17 gennaio 2026*

**Formato risposta richiesto:** Un punto per riga, formato x,y,tipo (es: 0,0,minimo).

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = 3 x^{4} - 4 x^{2} y + y^{2}$$
- Passo 1 — annulliamo il gradiente per trovare i punti stazionari:  
  $$- 2 x \left(- 3 x^{2} + y\right) - 6 x \left(- x^{2} + y\right)=0,\quad- 4 x^{2} + 2 y=0$$
- Passo 2 — matrice Hessiana:  
  $$H(x,y) = \left[\begin{matrix}36 x^{2} - 8 y & - 8 x\\- 8 x & 2\end{matrix}\right]$$
- Punto (0, 0):  
  $$H=\left[\begin{matrix}0 & 0\\0 & 2\end{matrix}\right],\ \det H=0,\ \mathrm{tr}\,H=2\ \Rightarrow\ \textbf{INDETERMINATO}$$
- Attenzione: qui l'Hessiano nell'origine ha determinante nullo (caso indeterminato). Lungo OGNI retta y=mx per l'origine, f(x,mx)=x^2(mx-3x)(mx-x) ha il segno di x^2 vicino a 0 (quindi sembra un minimo). Ma lungo la parabola y=2x^2 si ha f(x,2x^2)=(2x^2-3x^2)(2x^2-x^2)=-x^4<0: la funzione è NEGATIVA vicino all'origine lungo questo cammino. Quindi (0,0) NON è un minimo locale, nonostante lo sembri lungo ogni retta: è un punto stazionario che l'Hessiano da solo non basta a classificare, e il test lungo le rette è fuorviante (classico controesempio).

**Risposta corretta:** (0, 0) → indeterminato

---

## EDO 2° ordine / Cauchy  <a id="edo"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Risolvere il problema di Cauchy:  y'' + 0y' + 4y = x,  con y(0) = 1, y'(0) = 1.

$$y'' + 0y' + 4y = x,\quad y(0) = 1,\ y'(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+0y'+4y=x,\quad y(0)=1,\ y'(0)=1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+0r+4=0\ \Rightarrow\ \left[ - 2 i, \  2 i\right]$$
- Radici complesse coniugate:  
  $$0\pm i2\ \Rightarrow\ y_{om}(x)=e^{0x}\left(c_1\cos(2x)+c_2\sin(2x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' un polinomio di grado 1 e 0 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio generico di grado 1 (es. A*x + B).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{x}{4}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} \sin{\left(2 x \right)} + C_{2} \cos{\left(2 x \right)} + \frac{x}{4}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2}=1,\quad y'(0)=2 C_{1} + \frac{1}{4}=1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{3}{8},\quad C_2=1$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{x}{4} + \frac{3 \sin{\left(2 x \right)}}{8} + \cos{\left(2 x \right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Risolvere il problema di Cauchy:  y'' + 0y' + 1y = 0,  con y(0) = 1, y'(0) = 1.

$$y'' + 0y' + 1y = 0,\quad y(0) = 1,\ y'(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+0y'+1y=0,\quad y(0)=1,\ y'(0)=1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+0r+1=0\ \Rightarrow\ \left[ - i, \  i\right]$$
- Radici complesse coniugate:  
  $$0\pm i1\ \Rightarrow\ y_{om}(x)=e^{0x}\left(c_1\cos(1x)+c_2\sin(1x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): y_p = 0 (il termine noto e' nullo, l'equazione e' gia' omogenea).
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} \sin{\left(x \right)} + C_{2} \cos{\left(x \right)}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2}=1,\quad y'(0)=C_{1}=1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=1,\quad C_2=1$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\sin{\left(x \right)} + \cos{\left(x \right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Risolvere il problema di Cauchy:  y'' + 0y' + 4y = 0,  con y(0) = 1, y'(0) = 0.

$$y'' + 0y' + 4y = 0,\quad y(0) = 1,\ y'(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+0y'+4y=0,\quad y(0)=1,\ y'(0)=0$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+0r+4=0\ \Rightarrow\ \left[ - 2 i, \  2 i\right]$$
- Radici complesse coniugate:  
  $$0\pm i2\ \Rightarrow\ y_{om}(x)=e^{0x}\left(c_1\cos(2x)+c_2\sin(2x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): y_p = 0 (il termine noto e' nullo, l'equazione e' gia' omogenea).
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} \sin{\left(2 x \right)} + C_{2} \cos{\left(2 x \right)}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2}=1,\quad y'(0)=2 C_{1}=0$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=0,\quad C_2=1$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\cos{\left(2 x \right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Risolvere il problema di Cauchy:  y'' + 0y' + 1y = x,  con y(0) = 0, y'(0) = 1.

$$y'' + 0y' + 1y = x,\quad y(0) = 0,\ y'(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+0y'+1y=x,\quad y(0)=0,\ y'(0)=1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+0r+1=0\ \Rightarrow\ \left[ - i, \  i\right]$$
- Radici complesse coniugate:  
  $$0\pm i1\ \Rightarrow\ y_{om}(x)=e^{0x}\left(c_1\cos(1x)+c_2\sin(1x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' un polinomio di grado 1 e 0 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio generico di grado 1 (es. A*x + B).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = x$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} \sin{\left(x \right)} + C_{2} \cos{\left(x \right)} + x$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2}=0,\quad y'(0)=C_{1} + 1=1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=0,\quad C_2=0$$
- Soluzione del problema di Cauchy:  
  $$y(x)=x$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Risolvere il problema di Cauchy:  y'' + 0y' + 4y = x,  con y(0) = 0, y'(0) = 0.

$$y'' + 0y' + 4y = x,\quad y(0) = 0,\ y'(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+0y'+4y=x,\quad y(0)=0,\ y'(0)=0$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+0r+4=0\ \Rightarrow\ \left[ - 2 i, \  2 i\right]$$
- Radici complesse coniugate:  
  $$0\pm i2\ \Rightarrow\ y_{om}(x)=e^{0x}\left(c_1\cos(2x)+c_2\sin(2x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' un polinomio di grado 1 e 0 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio generico di grado 1 (es. A*x + B).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{x}{4}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} \sin{\left(2 x \right)} + C_{2} \cos{\left(2 x \right)} + \frac{x}{4}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2}=0,\quad y'(0)=2 C_{1} + \frac{1}{4}=0$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=- \frac{1}{8},\quad C_2=0$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{x}{4} - \frac{\sin{\left(2 x \right)}}{8}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Risolvere il problema di Cauchy:  y'' + 4y' + 5y = exp(x),  con y(0) = 1, y'(0) = 0.

$$y'' + 4y' + 5y = e^{x},\quad y(0) = 1,\ y'(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+4y'+5y=e^{x},\quad y(0)=1,\ y'(0)=0$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+4r+5=0\ \Rightarrow\ \left[ -2 - i, \  -2 + i\right]$$
- Radici complesse coniugate:  
  $$-2\pm i1\ \Rightarrow\ y_{om}(x)=e^{-2x}\left(c_1\cos(1x)+c_2\sin(1x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' del tipo e^x e 1 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = A*e^x.
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{e^{x}}{10}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\left(C_{1} \sin{\left(x \right)} + C_{2} \cos{\left(x \right)}\right) e^{- 2 x} + \frac{e^{x}}{10}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2} + \frac{1}{10}=1,\quad y'(0)=C_{1} - 2 C_{2} + \frac{1}{10}=0$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{17}{10},\quad C_2=\frac{9}{10}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\left(\frac{17 \sin{\left(x \right)}}{10} + \frac{9 \cos{\left(x \right)}}{10}\right) e^{- 2 x} + \frac{e^{x}}{10}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Risolvere il problema di Cauchy:  y'' + 2y' + 1y = cos(x),  con y(0) = 1, y'(0) = 1.

$$y'' + 2y' + 1y = \cos{\left(x \right)},\quad y(0) = 1,\ y'(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+1y=\cos{\left(x \right)},\quad y(0)=1,\ y'(0)=1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+2r+1=0\ \Rightarrow\ \left[ -1\right]$$
- Radice reale doppia:  
  $$r=-1\ \Rightarrow\ y_{om}(x)=c_1e^{-1x}+c_2xe^{-1x}$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' del tipo cos(x)/sin(x) e +-i non sono radici dell'equazione caratteristica (nessuna risonanza): si cerca y_p = A*cos(x) + B*sin(x).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{\sin{\left(x \right)}}{2}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\left(C_{1} + C_{2} x\right) e^{- x} + \frac{\sin{\left(x \right)}}{2}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{1}=1,\quad y'(0)=- C_{1} + C_{2} + \frac{1}{2}=1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=1,\quad C_2=\frac{3}{2}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\left(\frac{3 x}{2} + 1\right) e^{- x} + \frac{\sin{\left(x \right)}}{2}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Risolvere il problema di Cauchy:  y'' + 2y' + 5y = 0,  con y(0) = 2, y'(0) = 1.

$$y'' + 2y' + 5y = 0,\quad y(0) = 2,\ y'(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+5y=0,\quad y(0)=2,\ y'(0)=1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+2r+5=0\ \Rightarrow\ \left[ -1 - 2 i, \  -1 + 2 i\right]$$
- Radici complesse coniugate:  
  $$-1\pm i2\ \Rightarrow\ y_{om}(x)=e^{-1x}\left(c_1\cos(2x)+c_2\sin(2x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): y_p = 0 (il termine noto e' nullo, l'equazione e' gia' omogenea).
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\left(C_{1} \sin{\left(2 x \right)} + C_{2} \cos{\left(2 x \right)}\right) e^{- x}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2}=2,\quad y'(0)=2 C_{1} - C_{2}=1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{3}{2},\quad C_2=2$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\left(\frac{3 \sin{\left(2 x \right)}}{2} + 2 \cos{\left(2 x \right)}\right) e^{- x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Risolvere il problema di Cauchy:  y'' + 2y' + 4y = cos(x),  con y(0) = 1, y'(0) = 2.

$$y'' + 2y' + 4y = \cos{\left(x \right)},\quad y(0) = 1,\ y'(0) = 2$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+4y=\cos{\left(x \right)},\quad y(0)=1,\ y'(0)=2$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+2r+4=0\ \Rightarrow\ \left[ -1 - \sqrt{3} i, \  -1 + \sqrt{3} i\right]$$
- Radici complesse coniugate:  
  $$-1\pm i\sqrt{3}\ \Rightarrow\ y_{om}(x)=e^{-1x}\left(c_1\cos(\sqrt{3}x)+c_2\sin(\sqrt{3}x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' del tipo cos(x)/sin(x) e +-i non sono radici dell'equazione caratteristica (nessuna risonanza): si cerca y_p = A*cos(x) + B*sin(x).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{2 \sin{\left(x \right)}}{13} + \frac{3 \cos{\left(x \right)}}{13}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\left(C_{1} \sin{\left(\sqrt{3} x \right)} + C_{2} \cos{\left(\sqrt{3} x \right)}\right) e^{- x} + \frac{2 \sin{\left(x \right)}}{13} + \frac{3 \cos{\left(x \right)}}{13}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2} + \frac{3}{13}=1,\quad y'(0)=\sqrt{3} C_{1} - C_{2} + \frac{2}{13}=2$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{34 \sqrt{3}}{39},\quad C_2=\frac{10}{13}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\left(\frac{34 \sqrt{3} \sin{\left(\sqrt{3} x \right)}}{39} + \frac{10 \cos{\left(\sqrt{3} x \right)}}{13}\right) e^{- x} + \frac{2 \sin{\left(x \right)}}{13} + \frac{3 \cos{\left(x \right)}}{13}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Risolvere il problema di Cauchy:  y'' + 2y' + 4y = cos(x),  con y(0) = -1, y'(0) = -1.

$$y'' + 2y' + 4y = \cos{\left(x \right)},\quad y(0) = -1,\ y'(0) = -1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+4y=\cos{\left(x \right)},\quad y(0)=-1,\ y'(0)=-1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+2r+4=0\ \Rightarrow\ \left[ -1 - \sqrt{3} i, \  -1 + \sqrt{3} i\right]$$
- Radici complesse coniugate:  
  $$-1\pm i\sqrt{3}\ \Rightarrow\ y_{om}(x)=e^{-1x}\left(c_1\cos(\sqrt{3}x)+c_2\sin(\sqrt{3}x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' del tipo cos(x)/sin(x) e +-i non sono radici dell'equazione caratteristica (nessuna risonanza): si cerca y_p = A*cos(x) + B*sin(x).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{2 \sin{\left(x \right)}}{13} + \frac{3 \cos{\left(x \right)}}{13}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\left(C_{1} \sin{\left(\sqrt{3} x \right)} + C_{2} \cos{\left(\sqrt{3} x \right)}\right) e^{- x} + \frac{2 \sin{\left(x \right)}}{13} + \frac{3 \cos{\left(x \right)}}{13}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2} + \frac{3}{13}=-1,\quad y'(0)=\sqrt{3} C_{1} - C_{2} + \frac{2}{13}=-1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=- \frac{31 \sqrt{3}}{39},\quad C_2=- \frac{16}{13}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\left(- \frac{31 \sqrt{3} \sin{\left(\sqrt{3} x \right)}}{39} - \frac{16 \cos{\left(\sqrt{3} x \right)}}{13}\right) e^{- x} + \frac{2 \sin{\left(x \right)}}{13} + \frac{3 \cos{\left(x \right)}}{13}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Risolvere il problema di Cauchy:  y'' + 2y' + 6y = x,  con y(0) = 3, y'(0) = 3.

$$y'' + 2y' + 6y = x,\quad y(0) = 3,\ y'(0) = 3$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+6y=x,\quad y(0)=3,\ y'(0)=3$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+2r+6=0\ \Rightarrow\ \left[ -1 - \sqrt{5} i, \  -1 + \sqrt{5} i\right]$$
- Radici complesse coniugate:  
  $$-1\pm i\sqrt{5}\ \Rightarrow\ y_{om}(x)=e^{-1x}\left(c_1\cos(\sqrt{5}x)+c_2\sin(\sqrt{5}x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' un polinomio di grado 1 e 0 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio generico di grado 1 (es. A*x + B).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{x}{6} - \frac{1}{18}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\frac{x}{6} + \left(C_{1} \sin{\left(\sqrt{5} x \right)} + C_{2} \cos{\left(\sqrt{5} x \right)}\right) e^{- x} - \frac{1}{18}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2} - \frac{1}{18}=3,\quad y'(0)=\sqrt{5} C_{1} - C_{2} + \frac{1}{6}=3$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{53 \sqrt{5}}{45},\quad C_2=\frac{55}{18}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{x}{6} + \left(\frac{53 \sqrt{5} \sin{\left(\sqrt{5} x \right)}}{45} + \frac{55 \cos{\left(\sqrt{5} x \right)}}{18}\right) e^{- x} - \frac{1}{18}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Risolvere il problema di Cauchy:  y'' + 6y' + 5y = cos(x),  con y(0) = -1, y'(0) = 0.

$$y'' + 6y' + 5y = \cos{\left(x \right)},\quad y(0) = -1,\ y'(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+6y'+5y=\cos{\left(x \right)},\quad y(0)=-1,\ y'(0)=0$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+6r+5=0\ \Rightarrow\ \left[ -5, \  -1\right]$$
- Radici reali distinte:  
  $$y_{om}(x)=c_1e^{-5x}+c_2e^{-1x}$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' del tipo cos(x)/sin(x) e +-i non sono radici dell'equazione caratteristica (nessuna risonanza): si cerca y_p = A*cos(x) + B*sin(x).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{3 \sin{\left(x \right)}}{26} + \frac{\cos{\left(x \right)}}{13}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} e^{- 5 x} + C_{2} e^{- x} + \frac{3 \sin{\left(x \right)}}{26} + \frac{\cos{\left(x \right)}}{13}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{1} + C_{2} + \frac{1}{13}=-1,\quad y'(0)=- 5 C_{1} - C_{2} + \frac{3}{26}=0$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{31}{104},\quad C_2=- \frac{11}{8}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{3 \sin{\left(x \right)}}{26} + \frac{\cos{\left(x \right)}}{13} - \frac{11 e^{- x}}{8} + \frac{31 e^{- 5 x}}{104}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Risolvere il problema di Cauchy:  y'' + 4y' + 5y = x,  con y(0) = 0, y'(0) = 2.

$$y'' + 4y' + 5y = x,\quad y(0) = 0,\ y'(0) = 2$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+4y'+5y=x,\quad y(0)=0,\ y'(0)=2$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+4r+5=0\ \Rightarrow\ \left[ -2 - i, \  -2 + i\right]$$
- Radici complesse coniugate:  
  $$-2\pm i1\ \Rightarrow\ y_{om}(x)=e^{-2x}\left(c_1\cos(1x)+c_2\sin(1x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' un polinomio di grado 1 e 0 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio generico di grado 1 (es. A*x + B).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{x}{5} - \frac{4}{25}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\frac{x}{5} + \left(C_{1} \sin{\left(x \right)} + C_{2} \cos{\left(x \right)}\right) e^{- 2 x} - \frac{4}{25}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2} - \frac{4}{25}=0,\quad y'(0)=C_{1} - 2 C_{2} + \frac{1}{5}=2$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{53}{25},\quad C_2=\frac{4}{25}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{x}{5} + \left(\frac{53 \sin{\left(x \right)}}{25} + \frac{4 \cos{\left(x \right)}}{25}\right) e^{- 2 x} - \frac{4}{25}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Risolvere il problema di Cauchy:  y'' + 2y' + 10y = x,  con y(0) = 3, y'(0) = 1.

$$y'' + 2y' + 10y = x,\quad y(0) = 3,\ y'(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+10y=x,\quad y(0)=3,\ y'(0)=1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+2r+10=0\ \Rightarrow\ \left[ -1 - 3 i, \  -1 + 3 i\right]$$
- Radici complesse coniugate:  
  $$-1\pm i3\ \Rightarrow\ y_{om}(x)=e^{-1x}\left(c_1\cos(3x)+c_2\sin(3x)\right)$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' un polinomio di grado 1 e 0 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = polinomio generico di grado 1 (es. A*x + B).
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{x}{10} - \frac{1}{50}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=\frac{x}{10} + \left(C_{1} \sin{\left(3 x \right)} + C_{2} \cos{\left(3 x \right)}\right) e^{- x} - \frac{1}{50}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{2} - \frac{1}{50}=3,\quad y'(0)=3 C_{1} - C_{2} + \frac{1}{10}=1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{98}{75},\quad C_2=\frac{151}{50}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{x}{10} + \left(\frac{98 \sin{\left(3 x \right)}}{75} + \frac{151 \cos{\left(3 x \right)}}{50}\right) e^{- x} - \frac{1}{50}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Risolvere il problema di Cauchy:  y'' + 6y' + 6y = exp(x),  con y(0) = 2, y'(0) = -1.

$$y'' + 6y' + 6y = e^{x},\quad y(0) = 2,\ y'(0) = -1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+6y'+6y=e^{x},\quad y(0)=2,\ y'(0)=-1$$
- Passo 1 — equazione caratteristica dell'omogenea associata:  
  $$r^2+6r+6=0\ \Rightarrow\ \left[ -3 - \sqrt{3}, \  -3 + \sqrt{3}\right]$$
- Radici reali distinte:  
  $$y_{om}(x)=c_1e^{-3 - \sqrt{3}x}+c_2e^{-3 + \sqrt{3}x}$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza): il termine noto e' del tipo e^x e 1 non e' radice dell'equazione caratteristica (nessuna risonanza): si cerca y_p = A*e^x.
- Sostituendo l'ansatz nell'equazione e uguagliando i coefficienti (metodo dei coefficienti indeterminati) si trova la soluzione particolare:  
  $$y_p(x) = \frac{e^{x}}{13}$$
- Passo 3 — per sovrapposizione, la soluzione generale è omogenea + particolare:  
  $$y(x)=C_{1} e^{x \left(-3 + \sqrt{3}\right)} + C_{2} e^{- x \left(\sqrt{3} + 3\right)} + \frac{e^{x}}{13}$$
- Passo 4 — imponiamo le condizioni iniziali: calcoliamo y(x) e y'(x) in x=0 e li uguagliamo ai valori assegnati:  
  $$y(0)=C_{1} + C_{2} + \frac{1}{13}=2,\quad y'(0)=C_{1} \left(-3 + \sqrt{3}\right) + C_{2} \left(-3 - \sqrt{3}\right) + \frac{1}{13}=-1$$
- Risolvendo il sistema lineare in C1, C2:  
  $$C_1=\frac{25}{26} + \frac{61 \sqrt{3}}{78},\quad C_2=\frac{25}{26} - \frac{61 \sqrt{3}}{78}$$
- Soluzione del problema di Cauchy:  
  $$y(x)=\frac{e^{x}}{13} + \left(\frac{25}{26} + \frac{61 \sqrt{3}}{78}\right) e^{x \left(-3 + \sqrt{3}\right)} + \left(\frac{25}{26} - \frac{61 \sqrt{3}}{78}\right) e^{- x \left(\sqrt{3} + 3\right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Temi d'esame (problemi reali) (5 esercizi)

#### Esercizio 1
**Testo:** [25 ottobre 2025, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' - y' - 2y = -3e^(2x) - 2e^(-x), con y(0)=0, y'(0)=3. (doppia risonanza: entrambi i termini forzanti coincidono con le due radici dell'equazione caratteristica)

$$y''-y'-2y=-3e^{2x}-2e^{-x},\quad y(0)=0,\ y'(0)=3$$

*Fonte: 25 ottobre 2025*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''-y'-2y=-3e^{2x}-2e^{-x},\quad y(0)=0,\ y'(0)=3$$
- Passo 1 — equazione caratteristica:  
  $$r^2+-1r+-2=0 \Rightarrow \left[ -1, \  2\right]$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza, dal formulario): per ogni termine del termine noto, verifichiamo se coincide con una radice dell'equazione caratteristica (risonanza):
- Radici: r=2 e r=-1 (Caso 2 del formulario, esponenziale A·e^(λx)).
- Termine -3e^(2x): λ=2 È radice → RISONANZA → ansatz  
  $$y_{p1} = c_1\,x\,e^{2x}$$
- Termine -2e^(-x): λ=-1 È radice → RISONANZA → ansatz  
  $$y_{p2} = c_2\,x\,e^{-x}$$
- Soluzione generale (omogenea + particolare, sovrapponendo eventuali più termini del termine noto):  
  $$y(x)=\left(C_{1} - x\right) e^{2 x} + \left(C_{2} + \frac{2 x}{3}\right) e^{- x}$$
- Passo 3 — imponendo le condizioni iniziali:  
  $$y(x)=\left(\frac{10}{9} - x\right) e^{2 x} + \left(\frac{2 x}{3} - \frac{10}{9}\right) e^{- x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** [14 gennaio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' + 2y' + y = 3x^2 + e^(-x)sin(x), con y(0)=17, y'(0)=-10.

$$y''+2y'+y=3x^2+e^{-x}\sin x,\quad y(0)=17,\ y'(0)=-10$$

*Fonte: 14 gennaio 2026*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+2y'+y=3x^2+e^{-x}\sin x,\quad y(0)=17,\ y'(0)=-10$$
- Passo 1 — equazione caratteristica:  
  $$r^2+2r+1=0 \Rightarrow \left[ -1\right]$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza, dal formulario): per ogni termine del termine noto, verifichiamo se coincide con una radice dell'equazione caratteristica (risonanza):
- Radice: r=-1 doppia (radice reale, non complessa).
- Termine 3x² (Caso 1, polinomio grado 2): 0 non è radice → NO risonanza → ansatz  
  $$y_{p1} = Ax^2+Bx+C$$
- Termine e^(-x)sin(x) (Caso 4, e^(αx)(A cosβx+B sinβx) con α=-1,β=1): α+iβ=-1+i NON è radice (la radice è -1, reale) → NO risonanza → ansatz  
  $$y_{p2} = e^{-x}(D\cos x+E\sin x)$$
- Soluzione generale (omogenea + particolare, sovrapponendo eventuali più termini del termine noto):  
  $$y(x)=3 x^{2} - 12 x + \left(C_{1} + C_{2} x - \sin{\left(x \right)}\right) e^{- x} + 18$$
- Passo 3 — imponendo le condizioni iniziali:  
  $$y(x)=3 x^{2} - 12 x + \left(2 x - \sin{\left(x \right)} - 1\right) e^{- x} + 18$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** [16 gennaio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' - 2y' + 5y = e^x·cos(x), con y(0)=1, y'(0)=1.

$$y''-2y'+5y=e^{x}\cos x,\quad y(0)=1,\ y'(0)=1$$

*Fonte: 16 gennaio 2026*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''-2y'+5y=e^{x}\cos x,\quad y(0)=1,\ y'(0)=1$$
- Passo 1 — equazione caratteristica:  
  $$r^2+-2r+5=0 \Rightarrow \left[ 1 - 2 i, \  1 + 2 i\right]$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza, dal formulario): per ogni termine del termine noto, verifichiamo se coincide con una radice dell'equazione caratteristica (risonanza):
- Radici: r=1±2i (complesse coniugate).
- Termine e^x·cos(x) (Caso 4, α=1,β=1): α+iβ=1+i NON coincide con 1±2i → NO risonanza → ansatz  
  $$y_p = e^{x}(A\cos x+B\sin x)$$
- Soluzione generale (omogenea + particolare, sovrapponendo eventuali più termini del termine noto):  
  $$y(x)=\left(C_{1} \sin{\left(2 x \right)} + C_{2} \cos{\left(2 x \right)} + \frac{\cos{\left(x \right)}}{3}\right) e^{x}$$
- Passo 3 — imponendo le condizioni iniziali:  
  $$y(x)=\left(\frac{\cos{\left(x \right)}}{3} + \frac{2 \cos{\left(2 x \right)}}{3}\right) e^{x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** [17 gennaio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' - 4y' + 4y = (x+3)e^(2x), con y(0)=1, y'(0)=-1. (risonanza: radice doppia r=2 uguale alla frequenza del termine forzante)

$$y''-4y'+4y=(x+3)e^{2x},\quad y(0)=1,\ y'(0)=-1$$

*Fonte: 17 gennaio 2026*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''-4y'+4y=(x+3)e^{2x},\quad y(0)=1,\ y'(0)=-1$$
- Passo 1 — equazione caratteristica:  
  $$r^2+-4r+4=0 \Rightarrow \left[ 2\right]$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza, dal formulario): per ogni termine del termine noto, verifichiamo se coincide con una radice dell'equazione caratteristica (risonanza):
- Radice: r=2 doppia (molteplicità 2).
- Termine (x+3)e^(2x) (Caso 5, e^(λx)·p(x) con λ=2, p grado 1): λ=2 È radice con molteplicità 2 → RISONANZA doppia → si moltiplica per x² → ansatz  
  $$y_p = x^2(Ax+B)e^{2x}$$
- Soluzione generale (omogenea + particolare, sovrapponendo eventuali più termini del termine noto):  
  $$y(x)=\left(C_{1} + x \left(C_{2} + \frac{x^{2}}{6} + \frac{3 x}{2}\right)\right) e^{2 x}$$
- Passo 3 — imponendo le condizioni iniziali:  
  $$y(x)=\left(x \left(\frac{x^{2}}{6} + \frac{3 x}{2} - 3\right) + 1\right) e^{2 x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** [9 maggio 2026, Esercizio 2] Risolvere il seguente problema di Cauchy: y'' + y = 5e^(2x)cos(x), con y(0)=1, y'(0)=1.

$$y''+y=5e^{2x}\cos x,\quad y(0)=1,\ y'(0)=1$$

*Fonte: 9 maggio 2026*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y''+y=5e^{2x}\cos x,\quad y(0)=1,\ y'(0)=1$$
- Passo 1 — equazione caratteristica:  
  $$r^2+0r+1=0 \Rightarrow \left[ - i, \  i\right]$$
- Passo 2 — forma della soluzione particolare (metodo di somiglianza, dal formulario): per ogni termine del termine noto, verifichiamo se coincide con una radice dell'equazione caratteristica (risonanza):
- Radici: r=±i (complesse coniugate, parte reale nulla).
- Termine 5e^(2x)cos(x) (Caso 4, α=2,β=1): α+iβ=2+i NON coincide con ±i → NO risonanza → ansatz  
  $$y_p = e^{2x}(A\cos x+B\sin x)$$
- Soluzione generale (omogenea + particolare, sovrapponendo eventuali più termini del termine noto):  
  $$y(x)=\left(C_{1} + \frac{5 e^{2 x}}{8}\right) \sin{\left(x \right)} + \left(C_{2} + \frac{5 e^{2 x}}{8}\right) \cos{\left(x \right)}$$
- Passo 3 — imponendo le condizioni iniziali:  
  $$y(x)=\left(\frac{5 e^{2 x}}{8} - \frac{7}{8}\right) \sin{\left(x \right)} + \left(\frac{5 e^{2 x}}{8} + \frac{3}{8}\right) \cos{\left(x \right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

---

## EDO 1° ordine / Cauchy  <a id="edo1"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine (fattore integrante)):  y' + 2y = 4,  con y(0) = 1.

$$2 y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)} = 4,\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$2 y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)}=4,\quad y(0)=1$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=2,\quad q(x)=4$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=2 x\ \Rightarrow\ \mu(x)=e^{2 x}$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=2 e^{2 x}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = C_{1} e^{- 2 x} + 2$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = 2 - e^{- 2 x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine (fattore integrante)):  y' + 1y = 3,  con y(0) = 0.

$$y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)} = 3,\quad y(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)}=3,\quad y(0)=0$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=1,\quad q(x)=3$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=x\ \Rightarrow\ \mu(x)=e^{x}$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=3 e^{x}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = C_{1} e^{- x} + 3$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = 3 - 3 e^{- x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Risolvere il problema di Cauchy (equazione a variabili separabili):  y' = 1xy,  con y(0) = 1.

$$\frac{d}{d x} y{\left(x \right)} = x y{\left(x \right)},\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)}=x y{\left(x \right)},\quad y(0)=1$$
- Passo 1 — è a variabili separabili, y' = g(x)·h(y), con:  
  $$g(x)=x,\quad h(y)=y$$
- Passo 2 — separiamo le variabili e integriamo entrambi i membri:  
  $$\int\frac{dy}{h(y)}=\int g(x)\,dx$$
- Calcolando i due integrali:  
  $$\int\frac{dy}{h(y)}=\log{\left(y \right)}\qquad,\qquad \int g(x)\,dx=\frac{x^{2}}{2}+C_1$$
- Passo 3 — isolando y si ottiene la soluzione generale:  
  $$y(x) = C_{1} e^{\frac{x^{2}}{2}}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = e^{\frac{x^{2}}{2}}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Risolvere il problema di Cauchy (equazione a variabili separabili):  y' = 2xy,  con y(0) = 1.

$$\frac{d}{d x} y{\left(x \right)} = 2 x y{\left(x \right)},\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)}=2 x y{\left(x \right)},\quad y(0)=1$$
- Passo 1 — è a variabili separabili, y' = g(x)·h(y), con:  
  $$g(x)=2 x,\quad h(y)=y$$
- Passo 2 — separiamo le variabili e integriamo entrambi i membri:  
  $$\int\frac{dy}{h(y)}=\int g(x)\,dx$$
- Calcolando i due integrali:  
  $$\int\frac{dy}{h(y)}=\log{\left(y \right)}\qquad,\qquad \int g(x)\,dx=x^{2}+C_1$$
- Passo 3 — isolando y si ottiene la soluzione generale:  
  $$y(x) = C_{1} e^{x^{2}}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = e^{x^{2}}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine (fattore integrante)):  y' + -1y = 4,  con y(0) = 1.

$$- y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)} = 4,\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$- y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)}=4,\quad y(0)=1$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=-1,\quad q(x)=4$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=- x\ \Rightarrow\ \mu(x)=e^{- x}$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=- 4 e^{- x}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = C_{1} e^{x} - 4$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = 5 e^{x} - 4$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine a coefficienti variabili (fattore integrante)):  y' + (1/x)y = x^2,  con y(1) = 1.

$$\frac{d}{d x} y{\left(x \right)} + \frac{y{\left(x \right)}}{x} = x^{2},\quad y(1) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)} + \frac{y{\left(x \right)}}{x}=x^{2},\quad y(1)=1$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=\frac{1}{x},\quad q(x)=x^{2}$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=\log{\left(x \right)}\ \Rightarrow\ \mu(x)=x$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=\frac{x^{4}}{4}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = \frac{C_{1} + \frac{x^{4}}{4}}{x}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \frac{\frac{x^{4}}{4} + \frac{3}{4}}{x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Risolvere il problema di Cauchy (equazione di Bernoulli):  y' + y = 1xy^2,  con y(0) = 1.

$$y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)} = x y^{2}{\left(x \right)},\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)}=x y^{2}{\left(x \right)},\quad y(0)=1$$
- Passo 1 — è di Bernoulli, nella forma y' + p(x)y = q(x)y^2, con:  
  $$p(x)=1,\quad q(x)=x,\quad n=2$$
- Passo 2 — sostituzione v = y^(1-2) = 1/y: dividendo l'equazione per y^2 e sostituendo, si ottiene un'equazione LINEARE in v:  
  $$v'+(-1)v=- x$$
- Passo 3 — si risolve questa equazione lineare in v con lo stesso metodo del fattore integrante (Passo 2-3 del caso 'lineare'), e infine si torna a y=1/v. La soluzione generale (costante arbitraria C1) è:  
  $$y(x) = \frac{1}{C_{1} e^{x} + x + 1}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \frac{1}{x + 1}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Risolvere il problema di Cauchy (equazione a variabili separabili):  y' = 1x(1+y^2),  con y(0) = 0.

$$\frac{d}{d x} y{\left(x \right)} = x \left(y^{2}{\left(x \right)} + 1\right),\quad y(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)}=x \left(y^{2}{\left(x \right)} + 1\right),\quad y(0)=0$$
- Passo 1 — è a variabili separabili, y' = g(x)·h(y), con:  
  $$g(x)=x,\quad h(y)=y^{2} + 1$$
- Passo 2 — separiamo le variabili e integriamo entrambi i membri:  
  $$\int\frac{dy}{h(y)}=\int g(x)\,dx$$
- Calcolando i due integrali:  
  $$\int\frac{dy}{h(y)}=\operatorname{atan}{\left(y \right)}\qquad,\qquad \int g(x)\,dx=\frac{x^{2}}{2}+C_1$$
- Passo 3 — isolando y si ottiene la soluzione generale:  
  $$y(x) = \tan{\left(C_{1} + \frac{x^{2}}{2} \right)}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \tan{\left(\frac{x^{2}}{2} \right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine (fattore integrante)):  y' + -1y = exp(2*x),  con y(0) = 0.

$$- y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)} = e^{2 x},\quad y(0) = 0$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$- y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)}=e^{2 x},\quad y(0)=0$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=-1,\quad q(x)=e^{2 x}$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=- x\ \Rightarrow\ \mu(x)=e^{- x}$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=e^{x}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = \left(C_{1} + e^{x}\right) e^{x}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \left(e^{x} - 1\right) e^{x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Risolvere il problema di Cauchy (equazione di Bernoulli):  y' + (-1/x)y = y^2,  con y(1) = 1.

$$\frac{d}{d x} y{\left(x \right)} - \frac{y{\left(x \right)}}{x} = y^{2}{\left(x \right)},\quad y(1) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)} - \frac{y{\left(x \right)}}{x}=y^{2}{\left(x \right)},\quad y(1)=1$$
- Passo 1 — è di Bernoulli, nella forma y' + p(x)y = q(x)y^2, con:  
  $$p(x)=- \frac{1}{x},\quad q(x)=1,\quad n=2$$
- Passo 2 — sostituzione v = y^(1-2) = 1/y: dividendo l'equazione per y^2 e sostituendo, si ottiene un'equazione LINEARE in v:  
  $$v'+(\frac{1}{x})v=-1$$
- Passo 3 — si risolve questa equazione lineare in v con lo stesso metodo del fattore integrante (Passo 2-3 del caso 'lineare'), e infine si torna a y=1/v. La soluzione generale (costante arbitraria C1) è:  
  $$y(x) = \frac{2 x}{C_{1} - x^{2}}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \frac{2 x}{3 - x^{2}}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine a coefficienti variabili (fattore integrante)):  y' + (-2/x)y = x^3,  con y(1) = 2.

$$\frac{d}{d x} y{\left(x \right)} - \frac{2 y{\left(x \right)}}{x} = x^{3},\quad y(1) = 2$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)} - \frac{2 y{\left(x \right)}}{x}=x^{3},\quad y(1)=2$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=- \frac{2}{x},\quad q(x)=x^{3}$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=- 2 \log{\left(x \right)}\ \Rightarrow\ \mu(x)=\frac{1}{x^{2}}$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=\frac{x^{2}}{2}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = x^{2} \left(C_{1} + \frac{x^{2}}{2}\right)$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = x^{2} \left(\frac{x^{2}}{2} + \frac{3}{2}\right)$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** Risolvere il problema di Cauchy (equazione a variabili separabili):  y' = 1x^2y^2,  con y(0) = 1.

$$\frac{d}{d x} y{\left(x \right)} = x^{2} y^{2}{\left(x \right)},\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)}=x^{2} y^{2}{\left(x \right)},\quad y(0)=1$$
- Passo 1 — è a variabili separabili, y' = g(x)·h(y), con:  
  $$g(x)=x^{2},\quad h(y)=y^{2}$$
- Passo 2 — separiamo le variabili e integriamo entrambi i membri:  
  $$\int\frac{dy}{h(y)}=\int g(x)\,dx$$
- Calcolando i due integrali:  
  $$\int\frac{dy}{h(y)}=- \frac{1}{y}\qquad,\qquad \int g(x)\,dx=\frac{x^{3}}{3}+C_1$$
- Passo 3 — isolando y si ottiene la soluzione generale:  
  $$y(x) = - \frac{3}{C_{1} + x^{3}}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = - \frac{3}{x^{3} - 3}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 3
**Testo:** Risolvere il problema di Cauchy (equazione lineare del primo ordine a coefficienti variabili (fattore integrante)):  y' + (-1/x)y = x^4,  con y(1) = 1.

$$\frac{d}{d x} y{\left(x \right)} - \frac{y{\left(x \right)}}{x} = x^{4},\quad y(1) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)} - \frac{y{\left(x \right)}}{x}=x^{4},\quad y(1)=1$$
- Passo 1 — è lineare, nella forma y' + p(x)y = q(x), con:  
  $$p(x)=- \frac{1}{x},\quad q(x)=x^{4}$$
- Passo 2 — fattore integrante μ(x) = e^{∫p(x)dx}:  
  $$\int p(x)\,dx=- \log{\left(x \right)}\ \Rightarrow\ \mu(x)=\frac{1}{x}$$
- Passo 3 — la soluzione generale è y(x) = (1/μ(x))·[∫μ(x)q(x)dx + C1]; calcoliamo l'integrale:  
  $$\int \mu(x)q(x)\,dx=\frac{x^{4}}{4}$$
- Quindi (a meno della costante arbitraria C1):  
  $$y(x) = x \left(C_{1} + \frac{x^{4}}{4}\right)$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = x \left(\frac{x^{4}}{4} + \frac{3}{4}\right)$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 4
**Testo:** Risolvere il problema di Cauchy (equazione di Bernoulli):  y' + y = 2xy^2,  con y(0) = 1.

$$y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)} = 2 x y^{2}{\left(x \right)},\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$y{\left(x \right)} + \frac{d}{d x} y{\left(x \right)}=2 x y^{2}{\left(x \right)},\quad y(0)=1$$
- Passo 1 — è di Bernoulli, nella forma y' + p(x)y = q(x)y^2, con:  
  $$p(x)=1,\quad q(x)=2 x,\quad n=2$$
- Passo 2 — sostituzione v = y^(1-2) = 1/y: dividendo l'equazione per y^2 e sostituendo, si ottiene un'equazione LINEARE in v:  
  $$v'+(-1)v=- 2 x$$
- Passo 3 — si risolve questa equazione lineare in v con lo stesso metodo del fattore integrante (Passo 2-3 del caso 'lineare'), e infine si torna a y=1/v. La soluzione generale (costante arbitraria C1) è:  
  $$y(x) = \frac{1}{C_{1} e^{x} + 2 x + 2}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \frac{1}{2 x - e^{x} + 2}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 5
**Testo:** Risolvere il problema di Cauchy (equazione a variabili separabili):  y' = 1x(1+y^2),  con y(0) = 1.

$$\frac{d}{d x} y{\left(x \right)} = x \left(y^{2}{\left(x \right)} + 1\right),\quad y(0) = 1$$

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es:  exp(-x)*(1+x)

**Svolgimento passo-passo:**

- Equazione:  
  $$\frac{d}{d x} y{\left(x \right)}=x \left(y^{2}{\left(x \right)} + 1\right),\quad y(0)=1$$
- Passo 1 — è a variabili separabili, y' = g(x)·h(y), con:  
  $$g(x)=x,\quad h(y)=y^{2} + 1$$
- Passo 2 — separiamo le variabili e integriamo entrambi i membri:  
  $$\int\frac{dy}{h(y)}=\int g(x)\,dx$$
- Calcolando i due integrali:  
  $$\int\frac{dy}{h(y)}=\operatorname{atan}{\left(y \right)}\qquad,\qquad \int g(x)\,dx=\frac{x^{2}}{2}+C_1$$
- Passo 3 — isolando y si ottiene la soluzione generale:  
  $$y(x) = \tan{\left(C_{1} + \frac{x^{2}}{2} \right)}$$
- Passo finale — imponendo la condizione iniziale si ottiene:  
  $$y(x) = \tan{\left(\frac{x^{2}}{2} + \frac{\pi}{4} \right)}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione


### Temi d'esame (problemi reali) (2 esercizi)

#### Esercizio 1
**Testo:** [20 ottobre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: y' + y/x = log(x)/x, con y(1)=2.

$$y' + \tfrac{y}{x} = \tfrac{\log x}{x},\quad y(1)=2$$

*Fonte: 20 ottobre 2025*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: log(x)+3/x

**Svolgimento passo-passo:**

- Equazione:  
  $$y' + \tfrac{y}{x} = \tfrac{\log x}{x},\quad y(1)=2$$
- Passo 1 — equazione lineare del primo ordine a coefficienti variabili: si risolve con il fattore integrante μ(x) = e^{∫(1/x)dx} = x.
- Passo 2 — soluzione generale (costante arbitraria C1):  
  $$y(x) = \frac{C_{1}}{x} + \log{\left(x \right)} - 1$$
- Passo 3 — imponendo la condizione iniziale:  
  $$y(x) = \log{\left(x \right)} - 1 + \frac{3}{x}$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

#### Esercizio 2
**Testo:** [18 ottobre 2025, Esercizio 2] Determinare l'unica soluzione del problema di Cauchy: y' + (log x)·y = log x, con y(2)=2.

$$y' + (\log x)\,y = \log x,\quad y(2)=2$$

*Fonte: 18 ottobre 2025*

**Formato risposta richiesto:** Scrivi y(x) in sintassi Python, es: log(x)+3/x

**Svolgimento passo-passo:**

- Equazione:  
  $$y' + (\log x)\,y = \log x,\quad y(2)=2$$
- Passo 1 — equazione lineare del primo ordine a coefficienti variabili: si risolve con il fattore integrante μ(x) = e^{∫\log x\,dx} = e^{x\log x - x} (l'integrale di log x si fa per parti).
- Passo 2 — soluzione generale (costante arbitraria C1):  
  $$y(x) = C_{1} e^{x \left(1 - \log{\left(x \right)}\right)} + 1$$
- Passo 3 — imponendo la condizione iniziale:  
  $$y(x) = \frac{4 e^{x \left(1 - \log{\left(x \right)}\right)}}{e^{2}} + 1$$

**Risposta corretta:** è una **funzione** (l'espressione esplicita è nell'ultimo passo dello svolgimento qui sotto); viene verificata numericamente confrontando alcuni punti campione

---

## Integrali doppi  <a id="integrali"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Calcolare l'integrale doppio di f(x,y) = x**2 + y**2 su D = { (x,y) : x^2 + y^2 <= 1 }, usando le coordinate polari.

$$\iint_D x^{2} + y^{2}\, dA, \quad D = \{(x,y): x^2+y^2 \le 1\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 1\},\quad f(x,y)=x^{2} + y^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{3}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 1], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{3}\,dr = \frac{r^{4}}{4}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{4}}{4}\Big]_{0}^{1} = \frac{1}{4}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{1}{4}\,d\theta = \frac{\theta}{4}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{\theta}{4}\Big]_0^{2\pi} = \frac{\pi}{2}$$

**Risposta corretta:** **pi/2**

#### Esercizio 2
**Testo:** Calcolare l'integrale doppio di f(x,y) = 1 su D = { (x,y) : x^2 + y^2 <= 4 }, usando le coordinate polari.

$$\iint_D 1\, dA, \quad D = \{(x,y): x^2+y^2 \le 4\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 4\},\quad f(x,y)=1$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r$$
- Passo 2 — estremi di integrazione: r ∈ [0, 2], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r\,dr = \frac{r^{2}}{2}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{2}}{2}\Big]_{0}^{2} = 2$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int 2\,d\theta = 2 \theta$$
- valutata tra 0 e 2π:  
  $$\Big[2 \theta\Big]_0^{2\pi} = 4 \pi$$

**Risposta corretta:** **4*pi**

#### Esercizio 3
**Testo:** Calcolare l'integrale doppio di f(x,y) = 1 su D = { (x,y) : x^2 + y^2 <= 1 }, usando le coordinate polari.

$$\iint_D 1\, dA, \quad D = \{(x,y): x^2+y^2 \le 1\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 1\},\quad f(x,y)=1$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r$$
- Passo 2 — estremi di integrazione: r ∈ [0, 1], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r\,dr = \frac{r^{2}}{2}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{2}}{2}\Big]_{0}^{1} = \frac{1}{2}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{1}{2}\,d\theta = \frac{\theta}{2}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{\theta}{2}\Big]_0^{2\pi} = \pi$$

**Risposta corretta:** **pi**

#### Esercizio 4
**Testo:** Calcolare l'integrale doppio di f(x,y) = x**2 + y**2 su D = { (x,y) : x^2 + y^2 <= 4 }, usando le coordinate polari.

$$\iint_D x^{2} + y^{2}\, dA, \quad D = \{(x,y): x^2+y^2 \le 4\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 4\},\quad f(x,y)=x^{2} + y^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{3}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 2], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{3}\,dr = \frac{r^{4}}{4}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{4}}{4}\Big]_{0}^{2} = 4$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int 4\,d\theta = 4 \theta$$
- valutata tra 0 e 2π:  
  $$\Big[4 \theta\Big]_0^{2\pi} = 8 \pi$$

**Risposta corretta:** **8*pi**

#### Esercizio 5
**Testo:** Calcolare l'integrale doppio di f(x,y) = 1 su D = { (x,y) : x^2 + y^2 <= 9 }, usando le coordinate polari.

$$\iint_D 1\, dA, \quad D = \{(x,y): x^2+y^2 \le 9\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 9\},\quad f(x,y)=1$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r$$
- Passo 2 — estremi di integrazione: r ∈ [0, 3], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r\,dr = \frac{r^{2}}{2}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{2}}{2}\Big]_{0}^{3} = \frac{9}{2}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{9}{2}\,d\theta = \frac{9 \theta}{2}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{9 \theta}{2}\Big]_0^{2\pi} = 9 \pi$$

**Risposta corretta:** **9*pi**


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Calcolare l'integrale doppio di f(x,y) = 1 su D = { (x,y) : 1^2 <= x^2+y^2 <= 3^2 }, usando le coordinate polari.

$$\iint_D 1\, dA, \quad D = \{(x,y): 1 \le x^2+y^2 \le 9\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): 1 \le x^2+y^2 \le 9\},\quad f(x,y)=1$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r$$
- Passo 2 — estremi di integrazione: r ∈ [1, 3], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r\,dr = \frac{r^{2}}{2}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{2}}{2}\Big]_{1}^{3} = 4$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int 4\,d\theta = 4 \theta$$
- valutata tra 0 e 2π:  
  $$\Big[4 \theta\Big]_0^{2\pi} = 8 \pi$$

**Risposta corretta:** **8*pi**

#### Esercizio 2
**Testo:** Calcolare l'integrale doppio di f(x,y) = x**2 + y**2 su D = { (x,y) : x^2 + y^2 <= 1 }, usando le coordinate polari.

$$\iint_D x^{2} + y^{2}\, dA, \quad D = \{(x,y): x^2+y^2 \le 1\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 1\},\quad f(x,y)=x^{2} + y^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{3}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 1], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{3}\,dr = \frac{r^{4}}{4}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{4}}{4}\Big]_{0}^{1} = \frac{1}{4}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{1}{4}\,d\theta = \frac{\theta}{4}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{\theta}{4}\Big]_0^{2\pi} = \frac{\pi}{2}$$

**Risposta corretta:** **pi/2**

#### Esercizio 3
**Testo:** Calcolare l'integrale doppio di f(x,y) = sqrt(x**2 + y**2) su D = { (x,y) : x^2 + y^2 <= 4 }, usando le coordinate polari.

$$\iint_D \sqrt{x^{2} + y^{2}}\, dA, \quad D = \{(x,y): x^2+y^2 \le 4\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 4\},\quad f(x,y)=\sqrt{x^{2} + y^{2}}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r \sqrt{r^{2}}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 2], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r \sqrt{r^{2}}\,dr = \frac{r^{2} \sqrt{r^{2}}}{3}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{2} \sqrt{r^{2}}}{3}\Big]_{0}^{2} = \frac{8}{3}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{8}{3}\,d\theta = \frac{8 \theta}{3}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{8 \theta}{3}\Big]_0^{2\pi} = \frac{16 \pi}{3}$$

**Risposta corretta:** **16*pi/3**

#### Esercizio 4
**Testo:** Calcolare l'integrale doppio di f(x,y) = x**2 + y**2 su D = { (x,y) : 1^2 <= x^2+y^2 <= 2^2 }, usando le coordinate polari.

$$\iint_D x^{2} + y^{2}\, dA, \quad D = \{(x,y): 1 \le x^2+y^2 \le 4\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): 1 \le x^2+y^2 \le 4\},\quad f(x,y)=x^{2} + y^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{3}$$
- Passo 2 — estremi di integrazione: r ∈ [1, 2], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{3}\,dr = \frac{r^{4}}{4}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{4}}{4}\Big]_{1}^{2} = \frac{15}{4}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{15}{4}\,d\theta = \frac{15 \theta}{4}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{15 \theta}{4}\Big]_0^{2\pi} = \frac{15 \pi}{2}$$

**Risposta corretta:** **15*pi/2**

#### Esercizio 5
**Testo:** Calcolare l'integrale doppio di f(x,y) = sqrt(x**2 + y**2) su D = { (x,y) : x^2 + y^2 <= 1 }, usando le coordinate polari.

$$\iint_D \sqrt{x^{2} + y^{2}}\, dA, \quad D = \{(x,y): x^2+y^2 \le 1\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 1\},\quad f(x,y)=\sqrt{x^{2} + y^{2}}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r \sqrt{r^{2}}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 1], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r \sqrt{r^{2}}\,dr = \frac{r^{2} \sqrt{r^{2}}}{3}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{2} \sqrt{r^{2}}}{3}\Big]_{0}^{1} = \frac{1}{3}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{1}{3}\,d\theta = \frac{\theta}{3}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{\theta}{3}\Big]_0^{2\pi} = \frac{2 \pi}{3}$$

**Risposta corretta:** **2*pi/3**


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Calcolare l'integrale doppio di f(x,y) = (x**2 + y**2)**2 su D = { (x,y) : 2^2 <= x^2+y^2 <= 4^2 }, usando le coordinate polari.

$$\iint_D \left(x^{2} + y^{2}\right)^{2}\, dA, \quad D = \{(x,y): 4 \le x^2+y^2 \le 16\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): 4 \le x^2+y^2 \le 16\},\quad f(x,y)=\left(x^{2} + y^{2}\right)^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{5}$$
- Passo 2 — estremi di integrazione: r ∈ [2, 4], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{5}\,dr = \frac{r^{6}}{6}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{6}}{6}\Big]_{2}^{4} = 672$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int 672\,d\theta = 672 \theta$$
- valutata tra 0 e 2π:  
  $$\Big[672 \theta\Big]_0^{2\pi} = 1344 \pi$$

**Risposta corretta:** **1344*pi**

#### Esercizio 2
**Testo:** Calcolare l'integrale doppio di f(x,y) = (x**2 + y**2)**2 su D = { (x,y) : x^2 + y^2 <= 9 }, usando le coordinate polari.

$$\iint_D \left(x^{2} + y^{2}\right)^{2}\, dA, \quad D = \{(x,y): x^2+y^2 \le 9\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 9\},\quad f(x,y)=\left(x^{2} + y^{2}\right)^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{5}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 3], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{5}\,dr = \frac{r^{6}}{6}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{6}}{6}\Big]_{0}^{3} = \frac{243}{2}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{243}{2}\,d\theta = \frac{243 \theta}{2}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{243 \theta}{2}\Big]_0^{2\pi} = 243 \pi$$

**Risposta corretta:** **243*pi**

#### Esercizio 3
**Testo:** Calcolare l'integrale doppio di f(x,y) = x*y su D = { (x,y) : x^2 + y^2 <= 4 }, usando le coordinate polari.

$$\iint_D x y\, dA, \quad D = \{(x,y): x^2+y^2 \le 4\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 4\},\quad f(x,y)=x y$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = \frac{r^{3} \sin{\left(2 \theta \right)}}{2}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 2], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int \frac{r^{3} \sin{\left(2 \theta \right)}}{2}\,dr = \frac{r^{4} \sin{\left(2 \theta \right)}}{8}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{4} \sin{\left(2 \theta \right)}}{8}\Big]_{0}^{2} = 2 \sin{\left(2 \theta \right)}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int 2 \sin{\left(2 \theta \right)}\,d\theta = - \cos{\left(2 \theta \right)}$$
- valutata tra 0 e 2π:  
  $$\Big[- \cos{\left(2 \theta \right)}\Big]_0^{2\pi} = 0$$

**Risposta corretta:** **0**

#### Esercizio 4
**Testo:** Calcolare l'integrale doppio di f(x,y) = (x**2 + y**2)**2 su D = { (x,y) : x^2 + y^2 <= 4 }, usando le coordinate polari.

$$\iint_D \left(x^{2} + y^{2}\right)^{2}\, dA, \quad D = \{(x,y): x^2+y^2 \le 4\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): x^2+y^2 \le 4\},\quad f(x,y)=\left(x^{2} + y^{2}\right)^{2}$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = r^{5}$$
- Passo 2 — estremi di integrazione: r ∈ [0, 2], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int r^{5}\,dr = \frac{r^{6}}{6}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{6}}{6}\Big]_{0}^{2} = \frac{32}{3}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{32}{3}\,d\theta = \frac{32 \theta}{3}$$
- valutata tra 0 e 2π:  
  $$\Big[\frac{32 \theta}{3}\Big]_0^{2\pi} = \frac{64 \pi}{3}$$

**Risposta corretta:** **64*pi/3**

#### Esercizio 5
**Testo:** Calcolare l'integrale doppio di f(x,y) = x*y su D = { (x,y) : 3^2 <= x^2+y^2 <= 4^2 }, usando le coordinate polari.

$$\iint_D x y\, dA, \quad D = \{(x,y): 9 \le x^2+y^2 \le 16\}$$

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es:  pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$D = \{(x,y): 9 \le x^2+y^2 \le 16\},\quad f(x,y)=x y$$
- Passo 1 — cambio in coordinate polari (Jacobiano = r):  
  $$x=r\cos\theta,\ y=r\sin\theta,\quad dx\,dy=r\,dr\,d\theta$$
- f in coordinate polari, con Jacobiano incluso:  
  $$f(r,\theta)\cdot r = \frac{r^{3} \sin{\left(2 \theta \right)}}{2}$$
- Passo 2 — estremi di integrazione: r ∈ [3, 4], θ nell'angolo giro [0, 2π].
- Passo 3 — calcoliamo prima la primitiva rispetto a r:  
  $$\int \frac{r^{3} \sin{\left(2 \theta \right)}}{2}\,dr = \frac{r^{4} \sin{\left(2 \theta \right)}}{8}$$
- e la valutiamo tra gli estremi (primitiva(r_max) − primitiva(r_min)):  
  $$\Big[\frac{r^{4} \sin{\left(2 \theta \right)}}{8}\Big]_{3}^{4} = \frac{175 \sin{\left(2 \theta \right)}}{8}$$
- Passo 4 — allo stesso modo, la primitiva rispetto a θ:  
  $$\int \frac{175 \sin{\left(2 \theta \right)}}{8}\,d\theta = - \frac{175 \cos{\left(2 \theta \right)}}{16}$$
- valutata tra 0 e 2π:  
  $$\Big[- \frac{175 \cos{\left(2 \theta \right)}}{16}\Big]_0^{2\pi} = 0$$

**Risposta corretta:** **0**


### Temi d'esame (problemi reali) (4 esercizi)

#### Esercizio 1
**Testo:** [20 ottobre 2025, Esercizio 3] Dato il dominio D = {(x,y) ∈ R²: x ≤ y/2+1/2, x ≥ y²-1}, disegnare il dominio descrivendo le caratteristiche delle curve e calcolare l'area di D (l'integrale doppio di 1 su D).

$$\iint_D 1\,dA,\quad D: x \le \tfrac{y}{2}+\tfrac12,\ \ x \ge y^2-1$$

*Fonte: 20 ottobre 2025*

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es: pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$\iint_D 1\,dA,\quad D: x \le \tfrac{y}{2}+\tfrac12,\ \ x \ge y^2-1$$
- Intersezione retta-parabola: risolvendo y/2+1/2 = y²-1 si trovano y=-1 e y=3/2.
- Integrando rispetto a x tra la parabola e la retta, poi rispetto a y:  
  $$\int_{-1}^{3/2}\left[\left(\tfrac{y}{2}+\tfrac12\right)-(y^2-1)\right]dy$$
- Valore dell'integrale:  
  $$= \frac{125}{48}$$

**Risposta corretta:** **125/48**

#### Esercizio 2
**Testo:** [23 ottobre 2025, Esercizio 3] Dato l'integrale doppio di f(x,y)=x sul dominio D = {(x,y) ∈ R²: y ≤ 2, x²+y² ≤ 5, x+y ≥ 1}, disegnare il dominio e calcolarne il valore.

$$\iint_D x\,dA,\quad D: y\le2,\ x^2+y^2\le5,\ x+y\ge1$$

*Fonte: 23 ottobre 2025*

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es: pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$\iint_D x\,dA,\quad D: y\le2,\ x^2+y^2\le5,\ x+y\ge1$$
- Valore dell'integrale:  
  $$= \frac{9}{2}$$

**Risposta corretta:** **9/2**

#### Esercizio 3
**Testo:** [16 gennaio 2026, Esercizio 3] Dato l'integrale doppio di f(x,y)=xy sul dominio D = parte di piano delimitata dalle rette x+y=4, 3x+y=4 e x+3y=4, disegnare il dominio e calcolarne il valore.

$$\iint_D xy\,dA,\quad D: \text{triangolo di vertici } (0,4),(1,1),(4,0)$$

*Fonte: 16 gennaio 2026*

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es: pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$\iint_D xy\,dA,\quad D: \text{triangolo di vertici } (0,4),(1,1),(4,0)$$
- Valore dell'integrale:  
  $$= \frac{26}{3}$$

**Risposta corretta:** **26/3**

#### Esercizio 4
**Testo:** [17 gennaio 2026, Esercizio 3] Dato l'integrale doppio di f(x,y)=xy sul dominio D = {(x,y) ∈ R², I quadrante: xy ≥ 10, x²+y² ≤ 29}, descrivere le curve, disegnare il dominio e calcolarne il valore.

$$\iint_D xy\,dA,\quad D: xy\ge10,\ x^2+y^2\le29\ (x,y>0)$$

*Fonte: 17 gennaio 2026*

**Formato risposta richiesto:** Scrivi il valore (numerico o simbolico), es: pi/2

**Svolgimento passo-passo:**

- Dominio e integranda:  
  $$\iint_D xy\,dA,\quad D: xy\ge10,\ x^2+y^2\le29\ (x,y>0)$$
- Le curve xy=10 e x²+y²=29 si intersecano in (2,5) e (5,2): per x tra 2 e 5, y varia tra l'iperbole (sotto) e la circonferenza (sopra).  
  $$\int_2^5\int_{10/x}^{\sqrt{29-x^2}} xy\,dy\,dx$$
- Valore dell'integrale:  
  $$= \frac{609}{8} - 50 \log{\left(\frac{5}{2} \right)}$$

**Risposta corretta:** **609/8 - 50*log(5/2)**

---

## Continuità e differenziabilità  <a id="continuita"></a>

### Livello facile (5 esercizi)

#### Esercizio 1
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x*y/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x y}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x y}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to \frac{\sin{\left(2 \theta \right)}}{2}\ \ (r\to0^+)$$
- Passo 2 — il limite dipende da θ (limite direzionale non unico):  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{4}:\ \frac{1}{2}$$
- Conclusione:  
  $$\textbf{f NON è continua in (0,0)}$$

**Risposta corretta:** NON continua, differenziabilità non rilevante/non richiesta

#### Esercizio 2
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**2 + y**2  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} x^{2} + y^{2} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = x^{2} + y^{2}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il limite per r→0+ è 0 indipendentemente da θ.  
  $$\textbf{f è differenziabile in (0,0)}$$
- Piano tangente in (0,0,0):  
  $$z = 0$$

**Risposta corretta:** continua, differenziabile

#### Esercizio 3
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**2*y/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{2} y}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{2} y}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ 0$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile

#### Esercizio 4
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**3/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{3}}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{3}}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=1,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ 0$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile

#### Esercizio 5
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**2*y**2/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{2} y^{2}}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{2} y^{2}}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il limite per r→0+ è 0 indipendentemente da θ.  
  $$\textbf{f è differenziabile in (0,0)}$$
- Piano tangente in (0,0,0):  
  $$z = 0$$

**Risposta corretta:** continua, differenziabile


### Livello medio (5 esercizi)

#### Esercizio 1
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = (x**2 - y**2)/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{2} - y^{2}}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{2} - y^{2}}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to \cos{\left(2 \theta \right)}\ \ (r\to0^+)$$
- Passo 2 — il limite dipende da θ (limite direzionale non unico):  
  $$\theta=0:\ 1\quad\ne\quad \theta=\frac{\pi}{4}:\ 0$$
- Conclusione:  
  $$\textbf{f NON è continua in (0,0)}$$

**Risposta corretta:** NON continua, differenziabilità non rilevante/non richiesta

#### Esercizio 2
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = y**3/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{y^{3}}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{y^{3}}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=1$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ 0$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile

#### Esercizio 3
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x*y**2/(x**2 + y**4)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x y^{2}}{x^{2} + y^{4}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x y^{2}}{x^{2} + y^{4}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ \tilde{\infty}$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile

#### Esercizio 4
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x*y*(x**2 - y**2)/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x y \left(x^{2} - y^{2}\right)}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x y \left(x^{2} - y^{2}\right)}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il limite per r→0+ è 0 indipendentemente da θ.  
  $$\textbf{f è differenziabile in (0,0)}$$
- Piano tangente in (0,0,0):  
  $$z = 0$$

**Risposta corretta:** continua, differenziabile

#### Esercizio 5
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x*y/sqrt(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x y}{\sqrt{x^{2} + y^{2}}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x y}{\sqrt{x^{2} + y^{2}}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ 0$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile


### Livello difficile (5 esercizi)

#### Esercizio 1
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**2*y/(x**4 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{2} y}{x^{4} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{2} y}{x^{4} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite a θ fissato è 0, ma non basta: proviamo il cammino curvo  
  $$y = k x^{2}$$
- Lungo questo cammino:  
  $$f(x,k x^{2}) \to \frac{k}{k^{2} + 1}\ \ (x\to0,\ \text{dipende da } k)$$
- Conclusione:  
  $$\textbf{f NON è continua in (0,0)} \text{ (il test lungo le rette era fuorviante)}$$

**Risposta corretta:** NON continua, differenziabilità non rilevante/non richiesta

#### Esercizio 2
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**3*y/(x**6 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{3} y}{x^{6} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{3} y}{x^{6} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite a θ fissato è 0, ma non basta: proviamo il cammino curvo  
  $$y = k x^{3}$$
- Lungo questo cammino:  
  $$f(x,k x^{3}) \to \frac{k}{k^{2} + 1}\ \ (x\to0,\ \text{dipende da } k)$$
- Conclusione:  
  $$\textbf{f NON è continua in (0,0)} \text{ (il test lungo le rette era fuorviante)}$$

**Risposta corretta:** NON continua, differenziabilità non rilevante/non richiesta

#### Esercizio 3
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = (x**3 + y**3)/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{3} + y^{3}}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{3} + y^{3}}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=1,\quad f_y(0,0)=1$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ 0$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile

#### Esercizio 4
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = x**2*y**3/(x**4 + y**6)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{x^{2} y^{3}}{x^{4} + y^{6}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{x^{2} y^{3}}{x^{4} + y^{6}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il resto dipende da θ:  
  $$\theta=0:\ 0\quad\ne\quad \theta=\frac{\pi}{2}:\ \tilde{\infty}$$
- Conclusione:  
  $$\textbf{f è continua ma NON differenziabile in (0,0)}$$

**Risposta corretta:** continua, NON differenziabile

#### Esercizio 5
**Testo:** Studiare la continuita' e la differenziabilita' in (0,0) della funzione
f(x,y) = y**4/(x**2 + y**2)  per (x,y) != (0,0),   f(0,0) = 0.
(non sono ammesse maggiorazioni: usare sostituzioni esatte)

$$f(x,y) = \begin{cases} \frac{y^{4}}{x^{2} + y^{2}} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0) \end{cases}$$

**Formato risposta richiesto:** Scrivi: continua,differenziabile  oppure  continua,non differenziabile  oppure  non continua

**Svolgimento passo-passo:**

- Funzione (a tratti, singolare in (0,0)):  
  $$f(x,y) = \frac{y^{4}}{x^{2} + y^{2}}\ \ (\ne(0,0)),\quad f(0,0)=0$$
- Passo 1 — sostituzione in coordinate polari x=r\cosθ, y=r\sinθ:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — il limite è 0 indipendentemente da θ:  
  $$\textbf{f è continua in (0,0)}$$
- Passo 3 — derivate parziali in (0,0) per definizione:  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — studiamo il resto [f-f_x x-f_y y]/r in coordinate polari:
- Il limite per r→0+ è 0 indipendentemente da θ.  
  $$\textbf{f è differenziabile in (0,0)}$$
- Piano tangente in (0,0,0):  
  $$z = 0$$

**Risposta corretta:** continua, differenziabile


### Temi d'esame (problemi reali) (3 esercizi)

#### Esercizio 1
**Testo:** [11 aprile 2026, Esercizio 1] Data la funzione f(x,y) = x·sin(x²+y²)/(x²+y²) + 2x per (x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in (0,0). Determinare, se esiste, il piano tangente alla funzione nel punto (1,0).

$$f(x,y) = \begin{cases}\dfrac{x\sin(x^2+y^2)}{x^2+y^2}+2x & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0)\end{cases}$$

*Fonte: 11 aprile 2026*

**Formato risposta richiesto:** Scrivi: continua,differenziabile

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = \begin{cases}\dfrac{x\sin(x^2+y^2)}{x^2+y^2}+2x & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0)\end{cases}$$
- Passo 1 — sin(t)/t → 1 per t→0, quindi vicino a (0,0) f si comporta come una funzione liscia: sostituendo in polari il limite è 0 uniformemente:  
  $$f(r,\theta) \to 0\ \ (r\to0^+)$$
- Passo 2 — f E' continua in (0,0). Calcoliamo le derivate parziali per definizione:  
  $$f_x(0,0)=3,\quad f_y(0,0)=0$$
- Il resto [f - 3x]/r → 0 (essendo sin(t)/t - 1 = O(t²), quindi il resto è O(r^4)): f E' anche differenziabile in (0,0).
- Passo 3 — nel punto (1,0), lontano dall'origine, f è manifestamente liscia (il denominatore x²+y² non si annulla): calcoliamo il piano tangente con le derivate parziali ordinarie.
- Valori in (1,0):  
  $$f(1,0)=\sin{\left(1 \right)} + 2,\ f_x(1,0)=- \sin{\left(1 \right)} + 2 \cos{\left(1 \right)} + 2,\ f_y(1,0)=0$$
- Piano tangente in (1,0,f(1,0)):  
  $$z = \left(x - 1\right) \left(- \sin{\left(1 \right)} + 2 \cos{\left(1 \right)} + 2\right) + \sin{\left(1 \right)} + 2$$

**Risposta corretta:** continua, differenziabile

#### Esercizio 2
**Testo:** [9 maggio 2026, Esercizio 1] Data la funzione f(x,y) = sin(x²y²)/(x⁴+y²) per (x,y)≠(0,0), f(0,0)=0, studiarne la continuità e la differenziabilità in (0,0) (non sono ammesse maggiorazioni).

$$f(x,y) = \begin{cases}\dfrac{\sin(x^2y^2)}{x^4+y^2} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0)\end{cases}$$

*Fonte: 9 maggio 2026*

**Formato risposta richiesto:** Scrivi: continua,differenziabile

**Svolgimento passo-passo:**

- Funzione:  
  $$f(x,y) = \begin{cases}\dfrac{\sin(x^2y^2)}{x^4+y^2} & (x,y)\ne(0,0) \\ 0 & (x,y)=(0,0)\end{cases}$$
- Passo 1 — poiché |sin(t)| ≤ |t|, si ha |sin(x²y²)| ≤ x²y², quindi:  
  $$\left|\frac{\sin(x^2y^2)}{x^4+y^2}\right| \le \frac{x^2y^2}{x^4+y^2}$$
- Passo 2 — in coordinate polari, x²y²/(x⁴+y²) → 0 per r→0 indipendentemente da θ (si verifica anche lungo il cammino 'pericoloso' y=kx²: il limite resta 0 per ogni k). Quindi f E' continua in (0,0).
- Passo 3 — derivate parziali in (0,0):  
  $$f_x(0,0)=0,\quad f_y(0,0)=0$$
- Passo 4 — il resto f(x,y)/r → 0 anch'esso (stessa maggiorazione, un ordine di r più stringente): f E' anche differenziabile in (0,0).  
  $$\textbf{piano tangente: } z=0$$

**Risposta corretta:** continua, differenziabile

#### Esercizio 3
**Testo:** [6 dicembre 2025, Esercizio 1] Data la funzione f(x,y) = y²(x-2): a) studiare e rappresentare graficamente il segno; b) determinare gli eventuali punti di massimo e minimo utilizzando la matrice Hessiana; c) studiare continuità e differenziabilità; d) determinare, se esiste, il piano tangente in (-1,-2).

$$f(x,y) = y^2(x-2)$$

*Fonte: 6 dicembre 2025*

**Formato risposta richiesto:** Scrivi: continua,differenziabile

**Svolgimento passo-passo:**

- Funzione (polinomiale):  
  $$f(x,y) = y^2(x-2)$$
- Passo a) — segno: y² ≥ 0 sempre, quindi il segno di f dipende solo dal fattore (x-2):  
  $$f\ge0 \iff x\ge2,\qquad f\le0 \iff x\le2,\qquad f=0 \iff x=2 \text{ o } y=0$$
- Passo b) — annulliamo il gradiente per trovare i punti stazionari:  
  $$y^{2}=0,\quad2 y \left(x - 2\right)=0$$
- Il sistema (y²=0, 2y(x-2)=0) impone y=0 per QUALSIASI x: i punti stazionari non sono isolati, ma formano l'intera retta y=0 (caso degenere).
- Matrice Hessiana generale, e ristretta alla retta y=0:  
  $$H(x,y) = \left[\begin{matrix}0 & 2 y\\2 y & 2 x - 4\end{matrix}\right],\quad H(x,0) = \left[\begin{matrix}0 & 0\\0 & 2 x - 4\end{matrix}\right]$$
- Lungo y=0 si ha sempre det H = 0: il test dell'Hessiano NON decide da solo. Studiando il segno direttamente, f(x0,y)-f(x0,0)=y^2(x0-2): per x0>2 è un minimo (debole) locale, per x0<2 un massimo (debole) locale, per x0=2 f è identicamente nulla su entrambe le rette che si incrociano lì (nessun estremo stretto in alcun caso).
- Passo c) — continuità e differenziabilità: f è un POLINOMIO (somma e prodotto di funzioni continue e derivabili con continuità), quindi è automaticamente continua e differenziabile (di classe C^∞) in TUTTO R², incluso (0,0) — a differenza degli esercizi precedenti (funzioni definite a tratti vicino all'origine), qui non serve nessuna analisi di limite.
- Passo d) — piano tangente in (-1,-2): valori di f e delle derivate parziali in quel punto:  
  $$f(-1,-2)=-12,\ f_x(-1,-2)=4,\ f_y(-1,-2)=12$$
- Piano tangente:  
  $$z = 4 x + 12 y + 16$$

**Risposta corretta:** continua, differenziabile

---