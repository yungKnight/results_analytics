document.addEventListener('DOMContentLoaded', () => {
    const analysisButton = document.querySelector('.btnContainer .btn-primary');
    const studentNameContainer = document.getElementById('student-name');
    const studentInfo = document.getElementsByClassName('personal-info');
    
    if (studentNameContainer) {
        let name = studentNameContainer.textContent.trim();
        console.log(name);
        studentNameContainer.textContent = "";
        name.split("").forEach(letter => {
            let span = document.createElement("span");
            span.textContent = letter;
            span.style.opacity = "0";
            studentNameContainer.appendChild(span);
        });
        
        const tl = gsap.timeline();
        
        tl.to("#student-name span", {
            opacity: 1,
            duration: 0.05,
            stagger: 0.03,
            ease: "power4.out"
        });
        
        tl.from(".personal-info", {
            opacity: 0,
            x: 50,
            duration: 1,
            stagger: 0.5,
            ease: "power2.out"
        });
    }
 
    if (analysisButton) {
        gsap.set(analysisButton, {opacity: 0, y: 40, scale: 1.2});
    
        const observer = new IntersectionObserver(entries => {
            let btnIsVisible = entries.filter(entry => entry.isIntersecting).map(entry => entry.target);
    
            gsap.to(btnIsVisible, {
                opacity: 1,
                scale: 1.0,
                y: 0,
                duration: 0.5,
                ease: 'power4.out'
            });
        });
    
        analysisButton.addEventListener('click', () => {
            window.location.href += 'insight/visual';
        });
        
        observer.observe(analysisButton);
    }
});