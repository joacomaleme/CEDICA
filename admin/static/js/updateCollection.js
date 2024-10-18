document.addEventListener("DOMContentLoaded", function () {
  const montoField = document.getElementById("amount-field");

  const submitBtn = document.getElementById("button-submit");

  const MAXVALIDOS = 1;
  let validos = 0;

  const inputs = {
    "name-field": [montoField, validateEmpty],
  };

  Object.keys(inputs).forEach(e => {
    inputs[e][0].addEventListener("input", inputs[e][1]);
    inputs[e][0].addEventListener("focus", inputs[e][1]);
  })

  callAll();

  // Valida que el campo no esté vacío
  function validateEmpty(event) {
    const field = event.target;

    if (field.value.trim() === "") {
      activateError(field, "Este campo es obligatorio");
    } else {
      deactivateError(field);
    }
  }

  // Activa el error del input indicado con el mensaje dado
  function activateError(field, message) {
    const id = trimID(field.id);
    const errorMessage = document.getElementById(id + "-error");

    // Uso la clase valid para no decrementar dos veces seguidas
    if (field.classList.contains('valid')) {
      validos--;
      field.classList.remove('valid');
    }

    errorMessage.innerHTML = message;
    errorMessage.style.top = "80%";
    
    field.style.borderBottomColor = "red";
    submitBtn.disabled = validos !== MAXVALIDOS;
  }

  // Desactiva el error del input dado
  function deactivateError(field) {
    const id = trimID(field.id);
    const errorMessage = document.getElementById(id + "-error");

    // Uso la clase valid para no aumentar dos veces seguidas
    if (!field.classList.contains('valid')) {
      validos++;
      field.classList.add('valid');
    }

    errorMessage.innerHTML = "";
    field.style.borderBottomColor = "rgb(0, 170, 0)";
    submitBtn.disabled = validos !== MAXVALIDOS
  }

  // Elimina la parte de "-label" del id del input tag
  function trimID(id) {
    const split = id.split("-");
    return split.slice(0, split.length - 1).join("-");
  }

  // Activa el evento input para todos, checkeando sus valores
  function callAll() {
    const changeEvent = new Event('input');
    Object.keys(inputs).forEach(e => inputs[e][0].dispatchEvent(changeEvent))
  }
});
