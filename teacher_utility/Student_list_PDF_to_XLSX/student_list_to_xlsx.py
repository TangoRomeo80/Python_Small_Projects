import re
import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path


# ---------- Configuration ----------
PDF_PATH = r"C:\Codes\Python_Small_Projects\teacher_utility\Student_list_PDF_to_XLSX\Student List.pdf"
EXCEL_PATH = r"C:\Codes\Python_Small_Projects\teacher_utility\Student_list_PDF_to_XLSX\Student List.xlsx"
START_ROW = 2   # 0-indexed -> writes header beginning at Excel row 3
START_COL = 1   # 0-indexed -> writes header beginning at Excel column B
EXCEL_ENGINE = "xlsxwriter"  # requires `pip install xlsxwriter`
# ----------------------------------


def looks_like_cgpa(s: str) -> bool:
    """
    Returns True if s looks like a CGPA number on a 0.00–4.00 scale,
    e.g., '0', '3', '3.2', '3.75', '4', '4.0', '4.00'.
    """
    s = s.strip()
    return bool(re.fullmatch(r'(?:[0-3](?:\.\d{1,2})?|4(?:\.0{1,2})?)', s))


def is_serial_line(s: str) -> bool:
    """Digits-only line, e.g., '1', '2', '15'."""
    return s.strip().isdigit()


def next_is_id_prefix(lines, idx: int) -> bool:
    """
    Checks if lines[idx+1] exists and ends with '-' which we treat
    as the first line of a split student ID, e.g., '25-'
    """
    return (idx + 1) < len(lines) and lines[idx + 1].strip().endswith("-")


def normalize_spaces(s: str) -> str:
    """Collapse multiple spaces and trim."""
    return " ".join(s.split())


def reconstruct_student_id(id_part1: str, id_part2: str) -> str:
    """
    Join two ID parts safely and validate basic pattern like '25-60525-1'.
    The first part typically ends with '-', the second part continues.
    """
    candidate = (id_part1.strip() + id_part2.strip()).replace(" ", "")
    # Optional: validate loose pattern ##-#####-#
    if re.fullmatch(r'\d{2}-\d{5}-\d', candidate):
        return candidate
    return candidate  # fall back to raw join if pattern varies


def extract_students_from_pdf(pdf_path: str):
    students = []
    pdf_path = str(pdf_path)

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text")
            # Remove blank lines but keep order
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            i = 0
            while i < len(lines):
                line = lines[i]

                # Pattern for the start of a student record:
                #   lines[i] is digits-only (serial number)
                #   lines[i+1] ends with '-' (first part of the ID)
                if is_serial_line(line) and next_is_id_prefix(lines, i):
                    # Safely read ID parts
                    id_part1 = lines[i + 1].strip()
                    id_part2 = lines[i + 2].strip() if (i + 2) < len(lines) else ""
                    student_id = reconstruct_student_id(id_part1, id_part2)

                    # Collect name starting from i+3 until a stop condition
                    name_parts = []
                    j = i + 3

                    while j < len(lines):
                        w = lines[j].strip()

                        # --- Stop conditions for end of "name" block ---
                        # 1) CGPA-like number line (e.g., 3.21, 4.00)
                        if looks_like_cgpa(w):
                            break
                        # 2) Email encountered
                        if "@" in w:
                            break
                        # 3) Next student record header encountered
                        if is_serial_line(w) and next_is_id_prefix(lines, j):
                            break
                        # 4) Optional: common section headers that may appear after names
                        if w.lower().startswith(("program", "credits", "credit", "remarks", "student id", "name ")):
                            break

                        if w:
                            name_parts.append(w)
                        j += 1

                        # Defensive guard to avoid runaway
                        if j - (i + 3) > 10:  # unlikely a name spans >10 lines
                            break

                    name = normalize_spaces(" ".join(name_parts))

                    # Store if both present
                    if student_id and name:
                        students.append([student_id, name])

                    # Continue scanning from where we stopped
                    i = j
                else:
                    i += 1

    # Deduplicate by Student ID (keep first occurrence)
    seen = set()
    unique_students = []
    for sid, name in students:
        if sid not in seen:
            seen.add(sid)
            unique_students.append([sid, name])

    return unique_students


def write_to_excel(rows, out_path: str, start_row: int = 2, start_col: int = 1, engine: str = "xlsxwriter"):
    df = pd.DataFrame(rows, columns=["Student ID", "Student Name"])
    out_path = str(out_path)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out_path, engine=engine) as writer:
        df.to_excel(writer, index=False, startrow=start_row, startcol=start_col)


def main():
    students = extract_students_from_pdf(PDF_PATH)
    write_to_excel(students, EXCEL_PATH, START_ROW, START_COL, EXCEL_ENGINE)
    print(f"Extracted {len(students)} students.")
    print(f"Excel file saved at: {EXCEL_PATH}")


if __name__ == "__main__":
    main()
