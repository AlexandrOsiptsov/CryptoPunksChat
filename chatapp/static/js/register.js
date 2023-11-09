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

document.getElementById("register-btn").addEventListener("click", function(event) {
    event.preventDefault();
  
    let email = document.getElementById("email").value;
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm-password").value;
    //var errorMessage = document.getElementById("error-message");

    if (email != "" && username != "" && password != "" && confirmPassword != "" && password === confirmPassword) {
        socket.emit("reg",{username:username,password:password,email:email})
        //window.location.href = "/";
    } 
    else {
        alert('ТЫ ДАУН!!! ЗАПОЛНИ ВСЕ ПОЛЯ ИЛИ ПАРОЛИ НЕ СОВПАДАЮТ')
        //errorMessage.innerText = "Пароли не совпадают или одно из полей не заполнено";
        //errorMessage.style.display = "block";    
    }
  });
  