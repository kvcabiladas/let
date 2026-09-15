import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789423743389.pdf')

questions = []

for p_idx in range(1, len(reader.pages) - 1):
    page_text = reader.pages[p_idx].extract_text()
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    
    # Filter header/footer noise
    filtered = []
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
            re.match(r'^\d+/\d+/\d+', l)):
            continue
        filtered.append(l)

    # Separate options area from questions area
    # Options area contains lines starting with score (e.g. 1/1, 0/1), option letters (A., B., C., D., a., b., c., d.), or "Correct answer"
    option_blocks = []
    question_lines = []
    
    curr_block = None
    
    for l in filtered:
        score_match = re.match(r'^\*?\s*([01])/1$', l)
        if score_match:
            if curr_block:
                option_blocks.append(curr_block)
            score_val = int(score_match.group(1))
            curr_block = {'score': score_val, 'options': [], 'correct_answer_override': None}
        elif curr_block is not None:
            # Check if option line or correct answer line
            if re.match(r'^[A-Da-d]\.\s+', l):
                curr_block['options'].append(l)
            elif l == 'Correct answer':
                # next line will be correct answer override
                curr_block['in_correct_answer'] = True
            elif curr_block.get('in_correct_answer'):
                curr_block['correct_answer_override'] = l
                curr_block['in_correct_answer'] = False
            else:
                # We have finished option blocks, now in question title lines!
                if curr_block:
                    option_blocks.append(curr_block)
                    curr_block = None
                question_lines.append(l)
        else:
            question_lines.append(l)
            
    if curr_block:
        option_blocks.append(curr_block)
        
    # Group question_lines into individual prompts
    prompts = []
    accum = []
    for l in question_lines:
        accum.append(l)
        if l.endswith('*'):
            p = " ".join(accum).rstrip('*').strip()
            p = re.sub(r'\s+', ' ', p)
            prompts.append(p)
            accum = []
    if accum:
        p = " ".join(accum).rstrip('*').strip()
        if p:
            p = re.sub(r'\s+', ' ', p)
            prompts.append(p)

    if len(option_blocks) != len(prompts):
        print(f"Mismatch on Page {p_idx+1}: {len(option_blocks)} option blocks vs {len(prompts)} prompts")
        print("   Options blocks:", option_blocks)
        print("   Prompts:", prompts)
    else:
        for ob, pr in zip(option_blocks, prompts):
            # Parse options
            raw_opts = ob['options']
            # We expect 4 options
            opts_dict = {}
            selected_letter = None
            
            # Standard options: A. ..., B. ..., C. ..., D. ...
            for opt in raw_opts:
                m = re.match(r'^([A-Da-d])\.\s+(.*)$', opt)
                if m:
                    let = m.group(1).upper()
                    text = m.group(2).strip()
                    opts_dict[let] = text

            # If score == 1, selected option is correct answer
            # Wait, which option was selected? In Google Forms PDF viewscore, when score is 1/1, the options printed are the ones of the form, and pypdf extracts text. Wait, how do we know which option was selected if score == 1?
            # Let's check!
            questions.append({
                'page': p_idx + 1,
                'prompt': pr,
                'score': ob['score'],
                'raw_options': raw_opts,
                'correct_override': ob.get('correct_answer_override')
            })

print(f"Extracted {len(questions)} total items.")
