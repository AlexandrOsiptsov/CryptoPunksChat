// Header text animation when loading first time:
setTimeout(function(){document.getElementById('header-text').classList.add('show');}, 50);

// Client connection to server
var socket = io();

function sendMsg(username, message) {
    var messageUserStr = username;
    var messageTextStr = message;

    var messageContainer = document.createElement('div');
    messageContainer.classList.add('msg-container');

    messageUser = document.createElement('div');
    messageUser.classList.add('msg-user');
    messageUser.textContent = messageUserStr; 

    messageText = document.createElement('div');
    messageText.classList.add('msg-text');
    messageText.textContent = messageTextStr;

    messageContainer.appendChild(messageUser);
    messageContainer.appendChild(messageText);

    document.getElementById('chat-box').appendChild(messageContainer);
    setTimeout(function() { messageContainer.classList.add('show'); }, 50);

    var chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

function emitMsgSending(){
    var messageTextStr = document.getElementById('msg-input-form').value;
    if(messageTextStr !== ''){
        socket.emit('chat_message_request', {username: localStorage.getItem('username'), message: messageTextStr});
        document.getElementById('msg-input-form').value = '';
    }
}

document.getElementById('send-msg-btn').addEventListener('click', function(event) {
    emitMsgSending();
  });

document.getElementById('msg-input-form').addEventListener('keydown', function(event) {
    if(event.key === 'Enter'){
        emitMsgSending();
    }
});

socket.on('chat_message_response', function(response){
    sendMsg(response.username, response.message);
})

