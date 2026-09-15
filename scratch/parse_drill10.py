import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789428268196.pdf')

print("Total pages:", len(reader.pages))

pages_data = []

for p_idx in range(1, len(reader.pages) - 1): # Skip cover (p0) and last page (52)
    page_text = reader.pages[p_idx].extract_text()
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    
    filtered = []
    for l in lines:
        if ('https://docs.google.com' in l or 
            'DRILL 10' in l or 
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
        
    pages_data.append((p_idx + 1, filtered))

print(f"Collected {len(pages_data)} pages.")
for p_num, lines in pages_data[:4]:
    print(f"=== PAGE {p_num} ===")
    for l in lines:
        print("  ", l)

