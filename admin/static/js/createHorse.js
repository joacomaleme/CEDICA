document.addEventListener("DOMContentLoaded", function () {
  const nameField = document.getElementById("name-field");
  const birthField = document.getElementById("birth-field");
  const breedField = document.getElementById("breed-field");
  const coatField = document.getElementById("coat-field");

  const submitBtn = document.getElementById("button-submit");

  const MAXVALIDOS = 4;
  let validos = 0;

  // Se les asigna el evento adecuado a cada atributo
  const inputs = {
    "name-field": [nameField, (e) => validateLength(e, 100)],
    "birth-field": [birthField, validateDate],
    "breed-field": [breedField, (e) => validateLength(e, 100)],
    "coat-field": [coatField, (e) => validateLength(e, 64)],
  };
  Object.keys(inputs).forEach(e => {
    inputs[e][0].addEventListener("input", inputs[e][1]);
    inputs[e][0].addEventListener("focus", inputs[e][1]);
  });

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

  // Validates field length and emptiness
  function validateLength(event, maxLength) {
    const field = event.target;
    if (field.value.trim() === "") {
      activateError(field, "Este campo es obligatorio");
    } else if (field.value.length > maxLength) {
      activateError(field, `Este campo debe tener menos de ${maxLength} caracteres`);
    } else {
      deactivateError(field);
    }
  }

  // Valida la fecha con el formato (YYYY-MM-DD)
  function validateDate(event) {
    const field = event.target;
    if (field.value.trim() === "") {
      activateError(field, "Este campo es obligatorio");
    } else if (!field.value.match(/^\d{4}-\d{2}-\d{2}$/)) {
      activateError(field, "Formato de fecha inválido (YYYY-MM-DD)");
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

  function callAll() {
    // Trigger initial validation for all fields
    Object.keys(inputs).forEach(e => {
      inputs[e][1]({ target: inputs[e][0] });
    });
  }
});
