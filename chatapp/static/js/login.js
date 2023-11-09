var socket = io();

document.getElementById("join-btn").addEventListener("click", function(event) {
    event.preventDefault()

    let username = document.getElementById("username").value;

    if(username != ''){
        socket.emit("user_chat_join", username);
        localStorage.setItem('username', username);
        socket.emit('navigate', {url: '/chat'});
    }
});


socket.on('navigate', function(data){
    window.location.href = data.url;
});