// Header text animation when loading first time:
setTimeout(function () { document.getElementById('header-text').classList.add('show'); }, 50);

// Client connection to server
var socket = io();

function sendMsg(username, message) {
    var messageUserStr = username;
    var client_id = localStorage.getItem('client_id')
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
    setTimeout(function () { messageContainer.classList.add('show'); }, 50);

    var chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

//Преобразование десятичного числа, записанного в строке, в шестнадцатиричное, записанное в строке 
function dec2hex(str) {
    var dec = str.toString().split(''), sum = [], hex = [], i, s
    while (dec.length) {
        s = 1 * dec.shift()
        for (i = 0; s || i < sum.length; i++) {
            s += (sum[i] || 0) * 10
            sum[i] = s % 16
            s = (s - sum[i]) / 16
        }
    }
    while (sum.length) {
        hex.push(sum.pop().toString(16))
    }
    return hex.join('')
}

function emitMsgSending() {
    var messageTextStr = document.getElementById('msg-input-form').value;
    if (messageTextStr !== '') {
        console.log('Aes key is: ' + localStorage.getItem('AesKey256').toString())
        //Пример использования шифрования AES
        var encrypted = CryptoJS.AES.encrypt(messageTextStr, CryptoJS.enc.Hex.parse(dec2hex(localStorage.getItem('AesKey256'))), {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        console.log('hex key', dec2hex(localStorage.getItem('AesKey256')));
        console.log('encrypted', encrypted);
        socket.emit('chat_message_request', { username: localStorage.getItem('username'), client_id: localStorage.getItem('client_id'), message: messageTextStr });
        document.getElementById('msg-input-form').value = '';
    }
}

document.getElementById('send-msg-btn').addEventListener('click', function (event) {
    emitMsgSending();
});

document.getElementById('msg-input-form').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        emitMsgSending();
    }
});

socket.on('chat_message_response', function (response) {
    sendMsg(response.username, response.message);
})

