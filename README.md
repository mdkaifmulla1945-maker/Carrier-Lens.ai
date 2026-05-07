# CarrierLens.ai

CarrierLens.ai is an AI-powered resume analysis and job matching system designed to simulate real-world Applicant Tracking System (ATS) behavior. It evaluates resumes against job descriptions using a custom-built skill extraction engine, weighted scoring logic, and structured decision-making rules to determine candidate-job compatibility.

The system provides a complete analysis including match percentage, skill gaps, hiring decision prediction, seniority estimation, confidence scoring, and human-readable explanations. It is built using Flask for backend processing and a modern web interface for user interaction.

## 🔴 Live Demo
<a href="https://huggingface.co/spaces/Kaif3118/carrierlens-ai" target="_blank">
  🚀 Try CarrierLens.ai
</a>

## 🧠 Features
- Resume vs Job Description Matching
- Skill Gap Detection
- AI Insights Panel
---

## Key Features

CarrierLens.ai delivers a full ATS-style evaluation pipeline with the following capabilities:

- Intelligent skill extraction from unstructured text
- Role-based skill expansion for improved job understanding
- Weighted scoring system for accurate candidate evaluation
- Automatic identification of matched and missing skills
- Hiring decision prediction (Hire, Maybe, Reject)
- Candidate seniority estimation (Junior, Mid, Senior)
- Confidence scoring based on match quality
- Explanation engine providing transparent reasoning
- Clean and responsive web interface for real-time analysis

---

## System Overview

The system works in three core stages:

### 1. Input Processing
The user provides a resume and a job description. The system normalizes the text by removing noise, standardizing formats, and preparing it for analysis.

### 2. Skill Extraction and Matching
A predefined skill intelligence map identifies technical and professional skills from both inputs. The engine expands job roles into relevant skill sets and compares them against the resume.

### 3. Scoring and Decision Engine
A weighted scoring algorithm evaluates the importance of each matched skill. Based on the final score and skill gaps, the system determines hiring suitability, seniority level, and confidence metrics.

---

## Technology Stack

- Python (Flask)
- HTML5, CSS3, JavaScript
- Regex-based NLP processing
- Rule-based AI scoring engine
- RESTful API architecture

---

## Project Structure

carrierlens-ai/  
app.py  
requirements.txt  
templates/  
index.html  
static/  
style.css  
script.js  

---

## Installation and Setup

To run the project locally:

### 1. Clone the repository
git clone https://github.com/mdkaifmulla1945-maker/Carrier-Lens.ai/tree/main  
cd carrierlens-ai  

### 2. Install dependencies
pip install flask  

### 3. Run the application
python app.py  

### 4. Open in browser
http://127.0.0.1:5000/

---

## API Endpoint

### POST /analyze

This endpoint processes resume and job description data and returns analysis results.

Request Body:
{
  "skills": "resume text here",
  "job": "job description here"
}

Response:
{
  "score": 85,
  "matched": ["Python", "Machine Learning"],
  "missing": ["Kubernetes"],
  "decision": "HIRE",
  "seniority": "MID",
  "reason": "Strong skill match with minor gaps",
  "skill_gap": "Minor skill gaps detected",
  "strength": "Strong alignment with job requirements",
  "confidence": "High confidence"
}

---

## Deployment

CarrierLens.ai can be deployed on multiple platforms:

- Hugging Face Spaces 

---

## Example Output

Score: 82%  
Decision: HIRE  
Seniority: MID  
Confidence: High  

Matched Skills:
- Python
- Machine Learning
- TensorFlow

Missing Skills:
- Kubernetes
- System Design

Reason: Strong skill alignment with minor gaps in advanced system design concepts.

---

## Future Enhancements

CarrierLens.ai is designed for extensibility. Planned improvements include:

- AI-based semantic matching using transformer models
- Resume ranking across multiple job descriptions
- PDF resume upload support
- Advanced ATS simulation with industry benchmarking
- Dashboard analytics for recruiters
- Multi-language support for global usage

---

## Purpose

This project is built as a practical AI system to demonstrate how real-world ATS platforms evaluate candidates. It focuses on bridging the gap between raw resume data and structured hiring decisions using interpretable AI logic.

---

## Author

CarrierLens.ai is developed as an AI engineering project focused on resume intelligence systems, skill extraction algorithms, and job matching automation.
