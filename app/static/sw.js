"use strict";

const VERSION = "sna-public-v26";
const SHELL = [
  "/", "/admin", "/manifest.webmanifest",
  "/static/style.css", "/static/map-views.css", "/static/coherence.css",
  "/static/app.js", "/static/admin.js", "/static/offline.js", "/static/assistant.js",
  "/static/vendor/maplibre/maplibre-gl.css", "/static/vendor/maplibre/maplibre-gl.js",
  "/static/syria-logo.png", "/static/syria-logo-transparent.png"
];
const PUBLIC_DATA = [
  "/api/v1/map/syria/boundary", "/api/v1/map/syria/governorates",
  "/api/v1/map/zabadani/roads", "/api/v1/map/zabadani/buildings",
  "/api/v1/addresses?q="
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(VERSION).then(cache => cache.addAll(SHELL.concat(PUBLIC_DATA))).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== VERSION).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (request.headers.has("Authorization") || url.pathname.startsWith("/api/v1/auth/") || url.pathname.startsWith("/api/v1/audit") || url.pathname.startsWith("/api/v1/change-requests") || url.pathname.startsWith("/api/v1/house-number-cases") || url.pathname.startsWith("/api/v1/field-jobs")) return;
  const cacheable = url.pathname.startsWith("/static/") || url.pathname === "/" || url.pathname === "/admin" || url.pathname === "/manifest.webmanifest" || PUBLIC_DATA.some(item => url.pathname + url.search === item);
  if (!cacheable) return;
  event.respondWith(fetch(request).then(response => {
    if (response.ok) caches.open(VERSION).then(cache => cache.put(request, response.clone()));
    return response;
  }).catch(() => caches.match(request).then(cached => cached || (request.mode === "navigate" ? caches.match("/") : Promise.reject(new Error("offline"))))));
});
