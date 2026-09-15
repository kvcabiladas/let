import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789425621795.pdf')

parsed_pages = []

for p_idx in range(1, len(reader.pages) - 1): # Pages 2 to 55 (index 1 to 54)
    page_text = reader.pages[p_idx].extract_text()
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    
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

    # Let's inspect the page content
    # On each page:
    # 1. Options for question 1 (A., B., C., D. and optional Correct answer)
    # 2. Options for question 2...
    # 3. Options for question 3...
    # 4. Question title 1 (ends with *)
    # 5. Question title 2 (ends with *)
    # 6. Question title 3 (ends with *)
    
    # Let's parse option blocks and question titles
    option_blocks = []
    question_title_lines = []
    
    curr_block = {'options': [], 'correct_answer_override': None}
    in_correct_ans = False
    
    for l in filtered:
        opt_match = re.match(r'^[A-D]\.\s+(.*)$', l)
        if opt_match:
            if in_correct_ans:
                # This is an option line for the next block, so save previous block!
                if curr_block['options']:
                    option_blocks.append(curr_block)
                curr_block = {'options': [l], 'correct_answer_override': None}
                in_correct_ans = False
            else:
                letter = l[0]
                if letter == 'A' and len(curr_block['options']) >= 4:
                    # New option block starting!
                    option_blocks.append(curr_block)
                    curr_block = {'options': [l], 'correct_answer_override': None}
                else:
                    curr_block['options'].append(l)
        elif l == 'Correct answer':
            in_correct_ans = True
        elif in_correct_ans:
            curr_block['correct_answer_override'] = l
            in_correct_ans = False
        else:
            # We reached question titles!
            if curr_block['options']:
                option_blocks.append(curr_block)
                curr_block = {'options': [], 'correct_answer_override': None}
            question_title_lines.append(l)
            
    if curr_block['options']:
        option_blocks.append(curr_block)

    # Reconstruct question titles (lines ending in *)
    prompts = []
    accum = []
    for l in question_title_lines:
        accum.append(l)
        if l.endswith('*'):
            prompt = " ".join(accum).rstrip('*').strip()
            prompt = re.sub(r'\s+', ' ', prompt)
            prompts.append(prompt)
            accum = []
    if accum:
        prompt = " ".join(accum).rstrip('*').strip()
        if prompt:
            prompt = re.sub(r'\s+', ' ', prompt)
            prompts.append(prompt)

    if len(option_blocks) != len(prompts):
        print(f"PAGE {p_idx+1} MISMATCH: {len(option_blocks)} option blocks vs {len(prompts)} prompts")
        print("   Option blocks:", [ob['options'] for ob in option_blocks])
        print("   Prompts:", prompts)
    else:
        for ob, pr in zip(option_blocks, prompts):
            parsed_pages.append({'page': p_idx+1, 'prompt': pr, 'block': ob})

print(f"Successfully extracted {len(parsed_pages)} items!")
