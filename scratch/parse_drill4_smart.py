import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789425621795.pdf')

parsed_pages = []

for p_idx in range(1, len(reader.pages) - 1): # Pages 2 to 55
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

    # Smart parsing:
    # Separate the page into two streams:
    # Stream 1: Option blocks & correct answer overrides
    # Stream 2: Question title prompts
    
    # Notice that on all Google Forms printouts, lines before question prompts are either:
    # - Option starting with A., B., C., D.
    # - Continuation of previous option
    # - "Correct answer"
    # - Correct answer text line
    # Then question prompts appear, each ending with '*'!
    
    option_blocks = []
    curr_block = None
    curr_opt = None
    
    q_title_lines = []
    in_q_section = False
    
    in_correct_ans = False
    
    for l in filtered:
        # Check if question prompt starts or continues
        # Question prompts end with * or start with "1.", "2.", etc., or appear after all option blocks are collected
        if in_q_section:
            q_title_lines.append(l)
            continue
            
        opt_start = re.match(r'^([A-D])\.\s+(.*)$', l)
        if opt_start:
            letter = opt_start.group(1)
            text = opt_start.group(2)
            
            if letter == 'A' and curr_block is not None and len(curr_block['opts']) >= 4:
                # Close current block and start new one
                option_blocks.append(curr_block)
                curr_block = {'opts': {letter: text}, 'correct_override': None}
            elif curr_block is None:
                curr_block = {'opts': {letter: text}, 'correct_override': None}
            else:
                curr_block['opts'][letter] = text
            curr_opt = letter
            in_correct_ans = False
        elif l == 'Correct answer':
            in_correct_ans = True
        elif in_correct_ans:
            if curr_block:
                curr_block['correct_override'] = l
            in_correct_ans = False
        else:
            # Check if this line is continuation of an option OR start of question section
            # If we already have 4 options in current block (or we have completed 3 blocks for 3 questions on page),
            # and line does not start with A-D, it's either continuation of option or start of question section!
            if curr_opt is not None and not l.endswith('*') and not re.match(r'^\d+\.\s+', l):
                # Continuation of current option!
                curr_block['opts'][curr_opt] += " " + l
            else:
                # Reached question section!
                if curr_block and curr_block['opts']:
                    option_blocks.append(curr_block)
                    curr_block = None
                in_q_section = True
                q_title_lines.append(l)
                
    if curr_block and curr_block['opts']:
        option_blocks.append(curr_block)
        
    # Build question prompts
    prompts = []
    accum = []
    for l in q_title_lines:
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
        print("  Options:", [b['opts'] for b in option_blocks])
        print("  Prompts:", prompts)
    else:
        for ob, pr in zip(option_blocks, prompts):
            parsed_pages.append({'page': p_idx+1, 'prompt': pr, 'opts': ob['opts'], 'override': ob.get('correct_override')})

print(f"Total parsed items: {len(parsed_pages)}")
