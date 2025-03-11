document.addEventListener("DOMContentLoaded", () => {
    let now = new Date();
    let hour = now.getHours();
    let greetingText = "Good morning,";

    let timeImage = document.getElementById("time-of-day-img");
    
    let morningImg = timeImage.getAttribute("data-morning");
    let afternoonImg = timeImage.getAttribute("data-afternoon");
    let eveningImg = timeImage.getAttribute("data-evening");
    let lateNightImg = timeImage.getAttribute("data-late-night");

    let imgSrc = morningImg;

    if (hour >= 0 && hour < 6) {
        greetingText = "Happy late night,";
        imgSrc = lateNightImg;
    } else if (hour >= 6 && hour < 12) {
        greetingText = "Good morning,";
        imgSrc = morningImg;
    } else if (hour >= 12 && hour < 17) {
        greetingText = "Good afternoon,";
        imgSrc = afternoonImg;
    } else if (hour >= 17 && hour <= 23) {
        greetingText = "Good evening,";
        imgSrc = eveningImg;
    }

    document.getElementById("time-of-day").textContent = greetingText;
    timeImage.src = imgSrc;

    let textElement = document.getElementById("greetingText");
    if (textElement) {
        let text = textElement.textContent.trim();
        textElement.textContent = "";

        text.split("").forEach(letter => {
            let span = document.createElement("span");
            span.textContent = letter;
            span.style.opacity = "0";
            textElement.appendChild(span);
        });

        gsap.to("#greetingText span", {
            opacity: 1,
            duration: 0.02,
            stagger: 0.02,
            ease: "power4.out"
        });
    }
});
