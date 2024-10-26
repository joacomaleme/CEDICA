document.addEventListener("DOMContentLoaded", function () {
  const nameField = document.getElementById("name-field");
  const birthField = document.getElementById("birth-field");
  const breedField = document.getElementById("breed-field");
  const coatField = document.getElementById("coat-field");
  //const employeesField = document.getElementById("obra-social-field");

  const submitBtn = document.getElementById("button-submit");

  const inputs = {
    "name-field": [nameField, (e) => validateLength(e, 100)],
    "birth-field": [birthField, validateDate],
    "breed-field": [breedField, (e) => validateLength(e, 100)],
    "coat-field": [coatField, (e) => validateLength(e, 64)],
  };
  
  const MAXVALIDOS = 4;
  let validos = 0;

  Object.keys(inputs).forEach(e => {
    inputs[e][0].addEventListener("input", inputs[e][1]);
    inputs[e][0].addEventListener("focus", inputs[e][1]);
  })

  callAll();

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

  // Valida el formato de la fecha
  function validateDate(event) {
    const field = event.target;
    if (!field.value.match(/^\d{4}-\d{2}-\d{2}$/)) {
      activateError(field, "Formato de fecha inválido (YYYY-MM-DD)");
    } else {
      deactivateError(field);
    }
  }

  // Activa el error para el campo especificado
  function activateError(field, message) {
    const id = trimID(field.id);
    const errorMessage = document.getElementById(id + "-error");

    if (field.classList.contains('valid')) {
      validos--;
      field.classList.remove('valid');
    }

    errorMessage.innerHTML = message;
    errorMessage.style.top = "80%";
    field.style.borderBottomColor = "red";
    submitBtn.disabled = validos !== MAXVALIDOS;
  }

  // Desactiva el error para el campo especificado
  function deactivateError(field) {
    const id = trimID(field.id);
    const errorMessage = document.getElementById(id + "-error");

    if (!field.classList.contains('valid')) {
      validos++;
      field.classList.add('valid');
    }

    errorMessage.innerHTML = "";
    field.style.borderBottomColor = "rgb(0, 170, 0)";
    submitBtn.disabled = validos !== MAXVALIDOS;
  }

  function trimID(id) {
    const split = id.split("-");
    return split.slice(0, split.length - 1).join("-");
  }

  function callAll() {
    const changeEvent = new Event('input');
    Object.keys(inputs).forEach(e => inputs[e][0].dispatchEvent(changeEvent));
  }
});
