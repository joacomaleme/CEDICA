const userLogo = document.querySelector(".user-logo");
const navDropdown = document.querySelector(".nav-dropdown");

// Cuando se cliquea afuera del botón userLogo, se cierra el dropdown
window.addEventListener("click", (e) => {
  const tieneClaseUserLogo = e.target.classList.contains("user-logo");
  if (!tieneClaseUserLogo) hideNavDropdown();
});

// Cuando clickeo el botón userLogo se chequea el estado del dropdown
userLogo.addEventListener("click", (e) => {
  checkNavDropdown();
  e.stopPropagation(); // Previene el evento de click en window
});

function checkNavDropdown() {
  // Arranca con display none para que no se vea la ejecución de la animación
  if (navDropdown.classList.contains("display-none")) {
    navDropdown.classList.remove("display-none");
  }

  // Intercambia entre las clases show y hidden
  if (navDropdown.classList.contains("show")) {
    navDropdown.classList.remove("show");
    navDropdown.classList.add("hidden");
  } else {
    navDropdown.classList.remove("hidden");
    navDropdown.classList.add("show");
  }
}

// Esconde el dropdown
function hideNavDropdown() {
  navDropdown.classList.remove("show");
  navDropdown.classList.add("hidden");
}
