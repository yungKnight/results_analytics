/*console.log('Needed Data:', neededData);
console.log('-'.repeat(50))*/

const viewBtn = document.getElementById('view_analysis');
const minimizeBtn = document.getElementById('minimize_analysis');
const advisory= document.getElementById('advisory');
const studentSpecificPerformance = document.getElementById('studentSpecificPerformance');
const studentSemesterPerformance = document.getElementById('studentSemesterPerformance');
const MoreOfOrNo =document.getElementById('toDoMoreOrNot');

advisory.style.display = "none";

const { 
  "semester performance": semesterPerformance, 
  "necessary checks": compulsoryChecks, 
  "personal checks": studentSpecificChecks 
} = neededData["filtered_emas_data"];

console.log(neededData["filtered_corr_data"]);
console.log('-'.repeat(50));

const { status, type} = semesterPerformance;

const sharedMeanings = {
  "divergence": {
    "positive": "Reinforce that recent performance is improving but advise on sustaining the trend.",
    "negative": "Warn the student about the risk of misalignment between recent performance and overall trends and suggest corrective measures."
  },
  "convergence": {
    "positive": "Encourage the student by highlighting their improving consistency.",
    "negative": "Alert the student to a potential decline and suggest actionable steps, such as seeking academic support or focusing on specific subjects.",
    "flattening": "Student's perormance is starting to improve signaling potential to get better in the long run"
  },
  "At equilibrium state": {
    "positive": "The relationship remains stable, the student's semester GPA is higher than the previous semester.",
    "negative": "The relationship remains stable, but the student's semester GPA is lower than the previous semester.",
    "steady": "The student is in a steady state and strategies to help them from dipping should be made.",
    "exemplary": "Outstanding! You have achieved a perfect GPA! Keep up the great work!"
  }
};

const extractSemesterPerformanceMeanings = (attribute) => {
  return Object.keys(sharedMeanings).reduce((acc, key) => {
    const meaning = sharedMeanings[key][attribute];
    meaning ? acc[key] = meaning : acc;
    return acc;
  }, {});
};

const negativeMeanings = extractSemesterPerformanceMeanings("negative");
const positiveMeanings = extractSemesterPerformanceMeanings("positive"); 
const flatteningMeaning = extractSemesterPerformanceMeanings("flattening");
const steadyMeaning = extractSemesterPerformanceMeanings("steady");
const exemplaryMeaning = extractSemesterPerformanceMeanings("exemplary");

viewBtn.addEventListener('click', () => {
  viewBtn.style.display= "none";
  advisory.style.display = "block";
  //studentSemesterPerformance.textContent = "Yes Baby"
});

minimizeBtn.addEventListener('click', () => {
  advisory.style.display = "none";
  viewBtn.style.display = "block";
});
