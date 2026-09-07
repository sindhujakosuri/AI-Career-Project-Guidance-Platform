import re

CAREER_KEYWORDS = {
    "Software Developer": [
        "java", "c++", "python", "data structures", "algorithms", "git"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "node", "express", "frontend"
    ],
    "Data Scientist": [
        "python", "pandas", "numpy", "machine learning", "scikit-learn",
        "statistics", "matplotlib"
    ],
    "AI / ML Engineer": [
        "machine learning", "deep learning", "nlp", "tensorflow",
        "pytorch", "scikit-learn", "artificial intelligence"
    ],
    "Backend Developer": [
        "python", "java", "flask", "django", "node", "express",
        "rest api", "sql", "mongodb"
    ]
}

def predict_career(text):
    lower = text.lower()
    scores = {}

    for career, keywords in CAREER_KEYWORDS.items():
        matched = [k for k in keywords if k in lower]
        scores[career] = {
            "score": len(matched),
            "matched": matched
        }

    ranked = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    top = ranked[:3]

    max_score = max((v["score"] for _, v in ranked), default=0)
    if max_score == 0:
        confidence = 0
    else:
        confidence = round((max_score / max(len(CAREER_KEYWORDS[top[0][0]]), 1)) * 100)

    return {
        "top_career": top[0][0] if top else "Unknown",
        "confidence": min(confidence, 100),
        "recommendations": [
            {
                "career": career,
                "score": data["score"],
                "matched_keywords": data["matched"]
            }
            for career, data in top
        ]
    }
