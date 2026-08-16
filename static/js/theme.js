(function () {
  var stored = localStorage.getItem("theme");
  if (stored) document.documentElement.setAttribute("data-theme", stored);

  window.toggleTheme = function () {
    var current = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
    var next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  };
})();
