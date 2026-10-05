/* ==========================================================================
   زيفورا — سكربت الواجهة
   الموقع يعمل كاملًا بدونه؛ وظيفته تحسين التجربة فقط.
   ========================================================================== */
(function () {
  "use strict";

  var doc = document;
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------ حالة الترويسة عند التمرير */
  var header = doc.querySelector("[data-header]");
  if (header) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        header.classList.toggle("is-scrolled", window.scrollY > 8);
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------------- قائمة الجوال */
  var menu = doc.querySelector(".menu");
  if (menu) {
    doc.addEventListener("click", function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.open) {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
    each(menu.querySelectorAll("a"), function (a) {
      a.addEventListener("click", function () { menu.open = false; });
    });
  }

  /* ------------------------------------- ترقيم العناصر المتتابعة داخل الشبكات */
  each(doc.querySelectorAll("[data-stagger]"), function (group) {
    each(group.children, function (child, i) { child.style.setProperty("--i", i); });
  });

  /* ------------------------------------- الظهور عند التمرير + امتلاء البراميل */
  var watched = doc.querySelectorAll(".reveal, .barrel__fill");
  if (watched.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      each(watched, function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
      each(watched, function (el) { io.observe(el); });
    }
  }

  /* ------------------------- اختيار المادة مسبقًا في النموذج (?product=sles) */
  var select = doc.querySelector("select[data-product-select]");
  if (select && "URLSearchParams" in window) {
    var wanted = new URLSearchParams(window.location.search).get("product");
    if (wanted) {
      each(select.options, function (opt) {
        if (opt.getAttribute("data-key") === wanted) select.value = opt.value;
      });
    }
  }

  /* --------------------------------------------------------- سنة حقوق النشر */
  each(doc.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
