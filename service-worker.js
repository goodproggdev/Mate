/*
 * Service worker per l'uso offline. Due cache separate:
 * - CACHE_APP: i file del sito (html/css/py/icone), piccoli, aggiornati ad ogni nuova versione.
 * - CACHE_RUNTIME: tutto cio' che viene scaricato a runtime (soprattutto Pyodide + numpy/sympy/
 *   matplotlib dal CDN jsdelivr, qualche decina di MB): una volta scaricato una volta con internet,
 *   resta in cache "per sempre" (le URL includono il numero di versione, quindi non cambiano mai)
 *   e da quel momento l'esercitazione funziona anche senza connessione.
 */
const CACHE_APP = "mm-app-v1";
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

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_APP).then((cache) => cache.addAll(APP_ASSETS)).then(() => self.skipWaiting())
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
