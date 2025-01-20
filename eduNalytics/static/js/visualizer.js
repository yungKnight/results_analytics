console.log('Needed Data:', neededData);
console.log('-'.repeat(50))

const viewBtn = document.getElementById('view_analysis');
const advisory= document.getElementById('advisory');
const studentSpecificPerformance = document.getElementById('studentSpecificPerformance');
const studentSemesterPerformance = document.getElementById('studentSemesterPerformance');
const MoreOfOrNo =document.getElementById('toDoMoreOrNot');

advisory.style.display = "none";

viewBtn.addEventListener('click', () => {
  viewBtn.style.display = "none";
  advisory.style.display = advisory.style.display === "none" ? "block" : "none";
});
