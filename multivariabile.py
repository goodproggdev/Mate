"""
Esercizi su funzioni di piu' variabili: punti critici, Hessiana, moltiplicatori di Lagrange.
"""
import random
import sympy as sp

x, y, lam = sp.symbols('x y lambda')


# Banco curato di funzioni per i punti stazionari liberi (Hessiana, senza vincolo):
# 'facile' sono quadratiche diagonali (un solo punto, lettura diretta del segno);
# 'medio' aggiungono un termine misto x*y (serve calcolare il determinante); 'difficile'
# sono cubiche/quartiche con piu' punti stazionari di tipo diverso (sella+estremo), il
# caso piu' frequente nei test d'esame reali. Ogni funzione e' verificata: i punti
# critici reali e la loro classificazione via Hessiana sono calcolati qui, non a mano.
_POOLS_PUNTI_LIBERI = {
    'facile': [
        (x - 0)**2 + (y - 0)**2,
        2 * (x - 1)**2 + (y + 1)**2,
        -(x + 2)**2 - 2 * y**2,
        3 * x**2 + (y - 2)**2,
        -(x - 1)**2 - (y - 1)**2,
    ],
    'medio': [
        x**2 + y**2 - 3 * x * y,
        x**2 + y**2 - x * y,
        (x - 1)**2 - (y + 2)**2,
        2 * x**2 + 3 * y**2 - 4 * x * y,
        x**2 - y**2 + 2 * x - 4 * y + 3,
    ],
    'difficile': [
        x**3 + y**3 - 3 * x * y,
        x**3 + y**3 - 6 * x * y,
        x**3 + y**3 - 9 * x * y,
        x**3 - 3 * x * y**2,
        x**4 + y**4 - 4 * x * y,
    ],
}


def _classifica_punti_critici(f, punti_grezzi):
    hess = sp.hessian(f, (x, y))
    classificazioni = []
    for p in punti_grezzi:
        xv, yv = p[x], p[y]
        if not (xv.is_real and yv.is_real):
            continue
        H = hess.subs(p)
        det = sp.simplify(H.det())
        tr = sp.simplify(H.trace())
        if det > 0 and tr > 0:
            tipo = 'minimo'
        elif det > 0 and tr < 0:
            tipo = 'massimo'
        elif det < 0:
            tipo = 'sella'
        else:
            tipo = 'indeterminato'
        classificazioni.append({'punto': (xv, yv), 'tipo': tipo})
    return classificazioni


def genera_punto_critico(difficolta='medio', indice=0):
    """Punto/i critico/i libero/i (senza vincoli) e classificazione via Hessiana.
    Banco curato (non casuale): 'indice' (0..4) sceglie quale delle 5 funzioni
    verificate per quella difficolta' usare, cosi' il banco statico precalcolato
    contiene sempre esattamente 5 esercizi distinti e corretti per livello."""
    pool = _POOLS_PUNTI_LIBERI.get(difficolta, _POOLS_PUNTI_LIBERI['medio'])
    f = pool[indice % len(pool)]

    testo = f"Trovare e classificare i punti stazionari di f(x,y) = {sp.expand(f)}"

    grad = [sp.diff(f, v) for v in (x, y)]
    punti_grezzi = sp.solve(grad, [x, y], dict=True)
    classificazioni = _classifica_punti_critici(f, punti_grezzi)

    return {'testo': testo, 'f': f, 'difficolta': difficolta, 'indice': indice,
            'classificazioni': classificazioni}


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


_POOLS_LAGRANGE = {
    'facile': {'tipi': ['cerchio'], 'ab': [1, 2, 3], 'c': [1, 2], 'r': [1, 2]},
    'medio': {'tipi': ['retta', 'cerchio'], 'ab': [1, 2, 3], 'c': [1, 2, 3, 4], 'r': [1, 2, 3]},
    'difficile': {'tipi': ['retta', 'cerchio'], 'ab': [1, 2, 3, 4, 5], 'c': [3, 4, 5, 6, 7], 'r': [2, 3, 4]},
}


def genera_lagrange(difficolta='medio'):
    """Ottimizzazione vincolata: f(x,y) quadratica su retta o circonferenza."""
    pool = _POOLS_LAGRANGE.get(difficolta, _POOLS_LAGRANGE['medio'])
    a = random.choice(pool['ab'])
    b = random.choice(pool['ab'])
    f = a * x**2 + b * y**2

    tipo_vincolo = random.choice(pool['tipi'])
    vincolo_c = vincolo_r = None
    if tipo_vincolo == 'retta':
        c = random.choice(pool['c'])
        g = x + y - c
        vincolo_testo = f"x + y = {c}"
        vincolo_c = c
    else:
        r = random.choice(pool['r'])
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
    lambda_per_punto = []
    for s in soluzioni:
        if x in s and y in s:
            xv, yv = s[x], s[y]
            if xv.is_real and yv.is_real:
                val = f.subs({x: xv, y: yv})
                punti.append((sp.nsimplify(xv), sp.nsimplify(yv), sp.nsimplify(val)))
                lambda_per_punto.append(sp.nsimplify(s.get(lam, sp.Integer(0))))

    # Il vincolo "cerchio" e' un insieme chiuso e limitato (compatto): per Weierstrass f
    # ammette sia massimo sia minimo assoluto. Il vincolo "retta" e' invece illimitato: dato
    # che f = a*x^2 + b*y^2 con a,b>0 tende a +infinito lungo la retta, esiste solo il minimo
    # assoluto, non il massimo (l'estremo superiore e' +infinito ma non e' raggiunto).
    if tipo_vincolo == 'cerchio':
        valore_max = max((p[2] for p in punti), default=None)
    else:
        valore_max = None
    valore_min = min((p[2] for p in punti), default=None)

    classificazioni_orlato = [_classifica_hessiana_orlata(f, g, px, py, lv)
                               for (px, py, _), lv in zip(punti, lambda_per_punto)]

    return {
        'testo': testo, 'f': f, 'g': g, 'tipo_vincolo': tipo_vincolo, 'difficolta': difficolta,
        'vincolo_c': vincolo_c, 'vincolo_r': vincolo_r, 'punti': punti,
        'lambda_per_punto': lambda_per_punto, 'classificazioni_orlato': classificazioni_orlato,
        'valore_max': valore_max, 'valore_min': valore_min,
    }


def _classifica_hessiana_orlata(f, g, px, py, lam_v):
    """Hessiano orlato (bordered Hessian) nel punto stazionario vincolato (px,py) con
    moltiplicatore lam_v: H_bar = [[0,gx,gy],[gx,Lxx,Lxy],[gy,Lxy,Lyy]] dove L=f-lambda*g.
    Per il formulario ufficiale: det(H_bar)>0 => massimo vincolato (relativo);
    det(H_bar)<0 => minimo vincolato (relativo); det(H_bar)=0 => non si puo' dire."""
    gx, gy = sp.diff(g, x), sp.diff(g, y)
    L = f - lam * g
    Lxx, Lyy, Lxy = sp.diff(L, x, 2), sp.diff(L, y, 2), sp.diff(L, x, y)
    H_bar = sp.Matrix([[0, gx, gy], [gx, Lxx, Lxy], [gy, Lxy, Lyy]])
    H_bar_val = H_bar.subs({x: px, y: py, lam: lam_v})
    det = sp.simplify(H_bar_val.det())
    if det > 0:
        tipo = 'massimo relativo vincolato'
    elif det < 0:
        tipo = 'minimo relativo vincolato'
    else:
        tipo = 'indeterminato (H orlato nullo)'
    return {'matrice': H_bar_val, 'det': det, 'tipo': tipo}


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
    righe.append("Passo 3 — classifichiamo OGNI punto stazionario con l'Hessiano orlato (matrice "
                 "bordata), come richiesto dal formulario: posto L(x,y,lambda)=f(x,y)-lambda*g(x,y),")
    righe.append("  H_bar = [[0, g'x, g'y], [g'x, L''xx, L''xy], [g'y, L''yx, L''yy]]")
    righe.append("  det(H_bar)>0 -> massimo relativo vincolato;  det(H_bar)<0 -> minimo relativo "
                 "vincolato;  det(H_bar)=0 -> indeterminato.")
    for (px, py, val), lam_v, cl in zip(esercizio['punti'], esercizio['lambda_per_punto'],
                                          esercizio['classificazioni_orlato']):
        righe.append(f"  punto ({px}, {py}), lambda={lam_v}:  det(H_bar) = {cl['det']}   ->   "
                     f"{cl['tipo'].upper()}")

    righe.append("")
    if esercizio['tipo_vincolo'] == 'cerchio':
        righe.append("Passo 4 — il vincolo e' una circonferenza: un insieme chiuso e limitato "
                     "(compatto). Per il teorema di Weierstrass f ammette sia massimo sia minimo "
                     "assoluto: si trovano confrontando i valori di f in TUTTI i punti stazionari "
                     "(anche quelli classificati come relativi dall'Hessiano orlato, perche' un "
                     "massimo/minimo relativo non e' detto sia anche quello assoluto):")
        righe.append(f"  massimo assoluto: f = {esercizio['valore_max']}")
        righe.append(f"  minimo assoluto:  f = {esercizio['valore_min']}")
    else:
        righe.append("Passo 4 — il vincolo e' una retta: un insieme chiuso ma NON limitato. Poiche' "
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
