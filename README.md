# AI Career & Project Guidance Platform

MVP based on the resume project description:
- ATS resume analysis
- Skill extraction
- Initial career prediction
- Career recommendations
- Flask web interface

## 1. Create a virtual environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Run

```bash
python app.py
```

Open:
http://127.0.0.1:5000

## 4. Current architecture

Browser -> Flask -> Resume Parser -> ATS Analyzer + Career Predictor -> JSON -> Dashboard

## 5. Next upgrade

Replace the keyword-based career predictor with a trained Scikit-learn model using a labeled career/resume dataset. Then add:
- target-job ATS matching
- NLP preprocessing
- project recommendations
- skill-gap analysis
- learning roadmap
- database/user accounts
- deployment
