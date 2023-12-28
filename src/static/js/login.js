const res = require("express/lib/response");

var socket = io();

sumbitButton = document.getElementById("join-btn");

sumbitButton.addEventListener("click", function(event) {
    event.preventDefault();
    alert("КАКОЙ-ТО АЛЕРТ111");
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (email != '' && password != '') {
        socket.emit("login_request", { email: email, password: password });
        alert("КАКОЙ-ТО АЛЕРТ");
        sumbitButton.disabled = true;
    }
});

socket.on("login_response", function(response) {
  if (response.success) {
    localStorage.setItem("clientname", response.clientname);
    localStorage.setItem("clientcolor", response.clientcolor);
    socket.emit('navigate', { url: '/chat' });
  } 
  else {
    alert("Неправильное имя пользователя или пароль");
  }
});

socket.on('navigate', function(data) {
    window.location.href = data.url;
});