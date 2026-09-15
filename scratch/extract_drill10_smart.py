import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789428268196.pdf')

parsed_items = []

for p_idx in range(1, len(reader.pages) - 1): # Pages 2 to 52
    text = reader.pages[p_idx].extract_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    filtered = []
    for l in lines:
        if ('https://docs.google.com' in l or 
            'DRILL 10' in l or 
            'cabiladasnicole' in l or 
            'School (ex.' in l or
            'QUESTIONS 131' in l or
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

    option_blocks = []
    question_lines = []
    
    curr_block = None
    in_q_section = False
    in_correct_ans = False
    
    for l in filtered:
        score_match = re.match(r'^\*?\s*([01])/(?:1|\.\.\.)$', l)
        if score_match and not in_q_section:
            if curr_block and curr_block['opts']:
                option_blocks.append(curr_block)
            score_val = int(score_match.group(1))
            curr_block = {'score': score_val, 'opts': [], 'correct_override': None}
            in_correct_ans = False
        elif curr_block is not None and not in_q_section:
            if l == 'Correct answer':
                in_correct_ans = True
            elif in_correct_ans:
                curr_block['correct_override'] = l
                in_correct_ans = False
            elif (re.match(r'^[A-D]\.\s+', l) or len(curr_block['opts']) < 4):
                curr_block['opts'].append(l)
            else:
                if curr_block and curr_block['opts']:
                    option_blocks.append(curr_block)
                    curr_block = None
                in_q_section = True
                question_lines.append(l)
        else:
            question_lines.append(l)
            
    if curr_block and curr_block['opts']:
        option_blocks.append(curr_block)
        
    prompts = []
    accum = []
    for l in question_lines:
        if 'This content is neither created nor endorsed' in l or 'Does this form look suspicious' in l or l == 'Forms':
            continue
        accum.append(l)
        if l.endswith('*'):
            p = " ".join(accum).rstrip('*').strip()
            p = re.sub(r'\s+', ' ', p)
            prompts.append(p)
            accum = []
    if accum:
        p = " ".join(accum).rstrip('*').strip()
        if p and p != 'Forms':
            p = re.sub(r'\s+', ' ', p)
            prompts.append(p)

    if len(option_blocks) != len(prompts):
        print(f"Page {p_idx+1} mismatch: {len(option_blocks)} option blocks vs {len(prompts)} prompts")
        print("  Options:", [ob['opts'] for ob in option_blocks])
        print("  Prompts:", prompts)
    else:
        for ob, pr in zip(option_blocks, prompts):
            parsed_items.append({'page': p_idx+1, 'prompt': pr, 'opts': ob['opts'], 'score': ob['score'], 'override': ob.get('correct_override')})

print(f"Total parsed items: {len(parsed_items)}")
