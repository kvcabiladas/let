import re

with open('scratch/drill3_raw.txt') as f:
    raw_pages = f.read().split('---PAGE---')

print(f"Total pages: {len(raw_pages)}")

parsed_questions = []

for p_idx, page in enumerate(raw_pages):
    if p_idx == 0:  # skip cover/header page
        continue
    
    # Clean page lines
    lines = [l.strip() for l in page.split('\n') if l.strip()]
    
    # Filter out footer URL and date
    lines = [l for l in lines if not ('https://docs.google.com' in l or 'BPED SPECIALIZATION DRILL' in l or l.startswith('SIS') or 'BASIC INFORMATION' in l or 'QUESTIONS 135' in l or 'School (ex.' in l)]
    
    # Find question texts (ending with *)
    q_texts = []
    for l in lines:
        if l.endswith('*') and not l.startswith('A.') and not l.startswith('B.') and not l.startswith('C.') and not l.startswith('D.') and not l.startswith('a.') and not l.startswith('b.') and not l.startswith('c.') and not l.startswith('d.'):
            q_texts.append(l.rstrip('*').strip())
            
    # Find option groups and scores
    # Each question block typically has a score indicator like 1/1 or 0/1 or *1/1 or *0/1
    # Followed by A., B., C., D.
    
    print(f"Page {p_idx+1}: Found {len(q_texts)} question titles: {q_texts}")

