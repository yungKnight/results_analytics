document.addEventListener('DOMContentLoaded', () => {
    const analysisButton = document.querySelector('.btnContainer .btn-primary');
    
    if (analysisButton) {
        analysisButton.addEventListener('click', () => {
            window.location.href += 'insight/visual';
        });
    }
});