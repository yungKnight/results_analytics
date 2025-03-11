document.addEventListener("DOMContentLoaded", function () {
    let textElement = document.getElementById("greetingText");
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
});