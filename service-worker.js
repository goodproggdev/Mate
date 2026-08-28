/*
 * Service worker per l'uso offline. Due cache separate:
 * - CACHE_APP: i file del sito (html/css/icone/il banco esercizi.json), aggiornati ad
 *   ogni nuova versione.
 * - CACHE_RUNTIME: risorse esterne da CDN (KaTeX, mathjs): una volta scaricate restano
 *   in cache "per sempre" (le URL includono il numero di versione, quindi non cambiano
 *   mai) e da quel momento l'area Esercizi si apre senza dover riscaricare nulla, anche
 *   offline.
 *
 * Dalla v4 il sito non usa piu' Pyodide: tutti gli esercizi (testo, soluzione passo-
 * passo, grafico) sono precalcolati e salvati in esercizi.json, quindi non serve piu'
 * scaricare un runtime Python + numpy/sympy/matplotlib nel browser (erano decine di MB
 * e qualche secondo di avvio); il banco statico e' piu' piccolo e si apre all'istante.
 */
const CACHE_APP = "mm-app-v5";
const CACHE_RUNTIME = "mm-runtime-v2";

const APP_ASSETS = [
  "./",
  "index.html",
  "esercizi.html",
  "teoria.html",
  "style.css",
  "manifest.json",
  "esercizi.json",
  "icon-192.png",
  "icon-512.png",
  "apple-touch-icon.png",
  "favicon-32.png",
];

const KATEX_BASE = "https://cdn.jsdelivr.net/npm/katex@0.18.1/dist/";
const KATEX_FILES = ["katex.min.css", "katex.min.js", "contrib/auto-render.min.js"];
const MATHJS_URL = "https://cdn.jsdelivr.net/npm/mathjs@12.4.3/lib/browser/math.js";

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
 * Pre-cache "best effort" delle risorse esterne (KaTeX + mathjs) subito dopo
 * l'installazione del service worker, cosi' l'utente non deve aspettare che le scarichi
 * "al volo" la prima volta che apre l'area Esercizi. Se qualcosa fallisce (rete assente,
 * CDN irraggiungibile) non blocchiamo l'installazione: verranno scaricate e salvate in
 * cache comunque al primo utilizzo reale, tramite il normale gestore "fetch" sopra.
 */
async function precacheRuntimeAssets() {
  try {
    const cache = await caches.open(CACHE_RUNTIME);
    const urls = [
      ...KATEX_FILES.map((f) => KATEX_BASE + f),
      MATHJS_URL,
    ];
    await Promise.allSettled(urls.map((u) => precacheOne(cache, u)));
  } catch (e) {
    console.warn("Pre-cache delle risorse esterne non riuscito (verranno scaricate al primo utilizzo):", e);
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
