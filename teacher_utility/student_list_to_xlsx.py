import re
import fitz  # PyMuPDF
import pandas as pd

pdf_path = "./Student List.pdf"
doc = fitz.open(pdf_path)

students = []

# Process each page in the PDF
for page in doc:
    text = page.get_text("text")
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # A valid record starts with a record number (like "1", "2", etc.)
        # followed immediately by a line ending with "-" (e.g., "25-")
        if line.isdigit() and (i + 1 < len(lines)) and lines[i+1].strip().endswith("-"):
            # Extract the two parts of the student ID.
            id_part1 = lines[i+1].strip()  # e.g., "25-"
            id_part2 = lines[i+2].strip() if (i + 2) < len(lines) else ""
            student_id = id_part1 + id_part2  # e.g., "25-60525-1"
            
            # The student name starts at the next line (i+3)
            # It may span one or two lines until we encounter "0.00"
            name = ""
            j = i + 3
            while j < len(lines) and lines[j].strip() != "0.00":
                # Accumulate name parts separated by a space.
                if name:
                    name += " " + lines[j].strip()
                else:
                    name = lines[j].strip()
                j += 1

            # Append the record if both ID and name are present.
            if student_id and name:
                students.append([student_id, name])
            i = j  # jump past the name block and "0.00" marker
        else:
            i += 1

# Optionally remove duplicate records (if headers/footers are repeated)
unique_students = []
seen = set()
for sid, name in students:
    if sid not in seen:
        seen.add(sid)
        unique_students.append([sid, name])

# Save the extracted data into an Excel file with student IDs in column B (starting at B3) 
# and student names in column C (starting at C3).
df = pd.DataFrame(unique_students, columns=["Student ID", "Student Name"])
excel_path = "./Attendance_and_marks_ipl[B1].xlsx"
with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, startrow=2, startcol=1)

print(f"Excel file saved at: {excel_path}")