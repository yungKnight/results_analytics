//const adjustChartsForSmallScreens = () => {
//  if (window.innerWidth < 767) { 
//    document.querySelectorAll('.chart-container .js-plotly-plot').forEach(plot => {
//      Plotly.relayout(plot, {
//        showlegend: false,
//        width: window.innerWidth * 0.95, 
//        height: 400 
//      });
//    });
//  }
//
//  if (window.innerWidth > 767 && window.innerWidth < 1025) {
//    const branch_gpa_removal = Array.from(document.querySelectorAll('.branch-gpa-chart .js-plotly-plot'));
//    const boxplot_removals = [
//      ...Array.from(document.querySelectorAll('.level-boxplot .js-plotly-plot')),
//      ...Array.from(document.querySelectorAll('.semester-boxplot .js-plotly-plot'))
//    ];
//    const branch_avg_removal = Array.from(document.querySelectorAll('.branch-avg-chart .js-plotly-plot'));
//    const pass_rate_removal = Array.from(document.querySelectorAll('.pass-rate-chart .js-plotly-plot'));
//    
//    const all_removals = [
//      ...branch_gpa_removal,
//      ...boxplot_removals,
//      ...branch_avg_removal,
//      ...pass_rate_removal
//    ];
//    console.log(Array.isArray(all_removals));
//
//    console.log(all_removals);
//
//    all_removals.forEach(removal => {
//      console.log(removal);
//      Plotly.relayout(removal, {
//        showlegend: false
//      });
//    });
//
//    document.querySelectorAll('.branch-pie-chart .js-plotly-plot').forEach(plot => {
//      Plotly.relayout(plot, {
//        'legend.font.size': 8,
//        'legend.width': 100,
//        'legend.height': 400 
//      });
//    });
//
//    branch_avg_removal.forEach(plot => {
//      Plotly.relayout(plot, {
//        'xaxis.showticklabels': false,
//        'xaxis.title.text': 'Semesters',
//        'xaxis.title.font.size': 14, 
//      });
//    });
//  }
//}
//adjustChartsForSmallScreens();



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