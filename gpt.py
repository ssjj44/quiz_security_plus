import PyPDF2
import json
import re

def extract_questions_from_pdf(pdf_path):
    questions = []
    
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    # Updated regex pattern with (https://\S+) for the link
    question_pattern = re.compile(r"([A-Z]\d+\.\s.*?\?)\s*(?:\n|\s)*❍\s*A\.\s(.*?)\s*❍\s*B\.\s(.*?)\s*❍\s*C\.\s(.*?)\s*❍\s*D\.\s(.*?)\s*The Answer:\s*(\w)\.\s(.*?)\n(.*?)\nMore information:\s*(.*?)\n(https://professormesser\.link/\d{9})", re.DOTALL)

    
    for match in question_pattern.finditer(text):
        question_text = match.group(1).strip()
        options = [match.group(i).strip() for i in range(2, 6)]
        answer_letter = match.group(6).strip()
        answer_text = match.group(7).strip()
        explanation = match.group(8).strip()
        more_info = match.group(9).strip()
        link = match.group(10).strip()
        
        question_data = {
            "question": question_text,
            "options": options,
            "answer": answer_text,
            "explanation": f"{answer_letter}. {answer_text}\n{explanation}\nMore information:\n{more_info} {link}"
        }
        questions.append(question_data)
    
    return questions

pdf_path = "test.pdf"
extracted_questions = extract_questions_from_pdf(pdf_path)

# Salvăm rezultatele într-un fișier JSON
with open("questions.json", "w", encoding="utf-8") as json_file:
    json.dump(extracted_questions, json_file, indent=4, ensure_ascii=False)

print("Întrebările au fost extrase și salvate în 'questions.json'.")