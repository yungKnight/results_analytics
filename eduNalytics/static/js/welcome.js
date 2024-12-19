const usernameInput = document.getElementById('username');
const submitButton = document.getElementById('submit');

usernameInput.addEventListener('input',() => {
    const username = usernameInput.value;

    console.log('Username input value:', username);

    if (regex.test(username)) {
        console.log('Valid username!');
    } else {
        console.log('Invalid username!');
    }
});

const regex = /^[A-Za-z]+(\s+[A-Za-z]*\s*)?$/;