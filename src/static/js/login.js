var socket = io();

sumbitButton = document.getElementById("join-btn")

sumbitButton.addEventListener("click", function(event) {
    event.preventDefault();

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username != '' && password != '') {
        socket.emit("login", { username: username, password: password })
        socket.emit("user_chat_join", { username: username });
        localStorage.setItem('username', username);

        sumbitButton.disabled = true
    }
});

socket.on("login_response", function(response) {
  if (response.success) {
       socket.emit('navigate', { url: '/chat' });
  } 
  else {
    alert("Неправильное имя пользователя или пароль");
  }
});

socket.on('navigate', function(data) {
    window.location.href = data.url;
});