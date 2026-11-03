// Piramide interattiva: mattoncini dai fondamentali (base) ai tipi d'esame (vertice).
(function () {
  const R = String.raw;
  // livello: 0 = base ... 5 = vertice. tier: t1 fondamentali, t2 strumenti, t3 tipi d'esame, t4 metodo
  const B = [
    { id: "alg", l: 0, t: "t1", n: "Algebra, disequazioni", req: [],
      f: [R`$a^2-b^2=(a-b)(a+b)$`, R`$x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$`, R`$|A|<B\iff -B<A<B$`, R`$|A|>B\iff A<-B\ \lor\ A>B$`, R`$\dfrac AB>0\iff A,B$ concordi`],
      g: "Ogni dominio e ogni studio del segno si riduce a disequazioni: porta tutto a un lato, scomponi, studia il segno di ogni fattore e componi la tabella dei segni.",
      u: "Domini (radici, log, frazioni), segno di f, punti critici." },
    { id: "exp", l: 0, t: "t1", n: "Potenze, log, exp", req: [],
      f: [R`$\ln(ab)=\ln a+\ln b$`, R`$\ln a^k=k\ln a$`, R`$e^{a+b}=e^ae^b,\quad e^{\ln a}=a$`, R`$e^A>c\iff A>\ln c\quad(c>0)$`, R`$\ln A>c\iff A>e^c$`],
      g: "log ed exp sono una l'inversa dell'altra: per togliere un esponente usa il log, per togliere un log usa l'exp. Il log esiste solo per argomento $>0$.",
      u: "Domini con $\\ln$, EDO a variabili separabili, serie geometriche." },
    { id: "trig", l: 0, t: "t1", n: "Trigonometria", req: [],
      f: [R`$\sin^2x+\cos^2x=1$`, R`$\sin2x=2\sin x\cos x$`, R`$\sin^2x=\tfrac{1-\cos2x}2,\ \cos^2x=\tfrac{1+\cos2x}2$`, R`$\theta=\tfrac\pi6,\tfrac\pi4,\tfrac\pi3:\ \sin=\tfrac12,\tfrac{\sqrt2}2,\tfrac{\sqrt3}2$`],
      g: "Le formule di bisezione abbassano il grado di $\\sin^2,\\cos^2$: indispensabili per integrare in polari.",
      u: "Coordinate polari, integrali di $\\sin^2,\\cos^2$, EDO2 con soluzioni oscillanti." },
    { id: "lim", l: 0, t: "t1", n: "Limiti notevoli", req: [],
      f: [R`$\dfrac{\sin t}t\to1,\quad\dfrac{1-\cos t}{t^2}\to\dfrac12$`, R`$\dfrac{e^t-1}t\to1,\quad\dfrac{\ln(1+t)}t\to1$`, R`$(1+t)^{1/t}\to e\qquad(t\to0)$`],
      g: "Valgono anche con $t=g(x)\\to0$ (es. $\\frac{\\sin x^2}{x^2}\\to1$): riconosci il pezzo che tende a zero e sostituiscilo.",
      u: "Confronto asintotico nelle serie, continuità, limiti in due variabili." },
    { id: "der", l: 0, t: "t1", n: "Derivate base", req: [],
      f: [R`$(x^\alpha)'=\alpha x^{\alpha-1},\ (e^x)'=e^x$`, R`$(\ln x)'=\tfrac1x,\ (\sin x)'=\cos x$`, R`$(\cos x)'=-\sin x,\ (\arctan x)'=\tfrac1{1+x^2}$`],
      g: "La tabella va saputa a memoria: tutte le regole successive la combinano.",
      u: "Gradiente, Hessiano, EDO." },
    { id: "int", l: 0, t: "t1", n: "Integrali base", req: [],
      f: [R`$\int x^\alpha=\tfrac{x^{\alpha+1}}{\alpha+1}\ (\alpha\ne-1),\ \int\tfrac1x=\ln|x|$`, R`$\int e^{\lambda x}=\tfrac{e^{\lambda x}}\lambda,\ \int\tfrac{f'}f=\ln|f|$`, R`$\int\tfrac1{1+x^2}=\arctan x$`],
      g: "Prima di cercare trucchi controlla se l'integrando è nella tabella o è del tipo $f'/f$.",
      u: "EDO, integrali doppi." },

    { id: "regole", l: 1, t: "t2", n: "Derivazione", req: ["der"],
      f: [R`$(fg)'=f'g+fg'$`, R`$\left(\tfrac fg\right)'=\dfrac{f'g-fg'}{g^2}$`, R`$\big(f(g)\big)'=f'(g)\,g'$`],
      g: "Derivata composta: deriva da fuori a dentro, moltiplicando. Per $f^g$ usa $f^g=e^{g\\ln f}$.",
      u: "Punti stazionari, equazioni di Cauchy." },
    { id: "parti", l: 1, t: "t2", n: "Per parti, sostituzione", req: ["int", "regole"],
      f: [R`$\int fg'=fg-\int f'g$`, R`$t=g(x),\ dt=g'(x)dx$`, R`$\int xe^x=xe^x-e^x$`],
      g: "Per parti: $f$ è ciò che si semplifica derivando (polinomio, $\\ln$), $g'$ ciò che resta integrabile ($e^x,\\sin,\\cos$). Sostituzione: cerca dentro l'integrale una funzione e la sua derivata.",
      u: "EDO lineari, integrali doppi." },
    { id: "fratti", l: 1, t: "t2", n: "Fratti semplici", req: ["alg", "int"],
      f: [R`$\dfrac1{(x-a)(x-b)}=\dfrac A{x-a}+\dfrac B{x-b}$`, R`$A=\big[(x-a)f(x)\big]_{x=a}$`, R`$\dfrac{Ax+B}{x^2+\beta^2}$ (irriducibile)`, R`$\dfrac1{(1-y)(2-y)}=\dfrac1{1-y}-\dfrac1{2-y}$`],
      g: "Regola del coprire: per trovare $A$ copri il fattore $(x-a)$ e valuta il resto in $x=a$.",
      u: "EDO a variabili separabili, serie telescopiche." },
    { id: "quad", l: 1, t: "t2", n: "Completare il quadrato", req: ["alg"],
      f: [R`$x^2+px=\left(x+\tfrac p2\right)^2-\tfrac{p^2}4$`, R`$x^2+y^2+2x=0\iff(x+1)^2+y^2=1$`],
      g: "Raccogli i termini in $x$ e in $y$ separatamente e completa: leggi subito centro e raggi.",
      u: "Riconoscere coniche, disegnare vincoli e domini." },
    { id: "det", l: 1, t: "t2", n: "Determinanti", req: ["alg"],
      f: [R`$\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc$`, R`Sarrus: $(aei+bfg+cdh)-(ceg+afh+bdi)$`, R`Laplace: sviluppa sulla riga/colonna con più zeri`],
      g: "Nel $3\\times3$ ricopia le prime due colonne a destra: diagonali discendenti $+$, ascendenti $-$.",
      u: "$\\det H$ e determinante dell'Hessiano orlato." },

    { id: "coniche", l: 2, t: "t2", n: "Curve e coniche", req: ["quad", "alg"],
      f: [R`Circonferenza: $(x-x_0)^2+(y-y_0)^2=r^2$`, R`Ellisse: $\tfrac{x^2}{a^2}+\tfrac{y^2}{b^2}=1$, area $\pi ab$`, R`Iperbole: $\tfrac{x^2}{a^2}-\tfrac{y^2}{b^2}=\pm1$, asintoti $y=\pm\tfrac bax$`, R`Parabola: vertice $x_v=-\tfrac b{2a}$`],
      g: "Senza termine $xy$: $A,B$ stesso segno $\\Rightarrow$ ellisse, segno opposto $\\Rightarrow$ iperbole, uno nullo $\\Rightarrow$ parabola. Circonferenza ed ellisse sono compatte, le altre no.",
      u: "Vincoli di Lagrange, domini, Weierstrass." },
    { id: "taylor", l: 2, t: "t2", n: "Taylor / Mac Laurin", req: ["der", "lim"],
      f: [R`$e^x=\sum\tfrac{x^n}{n!}$`, R`$\sin x=x-\tfrac{x^3}6+\dots,\ \cos x=1-\tfrac{x^2}2+\dots$`, R`$\ln(1+x)=x-\tfrac{x^2}2+\dots$`, R`$\tfrac1{1-x}=\sum x^n$`],
      g: "Sostituisci l'argomento nello sviluppo noto e tronca all'ordine richiesto, scrivendo il resto $o(x^n)$.",
      u: "Limiti, serie di potenze, natura dei punti con $H=0$." },
    { id: "parz", l: 2, t: "t2", n: "Derivate parziali, Hessiano", req: ["regole", "der"],
      f: [R`$\nabla f=(f_x,f_y)$`, R`$H=\begin{pmatrix}f_{xx}&f_{xy}\\f_{xy}&f_{yy}\end{pmatrix}$, $\det H=f_{xx}f_{yy}-f_{xy}^2$`, R`$f_x(0,0)=\lim_{h\to0}\tfrac{f(h,0)-f(0,0)}h$`],
      g: "Derivando in $x$ tratta $y$ come costante (e viceversa). Nell'origine, se la formula non è valida, usa la definizione.",
      u: "Stazionari, piano tangente, differenziabilità." },
    { id: "polari", l: 2, t: "t2", n: "Polari e disegno domini", req: ["trig", "coniche"],
      f: [R`$x=r\cos\theta,\ y=r\sin\theta,\ dx\,dy=r\,dr\,d\theta$`, R`Ellisse: $x=x_0+ar\cos\theta,\ y=y_0+br\sin\theta$, $dx\,dy=ab\,r\,dr\,d\theta$`],
      g: "Disegno: ogni disequazione diventa un'equazione (curva), prova un punto per scegliere il lato, colora l'intersezione. Poi leggi gli estremi.",
      u: "Integrali doppi, continuità in $(0,0)$." },

    { id: "serie", l: 3, t: "t3", n: "Serie numeriche", req: ["lim", "taylor", "exp", "alg"],
      f: [R`$a_n\not\to0\Rightarrow$ diverge`, R`Rapporto: $L=\lim\tfrac{a_{n+1}}{a_n}$; $L<1$ conv., $L>1$ div.`, R`Confronto asintotico: $a_n\sim b_n\Rightarrow$ stesso carattere`, R`Leibniz: $b_n\downarrow0\Rightarrow\sum(-1)^nb_n$ conv.`, R`$\sum q^n=\tfrac1{1-q}\ (|q|<1)$; telescopica: $S_N=$ primo $-$ ultimo`],
      g: "Prima: $a_n\\to0$? poi riconosci la forma (geometrica, telescopica); altrimenti criterio. Nomina sempre il criterio usato.",
      u: "Carattere, somma, convergenza al variare di un parametro." },
    { id: "cont", l: 3, t: "t3", n: "Continuità, piano tangente", req: ["polari", "lim", "parz"],
      f: [R`Continuità in $0$: $\lim F(r,\theta)=L$ per ogni $\theta$ (uniforme)`, R`Differenziabile: $\tfrac{f-f(0)-f_xx-f_yy}{\sqrt{x^2+y^2}}\to0$`, R`Piano: $z=f(P)+f_x(x-x_0)+f_y(y-y_0)$`],
      g: "Passa in polari: se il limite dipende da $\\theta$ non esiste. Piano tangente esiste solo se $f$ è differenziabile.",
      u: "Segno, dominio, continuità, differenziabilità." },
    { id: "liberi", l: 3, t: "t3", n: "Max/min liberi", req: ["parz", "det", "regole"],
      f: [R`$\nabla f=0$`, R`$\det H>0,\ f_{xx}>0$: min; $\det H>0,\ f_{xx}<0$: max`, R`$\det H<0$: sella; $\det H=0$: studia $f-f(P)$`],
      g: "Risolvi il sistema fattorizzando; classifica ogni punto con $H$; ricorda i punti sul bordo del dominio.",
      u: "Punti stazionari e loro natura." },
    { id: "edo1", l: 3, t: "t3", n: "EDO 1° ordine", req: ["fratti", "parti", "exp"],
      f: [R`Separabile: $\int\tfrac{dy}{h(y)}=\int g(x)\,dx$`, R`Lineare $y'+py=q$: $y=e^{-P}\left(\int qe^{P}dx+c\right)$, $P=\int p$`, R`Bernoulli $y'+py=qy^n$: $v=y^{1-n}$`],
      g: "Classifica prima (separabile / lineare / Bernoulli). Per Cauchy imposta la costante solo alla fine.",
      u: "Soluzione generale e problema di Cauchy." },

    { id: "vinc", l: 4, t: "t3", n: "Vincolati (Lagrange)", req: ["liberi", "coniche", "det"],
      f: [R`$\mathcal L=f-\lambda g$; $\nabla f=\lambda\nabla g,\ g=0$`, R`$\overline H=\begin{pmatrix}0&g_x&g_y\\g_x&\mathcal L_{xx}&\mathcal L_{xy}\\g_y&\mathcal L_{xy}&\mathcal L_{yy}\end{pmatrix}$`, R`$\det\overline H>0\Rightarrow$ max; $<0\Rightarrow$ min`],
      g: "Vincolo compatto: Weierstrass garantisce max e min, confronta i valori di $f$ nei candidati. Controlla i punti con $\\nabla g=0$.",
      u: "Estremi di $f$ su una curva." },
    { id: "doppi", l: 4, t: "t3", n: "Integrali doppi", req: ["polari", "parti", "int"],
      f: [R`$\iint_Df=\int_a^b\!\!\int_{\alpha(x)}^{\beta(x)}f\,dy\,dx$`, R`Polari: $\iint f\,r\,dr\,d\theta$`, R`Area $=\iint_D1$`],
      g: "Disegno obbligatorio. Se l'integrale interno non si fa, scambia l'ordine. Domini con $\\min/\\max$: spezza.",
      u: "Volumi, aree, integrali su domini da disequazioni." },
    { id: "edo2", l: 4, t: "t3", n: "EDO 2° ordine", req: ["alg", "regole", "exp"],
      f: [R`$r^2+pr+q=0$`, R`$\Delta>0$: $c_1e^{r_1x}+c_2e^{r_2x}$; $\Delta=0$: $(c_1+c_2x)e^{rx}$`, R`$\Delta<0$: $e^{\alpha x}(c_1\cos\beta x+c_2\sin\beta x)$`, R`$y=y_{om}+y_p$; risonanza: $y_p\cdot x^m$`],
      g: "Risolvi l'omogenea, poi $y_p$ per somiglianza con $f$; se $f$ risolve l'omogenea, moltiplica per $x$.",
      u: "Integrale generale e Cauchy." },

    { id: "metodo", l: 5, t: "t4", n: "Metodo d'esame", req: ["serie", "cont", "liberi", "edo1", "vinc", "doppi", "edo2"],
      f: [R`1) classifica dal testo; 2) scaletta del tipo; 3) mostra i passaggi; 4) verifica (sostituisci, deriva, segno, dominio)`],
      g: "Circa 25 minuti a esercizio. Parti da quello che conosci meglio, scrivi sempre il criterio o il teorema usato.",
      u: "Gestione del tempo e della consegna." },
  ];
  const byId = Object.fromEntries(B.map((b) => [b.id, b]));
  const KEY = "mm_pir_v1";
  let done = {};
  try { done = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {} };

  function render(root) {
    root.innerHTML = "";
    const pyr = document.createElement("div"); pyr.className = "pir";
    const sel = pyr.dataset;
    for (let l = 5; l >= 0; l--) {
      const row = document.createElement("div"); row.className = "pir-row";
      B.filter((b) => b.l === l).forEach((b) => {
        const el = document.createElement("button");
        el.type = "button"; el.className = "pir-brick " + b.t + (done[b.id] ? " done" : "");
        el.dataset.id = b.id; el.textContent = b.n;
        row.appendChild(el);
      });
      pyr.appendChild(row);
    }
    const det = document.createElement("div"); det.className = "pir-detail"; det.id = "pir-detail";
    det.innerHTML = '<p class="pir-hint">Tocca un mattoncino: vedi formule, logica e a cosa serve. Si illuminano i mattoni che servono per capirlo.</p>';
    const prog = document.createElement("div"); prog.className = "pir-prog"; prog.id = "pir-prog";
    root.append(prog, pyr, det);
    pyr.addEventListener("click", (e) => {
      const b = e.target.closest(".pir-brick"); if (b) apri(b.dataset.id, root);
    });
    aggiornaProgresso();
  }

  function aggiornaProgresso() {
    const p = document.getElementById("pir-prog"); if (!p) return;
    const n = B.filter((b) => done[b.id]).length;
    p.textContent = "Mattoncini studiati: " + n + " / " + B.length;
  }

  function ricorsivi(id, acc) {
    byId[id].req.forEach((r) => { if (!acc.has(r)) { acc.add(r); ricorsivi(r, acc); } });
    return acc;
  }

  function apri(id, root) {
    const esc = (x) => x.replace(/</g, "&lt;");
    const b = byId[id], need = ricorsivi(id, new Set());
    root.querySelectorAll(".pir-brick").forEach((el) => {
      el.classList.toggle("sel", el.dataset.id === id);
      el.classList.toggle("need", need.has(el.dataset.id));
      el.classList.toggle("dim", el.dataset.id !== id && !need.has(el.dataset.id));
    });
    const det = document.getElementById("pir-detail");
    const chips = b.req.map((r) => '<button type="button" class="pir-chip" data-go="' + r + '">' + byId[r].n + "</button>").join("");
    det.className = "pir-detail " + b.t;
    det.innerHTML =
      "<h3>" + b.n + "</h3>" +
      '<div class="pir-sec">Formule</div><ul>' + b.f.map((x) => "<li>" + esc(x) + "</li>").join("") + "</ul>" +
      '<div class="pir-sec">Logica</div><p>' + esc(b.g) + "</p>" +
      '<div class="pir-sec">Applicazioni</div><p>' + esc(b.u) + "</p>" +
      (chips ? '<div class="pir-sec">Prima di questo ti servono</div><div class="pir-chips">' + chips + "</div>" : "") +
      '<div class="pir-actions"><button type="button" class="btn" id="pir-done">' + (done[id] ? "Segna da ripassare" : "Segna come studiato") + '</button>' +
      (b.t === "t3" || b.t === "t4" ? '<a href="#" class="btn secondary" data-goto="esercizi">Vai agli esercizi</a>' : "") +
      '<a href="#" class="btn secondary" data-goto="formulario">Formulario</a></div>';
    if (typeof renderMathInElement === "function") {
      renderMathInElement(det, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }], throwOnError: false });
    }
    det.querySelector("#pir-done").onclick = () => {
      done[id] = !done[id]; save();
      root.querySelector('.pir-brick[data-id="' + id + '"]').classList.toggle("done", !!done[id]);
      det.querySelector("#pir-done").textContent = done[id] ? "Segna da ripassare" : "Segna come studiato";
      aggiornaProgresso();
    };
    det.querySelectorAll("[data-go]").forEach((c) => (c.onclick = () => apri(c.dataset.go, root)));
    det.scrollIntoView && det.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const root = document.getElementById("pir-root");
    if (root) render(root);
  });
})();
