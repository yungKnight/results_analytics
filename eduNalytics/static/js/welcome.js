const usernameInput = document.getElementById('username');
const submitButton = document.getElementById('submit');

const regex = /^(\s)?[A-Za-z]+(\s+[A-Za-z]*\s*)?$/;

submitButton.addEventListener('click', (e) => {
    const username = usernameInput.value.trim();

    if (!regex.test(username)) {
        e.preventDefault();
        alert('Invalid username! Please enter a valid name using alphabets only.');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.step-card');

    gsap.set(cards, { opacity: 0, y: 20, scale: 1.1 });

    const observer = new IntersectionObserver(entries => {
        let visibleCards = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);

        if (visibleCards.length) {
            gsap.to(visibleCards, {
                opacity: 1,
                y: 0,
                scale: 1.0,
                duration: 0.5,
                stagger: 0.4,
                ease: 'power2.out'
            });

            visibleCards.forEach(card => observer.unobserve(card));
        }
    }, { threshold: 0.5 });

    cards.forEach(card => observer.observe(card));
});