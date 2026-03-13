from flask import Flask, render_template, request
from summarizer import summarize_text
import PyPDF2
import docx

app = Flask(__name__)

# Function to extract text from PDF
def extract_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to extract text from DOCX
def extract_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text


@app.route("/", methods=["GET", "POST"])
def index():

    summary = ""

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filename = file.filename

            # TEXT FILE
            if filename.endswith(".txt"):
                text = file.read().decode("utf-8", errors="ignore")

            # PDF FILE
            elif filename.endswith(".pdf"):
                text = extract_pdf(file)

            # DOCX FILE
            elif filename.endswith(".docx"):
                text = extract_docx(file)

            else:
                text = "Unsupported file format"

            summary = summarize_text(text)

    return render_template("index.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=True)