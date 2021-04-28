
function qrCode_modal_copy() {
    let copyText = document.getElementById('pubKey_textarea_modal');

    copyText.select();
    copyText.setSelectionRange(0, 99999);

    document.execCommand("copy");
    window.getSelection().removeAllRanges();
}

function qrCode_modal(data, name, add=" public key:", del=true) {
    let old = $('#QRcode_pubKey img');
    if (old != null) {
        old.remove();
    }

    let title = document.getElementById('table_item_text');
    let key   = document.getElementById('pubKey_textarea_modal');
    let qr    = document.getElementById('QRcode_pubKey');
    let delB  = document.getElementById('table_item_del');

    title.innerText = name + add;
    key.value = data;

    if (del == true) {
        delB.setAttribute("onclick", `del_friend_key('${name}')`);
    } else {
        delB.style.display = 'none';
    }

    new QRCode(qr, {
        text: data,
        width: 300,
        height: 300,
        colorDark : "#ffffff",
        colorLight : "#212529",
        correctLevel : QRCode.CorrectLevel.H
        });
    
    qr.style.title = "";
    $('#table_item_modal').modal();
}

function table_init(arr) {
    // eel.get_friends_keys() (table_init)
    let table_body  = document.getElementById('friends_table_body');
    let select      = document.getElementById('Select_pubKeys');

    $('#Select_pubKeys option').remove();

    while (table_body.rows[0]) {
        table_body.deleteRow(0);
    }

    if (arr.length == 0) {
        table_body.insertAdjacentHTML('beforeend', `<tr><th scope="row"><small style="font-size: 18px;" class="text-muted">You haven't friends public keys</small></th><td></td></tr>`);
        select.insertAdjacentHTML('beforeend', `<option value="">You haven't public keys!</option>`);
    }

    for ( let i = 0; i < arr.length; i++) {

        let name = arr[i]['nickname'];
        let pkey = arr[i]['key'];

        select.insertAdjacentHTML('beforeend', `<option value="${pkey}">${name}</option>`);

        if (pkey.length > 58) {
            pkeyShort = pkey.slice(0, 50) + '...';
        } else {
            pkeyShort = pkey;
        }

        table_body.insertAdjacentHTML('beforeend', `<tr onclick="qrCode_modal('${pkey}','${name}')"><th scope="row">${name}</th><td>${pkeyShort}</td></tr>`);
    }

}

function insert_pubKey(key) {
    element         = document.getElementById('pubKey_textarea')
    element.value   = key
}

// Init Function
function auth(status) {
    if (status == false) {
        $('#Error_pass').modal();
    } else {
        let page = document.getElementById('Login_page');
        let main = document.getElementById('Main');

        eel.get_friends_keys() (table_init)
        eel.get_messages_pubKey() (insert_pubKey)

        page.style.display = 'none';
        main.style.display = 'block';
    }
}

function login() {
    let pass = document.getElementById('password-input').value;
    let path = document.getElementById('file_input').value;

    eel.login(path, pass) (auth);
}

function loading_end() {
    $('#Loading_modal').modal('hide');
    $('#Done_file_creating').modal();
}

function create_new_file() {
    let name = document.getElementById('Form_nickname').value;
    let pass = document.getElementById('Form_password').value;

    $('#Create_file').modal('hide');
    $('#Loading_modal').modal();

    eel.create_file(name, pass) (loading_end);
}


// Friend keys Functions
function name_exists(status) {
    if (status == false) {
        $('#error_name_exists').modal();
    } else {
        eel.get_friends_keys() (table_init);
    }
}

function add_friend_key() {
    let name = document.getElementById('Add_Nickname').value;
    let key  = document.getElementById('Add_PubKey').value;

    if (name == '' || name == ' ' || key == '' || key == ' ') {
        $('#error_addFriend_args').modal();

    } else {
        eel.add_friend_key(name, key) (name_exists);
    }
}

function name_check(status) {
    if (status == false) {
        $('#error_del_name').modal();
    } else {
        $('#table_item_modal').modal('hide');
        $('#info_del_name').modal();
        
        eel.get_friends_keys() (table_init);
    }
}

function del_friend_key(name) {
    if (name == '' || name == ' ') {
        $('#error_del_name').modal();

    } else {
        eel.del_friend_key(name) (name_check);
    }
}


// Public Key Page
function copy_pubKey() {
    let copyText = document.getElementById('pubKey_textarea');

    copyText.select();
    copyText.setSelectionRange(0, 99999);

    document.execCommand("copy");
    window.getSelection().removeAllRanges();

    $('#Done_pubKey_copy').modal();
}


// Encrypt Key Page
function Encryption_output(Ciphertext) {
    if (Ciphertext == false) {
        $('#error_encryption').modal();

    } else {
        let out     = document.getElementById('Ciphertext_output');
        out.value   = Ciphertext;
    }
}

function Encrypt_text() {
    text = document.getElementById('Text_to_encrypt').value;
    key  = document.getElementById('Select_pubKeys').value;

    if (text == '' || text == ' ' || key == '' || key == ' ') {
        $('#error_encryption').modal();

    } else {
        eel._Encrypt(text, key) (Encryption_output);
    }
}


// Decrypt Key Page
function Decryption_output(Text) {
    if (Text == false) {
        $('#error_decryption').modal();

    } else {
        let out     = document.getElementById('Text_output');
        out.value   = Text;
    }
}

function Decrypt_text() {
    Ciphertext = document.getElementById('Text_to_decrypt').value;

    if (Ciphertext == '' || Ciphertext == ' ') {
        $('#error_decryption').modal();

    } else {
        eel._Decrypt(Ciphertext) (Decryption_output);
    }
}