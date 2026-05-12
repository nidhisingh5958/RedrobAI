const SKILL_ALIASES = {
  python: "python",
  pyhton: "python",
  java: "java",
  javascript: "javascript",
  javascrpit: "javascript",
  js: "javascript",
  typescript: "typescript",
  typescrpit: "typescript",
  "c++": "cpp",
  cpp: "cpp",
  r: "r",
  kotlin: "kotlin",
  machinelearning: "machine_learning",
  "machine learning": "machine_learning",
  ml: "machine_learning",
  sklearn: "machine_learning",
  deeplearning: "deep_learning",
  "deep learning": "deep_learning",
  "deep-learning": "deep_learning",
  tensorflow: "tensorflow",
  pytorch: "pytorch",
  keras: "keras",
  nlp: "nlp",
  bert: "bert",
  xgboost: "xgboost",
  "feature engineering": "feature_engineering",
  statistics: "statistics",
  stats: "statistics",
  regression: "regression",
  clustering: "clustering",
  "data-viz": "data_visualization",
  "data visualization": "data_visualization",
  "data viz": "data_visualization",
  matplotlib: "data_visualization",
  tableau: "data_visualization",
  "power-bi": "data_visualization",
  "power bi": "data_visualization",
  powerbi: "data_visualization",
  pandas: "pandas",
  numpy: "numpy",
  react: "react",
  reacts: "react",
  reactjs: "react",
  vue: "vue",
  "vue.js": "vue",
  vuejs: "vue",
  redux: "redux",
  tailwind: "tailwind",
  "html/css": "html_css",
  "html css": "html_css",
  html: "html_css",
  css: "html_css",
  jest: "jest",
  graphql: "graphql",
  "node.js": "nodejs",
  nodejs: "nodejs",
  "node js": "nodejs",
  flask: "flask",
  "spring boot": "spring_boot",
  springboot: "spring_boot",
  "rest api": "rest_api",
  rest: "rest_api",
  restapi: "rest_api",
  microservices: "microservices",
  sql: "sql",
  mysql: "mysql",
  mysq: "mysql",
  postgresql: "postgresql",
  postgres: "postgresql",
  mongodb: "mongodb",
  redis: "redis",
  docker: "docker",
  kubernetes: "kubernetes",
  kubernates: "kubernetes",
  k8s: "kubernetes",
  "ci/cd": "ci_cd",
  cicd: "ci_cd",
  "ci cd": "ci_cd",
  aws: "aws",
  android: "android",
  firebase: "firebase",
  algorithms: "algorithms",
  algoritms: "algorithms",
  "data structure": "data_structures",
  "data structures": "data_structures",
  "competitive programming": "competitive_programming",
  "ui/ux": "ui_ux",
  "ui ux": "ui_ux",
  figma: "figma",
};

const RESUMES = {
  "Arjun Sharma": "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning",
  "Priya Nair": "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS",
  "Rahul Gupta": "Java, Spring Boot, MySql, Microservices, Docker, kubernates",
  "Sneha Patel": "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib",
  "Vikram Singh": "C++, Algoritms, Data Structure, competitive programming, python",
  "Ananya Krishnan": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD",
  "Karan Mehta": "Python, Sklearn, XGboost, feature engineering, SQL, tableau",
  "Deepika Rao": "Java, Android, Kotlin, Firebase, REST, UI/UX, figma",
  "Aditya Kumar": "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest",
  "Meera Iyer": "python, R, statistics, ML, regression, clustering, Power-BI",
};

const JOB_DESCRIPTIONS = {
  "JD-1": {
    company: "Kakao (Seoul)",
    role: "ML Engineer",
    skills: "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization",
  },
  "JD-2": {
    company: "Naver (Seongnam)",
    role: "Backend Engineer",
    skills: "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes",
  },
  "JD-3": {
    company: "Line (Seoul)",
    role: "Frontend Engineer",
    skills: "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS",
  },
};

function normalizeSkills(rawSkills) {
  return rawSkills
    .split(",")
    .map((chunk) => chunk.trim().toLowerCase())
    .filter(Boolean)
    .map((token) => SKILL_ALIASES[token])
    .filter(Boolean);
}

function deduplicateSkills(skills) {
  const seen = new Set();
  const result = [];

  for (const skill of skills) {
    if (seen.has(skill)) continue;
    seen.add(skill);
    result.push(skill);
  }

  return result;
}

function prepareResumeSkills(resumes) {
  const prepared = {};
  const vocabulary = new Set();

  for (const [candidateName, rawSkills] of Object.entries(resumes)) {
    const skills = deduplicateSkills(normalizeSkills(rawSkills));
    prepared[candidateName] = skills;
    skills.forEach((skill) => vocabulary.add(skill));
  }

  return { prepared, vocabulary: [...vocabulary].sort() };
}

function computeTfidf(resumes) {
  const { prepared, vocabulary } = prepareResumeSkills(resumes);
  const documentFrequency = Object.fromEntries(vocabulary.map((skill) => [skill, 0]));

  Object.values(prepared).forEach((skills) => {
    skills.forEach((skill) => {
      documentFrequency[skill] += 1;
    });
  });

  const totalDocuments = Object.keys(prepared).length;
  const vectors = {};

  for (const [candidateName, skills] of Object.entries(prepared)) {
    const uniqueSkillCount = skills.length;
    const vector = {};

    for (const skill of vocabulary) {
      if (!skills.includes(skill) || uniqueSkillCount === 0) {
        vector[skill] = 0;
        continue;
      }

      const tf = 1 / uniqueSkillCount;
      const idf = Math.log(totalDocuments / documentFrequency[skill]);
      vector[skill] = tf * idf;
    }

    vectors[candidateName] = vector;
  }

  return vectors;
}

function buildJobVector(rawSkills, vocabulary) {
  const skills = new Set(deduplicateSkills(normalizeSkills(rawSkills)));
  return Object.fromEntries(vocabulary.map((skill) => [skill, skills.has(skill) ? 1 : 0]));
}

function cosineSimilarity(vecA, vecB) {
  const keys = new Set([...Object.keys(vecA), ...Object.keys(vecB)]);
  let dot = 0;
  let magA = 0;
  let magB = 0;

  for (const key of keys) {
    dot += (vecA[key] || 0) * (vecB[key] || 0);
  }

  for (const value of Object.values(vecA)) magA += value * value;
  for (const value of Object.values(vecB)) magB += value * value;

  if (magA === 0 || magB === 0) return 0;
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

function rankCandidates(tfidfVectors, jdVector) {
  return Object.entries(tfidfVectors)
    .map(([candidateName, vector]) => ({
      name: candidateName,
      score: cosineSimilarity(vector, jdVector),
    }))
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name))
    .slice(0, 5);
}

function render() {
  const { vocabulary } = prepareResumeSkills(RESUMES);
  const tfidfVectors = computeTfidf(RESUMES);
  const results = document.getElementById("results");

  results.innerHTML = Object.entries(JOB_DESCRIPTIONS)
    .map(([jdId, jd]) => {
      const jdVector = buildJobVector(jd.skills, vocabulary);
      const ranked = rankCandidates(tfidfVectors, jdVector);

      return `
        <article class="card">
          <div class="card-head">
            <div>
              <h2>${jdId}</h2>
              <p class="meta">${jd.company} · ${jd.role}</p>
            </div>
          </div>
          <ol class="rank-list">
            ${ranked
              .map(
                (candidate) => `
                  <li class="rank-item">
                    <span class="candidate">${candidate.name}</span>
                    <span class="score">${candidate.score.toFixed(2)}</span>
                  </li>
                `,
              )
              .join("")}
          </ol>
          <div class="skills">
            ${deduplicateSkills(normalizeSkills(jd.skills))
              .map((skill) => `<span class="chip">${skill}</span>`)
              .join("")}
          </div>
        </article>
      `;
    })
    .join("");
}

document.getElementById("rerunBtn").addEventListener("click", render);
render();