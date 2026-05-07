from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# -------------------------------
# SKILL DATABASE (CORE INTELLIGENCE)
# -------------------------------

SKILL_MAP = {
    # -----------------------
    # FRONTEND
    # -----------------------
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind", "bootstrap"],
    "javascript": ["javascript", "java script", "js", "ecmascript", "es6"],
    "typescript": ["typescript", "ts"],

    "react": ["react", "reactjs", "react.js", "react native"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs", "vue.js"],

    "frontend": ["frontend", "front end", "ui", "ui ux", "uiux", "user interface"],

    # -----------------------
    # BACKEND
    # -----------------------
    "backend": ["backend", "back end", "server side"],
    "node.js": ["node", "nodejs", "node.js", "express", "express.js"],
    "java": ["java", "spring", "spring boot"],
    "python": ["python", "django", "flask", "fastapi"],
    "php": ["php", "laravel", "codeigniter"],
    
    # -----------------------
    # DATABASES
    # -----------------------
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "mongodb": ["mongodb", "mongo", "nosql"],
    # AI / DATA SCIENCE STACK
    
    "deep learning": ["deep learning", "dl"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "matplotlib": ["matplotlib", "plt"],
    "keras": ["keras"],
    "tensorflow": ["tensorflow", "tf"],
    "scikit-learn": ["scikit-learn", "sklearn"],

    # -----------------------
    # DATA / AI / ML
    # -----------------------
    "machine learning": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
    "deep learning": ["deep learning", "dl", "neural networks", "cnn", "rnn"],
    "nlp": ["nlp", "natural language processing"],
    "data science": ["data science", "data analysis", "data analytics"],

    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch"],

    # -----------------------
    # DEVOPS / CLOUD
    # -----------------------
    "git": ["git", "github", "gitlab"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],

    # -----------------------
    # MOBILE
    # -----------------------
    "android": ["android", "kotlin", "java android"],
    "ios": ["ios", "swift", "objective c"],

    # -----------------------
    # GENERAL / SOFT TECH
    # -----------------------
    "api": ["api", "rest api", "restful"],
    "rest": ["rest", "restful services"],
    "microservices": ["microservices", "micro services"],
    "express": ["express", "express.js"],
    "system design": ["system design", "scalability", "low level design", "lld", "hld"],
}

STOPWORDS = {
    # -------------------
    # BASIC GRAMMAR
    # -------------------
    "the", "and", "a", "an", "to", "of", "in", "for",
    "with", "on", "at", "by", "from", "is", "are", "was", "were",
    "be", "been", "being", "this", "that", "these", "those",

    # -------------------
    # JOB DESCRIPTION NOISE
    # -------------------
    "we", "our", "us", "you", "your",
    "looking", "seeking", "hiring", "require", "required", "requirements",
    "candidate", "candidates", "role", "position", "job", "opportunity",

    # -------------------
    # GENERIC SOFT WORDS (VERY IMPORTANT)
    # -------------------
    "good", "excellent", "strong", "skilled", "experienced",
    "hardworking", "motivated", "passionate", "dedicated",

    # -------------------
    # TEAM / CORPORATE NOISE
    # -------------------
    "team", "player", "teamwork", "collaboration",
    "fast", "paced", "environment", "dynamic",

    # -------------------
    # FILLER WORDS
    # -------------------
    "plus", "also", "must", "should", "will", "can",
    "ability", "knowledge", "experience"
} 

ROLE_MAP = {
    "ai developer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "matplotlib",
        "keras",
        "scikit-learn"
    ],

    "ml engineer": [
        "machine learning",
        "deep learning",
        "python",
        "tensorflow",
        "pandas",
        "numpy"
    ],

    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "ui ux"
    ],

    "backend developer": [
        "node.js",
        "express",
        "python",
        "java",
        "sql"
    ],

    "full stack developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "express",
        "sql"
    ]
}

SKILL_WEIGHT = {
    "html": 1,
    "css": 1,
    "javascript": 2,
    "react": 3,

    "node.js": 3,
    "express": 3,
    "sql": 3,

    "python": 3,
    "machine learning": 4,
    "deep learning": 4,
    "tensorflow": 4,
    "pytorch": 4,

    "system design": 5
}
# -------------------------------
# TEXT NORMALIZATION
# -------------------------------

def normalize(text):
    if not text:
        return ""

    text = text.lower()

    # fix broken phrases
    text = text.replace("java script", "javascript")
    text = text.replace("react js", "react")
    text = text.replace("java script", "javascript")
    text = text.replace("react js", "react")
    text = text.replace("low level design", "system design")
    text = text.replace("high level design", "system design")
    text = text.replace("tensor flow", "tensorflow")
    text = text.replace("scikit learn", "scikit-learn")
    text = text.replace("machine learning", "ml")
    text = text.replace("deep learning", "dl")
    text = text.replace("ai developer", "machine learning engineer")

    text = re.sub(r'[^a-z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# -------------------------------
# SKILL EXTRACTION ENGINE
# -------------------------------
def extract_skills(text):
    text = normalize(text)
    words = set(text.split())

    found = set()

    for skill, variants in SKILL_MAP.items():
        for v in variants:
            v = v.lower()

            # single word match
            if len(v.split()) == 1:
                if v in words:
                    found.add(skill)

            # phrase match
            else:
                if v in text:
                    found.add(skill)

    return found



def get_decision(score, matched, missing):

    if score >= 75 and len(missing) <= 2:
        return "HIRE"

    if 50 <= score < 75:
        return "MAYBE"

    return "REJECT"

def detect_seniority(matched):

    if len(matched) >= 8:
        return "SENIOR"
    elif len(matched) >= 4:
        return "MID"
    else:
        return "JUNIOR"
    
def generate_reason(decision, score, missing):

    if decision == "HIRE":
        return "Strong skill match with minimal gaps"

    if decision == "MAYBE":
        return "Moderate match but some key skills missing"

    return "Low match. Missing critical skills: " + ", ".join(missing[:3])    
# -------------------------------
# ROLE EXPANSION
# -------------------------------

def expand_role(text):
    text = normalize(text)
    expanded = set()

    for role, skills in ROLE_MAP.items():
        if role in text:
            expanded.update(skills)

    return expanded
# -------------------------------
# WEIGHTED SCORE ENGINE
# -------------------------------

def compute_score(matched, job_skills):
    if not job_skills:
        return 0

    match_weight = sum(SKILL_WEIGHT.get(s.lower(), 1) for s in matched)
    total_weight = sum(SKILL_WEIGHT.get(s.lower(), 1) for s in job_skills)

    if total_weight == 0:
        return 0

    return int((match_weight / total_weight) * 100)

# -------------------------------
# EXPLANATION ENGINE
# -------------------------------

def generate_explanations(matched, missing):
    explanations = []

    for m in matched:
        explanations.append(f"Matched skill: {m}")

    for m in missing:
        explanations.append(f"Missing skill: {m}")

    if len(missing) > 5:
        explanations.append("High skill gap detected. Upskilling recommended.")

    return explanations

# -------------------------------
# CORE ANALYSIS ENGINE
# -------------------------------

def analyze(resume, job):

    resume_skills = extract_skills(resume)

    job_skills = extract_skills(job)
    job_skills = job_skills.union(expand_role(job))

    # HARD SAFETY CLEANUP (IMPORTANT)
    job_skills.discard("frontend")
    job_skills.discard("backend")
    job_skills.discard("ai developer")

    if not resume_skills and not job_skills:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "tips": ["Provide valid input"],
            "skill_gap": "No data",
            "strength": "No data",
            "confidence": "Low confidence"
        }

    matched = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)
 
    score = compute_score(matched, job_skills)

    decision = get_decision(score, matched, missing)
    seniority = detect_seniority(matched)
    reason = generate_reason(decision, score, missing)

    if "machine learning" in matched and "ml" not in resume.lower():
        matched.remove("machine learning")
    # clean display
    matched = [m.title() for m in matched]
    missing = [m.title() for m in missing]
    

    explanations = generate_explanations(matched, missing)





    # INSIGHTS
    skill_gap = (
        "No major gaps. Strong alignment."
        if len(missing) == 0 else
        "Minor skill gaps detected."
        if len(missing) < 5 else
        "Significant skill gaps. Upskilling needed."
    )

    strength = (
        "No strong alignment found."
        if len(matched) == 0 else
        "Basic alignment with role."
        if len(matched) < 5 else
        "Strong alignment with job requirements."
    )

    confidence = (
        "Low confidence" if score < 40 else
        "Moderate confidence" if score < 70 else
        "High confidence"
    )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "explanations": explanations,
        "decision": decision,
        "seniority": seniority,
        "reason": reason,
        "skill_gap": skill_gap,
        "strength": strength,
        "confidence": confidence
    }


# -------------------------------
# ROUTES
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_api():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input received"}), 400

        result = analyze(
            data.get('skills', ''),
            data.get('job', '')
        )

        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Server error"}), 500


# -------------------------------
# RUN
# -------------------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860)