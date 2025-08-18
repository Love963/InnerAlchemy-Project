document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', function (e) {
        const password1 = form.querySelector('input[name="password1"]');
        const password2 = form.querySelector('input[name="password2"]');
        if (password1 && password2 && password1.value !== password2.value) {
            alert('Passwords do not match!');
            e.preventDefault();
        }
    });
});