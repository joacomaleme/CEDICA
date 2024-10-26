document.addEventListener("DOMContentLoaded", function () {
  const nameField = document.getElementById("name-field");
  const surnameField = document.getElementById("surname-field");
  const dniField = document.getElementById("dni-field");
  const ageField = document.getElementById("age-field");
  const birthdateField = document.getElementById("birthdate-field");
  const streetField = document.getElementById("street-field");
  const numberField = document.getElementById("number-field");
  const phoneField = document.getElementById("phone-field");
  const emergencyContactField = document.getElementById("emergency-contact-name-field");
  const emergencyContactPhoneField = document.getElementById("emergency-contact-phone-field");
  const newDisabilityField = document.getElementById("new-disability-field");
  const healthInsuranceField = document.getElementById("health-insurance-field");
  const affiliateNumberField = document.getElementById("affiliate-number-field");
  const schoolField = document.getElementById("school-id-field");
  const schoolNameField = document.getElementById("school-name-field");
  const schoolAddressField = document.getElementById("school-address-field");
  const schoolNumberField = document.getElementById("school-phone-field");
  const currentGradeField = document.getElementById("current-grade-field");
  const guardian1NameField = document.getElementById("guardian1-name-field");
  const guardian1SurnameField = document.getElementById("guardian1-surname-field");
  const guardian1DniField = document.getElementById("guardian1-dni-field");
  const guardian1StreetField = document.getElementById("guardian1-street-field");
  const guardian1NumberField = document.getElementById("guardian1-number-field");
  const guardian1PhoneField = document.getElementById("guardian1-phone-field");
  const guardian1EmailField = document.getElementById("guardian1-email-field");
  const guardian1OccupationField = document.getElementById("guardian1-occupation-field");
  const guardian1RelationshipField = document.getElementById("guardian1-relationship-field");
  const guardian2NameField = document.getElementById("guardian2-name-field");
  const guardian2SurnameField = document.getElementById("guardian2-surname-field");
  const guardian2DniField = document.getElementById("guardian2-dni-field");
  const guardian2StreetField = document.getElementById("guardian2-street-field");
  const guardian2NumberField = document.getElementById("guardian2-number-field");
  const guardian2PhoneField = document.getElementById("guardian2-phone-field");
  const guardian2EmailField = document.getElementById("guardian2-email-field");
  const guardian2OccupationField = document.getElementById("guardian2-occupation-field");
  const guardian2RelationshipField = document.getElementById("guardian2-relationship-field");

  const disableCertificateCheckbox = document.getElementById("disable-certificate-checkbox");
  const disabilityDiagnosis = document.getElementById("disability-diagnosis-field");
  const hasFamilyAllowanceCheckbox = document.getElementById("has-family-allowance-checkbox");
  const receivesPensionCheckbox = document.getElementById("receives-pension-checkbox");

  const disabiliyDiagnosisEntero = document.getElementById("disability-diagnosis-entero");
  const familyAllowanceTypeEntero = document.getElementById("family-allowance-type-entero");
  const pensionTypeEntero = document.getElementById("pension-type-entero");
  
  const submitBtn = document.getElementById("button-submit");

  const inputs = {
      "name-field": [nameField, validateEmpty],
      "surname-field": [surnameField, validateEmpty],
      "dni-field": [dniField, validateDNI],
      "age-field": [ageField, validateEmpty],
      "birthdate-field": [birthdateField, validateEmpty],
      "street-field": [streetField, validateEmpty],
      "number-field": [numberField, validateNumber],
      "phone-field": [phoneField, validatePhone],
      "emergency-contact-field": [emergencyContactField, validateEmpty],
      "emergency-contact-phone-field": [emergencyContactPhoneField, validatePhone],
      "new-disability-field": [newDisabilityField, validateNewDisability],
      "health-insurance-field": [healthInsuranceField, validateEmpty],
      "affiliate-number-field": [affiliateNumberField, validateAffiliateNumber],
      "school-name-field": [schoolNameField, validateSchool],
      "school-address-field": [schoolAddressField, validateSchool],
      "school-number-field": [schoolNumberField, validateSchool],
      "current-grade-field": [currentGradeField, validateEmpty],
      "guardian1-name-field": [guardian1NameField, validateEmpty],
      "guardian1-surname-field": [guardian1SurnameField, validateEmpty],
      "guardian1-dni-field": [guardian1DniField, validateDNI],
      "guardian1-street-field": [guardian1StreetField, validateEmpty],
      "guardian1-number-field": [guardian1NumberField, validateNumber],
      "guardian1-phone-field": [guardian1PhoneField, validatePhone],
      "guardian1-email-field": [guardian1EmailField, validateEmpty],
      "guardian1-occupation-field": [guardian1OccupationField, validateEmpty],
      "guardian1-relationship-field": [guardian1RelationshipField, validateEmpty],
      "guardian2-name-field": [guardian2NameField, validateEmpty],
      "guardian2-surname-field": [guardian2SurnameField, validateEmpty],
      "guardian2-dni-field": [guardian2DniField, validateDNI],
      "guardian2-street-field": [guardian2StreetField, validateEmpty],
      "guardian2-number-field": [guardian2NumberField, validateNumber],
      "guardian2-phone-field": [guardian2PhoneField, validatePhone],
      "guardian2-email-field": [guardian2EmailField, validateEmpty],
      "guardian2-occupation-field": [guardian2OccupationField, validateEmpty],
      "guardian2-relationship-field": [guardian2RelationshipField, validateEmpty]
  };
  
  const MAXVALIDOS = 35;
  let validos = 0;

  Object.keys(inputs).forEach(e => {
      inputs[e][0].addEventListener("input", inputs[e][1]);
      inputs[e][0].addEventListener("focus", inputs[e][1]);
  })

  disableCertificateCheckbox.addEventListener("change", showDisabilityDiagnosis);
  hasFamilyAllowanceCheckbox.addEventListener("change", showFamilyAllowanceType);
  receivesPensionCheckbox.addEventListener("change", showPensionType);

  callAll();

  function showDisabilityDiagnosis() {
    if (disableCertificateCheckbox.checked) {
        disabiliyDiagnosisEntero.style.display = "block";
    }
    else {
        disabiliyDiagnosisEntero.style.display = "none";
    }
  }

  function showFamilyAllowanceType() {
      if (hasFamilyAllowanceCheckbox.checked) {
          familyAllowanceTypeEntero.style.display = "block";
      }
      else {
          familyAllowanceTypeEntero.style.display = "none";
      }
  }

  function showPensionType() {
      if (receivesPensionCheckbox.checked) {
          pensionTypeEntero.style.display = "block";
      }
      else {
          pensionTypeEntero.style.display = "none";
      }
  }

  // Valida que el campo no esté vacío
  function validateEmpty(event) {
    const field = event.target;

    if (field.value.trim() === "") {
      activateError(field, "Este campo es obligatorio");
    } else {
      deactivateError(field);
    }
  }

  function validateNewDisability(event) {
      const field = event.target;

      if (field.value.trim() === "" && disabilityDiagnosis.value === "Otro") {
          activateError(field, "Este campo es obligatorio");
      } else {
          deactivateError(field);
      }
  }

  function validateSchool(event) {
    const field = event.target;

    if (field.value.trim() === "" && schoolField.value === "Otro") {
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