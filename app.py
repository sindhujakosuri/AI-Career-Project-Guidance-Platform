import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from ml.resume_parser import extract_resume_text
from ml.ats_analyzer import analyze_ats
from ml.career_predictor import predict_career

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "uploads"
)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "Please upload a resume."}), 400

    file = request.files["resume"]
    if not file.filename:
        return jsonify({"error": "Please select a resume file."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF or TXT resumes are supported in this MVP."}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    try:
        text = extract_resume_text(path)
        ats = analyze_ats(text)
        career = predict_career(text)
        return jsonify({
            "ats": ats,
            "career": career
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)

    app.run(host="0.0.0.0", port=5000, debug=True)
(Prepare application for deployment)
