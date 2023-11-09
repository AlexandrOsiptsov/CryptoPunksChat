var socket = io();

socket.on("existing_user", function(response) {
    if (response.error) {
         alert("Неверный пользователь")
    } 
  });

  socket.on("change_psw", function(response) {
    if (response.success) {
         alert("Пароль восстановлен")
         window.location.href = "/";
    } 
  });

document.getElementById("forgot-btn").addEventListener("click", function(event) {
    event.preventDefault();
  
    let username = document.getElementById("username").value;
    let newpassword = document.getElementById("newpassword").value;
    let confirmNEWPassword = document.getElementById("confirm-newpassword").value;

    if (username != "" && newpassword != "" && confirmNEWPassword != "" && newpassword === confirmNEWPassword) {
        socket.emit("forgot_psw",{username:username,newpassword:newpassword,confirmNEWPassword:confirmNEWPassword})
    } 
    else {
        alert('ТЫ ДАУН!!! ЗАПОЛНИ ВСЕ ПОЛЯ ИЛИ ПАРОЛИ НЕ СОВПАДАЮТ')
    }
  });