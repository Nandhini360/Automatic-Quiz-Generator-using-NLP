# Automated Question Generator

A simple Flask web app to:
- Upload a PDF
- Scan all or specific pages
- Generate questions automatically (fill-in-the-blanks or AI-generated)
- Show answers only when you click

---

## How to Use

1. **Install requirements**
pip install -r requirements.txt
python -m spacy download en_core_web_sm

2. **Run the app**
python app.py

3. **Open in browser**
http://127.0.0.1:5000/


4. **Upload your PDF**, choose pages & number of questions → click **Generate Questions**.

---

## Project Files

- `app.py` — main Flask app
- `templates/` — HTML files
- `uploads/` — stores uploaded files

---

## Requirements

- Flask
- PyMuPDF (`fitz`)
- spaCy
- transformers + torch *(optional, for AI questions)*

---
