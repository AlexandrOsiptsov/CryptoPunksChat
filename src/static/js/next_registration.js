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
  
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm-password").value;
    const storedEmail = localStorage.getItem("email");
    
    if (password != confirmPassword){
      alert('Пароли не совпадают');
    }
    else if (username == '' || password == '' || confirmPassword == ''){
      alert('Заполни все поля');
    }
    else {
      socket.emit('reg', {username: username, password: password, email: storedEmail});
    }
  });