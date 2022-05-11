var regex = new RegExp("^[a-z0-9_.-]*$");

function onChange() {
    const password = document.querySelector('input[id=password]');
    const confirm = document.querySelector('input[id=confirm]');
    if (testPassword()) {
        password.setCustomValidity('');
        if (confirm.value === password.value) {
            confirm.setCustomValidity('');
        } else {
            confirm.setCustomValidity('Passwords do not match');
        }
    } else {
        password.setCustomValidity('Account passwords are restricted to lowercase letters, numbers, dots, hyphens and underscores')
    }
}

function verifyUserName() {
    const username = document.querySelector('input[id=username]')
    if (regex.test(username.value)) {
        username.setCustomValidity('');
    } else {
        username.setCustomValidity('Account names are restricted to lowercase letters, numbers, dots, hyphens and underscores');
    }
}

function testPassword() {
    const password = document.querySelector('input[id=password]')
    return regex.test(password.value);
}

function setTwoNumberDecimal() {
    const balance = document.querySelector('input[id=balance]')
    balance.value = parseFloat(balance.value).toFixed(2);
}
