import pypdf
import json
import re

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789423743389.pdf')

parsed_items = []

for idx, page in enumerate(reader.pages):
    if idx == 0 or idx == len(reader.pages) - 1:
        continue
    
    words = []
    def visitor(text, cm, tm, font_dict, font_size):
        if text:
            words.append((cm[5], cm[4], text))
            
    page.extract_text(visitor_text=visitor)
    words.sort(key=lambda w: (-w[0], w[1]))
    
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

    cleaned_lines = []
    for l in lines:
        if ('https://docs.google.com' in l or 
            'BPED SPECIALIZATION DRILL' in l or 
            'cabiladasnicole' in l or 
            'QUESTIONS 135' in l or 
            'School (ex.' in l or
            l.startswith('SIS') or
            'BASIC INFORMATION' in l or
            'HELLO mga' in l or
            'Hello Future' in l or
            'Since this is' in l or
            'The respondent' in l or
            'Email Address' in l or
            'NAME (ex.' in l or
            'BRANCH' in l or
            l.startswith('9/7/26')):
            continue
        cleaned_lines.append(l)

    # Divide page into option blocks and question title blocks
    # Step 1: Collect question titles (lines that form question prompts)
    # Step 2: Collect option blocks (score, options, correct answer if 0/1)
    
    option_blocks = []
    question_titles = []
    
    curr_opt_block = None
    in_question_section = False
    
    curr_q_lines = []
    
    for l in cleaned_lines:
        if re.match(r'^\*?\s*[01]/1', l):
            if curr_opt_block:
                option_blocks.append(curr_opt_block)
            curr_opt_block = {'score': l, 'lines': []}
        elif curr_opt_block is not None and not in_question_section:
            # Check if this line looks like a question title starting (e.g. non-option text when we already have 4 options, or ending in *)
            # Standard options start with A., B., C., D., a., b., c., d. or "Correct answer"
            if (l.startswith('A.') or l.startswith('B.') or l.startswith('C.') or l.startswith('D.') or
                l.startswith('a.') or l.startswith('b.') or l.startswith('c.') or l.startswith('d.') or
                l.startswith('Correct answer')):
                curr_opt_block['lines'].append(l)
            else:
                # We reached question titles section!
                if curr_opt_block:
                    option_blocks.append(curr_opt_block)
                    curr_opt_block = None
                in_question_section = True
                curr_q_lines.append(l)
        elif in_question_section:
            curr_q_lines.append(l)
            
    if curr_opt_block:
        option_blocks.append(curr_opt_block)

    # Now group curr_q_lines into individual question prompts (each ending with *)
    q_prompts = []
    accum = []
    for l in curr_q_lines:
        accum.append(l)
        if l.endswith('*'):
            prompt = " ".join(accum).rstrip('*').strip()
            # Clean up double spaces
            prompt = re.sub(r'\s+', ' ', prompt)
            q_prompts.append(prompt)
            accum = []
    if accum:
        prompt = " ".join(accum).rstrip('*').strip()
        if prompt:
            prompt = re.sub(r'\s+', ' ', prompt)
            q_prompts.append(prompt)

    # Pair option_blocks with q_prompts
    if len(option_blocks) != len(q_prompts):
        print(f"PAGE {idx+1} MISMATCH: {len(option_blocks)} option blocks vs {len(q_prompts)} prompts")
        print("   Options:", [o['lines'] for o in option_blocks])
        print("   Prompts:", q_prompts)
    else:
        for ob, qp in zip(option_blocks, q_prompts):
            parsed_items.append({'page': idx+1, 'prompt': qp, 'opt_block': ob})

print(f"Successfully parsed {len(parsed_items)} items!")
