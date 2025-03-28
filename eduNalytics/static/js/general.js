let previousWidth = window.innerWidth;

window.addEventListener("resize", function () {
    let currentWidth = window.innerWidth;
    if (Math.abs(currentWidth - previousWidth) > 200) { 
        location.reload();
    }
});