import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789425621795.pdf')

full_page_lines = []

for p_idx in range(1, len(reader.pages) - 1):
    text = reader.pages[p_idx].extract_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # filter trash
    filtered = []
    for l in lines:
        if ('https://docs.google.com' in l or 
            'BPED DRILL 4' in l or 
            'cabiladasnicole' in l or 
            'School (ex.' in l or
            l.startswith('SIS') or
            'BASIC INFORMATION' in l or
            'Hello Future' in l or
            'Since this is' in l or
            'The respondent' in l or
            'Email Address' in l or
            'NAME (ex.' in l or
            'BRANCH' in l or
            re.match(r'^\d+/\d+/\d+', l)):
            continue
        filtered.append(l)
    full_page_lines.append((p_idx + 1, filtered))

# Let's inspect how questions are numbered across all pages
# Each question title starts with a number like "1.", "2.", "150." or is unnumbered/numbered
for p_num, lines in full_page_lines:
    q_titles = [l for l in lines if re.match(r'^\d+\.\s+', l) or (l.endswith('*') and not l.startswith('A.') and not l.startswith('B.') and not l.startswith('C.') and not l.startswith('D.'))]
    # print(f"Page {p_num}: {len(q_titles)} titles:", q_titles)

print(f"Total page count: {len(full_page_lines)}")

