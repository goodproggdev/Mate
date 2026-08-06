"""
Rappresentazioni grafiche degli esercizi (matplotlib), per visualizzare il problema
prima o dopo averlo risolto: curve di livello, vincoli, domini di integrazione,
funzione vs sviluppo di Taylor, somme parziali di una serie, soluzione di un'EDO.

Ogni funzione grafico_X(esercizio) restituisce una matplotlib Figure: il chiamante
decide se mostrarla (plt.show(), da CLI) o incorporarla in una finestra (GUI).

Nota su "2D vs 3D": in questo esercizio ci sono due famiglie di funzioni.
- serie, taylor, edo, integrali: il problema E' genuinamente 2D (una sequenza, una
  funzione di una variabile, o una regione del piano). Il grafico e' quindi 2D.
- lagrange, punto_critico: f(x,y) e' una SUPERFICIE nello spazio (z=f(x,y)), quindi
  qui si disegnano DUE viste affiancate: una superficie 3D vera e propria, e la sua
  proiezione dall'alto (curve di livello), che e' il modo standard con cui si
  rappresenta un problema di questo tipo su carta durante l'esame.
"""
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registra la projection='3d')

import serie as serie_mod
import taylor as taylor_mod
import multivariabile as mv_mod
import edo as edo_mod


def _didascalia(fig, testo):
    """Aggiunge una didascalia in corsivo sotto il grafico, riservando spazio in base
    al numero di righe del testo (altrimenti rischia di sovrapporsi agli assi)."""
    n_righe = testo.count('\n') + 1
    margine_basso = 0.03 + 0.038 * n_righe
    fig.text(0.5, 0.012, testo, ha='center', va='bottom', fontsize=8.5,
              style='italic', color='#444444', wrap=True)
    fig.tight_layout(rect=(0, margine_basso, 1, 1))


def grafico_serie(esercizio, n_termini=40):
    """Somme parziali S_n della serie, per vedere a occhio se si stabilizzano o esplodono."""
    n = serie_mod.n
    f_num = sp.lambdify(n, esercizio['termine_generale'], 'numpy')
    ns = np.arange(1, n_termini + 1, dtype=float)  # float: evita "int a potenza negativa" con numpy
    valori = np.array([float(f_num(k)) for k in ns])
    parziali = np.cumsum(valori)

    fig, ax = plt.subplots(figsize=(6, 4.4))
    ax.plot(ns, parziali, marker='o', markersize=3, linewidth=1, color='#2e5c8a')
    ax.set_yscale('symlog')
    ax.axhline(0, color='gray', linewidth=0.7)
    stato = 'CONVERGENTE' if esercizio['converge'] else 'DIVERGENTE'
    ax.set_title(f"Somme parziali S_n = a_1+...+a_n  ({stato})")
    ax.set_xlabel('n')
    ax.set_ylabel('S_n  (scala symlog)')
    _didascalia(fig, "Ogni punto e' la somma dei primi n termini. Se la linea si stabilizza\n"
                     "attorno a un valore, la serie converge; se continua a crescere (in valore\n"
                     "assoluto) senza fermarsi, diverge.")
    return fig


_DOMINI_TAYLOR = None


def _dominio_taylor(f_expr):
    global _DOMINI_TAYLOR
    x = taylor_mod.x
    if _DOMINI_TAYLOR is None:
        _DOMINI_TAYLOR = [
            (sp.exp(x), (-3, 3)),
            (sp.sin(x), (-3, 3)),
            (sp.cos(x), (-3, 3)),
            (sp.log(1 + x), (-0.9, 3)),
            (1 / (1 - x), (-3, 0.9)),
            (sp.sqrt(1 + x), (-0.9, 4)),
        ]
    for candidato, rng in _DOMINI_TAYLOR:
        if sp.simplify(f_expr - candidato) == 0:
            return rng
    return (-2, 2)


def _valuta(f_num, xs):
    """Valuta f_num sull'array xs, gestendo il caso limite in cui il risultato sia
    costante (sympy/numpy a volte restituiscono uno scalare invece di un array)."""
    with np.errstate(all='ignore'):
        ys = np.asarray(f_num(xs), dtype=float)
    if ys.shape != xs.shape:
        ys = np.broadcast_to(ys, xs.shape).copy()
    return ys


def _ylim_range(ys):
    finite = ys[np.isfinite(ys)]
    if finite.size == 0:
        return (-5, 5)
    lo, hi = float(np.min(finite)), float(np.max(finite))
    pad = 0.15 * (hi - lo) + 1e-6
    return (lo - pad, hi + pad)


def grafico_taylor(esercizio):
    """Confronta f(x) con il polinomio di Taylor P_n(x) nell'intorno di x0."""
    x = taylor_mod.x
    f_expr = esercizio['funzione']
    x0 = esercizio['x0']
    poly = esercizio['sviluppo_atteso']
    xmin, xmax = _dominio_taylor(f_expr)

    xs = np.linspace(xmin, xmax, 400)
    f_num = sp.lambdify(x, f_expr, 'numpy')
    p_num = sp.lambdify(x, poly, 'numpy')
    ys_f = _valuta(f_num, xs)
    ys_p = _valuta(p_num, xs)

    fig, ax = plt.subplots(figsize=(6, 4.4))
    ax.plot(xs, ys_f, linewidth=2, label=f"f(x) = {f_expr}")
    ax.plot(xs, ys_p, '--', linewidth=2, color='#c0392b', label=f"P_{esercizio['ordine']}(x)")
    ax.axvline(x0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_ylim(_ylim_range(ys_f))
    ax.set_title("Funzione vs polinomio di Taylor")
    ax.legend()
    _didascalia(fig, "La curva blu e' la funzione vera, quella rossa tratteggiata e' la sua\n"
                     "approssimazione polinomiale attorno a x0: piu' ci si allontana da x0,\n"
                     "piu' le due curve si separano (l'approssimazione peggiora).")
    return fig


def grafico_lagrange(esercizio):
    """Superficie z=f(x,y) in 3D + curve di livello con vincolo, affiancate."""
    x, y = mv_mod.x, mv_mod.y
    f_expr = esercizio['f']
    punti = esercizio['punti']

    xs_pts = [float(p[0]) for p in punti] or [0.0]
    ys_pts = [float(p[1]) for p in punti] or [0.0]
    margin = 2.5
    xmin, xmax = min(xs_pts) - margin, max(xs_pts) + margin
    ymin, ymax = min(ys_pts) - margin, max(ys_pts) + margin

    X, Y = np.meshgrid(np.linspace(xmin, xmax, 80), np.linspace(ymin, ymax, 80))
    f_num = sp.lambdify((x, y), f_expr, 'numpy')
    Z = f_num(X, Y)

    if esercizio['tipo_vincolo'] == 'retta':
        c = esercizio['vincolo_c']
        t = np.linspace(xmin, xmax, 200)
        vx, vy = t, c - t
        etichetta_vincolo = f"vincolo: x+y={c}"
    else:
        r = esercizio['vincolo_r']
        theta = np.linspace(0, 2 * np.pi, 200)
        vx, vy = r * np.cos(theta), r * np.sin(theta)
        etichetta_vincolo = f"vincolo: x²+y²={r**2}"
    vz = f_num(vx, vy)

    fig = plt.figure(figsize=(11, 5.5))

    # --- vista 3D: la superficie e il vincolo "srotolato" sulla superficie ---
    ax3d = fig.add_subplot(1, 2, 1, projection='3d')
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, linewidth=0, antialiased=True)
    ax3d.plot(vx, vy, vz, color='#c0392b', linewidth=2.5, label=etichetta_vincolo)
    for px, py, val in punti:
        ax3d.scatter([float(px)], [float(py)], [float(val)], color='black', s=40)
    ax3d.set_xlabel('x')
    ax3d.set_ylabel('y')
    ax3d.set_zlabel('f(x,y)')
    ax3d.set_title("Superficie z=f(x,y) e vincolo")

    # --- vista dall'alto: curve di livello (proiezione 2D della superficie) ---
    ax2d = fig.add_subplot(1, 2, 2)
    cs = ax2d.contour(X, Y, Z, levels=12, cmap='viridis', linewidths=0.9)
    ax2d.clabel(cs, inline=True, fontsize=7)
    ax2d.plot(vx, vy, color='#c0392b', linewidth=2, label=etichetta_vincolo)
    for px, py, val in punti:
        pxf, pyf = float(px), float(py)
        ax2d.plot(pxf, pyf, 'ko', markersize=7)
        ax2d.annotate(f"f={val}", (pxf, pyf), textcoords="offset points", xytext=(7, 7), fontsize=8)
    ax2d.set_title("Vista dall'alto: curve di livello")
    ax2d.set_aspect('equal', 'box')
    ax2d.legend(loc='upper right', fontsize=8)

    _didascalia(fig, "A sinistra: la superficie z=f(x,y) vista in 3D, con il vincolo g=0 \"srotolato\"\n"
                     "sulla superficie (curva rossa) e i punti stazionari trovati (pallini neri).\n"
                     "A destra: la stessa cosa vista dall'alto — le curve colorate sono sezioni\n"
                     "orizzontali della superficie a quota costante (curve di livello).")
    return fig


def grafico_punto_critico(esercizio):
    """Superficie z=f(x,y) in 3D + curve di livello, affiancate, con la classificazione del punto."""
    x, y = mv_mod.x, mv_mod.y
    f_expr = esercizio['f']
    c = esercizio['classificazioni'][0]
    cx, cy = float(c['punto'][0]), float(c['punto'][1])
    margin = 3
    X, Y = np.meshgrid(np.linspace(cx - margin, cx + margin, 80), np.linspace(cy - margin, cy + margin, 80))
    f_num = sp.lambdify((x, y), f_expr, 'numpy')
    Z = f_num(X, Y)
    cz = float(f_num(cx, cy))

    fig = plt.figure(figsize=(11, 5.5))

    ax3d = fig.add_subplot(1, 2, 1, projection='3d')
    ax3d.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.75, linewidth=0, antialiased=True)
    ax3d.scatter([cx], [cy], [cz], color='black', s=50)
    ax3d.set_xlabel('x')
    ax3d.set_ylabel('y')
    ax3d.set_zlabel('f(x,y)')
    ax3d.set_title(f"Superficie z=f(x,y)  —  {c['tipo'].upper()}")

    ax2d = fig.add_subplot(1, 2, 2)
    cs = ax2d.contourf(X, Y, Z, levels=20, cmap='coolwarm')
    fig.colorbar(cs, ax=ax2d, shrink=0.8)
    ax2d.plot(cx, cy, 'ko', markersize=8)
    ax2d.annotate(c['tipo'].upper(), (cx, cy), textcoords="offset points", xytext=(8, 8),
                  fontsize=9, fontweight='bold')
    ax2d.set_title("Vista dall'alto: curve di livello")
    ax2d.set_aspect('equal', 'box')

    spiegazioni = {
        'minimo': "una \"conca\": il punto e' il fondo della valle.",
        'massimo': "una \"cupola\": il punto e' la cima del colle.",
        'sella': "una sella: sale in una direzione e scende nell'altra.",
        'indeterminato': "un caso limite: l'Hessiano da solo non basta a deciderlo.",
    }
    _didascalia(fig, f"A sinistra: la superficie z=f(x,y) in 3D — vicino al punto trovato ha la forma di\n"
                     f"{spiegazioni.get(c['tipo'], '...')}\n"
                     "A destra: la stessa superficie vista dall'alto, come curve di livello colorate per quota.")
    return fig


def grafico_edo(esercizio):
    """Soluzione y(x) del problema di Cauchy sull'intervallo [0,5]."""
    x = edo_mod.x
    y_expr = esercizio['soluzione_attesa'].rhs
    y0 = esercizio['y0']
    y_num = sp.lambdify(x, y_expr, 'numpy')
    xs = np.linspace(0, 5, 400)
    ys = _valuta(y_num, xs)

    fig, ax = plt.subplots(figsize=(6, 4.4))
    ax.plot(xs, ys, linewidth=2, color='#2e5c8a')
    ax.plot(0, float(y0), 'ro', markersize=7, label=f"y(0) = {y0}")
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')
    ax.set_title("Soluzione del problema di Cauchy")
    ax.legend()
    _didascalia(fig, "La curva e' la soluzione y(x) trovata; il punto rosso e' la condizione\n"
                     "iniziale y(0) imposta dal problema di Cauchy, da cui la curva deve partire.")
    return fig


def grafico_integrale(esercizio):
    """Dominio D di integrazione (cerchio pieno o corona circolare), in coordinate cartesiane."""
    fig, ax = plt.subplots(figsize=(5, 5.4))
    theta = np.linspace(0, 2 * np.pi, 200)

    if esercizio['tipo'] == 'cerchio_pieno':
        R = esercizio['r_max']
        ax.fill(R * np.cos(theta), R * np.sin(theta), alpha=0.45, color='#2e5c8a')
        lim = R * 1.3
    else:
        R1, R2 = esercizio['r_min'], esercizio['r_max']
        ax.fill(R2 * np.cos(theta), R2 * np.sin(theta), alpha=0.45, color='#2e5c8a')
        ax.fill(R1 * np.cos(theta), R1 * np.sin(theta), color='white')
        lim = R2 * 1.3

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal', 'box')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_title(f"Dominio D  ({esercizio['dominio_testo']})", fontsize=9)
    _didascalia(fig, "La zona colorata e' il dominio D nel piano xy su cui si integra f(x,y)\n"
                     "(qui si vede solo la base piatta: l'integrale calcola il volume sotto la\n"
                     "superficie z=f(x,y) che sta sopra questa regione, non mostrato qui).")
    return fig


# Dispatcher usato da CLI e GUI: solo gli argomenti collegati al menu principale.
GRAFICI = {
    'serie': grafico_serie,
    'taylor': grafico_taylor,
    'lagrange': grafico_lagrange,
    'edo': grafico_edo,
    'integrali': grafico_integrale,
}
