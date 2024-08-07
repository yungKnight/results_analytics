document.addEventListener('DOMContentLoaded', function () {
    const nameForm = document.getElementById('name-form');
    const overlay = document.getElementById('name-overlay');
    const mainContent = document.getElementById('main-content');
    const greeting = document.getElementById('greeting');

    nameForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        greeting.textContent = 'Hello, ' + username;
        overlay.style.display = 'none';
        mainContent.style.display = 'block';
    });
});
