
function table_init(arr) {
    // eel.get_friends_keys() (table_init)
    let table_body = document.getElementById('friends_table_body');

    while (table_body.rows[0]) {
        table_body.deleteRow(0);
    }

    if (arr.length == 0) {
        table_body.insertAdjacentHTML('beforeend', `<tr><th scope="row"><small style="font-size: 18px;" class="text-muted">You haven't friends public keys</small></th><td></td></tr>`);
    }

    for ( let i = 0; i < arr.length; i++) {

        let name = arr[i]['nickname'];
        let pkey = arr[i]['key'];

        if (pkey.length > 58) {
            pkey = pkey.slice(0, 50) + '...';
        }

        table_body.insertAdjacentHTML('beforeend', `<tr><th scope="row">${name}</th><td>${pkey}</td></tr>`);
    }

}

function auth(status) {
    if (status == false) {
        $('#Error_pass').modal();
    } else {
        let page = document.getElementById('Login_page');
        let main = document.getElementById('Main');

        eel.get_friends_keys() (table_init)

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
        eel.get_friends_keys() (table_init);
    }
}

function del_friend_key() {
    let name = document.getElementById('Del_Nickname').value;

    if (name == '' || name == ' ') {
        $('#error_del_name').modal();

    } else {
        eel.del_friend_key(name) (name_check);
    }
}