import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789426515998.pdf')

full_text = []

for idx in range(1, len(reader.pages) - 1): # Pages 2 to 64
    txt = reader.pages[idx].extract_text()
    full_text.append(f"\n--- PAGE {idx+1} ---\n" + txt)

combined_text = "".join(full_text)

# Let's save combined text to file to inspect easily
with open('scratch/drill8_combined.txt', 'w') as f:
    f.write(combined_text)

print("Saved drill8_combined.txt. Total chars:", len(combined_text))

