
let initVar = {
    password: $('#id_password'),
    error: $('#error'),
}


let validScript = {
    initVar,

    activeEvent() {
        $("#auth-form").submit(function (e) {
                e.preventDefault();
                let serializedData = $(this).serialize();
                $.ajax({
                    type: 'POST',
                    url: url_view,
                    data: serializedData,
                    script: this,
                    success: function (response) {
                        validScript.checkOperation(response)
                    },
                    error: function (response) {
                        alert('Invalid request');
                    },
                })
         })
    },

    checkOperation(response) {
        if (response.status) {
            this.redirectToHome();
        }
        else {
            this.notValid(response);
        }
    },

    redirectToHome() {
        window.location.replace(url_redirect);
    },

    notValid(response) {
        if ($("#error")) {
            $("#error").remove()
        }
        $('label[for=id_email]').before(this.getErrorText(response.message))
    },

    getErrorText(message) {
        return '<div id="error" class="invalid-feedback d-block" ' +
            'id="usernameError"><p class="text-danger">' + message +'</p></div>'
    }
}

$(document).ready(function () {
    validScript.activeEvent()
})
