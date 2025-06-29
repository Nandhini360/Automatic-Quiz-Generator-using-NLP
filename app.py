from flask import Flask, render_template, request, redirect, url_for, session
import fitz  # PyMuPDF
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory storage for Q&A (use DB for production)
qa_pairs = []

def extract_text(pdf_path, page_numbers=None):
    text = ""
    doc = fitz.open(pdf_path)
    if page_numbers:
        for num in page_numbers:
            if 0 <= num < len(doc):
                text += doc[num].get_text()
    else:
        for page in doc:
            text += page.get_text()
    return text

def clean_text(raw_text):
    lines = raw_text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        if line.isupper():
            continue
        if "Edition" in line or "ISBN" in line or "Copyright" in line:
            continue
        if any(char.isdigit() for char in line) and len(line) < 30:
            continue
        cleaned.append(line)
    return ' '.join(cleaned)


import spacy

nlp = spacy.load("en_core_web_sm")

def generate_fill_in_the_blank(text, num_questions):
    doc = nlp(text)
    sentences = list(doc.sents)
    questions = []

    for sent in sentences:
        if sent.text.strip().startswith(("It", "This", "They")):
            continue

        sent_doc = nlp(sent.text)
        # Use only named entities
        entities = [ent for ent in sent_doc.ents if ent.label_ in ["PERSON", "ORG", "GPE", "DATE", "EVENT"]]

        if not entities:
            continue

        ent = random.choice(entities)
        question = sent.text.replace(ent.text, "_____")
        questions.append({'question': question, 'answer': ent.text})

        if len(questions) >= num_questions:
            break

    return questions



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["pdf_file"]
        pages = request.form.get("pages")  # e.g., "1,2,5"
        num_q = int(request.form.get("num_questions", 5))

        path = f"uploads/{file.filename}"
        file.save(path)

        page_numbers = None
        if pages:
            page_numbers = [int(p.strip()) - 1 for p in pages.split(',')]

        text = extract_text(path, page_numbers)
        text = clean_text(text)
        generated = generate_fill_in_the_blank(text, num_q)

        # Save Q&A in session (simple for demo)
        session['qa_pairs'] = generated

        return redirect(url_for('show_questions'))

    return render_template("index.html")

@app.route("/questions")
def show_questions():
    questions = session.get('qa_pairs', [])
    return render_template("questions.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
