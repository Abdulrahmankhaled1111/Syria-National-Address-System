(() => {
  "use strict";
  const translations = {
    ar: {online:"الخادم متصل",offline:"وضع دون اتصال · بيانات عامة مخزنة",unavailable:"الخادم غير متاح"},
    en: {online:"Server connected",offline:"Offline mode · cached public data",unavailable:"Server unavailable"},
    de: {online:"Server verbunden",offline:"Offline-Modus · öffentliche Daten aus Cache",unavailable:"Server nicht erreichbar"}
  };
  const language = () => document.documentElement.lang in translations ? document.documentElement.lang : "ar";
  function badge() {
    let element = document.querySelector(".system-state");
    if (element) return element;
    const actions = document.querySelector(".header-actions");
    if (!actions) return null;
    actions.insertAdjacentHTML("afterbegin",'<span class="system-state" id="offline-state"><i></i><span></span></span>');
    return document.querySelector("#offline-state");
  }
  async function refresh() {
    const element = badge();
    if (!element) return;
    let reachable = false;
    if (navigator.onLine) {
      try {
        const response = await fetch("/health", {cache:"no-store", signal:AbortSignal.timeout(3500)});
        reachable = response.ok;
      } catch (_) {}
    }
    const state = reachable ? "online" : (navigator.onLine ? "unavailable" : "offline");
    element.dataset.state = state;
    const target = element.querySelector("span");
    if (target) target.textContent = translations[language()][state];
    document.documentElement.dataset.connection = state;
    window.dispatchEvent(new CustomEvent("sna:connection", {detail:{state,reachable}}));
  }
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    navigator.serviceWorker.register("/sw.js", {scope:"/"}).catch(() => {});
  }
  addEventListener("online", refresh);
  addEventListener("offline", refresh);
  addEventListener("languagechange", refresh);
  document.addEventListener("DOMContentLoaded", refresh, {once:true});
  setInterval(refresh, 30000);
})();
