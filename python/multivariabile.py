"""
Esercizi su funzioni di piu' variabili: punti critici, Hessiana, moltiplicatori di Lagrange.
"""
import random
import sympy as sp

x, y, lam = sp.symbols('x y lambda')


def genera_punto_critico():
    """Punto critico libero (senza vincoli) e classificazione via Hessiana."""
    a = random.choice([1, 2, 3])
    b = random.choice([1, 2, 3])
    cx = random.choice([-3, -2, -1, 0, 1, 2, 3])
    cy = random.choice([-3, -2, -1, 0, 1, 2, 3])
    segno = random.choice([1, -1])
    f = segno * (a * (x - cx)**2 + b * (y - cy)**2)

    testo = f"Trovare e classificare i punti critici di f(x,y) = {sp.expand(f)}"

    grad = [sp.diff(f, v) for v in (x, y)]
    punti = sp.solve(grad, [x, y], dict=True)
    hess = sp.hessian(f, (x, y))

    classificazioni = []
    for p in punti:
        H = hess.subs(p)
        det = H.det()
        tr = H.trace()
        if det > 0 and tr > 0:
            tipo = 'minimo'
        elif det > 0 and tr < 0:
            tipo = 'massimo'
        elif det < 0:
            tipo = 'sella'
        else:
            tipo = 'indeterminato'
        classificazioni.append({'punto': (p[x], p[y]), 'tipo': tipo})

    return {'testo': testo, 'f': f, 'classificazioni': classificazioni}


def verifica_punto_critico(esercizio, punti_utente):
    """punti_utente: lista di dict {'punto': (x,y), 'tipo': 'minimo'/'massimo'/'sella'}"""
    attesi = {(sp.nsimplify(c['punto'][0]), sp.nsimplify(c['punto'][1])): c['tipo']
              for c in esercizio['classificazioni']}
    ok = True
    dettagli = []
    for pu in punti_utente:
        chiave = (sp.nsimplify(pu['punto'][0]), sp.nsimplify(pu['punto'][1]))
        atteso = attesi.get(chiave)
        match = (atteso == pu['tipo'])
        ok = ok and match
        dettagli.append({'punto': chiave, 'tipo_utente': pu['tipo'], 'tipo_atteso': atteso})
    ok = ok and len(punti_utente) == len(attesi)
    return {'corretto': ok, 'dettagli': dettagli, 'attesi': esercizio['classificazioni']}


def spiega_punto_critico(esercizio):
    """Ricostruisce il calcolo di gradiente, Hessiana e la classificazione dei punti critici."""
    f = esercizio['f']
    grad = [sp.diff(f, v) for v in (x, y)]
    hess = sp.hessian(f, (x, y))
    righe = [
        f"f(x,y) = {sp.expand(f)}",
        "",
        "Passo 1 — annulliamo il gradiente per trovare i punti critici:",
        f"  df/dx = {grad[0]} = 0",
        f"  df/dy = {grad[1]} = 0",
        "",
        "Passo 2 — calcoliamo la matrice Hessiana:",
        f"  H(x,y) = {hess.tolist()}",
        "",
        "Passo 3 — per ogni punto critico valutiamo H e ne studiamo il segno "
        "(det>0 e traccia>0 -> minimo; det>0 e traccia<0 -> massimo; det<0 -> sella):",
    ]
    for c in esercizio['classificazioni']:
        px, py = c['punto']
        H = hess.subs({x: px, y: py})
        righe.append(f"  punto ({px}, {py}):  H = {H.tolist()},  det = {H.det()}, "
                     f"traccia = {H.trace()}   ->   {c['tipo'].upper()}")
    return "\n".join(righe)


def genera_lagrange():
    """Ottimizzazione vincolata: f(x,y) quadratica su retta o circonferenza."""
    a = random.choice([1, 2, 3])
    b = random.choice([1, 2, 3])
    f = a * x**2 + b * y**2

    tipo_vincolo = random.choice(['retta', 'cerchio'])
    vincolo_c = vincolo_r = None
    if tipo_vincolo == 'retta':
        c = random.choice([1, 2, 3, 4])
        g = x + y - c
        vincolo_testo = f"x + y = {c}"
        vincolo_c = c
    else:
        r = random.choice([1, 2, 3])
        g = x**2 + y**2 - r**2
        vincolo_testo = f"x^2 + y^2 = {r**2}"
        vincolo_r = r

    testo = (f"Determinare, con il metodo dei moltiplicatori di Lagrange, i punti stazionari di "
              f"f(x,y) = {sp.expand(f)} vincolati a {vincolo_testo}, e classificare gli eventuali "
              f"estremi assoluti.")

    grad_f = [sp.diff(f, v) for v in (x, y)]
    grad_g = [sp.diff(g, v) for v in (x, y)]
    equazioni = [sp.Eq(grad_f[i], lam * grad_g[i]) for i in range(2)] + [sp.Eq(g, 0)]
    soluzioni = sp.solve(equazioni, [x, y, lam], dict=True)

    punti = []
    for s in soluzioni:
        if x in s and y in s:
            xv, yv = s[x], s[y]
            if xv.is_real and yv.is_real:
                val = f.subs({x: xv, y: yv})
                punti.append((sp.nsimplify(xv), sp.nsimplify(yv), sp.nsimplify(val)))

    # Il vincolo "cerchio" e' un insieme chiuso e limitato (compatto): per Weierstrass f
    # ammette sia massimo sia minimo assoluto. Il vincolo "retta" e' invece illimitato: dato
    # che f = a*x^2 + b*y^2 con a,b>0 tende a +infinito lungo la retta, esiste solo il minimo
    # assoluto, non il massimo (l'estremo superiore e' +infinito ma non e' raggiunto).
    if tipo_vincolo == 'cerchio':
        valore_max = max((p[2] for p in punti), default=None)
    else:
        valore_max = None
    valore_min = min((p[2] for p in punti), default=None)

    return {
        'testo': testo, 'f': f, 'g': g, 'tipo_vincolo': tipo_vincolo,
        'vincolo_c': vincolo_c, 'vincolo_r': vincolo_r, 'punti': punti,
        'valore_max': valore_max, 'valore_min': valore_min,
    }


def spiega_lagrange(esercizio):
    """Ricostruisce il sistema di Lagrange, le sue soluzioni e il confronto finale dei valori."""
    f, g = esercizio['f'], esercizio['g']
    grad_f = [sp.diff(f, v) for v in (x, y)]
    grad_g = [sp.diff(g, v) for v in (x, y)]
    righe = [
        f"f(x,y) = {sp.expand(f)}   vincolo: g(x,y) = {g} = 0",
        "",
        "Passo 1 — impostiamo il sistema di Lagrange: gradiente(f) = lambda * gradiente(g), g = 0.",
        f"  df/dx = {grad_f[0]}      dg/dx = {grad_g[0]}",
        f"  df/dy = {grad_f[1]}      dg/dy = {grad_g[1]}",
        "",
        "Sistema da risolvere:",
        f"  {grad_f[0]} = lambda * ({grad_g[0]})",
        f"  {grad_f[1]} = lambda * ({grad_g[1]})",
        f"  {g} = 0",
        "",
        "Passo 2 — risolvendo il sistema si trovano i punti stazionari (con il valore di f in ciascuno):",
    ]
    for px, py, val in esercizio['punti']:
        righe.append(f"  (x, y) = ({px}, {py})   ->   f(x,y) = {val}")

    righe.append("")
    if esercizio['tipo_vincolo'] == 'cerchio':
        righe.append("Passo 3 — il vincolo e' una circonferenza: un insieme chiuso e limitato "
                     "(compatto). Per il teorema di Weierstrass f ammette sia massimo sia minimo "
                     "assoluto, che si trovano confrontando i valori trovati nei punti stazionari:")
        righe.append(f"  massimo assoluto: f = {esercizio['valore_max']}")
        righe.append(f"  minimo assoluto:  f = {esercizio['valore_min']}")
    else:
        righe.append("Passo 3 — il vincolo e' una retta: un insieme chiuso ma NON limitato. Poiche' "
                     "f e' una forma quadratica con coefficienti positivi, f tende a +infinito "
                     "muovendosi lungo la retta: quindi NON esiste un massimo assoluto (l'estremo "
                     "superiore e' +infinito, ma non e' raggiunto). Esiste pero' il minimo assoluto, "
                     "raggiunto nell'unico punto stazionario trovato:")
        righe.append(f"  minimo assoluto: f = {esercizio['valore_min']}")
        righe.append("  massimo assoluto: non esiste (vincolo illimitato)")
    return "\n".join(righe)


def verifica_lagrange(esercizio, punti_utente):
    """punti_utente: lista di tuple (x,y) come stringhe o numeri."""
    attesi = {(p[0], p[1]) for p in esercizio['punti']}
    forniti = set()
    for px, py in punti_utente:
        forniti.add((sp.nsimplify(sp.sympify(px)), sp.nsimplify(sp.sympify(py))))
    ok = attesi == forniti
    return {
        'corretto': ok,
        'punti_attesi': esercizio['punti'],
        'valore_max': esercizio['valore_max'],
        'valore_min': esercizio['valore_min'],
    }
