document.addEventListener("DOMContentLoaded", function () {
    const nameField = document.getElementById("name-field");
    const surnameField = document.getElementById("surname-field");
    const dniField = document.getElementById("dni-field");
    const birthdateField = document.getElementById("birthdate-field");
    const streetField = document.getElementById("street-field");
    const numberField = document.getElementById("number-field");
    const apartmentField = document.getElementById("apartment-field");
    const phoneField = document.getElementById("phone-field");
    const emergencyContactField = document.getElementById("emergency-contact-name-field");
    const emergencyContactPhoneField = document.getElementById("emergency-contact-phone-field");
    const newDisabilityField = document.getElementById("new-disability-field");
    const healthInsuranceField = document.getElementById("health-insurance-field");
    const affiliateNumberField = document.getElementById("affiliate-number-field");
    const schoolNameField = document.getElementById("school-name-field");
    const schoolAddressField = document.getElementById("school-address-field");
    const schoolNumberField = document.getElementById("school-phone-field");
    const currentGradeField = document.getElementById("current-grade-field");

    const disableCertificateCheckbox = document.getElementById("disable-certificate-checkbox");
    const disabilityDiagnosis = document.getElementById("disability-diagnosis-field");
    const disableCertificateCheckbox = document.getElementById("disable-certificate-checkbox");
    const disableCertificateCheckbox = document.getElementById("disable-certificate-checkbox");
    const disableCertificateCheckbox = document.getElementById("disable-certificate-checkbox");
    const schoolField = document.getElementById("school-id-field");

    const disabiliyDiagnosisEntero = document.getElementById("disability-diagnosis-entero");
    const opcionOtro = document.getElementById("opcion-otro");
    const familyAllowanceTypeEntero = document.getElementById("family-allowance-type-entero");
    const pensionTypeEntero = document.getElementById("pension-type-entero");
    const newSchool = document.getElementById("new-school");
  
    const submitBtn = document.getElementById("button-submit");
  
    const inputs = {
        "name-field": [nameField, validateEmpty],
        "surname-field": [surnameField, validateEmpty],
        "dni-field": [dniField, validateDNI],
        "birthdate-field": [birthdateField, validateEmpty],
        "street-field": [streetField, validateEmpty],
        "number-field": [numberField, validateNumber],
        "apartment-field": [apartmentField, validateEmpty],
        "phone-field": [phoneField, validatePhone],
        "emergency-contact-field": [emergencyContactField, validateEmpty],
        "emergency-contact-phone-field": [emergencyContactPhoneField, validatePhone],
        "new-disability-field": [newDisabilityField, validateNewDisability],
        "health-insurance-field": [healthInsuranceField, validateEmpty],
        "affiliate-number-field": [affiliateNumberField, validateAffiliateNumber],
        "school-name-field": [schoolNameField, validateEmpty],
        "school-address-field": [schoolAddressField, validateEmpty],
        "school-number-field": [schoolNumberField, validateEmpty],
        "current-grade-field": [currentGradeField, validateEmpty]
    };
    
    const MAXVALIDOS = 17;
    let validos = 0;
  
    Object.keys(inputs).forEach(e => {
        inputs[e][0].addEventListener("input", inputs[e][1]);
        inputs[e][0].addEventListener("focus", inputs[e][1]);
    })

    disableCertificateCheckbox.addEventListener("change", showDisabilityDiagnosis)
    disabilityDiagnosis.addEventListener("change", showOpcionOtro)
    disableCertificateCheckbox.addEventListener("change", showFamilyAllowanceType)
    disableCertificateCheckbox.addEventListener("change", showPensionType)
    schoolField.addEventListener("change", showNewSchool)
  
    callAll();

    function showDisabilityDiagnosis() {
        if (disabilityDiagnosis == "Otro") {
            disabiliyDiagnosisEntero.style.display = "block";
        }
        else {
            disabiliyDiagnosisEntero.style.display = "none";
        }
    }

    function showOpcionOtro() {
        if (disableCertificateCheckbox.checked) {
            opcionOtro.style.display = "block";
        }
        else {
            opcionOtro.style.display = "none";
        }
    }

    function showFamilyAllowanceType() {
        if (disableCertificateCheckbox.checked) {
            familyAllowanceTypeEntero.style.display = "block";
        }
        else {
            familyAllowanceTypeEntero.style.display = "none";
        }
    }

    function showPensionType() {
        if (disableCertificateCheckbox.checked) {
            pensionTypeEntero.style.display = "block";
        }
        else {
            pensionTypeEntero.style.display = "none";
        }
    }

    function showNewSchool() {
        if (disableCertificateCheckbox.checked) {
            newSchool.style.display = "block";
        }
        else {
            newSchool.style.display = "none";
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
  
        if (field.value.trim() === "" && disabilityDiagnosis == "Otro") {
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