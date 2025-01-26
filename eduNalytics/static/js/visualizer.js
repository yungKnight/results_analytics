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

//console.log(neededData);
//console.log('-'.repeat(50));
////console.log(compulsoryChecks);
//console.log('-'.repeat(50));
//console.log(studentSpecificChecks);
console.log('-'.repeat(50));

const { status, type } = semesterPerformance;
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
const semesterPerformanceOverview = ({ status, type }) => {
    if (status === "divergence" &&
     sharedMeanings[status] && 
     sharedMeanings[status][type]) {
        console.log(`${sharedMeanings[status][type]}`);
        console.log('-'.repeat(45));
    } else if (status === "convergence" &&
        sharedMeanings[status] && 
        sharedMeanings[status][type]) {
          console.log(`${sharedMeanings[status][type]}`);
          console.log('-'.repeat(45));
    } else if (status === "At equilibrium state" &&
        sharedMeanings[status] && 
        sharedMeanings[status][type]) {
          console.log(`${sharedMeanings[status][type]}`);
          console.log('-'.repeat(45));
    }
};
semesterPerformanceOverview(semesterPerformance);

const processEmasSemesterChecks = (checks) => {
  Object.entries(checks).forEach(([key, { crossover, cross_type }]) => {
    const compulsoryKeysRegex = /^([A-Za-z]+)_and_([A-Za-z]+)_(\w+)$/;
    const validCCKey = key.match(compulsoryKeysRegex);

    const personalKeysRegex = /^([A-Za-z]+)_[A-Za-z]+_and_(.+)$/;
    const validSSCkey = key.match(personalKeysRegex);

    if (validSSCkey) {
      let comparisonAvg = validSSCkey[1];
      let currAvg = validSSCkey[2];

      if (crossover) {
        if (cross_type === "positive") {
          console.log(`Student is performing better in courses from this branch- ${
            currAvg} than their ${
              comparisonAvg === "cgpa" ? "long-term" : ""} adjusted average`);
        } else if (cross_type === "negative") {
          console.log(`Student's performance is getting worse in courses from this branch- ${
            currAvg} than their ${
              comparisonAvg === "cgpa" ? "long-term" : ""} adjusted average`);
        }
      }
    }

    if (validCCKey) {
      let comparisonAvg = validCCKey[1];
      let currAvg = validCCKey[2];
      let ema = validCCKey[3];

      const multiEmaCheck = ema === 'emas';

      if (!multiEmaCheck) {
        if (crossover) {
          cross_type === "positive" 
            ? console.log(`The student's most recent performance reflected in ${
                comparisonAvg} is now better than their ${currAvg} historical adjusted average`)
            : console.log(`The student's most recent performance reflected in ${
                comparisonAvg} is now worse than their ${currAvg} historical adjusted average`);
        }

      } else {
        if (crossover) {
          cross_type === "positive" 
            ? console.log(`The student's most recent performance in ${comparisonAvg
                } adjusted averaging is now better than their ${currAvg} historical adjusted average`)
            : console.log(`The student's most recent performance in ${comparisonAvg
                } adjusted averaging is now worse than their ${currAvg} historical adjusted average`);
        }
      }
      console.log('='.repeat(40));
    }
  });
}
processEmasSemesterChecks(compulsoryChecks);
processEmasSemesterChecks(studentSpecificChecks);


const correlation_data = neededData["filtered_corr_data"];
const corrMeaning = ({ key, strength, type }) => {
    if (strength === "Very Strong") {
        return `The relationship between ${key[0]} and ${key[1]} is ${strength} ${
            type === "Negative" ? "but" : "and"
        } ${type}`;
    }
    return `The relationship between ${key[0]} and ${key[1]} is ${strength}ly ${type}`;
};
/*This set of meanings below will be a part of an object that disseminates final messages
  to the frontend-
    This would be used to advise overall on impact of the 
    total units and courses offered per semester with the ones against cgpa the tests
    for some kind of divergence e.g if any of the key[1] contains 'cgpa' and an inverse value
                                    might mean a disparity in potential
    (for me to recall faster)*/
const correlationMeanings = correlation_data.map(item => corrMeaning(item));
console.log(`${'=*'.repeat(20)}`);
console.log(correlationMeanings);
//console.log(Array.isArray(correlationMeanings))
//console.log(`${'=*'.repeat(20)}`);


const partial_correlation_data = neededData["filtered_par_corr_data"];
const parCorrMeaning = ({ key, significance, strength, type }) => {
    const keyRegex = /^([a-zA-Z\s]+)(?:_([a-zA-Z]+))?$/;

    const validPredictor = key[0].match(keyRegex);
    const validKeys = validPredictor && keyRegex.test(key[1]) ? true : false;
    
    if (validKeys) {
      const predictorBranch = validPredictor[1];
      const predictorSuffix = validPredictor[2] || null;
      
      if (!predictorSuffix) {
        return `The impact of ${key[0]} branch on ${key[1]} is considered ${type}ly ${
          strength
        } in nature and also ${significance} statistically`
      } else if (predictorSuffix === "units") {
        if (key[1] === 'cgpa') {
          return type === "Positive" 
            ? `Student should look to offer more units from ${
              predictorBranch} as it is beneficial in the long run`
            : `Student should avoid taking courses from ${
              predictorBranch} if possible as its long-run negative effect is glaring`
        }
        return type === "Positive" 
          ? `Student should look to offer more units from ${predictorBranch}`
          : `Student should avoid taking courses from ${predictorBranch} if possible`
      } else if (predictorSuffix === "count") {
        if (key[1] === 'cgpa') {
          return type === "Positive" 
            ? `Student should look to offer more courses from ${
              predictorBranch} as it is beneficial in the long run`
            : `Student should avoid taking courses from ${
              predictorBranch} if possible as its long-run negative effect is glaring`
        }
        return type === "Positive" 
          ? `Student should look to offer more courses from ${predictorBranch}`
          : `Student should avoid taking courses from ${predictorBranch} if possible`
      }
    }
}
const parCorrelationMeanings = partial_correlation_data.map(item => parCorrMeaning(item));
console.log(parCorrelationMeanings)
//console.log(Array.isArray(parCorrelationMeanings))
console.log('=*'.repeat(20));

viewBtn.addEventListener('click', () => {
  viewBtn.style.display= "none";
  advisory.style.display = "block";
  //studentSemesterPerformance.textContent = "Yes Baby"
});

minimizeBtn.addEventListener('click', () => {
  advisory.style.display = "none";
  viewBtn.style.display = "block";
});
