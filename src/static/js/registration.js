var socket = io();

const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
const authCodeRegex = /^\d{6}$/

// Валидация email
const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(emailRegex);
};

// Валидация кода ауентификации
const validateAuthCode = (code) => {
  return String(code)
    .toLowerCase()
    .match(authCodeRegex);
}

function setEmailErrorMsg(errorMsg, inputBlock, elementAfter){
  let prevEmailErrorText = document.getElementById("emailErrorText");
  if (prevEmailErrorText) {
    inputBlock.removeChild(prevEmailErrorText);
  }

  let emailErrorText = document.createElement('div');
  emailErrorText.id = "emailErrorText";
  inputBlock.insertBefore(emailErrorText, elementAfter);

  setTimeout(function() {  
    emailErrorText.innerText = errorMsg;
    emailErrorText.classList.add('email-error'); 
  }, 30);
}

function setCodeErrorMsg(errorMsg, inputBlock, elementAfter){
  let prevCodeErrorText = document.getElementById("codeErrorText");
  if (prevCodeErrorText) {
    inputBlock.removeChild(prevCodeErrorText);
  }

  let codeErrorText = document.createElement("div");
  codeErrorText.id = "codeErrorText";
  inputBlock.insertBefore(codeErrorText, elementAfter);

  setTimeout(function() {  
    codeErrorText.innerText = errorMsg;
    codeErrorText.classList.add('code-error'); 
  }, 30);
}

let inputBlock = document.getElementById("inputBlock");
let emailInput = document.getElementById("emailInput");
let registrationButton = document.getElementById("registrationButton");
registrationButton.disabled = true

// Проверка валидности во время ввода адреса почты
emailInput.addEventListener('input', function() {
  const emailInputVal = emailInput.value;
  if(!validateEmail(emailInputVal)){
    emailInput.classList.add('invalid-input');
    registrationButton.disabled = true;
  }
  else {
    emailInput.classList.remove('invalid-input');
    registrationButton.disabled = false;
  }
});

// Отправка адреса почты на сервер
registrationButton.addEventListener("click", function(event) {
    event.preventDefault();
    const emailInputVal = emailInput.value;

    if (validateEmail(emailInputVal)) {
        socket.emit("email_code_request", { email: emailInputVal });
        registrationButton.disabled = true
        emailInput.disabled = true
    } 
  });
  
let closeIcon = document.getElementById("closeIcon");
let modalWindow = document.getElementById("modalWindow");

let codeSumbitButton = document.getElementById("codeSumbitButton");
let codeInputField = document.getElementById("codeInputField");

// Закрытие окна с подтверждением кода
closeIcon.onclick = function() {
  emailInput.disabled = false;

  modalWindow.classList.remove("show");
  modalWindow.classList.add("hide");

  codeInputField.disabled = false;
  codeInputField.value = '';
}

// Проверка валидности во время ввода кода ауентификации
codeInputField.addEventListener("input", function(event) {
  authCode = codeInputField.value
  if (validateAuthCode(authCode)) {
    codeInputField.classList.remove('invalid-input');
    codeSumbitButton.disabled = false;
  } else {
    codeInputField.classList.add('invalid-input');
    codeSumbitButton.disabled = true;
  }
});

// Отправка кода ауентификации на сервер
codeSumbitButton.onclick = function() {
  codeSumbitButton.disabled = true;
  codeInputField.disabled = true;
  authCode = codeInputField.value;

  modalEmail = document.getElementById("modalEmailText");
  socket.emit("auth_code_verification", {email: modalEmail.innerText, authCode: authCode});
}

socket.on("email_code_response", function(response) {
  if (response.success) {
    modalWindow.classList.remove("hide");
    modalWindow.classList.add("show");

    modalEmail = document.getElementById("modalEmailText");
    modalEmail.innerText = response.email;

  } else {
    setEmailErrorMsg("Ошибка запроса на сервер", inputBlock, registrationButton);
  }
})

socket.on("email_error", function(response) {
  setEmailErrorMsg(response["error_msg"], inputBlock, registrationButton);
  emailInput.disabled = false;
});

let codeInputBlock = document.getElementById("codeInputBlock");
socket.on("auth_code_verification_error", function(response) {
  setCodeErrorMsg(response["error_msg"], codeInputBlock, codeSumbitButton);
  codeInputField.disabled = false;
});

socket.on("reg_response", function(response) {
  if (response.success) {
        alert("Регистрация выполнена")
        window.location.href = "/";
  } 
});