document.querySelector('.burger').addEventListener('click',function(){var m=document.getElementById('menu');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o);});
document.querySelectorAll('.has-sub>a').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth<=840){/* mobile: let the link work, submenu is already expanded */}});});
// A "Teklif Al" / "Pilot başla" link (#form, #basvuru, #apply) lands with the form centred on the
// screen under the header (or at the top when the form is taller than the screen).
(function () {
  var targets = { "#form": 1, "#basvuru": 1, "#apply": 1 };
  function centreForm(smooth) {
    if (!targets[location.hash]) return;
    var section = document.querySelector(location.hash);
    var form = section && section.querySelector("form");
    if (!form) return;
    var header = document.querySelector(".header");
    var top = header ? header.getBoundingClientRect().height : 0;
    var room = window.innerHeight - top;
    var box = form.getBoundingClientRect();
    var gap = box.height < room ? (room - box.height) / 2 : 16;
    var y = window.scrollY + box.top - top - gap;
    if (smooth) return window.scrollTo({ top: y, behavior: "smooth" });
    // The site scrolls smoothly (CSS); on arrival that animation fights the browser's own jump to the
    // anchor, so the first placement is instant.
    var root = document.documentElement;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, y);
    requestAnimationFrame(function () { root.style.scrollBehavior = ""; });
  }
  // The browser jumps to the anchor itself and fonts/images can still shift the page after that, so
  // centre once the page has loaded and again shortly after, unless the visitor has scrolled since.
  var touched = false;
  ["wheel", "touchstart", "keydown"].forEach(function (ev) { window.addEventListener(ev, function () { touched = true; }, { passive: true }); });
  function settle() { if (!touched) centreForm(false); }
  window.addEventListener("load", function () {
    settle();
    requestAnimationFrame(settle);
    setTimeout(settle, 150);
    setTimeout(settle, 500);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(settle);
  });
  window.addEventListener("hashchange", function () { centreForm(true); });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var url = new URL(a.getAttribute("href"), location.href);
    // A link to the form of the page already open: centre it again even if the hash stays the same.
    if (url.pathname === location.pathname && targets[url.hash] && url.hash === location.hash) {
      e.preventDefault();
      centreForm(true);
    }
  });
})();