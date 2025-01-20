// Validate Phone Number (must be 10 digits)
function validatePhoneNumber(phone) {
    if (phone.length !== 10 || isNaN(phone)) {
        alert("Phone number must be exactly 10 digits.");
        return false;
    }
    return true;
}

// Validate Email (basic pattern)
function validateEmail(email) {
    const atSymbol = email.indexOf("@");
    const dotSymbol = email.indexOf(".", atSymbol);
    if (atSymbol === -1 || dotSymbol === -1 || email.length < 5) {
        alert("Please enter a valid email address.");
        return false;
    }
    return true;
}

// Validate Password (must be at least 6 characters)
function validatePassword(password) {
    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        return false;
    }
    return true;
}

// Function to validate the form before submission
function validateForm(event) {
    const phone = document.getElementById('add_phone').value;
    const email = document.getElementById('add_email').value;
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    // Check if phone, email, and password are valid
    if (!validatePhoneNumber(phone) || !validateEmail(email) || !validatePassword(password1)) {
        event.preventDefault();  // Prevent form from submitting if validation fails
        return false;
    }

    // Check if both passwords match
    if (password1 !== password2) {
        alert("Passwords do not match.");
        event.preventDefault();
        return false;
    }

    return true;  // Allow form submission if everything is valid
}
