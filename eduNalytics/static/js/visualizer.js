document.addEventListener("DOMContentLoaded", () => {
 
  const initAutoScroll = () => {
    if (window.innerWidth >= 768) {
      return;
    }
 
   gsap.registerPlugin(ScrollToPlugin);

   const container = document.querySelector(".semester-distribution-inner");
   const items = document.querySelectorAll(".semester-distribution-item");
 
    if (!container || items.length === 0) {
      return;
    }
 
    let currentIndex = 0;
    const itemWidth = items[0].offsetWidth;
    const totalItems = items.length;
    let isUserScrolling = false;
    let scrollTimeout;
 
    const scrollToNext = () => {
      if (isUserScrolling) {
        return;
      }
 
      currentIndex = (currentIndex + 1) % totalItems;
 
      gsap.to(container, {
        duration: 1,
        scrollTo: { x: itemWidth * currentIndex },
        ease: "power2.inOut",
      });
    }
 
    function updateIndexFromScroll() {
      const scrollLeft = container.scrollLeft;
      currentIndex = Math.round(scrollLeft / itemWidth);
    }
 
    container.addEventListener("scroll", () => {
      isUserScrolling = true;
      clearTimeout(scrollTimeout);
 
      scrollTimeout = setTimeout(() => {
        isUserScrolling = false;
        updateIndexFromScroll();
      }, 1000);
    });
 
    setInterval(scrollToNext, 3000);
  }
 
  initAutoScroll();
});