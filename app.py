import logging
from flask import render_template, request, Flask
from pdf_to_text import pdfToText
from grammar_check import grammarCheck, getLineNo
from extraction import Job_Title_Extraction, Skills_Extraction
from skill_recommendation import skillRecommendation
from certificate_recommendation import certificateRecommendation

app = Flask(__name__)
# app.debug = True
app.logger.setLevel(logging.DEBUG)


# Set up the route for the home page
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file and file.filename.endswith(".pdf"):
        text = pdfToText(file)

        # grammer check
        grammar_errors = grammarCheck(text)
        line = getLineNo(text, grammar_errors)

        job = Job_Title_Extraction(text)
        skill = Skills_Extraction(text)

        # skill recommendation
        skillRec = skillRecommendation(job, skill)
        skillRec = skillRec.split(",")

        # certification recommendation
        certificateRec = certificateRecommendation(job)
        certificateRec = certificateRec.split(",")

        return render_template(
            "index.html",
            text=text,
            grammar_errors=grammar_errors,
            line=line,
            certificateRec=certificateRec,
            skillRec=skillRec,
        )
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
