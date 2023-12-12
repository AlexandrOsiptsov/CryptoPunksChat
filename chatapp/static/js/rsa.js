
var form = document.getElementById('dataForm');
var clientIdInput = form.elements['client_id'];
var exponentInput = form.elements['exponent'];
var nValInput = form.elements['modulus'];


client_id = clientIdInput.value
localStorage.setItem('client_id', client_id);
exponent = exponentInput.value
modulus = nValInput.value

//Генерируем 256-битное число
function rnd256() {
    const bytes = new Uint8Array(32);

    window.crypto.getRandomValues(bytes);

    // byte array -> hex
    const bytesHex = bytes.reduce((o, v) => o + ('00' + v.toString(16)).slice(-2), '');

    // hex -> dec str
    return BigInt('0x' + bytesHex).toString(10);
}

//НОД
function gcd(a, b) {
    if (!a)
        return b;
    return gcd(b % a, a);
}


// 'a' - int,  'b' - str.
//Идея заключается в том, чтобы сделать второе число
//меньшим или равным первому числу
function reduceB(a, b) {
    let mod = 0n;

    // calculating mod of b with a to make
    // b like 0 <= b < a
    for (let i = 0; i < b.length - 1; i++)
        mod = (mod * 10 + b[i] - '0') % a;

    return mod;
}

// Возвращает нод а и b. b может быть очень большим
function gcdLarge(a, b) {

    let num = BigInt(reduceB(a, b));

    return gcd(a, num);
}

// НОД ?= 1
function isGCDone(a, b) {

    if (gcdLarge(a, b) != 1)
        return false;
    else
        return true;
}

// Получаем client ID, modulus и exponent
function getClientId() {

    if (!client_id || !exponent || !modulus) {
        fetch('/get_client_id')
            .then(response => response.json())
            .then(data => {
                client_id = data.client_id;
                exponent = data.exponent;
                modulus = data.modulus;
                localStorage.setItem('client_id', client_id);
                document.getElementById('client-id').innerText = client_id;
            })
            .catch(error => {
                console.error('GetClientId error:', error);
            });
    } else {
        document.getElementById('client-id').innerText = client_id;
    }
}

// Отображаем инфо клиента 
function displayData() {

    if (client_id && exponent && modulus) {
        console.log('Data from client storage:', client_id, exponent, modulus);
    } else {
        console.log('No data in client storage');
        getClientId();
    }
}


//Модулярное возведение в степень
function modPow(expo, base, p) {
    let x = BigInt(base) % p, res = expo & 1n ? x : 1n
    do {
        x = x ** 2n % p
        if (expo & 2n) res = res * x % p
    } while (expo /= 2n)
    return res
}


// Шифрование
function encrypt(msg, exponent, modulus) {

    if (msg < 0n || msg >= modulus) {

        throw new Error(`Condition 0 <= msg < modulus not met. msg = ${msg}; ${modulus}`);
    }

    if (isGCDone(msg, modulus)) {
        throw new Error(`Condition gcd(msg, modulus) = 1 not met. msg = ${msg}; ${modulus}`);
    }

    return modPow(exponent, msg, modulus);
}

// POST запрос с зашифрованным ключом AES
function sendData() {
  
    let aes_key = BigInt(rnd256());
    localStorage.setItem('AesKey256', aes_key.toString(10));
    let encrypted_aes_key = encrypt(aes_key, BigInt(exponent), BigInt(modulus)).toString();
    console.log('Data transaction ended:', encrypted_aes_key);
    console.log('AES_KEY in SENDDATA: ' + aes_key)

    const request = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            client_id: client_id,
            e_msg: encrypted_aes_key
        }),
    };

    fetch('/process_data', request)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('SendData Error:', error);
        });
}



document.addEventListener('DOMContentLoaded', function () {
    displayData();
    sendData();
});
