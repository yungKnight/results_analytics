const viewBtn = document.getElementById('view_analysis');
const minimizeBtn = document.getElementById('minimize_analysis');
const advisory= document.getElementById('advisory');
const studentSpecificPerformance = document.getElementById('studentSpecificPerformance');
const studentSemesterPerformance = document.getElementById('studentSemesterPerformance');
const MoreOfOrNo =document.getElementById('toDoMoreOrNot');

let semesterOverview;
advisory.style.display = "none";

const emas_data = neededData ? neededData["filtered_emas_data"] : null;
const correlation_data = neededData ? neededData["filtered_corr_data"] : null;
const partial_correlation_data = neededData ? neededData["filtered_par_corr_data"] : null;

const { 
  "semester performance": semesterPerformance, 
  "necessary checks": compulsoryChecks, 
  "personal checks": studentSpecificChecks 
} = emas_data
console.log(neededData);
console.log('-'.repeat(50));

if (semesterPerformance) {
  const { status, type } = semesterPerformance;
  const semesterPerformanceMeanings = {
  "divergence": {
    "positive": "Your recent performance is improving! Stay consistent and continue reinforcing strong study habits.",
    "negative": "Your recent performance is deviating from overall trends. Identify weak areas and take corrective action to stay on track."
  },
  "convergence": {
    "positive": "Great progress! Your consistency is improving, maintain focus and keep building on current momentum.",
    "negative": "Your performance is declining toward a concerning trend. Consider seeking academic support or prioritizing key subjects.",
    "flattening": "Your performance is beginning to stabilize with potential to get better. Stay dedicated to see long-term gains."
  },
  "At equilibrium state": {
    "positive": "You're maintaining a stable trend with a higher semester GPA than before. Keep up the good work!",
    "negative": "Your performance is stable, but your semester GPA has dropped. Reflect on challenges and adjust strategies accordingly.",
    "steady": "You're in a steady state. Implement strategies to prevent dips and sustain progress.",
    "exemplary": "Outstanding achievement! You've attained a perfect GPA—continue your excellent efforts!"
  }
  };
  const semesterPerformanceOverview = ({ status, type }) => {
    if (status === "divergence" &&
     semesterPerformanceMeanings[status] && 
     semesterPerformanceMeanings[status][type]) {
        return `${semesterPerformanceMeanings[status][type]}`;
    } else if (status === "convergence" &&
        semesterPerformanceMeanings[status] && 
        semesterPerformanceMeanings[status][type]) {
          return `${semesterPerformanceMeanings[status][type]}`;
    } else if (status === "At equilibrium state" &&
        semesterPerformanceMeanings[status] && 
        semesterPerformanceMeanings[status][type]) {
          return `${semesterPerformanceMeanings[status][type]}`;
    }
  };
  semesterOverview = semesterPerformanceOverview(semesterPerformance);
}
console.log("semester overview: \n")
console.log('-'.repeat(15))
console.log(semesterOverview);
console.log(typeof semesterOverview);
console.log('-'.repeat(45))

if (!compulsoryChecks) {
  const processCompulsoryChecks = (checks) => {
  const compulsoryMessages = [];
  
  Object.entries(checks).forEach(([key, { crossover, cross_type }]) => {
    const compulsoryKeysRegex = /^([A-Za-z]+)_and_([A-Za-z]+)_(\w+)$/;
    const validCCKey = key.match(compulsoryKeysRegex);
    if (validCCKey) {
      let comparisonAvg = validCCKey[1];
      let currAvg = validCCKey[2];
      let ema = validCCKey[3];
      const multiEmaCheck = ema === 'emas';
      
      if (!multiEmaCheck && crossover) {
        compulsoryMessages.push(
          cross_type === "positive" 
            ? `Your latest performance in ${comparisonAvg} has improved beyond your ${
                currAvg === 'cgpa' 
                  ? "long-term" : ""} historical average. Keep up the progress!`
            : `Your latest performance in ${comparisonAvg} has dropped below your ${
                currAvg === 'cgpa' 
                  ? "long-term" : ""} historical average. Consider reviewing your study strategies.`
        );
      } else if (multiEmaCheck && crossover) {
        compulsoryMessages.push(
          cross_type === "positive" 
            ? `Your recent performance in ${comparisonAvg} has surpassed your ${
                currAvg} historical trend. Keep doing what you have!`
            : `Your recent performance in ${comparisonAvg} has fallen below your ${
                currAvg} historical trend. Take necessary action(s) to improve.`
        );
      }
    }
  });
  return compulsoryMessages;
  };
  const compulsoryChecksMeanings = processCompulsoryChecks(compulsoryChecks);
  //console.log("semester compulsory checks: \n")
  //console.log('-'.repeat(15))
  //console.log(compulsoryChecksMeanings);
  //console.log(typeof compulsoryChecksMeanings);
}

if (!studentSpecificChecks) {
  const processPersonalChecks = (checks) => {
  const personalMessages = [];

  Object.entries(checks).forEach(([key, { crossover, cross_type }]) => {
    const personalKeysRegex = /^([A-Za-z]+)_[A-Za-z]+_and_(.+)$/;
    const validSSCkey = key.match(personalKeysRegex);

    if (validSSCkey) {
      let comparisonAvg = validSSCkey[1];
      let currAvg = validSSCkey[2];

      if (crossover) {
        if (cross_type === "positive") {
          personalMessages.push(`Great job! Your performance in ${currAvg} courses has surpassed your ${
            comparisonAvg === "cgpa" 
              ? "long-term " : ""}average. Keep building on this progress!`);
        } else if (cross_type === "negative") {
          personalMessages.push(`Your performance in ${currAvg} courses has dropped below your ${
            comparisonAvg === "cgpa" 
              ? "long-term " : ""}average. Take action to get back on track.`);
        }
      }
    }
  });
  return personalMessages;
  };
  const personalChecksMeanings = processPersonalChecks(studentSpecificChecks);
  //console.log("student specific checks: \n")
  //console.log('-'.repeat(15))
  //console.log(personalChecksMeanings)
  //console.log(typeof personalChecksMeanings);
}

if (correlation_data != []) {
  const expectedVariables = ["total_units", "gpa", "cgpa", "semester_course_count"];
  const correlationPairMeanings = {
  "very negative": {
    [expectedVariables[0]]: {
      [expectedVariables[1]]: "Strongly consider reducing your course load to prevent further academic strain.",
      [expectedVariables[2]]: "To avoid long-term setbacks, consider taking fewer units moving forward."
    },
    [expectedVariables[1]]: {
      [expectedVariables[2]]: "Your recent performance has significantly impacted your overall GPA. Immediate improvement is crucial.",
      [expectedVariables[3]]: "Reduce your course load now to prevent further performance decline.",

    },
    [expectedVariables[2]]: {
      [expectedVariables[3]]: "Lowering your course load can help mitigate long-term academic risks."
    }
  },
  "negative": {
    [expectedVariables[0]]: {
      [expectedVariables[1]]: "Consider reducing your course load to maintain academic balance.",
      [expectedVariables[2]]: "Reducing total units may help improve long-term performance."
    },
    [expectedVariables[1]]: {
      [expectedVariables[2]]: "Your recent performance has negatively affected your GPA. Take steps to improve.",
      [expectedVariables[3]]: "Reducing courses soon may help prevent further GPA decline.",
    },
    [expectedVariables[2]]: {
      [expectedVariables[3]]: "A lower course load could improve your long-term academic performance."
    }
  },
  "slightly negative": {
    [expectedVariables[0]]: {
      [expectedVariables[1]]: "You may benefit from reducing your course load slightly.",
      [expectedVariables[2]]: "A small reduction in units may support long-term improvement."
    },
    [expectedVariables[1]]: {
      [expectedVariables[2]]: "Your performance is slightly declining. Stay cautious and make adjustments as needed.",
      [expectedVariables[3]]: "Reducing your course load now may help reverse short-term performance dips."  
    },
    [expectedVariables[2]]: {
      [expectedVariables[3]]: "Consider reducing your courses to counteract long-term negative effects." 
    }
  },
  "slightly positive": {
    [expectedVariables[0]]: {
      [expectedVariables[1]]: "Consider increasing your course load slightly to take advantage of your progress.",
      [expectedVariables[2]]: "If sustained, adding more units could be beneficial in the long run."
    },
    [expectedVariables[1]]: {
      [expectedVariables[2]]: "Your recent performance is slightly improving. Keep building on this progress!",
      [expectedVariables[3]]: "Increasing your course load now could help maximize your momentum." 
    },
    [expectedVariables[2]]: {
      [expectedVariables[3]]: "Sustained performance improvements may allow you to handle more courses next semester."
    }
  },
  "positive": {
    [expectedVariables[0]]: {
      [expectedVariables[1]]: "Your performance is strong, consider adding more courses if feasible.",
      [expectedVariables[2]]: "With consistent performance, adding more units may benefit your long-term growth."
    },
    [expectedVariables[1]]: {
      [expectedVariables[2]]: "Great job! Your performance is improving overall, stay on this path.",
      [expectedVariables[3]]: "Expanding your course load now could help accelerate academic progress." 
    },
    [expectedVariables[2]]: {
      [expectedVariables[3]]: "Sustained success may allow you to take on more challenging courses in the future."    
    }
  },
  "very positive": {
    [expectedVariables[0]]: {
      [expectedVariables[1]]: "You're excelling! If manageable, consider adding more courses to challenge yourself.",
      [expectedVariables[2]]: "Your strong performance suggests you could take on more courses for long-term benefits."
    },
    [expectedVariables[1]]: {
      [expectedVariables[2]]: "Outstanding work! Your performance is consistently improving, keep pushing forward.",
      [expectedVariables[3]]: "Consider increasing your course load to fully leverage your academic growth."
    },
    [expectedVariables[2]]: {
      [expectedVariables[3]]: "Your exceptional performance could support a more ambitious course load next semester."    
    }
  }
  };
  const extractCorrMeaning = ({ key, strength, type }) => {
  if (!expectedVariables.includes(key[0]) || !expectedVariables.includes(key[1])) {
    return;
  }

  let correlationType;

  if (strength === "Moderate") {
    correlationType = type === "Negative" ? "slightly negative" : "slightly positive";
  } else if (strength === "Strong") {
    correlationType = type === "Negative" ? "negative" : "positive";
  } else if (strength === "Very Strong") {
    correlationType = type === "Negative" ? "very negative" : "very positive";
  }

  return correlationPairMeanings[correlationType]?.[key[0]]?.[key[1]];
  };
  const correlationMeanings = correlation_data.map(item => extractCorrMeaning(item));
  //console.log(`${'=*'.repeat(20)}`);
  //console.log("Correlation inference:")
  //console.log('-'.repeat(15))
  //console.log(correlationMeanings);
  //console.log(`${'+'.repeat(20)}`);
}

if (partial_correlation_data) {
  const parCorrMeaning = ({ key, significance, strength, type }) => {
    const keyRegex = /^([a-zA-Z\s]+)(?:_([a-zA-Z]+))?$/;
    const validPredictor = key[0].match(keyRegex);
    const validKeys = validPredictor && keyRegex.test(key[1]);

    if (validKeys) {
      const predictorBranch = validPredictor[1];
      const predictorSuffix = validPredictor[2] || null;

      if (!predictorSuffix) {
        return {
          message: `The influence of ${key[0]} on ${key[1]} is ${
            type.toLowerCase()}ly ${strength} and statistically ${significance}.`,
          suffix: predictorSuffix
        }
      } 
      
      if (predictorSuffix === "units") {
        if (key[1] === 'cgpa') {
          return {
            message: type === "Positive" 
              ? `Taking more units from ${predictorBranch} can benefit your long-term performance.`
              : `Reducing courses from ${predictorBranch} may help avoid long-term negative effects.`,
            suffix: predictorSuffix
          };
        }
        return {
          message: type === "Positive" 
            ? `Consider taking more units from ${predictorBranch}.`
            : `It may be beneficial to limit courses from ${predictorBranch}.`,
          suffix: predictorSuffix
        };
      } 
      if (predictorSuffix === "count") {
        if (key[1] === 'cgpa') {
          return {
            message: type === "Positive" 
              ? `Adding more courses from ${predictorBranch} could boost your long-term performance.`
              : `Avoiding courses from ${predictorBranch} may help prevent negative academic impact.`,
            suffix: predictorSuffix
          };
        }
        return {
          message: type === "Positive" 
            ? `Consider taking more courses from ${predictorBranch}.`
            : `Reducing courses from ${predictorBranch} might be a good strategy.`,
          suffix: predictorSuffix
        };
      }
    }
  };
  const parCorrelationMeanings = partial_correlation_data.map(item => parCorrMeaning(item));
  //console.log("Partial Correlation inference:")
  //console.log('-'.repeat(15))
  //console.log(parCorrelationMeanings)
  //console.log('=*'.repeat(20));
}

/*This set of meanings above will be a part of an object that disseminates final messages
  to the frontend-
    This would be used to advise overall on impact of the 
    total units and courses offered per semester with the ones against cgpa the tests
    for some kind of divergence e.g if any of the key[1] contains 'cgpa' and an inverse value
                                    might mean a disparity in potential
    (for me to recall faster)*/

/* The function below is would be responsible for sending the inferences and in what manner to
  the frontend */

const parseToView = (semesterOverview) => {
  return studentSemesterPerformance.textContent = String(semesterOverview);
}

viewBtn.addEventListener('click', () => {
  viewBtn.style.display = "none";
  advisory.style.display = "block";

  if (semesterOverview) {
    parseToView(semesterOverview);
  } else {
    console.error("semesterOverview is not defined yet.");
  }
});

minimizeBtn.addEventListener('click', () => {
  advisory.style.display = "none";
  viewBtn.style.display = "block";
});
