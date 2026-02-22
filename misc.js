const html = document.documentElement;
const icon = document.getElementById("themeIcon")

// Beim Laden gespeicherten Wert anwenden
const saved = localStorage.getItem("theme");
if (saved){
  html.setAttribute("data-bs-theme", saved);
  if (saved === "dark") {
    icon.classList.replace("bi-sun-fill", "bi-moon-fill");
  } else {
    icon.classList.replace("bi-moon-fill", "bi-sun-fill");
  }
}
else{
  html.setAttribute("data-bs-theme", "dark");
  icon.classList.replace("bi-sun-fill", "bi-moon-fill");
}

document.getElementById("themeToggle").addEventListener("click", () => {
  const current = html.getAttribute("data-bs-theme");
  const next = current === "dark" ? "light" : "dark";

  html.setAttribute("data-bs-theme", next);
  localStorage.setItem("theme", next);
  
  if (next === "dark") {
    icon.classList.replace("bi-sun-fill", "bi-moon-fill");
  } else {
    icon.classList.replace("bi-moon-fill", "bi-sun-fill");
  }
});
