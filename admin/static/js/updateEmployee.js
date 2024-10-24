document.addEventListener("DOMContentLoaded", function () {
  const nameField = document.getElementById("name-field");
  const surnameField = document.getElementById("surname-field");
  const dniField = document.getElementById("dni-field");
  const addressStreetField = document.getElementById("street-field");
  const addressNumberField = document.getElementById("number-field");
  const emailField = document.getElementById("email-field");
  const phoneField = document.getElementById("phone-field");
  const emergencyContactNameField = document.getElementById("emergency-contact-name-field");
  const emergencyContactPhoneField = document.getElementById("emergency-contact-phone-field");
  const obraSocialField = document.getElementById("obra-social-field");
  const affiliateNumberField = document.getElementById("affiliate-number-field");

  const submitBtn = document.getElementById("button-submit");

  // Se les asigna el evento adecuado a cada atributo
  const inputs = {
    "name-field": [nameField, (e) => validateLength(e, 100)],
    "surname-field": [surnameField, (e) => validateLength(e, 100)],
    "dni-field": [dniField, validateDNI],
    "street-field": [addressStreetField, (e) => validateLength(e, 255)],
    "number-field": [addressNumberField, validateNumber],
    "email-field": [emailField, validateEmail],
    "phone-field": [phoneField, validatePhone],
    "emergency-contact-name-field": [emergencyContactNameField, (e) => validateLength(e, 100)],
    "emergency-contact-phone-field": [emergencyContactPhoneField, validatePhone],
    "obra-social-field": [obraSocialField, (e) => validateLength(e, 100)],
    "affiliate-number-field": [affiliateNumberField, validateAffiliateNumber],
  };
  
  const MAXVALIDOS = 11;
  let validos = 0;

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

  function validateNumber(event) {
    const field = event.target;

    if (!field.value.match(/^\d+$/)) {
      activateError(field, "Formato inválido");
    } else {
      deactivateError(field);
    }
  }

  function validatePhone(event) {
    const field = event.target;

    if (!field.value.match(/^[\d\-]+$/)) {
      activateError(field, "Formato inválido");
    } else {
      deactivateError(field);
    }
  }

  // Valida que el DNI tenga el formato adecuado y que no esté repetido
  function validateDNI(event) {
    const field = event.target;

    if (!field.value.match(/^\d+$/)) {
      activateError(field, "Formato de DNI inválido");
    } else {
        if (dnis.includes(field.value)) {
          activateError(field, "DNI ya registrado");
        } else {
          deactivateError(field);
        }
    }
  }

  // Valida que el mail tenga el formato adecuado y que no esté repetido
  function validateEmail() {
    if (!emailField.value.match(/^[A-Za-z\._\-0-9]+[@][A-Za-z]+[\.][a-z]{2,4}$/)) {
      activateError(emailField, "Formato de email inválido");
    } else {
      if (mails.includes(emailField.value)) {
        activateError(emailField, "Email ya registrado");
      } else {
        deactivateError(emailField);
      }
    }
  }

  // Valida que el número de afiliado tenga el formato adecuado y que no esté repetido
  function validateAffiliateNumber() {
    if (affiliateNumberField.value.trim() === "") {
      activateError(affiliateNumberField, "Formato de número inválido");
    } else {
      if (affiliate_numbers.includes(affiliateNumberField.value)) {
        activateError(affiliateNumberField, "Número ya registrado");
      } else {
        deactivateError(affiliateNumberField);
      }
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
    submitBtn.disabled = validos !== MAXVALIDOS;
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