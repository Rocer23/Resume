// create a alert message, in red color (in form of rectangle with red background)
document.addEventListener('DOMContentLoaded', () => {
    function showAlert(message) {
        const alertBox = document.createElement('div');
        alertBox.className = 'alert alert-danger';
        alertBox.textContent = message;
        alertBox.style.position = 'fixed';
        alertBox.style.top = '20px';
        alertBox.style.right = '20px';
        alertBox.style.zIndex = '1000';
        alertBox.style.backgroundColor = 'red';
        alertBox.style.color = '#fff';
        
        document.body.appendChild(alertBox);
        setTimeout(() => {
            alertBox.remove();
        }, 3000);
    }
    // create a success message, in green color (in form of rectangle with green background)
    function showSuccess(message) {
        const successBox = document.createElement('div');
        successBox.className = 'alert alert-success';
        successBox.textContent = message;
        successBox.style.position = 'fixed';
        successBox.style.top = '20px';
        successBox.style.right = '20px';
        successBox.style.zIndex = '1000';
        successBox.style.backgroundColor = 'green';
        successBox.style.color = '#fff';
        
        document.body.appendChild(successBox);
        setTimeout(() => {
            successBox.remove();
        }, 3000);
    }

    // activate the showAlert and showSuccess functions
    // show alert under the login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (username === '' || password === '') {
                showAlert('Username and password cannot be empty.');
            } else {
                showSuccess('Login successful! Redirecting...');
                // Change the URL to the index page after 1.5 seconds
                setTimeout(()=> {
                    window.location.href = "/";
                }, 1500);
            }
        })
    }

    // show alert under the register form
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const name = document.getElementById('first_name').value;
            const surname = document.getElementById('last_name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (username === '' || name === '' || surname === '' || email === '' || password === '' || confirmPassword === '') {
                showAlert("All fields are required.");
            } else if (password !== confirmPassword) {
                showAlert("Passwords do not match.");
            } else {
                showSuccess('Registration successful! Redirecting...');
                // Change the URL to the index page after 1.5 seconds
                setTimeout(() => {
                    window.location.href = "/";
                }, 1500);
            }
        })
    }
})