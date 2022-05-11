var regex = new RegExp("^[a-z0-9_.-]*$");

function passOnChange() {
    const password = $("#password").val(),
        confirm = $("#confirm").val();
    if (regex.test(password)) {
        $("#password").get(0).setCustomValidity('');
        if (confirm === password) {
            $("#confirm").get(0).setCustomValidity('');
        } else {
            $("#confirm").get(0).setCustomValidity('Passwords do not match');
        }
    } else {
        $("#password").get(0).setCustomValidity('Account passwords are restricted to lowercase letters, numbers, dots, hyphens and underscores')
    }
}

$(document).ready(function () {
    $("#username").change(function () {
        const username = $("#username").val();
        if (regex.test(username)) {
            $("#username").get(0).setCustomValidity('');
        } else {
            $("#username").get(0).setCustomValidity('Account names are restricted to lowercase letters, numbers, dots, hyphens and underscores');
        }
    });

    $("#balance").change(function () {
        const balance = $("#balance").val();
        $("#balance").val(parseFloat(balance).toFixed(2));
    })

    $("#password").change(function () {
        passOnChange();
    });

    $("#confirm").change(function () {
        passOnChange();
    });
})


