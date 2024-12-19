const usernameInput = document.getElementById('username');
const submitButton = document.getElementById('submit');

const regex = /^(\s)?[A-Za-z]+(\s+[A-Za-z]*\s*)?$/;

submitButton.addEventListener('click', (e) => {
    const username = usernameInput.value.trim();
    console.log(username)

    if (!regex.test(username)) {
        e.preventDefault();
        alert('Invalid username! Please enter a valid name using alphabets only.');
    }
});