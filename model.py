from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# -------------------------------
# SYNONYMS
# -------------------------------
SYNONYMS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "js": "javascript",
    "py": "python"
}

# -------------------------------
# STOPWORDS
# -------------------------------
STOPWORDS = set([
    "the", "and", "a", "an", "to", "of", "in", "for",
    "with", "on", "at", "by", "from", "is", "are",
    "good", "hardworking", "team", "player"
])

def format_text_list(words):
    return [w.title() for w in words]

# -------------------------------
# FORMAT TEXT (Fix UI issue)
# -------------------------------
def format_text(text):
    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())

# -------------------------------
# PREPROCESS
# -------------------------------
def preprocess(text):
    if not text:
        return ""

    text = text.lower().strip()

    # Replace synonyms safely (VERY IMPORTANT)
    for short, full in SYNONYMS.items():
        text = re.sub(rf"\b{short}\b", full, text)

    # Replace symbols with SPACE (not empty string)
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    words = text.split()

    # Remove stopwords
    words = [w for w in words if w not in STOPWORDS]

    return " ".join(words)

# -------------------------------
# SMART MATCH (better logic)
# -------------------------------
def smart_match(resume_words, job_words):
    matched = set()

    for r in resume_words:
        for j in job_words:
            if r == j or r in j or j in r:
                matched.add(j)

    return matched

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def calculate_match(resume, job):
    resume_clean = preprocess(resume)
    job_clean = preprocess(job)

    # Safety check
    if not resume_clean or not job_clean:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "skill_gap": "No Input",
            "strength": "No Input",
            "confidence": "No Input",
            "tips": ["Provide valid input"]
        }

    # -------------------------------
    # TF-IDF SIMILARITY
    # -------------------------------
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([resume_clean, job_clean])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    # -------------------------------
    # WORD SETS
    # -------------------------------
    resume_words = set(resume_clean.split())
    job_words = set(job_clean.split())

    # -------------------------------
    # SMART MATCH
    # -------------------------------
    matched = smart_match(resume_words, job_words)
    missing = job_words - matched

    # -------------------------------
    # SCORING
    # -------------------------------
    score = similarity

    if len(matched) >= 1:
        score += 0.25

    if len(matched) >= 3:
        score += 0.15

    if len(matched) == 0:
        score *= 0.4

    score = min(score, 1.0)
    score = int(score * 100)

    # -------------------------------
    # FORMAT OUTPUT (IMPORTANT)
    # -------------------------------
    matched_list = [format_text(m) for m in list(matched)[:10]]
    missing_list = [format_text(m) for m in list(missing)[:10]]

    # -------------------------------
    # AI INSIGHTS (RIGHT PANEL)
    # -------------------------------
    if score < 40:
        skill_gap = "High Gap"
        strength = "Weak Profile"
        confidence = "Low Confidence"
    elif score < 70:
        skill_gap = "Moderate Gap"
        strength = "Developing Profile"
        confidence = "Medium Confidence"
    else:
        skill_gap = "Low Gap"
        strength = "Strong Profile"
        confidence = "High Confidence"

    # -------------------------------
    # AI TIPS
    # -------------------------------
    tips = []

    if score < 40:
        tips.append("Add more relevant technical skills")
    elif score < 70:
        tips.append("Improve keyword alignment with job role")
    else:
        tips.append("Fine-tune resume for optimization")

    if len(missing_list) > 5:
        tips.append("Focus on missing high-demand skills")

    if "Python" in missing_list:
        tips.append("Consider adding Python if role requires it")

    if len(matched_list) > 5:
        tips.append("Good skill coverage detected")

    # -------------------------------
    # FINAL RESPONSE (API READY)
    # -------------------------------
    return {
        "score": score,
        "matched": matched_list,
        "missing": missing_list,
        "skill_gap": skill_gap,
        "strength": strength,
        "confidence": confidence,
        "tips": tips
    }