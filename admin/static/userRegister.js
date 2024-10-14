document.addEventListener("DOMContentLoaded", function () {
  const mails = {{ mails|tojson }};
  const aliases = {{ aliases|tojson }};
  
  var emailField = document.getElementById("email-field");
  var emailLabel = document.getElementById("email-label");
  var emailError = document.getElementById("email-error");

  var passwordField = document.getElementById("password-field");
  var passwordLabel = document.getElementById("password-label");
  var passwordError = document.getElementById("password-error");

  var aliasField = document.getElementById("alias-field");
  var aliasLabel = document.getElementById("alias-label");
  var aliasError = document.getElementById("alias-error");

  var button = document.getElementById('button-submit');


  var contraValida = false;
  var mailValido = false;
  var aliasValido = false;
  
  aliasField.addEventListener("input", validateAlias);
  aliasField.addEventListener("focus", validateAlias);
  emailField.addEventListener("input", validateEmail);
  emailField.addEventListener("focus", validateEmail);
  passwordField.addEventListener("input", validatePassword);
  passwordField.addEventListener("focus", validatePassword);

  if (emailField.value) {
      validateEmail();
  }
  if (passwordField.value) {
      validatePassword();
  }
  
  
  function validateEmail(){
      emailLabel.style.top = "-0.2rem";

      if(!emailField.value.match(/^[A-Za-z\._\-0-9]+[@][A-Za-z]+[\.][a-z]{2,4}$/)){
          emailError.innerHTML = "Mail invalido";
          emailError.style.top = "80%";
          emailField.style.borderBottomColor = "red";
          mailValido = false;
          button.disabled = true;
          return false;
      }
      else{
          if(mails.includes(emailField.value)){
              emailError.innerHTML = "Mail ya registrado";
              emailError.style.top = "80%";
              emailField.style.borderBottomColor = "red";
              mailValido = false;
              button.disabled = true;
              return false;
          }
          else{
              emailError.innerHTML = "";
              emailField.style.borderBottomColor = "green";
              emailError.style.top = "50%";
              mailValido = true;
              button.disabled = !(contraValida && mailValido && aliasValido);
              return true;
          }
      }
  }

  function validateAlias(){
      aliasLabel.style.top = "-0.2rem";

      if(aliasField.value.length == 0){
          aliasError.innerHTML = "Este campo es obligatorio";
          aliasError.style.top = "80%";
          aliasField.style.borderBottomColor = "red";
          aliasValido = false;
          button.disabled = true;
          return false;
      }
      else{
          if(aliases.includes(aliasField.value)){
              aliasError.innerHTML = "Alias ya registrado";
              aliasError.style.top = "80%";
              aliasField.style.borderBottomColor = "red";
              aliasValido = false;
              button.disabled = true;
              return false;
          }
          else{
              aliasError.innerHTML = "";
              aliasError.style.top = "50%";
              aliasField.style.borderBottomColor = "green";
              aliasValido = true;
              button.disabled = !(contraValida && mailValido && aliasValido);
              return true;
          }
      }
  }   

  function validatePassword(){
      passwordLabel.style.top = "-0.2rem";

      if(passwordField.value.length < 7){
          passwordError.innerHTML = "Contraseña demasiado corta, faltan " + (7-passwordField.value.length) + " caracteres.";
          passwordError.style.top = "80%";
          passwordField.style.borderBottomColor = "red";
          contraValida = false;
          button.disabled = true;
          return false;
      }
      else{
          if(passwordField.value.match(/^[A-Za-z]+$/)){
              passwordError.innerHTML = "Incluya un número o caracter especial";
              passwordError.style.top = "80%";
              passwordField.style.borderBottomColor = "red";
              contraValida = false;
              button.disabled = true;
              return false;
          }
          else{
              passwordError.innerHTML = "";
              passwordError.style.top = "50%";
              passwordField.style.borderBottomColor = "green";
              contraValida = true;
              button.disabled = !(contraValida && mailValido && aliasValido);
              return true;
          }
      }
  }            
});