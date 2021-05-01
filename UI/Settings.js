

function settingsModal(text) {
    let textElement       = document.getElementById("Settings_info_modal_text");
    textElement.innerText = text;

    $("#Settings_info_modal").modal();
}

function initSettings(data) {
    let nickNameElement = document.getElementById("exampleInputNickname");

    let keyHashElement  = document.getElementById("KeyHash");

    let apiIdElement    = document.getElementById("api_id");
    let apiHashElement  = document.getElementById("api_hash");
    let apiPassElement  = document.getElementById("api_password");
    let apiPhoneElement = document.getElementById("api_phone");

    nickNameElement.value   = data["nickName"];

    keyHashElement.value    = data["privKeyHash"];

    apiIdElement.value      = data["api_id"];
    apiHashElement.value    = data["api_hash"];
    apiPassElement.value    = data["password"];
    apiPhoneElement.value   = data["phone"];

    $("#settingsModal").modal();
}

function saveSettings(data) {
    let nickNameElement = document.getElementById("exampleInputNickname");
    let passwordElement = document.getElementById("exampleInputPassword");

    let apiIdElement    = document.getElementById("api_id");
    let apiHashElement  = document.getElementById("api_hash");
    let apiPassElement  = document.getElementById("api_password");
    let apiPhoneElement = document.getElementById("api_phone");

    let res = {};

    if (nickNameElement.value != data["nickName"]) {
        res["nickName"] = nickNameElement.value;
    }
    if (passwordElement.value != "000000") {
        res["keyPassword"] = passwordElement.value;
    }

    if (apiIdElement.value != data["api_id"] || 
        apiHashElement.value != data["api_hash"] ||
        apiPassElement.value != data["password"] ||
        apiPhoneElement.value != data["phone"]) {
            
        res["api"] = {  "api_id": apiIdElement.value,
                        "api_hash": apiHashElement.value,
                        "password": apiPassElement.value,
                        "phone": apiPhoneElement.value,
                    };
    }

    eel.saveSettings(res);

    $('#settingsModal').modal("hide");
    settingsModal("All settings saved!");
}

function regeneratePrivKey() {
    $('#settingsModal').modal("hide");
    settingsModal("Your private key is regenerating!");

    eel.regeneratePrivKey();

    eel.get_messages_pubKey() (insert_pubKey);
}

function exportPrivKey(encKey) {
    $('#settingsModal').modal("hide");

    qrCode_modal(encKey, "Your encrypted private key: ", "", false, QRCode.CorrectLevel.L, 370, 370);
}