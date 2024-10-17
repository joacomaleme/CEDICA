const navMenu = document.querySelector(".nav-menu");
const navLinksMenu = document.querySelector(".nav-links");

const userLogo = document.querySelector(".user-logo");
const navDropdown = document.querySelector(".nav-dropdown");

navMenu.addEventListener("click", (e) => {
  navMenu.classList.toggle("open-menu");
  navLinksMenu.classList.toggle("open");
  e.stopPropagation(); // Previene el evento de click en window
});

if (userLogo) { // Si el usuario no está logueado userLogo será null
  // Cuando clickeo el botón userLogo se chequea el estado del dropdown
  userLogo.addEventListener("click", (e) => {
    checkNavDropdown();
    hideLinksMenu(); // Lo cierro manual porque los clicks en window no pasan
    e.stopPropagation(); // Previene el evento de click en window
  });
}

// Cuando se cliquea afuera del botón userLogo, se cierra el dropdown
window.addEventListener("click", (e) => {
  const clases = e.target.classList;
  const selector = ".nav-menu, .nav-links, menu-bar";

  if (!e.target.matches(selector)) hideLinksMenu();
  if (!clases.contains("user-logo")) hideNavDropdown();
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

function hideLinksMenu() {
  navMenu.classList.remove("open-menu");
  navLinksMenu.classList.remove("open");
}
