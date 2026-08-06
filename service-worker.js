/*
 * Service worker per l'uso offline. Due cache separate:
 * - CACHE_APP: i file del sito (html/css/py/icone), piccoli, aggiornati ad ogni nuova versione.
 * - CACHE_RUNTIME: tutto cio' che viene scaricato a runtime (soprattutto Pyodide + numpy/sympy/
 *   matplotlib dal CDN jsdelivr, qualche decina di MB): una volta scaricato, resta in cache "per
 *   sempre" (le URL includono il numero di versione, quindi non cambiano mai) e da quel momento
 *   l'area Esercizi si apre senza dover riscaricare nulla, anche offline.
 *
 * All'installazione, oltre ai file del sito, proviamo a scaricare in anticipo (pre-cache) anche
 * il runtime di Pyodide e i package numpy/sympy/matplotlib: cosi' la PRIMA visita all'area
 * Esercizi e' gia' rapida, non solo la seconda.
 */
const CACHE_APP = "mm-app-v3";
const CACHE_RUNTIME = "mm-runtime-v1";

const APP_ASSETS = [
  "./",
  "index.html",
  "esercizi.html",
  "teoria.html",
  "style.css",
  "manifest.json",
  "serie.py",
  "taylor.py",
  "multivariabile.py",
  "edo.py",
  "integrali.py",
  "grafico.py",
  "bridge.py",
  "icon-192.png",
  "icon-512.png",
  "apple-touch-icon.png",
  "favicon-32.png",
];

const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v314.0.4/full/";
const PYODIDE_CORE_FILES = [
  "pyodide.js",
  "pyodide.asm.js",
  "pyodide.asm.wasm",
  "pyodide-lock.json",
  "python_stdlib.zip",
];
const PYODIDE_TOP_PACKAGES = ["numpy", "sympy", "matplotlib"];
const KATEX_BASE = "https://cdn.jsdelivr.net/npm/katex@0.18.1/dist/";
const KATEX_FILES = ["katex.min.css", "katex.min.js", "contrib/auto-render.min.js"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_APP)
      .then((cache) => cache.addAll(APP_ASSETS))
      .then(() => precacheRuntimeAssets())
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_APP && k !== CACHE_RUNTIME)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  const isOwnOrigin = url.origin === self.location.origin;
  const cacheName = isOwnOrigin ? CACHE_APP : CACHE_RUNTIME;

  event.respondWith(
    caches.open(cacheName).then((cache) =>
      cache.match(req).then((cached) => {
        if (cached) return cached;
        return fetch(req)
          .then((resp) => {
            // Salviamo in cache solo risposte valide (o opache da CDN cross-origin, comunque utili offline).
            if (resp && (resp.ok || resp.type === "opaque")) {
              cache.put(req, resp.clone());
            }
            return resp;
          })
          .catch(() => {
            // Offline e non in cache: per una navigazione HTML, meglio mostrare la home che un errore secco.
            if (req.mode === "navigate") return cache.match("index.html");
            throw new Error("offline e risorsa non in cache: " + req.url);
          });
      })
    )
  );
});

/*
 * Pre-cache "best effort" dei file pesanti (Pyodide + package + KaTeX) subito dopo
 * l'installazione del service worker, cosi' l'utente non deve aspettare che li scarichi
 * "al volo" la prima volta che apre l'area Esercizi. Se qualcosa fallisce (rete assente,
 * CDN irraggiungibile) non blocchiamo l'installazione: verranno scaricati e salvati in
 * cache comunque al primo utilizzo reale, tramite il normale gestore "fetch" sopra.
 */
async function precacheRuntimeAssets() {
  try {
    const cache = await caches.open(CACHE_RUNTIME);

    const urlsFisse = [
      ...PYODIDE_CORE_FILES.map((f) => PYODIDE_BASE + f),
      ...KATEX_FILES.map((f) => KATEX_BASE + f),
    ];
    await Promise.allSettled(urlsFisse.map((u) => precacheOne(cache, u)));

    const lockResp = await fetch(PYODIDE_BASE + "pyodide-lock.json");
    if (!lockResp.ok) return;
    const lock = await lockResp.json();
    const packages = lock.packages || {};

    const voluti = new Set();
    const visita = (chiave) => {
      const k = chiave.toLowerCase();
      if (voluti.has(k)) return;
      const pkg = packages[k];
      if (!pkg) return;
      voluti.add(k);
      (pkg.depends || []).forEach((dep) => visita(dep));
    };
    PYODIDE_TOP_PACKAGES.forEach((p) => visita(p));

    const fileUrls = [...voluti]
      .map((k) => packages[k] && packages[k].file_name)
      .filter(Boolean)
      .map((fn) => PYODIDE_BASE + fn);
    await Promise.allSettled(fileUrls.map((u) => precacheOne(cache, u)));
  } catch (e) {
    console.warn("Pre-cache del runtime Pyodide non riuscito (verra' scaricato al primo utilizzo):", e);
  }
}

async function precacheOne(cache, url) {
  try {
    const esistente = await cache.match(url);
    if (esistente) return;
    let resp;
    try {
      resp = await fetch(url, { mode: "cors" });
    } catch (e) {
      resp = await fetch(url, { mode: "no-cors" });
    }
    if (resp && (resp.ok || resp.type === "opaque")) {
      await cache.put(url, resp);
    }
  } catch (e) {
    // ignorato: verra' scaricato (e messo in cache) al primo utilizzo effettivo dell'app.
  }
}
