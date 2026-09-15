import pypdf

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789423743389.pdf')

full_text = []
for page in reader.pages:
    full_text.append(page.extract_text())

all_str = "\n---PAGE---\n".join(full_text)

with open('scratch/drill3_raw.txt', 'w') as f:
    f.write(all_str)

print("Saved raw text. Total length:", len(all_str))
