import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789426515998.pdf')

pages = []

for idx in range(1, len(reader.pages) - 1): # pages 2 to 64
    text = reader.pages[idx].extract_text()
    pages.append((idx + 1, text))

# Let's inspect pages where mismatch occurred (e.g. Page 3, Page 14, Page 22, Page 29, Page 51, Page 57, Page 59)
for p_num in [3, 14, 22, 29, 51, 57, 59]:
    for p, txt in pages:
        if p == p_num:
            print(f"=== PAGE {p} ===")
            print(txt)

