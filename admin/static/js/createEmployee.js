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

  const MAXVALIDOS = 11;
  let validos = 0;

  // Se valida que ninguno de estos inputs esté vacío
  const inputs = [nameField, surnameField, addressStreetField, emergencyContactNameField, obraSocialField, affiliateNumberField];
  inputs.forEach((e) => {
    e.addEventListener("input", validateEmpty);
    e.addEventListener("focus", validateEmpty);
  });

  emailField.addEventListener("input", validateEmail);
  emailField.addEventListener("focus", validateEmail);
  dniField.addEventListener("input", validateDNI);
  dniField.addEventListener("focus", validateDNI);
  addressNumberField.addEventListener("input", validateNumber);
  addressNumberField.addEventListener("focus", validateNumber);
  phoneField.addEventListener("input", validatePhone);
  phoneField.addEventListener("focus", validatePhone);
  emergencyContactPhoneField.addEventListener("input", validatePhone);
  emergencyContactPhoneField.addEventListener("focus", validatePhone);
  affiliateNumberField.addEventListener("input", validateAffiliateNumber);
  affiliateNumberField.addEventListener("focus", validateAffiliateNumber);

  // Valida que el campo no esté vacío
  function validateEmpty(event) {
    const field = event.target;

    if (field.value.trim() === "") {
      activateError(field, "Este campo es obligatorio");
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
});
