const viewBtn = document.getElementById('view_analysis');
const minimizeBtn = document.getElementById('minimize_analysis');
const advisory= document.getElementById('advisory');
const studentSpecificPerformance = document.getElementById('studentSpecificPerformance');
const studentSemesterPerformance = document.getElementById('studentSemesterPerformance');
const moreOfOrNo =document.getElementById('toDoMoreOrNot');

const advisoryTitles = document.getElementsByClassName('advisory-section-title');

const secondTitle = advisoryTitles[1];
const thirdTitle = advisoryTitles[2];

secondTitle.style.display = "none";
thirdTitle.style.display = "none"

let compulsoryMessages = [];
let personalMessages = [];
let semesterOverview;
let correlationMeanings = [];
let parCorrelationMeanings = []; 

advisory.style.display = "none";

const emas_data = neededData ? neededData["filtered_emas_data"] : null;
const correlation_data = neededData ? neededData["filtered_corr_data"] : null;
const partial_correlation_data = neededData ? neededData["filtered_par_corr_data"] : null;

const { 
  "semester performance": semesterPerformance, 
  "necessary checks": compulsoryChecks, 
  "personal checks": studentSpecificChecks 
} = emas_data

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

const { status, type } = semesterPerformance;
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

if (semesterPerformance) {
  semesterOverview = semesterPerformanceOverview(semesterPerformance);
}

const processCompulsoryChecks = (checks) => {
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
            ? `Your latest performance in ${comparisonAvg} has improved beyond your${
                currAvg === 'cgpa' 
                  ? " long-term" : ""} historical average. Keep up the progress!`
            : `Your latest performance in ${comparisonAvg} has dropped below your${
                currAvg === 'cgpa' 
                  ? " long-term" : ""} historical average. Consider reviewing your study strategies.`
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

const compulsoryMessagesCleaner = (compulsoryMessages) => {
  const multiCrossCheckRegex = /Your (?:latest|recent) performance in ([A-Za-z]+) has (improved|dropped) (?:beyond|below) your (long-term )?historical average\./i;
  
  const toPop = {};
  const mergedMessages = [];

  const neededStatements = compulsoryMessages
    .map((msg, index) => ({ match: msg.match(multiCrossCheckRegex), index, fullMsg: msg }))
    .filter(entry => entry.match);

  neededStatements.forEach(({ match, index, fullMsg }) => {
    if (match) {
      const neededKey = match[1];
      const keyStatus = match[2];
      const longTermOrNo = !!match[3];

      if (!toPop[neededKey]) {
        toPop[neededKey] = [];
      }

      toPop[neededKey].push({ keyStatus, longTermOrNo, index, fullMsg });
    }
  });

  const indexesToRemove = new Set();

  Object.entries(toPop).forEach(([key, values]) => {
    const longTermEntries = values.filter(v => v.longTermOrNo);
    const shortTermEntries = values.filter(v => !v.longTermOrNo);

    if (longTermEntries.length > 0 && shortTermEntries.length > 0) {
      const keyStatus = longTermEntries[0].keyStatus; 

      const originalMessages = [...longTermEntries, ...shortTermEntries];

      originalMessages.forEach(v => indexesToRemove.add(v.index));

      mergedMessages.push(
        `Your most recent performance in ${key} has ${keyStatus} across both your short-term and long-term trends. Keep it going!`
      );
    }
  });

  for (let i = compulsoryMessages.length - 1; i >= 0; i--) {
    if (indexesToRemove.has(i)) {
      compulsoryMessages.splice(i, 1);
    }
  }

  compulsoryMessages.push(...mergedMessages);
  return;
};

if (compulsoryChecks) {
  processCompulsoryChecks(compulsoryChecks);
  compulsoryMessagesCleaner(compulsoryMessages);
};

const processPersonalChecks = (checks) => {
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

const personalMessagesCleaner = (personalMessages) => {
  const multipleCrossRegex = /your performance in ([\w\s]+)courses has (surpassed|dropped below) your (long-term )?average/i;
  const toPop = {};
  const mergedMessages = [];

  const neededStatements = personalMessages
    .map((msg, index) => ({ match: msg.match(multipleCrossRegex), index, fullMsg: msg }))
    .filter(entry => entry.match);

  neededStatements.forEach(({ match, index, fullMsg }) => {
    if (match) {
      const neededKey = match[1];
      const positiveStatus = match[2] === "surpassed";
      const longTermOrNo = !!match[3];

      if (!toPop[neededKey]) {
        toPop[neededKey] = [];
      }

      toPop[neededKey].push({ positiveStatus, longTermOrNo, index, fullMsg });
    }
  });
  
  const indexesToRemove = new Set();

  Object.entries(toPop).forEach(([key, values]) => {
    const positiveStatus = [];

    const longTermEntries = values.filter(value => value.longTermOrNo);
    const shortTermEntries = values.filter(value => !value.longTermOrNo);
    
    const positiveEntries = values.filter(value => value.positiveStatus);
    const negativeEntries = values.filter(value => !value.positiveStatus);

    if (longTermEntries.length > 0 && shortTermEntries.length > 0) {
      const keyType = positiveStatus ? "positive" : "negative";

      const originalMessages = [...longTermEntries, ...shortTermEntries];

      originalMessages.forEach(msg => indexesToRemove.add(msg.index));

      if (keyType === "positive") {
        mergedMessages.push(
          `Your most recent performance in courses of the ${
            key} branch has surpassed your cumulative adjusted average and also is better than semester adjusted average. Keep the momentum going!`
        )
      }

      if (keyType === "negative") {
        mergedMessages.push(
          `Your most recent performance in courses of the ${
            key} branch has dipped below your cumulative adjusted average and is worse than semester adjusted average. Take immediate actions to get back on track!`
        )
      }

    }
  });

  for (let i = personalMessages.length - 1; i >= 0; i--) {
    if (indexesToRemove.has(i)) {
      personalMessages.splice(i, 1);
    }
  } 

  personalMessages.push(...mergedMessages);
  return;
};

if (studentSpecificChecks) {
  processPersonalChecks(studentSpecificChecks);
  personalMessagesCleaner(personalMessages);
}

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
    console.warn("Unexpected keys:", key);
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

if (correlation_data) {
  correlation_data.forEach(item => {
    const meaning = extractCorrMeaning(item);
    if (meaning) correlationMeanings.push(meaning);
  });
}

const extractParCorrMeaning = ({ key, significance, strength, type }) => {
  const keyRegex = /^([a-zA-Z\s]+)(?:_([a-zA-Z]+))?$/;
  const validPredictor = key[0].match(keyRegex);
  const validKeys = validPredictor && keyRegex.test(key[1]);

  if (validKeys) {
    const predictorBranch = validPredictor[1];
    const predictorSuffix = validPredictor[2] || null;
    if (!predictorSuffix) {
        return {
          message: `The influence of ${key[0]} on ${key[1]} is ${
            type.toLowerCase()}ly ${strength.toLowerCase()} and statistically ${significance.toLowerCase()}.`,
          suffix: predictorSuffix
        }
    } 
    
    if (predictorSuffix === "units") {
        if (key[1] === 'cgpa') {
          return {
            message: type === "Positive" 
              ? `Taking more units from ${predictorBranch} can benefit your long-term performance.`
              : `Reducing course units from ${predictorBranch} may help avoid long-term negative effects.`,
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

const parCorrelationMeaningsCleaner = (parCorrelationMeanings) => {
  const toPop = {};
  const unitToPop = {};
  const countToPop = {}; 

  const mergedMessages = [];
  const indexesToRemove = new Set();
  
  const noSuffixRegex = /^[\w\s]+of\s([A-Za-z\s]+)\son\s([A-Za-z]+)\sis\s([A-Za-z]+)ly/i;
  const unitSuffixRegex = /^(?:Taking more units from|Reducing course units from|Consider taking more units from|It may be beneficial to limit courses from)\s([A-Za-z\s]+)(?:can benefit your long-term performance|may help avoid long-term negative effects|.)$/i;  
  const countSuffixRegex = /^(?:Adding more courses from|Avoiding courses from|Consider taking more courses from|Reducing courses from)\s([A-Za-z\s]+?)(?:\s)(?:could boost your long-term performance|may help prevent negative academic impact|might be a good strategy|$)\.?$/i;

  const neededStatements = parCorrelationMeanings
    .map((meaning, index) => ({match: meaning.match(noSuffixRegex), index, fullMeaning: meaning}))
    .filter(entry => entry.match);

  const unitNeededStatements = parCorrelationMeanings
    .map((meaning, index) => ({match: meaning.match(unitSuffixRegex), index, fullMeaning: meaning}))
    .filter(entry => entry.match)

  const countNeededStatements = parCorrelationMeanings
    .map((meaning, index) => ({match: meaning.match(countSuffixRegex), index, fullMeaning: meaning}))
    .filter(entry => entry.match)

  neededStatements.forEach(({match, index, fullMeaning}) => {
    if (match) {
      const neededKey = match[1];
      const longTermOrNo = match[2];
      const status = match[3];

      if (!toPop[neededKey]) {
        toPop[neededKey] = [];
      }

      toPop[neededKey].push({ status, longTermOrNo, index, fullMeaning });
    }
  });

  unitNeededStatements.forEach(({match, index, fullMeaning}) => {
    if (match) {
      const neededKey = match[1];
      const longTerm = fullMeaning.includes("long-term") ? true : false;
      const status = fullMeaning.includes("can benefit" || "taking more units") ? "positive" : "negative";

      if (!unitToPop[neededKey]) {
        unitToPop[neededKey] = [];
      }

      unitToPop[neededKey].push({ status, longTerm, index, fullMeaning });
    }
  })

  countNeededStatements.forEach(({match, index, fullMeaning}) => {
      if (match) {
        const neededKey = match[1];
        const longTerm = fullMeaning.includes("long-term" || "academic impact") ? true : false;
        const status = fullMeaning.includes("more courses from") ? "positive" : "negative";

        if (!countToPop[neededKey]) {
            countToPop[neededKey] = [];
        }
  
        countToPop[neededKey].push({ status, longTerm, index, fullMeaning });
      }
  })

  const mergeObjectsWithArrayValues = (obj1, obj2) => {
    const result = { ...obj1 };
    
    Object.keys(obj2).forEach(key => {
      if (key in result) {
        if (!Array.isArray(result[key])) {
          result[key] = [result[key]];
        }
        
        if (Array.isArray(obj2[key])) {
          result[key] = [...result[key], ...obj2[key]];
        } else {
          result[key].push(obj2[key]);
        }
      } else {
        result[key] = obj2[key];
      }
    });
    
    return result;
  };

  const conjoinPop = mergeObjectsWithArrayValues(unitToPop, countToPop);

  Object.entries(conjoinPop).forEach(([key, values]) => {
    const longTermEntries = values.filter(value => value.longTerm);
    const shortTermEntries = values.filter(value => !value.longTerm);

    const shortTermNegatives = values.filter(value => 
      value["fullMeaning"].includes("It may be") || 
      value["fullMeaning"].includes("Reducing courses from")
    );
    
    const longTermNegatives = values.filter(value => 
      value["fullMeaning"].includes("Reducing course units from") || 
      value["fullMeaning"].includes("Avoiding courses from")
    );

    const shortTermPositives = values.filter(value => 
      value["fullMeaning"].includes("Consider taking more courses") || 
      value["fullMeaning"].includes("Consider taking more units from")
    );
    
    const longTermPositives = values.filter(value => 
      value["fullMeaning"].includes("Taking more units from") || 
      value["fullMeaning"].includes("Adding more courses from")
    );

    const keysWithMultipleValues = values.length > 1;

    if (keysWithMultipleValues) {
      if (longTermEntries.length > 1) {
        const neededLongNegatives = longTermEntries.filter(entry => 
          longTermNegatives.includes(entry)
        );
        
        const neededLongPositives = longTermEntries.filter(entry => 
          longTermPositives.includes(entry)
        );

        if (neededLongPositives.length > 1) {
          mergedMessages.push(
            `You should be really looking to offer more courses of ${
              key} branch as it has historically proven to be beneficial in the long-term.`
          );
          neededLongPositives.forEach(value => indexesToRemove.add(value.index))
        }

        if (neededLongNegatives.length > 1) {
          mergedMessages.push(
            `You should remove as many courses of the ${
              key} branch with immediate alacrity to put a stop to its historical drastic effects.`
          );
          neededLongNegatives.forEach(value => indexesToRemove.add(value.index))
        }
      }

      if (shortTermEntries.length > 1) {
        const neededShortNegatives = shortTermEntries.filter(entry => 
          shortTermNegatives.includes(entry)
        );
        
        const neededShortPositives = shortTermEntries.filter(entry => 
          shortTermPositives.includes(entry)
        );
        
        if (neededShortPositives.length > 1) {
          mergedMessages.push(
            `You should look to seize on any available opportunities to offer more courses from ${
              key} branch as it bodes well and if maintained can probably extend into the long-run.`
          );
          neededShortPositives.forEach(value => indexesToRemove.add(value.index))
        }

        if (neededShortNegatives.length > 1) {
          mergedMessages.push(
            `You must actively look to reduce courses of the ${
              key} branch to avoid a drawdown on long-term performance by extension.`
          );
          neededShortNegatives.forEach(value => indexesToRemove.add(value.index))
        }
      }
    }
  });

  Object.entries(toPop).forEach(([key, values]) => {
    const longTermEntries = values.filter(value => value.longTermOrNo === "cgpa");
    const shortTermEntries = values.filter(value => value.longTermOrNo === "gpa");

    if (longTermEntries.length > 0 && shortTermEntries.length > 0) {
      const longTermStatus = longTermEntries[0].status;
      const shortTermStatus = shortTermEntries[0].status;
      if (longTermStatus === shortTermStatus) {  
        [...longTermEntries, ...shortTermEntries].forEach(value => indexesToRemove.add(value.index));

        mergedMessages.push(
          `The influence of ${
            key} on both short and long term performances is ${
              longTermStatus}ly significant.`
        );
      }
    }
  })

  Object.entries(unitToPop).forEach(([key, values]) => {
    const longTermEntries = values.filter(value => value.longTerm);
    const shortTermEntries = values.filter(value => !value.longTerm);

    if (longTermEntries.length > 0 && shortTermEntries.length > 0) {
      const longTermStatus = longTermEntries[0].status;
      const shortTermStatus = shortTermEntries[0].status;


      if (longTermStatus === shortTermStatus && longTermStatus === "positive") {
        [...longTermEntries, ...shortTermEntries].forEach(value => indexesToRemove.add(value.index));
        
        mergedMessages.push(
          `You should really consider adding course units from ${
            key} branch as it has historically proven to be beneficial to your cause.`
        );
      }

      if (longTermStatus === shortTermStatus && longTermStatus === "negative") {
        [...longTermEntries, ...shortTermEntries].forEach(value => indexesToRemove.add(value.index));
        
        mergedMessages.push(
          `You should really consider reducing number of units offered from ${
            key} branch as it has historically proven to be detrimental to your cause.`
        );
      }      
    }
  })

  Object.entries(countToPop).forEach(([key, values]) => {
    const longTermEntries = values.filter(value => value.longTerm);
    const shortTermEntries = values.filter(value => !value.longTerm);

    if (longTermEntries.length > 0 && shortTermEntries.length > 0) {
      const longTermStatus = longTermEntries[0].status;
      const shortTermStatus = shortTermEntries[0].status;


      if (longTermStatus === shortTermStatus && longTermStatus === "positive") {
        [...longTermEntries, ...shortTermEntries].forEach(value => indexesToRemove.add(value.index));
        
        mergedMessages.push(
          `You should really consider adding more of courses from ${
            key} branch as it has historically proven to be beneficial to your cause.`
        );
      }

      if (longTermStatus === shortTermStatus && longTermStatus === "negative") {
        [...longTermEntries, ...shortTermEntries].forEach(value => indexesToRemove.add(value.index));
        
        mergedMessages.push(
          `You should really consider reducing number of courses offered from ${
            key} branch as it has historically proven to be detrimental to your cause.`
        );
      }      
    }
  })

  for (let i = parCorrelationMeanings.length - 1; i >= 0; i--) {
    if (indexesToRemove.has(i)) {
      parCorrelationMeanings.splice(i, 1);
    }
  }
  
  parCorrelationMeanings.push(...mergedMessages);
  return;
};

if (partial_correlation_data) {
  secondTitle.style.display = "block";

  partial_correlation_data.forEach(item => {
    const meaning = extractParCorrMeaning(item);
    if (meaning) parCorrelationMeanings.push(meaning["message"]);
  })
  
  parCorrelationMeaningsCleaner(parCorrelationMeanings);
}

const newbieAdvices = [
  "Engage with material through active techniques like summarizing key points in your own words, creating mind maps, teaching concepts to others, and using practice questions. This approach enhances comprehension and retention.", 
  "Familiarize yourself with academic support services like tutoring centers, writing labs, study skills workshops, and peer mentoring programs. These free resources can provide targeted assistance and help you develop stronger academic skills.", 
  "Form study groups with motivated, focused peers who complement your learning style. Choose collaborators who are committed to mutual learning.", 
  "Communicate promptly with professors about challenges, seek clarification early, and take responsibility for your learning.", 
  "Embrace a Growth Mindset, view challenges as opportunities for learning, not insurmountable obstacles. Understand that intelligence and abilities can be developed through dedication and hard work. Celebrate progress, learn from setbacks, and maintain a positive, resilient attitude toward academic challenges."
]

const parseToView = () => {
  if (!emas_data || !correlation_data) {
    if (!emas_data && !correlation_data && !partial_correlation_data) {
      advisory.innerHTML = `
        <h2 class="advisory-section-title">Tips for achieving academic success as a newbie</h2>
        <ul id="new-student-advice">
          ${newbieAdvices.map(advice => `<li class="adviceOfAdvices">${advice}</li>`).join('')}
        </ul>
      `;
    }
    return;
  }  

  if (semesterPerformance) {
    studentSemesterPerformance.textContent = String(semesterOverview);    
  }

  if (compulsoryChecks) {
    studentSemesterPerformance.textContent += ` ${compulsoryMessages.map(msg => String(
        msg)).join(" ")}`;
  }
  
  if (studentSpecificChecks) {
    studentSpecificPerformance.textContent = personalMessages.map(msg => String(
        msg)).join(" ");
    const multipleCrossesRegex = /[A-Za-z\s]+of([A-Za-z]+)\son[(c)?gpa]+\sis\s((?:positively|negatively))/ig;
  }

  if (correlation_data) {
    thirdTitle.style.display = "block";
    moreOfOrNo.innerHTML += `<span class="next-semester-overview">${
      correlationMeanings.map(msg => String(msg)).join(" ")
    }</span>${
      partial_correlation_data
        ? `<span class="next-semester-courses-overview">${
            parCorrelationMeanings.map(msg => String(msg)).join(" ")
          }</span>`
        : `<h1 class="next-semester-courses-overview">Available dataset isn't sufficient enough
            to suggest specific targets for you, sorry you'll have to rawdog this mate.</h1>`
    }`;
  }
  return;
}

const adjustChartsForSmallScreens = () => {
  if (window.innerWidth < 767) { 
    document.querySelectorAll('.chart-container .js-plotly-plot').forEach(plot => {
      Plotly.relayout(plot, {
        showlegend: false,
        width: window.innerWidth * 0.95, 
        height: 400 
      });
    });
  }
}
adjustChartsForSmallScreens();

viewBtn.addEventListener('click', () => {
  viewBtn.style.display = "none";
  advisory.style.display = "block";
  parseToView();
});

minimizeBtn.addEventListener('click', () => {
  advisory.style.display = "none";
  viewBtn.style.display = "block";
});