from PyPDF2 import PdfReader
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import SKILLS

nltk.download('stopwords')

# Extract text
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stopwords.words('english')]
    return " ".join(words)

# Similarity
def get_similarity(resume, job):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, job])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)

# Extract skills
def extract_skills(text):
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
    return found_skills

# Skill comparison
def skill_match(resume_text, job_text):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    return list(matched), list(missing)

# Keywords
def get_keywords(text):
    words = text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:10]]

def calculate_score(skill_match_count, total_job_skills, similarity):
    skill_score = (skill_match_count / total_job_skills) * 100 if total_job_skills else 0
    overall = (0.6 * skill_score) + (0.4 * similarity)
    
    return round(skill_score, 2), round(overall, 2)

def common_words(resume, job):
    resume_set = set(resume.split())
    job_set = set(job.split())
    return list(resume_set.intersection(job_set))[:10]