import pypdf

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789423743389.pdf')

pages_text = []

for idx, page in enumerate(reader.pages):
    if idx == 0 or idx == len(reader.pages) - 1: # skip cover and last empty page
        continue
    
    # Let's extract words with coordinates using visitor
    words = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text:
            words.append((cm[5], cm[4], text)) # y, x, text
            
    page.extract_text(visitor_text=visitor)
    # Sort top-to-bottom (Y descending)
    words.sort(key=lambda w: (-w[0], w[1]))
    
    # Group into lines by Y coordinate (within 4 points)
    lines = []
    curr_y = None
    curr_line = []
    for y, x, t in words:
        if curr_y is None or abs(y - curr_y) < 4:
            curr_line.append(t)
            curr_y = y
        else:
            lines.append("".join(curr_line).strip())
            curr_line = [t]
            curr_y = y
    if curr_line:
        lines.append("".join(curr_line).strip())
        
    pages_text.append((idx + 1, lines))

print(f"Extracted {len(pages_text)} pages.")
for page_num, lines in pages_text[:3]:
    print(f"=== Page {page_num} ===")
    for l in lines:
        print("  ", l)

