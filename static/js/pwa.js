(function () {
  if (!("serviceWorker" in navigator)) return;

  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {
      // El registro falla en contextos no seguros (por ejemplo, IP sin HTTPS).
    });
  });
})();
