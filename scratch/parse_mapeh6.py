import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789429205203.pdf')

full_text = []

for idx, page in enumerate(reader.pages):
    full_text.append(f"\n--- PAGE {idx+1} ---\n" + page.extract_text())

all_txt = "\n".join(full_text)

with open('scratch/mapeh6_raw.txt', 'w') as f:
    f.write(all_txt)

print("Saved mapeh6_raw.txt. Total length:", len(all_txt))
