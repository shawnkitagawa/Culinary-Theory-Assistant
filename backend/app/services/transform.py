import os
from pypdf import PdfReader

pdf_folder = r"C:\Users\seank\Desktop\PROJECT_FREE\Q-A-StudyAssistant\raw"
txt_folder = r"C:\Users\seank\Desktop\PROJECT_FREE\Q-A-StudyAssistant\raw_text"

os.makedirs(txt_folder, exist_ok=True)

for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(txt_folder, txt_filename)

        reader = PdfReader(pdf_path)
        extracted_pages = []

        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                extracted_pages.append(f"--- Page {i} ---\n{text}")
            else:
                extracted_pages.append(f"--- Page {i} ---\n[No text found]")

        full_text = "\n\n".join(extracted_pages)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Created: {txt_filename}")

print("Finished converting all PDFs.")