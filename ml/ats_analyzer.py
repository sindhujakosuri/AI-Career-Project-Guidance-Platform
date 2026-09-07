import re

SKILLS = [
    "python", "java", "c", "c++", "javascript", "html", "css",
    "react", "node.js", "node", "express", "mongodb", "mysql",
    "flask", "django", "git", "github", "rest api", "machine learning",
    "scikit-learn", "nlp", "sql", "docker", "aws"
]

SECTIONS = [
    "education", "experience", "projects", "skills",
    "certifications", "achievements"
]

def analyze_ats(text):
    lower = text.lower()

    found_skills = [s for s in SKILLS if s in lower]
    missing_skills = [s for s in SKILLS if s not in lower][:8]

    found_sections = [s for s in SECTIONS if s in lower]

    word_count = len(re.findall(r"\b[\w+#.-]+\b", text))
    contact_email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
    phone = bool(re.search(r"(?:\+91[\s-]?)?\d{10}", text))

    score = 0
    score += min(40, len(found_skills) * 2)
    score += min(25, len(found_sections) * 4)
    score += 10 if contact_email else 0
    score += 10 if phone else 0
    score += 15 if 250 <= word_count <= 900 else 8 if word_count > 100 else 0
    score = min(100, score)

    suggestions = []
    if not contact_email:
        suggestions.append("Add a professional email address.")
    if not phone:
        suggestions.append("Add a reachable phone number.")
    if len(found_sections) < 5:
        suggestions.append("Use clear ATS-friendly section headings.")
    if word_count < 250:
        suggestions.append("Add measurable project/experience details.")
    if not found_skills:
        suggestions.append("Include relevant technical keywords from the target job.")
    suggestions.append("Prefer simple formatting, standard headings, and text-based content.")

    return {
        "score": score,
        "skills_found": found_skills,
        "skills_missing": missing_skills,
        "sections_found": found_sections,
        "word_count": word_count,
        "suggestions": suggestions
    }
