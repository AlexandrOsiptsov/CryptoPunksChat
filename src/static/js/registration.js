const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

// Валидация email
const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(emailRegex);
};

let emailInput = document.getElementById("emailInput");
let sumbitButton = document.getElementById("register-btn");
sumbitButton.disabled = true

// Проверка валидности во время ввода
emailInput.addEventListener('input', function() {
  const emailInputVal = emailInput.value;
  if(!validateEmail(emailInputVal)){
    emailInput.classList.add('invalid-input');
    sumbitButton.disabled = true;
  }
  else {
    emailInput.classList.remove('invalid-input');
    sumbitButton.disabled = false;
  }
});


sumbitButton.addEventListener("click", function(event) {
    event.preventDefault();
    const emailInputVal = emailInput.value;

    if (validateEmail(emailInputVal)) {
        socket.emit("email_code_request", { email: emailInputVal });
    } 
  });
  

var socket = io();

socket.on("existing_user", function(response) {
  if (response.error) {
        alert("Пользователь с таким именем уже существует")
  } 
});

socket.on("reg_response", function(response) {
  if (response.success) {
        alert("Регистрация выполнена")
        window.location.href = "/";
  } 
});